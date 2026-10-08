# AGENTS.md

Instructions for AI coding agents working in this repository.

## Governing ownership boundary

Agents author within authorized scope. Repository code owns designated structure and metadata, finalizes
those outputs at defined boundaries, and verifies persisted results. Passing checks does not grant authority
for policy acceptance, verification, commit, or publication. Read [enforcement](bundle/enforcement.md) for
current versus proposed ownership; never bypass a code owner or change its machinery as a workaround.

## Purpose and governing sources

Configuration-only repository containing centralized Renovate presets for dependency management.
`default.json` and `presets/*.json` implement shared behavior for repositories extending those presets;
`renovate.json` configures this repository itself. There is no runtime application or traditional test suite.

Read the [local operating contract](bundle/governance.md), the
[prospective decision record](bundle/decisions.md), and the
[preset-management guide](bundle/preset-management.md) for this work.
Use root [log.md](bundle/log.md) for the chronological trail and decisions.md for material rationale.
Use [bundle document formatting](bundle/formatting.md) for OKF metadata and provenance style.
The [bundle index](bundle/index.md) routes to local knowledge and supporting tools.
Read the [knowledge layers and source evaluation criteria](bundle/governance.md#knowledge-layers-and-source-evaluation)
before admitting evidence or promoting knowledge. [Sources to evaluate](sources/evaluate/index.md) are pending, not
adopted.
This bundle is an exemplar within this repository; standalone distribution is not required. Local resource
and source paths may leave `bundle/` but must resolve within this repository, including through symlinks.
Use Git-hosted artifact URLs for material in other repositories; do not link into another local checkout.
**The prior contract is adopted locally; the exemplar documentation revision is a candidate.**
The operator accepted Slice 1 candidate `33e5e1f29df4` on 2026-10-06;
[decision D005](bundle/decisions.md#2026-10-06--d005-adopt-slice-1-locally) records authority and scope. The completed
shared-policy review is [reconciled](sources/evaluate/2026-10-06-review-reconciliation.md). Shared adoption and
dependency-policy selection remain separate; #122 stays paused.
CLAUDE.md remains a symlink to this entry point.

## Governed indexes

Agents must never issue direct filesystem, editor, shell, or script tool calls targeting a governed `index.md`.
Agents author permitted source and concept documents; deterministic code owns index files. Do not manually
create, edit, repair, reorder, or regenerate an individual index. Use the repository's mise interface:
`mise run bundle:finalize` finalizes the complete declared scope; `mise run bundle:check` checks it.
The governed indexes are every bundle directory's `index.md` plus `sources/evaluate/index.md`.
The configured pre-commit hook automatically calls `mise run bundle:finalize`, before commit and therefore
before ordinary publication of that commit. If generation modifies files, the hook stops the commit so the
generated diff can be reviewed and included before retrying. Do not bypass the hook to publish stale outputs.
Index files provide navigation; governance semantics belong in their owning documents.
See [index ownership](bundle/formatting.md#generate-governed-indexes).

Bundle concepts use only the accepted tags `governance`, `enforcement`, `formatting`, and `presets`.
Descriptions are single complete sentences; in-bundle links begin with `/`. Logs use only `**Update**`,
`**Creation**`, and `**Deprecation**` as leading labels. Follow the [owning formatting rules](bundle/formatting.md)
for binding versus derivation, provenance, and the human PR acceptance needed to extend vocabulary.

## Change protocol and authority

- Read the task and relevant discussion. Separate investigation, policy selection, implementation, and maintenance.
- For material work, name the authorized outcome, affected surfaces and consumers, exclusions, and completion condition.
- The operator decides dependency policy. Suggested issue code, broad risk categories, and passing checks are not approval.
- Use existing task authorization for preparation and commits; surface unresolved consequential operator choices.
- Obtain separate approval of the concrete result before each push, merge, publication, or external change.
- For shared preset behavior changes, require representative consumer evidence or an explicit operator exception.
- Preserve unrelated work and distinguish preparation, adoption, implementation, commit, and publication authority.
- Keep decisions and rationale discoverable; do not manufacture historical approval for operative JSON.
- Specialist capability and tool access do not authorize consumer edits, organization changes, or new enforcement.

Slice 1 adopted local guidance and standalone supporting scripts. D007 corrects the capture placement:
records in `sources/evaluate/` await evaluation; prior capture and citation do not establish acceptance. Keep preset
JSON, dogfooding configuration, and consumer workflows unchanged. D009 authorizes mise index finalization;
D011 authorizes the authored-document lint task and capture-preserving hook reconciliation.
The operator selected retention of both Copilot documents; deletion
requires a
separate reviewed change. No commit or publication is authorized by adoption.

## Verification responsibilities

`renovate-config-validator --strict` is the configuration acceptance gate. It does not prove dependency
extraction, rule matching, resolved inheritance, consumer behavior, or policy suitability. For authorized
behavior changes, check the relevant boundary or report what remains unverified. Identify consumer revisions
and environments when claiming downstream results. Branch protection and passing checks are merge conditions.

For documentation changes, review complete bodies, local links, metadata, and actual Markdown lint coverage.
The current umbrella task includes `docs/*.md`, README, and WARP and excludes `.github`; it does not establish
coverage for the bundle or every agent entry point. Use `mise run bundle:lint` for governed Markdown.
Do not assume validation was executed from a proposed command or install tooling merely to satisfy retained examples.
Use the [standalone bundle checks](bundle/formatting.md#use-standalone-deterministic-checks) for metadata,
source joins, index drift, and capture fidelity. They do not establish factual accuracy or adoption.

## Commands

```bash
mise run validate-renovate-root      # Validate default.json, renovate.json
mise run validate-renovate-presets   # Validate all presets/*.json files
mise run pre-commit-run              # Run all pre-commit hooks
mise run markdown-lint               # Lint files covered by .rumdl.toml
mise run markdown-fix                # Fix files covered by .rumdl.toml
```

### Governed Markdown lint

```bash
mise run bundle:lint
```

This task discovers authored bundle concepts and history, authored evaluation records, AGENTS.md, README.md,
and retained `.github` instructions. It checks generated indexes separately with a 240-character limit so
metadata descriptions remain intact. The concept override permits an OKF frontmatter title alongside a body
heading. Imported captures retain their bytes and are checked for fidelity rather than local prose style.
The pre-commit pipeline runs both bundle finalization and this lint task through mise.

### Direct Validation

```bash
# Validate specific file
npx --yes --package renovate -- renovate-config-validator --strict default.json

# Validate single preset
npx --yes --package renovate -- renovate-config-validator --strict presets/python.json

# Validate all presets (from presets/ directory)
cd presets && npx --yes --package renovate -- renovate-config-validator --strict *.json
```

First run downloads renovate (~60s). Ignore npm deprecation warnings.
Success: `Config validated successfully`.

## File Structure

```text
renovate-config/
├── default.json              # Base preset for repos extending it
├── renovate.json             # This repo's own config (dogfooding)
├── presets/                  # Shared presets, some global and some optional
│   ├── github-actions-security.json, mise.json
│   ├── python.json, python-mcp.json, docker.json
│   ├── ansible.json, rust.json, terraform-tofu.json
│   └── kubernetes.json, javascript.json
├── examples/                 # Real-world configuration examples
├── bundle/                   # Local contract, decisions, and preset guide
├── sources/                  # Source material; evaluate/ records pending evaluation
├── research/                 # Provisional synthesis, when needed
└── docs/                     # Historical audits and upstream reference mirrors
```

## JSON Formatting

### Required Structure

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "description": "Brief description of preset purpose",
  "packageRules": []
}
```

### Key Ordering

`$schema` → `description` → `extends` → top-level options → `packageRules`

### Formatting Rules

- 2-space indentation, no trailing commas (standard JSON)
- Files end with single newline
- Short arrays on single line: `["mise"]`
- Multi-item arrays: one item per line
- Every `packageRule` must have a `description` field

### PackageRule Example

```json
{
  "description": "Auto-merge Python patch updates (PR merge)",
  "matchCategories": ["python"],
  "matchUpdateTypes": ["patch"],
  "automerge": true
}
```

## Naming Conventions

**Files**: Lowercase with hyphens (`python-mcp.json`, `github-actions-security.json`)
**Groups**: Title case (`"Python test dependencies"`, `"Terraform Providers (Minor)"`)
**Labels**: Lowercase, hyphenated (`"renovate"`, `"github-actions"`)

## Renovate Concepts

### Matchers

```text
matchCategories: ["python"]              # All Python packages
matchDatasources: ["docker"]             # Docker images
matchManagers: ["mise", "github-actions"] # Package managers
matchUpdateTypes: ["digest", "patch", "minor", "major"]
matchDepTypes: ["devDependencies", "provider", "module"]
matchPackageNames: ["/^pattern/", "exact-name"]  # Regex or exact
```

### Actions

```text
automerge: true                    # Auto-merge via PR (default)
automergeType: "branch"            # Create branch first, merge passing branch without PR
dependencyDashboardApproval: true  # Require manual approval
pinDigests: true                   # Pin to SHA digests
allowedVersions: "<3.14.0"         # Version constraints
groupName: "..."                   # Group updates together
```

## Configuration Inheritance

```text
config:best-practices + workarounds:all
    └── default.json (extends built-ins plus github-actions-security.json and mise.json)
        └── Repository renovate.json (extends default plus optional presets)
```

Extension syntax:

```json
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/python.json"
  ]
}
```

## Presets

Global presets are included by `default.json`: currently `github-actions-security.json` and `mise.json`.
They apply to repositories inheriting the base, subject to local overrides. Optional presets are extended
explicitly per repository. This list describes configured behavior, not an inventory of all consumers.

- `python.json` — Auto-merges patches, groups linters, test tools, and type stubs
- `python-mcp.json` — MCP projects with Python version constraints (extends `python.json`)
- `docker.json` — Digest pinning, auto-merge patches/digests, approval for critical images
- `kubernetes.json` — Kubernetes manifests, Helm charts, Kustomize, and Talhelper updates
- `rust.json` — Auto-merges patches, groups ecosystem crates (Tokio, Serde, observability), approval for critical majors
- `javascript.json` — Auto-merges patches, groups linters, test tools, and TypeScript type definitions (npm & Bun)
- `github-actions-security.json` — Groups updates, auto-merges digests/patches/minor
- `mise.json` — Groups and auto-merges mise-managed development tool updates
- `ansible.json` — Ansible collection/role updates with an Ansible-specific mise Python cap
- `terraform-tofu.json` — Terraform/OpenTofu provider and module rules

## Automerge guidance and current configuration

The broad categories below guide investigation and recommendations; they do not authorize selecting or
changing shared dependency policy. Consult the actual JSON, matched rules, and applicable approved decision.
Passing schema checks or classifying an update as low risk does not itself establish suitability.

**Generally lower risk, often configured with `automerge: true`**:
Digest updates, patch updates, dev/test minor updates, non-critical Docker patches

**Generally higher risk, often without automerge or with approval requirements**:
Major updates, security-sensitive Actions, critical Docker images, Terraform majors

Python runtime caps belong in stack-specific presets such as `python-mcp.json` and `ansible.json`,
not in the global `mise.json` preset.

## Validation

Always validate before committing:

```bash
mise run validate-renovate-root && mise run validate-renovate-presets
```

Common errors: missing `$schema`, invalid matcher values, bad regex syntax, trailing commas

## Writing Style

- Fenced code blocks: always specify language, surround with blank lines
- Lists: surround with blank lines
- Scripts: use `rg` instead of `grep`, bash uses `set -euo pipefail`

## Reference

Canonical: <https://docs.renovatebot.com/>

- [Config overview](https://docs.renovatebot.com/config-overview/)
- [Configuration options](https://docs.renovatebot.com/configuration-options/)
- [Config validation](https://docs.renovatebot.com/config-validation/)
- [Dependency pinning](https://docs.renovatebot.com/dependency-pinning/)
- [How Renovate works](https://docs.renovatebot.com/key-concepts/how-renovate-works/)
- [Presets](https://docs.renovatebot.com/key-concepts/presets/)
- [Automerge](https://docs.renovatebot.com/key-concepts/automerge/)
