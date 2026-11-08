# AGENTS.md

Centralized Renovate presets. `default.json` and `presets/*.json` are consumed by other repositories;
`renovate.json` configures this repository. No runtime application or test suite.

## This file

- Edits to AGENTS.md require the user's explicit approval of the specific change.
- Standing instructions only. Never add status, slice, decision (Dnnn), or history entries;
  those belong in `bundle/decisions.md` and `bundle/log.md`.

## Where to look

- [Operating contract](bundle/governance.md): authority, knowledge layers, source evaluation
- [Decisions](bundle/decisions.md): rationale and current authorizations; check before policy-adjacent work
- [Preset management](bundle/preset-management.md): global vs optional presets, current preset inventory
- [Formatting](bundle/formatting.md): OKF metadata, tags, log labels, provenance
- [Enforcement](bundle/enforcement.md): what code owns versus what agents author

## Authority

- The operator decides dependency policy. Passing checks, risk categories, and suggested issue code are not approval.
- Get separate approval of the concrete result before each push, merge, publication, or external change.
- Shared preset behavior changes need representative consumer evidence or an explicit operator exception.
- Never bypass a code owner or modify its machinery as a workaround.
- `sources/evaluate/` holds pending material and draft proposals, not adopted policy.
  Exploratory analysis goes in `research/`.
- Link to other repositories via Git-hosted URLs, never into another local checkout.

## Governed indexes

Never create, edit, or regenerate any bundle `index.md` or `sources/evaluate/index.md` directly.
Run `mise run bundle:finalize` (the pre-commit hook also runs it). If it changes files, review and stage
the generated diff, then retry the commit.

## Commands

Tasks are defined in `mise.toml`; run `mise tasks` to list them. Key tasks:

```bash
mise run validate-renovate-root && mise run validate-renovate-presets   # required before committing
mise run bundle:lint       # governed Markdown
mise run bundle:check      # metadata, links, index drift, capture fidelity
mise run pre-commit-run    # all hooks
```

`--strict` validation proves schema acceptance only, not rule matching, inheritance, or consumer behavior.
Report what remains unverified.

## Pull requests

For PRs touching `default.json`, `renovate.json`, or `presets/*.json`: fill
[the PR template](.github/pull_request_template.md) in a scratch file passed to `gh pr create --body-file`.
Never edit the tracked template. Survey consumer default branches first; report blast radius, required
consumer changes, and operator attention cost. Other PRs: concise summary and verification.

## JSON conventions

- Key order: `$schema` → `description` → `extends` → top-level options → `packageRules`
- 2-space indent, single trailing newline
- Short arrays inline (`["mise"]`); multi-item arrays one item per line
- Every `packageRule` has a `description`
- Files: lowercase-hyphenated. Group names: Title Case. Labels: lowercase-hyphenated.

## Preset rules

- Python runtime caps go in stack presets (`python-mcp.json`, `ansible.json`), never global `mise.json`.
- Automerge risk categories in `bundle/preset-management.md` guide recommendations; they don't authorize changes.

Renovate docs: <https://docs.renovatebot.com/>
