# MCP Hangar Helm Charts

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Helm](https://img.shields.io/badge/Helm-v3-blue.svg)](https://helm.sh)

**Helm charts for deploying the MCP Hangar ecosystem on Kubernetes.**

This repository contains official Helm charts for MCP Hangar.

## Charts

- **mcp-hangar** — Core MCP Hangar server (chart `0.13.2`, appVersion `1.5.0`)
- **mcp-hangar-operator** — Kubernetes operator for MCP provider lifecycle management (chart `0.12.1`, appVersion `0.12.2`)

Versions above are the current published charts. See [RELEASE.md](RELEASE.md) for
how charts are versioned and published, and the
[compatibility matrix](https://github.com/mcp-hangar/docs/blob/main/operations/RELEASE_COMPATIBILITY.md)
for supported combinations and verified digests.

## Prerequisites

- Kubernetes 1.25+
- Helm 3.x

## Quick Start

Install the charts directly from the GHCR OCI registry.

```bash
# Add namespace
kubectl create namespace mcp-hangar

# Install core server.
# The 1.5 server refuses to bind a non-loopback interface without auth. For a
# quick/insecure demo, opt in with config.unsafeNoAuth=true; for anything real,
# configure the `auth` block instead (see the chart's values.yaml).
helm install mcp-hangar oci://ghcr.io/mcp-hangar/charts/mcp-hangar \
  --version 0.13.2 \
  --namespace mcp-hangar \
  --set config.unsafeNoAuth=true

# Install operator
helm install mcp-hangar-operator oci://ghcr.io/mcp-hangar/charts/mcp-hangar-operator \
  --version 0.12.1 \
  --namespace mcp-hangar
```

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
- `config.mcp_servers`: Backend MCP servers the gateway fronts.
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
