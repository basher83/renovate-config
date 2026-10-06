# AGENTS.md

Instructions for AI coding agents working in this repository.

## Purpose and governing sources

Configuration-only repository containing centralized Renovate presets for dependency management.
`default.json` and `presets/*.json` implement shared behavior for repositories extending those presets;
`renovate.json` configures this repository itself. There is no runtime application or traditional test suite.

Read the [local operating contract](bundle/governance.md), the
[prospective decision record](bundle/decisions.md), and the
[preset-management guide](bundle/preset-management.md) for this work.
Use [bundle document formatting](bundle/formatting.md) for OKF metadata and provenance style.
The [bundle index](bundle/index.md) routes to local guidance and its captured references.
**The contract is adopted locally.** The operator accepted Slice 1 candidate `33e5e1f29df4` on 2026-10-06;
[decision D005](bundle/decisions.md#2026-10-06--d005-adopt-slice-1-locally) records authority and scope. The completed
shared-policy review is [reconciled](bundle/references/2026-10-06-review-reconciliation.md). Shared adoption and
dependency-policy selection remain separate; #122 stays paused.
CLAUDE.md remains a symlink to this entry point.

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

Slice 1 adopts the local guidance and standalone supporting scripts, with captures retained as evidence. Keep preset
JSON, dogfooding configuration, consumer workflows, CI, hooks, and mise/linter
configuration unchanged. The operator selected retention of both Copilot documents; deletion requires a
separate reviewed change. No commit or publication is authorized by adoption.

## Verification responsibilities

`renovate-config-validator --strict` is the configuration acceptance gate. It does not prove dependency
extraction, rule matching, resolved inheritance, consumer behavior, or policy suitability. For authorized
behavior changes, check the relevant boundary or report what remains unverified. Identify consumer revisions
and environments when claiming downstream results. Branch protection and passing checks are merge conditions.

For documentation changes, review complete bodies, local links, metadata, and actual Markdown lint coverage.
The current umbrella task includes `docs/*.md`, README, and WARP and excludes `.github`; it does not establish
coverage for the new bundle or every agent entry point. Use the scoped command below for Slice 1 files.
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

### Scoped Slice 1 Markdown lint

The installed rumdl supports explicit include overrides and `--no-exclude`. The MD025 override allows an
OKF frontmatter title alongside one body heading. Check the authored Markdown files without changing
persistent linter configuration. Imported source bodies are preserved verbatim and checked for capture fidelity
rather than rewritten to satisfy local prose lint:

```bash
rumdl check --no-cache --no-exclude --config 'MD025.front-matter-title = ""' --deny-config-warnings \
  --include 'AGENTS.md,README.md,bundle/*.md,bundle/references/index.md,bundle/references/2026-*.md,.github/*.md,.github/agents/*.md' \
  AGENTS.md README.md bundle/governance.md bundle/decisions.md bundle/preset-management.md bundle/formatting.md \
  bundle/references/2026-10-06-slice-1-rulings.md \
  bundle/references/2026-10-06-source-captures.md \
  bundle/references/2026-10-06-adoption-rulings.md \
  bundle/references/2026-10-06-review-reconciliation.md \
  .github/copilot-instructions.md .github/agents/renovate-expert.agent.md

# Derived index entries keep frontmatter descriptions byte-identical on one line.
rumdl check --no-cache --no-exclude --config 'MD013.line-length = 240' --deny-config-warnings \
  --include 'bundle/index.md,bundle/references/index.md' bundle/index.md bundle/references/index.md
```

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
├── sources/                  # Discovery and source material
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
