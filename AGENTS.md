# MCP Hangar Helm Charts

## Quick Reference

| Property | Value |
|----------|-------|
| Chart format | Helm v3 (apiVersion: v2) |
| Kubernetes | >= 1.25 |
| Charts | `mcp-hangar` (app), `mcp-hangar-operator` (operator) |
| Registry | `oci://ghcr.io/mcp-hangar/charts` |

## Commands

Run everything from the repository root -- this repo *is* the charts repo,
there is no `packages/` prefix.

```bash
# Lint
helm lint mcp-hangar
helm lint mcp-hangar-operator

# Template (dry-run render)
helm template my-release mcp-hangar
helm template my-release mcp-hangar-operator

# Render the shapes CI renders (see .github/workflows/ci-charts.yml)
helm template t mcp-hangar -f mcp-hangar/ci-values.yaml
helm template t mcp-hangar -f mcp-hangar/ci-cluster-values.yaml
helm template t mcp-hangar-operator -f mcp-hangar-operator/ci-values.yaml

# Install (to cluster)
helm install mcp-hangar ./mcp-hangar --namespace mcp-hangar --create-namespace
helm install mcp-hangar-operator ./mcp-hangar-operator --namespace mcp-hangar --create-namespace

# Package
helm package mcp-hangar
helm package mcp-hangar-operator

# Push to OCI registry
helm push mcp-hangar-*.tgz oci://ghcr.io/mcp-hangar/charts
helm push mcp-hangar-operator-*.tgz oci://ghcr.io/mcp-hangar/charts
```

## Chart: mcp-hangar

Application chart for deploying MCP Hangar core (Python backend).

```
mcp-hangar/
├── Chart.yaml            # Chart metadata (version, appVersion, kubeVersion)
├── values.yaml           # Default configuration values
├── ci-values.yaml        # Single-replica shape, rendered and installed in CI
├── ci-cluster-values.yaml# Multi-replica shape, RENDER validation only
├── README.md
├── files/                # Shipped payloads (.Files.Get)
│   ├── dashboards/       # 4 Grafana dashboards
│   └── prometheus-alerts.yaml
└── templates/
    ├── _helpers.tpl      # Template helpers (labels, names, selectors)
    ├── _cluster.tpl      # Render-time guards for the multi-replica shape
    ├── NOTES.txt         # Post-install instructions
    ├── deployment.yaml
    ├── service.yaml      # ClusterIP Service (sessionAffinity: ClientIP)
    ├── configmap.yaml    # config.yaml, mounted into the pod
    ├── pvc.yaml          # Optional PVC for the sqlite backend
    ├── serviceaccount.yaml
    ├── networkpolicy.yaml
    ├── poddisruptionbudget.yaml
    ├── servicemonitor.yaml   # Prometheus ServiceMonitor
    ├── prometheusrule.yaml   # Alert rules from files/
    ├── dashboards.yaml       # Dashboard ConfigMaps from files/
    ├── hpa.yaml
    └── tests/                # Helm test hooks
```

There is no `templates/ingress.yaml`. Bring your own Ingress; the chart owns
the Service.

### Key Values

Abridged -- `values.yaml` is the reference and carries the reasoning in
comments.

```yaml
replicaCount: 1
image:
  repository: ghcr.io/mcp-hangar/mcp-hangar
  tag: ""  # defaults to appVersion
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080
  sessionAffinity: ClientIP   # MCP sessions live in one replica's memory

config:
  port: 8080
  logLevel: INFO
  jsonLogs: true
  unsafeNoAuth: false   # demo only; otherwise configure `auth`
  trustedHosts: []      # renders MCP_TRUSTED_HOSTS; the dev default 400s

# Backend MCP servers the gateway fronts. Top level, NOT under `config`.
mcp_servers: {}
  # math:
  #   mode: remote
  #   endpoint: http://math.internal:8000/mcp

auth: {}

persistence:
  backend: ""           # "" | sqlite | postgresql (core 2.5.0+)
coordination:
  enabled: false        # required for more than one replica

extraEnv: []            # appended last, so it wins

resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

networkPolicy:
  enabled: true
serviceMonitor:
  enabled: false
prometheusRule:
  enabled: false
dashboards:
  enabled: false
```

