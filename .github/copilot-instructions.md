# Copilot Instructions for renovate-config

## Repository Overview

This repository contains centralized Renovate presets for dependency management across basher83
repositories. It is a small, configuration-only repository with no build artifacts or
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
├── presets/                  # Shared presets, some global and some optional
│   ├── ansible.json          # Ansible collection/role updates
│   ├── docker.json           # Docker security (digest pinning, automerge)
│   ├── github-actions-security.json  # Global GitHub Actions security
│   ├── kubernetes.json       # Kubernetes, Helm, Kustomize, and Talhelper updates
│   ├── mise.json             # Global mise-managed development tool updates
│   ├── python.json           # Python project defaults
│   ├── python-mcp.json       # MCP projects (extends python.json)
│   ├── rust.json             # Rust/Cargo crate updates
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

Markdown lint should pass before commit. If lint fails, fix the reported files before committing.

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
- `automergeType: "branch"` - Creates a Renovate branch without opening a PR first; if checks pass,
  Renovate automerges it into the base branch and opens a PR only as fallback
- `dependencyDashboardApproval: true` - Requires manual approval via dashboard

### Configuration Inheritance

Repositories extend the base preset and any optional presets using this syntax:

```jsonc
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/python.json"
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

## Preset Scope

`default.json` globally includes `github-actions-security.json` and `mise.json`. Python runtime caps
belong in stack-specific presets such as `python-mcp.json` and `ansible.json`, not in the global
`mise.json` preset. Refer to `docs/preset-management.md` for detailed automerge strategy and preset
philosophy.
