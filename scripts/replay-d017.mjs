#!/usr/bin/env node
/**
 * D017 replay: applyPackageRules for mise/terraform presets (Renovate 44.x).
 */
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';

const [runtime, root] = process.argv.slice(2);
if (!runtime || !root) {
  console.error(
    'Usage: node scripts/replay-d017.mjs <renovate-dist-dir> <renovate-config-repo-root>',
  );
  process.exit(1);
}
const load = (rel) => import(pathToFileURL(path.join(runtime, rel)).href);
const { init: initLogger } = await load('logger/index.js');
process.env.LOG_LEVEL = 'error';
await initLogger();
const { applyPackageRules } = await load('util/package-rules/index.js');
const { mergeChildConfig } = await load('config/utils.js');
const { getConfig } = await load('config/defaults.js');
const { generateBranchName } = await load('workers/repository/updates/branch-name.js');
const { generateBranchConfig } = await load('workers/repository/updates/generate.js');
const { classifyRelease } = await load('workers/repository/process/lookup/update-type.js');
const { api: hashicorp } = await load('modules/versioning/hashicorp/index.js');

function sha256File(rel) {
  return createHash('sha256').update(fs.readFileSync(path.join(root, rel))).digest('hex');
}

function readJson(rel) {
  return JSON.parse(fs.readFileSync(path.join(root, rel), 'utf8'));
}

function project(obj) {
  return {
    automerge: obj.automerge,
    dependencyDashboardApproval: obj.dependencyDashboardApproval,
    groupName: obj.groupName,
    groupSlug: obj.groupSlug,
    minimumReleaseAge: obj.minimumReleaseAge,
    allowedVersions: obj.allowedVersions,
  };
}

function buildBaseConfig() {
  const d = readJson('default.json');
  const mise = readJson('presets/mise.json');
  const gha = readJson('presets/github-actions-security.json');
  return mergeChildConfig(getConfig(), mergeChildConfig(d, mergeChildConfig(gha, mise)));
}

function buildZammadConfig() {
  const pythonMcp = readJson('presets/python-mcp.json');
  const docker = readJson('presets/docker.json');
  const localRules = {
    packageRules: [
      {
        description: 'Keep Python pinned below 3.14 until MCP SDK v1.x officially supports it',
        matchDepNames: ['python'],
        allowedVersions: '<3.14',
      },
      {
        description: 'Update the uv pins in mise.toml and the uv-pre-commit hook in one PR',
        matchDepNames: ['uv', 'astral-sh/uv-pre-commit'],
        groupName: 'uv version pins',
      },
    ],
  };
  let cfg = buildBaseConfig();
  cfg = mergeChildConfig(cfg, pythonMcp);
  cfg = mergeChildConfig(cfg, docker);
  cfg = mergeChildConfig(cfg, localRules);
  return cfg;
}

function buildTerraformConfig() {
  return mergeChildConfig(buildBaseConfig(), readJson('presets/terraform-tofu.json'));
}

async function apply(cfg, dep) {
  const merged = await applyPackageRules({
    ...cfg,
    ...dep,
    packageName: dep.packageName ?? dep.depName,
    packageFile: dep.packageFile ?? 'fixture',
  });
  return project(merged);
}

const pc47 = [
  { depName: 'python', manager: 'mise', updateType: 'minor', currentValue: '3.14.8' },
  { depName: 'uv', manager: 'mise', updateType: 'minor', currentValue: '0.12.23' },
  { depName: 'node', manager: 'mise', updateType: 'minor', currentValue: '26.10.0' },
];

const results = {
  purpose:
    'Replay D017 mise/terraform preset rules: personal-computing#47 bundle, terraform required_provider patch, Zammad-MCP local caps/groups, tool and fallback cases, branch-level grouping for two extending consumers, and open Terraform provider PRs on two terraform-tofu consumers.',
  completed_at: new Date().toISOString(),
  runtime: { version: '44.145.1', node: process.version },
  candidate_presets: {
    'presets/mise.json': { sha256: sha256File('presets/mise.json') },
    'presets/terraform-tofu.json': { sha256: sha256File('presets/terraform-tofu.json') },
  },
  personal_computing_47: [],
  terraform_required_provider_patch: null,
  zammad_mcp_mise: [],
  vulnerability_alert_control: null,
  limits:
    'Merged local preset bytes only; built-in preset expansion differs from hosted preset fetch. Branch replay groups fixture upgrades with generateBranchName and generateBranchConfig; it does not run lookup, branchify filtering, or the dashboard. Terraform update types are derived from the fixture current and new versions with Renovate classifyRelease and hashicorp versioning, not from lookup; range pins (proxmox ~> 0.90, ~> 0.111.0) use the range floor as the current version, and 0.x steps such as infisical 0.19.20 to 0.20.3 classify as minor.',
};