`persistence`, `coordination` and `mcp_servers` are cross-checked at render
time by `templates/_cluster.tpl`: replicas without a shared backend, a
coordinated release running a subprocess-mode server, a `renewDeadlineSeconds`
that is not under the lease TTL and similar combinations fail `helm template`
rather than the pod.

## Chart: mcp-hangar-operator

Operator chart for deploying the Kubernetes operator.

```
mcp-hangar-operator/
├── Chart.yaml
├── values.yaml
├── ci-values.yaml
└── templates/
    ├── _helpers.tpl
    ├── NOTES.txt
    ├── deployment.yaml
    ├── service.yaml                        # Metrics service
    ├── webhook-service.yaml
    ├── validatingwebhookconfiguration.yaml
    ├── certificate.yaml                    # cert-manager Certificate/Issuer
    ├── serviceaccount.yaml
    ├── clusterrole.yaml                    # RBAC for operator
    ├── clusterrolebinding.yaml
    ├── secret.yaml                         # Optional secrets
    ├── networkpolicy.yaml
    ├── poddisruptionbudget.yaml
    ├── servicemonitor.yaml
    ├── prometheusrule.yaml
    ├── crds/                               # CRD templates, gated by values.crds.install
    └── tests/
```

Main value groups: `operator.*` (log level, metrics port, health port, leader
election, graceful shutdown), `hangar.*` (gateway URL and API key), `webhook.*`
(admission webhooks, cert-manager wiring, failure policy) and `crds.*`
(install/keep/conversion).

### CRDs

CRD manifests live only in `templates/crds/` (release-owned, gated by
`values.crds.install`). There is no top-level `crds/` directory -- shipping
CRDs through both Helm's native `crds/` dir and `templates/crds/`
simultaneously causes a Helm ownership conflict on `helm install`. Each
templated CRD carries `helm.sh/resource-policy: keep` (toggled by
`values.crds.keep`) so `helm uninstall` does not cascade-delete CRDs and the
custom resources under them. When operator CRD types change:

1. Regenerate in the `mcp-hangar-operator` repo: `make manifests`
2. Copy from `operator/config/crd/bases/` into `mcp-hangar-operator/templates/crds/`,
   wrapping each with the `{{- if .Values.crds.install }}` guard, the
   `helm.sh/resource-policy: keep` annotation and the conversion stanza used by
   the existing files
3. Verify with `helm lint mcp-hangar-operator`

## Conventions

### Template Helpers

Use `_helpers.tpl` for reusable template functions:

```yaml
{{- define "mcp-hangar.labels" -}}
helm.sh/chart: {{ include "mcp-hangar.chart" . }}
app.kubernetes.io/name: {{ include "mcp-hangar.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

### Values Structure

- Use flat keys where possible
- Group related values under a parent key
- Document all values with comments in `values.yaml`
- Use `""` (empty string) as default for optional strings
- Use `{}` as default for optional objects
- Boolean feature flags: `enabled: false` pattern
- A value the templates never read is a lie; delete the key instead of
  carrying it

### NOTES.txt

Update `NOTES.txt` when adding new features. It should contain:
- Connection instructions
- URLs for accessing the service
- Next steps for the user

### Versioning

- `version` in Chart.yaml tracks chart changes
- `appVersion` in Chart.yaml tracks the application version, and deliberately
  tracks the last STABLE release -- never a candidate
- Do not hardcode version numbers in docs. The current numbers live in each
  chart's `Chart.yaml`; the supported combinations live in the
  [release compatibility matrix](https://github.com/mcp-hangar/docs/blob/main/operations/RELEASE_COMPATIBILITY.md),
  which is the single source of truth (ADR-011)

## Dependencies on Other Subprojects

- **core**: `mcp-hangar` chart deploys the core Python application; `appVersion`
  names the image tag
- **operator**: `mcp-hangar-operator` chart deploys the Go operator; CRD
  manifests are copied from the operator build

## What NOT to Do

- No hardcoded image tags -- use `values.yaml` and `.Chart.AppVersion`
- No hardcoded namespaces in templates -- use `{{ .Release.Namespace }}`
- No `helm.sh/hook` unless truly needed (operator CRDs use `templates/crds/`, gated by `values.crds.install`, instead)
- No secrets in `values.yaml` defaults -- use external secret management
- No emoji in comments or NOTES.txt
