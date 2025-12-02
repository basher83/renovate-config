# Copilot Instructions for renovate-config

## Repository Overview

This repository contains centralized Renovate presets for dependency management across basher83
repositories. It is a small, configuration-only repository (~60 files) with no build artifacts or
runtime code. All presets are JSON configuration files validated against Renovate's schema.

**Key characteristics:**

- **Type:** Configuration repository (JSON presets)
- **Language:** JSON with Renovate schema
- **Tools:** mise task runner, rumdl markdown linter, npm for renovate-config-validator
- **No tests:** Validation is done via Renovate's schema validator

## Project Structure

```text
renovate-config/
├── default.json              # Base preset extended by all repos
├── renovate.json             # This repo's own Renovate config (dogfooding)
├── presets/                  # Optional presets extended per-project
│   ├── ansible.json          # Ansible collection/role updates
│   ├── docker.json           # Docker security (digest pinning, automerge)
│   ├── github-actions-security.json  # GitHub Actions security
│   ├── python.json           # Python project defaults
│   ├── python-mcp.json       # MCP projects (extends python.json)
│   └── terraform-tofu.json   # Terraform/OpenTofu providers
├── examples/                 # Real-world configuration examples
├── docs/                     # Documentation
│   ├── preset-management.md  # Guidelines for preset organization
│   └── offical-docs/         # Renovate reference documentation
├── mise.toml                 # Task runner configuration
├── .pre-commit-config.yaml   # Pre-commit hooks
├── .rumdl.toml               # Markdown linter configuration
└── cliff.toml                # Changelog generator config
```

## Validation Commands (Required Before Commit)

**Always run these commands to validate changes:**

```bash
# Validate root configs (default.json, renovate.json)
npx --yes --package renovate -- renovate-config-validator --strict default.json renovate.json

# Validate presets (run from presets/ directory)
cd presets && npx --yes --package renovate -- renovate-config-validator --strict *.json
```

**Important:** The `npx` command downloads renovate (~60s first run). Ignore npm deprecation
warnings in output—validation succeeds when output shows `Config validated successfully`.

**Markdown linting (optional, for .md file changes only):**

```bash
pip install rumdl
rumdl check .
```

Note: The repo has pre-existing markdown lint errors in docs/preset-management.md and README.md.
Only fix lint errors in files you modify.

## Making Changes

### Editing Existing Presets

1. Edit the JSON file in `presets/` or `default.json`
2. Validate: `npx --yes --package renovate -- renovate-config-validator --strict <file>`
3. Common mistakes:
   - Missing `$schema` key
   - Invalid `matchCategories`, `matchDatasources`, or `matchManagers` values
   - Incorrect `matchPackageNames` regex syntax (use `/^pattern/` format)

### Creating New Presets

1. Create file in `presets/` with `.json` extension
2. Include required keys:

   ```json
   {
     "$schema": "https://docs.renovatebot.com/renovate-schema.json",
     "description": "Descriptive name for this preset",
     "packageRules": []
   }
   ```

3. Validate before committing

### Key Renovate Concepts

- `matchCategories: ["python"]` - Matches all Python ecosystem packages
- `matchDatasources: ["docker"]` - Matches Docker image dependencies
- `matchManagers: ["github-actions"]` - Matches specific package manager
- `automerge: true` - Auto-merges via PR (default behavior)
- `automergeType: "branch"` - Merges to branch only, PR stays open
- `dependencyDashboardApproval: true` - Requires manual approval via dashboard

### Configuration Inheritance

Repositories extend presets using this syntax:

```jsonc
{
  "extends": [
    "local>basher83/renovate-config",                    // Base preset
    "local>basher83/renovate-config//presets/python.json" // Optional preset
  ]
}
```

## Pre-commit Hooks

This repo uses `prek` for pre-commit hooks. The hooks validate:

- Renovate config syntax
- YAML syntax
- Trailing whitespace
- JSON syntax
- Markdown formatting (via rumdl)

If pre-commit fails, run the validation commands above to identify the issue.

## Writing Style

- Fenced code blocks must have a language specified
- Fenced code blocks must be surrounded by blank lines
- Lists must be surrounded by blank lines
- Bash scripts use `set -euo pipefail`
- Use `rg` instead of `grep` in scripts

## Trust These Instructions

These instructions have been validated against the repository. Trust them and only perform
additional searches if:

- The information appears incomplete for your specific task
- Validation commands fail with unexpected errors
- You need to understand a specific preset's behavior not covered here

Refer to `docs/preset-management.md` for detailed automerge strategy and preset philosophy.
