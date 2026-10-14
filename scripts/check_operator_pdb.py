#!/usr/bin/env python3
"""Assert the operator chart's PodDisruptionBudget never blocks a node drain it was not asked to.

A budget of `minAvailable: 1` over a single pod can never be satisfied, so
`kubectl drain` waits on it for ever. That was the chart's default: one replica,
`Recreate`, and a budget of `minAvailable: 1` (#316). Nothing else in CI can see
it. `helm lint` and kubeconform check the shape of the object, and the install
smoke never drains a node.

This reads the budget back out of the render and checks the relation between it
and the replica count: how many pods it lets a drain take must be at least one.
It renders the defaults at one, two and three replicas, and the two ways a
release overrides them -- `minAvailable` alone, and the budget off -- because
the API server also refuses a budget that sets both fields, which a chart
default for one and a release value for the other would produce.

Usage: scripts/check_operator_pdb.py [HELM]    (HELM defaults to `helm`)
"""

from __future__ import annotations

import subprocess
import sys
from typing import Any

import yaml

CHART = "mcp-hangar-operator"


def render(helm: str, *sets: str) -> list[dict[str, Any]]:
    args = [helm, "template", "t", CHART]
    for item in sets:
        args += ["--set", item]
    out = subprocess.run(args, check=True, capture_output=True, text=True).stdout
    return [doc for doc in yaml.safe_load_all(out) if doc]


def budget(docs: list[dict[str, Any]]) -> dict[str, Any] | None:
    found = [doc for doc in docs if doc.get("kind") == "PodDisruptionBudget"]
    assert len(found) <= 1, "more than one PodDisruptionBudget rendered"
    return found[0]["spec"] if found else None


def drain_allows(spec: dict[str, Any], replicas: int) -> int:
    """How many of *replicas* pods a drain may take at once, per the PDB's own arithmetic."""
    if "minAvailable" in spec:
        return replicas - int(spec["minAvailable"])
    if "maxUnavailable" in spec:
        return int(spec["maxUnavailable"])
    return replicas


def main(helm: str) -> int:
    failures: list[str] = []

    for replicas in (1, 2, 3):
        spec = budget(render(helm, f"replicaCount={replicas}"))
        if spec is None:
            continue
        if "minAvailable" in spec and "maxUnavailable" in spec:
            failures.append(f"replicaCount={replicas}: the budget sets both minAvailable and maxUnavailable")
        elif drain_allows(spec, replicas) < 1:
            failures.append(f"replicaCount={replicas}: the default budget {spec} lets a drain take no pod")

    chosen = budget(render(helm, "podDisruptionBudget.minAvailable=1", "replicaCount=3"))
    if chosen != {"minAvailable": 1, "selector": chosen["selector"] if chosen else None}:
        failures.append(f"a release that sets minAvailable gets {chosen}, not minAvailable alone")

    if budget(render(helm, "podDisruptionBudget.enabled=false")) is not None:
        failures.append("podDisruptionBudget.enabled=false still renders a budget")

    for failure in failures:
        print(f"::error::{failure}")
    if not failures:
        print("operator PodDisruptionBudget: a drain can take a pod at 1, 2 and 3 replicas; minAvailable overrides cleanly")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "helm"))
