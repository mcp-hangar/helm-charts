# MCP-Hangar Helm Chart

Helm chart for deploying MCP-Hangar server on Kubernetes.

## Installation

```bash
helm install mcp-hangar oci://ghcr.io/mcp-hangar/charts/mcp-hangar
```

## Configuration

See `values.yaml` for all available options.

### Basic Example

```bash
helm install mcp-hangar oci://ghcr.io/mcp-hangar/charts/mcp-hangar \
  --set resources.requests.memory=512Mi
```

This example used to pass `--set replicaCount=2`. It should not have: until core
2.5.0 a second replica was not a second route to one gateway but a second
gateway, with its own fleet and its own idea of what was registered. The chart
now refuses that combination rather than rendering it -- see below.

### With MCP Servers

```yaml
# values.yaml
mcp_servers:
  math:
    mode: remote
    endpoint: http://math.internal:8000/mcp
```

`subprocess`, `docker` and `container` run the server as a child process of one
gateway. They work on a single instance and are refused when
`coordination.enabled` is true, because no peer has an address for a child
process.

```bash
helm install mcp-hangar oci://ghcr.io/mcp-hangar/charts/mcp-hangar -f values.yaml
```

### Storage

One decision, for everything the gateway keeps (core 2.5.0+). Leaving
`persistence.backend` empty keeps the previous per-subsystem behaviour.

```yaml
persistence:
  backend: sqlite
  sqlite:
    persistentVolume:
      enabled: true      # the `data` volume is an emptyDir without this,
      size: 8Gi          # so a pod restart loses the event log and the fleet
```

### Running More Than One Replica

Requires core 2.5.0+, one PostgreSQL every replica shares, and `remote`-mode
servers. The chart refuses any other combination at render time rather than
letting it install and disagree with itself.

```yaml
replicaCount: 3
image:
  tag: "2.5.0"

persistence:
  backend: postgresql
  postgresql:
    host: postgres.data.svc.cluster.local
    database: mcp_hangar
    user: hangar
    existingSecret: hangar-db     # keeps the password out of the ConfigMap

coordination:
  enabled: true
  leaseTtlSeconds: 15             # keep IDENTICAL on every replica: the tenure
  renewIntervalSeconds: 5         # in force is written by whichever replica
  renewDeadlineSeconds: 10        # holds the lease, from its own value
```

Every replica serves; exactly one holds the management lease and runs
discovery, garbage collection, TTL deregistration and metric snapshots. Check
it pod by pod rather than through the Service -- one should answer
`manages_fleet: true` at `GET /api/system`.

Two costs worth knowing before the rollout: rate limits are counted per
instance (a fleet-wide cap belongs at the ingress), and anything travelling by
the shared log reaches peers within a poll interval rather than immediately.

Full recipe: [Running more than one replica](https://mcp-hangar.io/docs/cookbook/25-multiple-replicas).

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| replicaCount | int | `1` | Number of replicas |
| image.repository | string | `ghcr.io/mcp-hangar/mcp-hangar` | Image repository |
| image.tag | string | `""` | Image tag (defaults to appVersion) |
| service.type | string | `ClusterIP` | Service type |
| service.port | int | `8080` | Service port |
| config.logLevel | string | `INFO` | Log level |
| config.jsonLogs | bool | `true` | Enable JSON logging |
| mcp_servers | object | `{}` | MCP server configurations |
| persistence.backend | string | `""` | `sqlite`, `postgresql`, or empty for the pre-2.5.0 per-subsystem behaviour |
| persistence.sqlite.persistentVolume.enabled | bool | `false` | Back the `data` volume with a PVC instead of an emptyDir |
| persistence.postgresql.host | string | `""` | Required when the backend is `postgresql` |
| persistence.postgresql.existingSecret | string | `""` | Secret holding the password; keeps it out of the ConfigMap |
| coordination.enabled | bool | `false` | Declares these replicas are one gateway. Required for more than one replica |
| coordination.leaseTtlSeconds | int | `15` | Management tenure. Keep identical across replicas |
| config.unsafeNoAuth | bool | `false` | Allow binding HTTP on non-loopback without auth (demo/insecure only) |
| auth | object | `{}` | Auth configuration rendered into config.yaml `auth:` section |
| serviceMonitor.enabled | bool | `false` | Enable Prometheus ServiceMonitor |

## License

MIT
