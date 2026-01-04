# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Centralized Renovate presets for dependency management across repositories.
`default.json` provides base config that all repos inherit; optional presets in `presets/` are
extended per-project.

## References

Canonical source: [Renovate Documentation](https://docs.renovatebot.com/)

Always validate settings using the webfetch tool. Quick reference:

`WebFetch(domain:docs.renovatebot.com)` - Main landing page
`WebFetch(domain:docs.renovatebot.com/config-overview/)` - Config overview
`WebFetch(domain:docs.renovatebot.com/configuration-options/)` - Configuration options
`WebFetch(domain:docs.renovatebot.com/config-validation/)` - Config validation
`WebFetch(domain:docs.renovatebot.com/dependency-pinning/)` - Dependency pinning
`WebFetch(domain:docs.renovatebot.com/key-concepts/presets/)` - Presets
`WebFetch(domain:docs.renovatebot.com/presets-config/)` - Presets config
`WebFetch(domain:docs.renovatebot.com/presets-default/)` - Presets default
`WebFetch(domain:docs.renovatebot.com/key-concepts/how-renovate-works/)` - How Renovate works
`WebFetch(domain:docs.renovatebot.com/key-concepts/automerge/)` - Automerge

## Commands

```bash
# Validate all preset files
mise run validate-renovate-presets

# Validate root config files (default.json, renovate.json)
mise run validate-renovate-root

# Run pre-commit hooks
mise run pre-commit-run

# Lint markdown files
mise run markdown-lint

# Fix markdown formatting
mise run markdown-fix
```

## Architecture

**Configuration Inheritance:**

- `default.json` - Base preset extended by all repos (`local>basher83/renovate-config`)
  - Extends `config:best-practices` and `workarounds:all`
  - Includes `presets/mise.json` globally
- `presets/*.json` - Optional presets extended per-project (e.g., `local>basher83/renovate-config//presets/python.json`)
- `renovate.json` - This repo's own Renovate config (dogfooding)

**Preset Philosophy:**

- Global presets (in `default.json`): Only tools used universally (currently just `mise.json`)
- Optional presets: Project-specific configs that repos explicitly extend

**Key Presets:**

- `python.json` - Auto-merges patches, groups linters/test tools
- `python-mcp.json` - MCP projects with Python version constraints (extends `python.json`)
- `docker.json` - Digest pinning, auto-merge patches/digests, approval for critical images
- `github-actions-security.json` - Groups updates, auto-merges digests/patches/minor
- `infrastructure.json` - Comprehensive IaC preset

## Renovate Concepts

- `matchCategories: ["python"]` - Matches all Python ecosystem packages
- `matchDatasources: ["docker"]` - Matches Docker image dependencies
- `matchManagers: ["mise"]` - Matches specific package manager
- `automergeType: "branch"` - Merges directly to branch without PR
- `dependencyDashboardApproval: true` - Requires manual approval via dashboard
