# Changelog

## [0.12.10](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.9...mcp-hangar-operator-v0.12.10) (2026-08-17)


### Fixed

* **operator:** drop v1alpha1 from the chart -- webhooks, CRDs, conversion knob (operator 0.16.0) ([#155](https://github.com/mcp-hangar/helm-charts/issues/155)) ([2ea89de](https://github.com/mcp-hangar/helm-charts/commit/2ea89de2bdaa73feae9906e4393dc5fe48263816))

## [0.12.9](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.8...mcp-hangar-operator-v0.12.9) (2026-08-17)


### Fixed

* **operator:** default the operator chart to image 0.15.3 ([#153](https://github.com/mcp-hangar/helm-charts/issues/153)) ([83a6b00](https://github.com/mcp-hangar/helm-charts/commit/83a6b00670699a0be2a304d172ecd05e5601bd3f))

## [0.12.8](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.7...mcp-hangar-operator-v0.12.8) (2026-08-14)


### Fixed

* **operator:** recopy CRDs after the operator field cuts ([#139](https://github.com/mcp-hangar/helm-charts/issues/139)) ([659bf36](https://github.com/mcp-hangar/helm-charts/commit/659bf36d6a6ba66f28bea1393384be18b9f0ede7)), closes [#127](https://github.com/mcp-hangar/helm-charts/issues/127)

## [0.12.7](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.6...mcp-hangar-operator-v0.12.7) (2026-08-14)


### Fixed

* **operator:** default the operator chart to image 0.15.2 ([#118](https://github.com/mcp-hangar/helm-charts/issues/118)) ([39d529b](https://github.com/mcp-hangar/helm-charts/commit/39d529b20100e2a89e322c5f85e2d5f49b77dc45))
* **operator:** hardcode the webhook port at 9443 ([#133](https://github.com/mcp-hangar/helm-charts/issues/133)) ([bb09533](https://github.com/mcp-hangar/helm-charts/commit/bb0953376694796ada365c71a4511796af00a113)), closes [#122](https://github.com/mcp-hangar/helm-charts/issues/122)

## [0.12.6](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.5...mcp-hangar-operator-v0.12.6) (2026-08-10)


### Fixed

* **operator:** default the operator chart to image 0.15.1 ([#107](https://github.com/mcp-hangar/helm-charts/issues/107)) ([f3e3a5e](https://github.com/mcp-hangar/helm-charts/commit/f3e3a5e43316e71f658a2863e3d1b98723b9dd3e))

## [0.12.5](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.4...mcp-hangar-operator-v0.12.5) (2026-07-27)


### Fixed

* **operator:** bump chart appVersion to 0.15.0 ([#76](https://github.com/mcp-hangar/helm-charts/issues/76)) ([b5acdf2](https://github.com/mcp-hangar/helm-charts/commit/b5acdf29d8ef82f71108e6d51a4cc1f3064a0c49))

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
