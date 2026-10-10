# Changelog

## [0.12.26](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.25...mcp-hangar-operator-v0.12.26) (2026-10-10)


### Added

* **operator:** ship operator 0.17.10 with authenticated HTTPS metrics ([#269](https://github.com/mcp-hangar/helm-charts/issues/269)) ([4d3216b](https://github.com/mcp-hangar/helm-charts/commit/4d3216b0f01b6c187ea2692d447e61e9809f3f27))

## [0.12.25](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.24...mcp-hangar-operator-v0.12.25) (2026-10-10)


### Added

* **operator:** expose --dns-egress-selectors in the operator chart ([#267](https://github.com/mcp-hangar/helm-charts/issues/267)) ([113e3e1](https://github.com/mcp-hangar/helm-charts/commit/113e3e1575b2b17e898e37a89b73c374bc004446))


### Fixed

* **operator:** default the mcp-hangar-operator chart to operator image 0.17.9 ([#266](https://github.com/mcp-hangar/helm-charts/issues/266)) ([4363359](https://github.com/mcp-hangar/helm-charts/commit/43633593c478ff700a808f1c1e7d7cb1039d84de))

## [0.12.24](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.23...mcp-hangar-operator-v0.12.24) (2026-10-10)


### Fixed

* **operator:** drop the Secret, ServiceAccount and pods/status grants ([#264](https://github.com/mcp-hangar/helm-charts/issues/264)) ([5c49f9d](https://github.com/mcp-hangar/helm-charts/commit/5c49f9deccfe96e4e6ffbee8cf1dea405daa5afb))

## [0.12.23](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.22...mcp-hangar-operator-v0.12.23) (2026-10-10)


### Fixed

* **operator:** default the mcp-hangar-operator chart to operator image 0.17.8 ([#262](https://github.com/mcp-hangar/helm-charts/issues/262)) ([6efa704](https://github.com/mcp-hangar/helm-charts/commit/6efa704fdb36e0cd1b5c6a74459ada3380297212))

## [0.12.22](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.21...mcp-hangar-operator-v0.12.22) (2026-10-10)


### Fixed

* **operator:** default the mcp-hangar-operator chart to operator image 0.17.7 ([#260](https://github.com/mcp-hangar/helm-charts/issues/260)) ([2599534](https://github.com/mcp-hangar/helm-charts/commit/25995343a7b30b5fae589a24a7ffb8de8a009698))

## [0.12.21](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.20...mcp-hangar-operator-v0.12.21) (2026-10-10)


### Added

* **operator:** expose the enforcement, DNS egress and image digest flags ([#258](https://github.com/mcp-hangar/helm-charts/issues/258)) ([c648c69](https://github.com/mcp-hangar/helm-charts/commit/c648c69fe422a975ff13768dd4a8860f0c1c43cb))

## [0.12.20](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.19...mcp-hangar-operator-v0.12.20) (2026-10-09)


### Fixed

* **operator:** ship operator 0.17.6 and its CRDs ([#255](https://github.com/mcp-hangar/helm-charts/issues/255)) ([9c5f121](https://github.com/mcp-hangar/helm-charts/commit/9c5f121212297a3b0ee71fcf4a33a5a8e70769c7))

## [0.12.19](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.18...mcp-hangar-operator-v0.12.19) (2026-10-09)


### Fixed

* **operator:** grant read on apps/daemonsets for the enforcement probe ([#253](https://github.com/mcp-hangar/helm-charts/issues/253)) ([53fcd31](https://github.com/mcp-hangar/helm-charts/commit/53fcd31ac9b7fb329a69b4e680ea68593613d48e))

## [0.12.18](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.17...mcp-hangar-operator-v0.12.18) (2026-10-09)


### Fixed

* **operator:** ship operator 0.17.5, its CRDs and the pod UPDATE webhook rule ([#251](https://github.com/mcp-hangar/helm-charts/issues/251)) ([5ef3f66](https://github.com/mcp-hangar/helm-charts/commit/5ef3f66c3baddd44d4f5ccd03281c19b26f72a98))

## [0.12.17](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.16...mcp-hangar-operator-v0.12.17) (2026-09-24)


### Added

* **operator:** expose --hangar-gateway-selector in the operator chart ([#241](https://github.com/mcp-hangar/helm-charts/issues/241)) ([9baac69](https://github.com/mcp-hangar/helm-charts/commit/9baac69ddb57248c99eb726e419ff87cd2919f2b))

## [0.12.16](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.15...mcp-hangar-operator-v0.12.16) (2026-09-21)


### Fixed

* **operator:** ship the CRDs the operator image writes, and gate the drift ([#234](https://github.com/mcp-hangar/helm-charts/issues/234)) ([dbed0a4](https://github.com/mcp-hangar/helm-charts/commit/dbed0a467498cb2a1055fab73e064f6bfcabde62))

## [0.12.15](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.14...mcp-hangar-operator-v0.12.15) (2026-09-20)


### Fixed

* **operator:** alert on reconcile errors from every controller ([#212](https://github.com/mcp-hangar/helm-charts/issues/212)) ([f3fffb6](https://github.com/mcp-hangar/helm-charts/commit/f3fffb65186569b7a151ae337391f7cbc4c1e842)), closes [#200](https://github.com/mcp-hangar/helm-charts/issues/200)
* **operator:** default the mcp-hangar-operator chart to operator image 0.17.2 ([#220](https://github.com/mcp-hangar/helm-charts/issues/220)) ([448b00c](https://github.com/mcp-hangar/helm-charts/commit/448b00c89ca9a056a85460aa63f23d27f42ea814))
* **operator:** match the job label the ServiceMonitor actually produces ([#225](https://github.com/mcp-hangar/helm-charts/issues/225)) ([2239846](https://github.com/mcp-hangar/helm-charts/commit/22398469ada161def1bbbfa8967701a9b8a1756b)), closes [#213](https://github.com/mcp-hangar/helm-charts/issues/213)

## [0.12.14](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.13...mcp-hangar-operator-v0.12.14) (2026-09-17)


### Fixed

* **operator:** default the mcp-hangar-operator chart to operator image 0.17.2 ([#220](https://github.com/mcp-hangar/helm-charts/issues/220)) ([448b00c](https://github.com/mcp-hangar/helm-charts/commit/448b00c89ca9a056a85460aa63f23d27f42ea814))

## [0.12.13](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.12...mcp-hangar-operator-v0.12.13) (2026-08-24)


### Fixed

* **operator:** re-vendor the CRDs for operator v0.17.1 ([#178](https://github.com/mcp-hangar/helm-charts/issues/178)) ([21dcbaa](https://github.com/mcp-hangar/helm-charts/commit/21dcbaa497aedba6a708f94a88a9ac4e2d63e43a))

## [0.12.12](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.11...mcp-hangar-operator-v0.12.12) (2026-08-20)


### Fixed

* **operator:** re-sync the vendored CRDs with operator v0.17.0 ([#170](https://github.com/mcp-hangar/helm-charts/issues/170)) ([20544fa](https://github.com/mcp-hangar/helm-charts/commit/20544fa7f3bdfd56aa4fbbd89175051cf8ddae04)), closes [#168](https://github.com/mcp-hangar/helm-charts/issues/168)

## [0.12.11](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-operator-v0.12.10...mcp-hangar-operator-v0.12.11) (2026-08-20)


### Fixed

* **operator:** grant events.k8s.io on the operator ClusterRole ([#167](https://github.com/mcp-hangar/helm-charts/issues/167)) ([bb0a186](https://github.com/mcp-hangar/helm-charts/commit/bb0a186ee03744dc0999101277f1645a9326c5cf)), closes [#166](https://github.com/mcp-hangar/helm-charts/issues/166)

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
