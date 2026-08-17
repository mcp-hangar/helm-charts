# MCP-Hangar Operator Helm Chart

Helm chart for deploying the MCP-Hangar Kubernetes operator: the controller
behind the `MCPServer`, `MCPServerGroup`, `MCPDiscoverySource` and
`MCPEgressPolicy` CRDs.

## Installation

```bash
helm install mcp-hangar-operator oci://ghcr.io/mcp-hangar/charts/mcp-hangar-operator
```

## Configuration

See `values.yaml` for all available options.

CRDs are installed as chart templates (release-owned, upgradeable), gated by
`crds.install`. `crds.keep: true` adds `helm.sh/resource-policy: keep` so an
uninstall leaves the CRDs -- and every CR of yours they define -- in place.

Webhooks are off by default; enabling them requires cert-manager
(`webhook.certManager.enabled`).
