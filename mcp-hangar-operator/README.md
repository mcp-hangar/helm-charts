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

The operator's two annotation-gated MCPServer rules ship as
ValidatingAdmissionPolicies (`admissionPolicies.enabled`, default `true`, chart
0.12.38 and operator 0.17.22 on): wildcard egress needs
`hangar.io/allow-unrestricted-egress: "true"`, and an image that is not
digest-pinned is handled per `operator.imageDigestPolicy` (`warn` by default,
`block`, `off`). The apiserver enforces them, so they hold without the
webhooks. `admissionPolicies.namespaceSelector` limits them to some namespaces.
Since chart 0.12.40 (operator 0.17.24) they are the only enforcement: the
webhook dropped its copies, so `admissionPolicies.enabled=false` leaves neither
rule in place.

Since operator 0.17.26 (chart 0.12.42) a `mode: remote` MCPServer whose name
core does not hold is registered with core and removed from it with the CR.
The operator records each registration as a Lease `mcp-server-<name>` in its own
namespace. Core 2.27.0 or newer must trust the endpoint's network
(`ssrf.trusted_networks`, set through the core chart's `extraConfig`). With auth
on, the key in `hangar.apiKey` needs `mcp_servers:write` and
`mcp_servers:lifecycle`, which `provider-admin` lacks.

Webhooks are off by default. With `webhook.enabled=true` the serving
certificate comes from cert-manager (`webhook.certManager.enabled`, default
`true`), or, with that off, from your own `kubernetes.io/tls` Secret
(`webhook.existingSecret`) plus the base64 PEM of its CA (`webhook.caBundle`).
The render fails if either is missing.

## Metrics

Since chart 0.12.26 (operator 0.17.10) `/metrics` is served over HTTPS with a
self-signed certificate and admits only a bearer token the API server
authenticates and authorizes for `get` on the `/metrics` URL
(`operator.metrics.secure`, default `true`). On upgrade:

- The bundled ServiceMonitor scrapes `https` with Prometheus's own
  ServiceAccount token and skips certificate verification.
- Bind the scraping ServiceAccount to the chart's `<release>-metrics-reader`
  ClusterRole with `operator.metrics.readers`, e.g.
  `[{name: prometheus-k8s, namespace: monitoring}]`. An unbound scraper gets
  `403`; the metrics are still produced, just unread.
- `networkPolicy.metricsFrom` narrows the metrics port to given peers, such as
  your monitoring namespace. It is open to any pod by default.
- `operator.metrics.secure: false` restores plain, unauthenticated HTTP.

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

### Opt-in provider ingress isolation

The draft implementation tracked by [operator #327](https://github.com/mcp-hangar/mcp-hangar-operator/issues/327)
adds a gateway-only ingress fence for container MCPServers. Use a stable operator
image containing that feature before configuring `providerIngress`; the chart's
current `appVersion` is not evidence that these unreleased flags are supported.

Set `providerIngress.gatewayNamespace` to the actual gateway namespace and
`hangar.gatewaySelector` to its pod labels (the operator default applies when
empty). Set `providerIngress.enabled=true` for global opt-in, or leave it false
and annotate individual MCPServers with `mcp-hangar.io/provider-ingress: "true"`.
An explicit `"false"` opts a server out and removes its owned ingress policy.
The namespace and pod selectors are combined; matching labels elsewhere do not
grant access. Remote targets have no provider pod to fence.

The first release stays opt-in. Verify gateway allow, non-gateway deny and health
probes on the actual CNI. `ProviderIngressApplied` reports the fence separately
from egress; other NetworkPolicies can widen ingress through additive allow
rules. The canonical boundaries and acceptance live in the
[ADR register](https://github.com/mcp-hangar/docs/blob/main/adr/README.md).
