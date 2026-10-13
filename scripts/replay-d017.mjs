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
    'Replay D017 mise/terraform preset rules: personal-computing#47 bundle, terraform required_provider patch, Zammad-MCP local caps/groups.',
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
    'Merged local preset bytes only; built-in preset expansion differs from hosted preset fetch. No branchify or dashboard replay.',
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

console.log(JSON.stringify(results, null, 2));