const base = buildBaseConfig();
for (const dep of pc47) {
  const after = await apply(base, dep);
  results.personal_computing_47.push({ dep, after });
  assert.equal(after.automerge, false, dep.depName);
  assert.equal(after.dependencyDashboardApproval, true, dep.depName);
}

const tfCfg = buildTerraformConfig();
const tfDep = {
  depName: 'aws',
  manager: 'terraform',
  depType: 'required_provider',
  updateType: 'patch',
  currentValue: '5.92.0',
  packageName: 'hashicorp/aws',
};
results.terraform_required_provider_patch = {
  dep: tfDep,
  after: await apply(tfCfg, tfDep),
};
assert.equal(results.terraform_required_provider_patch.after.automerge, true);

const providerBlockDep = { ...tfDep, depType: 'provider' };
results.terraform_provider_block_patch = {
  dep: providerBlockDep,
  after: await apply(tfCfg, providerBlockDep),
};
assert.equal(results.terraform_provider_block_patch.after.automerge, true);

// Terraform consumer replay: open provider PRs at the inventory revisions, with the candidate preset
// and the base preset (identical except that its provider rules omit required_provider).
const tfPreset = readJson('presets/terraform-tofu.json');
const legacyTfPreset = structuredClone(tfPreset);
for (const rule of legacyTfPreset.packageRules) {
  if (rule.matchDepTypes) {
    rule.matchDepTypes = rule.matchDepTypes.filter((t) => t !== 'required_provider');
  }
}
const tfConsumers = [
  {
    repo: 'basher83/Triangulum-Prime',
    sha: '32c06140ca203fa8bfa73204b50c7144dfa82a16',
    presets: [],
    deps: [
      {
        pr: 111,
        headRef: 'renovate/proxmox-0.x',
        depName: 'proxmox',
        packageName: 'bpg/proxmox',
        currentValue: '~> 0.90',
        currentVersion: '0.90.0',
        newValue: '~> 0.116',
        newVersion: '0.116.0',
      },
      {
        pr: 113,
        headRef: 'renovate/scalr-3.x',
        depName: 'scalr',
        packageName: 'scalr/scalr',
        currentValue: '3.12.0',
        currentVersion: '3.12.0',
        newValue: '3.19.0',
        newVersion: '3.19.0',
      },
    ],
  },
  {
    repo: 'basher83/Supernova-MicroK8s-Infra',
    sha: '68e15d0d058f923fb0d9cd1804a39027c4e7bf0c',
    presets: ['presets/python.json', 'presets/ansible.json'],
    deps: [
      {
        pr: 83,
        headRef: 'renovate/proxmox-0.x',
        depName: 'proxmox',
        packageName: 'bpg/proxmox',
        currentValue: '~> 0.111.0',
        currentVersion: '0.111.0',
        newValue: '~> 0.116.0',
        newVersion: '0.116.0',
      },
      {
        pr: 76,
        headRef: 'renovate/infisical-0.x',
        depName: 'infisical',
        packageName: 'infisical/infisical',
        currentValue: '0.19.20',
        currentVersion: '0.19.20',
        newValue: '0.20.3',
        newVersion: '0.20.3',
      },
    ],
  },
];

async function replayTerraformBranches(consumer, tfRules) {
  let cfg = buildBaseConfig();
  for (const rel of consumer.presets) cfg = mergeChildConfig(cfg, readJson(rel));
  cfg = mergeChildConfig(cfg, tfRules);
  const branches = new Map();
  for (const { pr, headRef: _headRef, ...d } of consumer.deps) {
    const [newMajor, newMinor] = d.newVersion.split('.').map(Number);
    const updateType = classifyRelease(hashicorp, d.currentVersion, d.newVersion);
    assert.equal(updateType, 'minor', `${consumer.repo} #${pr} classification`);
    const upgrade = await applyPackageRules({
      ...cfg,
      ...d,
      manager: 'terraform',
      depType: 'required_provider',
      updateType,
      depNameSanitized: d.depName,
      packageFile: 'versions.tf',
      newMajor,
      newMinor,
    });
    upgrade.pr = pr;
    generateBranchName(upgrade);
    if (!branches.has(upgrade.branchName)) branches.set(upgrade.branchName, []);
    branches.get(upgrade.branchName).push(upgrade);
  }
  return [...branches].map(([branchName, upgrades]) => {
    const branch = generateBranchConfig(upgrades);
    return {
      branchName,
      prs: upgrades.map((u) => u.pr),
      updateTypes: upgrades.map((u) => u.updateType),
      groupName: branch.groupName ?? null,
      schedule: branch.schedule,
      dependencyDashboardApproval: branch.dependencyDashboardApproval,
      automerge: branch.automerge,
    };
  });
}

