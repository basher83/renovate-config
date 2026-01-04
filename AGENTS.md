# AGENTS.md

Instructions for AI coding agents working in this repository.

## Repository Overview

Configuration-only repository containing centralized Renovate presets for dependency management.
No runtime code - only JSON configuration files validated against Renovate's schema.

- **Primary files**: `default.json` (base preset), `presets/*.json` (optional presets)
- **Validation**: `renovate-config-validator --strict` is the quality gate
- **No tests**: Schema validation replaces traditional testing

## Commands

```bash
mise run validate-renovate-root      # Validate default.json, renovate.json
mise run validate-renovate-presets   # Validate all presets/*.json files
mise run pre-commit-run              # Run all pre-commit hooks
mise run markdown-lint               # Lint markdown files
mise run markdown-fix                # Fix markdown formatting
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
├── default.json              # Base preset - ALL repos inherit this
├── renovate.json             # This repo's own config (dogfooding)
├── presets/                  # Optional presets extended per-project
│   ├── python.json, python-mcp.json, docker.json
│   ├── ansible.json, mise.json, terraform-tofu.json
│   └── github-actions-security.json
├── examples/                 # Real-world configuration examples
└── docs/                     # Documentation and reference material
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
automergeType: "branch"            # Branch-only, PR stays open
dependencyDashboardApproval: true  # Require manual approval
pinDigests: true                   # Pin to SHA digests
allowedVersions: "<3.14.0"         # Version constraints
groupName: "..."                   # Group updates together
```

## Configuration Inheritance

```text
config:best-practices + workarounds:all
    └── default.json (extends built-ins, includes global presets)
        └── Repository renovate.json (extends default + optional presets)
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

## Automerge Philosophy

**Safe (automerge: true)**:
Digest updates, patch updates, dev/test minor updates, non-critical Docker patches

**Risky (no automerge or require approval)**:
Major updates, security-sensitive Actions, critical Docker images, Terraform majors

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
- [Presets](https://docs.renovatebot.com/key-concepts/presets/)
- [Automerge](https://docs.renovatebot.com/key-concepts/automerge/)
