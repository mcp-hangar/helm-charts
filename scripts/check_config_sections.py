#!/usr/bin/env python3
"""Assert the mcp-hangar chart can reach core's process-wide config sections.

`tool_access`, `execution` and `config_reload` had no path into the rendered
config.yaml at all, so running the gateway in front_door mode meant editing the
ConfigMap by hand and losing it on the next upgrade (mcp-hangar/helm-charts#216).

This renders the chart and reads the sections back out of the ConfigMap rather
than out of values, so it checks what a cluster would receive. Then it checks
that every shape which core would refuse at boot -- an unknown mode, a key too
new for the image, a required server that is not configured, a partial tenant
budget, a removed key, an extraConfig section the chart also templates -- fails
to render instead.

Usage: scripts/check_config_sections.py [HELM]    (HELM defaults to `helm`)
"""

from __future__ import annotations

import subprocess
import sys

import yaml

CHART = "mcp-hangar"

# The first core that reads required_catalogue and tenant_limits, and the last
# that does not. Keep NEW_CORE in step with the guards in templates/_config.tpl.
NEW_CORE = "image.tag=2.21.0"
OLD_CORE = "image.tag=2.20.0"

SERVERS = 'mcp_servers={"math":{"mode":"remote","endpoint":"http://m:8000/mcp"}}'
GROUP = (
    'mcp_servers={"pool":{"mode":"group","members":[{"id":"inline-a","mode":"remote",'
    '"endpoint":"http://a:8000/mcp"}]}}'
)
BUDGET = 'execution.tenantLimits={"acme":{"maxConcurrency":8,"rps":5,"burst":10}}'

# name -> (helm args, the config.yaml sections that must come out of it).
RENDERS: dict[str, tuple[list[str], dict[str, object]]] = {
    "defaults render none of them": ([], {}),
    "ci-values.yaml renders none of them": (["-f", f"{CHART}/ci-values.yaml"], {}),
    "ci-cluster-values.yaml renders none of them": (["-f", f"{CHART}/ci-cluster-values.yaml"], {}),
    "the front door, on its own": (
        ["--set", "toolAccess.mode=front_door"],
        {"tool_access": {"mode": "front_door"}},
    ),
    "egress is still expressible": (
        ["--set", "toolAccess.mode=egress"],
        {"tool_access": {"mode": "egress"}},
    ),
    "a required catalogue": (
        ["--set", NEW_CORE, "--set", "toolAccess.mode=front_door", "--set-json", SERVERS,
         "--set-json", 'toolAccess.requiredCatalogue.servers=["math"]',
         "--set", "toolAccess.requiredCatalogue.retryForSeconds=600"],
        {"tool_access": {"mode": "front_door", "required_catalogue": {"servers": ["math"], "retry_for_s": 600}}},
    ),
    # A group member defined only inline is a server the loader builds, so the
    # catalogue may name it and the render must not object.
    "a required catalogue naming an inline group member": (
        ["--set", NEW_CORE, "--set-json", GROUP, "--set-json", 'toolAccess.requiredCatalogue.servers=["inline-a"]'],
        {"tool_access": {"required_catalogue": {"servers": ["inline-a"]}}},
    ),
    "per-tenant budgets": (
        ["--set", NEW_CORE, "--set-json", BUDGET],
        {"execution": {"tenant_limits": {"acme": {"max_concurrency": 8, "rps": 5, "burst": 10}}}},
    ),
    "the gateway-wide execution limits, which need no new core": (
        ["--set", OLD_CORE, "--set", "execution.maxConcurrency=64",
         "--set", "execution.defaultMcpServerConcurrency=8"],
        {"execution": {"max_concurrency": 64, "default_mcp_server_concurrency": 8}},
    ),
    "config reload": (
        ["--set", "configReload.enabled=true", "--set", "configReload.intervalSeconds=30",
         "--set", "configReload.useWatchdog=false"],
        {"config_reload": {"enabled": True, "interval_s": 30, "use_watchdog": False}},
    ),
    # enabled=false is a setting, not an absent one: it must render.
    "config reload turned off explicitly": (
        ["--set", "configReload.enabled=false"],
        {"config_reload": {"enabled": False}},
    ),
    "extraConfig reaches a section the chart does not template": (
        ["--set-json", 'extraConfig={"headers":{"param_validation":{"required":true}}}'],
        {"headers": {"param_validation": {"required": True}}},
    ),
    "the front door end to end": (
        ["--set", NEW_CORE, "--set", "toolAccess.mode=front_door", "--set-json", SERVERS,
         "--set-json", 'toolAccess.requiredCatalogue.servers=["math"]', "--set-json", BUDGET,
         "--set", "configReload.enabled=true"],
        {
            "tool_access": {"mode": "front_door", "required_catalogue": {"servers": ["math"]}},
            "execution": {"tenant_limits": {"acme": {"max_concurrency": 8, "rps": 5, "burst": 10}}},
            "config_reload": {"enabled": True},
        },
    ),
}

