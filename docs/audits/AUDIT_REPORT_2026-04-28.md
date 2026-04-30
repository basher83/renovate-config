# Documentation Audit Report

<!-- rumdl-disable MD013 -->

Generated: 2026-04-28 | Commit: d833dc1

## Scope

This audit checked the repository-owned, user-facing documentation against the current tree and against Renovate validation output. The audited docs were `README.md`, `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `docs/preset-management.md`, and the JSON examples in `examples/`. The copied Renovate reference material under `docs/offical-docs/` was treated as external reference content and was not audited as a local claim surface.

The main evidence sources were `default.json`, `presets/*.json`, `examples/*.json`, `mise.toml`, `.pre-commit-config.yaml`, the current filesystem inventory, `mise run validate-renovate-root`, `mise run validate-renovate-presets`, `npx --yes --package renovate -- renovate-config-validator --strict examples/*.json`, and `mise run markdown-lint`.

## Executive Summary

| Metric | Count |
|--------|-------|
| Documents scanned | 6 |
| Focused claims verified | 58 |
| Verified true | 42 |
| Verified false | 13 |
| Needs review | 3 |

The highest-impact issue is not prose drift; it is that the documented validation gate currently fails. `mise run validate-renovate-root` passes for `default.json` and `renovate.json`, but `mise run validate-renovate-presets` fails on `presets/kubernetes.json` because the validator rejects `managerFilePatterns` under `kubernetes` and under both custom managers. The same rejected field also makes `examples/omni-scale.json` fail direct example validation.

The second major pattern is preset inventory drift. Several docs either omit current presets such as `rust.json` and `kubernetes.json`, list deleted or absent presets such as `infrastructure.json` and `documentation.json`, or describe `presets/` as purely optional even though `default.json` globally extends both `github-actions-security.json` and `mise.json`.

## False Claims Requiring Fixes

| File | Line | Claim | Reality | Fix |
|------|------|-------|---------|-----|
| `README.md` | 48-62 | The available preset list includes `infrastructure.json` and `documentation.json`, and omits `rust.json` and `kubernetes.json`. | `find presets -name '*.json'` shows `ansible.json`, `docker.json`, `github-actions-security.json`, `kubernetes.json`, `mise.json`, `python-mcp.json`, `python.json`, `rust.json`, and `terraform-tofu.json`. There is no `infrastructure.json` or `documentation.json`. | Replace the preset list with the actual inventory. |
| `README.md` | 58 | `mise.json` handles dev tools and runtimes are handled in stack-specific presets. | `presets/mise.json` line 3 says it caps Python at 3.13.x, and lines 6-9 set `allowedVersions` to `<3.14.0` for mise-managed Python. | Describe `mise.json` as globally managing mise tools and globally capping mise-managed Python, or remove the global cap from the preset. |
| `README.md` | 64-65 | Runtime caps are handled in stack-specific presets like `python-mcp.json` or `ansible.json`. | The global `mise.json` preset also contains a Python runtime cap. | Update the note to distinguish the global mise Python cap from stack-specific caps. |
| `README.md` | 95 | The canonical configuration is `presets/default.json`. | The repository has `default.json` at the root and no `presets/default.json`. | Change this to `default.json`. |
| `docs/preset-management.md` | 44 | Only MCP projects should cap Python to 3.13. | `presets/mise.json` globally caps mise-managed Python to `<3.14.0`, and `presets/ansible.json` also caps mise-managed Python to `<3.14.0`. | Reword this example to say MCP projects need the MCP-specific caps, not that only MCP projects should cap Python. |
| `docs/preset-management.md` | 47-48 | Python runtime caps are handled in stack-specific presets. | The globally included `presets/mise.json` also caps mise-managed Python. | Update the note to match the current global cap. |
| `docs/preset-management.md` | 248-257 | The current optional presets are `python.json`, `python-mcp.json`, `docker.json`, `rust.json`, `terraform-tofu.json`, and `ansible.json`. | `presets/kubernetes.json` exists and is extended by `examples/omni-scale.json`, but it is missing from this list. | Add `kubernetes.json`, or remove the file and example if it is not meant to be supported. |
| `CLAUDE.md` | 53 | `default.json` includes `presets/mise.json` globally. | True but incomplete in a way that contradicts line 59. `default.json` lines 7-8 globally extend both `github-actions-security.json` and `mise.json`. | List both globally included presets. |
| `CLAUDE.md` | 59 | Global presets currently include only `mise.json`. | `default.json` globally includes both `github-actions-security.json` and `mise.json`. | Change to “currently `github-actions-security.json` and `mise.json`.” |
| `CLAUDE.md` | 69 | `infrastructure.json` is a key preset. | No `presets/infrastructure.json` exists. | Remove it or add the missing preset. |
| `CLAUDE.md` | 77 | `automergeType: "branch"` means “merges directly to branch without PR.” | Renovate’s current docs describe branch automerge as creating a Renovate branch without a PR, waiting for tests, then automerging the branch commit into the base branch, with a backup PR if tests fail or stay pending. | Reword to “creates no PR initially; merges the passing branch into the base branch; opens a PR only as fallback.” |
| `AGENTS.md` | 46 | `presets/` contains optional presets extended per-project. | `default.json` globally extends two files from `presets/`: `github-actions-security.json` and `mise.json`. | Describe `presets/` as shared presets, some global and some optional. |
| `.github/copilot-instructions.md` | 22-28 | `presets/` contains optional presets and the tree lists the preset set. | The directory includes globally extended presets, and the tree omits `mise.json`, `rust.json`, and `kubernetes.json`. | Update the tree and distinguish global from optional presets. |
| `.github/copilot-instructions.md` | 134-139 | These instructions have been validated against the repository. | Current preset validation fails on `presets/kubernetes.json`, and example validation fails on `examples/omni-scale.json`. | Remove the blanket validation claim or update it after fixing the failing configs. |
| `examples/omni-scale.json` | 12 and 24 | Custom managers use `managerFilePatterns`. | `renovate-config-validator --strict examples/*.json` rejects `customManagers[0].managerFilePatterns` and `customManagers[1].managerFilePatterns`. | Replace with the current Renovate-supported field for regex custom manager file matching. |
| `presets/kubernetes.json` | 5, 16, and 28 | The Kubernetes preset uses `managerFilePatterns`. | `mise run validate-renovate-presets` rejects `kubernetes.managerFilePatterns` and both custom manager `managerFilePatterns` entries. | Replace these fields with the current Renovate-supported configuration shape. |

## Validation Findings

`mise run validate-renovate-root` passed and reported `Config validated successfully` for `default.json` and `renovate.json`.

`mise run validate-renovate-presets` failed. The validator reported these errors for `kubernetes.json`: custom managers contain disallowed `managerFilePatterns`, `customManagers[0].managerFilePatterns` is invalid, `customManagers[1].managerFilePatterns` is invalid, and `kubernetes.managerFilePatterns` is invalid.

Direct example validation with `npx --yes --package renovate -- renovate-config-validator --strict examples/*.json` failed on `examples/omni-scale.json` for the same custom-manager `managerFilePatterns` issue.

`mise run markdown-lint` failed with two issues: `README.md:53` has `MD076` for an unexpected blank line between list items, and `docs/preset-management.md:6` has `MD025` for multiple top-level headings.

## Pattern Summary

| Pattern | Count | Root Cause |
|---------|-------|------------|
| Preset inventory drift | 5 | Presets were added, removed, or globalized without updating every instruction file. |
| Global versus optional confusion | 4 | Docs still describe `presets/` as optional-only even though `default.json` extends two preset files globally. |
| Stale runtime-cap language | 3 | `mise.json` now contains a global Python cap, but prose still says runtime caps live only in stack-specific presets. |
| Validator drift | 2 | `kubernetes.json` and `omni-scale.json` use fields rejected by the current Renovate validator. |

## Human Review Queue

- Review whether the global Python cap in `presets/mise.json` is intentional. If it is intentional, update the philosophy docs. If it is not intentional, move that rule back into stack-specific presets.
- Decide whether `kubernetes.json` is a supported preset. If yes, fix validation and document it in `README.md`, `docs/preset-management.md`, `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md`. If no, remove the file and `examples/omni-scale.json`.
- Decide whether the examples should be minimal examples or real current repo configs. Several examples redundantly extend `github-actions-security.json`, which is already globally included through `default.json`; this is valid but may teach unnecessary extension patterns.

## Sources

Renovate’s current automerge documentation for `automergeType=branch` is at
<https://docs.renovatebot.com/configuration-options/#automergetype> and
<https://docs.renovatebot.com/key-concepts/automerge/#branch-vs-pr-automerging>.
