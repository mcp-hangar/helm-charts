#!/usr/bin/env python3
"""Assert each chart's alerts match the `job` its ServiceMonitor produces.

A PromQL equality matcher that selects nothing is still valid PromQL: it
renders, it applies, promtool passes it, and the alert simply never fires. Both
charts shipped one.

- `mcp-hangar-operator`: `MCPOperatorDown` asked for `up{job="<fullname>"}`
  while the ServiceMonitor names the job after the Service it selects, which is
  `<fullname>-metrics` (#213).
- `mcp-hangar`: three alerts, one of them `severity: critical`, match a fixed
  `job="mcp-hangar"` while the job was `<release>-mcp-hangar` -- correct only
  for a release named `mcp-hangar` (#224). That file cannot be templated:
  `.Files.Get` inserts it verbatim, so the fix is a `jobLabel` pointing at a
  literal label the chart controls, and this check is what keeps the two ends
  tied together.

Nothing else in CI can catch this. `helm lint` and kubeconform stop at the shape
of the object, and promtool only parses the expression -- a matcher selecting
nothing parses perfectly.

Two release names are rendered per chart on purpose: one collapses through the
`fullname` helper and one does not, so a matcher right for only one of them
still fails here.

Usage: scripts/check_job_labels.py <chart> [HELM]    (HELM defaults to `helm`)
"""

from __future__ import annotations

import re
import subprocess
import sys
from typing import Any

import yaml

#: chart -> release names to render. The first collapses through `fullname`,
#: the second does not.
CHARTS: dict[str, tuple[str, ...]] = {
    "mcp-hangar": ("mcp-hangar", "prod"),
    "mcp-hangar-operator": ("mcp-hangar-operator", "prod"),
}

ENABLE = ["--set", "prometheusRule.enabled=true", "--set", "serviceMonitor.enabled=true"]

# The templates refuse to render without the Prometheus Operator CRDs, which is
# correct behaviour and would otherwise make this check need a cluster.
API_VERSIONS = ["--api-versions", "monitoring.coreos.com/v1"]

_JOB = re.compile(r'job\s*=\s*"([^"]*)"')


def _render(helm: str, chart: str, release: str) -> str:
    result = subprocess.run(
        [helm, "template", release, chart, *ENABLE, *API_VERSIONS],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"{release}: did not render: {result.stderr.strip()}")
    return result.stdout


def _job_from_servicemonitor(docs: list[dict[str, Any]]) -> str:
    """The `job` label Prometheus Operator gives the scraped series.

    With no `jobLabel`, it is the name of the Service the monitor selects. With
    one, it is the value of that label on the Service -- and a `jobLabel` naming
    a label the Service does not carry silently falls back, so that is an error
    here rather than a guess.
    """
    monitors = [d for d in docs if d.get("kind") == "ServiceMonitor"]
    if len(monitors) != 1:
        raise AssertionError(f"expected exactly one ServiceMonitor, rendered {len(monitors)}")
    monitor = monitors[0]

    selector = (monitor["spec"].get("selector") or {}).get("matchLabels") or {}
    if not selector:
        raise AssertionError("the ServiceMonitor selects by no labels at all")

    selected = [
        d
        for d in docs
        if d.get("kind") == "Service"
        and all((d["metadata"].get("labels") or {}).get(k) == v for k, v in selector.items())
    ]
    if len(selected) != 1:
        names = ", ".join(sorted(d["metadata"]["name"] for d in selected)) or "none"
        raise AssertionError(
            f"the ServiceMonitor's selector matches {len(selected)} Services ({names}); "
            "it must match exactly one, or the job label is whichever Prometheus scrapes"
        )
    service = selected[0]

    job_label = monitor["spec"].get("jobLabel")
    if not job_label:
        return str(service["metadata"]["name"])

    value = (service["metadata"].get("labels") or {}).get(job_label)
    if not value:
        raise AssertionError(f"jobLabel {job_label!r} names a label {service['metadata']['name']} does not carry")
    return str(value)


def _job_matchers(docs: list[dict[str, Any]]) -> set[str]:
    """Every `job="..."` an alert expression matches on."""
    rules = [d for d in docs if d.get("kind") == "PrometheusRule"]
    if len(rules) != 1:
        raise AssertionError(f"expected exactly one PrometheusRule, rendered {len(rules)}")

    matchers: set[str] = set()
    for group in rules[0]["spec"].get("groups") or []:
        for rule in group.get("rules") or []:
            matchers.update(_JOB.findall(rule.get("expr", "")))
    if not matchers:
        raise AssertionError("no alert matches on a job label; this check would assert nothing")
    return matchers


def _self_check() -> list[str]:
    """Prove the comparison bites, so a green run is not a vacuous one."""
    docs = [
        {"kind": "ServiceMonitor", "metadata": {"name": "m"}, "spec": {"selector": {"matchLabels": {"a": "b"}}}},
        {"kind": "Service", "metadata": {"name": "svc-metrics", "labels": {"a": "b"}}},
        {
            "kind": "PrometheusRule",
            "metadata": {"name": "r"},
            "spec": {"groups": [{"name": "g", "rules": [{"alert": "X", "expr": 'up{job="svc"} == 0'}]}]},
        },
    ]
    job = _job_from_servicemonitor(docs)
    matchers = _job_matchers(docs)
    if job == "svc-metrics" and matchers == {"svc"} and matchers != {job}:
        print("ok  self-check: a mismatched pair is detected")
        return []
    return [f"self-check did not detect a mismatched pair: job={job!r}, matchers={matchers!r}"]


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in CHARTS:
        print(f"usage: {sys.argv[0]} <{'|'.join(CHARTS)}> [HELM]", file=sys.stderr)
        return 2
    chart = sys.argv[1]
    helm = sys.argv[2] if len(sys.argv) > 2 else "helm"
    failures: list[str] = _self_check()

    for release in CHARTS[chart]:
        try:
            docs = [d for d in yaml.safe_load_all(_render(helm, chart, release)) if d]
            job = _job_from_servicemonitor(docs)
            matchers = _job_matchers(docs)
        except AssertionError as exc:
            failures.append(f"{chart}/{release}: {exc}")
            continue

        wrong = sorted(m for m in matchers if m != job)
        if wrong:
            failures.append(
                f"{chart}/{release}: the ServiceMonitor produces job={job!r}, "
                f"but alerts match on {wrong} -- those alerts select nothing and cannot fire"
            )
        else:
            print(f"ok  {chart}/{release}: alerts and ServiceMonitor agree on job={job!r}")

    for failure in failures:
        print(f"::error::{failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
