---
title: Preset Management Strategy
description: Guidelines for creating and organizing Renovate presets in the shared configuration repository
---

# Preset Management Strategy

This document outlines the standard operating procedures (SOP) for creating and managing Renovate presets
in the shared configuration repository.

## Core Principle: Global vs. Optional Presets

When creating a new preset, determine whether it should be:

1. **Globally included** - Extended in `default.json` for all repositories
2. **Optionally extended** - Repositories explicitly extend it when needed

## Decision Criteria

### Include in `default.json` When

- **Universal tool usage**: The preset manages tools/technologies used in **all or nearly all** repositories
- **Low risk**: The preset rules are safe to apply globally without negative side effects
- **Consistency benefit**: Having consistent behavior across all repos outweighs potential edge cases

**Examples:**

- `mise.json` - All repos use mise for tool management
- Common security presets used universally

### Keep as Optional Preset When

- **Selective usage**: Only specific repositories or project types need the preset
- **High risk**: The preset contains aggressive auto-merge rules or could cause issues if applied broadly
- **Project-specific**: The preset is tailored to specific use cases (e.g., `python-mcp.json` for MCP projects)

**Examples:**

- `python-mcp.json` - Only MCP projects need Python 3.13 cap
- `terraform-tofu.json` - Only infrastructure repos need Terraform-specific rules
- `documentation.json` - Only docs repos need aggressive auto-merge

## Implementation Pattern

### Step 1: Create the Preset

Create a focused preset file in `presets/` directory:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "description": "Universal mise tooling preset - conservative updates for all tool versions",
  "packageRules": [
    {
      "description": "Auto-update utility tools (patch and minor)",
      "matchManagers": ["mise"],
      "matchUpdateTypes": ["patch", "minor"],
      "automerge": true,
      "automergeType": "branch"
    }
  ]
}
```

### Step 2: Add to `default.json` (if globally applicable)

If the preset should apply to all repositories, add it to `default.json`:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "description": "Base Renovate preset for basher83 repositories",
  "extends": [
    "config:best-practices",
    "workarounds:all",
    "local>basher83/renovate-config//presets/mise.json"
  ],
  // ... rest of config
}
```

### Step 3: Update Repository Configs (if globally included)

Repositories that were previously extending the preset explicitly can now remove it:

**Before:**

```json
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/mise.json",
    "local>basher83/renovate-config//presets/python-mcp.json"
  ]
}
```

**After:**

```json
{
  "extends": [
    "local>basher83/renovate-config",
    "local>basher83/renovate-config//presets/python-mcp.json"
  ]
}
```

## Benefits of This Approach

1. **DRY Principle**: Common presets are defined once and inherited automatically
2. **Consistency**: All repositories get the same base behavior without manual configuration
3. **Maintainability**: Update preset rules in one place, affects all repos
4. **Simplicity**: Repository configs are cleaner and easier to understand
5. **Flexibility**: Repositories can still override or extend with additional presets

## Current Global Presets

The following presets are included in `default.json`:

- `mise.json` - Universal mise tool management (auto-merge patches/minors, pin critical tools)

## Current Optional Presets

The following presets are available but must be explicitly extended:

- `python.json` - Python project defaults
- `python-mcp.json` - MCP-specific Python rules (Python 3.13 cap)
- `docker.json` - Docker security and digest pinning
- `github-actions-security.json` - GitHub Actions security rules
- `terraform-tofu.json` - Terraform/OpenTofu provider/module rules
- `ansible.json` - Ansible collection/role updates
- `infrastructure.json` - Infrastructure-as-Code comprehensive preset
- `documentation.json` - Documentation site aggressive auto-merge

## Migration Checklist

When promoting a preset from optional to global:

- [ ] Verify the preset is safe to apply globally
- [ ] Confirm all or nearly all repos would benefit
- [ ] Add preset to `default.json` extends array
- [ ] Validate `default.json` configuration
- [ ] Update repository configs to remove explicit preset extension
- [ ] Test in a sample repository to ensure behavior is correct
- [ ] Document the change in this file

## Best Practices

1. **Keep presets focused**: Each preset should have a single, clear purpose
2. **Use descriptive names**: Preset filenames should clearly indicate their purpose
3. **Document decisions**: Add comments in preset files explaining why certain rules exist
4. **Test before globalizing**: Always test preset changes before adding to `default.json`
5. **Version control**: Use git tags for preset versions if needed for stability
6. **Review regularly**: Periodically review which presets should be global vs. optional
