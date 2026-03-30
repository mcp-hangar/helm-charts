# MCP Hangar Helm Charts

## Quick Reference

| Property | Value |
|----------|-------|
| Chart format | Helm v3 (apiVersion: v2) |
| Kubernetes | >= 1.25 |
| Charts | `mcp-hangar` (app), `mcp-hangar-operator` (operator) |
| Registry | `oci://ghcr.io/mcp-hangar/charts` |

## Commands

```bash
cd packages/helm-charts

# Lint
helm lint mcp-hangar
helm lint mcp-hangar-operator

# Template (dry-run render)
helm template my-release mcp-hangar
helm template my-release mcp-hangar-operator

# Install (to cluster)
helm install mcp-hangar ./mcp-hangar --namespace mcp-system --create-namespace
helm install mcp-hangar-operator ./mcp-hangar-operator --namespace mcp-system --create-namespace

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
├── Chart.yaml          # Chart metadata (version, appVersion, kubeVersion)
├── values.yaml         # Default configuration values
├── README.md
└── templates/
    ├── _helpers.tpl     # Template helpers (labels, names, selectors)
    ├── NOTES.txt        # Post-install instructions
    ├── deployment.yaml  # MCP Hangar Deployment
    ├── service.yaml     # ClusterIP Service
    ├── configmap.yaml   # Configuration (mounted as config.yaml)
    ├── serviceaccount.yaml
    ├── servicemonitor.yaml  # Prometheus ServiceMonitor
    ├── hpa.yaml         # HorizontalPodAutoscaler
    └── tests/           # Helm test hooks
```

### Key Values

```yaml
replicaCount: 1
image:
  repository: ghcr.io/mcp-hangar/mcp-hangar
  tag: ""  # defaults to appVersion
  pullPolicy: IfNotPresent

config:
  providers: {}  # Provider configuration (injected into ConfigMap)
  logging:
    level: INFO
    json_format: true

service:
  type: ClusterIP
  port: 8000

resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

serviceMonitor:
  enabled: false
  interval: 30s
```

## Chart: mcp-hangar-operator

Operator chart for deploying the Kubernetes operator.

```
mcp-hangar-operator/
├── Chart.yaml
├── values.yaml
├── crds/                # CRD manifests (installed before templates)
│   ├── mcpproviders.yaml
│   ├── mcpprovidergroups.yaml
│   └── mcpdiscoverysources.yaml
└── templates/
    ├── _helpers.tpl
    ├── NOTES.txt
    ├── deployment.yaml        # Operator Deployment
    ├── service.yaml           # Metrics service
    ├── serviceaccount.yaml
    ├── clusterrole.yaml       # RBAC for operator
    ├── clusterrolebinding.yaml
    ├── secret.yaml            # Optional secrets
    ├── servicemonitor.yaml    # Prometheus ServiceMonitor
    ├── crds/                  # CRD templates (if conditional install needed)
    └── tests/
```

### CRDs

CRD manifests live in `crds/` directory and are installed automatically by Helm before any templates. When operator CRD types change:

1. Regenerate in the `operator` repo: `make manifests`
2. Copy from `operator/config/crd/bases/` to `mcp-hangar-operator/crds/`
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

### NOTES.txt

Update `NOTES.txt` when adding new features. It should contain:
- Connection instructions
- URLs for accessing the service
- Next steps for the user

### Versioning

- `version` in Chart.yaml tracks chart changes
- `appVersion` in Chart.yaml tracks the application version
- Keep both in sync with core package version (currently 0.11.0)

## Dependencies on Other Subprojects

- **core**: `mcp-hangar` chart deploys the core Python application; image tag must match
- **operator**: `mcp-hangar-operator` chart deploys the Go operator; CRD manifests sourced from operator build

## What NOT to Do

- No hardcoded image tags -- use `values.yaml` and `.Chart.AppVersion`
- No hardcoded namespaces in templates -- use `{{ .Release.Namespace }}`
- No `helm.sh/hook` unless truly needed (CRDs use `crds/` directory instead)
- No secrets in `values.yaml` defaults -- use external secret management
- No emoji in comments or NOTES.txt