results.terraform_consumer_replay = {
  source:
    'Provider pins and open PR targets from the 2026-10-12 inventory. Update types come from Renovate classifyRelease with hashicorp versioning; range current versions use the range floor.',
  consumers: [],
};
for (const consumer of tfConsumers) {
  const before = await replayTerraformBranches(consumer, legacyTfPreset);
  const after = await replayTerraformBranches(consumer, tfPreset);
  results.terraform_consumer_replay.consumers.push({ repo: consumer.repo, sha: consumer.sha, before, after });
  assert.equal(before.length, consumer.deps.length, `${consumer.repo} base preset leaves one branch per PR`);
  for (const branch of before) {
    assert.equal(branch.groupName, null, `${consumer.repo} base preset rules are inert`);
    const live = consumer.deps.find((d) => d.pr === branch.prs[0]).headRef;
    assert.equal(branch.branchName, live, `${consumer.repo} base replay reproduces the live PR branch`);
  }
  assert.equal(after.length, 1, `${consumer.repo} candidate groups provider minors`);
  assert.equal(after[0].branchName, 'renovate/terraform-providers-(minor)');
  assert.deepEqual(after[0].schedule, ['before 5am on Monday']);
  assert.equal(after[0].dependencyDashboardApproval, false);
  assert.equal(after[0].automerge, false);
}

const zcfg = buildZammadConfig();
for (const dep of [
  { depName: 'python', manager: 'mise', updateType: 'minor', currentValue: '3.13.2' },
  { depName: 'uv', manager: 'mise', updateType: 'minor', currentValue: '0.12.23' },
]) {
  results.zammad_mcp_mise.push({ dep, after: await apply(zcfg, dep) });
}
assert.ok(
  ['<3.14', '<3.14.0'].includes(results.zammad_mcp_mise[0].after.allowedVersions),
  'python cap from python-mcp + local rules',
);
assert.equal(results.zammad_mcp_mise[1].after.automerge, false);

const vulnerabilityAlerts = readJson('default.json').vulnerabilityAlerts;
assert.equal(
  vulnerabilityAlerts?.minimumReleaseAge,
  null,
  'default.json vulnerabilityAlerts.minimumReleaseAge',
);
const vulnBase = mergeChildConfig(base, {
  packageRules: [
    {
      description: 'Simulated platform vulnerability alert rule (Renovate init)',
      matchManagers: ['mise'],
      matchDepNames: ['uv'],
      isVulnerabilityAlert: true,
      force: { ...vulnerabilityAlerts },
    },
  ],
});
const vulnUv = await apply(vulnBase, {
  depName: 'uv',
  manager: 'mise',
  updateType: 'patch',
  currentValue: '0.12.23',
  isVulnerabilityAlert: true,
});
results.vulnerability_alert_control = {
  dep: 'uv patch vulnerability alert (simulated alert packageRule + force)',
  default_vulnerability_alerts: { minimumReleaseAge: vulnerabilityAlerts.minimumReleaseAge },
  after: vulnUv,
  note: 'Preset must not use isVulnerabilityAlert as a matcher; hosted alerts apply force from vulnerabilityAlerts.',
};
assert.equal(vulnUv.minimumReleaseAge, null, 'vulnerability alert force clears minimumReleaseAge');

