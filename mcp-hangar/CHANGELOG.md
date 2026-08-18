# Changelog

## [0.15.6](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.15.5...mcp-hangar-v0.15.6) (2026-08-18)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.12.0 ([#162](https://github.com/mcp-hangar/helm-charts/issues/162)) ([4c45e48](https://github.com/mcp-hangar/helm-charts/commit/4c45e4878dfb0d9d66449a36e151e2662e31e51b))

## [0.15.5](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.15.4...mcp-hangar-v0.15.5) (2026-08-18)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.11.0 ([#159](https://github.com/mcp-hangar/helm-charts/issues/159)) ([48c4e8d](https://github.com/mcp-hangar/helm-charts/commit/48c4e8d3ffbe1172b67a05e859654ef20717ba9d))

## [0.15.4](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.15.3...mcp-hangar-v0.15.4) (2026-08-17)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.10.1 ([#157](https://github.com/mcp-hangar/helm-charts/issues/157)) ([f2959d8](https://github.com/mcp-hangar/helm-charts/commit/f2959d82aca6bb8ee5832ea95241950a4f7a2cb6))

## [0.15.3](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.15.2...mcp-hangar-v0.15.3) (2026-08-17)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.10.0 ([#147](https://github.com/mcp-hangar/helm-charts/issues/147)) ([8f9f37f](https://github.com/mcp-hangar/helm-charts/commit/8f9f37fe473c2b10318a614786d777422d993842))

## [0.15.2](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.15.1...mcp-hangar-v0.15.2) (2026-08-16)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.9.0 ([#145](https://github.com/mcp-hangar/helm-charts/issues/145)) ([fb8b0cc](https://github.com/mcp-hangar/helm-charts/commit/fb8b0cc0050f94d7ad11a72ca606c49f75edfb85))

## [0.15.1](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.15.0...mcp-hangar-v0.15.1) (2026-08-15)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.8.0 ([#142](https://github.com/mcp-hangar/helm-charts/issues/142)) ([4dce3a5](https://github.com/mcp-hangar/helm-charts/commit/4dce3a5012fe32e06fbe59f61366e9f927841d22))

## [0.15.0](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.14.4...mcp-hangar-v0.15.0) (2026-08-14)


### Added

