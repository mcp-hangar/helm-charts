# Releasing the MCP Hangar Helm charts

The three charts (`mcp-hangar`, `mcp-hangar-operator`, `hangar-agent`) are
versioned and released **independently**, each on its own SemVer line, per
[ADR-009](https://github.com/mcp-hangar/docs/blob/main/adr/ADR-009-independent-release-topology.md).

## Chart versions are automated — do not bump them by hand

`release-please` owns every chart's `version:`.

- It reads the [Conventional Commits](https://www.conventionalcommits.org/) that
  touch each chart's directory, computes the SemVer bump (on the pre-1.0 `0.x`
  line: a `fix`/`feat` is a patch; an explicit breaking change — `!` or a
  `BREAKING CHANGE:` footer — is a minor), updates `Chart.yaml`'s `version:` and
  the chart's `CHANGELOG.md`, and keeps a release PR open.
- Merging that release PR tags the release (`<chart>-vX.Y.Z`).
- **Do not edit `version:` in a `Chart.yaml` yourself.** A hand-bump collides
  with release-please; a missing bump means the change is silently never
  published (see below).

## `appVersion` is manual — it tracks the app image

`version:` is the chart's own version (release-please owns it). `appVersion:` is
the application image the chart deploys, and it is **bumped by hand**:

- When a new app image ships (e.g. core `1.5.1`, operator `0.12.3`), open a PR
  that repoints the chart at it — edit `appVersion:` and any template/values
  changes the new image needs.
- That PR's Conventional-Commit type then drives release-please to bump the
  chart's `version:` on the next release PR.

So an app-image update is one human PR (edit `appVersion` + templates); the chart
`version` bump that follows is automatic.

## Publication is automated and immutable

On push to `main`, `release-charts` (`.github/workflows/release.yml`):

- publishes any chart whose `version:` is **not yet** in the registry,
- signs it keyless with `cosign` and attaches an SBOM + provenance attestation.

The publish guard is **fail-safe**: it skips an already-published version and
refuses to push over one — a released tag is **immutable**, never re-pointed
(see [#36](https://github.com/mcp-hangar/helm-charts/issues/36)). Because the
guard skips unchanged versions, a chart change merged without a version bump is
never published — which is precisely why versioning is release-please's job, not
a manual one.

## CI gate

`ci-charts` (`.github/workflows/ci-charts.yml`) lints, renders (kubeconform), and
**installs** each chart against its pinned `appVersion` image on a real
Kubernetes cluster — install, health, upgrade, and rollback — because rendering
cleanly is not the same as installing and working. Its aggregate
`charts-required` job is the single required status check on `main`; a chart that
does not install cannot merge.

## Consuming a release

Pull by version or digest and verify the signature before deploying. The
[compatibility matrix & artifact-security policy](https://github.com/mcp-hangar/docs/blob/main/operations/RELEASE_COMPATIBILITY.md)
records the supported chart/image/Kubernetes combinations, the verified digests,
and the `cosign verify` recipe.
