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

### Response Truncation

Optional, core 2.12.0+. Renders a `truncation:` block into config.yaml only
when enabled; disabled emits nothing.

```yaml
truncation:
  enabled: true
  cacheDriver: redis                          # or `memory` (per-replica)
  redisUrl: redis://redis.cache.svc:6379/0    # required with `redis`
```

The Redis here is the **continuation cache** — where the gateway parks full
responses so a truncated one can be fetched later — not rate limits and not
sessions. Bring your own (external) Redis: the chart bundles no Redis subchart
and no Sentinel values. `cacheDriver: redis` without a `redisUrl` fails the
render, because the gateway would refuse the config anyway. With more than one
replica, `memory` means a continuation can land on a replica that never cached
it — use `redis`.

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

#### Sticky routing: no longer required, from appVersion 2.7.0

A gateway older than 2.7.0 kept each MCP Streamable HTTP session in **one
replica's memory**, so a request routed to a different pod than the one that ran
`initialize` was answered `Session not found` — most requests, on three replicas
without pinning. The chart pinned the Service for you and told you to pin your
ingress as well.

From 2.7.0 the gateway serves the transport without a session at all
([mcp-hangar#877](https://github.com/mcp-hangar/mcp-hangar/issues/877)). Every
replica can answer every request, a rolling restart costs a client nothing, and
`service.sessionAffinity` therefore defaults to `None`. A `ClientIP` pin is now
only a cost: it keys on the source address as the Service sees it, so behind a
proxy that does not preserve the client address it lands everything on one pod.

**Set `service.sessionAffinity: ClientIP` if you pin `image.tag` to a gateway
older than 2.7.0**, and pin your ingress too — Service affinity is kube-proxy
behaviour and does nothing for a controller that routes straight to pod
endpoints. For ingress-nginx that is

```yaml
nginx.ingress.kubernetes.io/upstream-hash-by: "$remote_addr"
```

— the hash rather than the usual cookie affinity, because an MCP client is not a
browser and will not carry the cookie back. Neither hop's pin survives a rolling
restart, which is why the gateway stopped needing them rather than the chart
getting better at arranging them.

The chart cannot read a version out of a tag, so `NOTES.txt` asks at install time
when `replicaCount > 1` and `image.tag` is set.

One thing clients can notice on 2.7.0: `DELETE /mcp` answers `405`, because there
is no session to terminate.

Whatever host you serve must also be in `config.trustedHosts`, or the gateway
answers `400 Invalid host header` from a pod that is Ready.

Full recipe: [Running more than one replica](https://mcp-hangar.io/docs/cookbook/25-multiple-replicas).

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| replicaCount | int | `1` | Number of replicas |
| image.repository | string | `ghcr.io/mcp-hangar/mcp-hangar` | Image repository |
| image.tag | string | `""` | Image tag (defaults to appVersion) |
| service.type | string | `ClusterIP` | Service type |
| service.port | int | `8080` | Service port |
| service.sessionAffinity | string | `None` | Round-robin. From appVersion 2.7.0 the gateway keeps no MCP session, so replicas are interchangeable. Set `ClientIP` only if `image.tag` names a gateway older than 2.7.0 |
| service.sessionAffinityConfig.clientIP.timeoutSeconds | int | `10800` | How long the pin survives idle time. Rendered only when `sessionAffinity` is `ClientIP` — Kubernetes rejects it otherwise |
| config.logLevel | string | `INFO` | Log level |
| config.trustedHosts | list | `[]` | Host headers the gateway answers, rendered as `MCP_TRUSTED_HOSTS`. Empty keeps core's **development** default, which answers `400 Invalid host header` through a Service or Ingress |
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
| truncation.enabled | bool | `false` | Render a `truncation:` block into config.yaml (core 2.12.0+). Off emits nothing |
| truncation.cacheDriver | string | `memory` | Continuation cache backend: `memory` (per-replica) or `redis` |
| truncation.redisUrl | string | `""` | External Redis URL for the continuation cache. Required when cacheDriver is `redis` — the render fails without it |
| serviceMonitor.enabled | bool | `false` | Enable Prometheus ServiceMonitor |

## Helm versions

Helm 3 and Helm 4 are both supported and CI-tested (install, `helm test`,
upgrade, rollback under each major, plus the helm3-install → helm4-upgrade
cross path). A Helm 4 fresh install uses server-side apply; a release created
by Helm 3 keeps client-side apply across Helm 4 upgrades until you opt in
with `helm upgrade --server-side=true`. Note `helm3 test --logs` exits
non-zero on a *passing* test of this chart — Helm 3 deletes the
`hook-succeeded` test pod before fetching its logs (Helm 4 prints them
first); run `helm test` without `--logs` under Helm 3. Details and the
pinned versions: the repo [README](../README.md#helm-versions).

## License

MIT