* **hangar:** stop pinning sessions, they no longer exist ([#136](https://github.com/mcp-hangar/helm-charts/issues/136)) ([a8d0220](https://github.com/mcp-hangar/helm-charts/commit/a8d0220d35e60191a2634d124618b269b6d265e3))

## [0.14.4](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.14.3...mcp-hangar-v0.14.4) (2026-08-14)


### Added

* **hangar:** a named value for the host allow-list, and a guard for the case that 400s ([#117](https://github.com/mcp-hangar/helm-charts/issues/117)) ([c4d7dea](https://github.com/mcp-hangar/helm-charts/commit/c4d7deab65ea47e9144ddb9f874d8a67bc33f87e)), closes [#104](https://github.com/mcp-hangar/helm-charts/issues/104)
* **hangar:** own the shipped dashboards and alerts, and fix the drift ([#135](https://github.com/mcp-hangar/helm-charts/issues/135)) ([b6f59c4](https://github.com/mcp-hangar/helm-charts/commit/b6f59c46fdc94e12ef269081805674cfaa2fed4f)), closes [#126](https://github.com/mcp-hangar/helm-charts/issues/126)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.6.0 ([#113](https://github.com/mcp-hangar/helm-charts/issues/113)) ([023a91c](https://github.com/mcp-hangar/helm-charts/commit/023a91cb989eb0f3c5b0ad46dabb20f6b454336a))
* **hangar:** pin an MCP session to one replica by default ([#115](https://github.com/mcp-hangar/helm-charts/issues/115)) ([8163762](https://github.com/mcp-hangar/helm-charts/commit/81637626e06d684c349f421575e3f2caf8bdfe1a)), closes [#109](https://github.com/mcp-hangar/helm-charts/issues/109)
* **hangar:** remove config.mode and configMap.create ([#132](https://github.com/mcp-hangar/helm-charts/issues/132)) ([c261cdc](https://github.com/mcp-hangar/helm-charts/commit/c261cdc4c7d5ac3d126610f156acd3a8a5aaa457)), closes [#121](https://github.com/mcp-hangar/helm-charts/issues/121)
* **hangar:** remove the ingress values the chart never rendered ([#131](https://github.com/mcp-hangar/helm-charts/issues/131)) ([2392d3c](https://github.com/mcp-hangar/helm-charts/commit/2392d3c8318fb7598f3ad1f0be19da8fc992803b)), closes [#120](https://github.com/mcp-hangar/helm-charts/issues/120)

## [0.14.3](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.14.2...mcp-hangar-v0.14.3) (2026-08-11)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.5.3 ([#111](https://github.com/mcp-hangar/helm-charts/issues/111)) ([9af46ee](https://github.com/mcp-hangar/helm-charts/commit/9af46ee41a3fda035d9f13606a132c5923c704e6))

## [0.14.2](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.14.1...mcp-hangar-v0.14.2) (2026-08-10)


### Added

* **hangar:** add extraEnv and extraEnvFrom to the mcp-hangar chart ([#105](https://github.com/mcp-hangar/helm-charts/issues/105)) ([f890d02](https://github.com/mcp-hangar/helm-charts/commit/f890d0267cd257a16fc957e14443a9cdc20133f3)), closes [#103](https://github.com/mcp-hangar/helm-charts/issues/103) [#102](https://github.com/mcp-hangar/helm-charts/issues/102)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.5.1 ([#100](https://github.com/mcp-hangar/helm-charts/issues/100)) ([47ad5c8](https://github.com/mcp-hangar/helm-charts/commit/47ad5c8821d638b7ac4cbb5ff13f33f58a9ad462))
* **hangar:** default the mcp-hangar chart to core image 2.5.2 ([#106](https://github.com/mcp-hangar/helm-charts/issues/106)) ([8939a80](https://github.com/mcp-hangar/helm-charts/commit/8939a80fb20b9023501aa7670b7e3ca8c9220208))

## [0.14.1](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.14.0...mcp-hangar-v0.14.1) (2026-08-09)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.5.0 ([#98](https://github.com/mcp-hangar/helm-charts/issues/98)) ([f9263ac](https://github.com/mcp-hangar/helm-charts/commit/f9263ac0faaa21623752ff4d30ed005ccf4cbb25))

## [0.14.0](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.13.11...mcp-hangar-v0.14.0) (2026-08-07)


### Added

* **hangar:** the chart can express a cluster, and refuses one it cannot ([#95](https://github.com/mcp-hangar/helm-charts/issues/95)) ([eeaebfc](https://github.com/mcp-hangar/helm-charts/commit/eeaebfc3a63114f5c8b86ca1044da5d8af0422a4))


### Changed

* **hangar:** let release-please own the chart version ([#97](https://github.com/mcp-hangar/helm-charts/issues/97)) ([1f07677](https://github.com/mcp-hangar/helm-charts/commit/1f07677e899d24513dfa01d686a4fce796ddd3d7))

## [0.13.11](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.13.10...mcp-hangar-v0.13.11) (2026-08-05)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.4.0 ([#93](https://github.com/mcp-hangar/helm-charts/issues/93)) ([edde09f](https://github.com/mcp-hangar/helm-charts/commit/edde09fa0d9861beeb368571b11361ab259b65af))

## [0.13.10](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.13.9...mcp-hangar-v0.13.10) (2026-08-05)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 2.3.0 ([#91](https://github.com/mcp-hangar/helm-charts/issues/91)) ([d3f24b9](https://github.com/mcp-hangar/helm-charts/commit/d3f24b94e936cae9fd4be263669e22a776125dd1))

## [0.13.9](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.13.8...mcp-hangar-v0.13.9) (2026-08-03)


### Fixed

* **hangar:** point the chart at core 2.2.1 ([#89](https://github.com/mcp-hangar/helm-charts/issues/89)) ([2ad88e6](https://github.com/mcp-hangar/helm-charts/commit/2ad88e650cbae21c5749a0a7ff26221301eca43f))

## [0.13.8](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.13.7...mcp-hangar-v0.13.8) (2026-08-03)


### Fixed

* **hangar:** point the chart at core 2.2.0 ([#86](https://github.com/mcp-hangar/helm-charts/issues/86)) ([f702890](https://github.com/mcp-hangar/helm-charts/commit/f70289055df9d1c69cb2c007d93dcf01d7ae5795))

## [0.13.7](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.13.6...mcp-hangar-v0.13.7) (2026-07-31)


### Added

* **hangar:** default the mcp-hangar chart to core image 2.0.0 ([#81](https://github.com/mcp-hangar/helm-charts/issues/81)) ([8a75f42](https://github.com/mcp-hangar/helm-charts/commit/8a75f42dd4256c3352179689a8702e452d4d4e32))
* **hangar:** package alert rules and dashboards into the chart ([#65](https://github.com/mcp-hangar/helm-charts/issues/65)) ([ae2f135](https://github.com/mcp-hangar/helm-charts/commit/ae2f1359874abc8d2b3cfa1d32da9da8fac9d689))
* **operator:** add MCPEgressPolicy CRD template; appVersion -&gt; 0.14.0 ([#66](https://github.com/mcp-hangar/helm-charts/issues/66)) ([129dfd2](https://github.com/mcp-hangar/helm-charts/commit/129dfd265b0ac986a3ceadbe34cab29afa23a1c9))


### Fixed

* **hangar:** default the mcp-hangar chart to core image 1.5.1 ([#48](https://github.com/mcp-hangar/helm-charts/issues/48)) ([82ef695](https://github.com/mcp-hangar/helm-charts/commit/82ef69595005109269ec885e1e40826207492057))
* **hangar:** default the mcp-hangar chart to core image 1.6.0 ([#67](https://github.com/mcp-hangar/helm-charts/issues/67)) ([360749a](https://github.com/mcp-hangar/helm-charts/commit/360749a3d96e2cf0b2210e131f51080922017feb))
* **hangar:** default the mcp-hangar chart to core image 1.6.3 ([#79](https://github.com/mcp-hangar/helm-charts/issues/79)) ([90426bb](https://github.com/mcp-hangar/helm-charts/commit/90426bbd1501435515a51b86054127353447ee36))

## [0.13.4](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.13.3...mcp-hangar-v0.13.4) (2026-07-19)


### Added

* **hangar:** package alert rules and dashboards into the chart ([#65](https://github.com/mcp-hangar/helm-charts/issues/65)) ([ae2f135](https://github.com/mcp-hangar/helm-charts/commit/ae2f1359874abc8d2b3cfa1d32da9da8fac9d689))
* **operator:** add MCPEgressPolicy CRD template; appVersion -&gt; 0.14.0 ([#66](https://github.com/mcp-hangar/helm-charts/issues/66)) ([129dfd2](https://github.com/mcp-hangar/helm-charts/commit/129dfd265b0ac986a3ceadbe34cab29afa23a1c9))


### Fixed

* **hangar:** default the mcp-hangar chart to core image 1.6.0 ([#67](https://github.com/mcp-hangar/helm-charts/issues/67)) ([360749a](https://github.com/mcp-hangar/helm-charts/commit/360749a3d96e2cf0b2210e131f51080922017feb))

## [0.13.3](https://github.com/mcp-hangar/helm-charts/compare/mcp-hangar-v0.13.2...mcp-hangar-v0.13.3) (2026-07-16)


### Fixed

* **hangar:** default the mcp-hangar chart to core image 1.5.1 ([#48](https://github.com/mcp-hangar/helm-charts/issues/48)) ([82ef695](https://github.com/mcp-hangar/helm-charts/commit/82ef69595005109269ec885e1e40826207492057))