// Per-dependency coverage requested in review: 0.x tool patch, 1.x+ tool minor, unlisted plugin.
results.tool_and_fallback_cases = [];
for (const [dep, expected] of [
  [
    { depName: 'uv', manager: 'mise', updateType: 'patch', currentValue: '0.12.23' },
    { automerge: true, dependencyDashboardApproval: false, groupSlug: 'mise-tools' },
  ],
  [
    { depName: 'rg', manager: 'mise', updateType: 'minor', currentValue: '15.1.0' },
    { automerge: true, dependencyDashboardApproval: false, groupSlug: 'mise-tools' },
  ],
  [
    { depName: 'gh-aw', manager: 'mise', updateType: 'minor', currentValue: '0.82.14' },
    { automerge: false, dependencyDashboardApproval: true, groupSlug: 'mise-tools-approval' },
  ],
  [
    { depName: 'npm:llm-checker', manager: 'mise', updateType: 'minor', currentValue: '3.8.1' },
    { automerge: false, dependencyDashboardApproval: true, groupSlug: 'mise-unspecified' },
  ],
  [
    { depName: 'npm:llm-checker', manager: 'mise', updateType: 'patch', currentValue: '3.8.1' },
    { automerge: false, dependencyDashboardApproval: false, groupSlug: null },
  ],
]) {
  const after = await apply(base, dep);
  results.tool_and_fallback_cases.push({ dep, after });
  for (const [key, value] of Object.entries(expected)) {
    assert.equal(after[key] ?? null, value, `${dep.depName} ${dep.updateType} ${key}`);
  }
}

// Branch-level replay: Renovate sets branch approval when any grouped update needs it and
// automerge only when every grouped update automerges (generateBranchConfig), so each
// update's own result must survive grouping.
const consumers = [
  {
    repo: 'basher83/prompting-eval-workbench',
    sha: '55d2017d1f07b95ef51e86dc7ef289632836183e',
    deps: [
      { depName: 'python', updateType: 'patch', currentValue: '3.14.7', newValue: '3.14.8' },
      { depName: 'node', updateType: 'minor', currentValue: '24.19.0', newValue: '24.20.0' },
      { depName: 'uv', updateType: 'minor', currentValue: '0.12.3', newValue: '0.13.0' },
      { depName: 'ruff', updateType: 'patch', currentValue: '0.16.2', newValue: '0.16.3' },
      { depName: 'hk', updateType: 'minor', currentValue: '1.54.1', newValue: '1.55.0' },
      { depName: 'watchexec', updateType: 'patch', currentValue: '2.5.1', newValue: '2.5.2' },
    ],
  },
  {
    repo: 'basher83/lunar-claude',
    sha: 'e81cabf81e7c58eb90b2dc656c8bc15d4a23227b',
    deps: [
      { depName: 'python', updateType: 'minor', currentValue: '3.14.6', newValue: '3.15.0' },
      { depName: 'uv', updateType: 'minor', currentValue: '0.11.28', newValue: '0.13.0' },
      { depName: 'rg', updateType: 'minor', currentValue: '15.1.0', newValue: '15.2.0' },
      { depName: 'fnox', updateType: 'patch', currentValue: '1.29.0', newValue: '1.29.1' },
    ],
  },
];
results.branch_replay = { source: 'Pins from the 2026-10-12 inventory; update targets are hypothetical.', consumers: [] };
for (const consumer of consumers) {
  const branches = new Map();
  for (const d of consumer.deps) {
    const [newMajor, newMinor] = d.newValue.split('.').map(Number);
    const upgrade = await applyPackageRules({
      ...base,
      ...d,
      manager: 'mise',
      packageName: d.depName,
      depNameSanitized: d.depName,
      packageFile: 'mise.toml',
      newVersion: d.newValue,
      newMajor,
      newMinor,
    });
    generateBranchName(upgrade);
    assert.ok(upgrade.branchName, `${d.depName} branchName`);
    if (!branches.has(upgrade.branchName)) branches.set(upgrade.branchName, []);
    branches.get(upgrade.branchName).push(upgrade);
  }
  const out = [];
  for (const [branchName, upgrades] of branches) {
    const branch = generateBranchConfig(upgrades);
    out.push({
      branchName,
      deps: upgrades.map((u) => `${u.depName} ${u.updateType}`),
      dependencyDashboardApproval: branch.dependencyDashboardApproval,
      automerge: branch.automerge,
    });
    for (const u of upgrades) {
      assert.equal(
        Boolean(u.automerge),
        branch.automerge,
        `${consumer.repo} ${branchName}: ${u.depName} automerge is overridden by its group`,
      );
      assert.equal(
        Boolean(u.dependencyDashboardApproval),
        branch.dependencyDashboardApproval,
        `${consumer.repo} ${branchName}: ${u.depName} approval is overridden by its group`,
      );
    }
  }
  results.branch_replay.consumers.push({ repo: consumer.repo, sha: consumer.sha, branches: out });
}

console.log(JSON.stringify(results, null, 2));