# name -> (helm args, a phrase the failed render must say).
REFUSED: dict[str, tuple[list[str], str]] = {
    "a misspelt mode": (["--set", "toolAccess.mode=front-door"], 'it must be "egress" or "front_door"'),
    "a required catalogue on a core that does not read it": (
        ["--set", OLD_CORE, "--set-json", SERVERS, "--set-json", 'toolAccess.requiredCatalogue.servers=["math"]'],
        "needs core 2.21.0",
    ),
    "a required catalogue naming a server that is not configured": (
        ["--set", NEW_CORE, "--set-json", SERVERS, "--set-json", 'toolAccess.requiredCatalogue.servers=["typo"]'],
        "which this release's\nmcp_servers does not build",
    ),
    "tenant budgets on a core that does not read them": (
        ["--set", OLD_CORE, "--set-json", BUDGET],
        "needs core 2.21.0",
    ),
    "a tenant budget missing a key": (
        ["--set", NEW_CORE, "--set-json", 'execution.tenantLimits={"acme":{"maxConcurrency":8,"rps":5}}'],
        "must set maxConcurrency, rps and burst",
    ),
    "extraConfig writing a section the chart templates": (
        ["--set-json", 'extraConfig={"auth":{"enabled":true}}'],
        "which this chart templates itself",
    ),
    # Removed in core 2.20.0. mcp_servers is a passthrough, so this is the one
    # removed key that can still be written through the chart.
    "a group's removed circuit reset timeout": (
        ["--set-json", 'mcp_servers={"pool":{"mode":"group","circuit_breaker":{"reset_timeout_s":30}}}'],
        "which core removed in 2.20.0",
    ),
    "the same key in its flat spelling": (
        ["--set-json", 'mcp_servers={"pool":{"mode":"group","circuit_reset_timeout_s":30}}'],
        "which core removed in 2.20.0",
    ),
}

# Sections that must never come out of the chart, whatever is set: core removed
# them, and a chart that can still write one is a gateway that will not start.
NEVER_RENDERED = {"tool_access": "rules"}


def _render(helm: str, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([helm, "template", "t", CHART, *args], capture_output=True, text=True, check=False)


def _core_config(manifest: str) -> dict[str, object]:
    docs = [doc for doc in yaml.safe_load_all(manifest) if doc]
    [configmap] = [doc for doc in docs if doc["kind"] == "ConfigMap" and "config.yaml" in (doc.get("data") or {})]
    return yaml.safe_load(configmap["data"]["config.yaml"]) or {}


def _contains(got: object, expected: object) -> bool:
    """Whether *got* carries everything *expected* names, at every depth."""
    if isinstance(expected, dict):
        return isinstance(got, dict) and all(_contains(got.get(key), value) for key, value in expected.items())
    return got == expected


def main() -> int:
    helm = sys.argv[1] if len(sys.argv) > 1 else "helm"
    failures: list[str] = []

    for name, (args, expected) in RENDERS.items():
        result = _render(helm, args)
        if result.returncode != 0:
            failures.append(f"{name}: did not render: {result.stderr.strip()}")
            continue
        config = _core_config(result.stdout)
        absent = [section for section in ("tool_access", "execution", "config_reload") if section not in expected]
        if not expected and any(section in config for section in absent):
            failures.append(f"{name}: rendered a section nothing asked for: {sorted(config)}")
        elif not _contains(config, expected):
            failures.append(f"{name}: config.yaml is {config!r}, which does not carry {expected!r}")
        else:
            for section, key in NEVER_RENDERED.items():
                if key in (config.get(section) or {}):
                    failures.append(f"{name}: rendered {section}.{key}, which core removed")
                    break
            else:
                print(f"ok  {name}")

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
