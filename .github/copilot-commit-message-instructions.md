# Copilot Commit Message Instructions

When generating a commit message for this repository, follow Conventional
Commits with this project's exact type and scope vocabulary.

## Format

`<type>(<scope>): <subject>`

- `type` (required): one of `feat`, `fix`, `perf`, `refactor`, `docs`,
  `test`, `build`, `ci`, `chore`, `revert`, `security`.
- `scope` (required): one of `hangar`, `operator`, `agent`, `ci`, `docs`,
  `deps`, `infra`, `release`, `repo`. Empty scope is rejected.
- `subject`: imperative mood, total header length <=72 characters.
- `!` after scope (e.g., `feat(hangar)!: ...`) marks a breaking change.

## Subject rules

- Lowercase start preferred; sentence-case start acceptable.
- All-uppercase subjects forbidden.
- Mid-string uppercase characters are allowed: file names, acronyms.
- No trailing period.
- No emoji.

## Examples (accepted)

- `feat(hangar): add resource limits to deployment template`
- `fix(operator): correct RBAC role binding namespace`
- `docs(repo): update CODEOWNERS`
- `chore(deps): bump appVersion to 1.2.0`

## Examples (rejected)

- `Add resource limits` -- missing type and scope
- `feat: add limits` -- missing required scope
- `feat(unknown): add limits` -- scope not in allow-list
- A 73+ character header -- exceeds `header-max-length`
