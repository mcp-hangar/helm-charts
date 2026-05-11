# Contributing

Thank you for your interest in contributing to MCP Hangar Helm Charts!

## Quick Start

```bash
git clone https://github.com/mcp-hangar/helm-charts.git
cd helm-charts

# Lint
helm lint mcp-hangar
helm lint mcp-hangar-operator
helm lint hangar-agent

# Template (dry-run render)
helm template my-release mcp-hangar
helm template my-release mcp-hangar-operator

# Package
helm package mcp-hangar
helm package mcp-hangar-operator
```

## Licensing

MCP Hangar Helm Charts is licensed under the [MIT License](LICENSE).

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.
