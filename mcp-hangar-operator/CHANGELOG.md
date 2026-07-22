# Changelog

## [0.12.4](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.3...mcp-hangar-operator-v0.12.4) (2026-07-21)


### Fixed

* **mcp-hangar-operator:** grant RBAC for CiliumNetworkPolicy so the Cilium egress flavor works ([#73](https://github.com/mcp-hangar/helm-charts/issues/73)) ([4b588c7](https://github.com/mcp-hangar/helm-charts/commit/4b588c78e19375d101af99f48b4bae7784a81869))

## [0.12.3](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.2...mcp-hangar-operator-v0.12.3) (2026-07-19)


### Added

* **operator:** add MCPEgressPolicy CRD template; appVersion -&gt; 0.14.0 ([#66](https://github.com/mcp-hangar/helm-charts/issues/66)) ([129dfd2](https://github.com/mcp-hangar/helm-charts/commit/129dfd265b0ac986a3ceadbe34cab29afa23a1c9))
* **operator:** add pod-registration admission webhook to chart ([#62](https://github.com/mcp-hangar/helm-charts/issues/62)) ([#63](https://github.com/mcp-hangar/helm-charts/issues/63)) ([fb701fa](https://github.com/mcp-hangar/helm-charts/commit/fb701fae5c90fc3c45df5767656245b2a069eec3))

## [0.12.2](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.1...mcp-hangar-operator-v0.12.2) (2026-07-16)


### Fixed

* **operator:** default to Recreate strategy so upgrades don't deadlock, and add a required-safe chart CI gate with upgrade/rollback coverage ([#40](https://github.com/mcp-hangar/helm-charts/issues/40)) ([9823500](https://github.com/mcp-hangar/helm-charts/commit/98235000d165d747f74843535ba2c983708a8e88))
