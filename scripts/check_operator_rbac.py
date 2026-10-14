#!/usr/bin/env python3
"""Assert the operator chart's ClusterRole is the operator's own role, and nothing wider (#315).

The chart renders its rules from `files/rbac/`, vendored from the operator's
generated `config/rbac/role.yaml`. vendor-operator-crds.py --check keeps those
files equal to the operator at the appVersion; this reads the render back and
checks the relation the template is responsible for: every rule of the operator
reaches the ClusterRole, the chart adds none of its own, and the three switches
(Cilium, secure metrics, leader election) remove exactly their rules.

Usage: scripts/check_operator_rbac.py [HELM]    (HELM defaults to `helm`)
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
from typing import Any

import yaml

CHART = "mcp-hangar-operator"
FILES = Path(CHART) / "files" / "rbac"
CILIUM = "cilium.io"
REVIEWS = {"authentication.k8s.io", "authorization.k8s.io"}


def rules_of(helm: str, *sets: str) -> list[dict[str, Any]]:
    args = [helm, "template", "t", CHART]
    for item in sets:
        args += ["--set", item]
    out = subprocess.run(args, check=True, capture_output=True, text=True).stdout
    roles = [d for d in yaml.safe_load_all(out) if d and d.get("kind") == "ClusterRole" and d["metadata"]["name"] == "t-mcp-hangar-operator"]
    assert len(roles) == 1, f"expected one manager ClusterRole, got {len(roles)}"
    return roles[0]["rules"]


def key(rule: dict[str, Any]) -> str:
    return yaml.safe_dump(rule, sort_keys=True)


def vendored(name: str) -> list[dict[str, Any]]:
    return yaml.safe_load((FILES / name).read_text(encoding="utf-8"))["rules"]


def main(helm: str) -> int:
    failures: list[str] = []
    role, lock = vendored("role.yaml"), vendored("leader_election_role.yaml")
    known = {key(r) for r in role + lock}

    got = rules_of(helm)
    keys = {key(r) for r in got}
    for rule in role + lock:
        if key(rule) not in keys:
            failures.append(f"the operator's rule is missing from the ClusterRole: {rule}")
    for rule in got:
        if key(rule) not in known:
            failures.append(f"the ClusterRole grants a rule the operator does not declare: {rule}")

    def groups(rules: list[dict[str, Any]]) -> set[str]:
        return {g for r in rules for g in r["apiGroups"]}

    if CILIUM in groups(rules_of(helm, "rbac.ciliumNetworkPolicies=false")):
        failures.append("rbac.ciliumNetworkPolicies=false still grants cilium.io")
    if groups(rules_of(helm, "operator.metrics.secure=false")) & REVIEWS:
        failures.append("operator.metrics.secure=false still grants token and access reviews")
    no_lock = {key(r) for r in rules_of(helm, "operator.leaderElection.enabled=false")}
    lock_only = [r for r in lock if key(r) not in {key(x) for x in role}]
    for rule in lock_only:
        if key(rule) in no_lock:
            failures.append(f"operator.leaderElection.enabled=false still grants the lock rule {rule}")

    pods = [r for r in got if "pods" in r["resources"] and r["apiGroups"] == [""]]
    if any(set(r["verbs"]) & {"create", "patch", "update"} for r in pods):
        failures.append("pods carry a write verb the operator's markers do not declare")
    leases = [r for r in got if r["resources"] == ["leases"]]
    if not any("delete" in r["verbs"] for r in leases):
        failures.append("leases has no delete verb: registration cannot remove its claim")

    for failure in failures:
        print(f"::error::{failure}")
    if not failures:
        print("operator ClusterRole: equals the vendored operator rules; Cilium, metrics review and lock rules follow their switches")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "helm"))
