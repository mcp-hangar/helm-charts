#!/usr/bin/env python3
"""Assert the mcp-hangar chart gives core's graceful shutdown room to finish.

The kubelet counts a pod's terminationGracePeriodSeconds from the start of its
preStop hook, and kills the pod when the period ends. Core waits up to
`http.graceful_shutdown_timeout_s` for the requests in flight only after the
hook returns. So every pod the chart renders must satisfy

    terminationGracePeriodSeconds > preStop sleep + graceful_shutdown_timeout_s

(mcp-hangar/mcp-hangar#1447). This renders the chart, reads the three numbers
back out of the rendered Deployment and ConfigMap rather than out of values,
and checks the rule on every shape in RENDERS. Then it checks that each shape
in REFUSED, which would break the rule or carry a bad value, fails to render.

Usage: scripts/check_shutdown_ordering.py [HELM]    (HELM defaults to `helm`)
"""

from __future__ import annotations

import subprocess
import sys

import yaml

CHART = "mcp-hangar"

# In force when the pod spec names no grace period.
KUBERNETES_DEFAULT_GRACE = 30

# The first core that reads http.graceful_shutdown_timeout_s, and the last that
# does not. Keep NEW_CORE in step with the guard in templates/_shutdown.tpl.
NEW_CORE = "image.tag=2.20.0"
OLD_CORE = "image.tag=2.19.1"

BOUND = "shutdown.gracefulTimeoutSeconds"
PRE_STOP = "shutdown.preStopSleepSeconds"
GRACE = "shutdown.terminationGracePeriodSeconds"

# name -> (helm args, the rendered (terminationGracePeriodSeconds, preStop sleep, bound)).
# A grace period of None is one the chart does not render: Kubernetes' default.
RENDERS: dict[str, tuple[list[str], tuple[int | None, int, int | None]]] = {
    "defaults": ([], (None, 5, None)),
    "ci-values.yaml": (["-f", f"{CHART}/ci-values.yaml"], (None, 5, None)),
    "ci-cluster-values.yaml": (["-f", f"{CHART}/ci-cluster-values.yaml"], (None, 5, None)),
    "a bound computes the grace period": (["--set", NEW_CORE, "--set", f"{BOUND}=90"], (105, 5, 90)),
    # --set-json hands the template a float64, the kind a values file gives it.
    "a bound from JSON": (["--set", NEW_CORE, "--set-json", f"{BOUND}=90"], (105, 5, 90)),
    "a bound with a longer grace period set": (
        ["--set", NEW_CORE, "--set", f"{BOUND}=90", "--set", f"{GRACE}=120"],
        (120, 5, 90),
    ),
    "no preStop": (["--set", f"{PRE_STOP}=0"], (None, 0, None)),
    "no preStop and a bound": (["--set", NEW_CORE, "--set", f"{PRE_STOP}=0", "--set", f"{BOUND}=20"], (30, 0, 20)),
    "a long preStop with a grace period to hold it": (
        ["--set", f"{PRE_STOP}=40", "--set", f"{GRACE}=60"],
        (60, 40, None),
    ),
}

# name -> (helm args, a phrase the failed render must say).
REFUSED: dict[str, tuple[list[str], str]] = {
    "a grace period no longer than preStop + bound": (
        ["--set", NEW_CORE, "--set", f"{BOUND}=90", "--set", f"{GRACE}=95"],
        "must be longer than",
    ),
    "a preStop that outlasts Kubernetes' default grace period": (["--set", f"{PRE_STOP}=30"], "must be longer than"),
    "a preStop that outlasts the grace period set": (
        ["--set", f"{PRE_STOP}=40", "--set", f"{GRACE}=40"],
        "must be longer than",
    ),
    "a zero bound": (["--set", NEW_CORE, "--set", f"{BOUND}=0"], "whole number of seconds"),
    "a fractional bound": (["--set", NEW_CORE, "--set-json", f"{BOUND}=1.5"], "whole number of seconds"),
    "a bound as a string": (["--set", NEW_CORE, "--set-string", f"{BOUND}=90"], "whole number of seconds"),
    "a negative preStop": (["--set", f"{PRE_STOP}=-1"], "whole number of seconds"),
    "a zero grace period": (["--set", f"{GRACE}=0"], "whole number of seconds"),
    "a bound on a core that does not read it": (["--set", OLD_CORE, "--set", f"{BOUND}=90"], "needs core 2.20.0"),
}


def _render(helm: str, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([helm, "template", "t", CHART, *args], capture_output=True, text=True, check=False)


def _rendered_shutdown(manifest: str) -> tuple[int | None, int, int | None]:
    """(terminationGracePeriodSeconds, preStop sleep, bound), as rendered."""
    docs = [doc for doc in yaml.safe_load_all(manifest) if doc]
    [deployment] = [doc for doc in docs if doc["kind"] == "Deployment"]
    [configmap] = [doc for doc in docs if doc["kind"] == "ConfigMap" and "config.yaml" in (doc.get("data") or {})]

    pod = deployment["spec"]["template"]["spec"]
    [container] = [c for c in pod["containers"] if c["name"] == CHART]
    command = (((container.get("lifecycle") or {}).get("preStop") or {}).get("exec") or {}).get("command")
    sleep = 0
    if command is not None:
        if len(command) != 2 or command[0] != "sleep":
            raise AssertionError(f"the preStop hook is not a plain sleep: {command}")
        sleep = int(command[1])

    core = yaml.safe_load(configmap["data"]["config.yaml"])
    bound = (core.get("http") or {}).get("graceful_shutdown_timeout_s")
    return pod.get("terminationGracePeriodSeconds"), sleep, bound


def main() -> int:
    helm = sys.argv[1] if len(sys.argv) > 1 else "helm"
    failures: list[str] = []

    for name, (args, expected) in RENDERS.items():
        result = _render(helm, args)
        if result.returncode != 0:
            failures.append(f"{name}: did not render: {result.stderr.strip()}")
            continue
        got = _rendered_shutdown(result.stdout)
        grace, sleep, bound = got
        in_force = KUBERNETES_DEFAULT_GRACE if grace is None else grace
        if in_force <= sleep + (bound or 0):
            failures.append(f"{name}: grace period {in_force} s is not longer than preStop {sleep} s + bound {bound} s")
        elif got != expected:
            failures.append(f"{name}: rendered (grace, preStop, bound) = {got}, expected {expected}")
        else:
            print(f"ok  {name}: (grace, preStop, bound) = {got}")

    for name, (args, phrase) in REFUSED.items():
        result = _render(helm, args)
        if result.returncode == 0:
            failures.append(f"{name}: rendered, and it must fail")
        elif phrase not in result.stderr:
            failures.append(f"{name}: failed without saying {phrase!r}: {result.stderr.strip()}")
        else:
            print(f"ok  {name}: refused")

    for failure in failures:
        print(f"::error::{failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
