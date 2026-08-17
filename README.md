# MCP Hangar Helm Charts

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)
[![Helm](https://img.shields.io/badge/Helm-v3%20%7C%20v4-0F1689?logo=helm&logoColor=white)](https://helm.sh)
[![mcp-hangar](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmcp-hangar%2Fhelm-charts%2Fmain%2Fmcp-hangar%2FChart.yaml&query=%24.version&label=mcp-hangar&prefix=v&logo=helm&logoColor=white&color=0F1689)](https://github.com/mcp-hangar/helm-charts/releases?q=mcp-hangar-v&expanded=true)
[![mcp-hangar-operator](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmcp-hangar%2Fhelm-charts%2Fmain%2Fmcp-hangar-operator%2FChart.yaml&query=%24.version&label=mcp-hangar--operator&prefix=v&logo=helm&logoColor=white&color=0F1689)](https://github.com/mcp-hangar/helm-charts/releases?q=mcp-hangar-operator-v&expanded=true)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/mcp-hangar)](https://artifacthub.io/packages/search?repo=mcp-hangar)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/mcp-hangar-operator)](https://artifacthub.io/packages/search?repo=mcp-hangar-operator)

**Helm charts for deploying the MCP Hangar ecosystem on Kubernetes.**

This repository contains official Helm charts for MCP Hangar.

## Charts

- **mcp-hangar** — Core MCP Hangar server
- **mcp-hangar-operator** — Kubernetes operator for MCP provider lifecycle management

Both charts are also listed on
[Artifact Hub](https://artifacthub.io/packages/search?ts_query_web=mcp-hangar&kind=0)
(verified publisher; the listing is claimed via `artifacthub/` +
the `artifacthub-metadata` workflow). GHCR stays the publish target and the
source of truth — Artifact Hub only indexes it.

For current chart and appVersion numbers, see the
[releases page](https://github.com/mcp-hangar/helm-charts/releases) and the
[compatibility matrix](https://github.com/mcp-hangar/docs/blob/main/operations/RELEASE_COMPATIBILITY.md),
which are the source of truth for supported combinations and verified digests.
See [RELEASE.md](RELEASE.md) for how charts are versioned and published.

## Prerequisites

- Kubernetes 1.25+
- Helm 3.x or 4.x (see [Helm versions](#helm-versions))

## Helm versions

Both Helm 3 and Helm 4 are supported and CI-tested on every PR (currently
pinned at v3.21.4 and v4.2.4; the pins in `.github/workflows/ci-charts.yml`
are the source of truth). CI asserts lint/render under both majors, an
identical rendered output across them, the full install → test → upgrade →
rollback lifecycle under each, and the cross path: installed by Helm 3,
upgraded by Helm 4.

What the majors do differently, as observed by those CI assertions:

- **One release = one apply model.** A fresh Helm 4 install uses server-side
  apply (SSA); a release created by Helm 3 keeps client-side apply across
  Helm 4 upgrades until you opt in with `helm upgrade --server-side=true`
  (the flag takes a value). Don't mix majors on the same release ad hoc.
- **SSA turns silent overwrites into explicit conflicts** — relevant here
  because the operator chart ships its CRDs as templates. On an SSA-installed
  release, a plain out-of-band `kubectl apply --server-side` to a helm-owned
  field is refused by the apiserver (`conflict with "helm"`). If the other
  writer forces the conflict and takes the field, the next `helm upgrade`
  fails with an explicit conflict error naming the competing manager — it
  does **not** silently take the field back; `helm upgrade --force-conflicts`
  is the documented way to reclaim it. A Helm-3-created (client-side) release
  has none of this protection: the same out-of-band write goes through
  silently.
- **`--wait` and `helm test` are stricter under Helm 4** (kstatus judges real
  readiness — probes and conditions, not the Helm 3 pod-status heuristic). A
  deploy that "passed" under Helm 3 and fails under 4 is the check getting
  honest, not the chart regressing. One concrete flip in the other direction:
  `helm3 test --logs` exits non-zero on a *passing* test of the mcp-hangar
  chart, because Helm 3 deletes the `hook-succeeded` test pod before fetching
  its logs; Helm 4 prints the logs first.

## Quick Start

Install the charts directly from the GHCR OCI registry.

```bash
# Add namespace
kubectl create namespace mcp-hangar

# Install the core server (latest published chart). For a quick, insecure demo
# opt in with config.unsafeNoAuth=true; the server's fail-closed auth behavior
# is documented in the core README (linked below).
helm install mcp-hangar oci://ghcr.io/mcp-hangar/charts/mcp-hangar \
  --namespace mcp-hangar \
  --set config.unsafeNoAuth=true

# Install the operator (latest published chart)
helm install mcp-hangar-operator oci://ghcr.io/mcp-hangar/charts/mcp-hangar-operator \
  --namespace mcp-hangar
```

> **Pin a version:** these commands install the latest published charts. For a
> reproducible deploy, add `--version <x.y.z>` from the
> [release compatibility matrix](https://github.com/mcp-hangar/docs/blob/main/operations/RELEASE_COMPATIBILITY.md),
> which is the single source of truth for which core, operator, and chart
> versions are released and tested together (never hardcoded here -- see
> [ADR-011](https://github.com/mcp-hangar/docs/blob/main/adr/ADR-011-single-source-of-truth-cross-repo-facts.md)).
>
> **Server auth behavior** (fail-closed on a non-loopback bind, `unsafeNoAuth`)
> is owned by the [core README](https://github.com/mcp-hangar/mcp-hangar#quickstart),
> not re-documented here.

## Install from Source

```bash
git clone https://github.com/mcp-hangar/helm-charts.git
cd helm-charts

helm install mcp-hangar ./mcp-hangar -n mcp-hangar
helm install mcp-hangar-operator ./mcp-hangar-operator -n mcp-hangar
```

## Chart Overview

### mcp-hangar

The core application chart for the MCP Hangar server.

Key configuration options in `values.yaml`:
- `replicaCount`: Number of server instances.
- `image`: Container image repository and tag.
- `mcp_servers`: Backend MCP servers the gateway fronts (top level, not under `config`).
- `config.unsafeNoAuth` / `auth`: bind without auth (demo) or configure OIDC/API-key auth.
- `service`: Service type and port configuration.
- `resources`: Pod resource requests and limits.
- `serviceMonitor`: Enable Prometheus monitoring.

### mcp-hangar-operator

The Kubernetes operator manages the lifecycle of MCP providers.

Key configuration options in `values.yaml`:
- `replicaCount`: Number of operator instances.
- `image`: Operator container image.
- `CRDs`: Manage Custom Resource Definition installation.
- `rbac`: RBAC resource creation.
- `resources`: Pod resource requests and limits.
- `metrics`: Metrics service configuration.

## Development

Use these commands for local development and testing.

### Linting

```bash
helm lint mcp-hangar
helm lint mcp-hangar-operator
```

### Rendering Templates

```bash
helm template mcp-hangar ./mcp-hangar
helm template mcp-hangar-operator ./mcp-hangar-operator
```

### Packaging

```bash
helm package mcp-hangar
helm package mcp-hangar-operator
```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

[Docs](https://mcp-hangar.io) | [GitHub](https://github.com/mcp-hangar/helm-charts)
