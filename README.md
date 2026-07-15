# MCP Hangar Helm Charts

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Helm](https://img.shields.io/badge/Helm-v3-blue.svg)](https://helm.sh)

**Helm charts for deploying the MCP Hangar ecosystem on Kubernetes.**

This repository contains official Helm charts for MCP Hangar.

## Charts

- **mcp-hangar** — Core MCP Hangar server (app chart, version 0.12.0, appVersion 0.12.0)
- **mcp-hangar-operator** — Kubernetes operator for MCP provider lifecycle management (version 0.12.0)
- **hangar-agent** — Agent deployed in Kubernetes clusters, connects to control plane via gRPC (version 0.1.0)

## Prerequisites

- Kubernetes 1.25+
- Helm 3.x

## Quick Start

Install the charts directly from the GHCR OCI registry.

```bash
# Add namespace
kubectl create namespace mcp-hangar

# Install core server
helm install mcp-hangar oci://ghcr.io/mcp-hangar/charts/mcp-hangar \
  --version 0.12.0 \
  --namespace mcp-hangar

# Install operator
helm install mcp-hangar-operator oci://ghcr.io/mcp-hangar/charts/mcp-hangar-operator \
  --version 0.12.0 \
  --namespace mcp-hangar

# Install agent
helm install hangar-agent oci://ghcr.io/mcp-hangar/charts/hangar-agent \
  --version 0.1.0 \
  --namespace mcp-hangar
```

## Install from Source

```bash
git clone https://github.com/mcp-hangar/helm-charts.git
cd helm-charts

helm install mcp-hangar ./mcp-hangar -n mcp-hangar
helm install mcp-hangar-operator ./mcp-hangar-operator -n mcp-hangar
helm install hangar-agent ./hangar-agent -n mcp-hangar
```

## Chart Overview

### mcp-hangar

The core application chart for the MCP Hangar server.

Key configuration options in `values.yaml`:
- `replicaCount`: Number of server instances.
- `image`: Container image repository and tag.
- `config.providers`: Configuration for MCP providers.
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

### hangar-agent

The agent connects remote Kubernetes clusters to the control plane.

Key configuration options in `values.yaml`:
- `agent.cloudAddr`: Address of the MCP Hangar control plane.
- `agent.licenseKey`: Required license key for agent authentication.
- `persistence`: Storage configuration for agent state.
- `tlsEnabled`: Enable TLS for gRPC communication.
- `WAL`: Write-ahead logging configuration for persistence.

## Development

Use these commands for local development and testing.

### Linting

```bash
helm lint mcp-hangar
helm lint mcp-hangar-operator
helm lint hangar-agent
```

### Rendering Templates

```bash
helm template mcp-hangar ./mcp-hangar
helm template mcp-hangar-operator ./mcp-hangar-operator
helm template hangar-agent ./hangar-agent
```

### Packaging

```bash
helm package mcp-hangar
helm package mcp-hangar-operator
helm package hangar-agent
```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

[Docs](https://mcp-hangar.io) | [GitHub](https://github.com/mcp-hangar/helm-charts)
