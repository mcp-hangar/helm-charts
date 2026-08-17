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

## Helm versions

Helm 3 and Helm 4 are both supported and CI-tested (install, upgrade,
rollback under each major, plus the helm3-install → helm4-upgrade cross
path). Because this chart ships its CRDs as templates, the apply model
matters: a Helm 4 fresh install manages them with server-side apply, so a
plain out-of-band `kubectl apply --server-side` to a helm-owned CRD field is
refused by the apiserver (`conflict with "helm"`), and if the other writer
forces the conflict, the next `helm upgrade` fails with an explicit conflict
error naming that manager rather than silently taking the field back —
`helm upgrade --force-conflicts` reclaims it. A release created by Helm 3
keeps client-side apply (no such protection) until you opt in with
`helm upgrade --server-side=true`. Details and the pinned versions: the repo
[README](../README.md#helm-versions).
