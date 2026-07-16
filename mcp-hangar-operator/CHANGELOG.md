# Changelog

## [0.12.2](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.1...mcp-hangar-operator-v0.12.2) (2026-07-16)


### Fixed

* **operator:** default to Recreate strategy so upgrades don't deadlock, and add a required-safe chart CI gate with upgrade/rollback coverage ([#40](https://github.com/mcp-hangar/helm-charts/issues/40)) ([9823500](https://github.com/mcp-hangar/helm-charts/commit/98235000d165d747f74843535ba2c983708a8e88))
