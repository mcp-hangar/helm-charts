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
  --set replicaCount=2 \
  --set resources.requests.memory=512Mi
```

### With MCP Servers

```yaml
# values.yaml
mcp_servers:
  math:
    mode: subprocess
    command: ["python", "-m", "math_server"]
  fetch:
    mode: container
    image: ghcr.io/mcp-hangar/mcp-fetch:latest
```

```bash
helm install mcp-hangar oci://ghcr.io/mcp-hangar/charts/mcp-hangar -f values.yaml
```

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
| config.unsafeNoAuth | bool | `false` | Allow binding HTTP on non-loopback without auth (demo/insecure only) |
| auth | object | `{}` | Auth configuration rendered into config.yaml `auth:` section |
| serviceMonitor.enabled | bool | `false` | Enable Prometheus ServiceMonitor |

## License

MIT
