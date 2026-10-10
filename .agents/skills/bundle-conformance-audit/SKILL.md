---
name: bundle-conformance-audit
description: >-
  Audit bundle/ against the OKF formatting rules and this repository's local extensions, fix what is
  non-compliant, and have Codex review the result. Use when asked to audit, validate, or check bundle
  conformance or OKF formatting.
---

# Bundle conformance audit

Find and fix documents in `bundle/` that break the formatting rules, including the rules no code enforces,
then have Codex review the result once. The audit is done when every finding is either fixed and committed
or reported to the operator as a named gap.

## Rule sources

Read these before judging anything; do not audit from memory of them.

- `bundle/formatting.md` owns the local conventions.
- `sources/evaluate/okf-spec.md` is the captured OKF v0.2 specification they extend.
- The operator's verdicts on pull request 123 extend the specification:
  `gh api repos/basher83/renovate-config/issues/comments/6025792492 --jq .body`. The operator's review comments
  on the same pull request cover resource binding, `sources`, and bundle-absolute links.
- Operator comments on later merged pull requests may add rules. Check that each rule you find there actually
  landed in `bundle/formatting.md`; a rule that did not land is a gap to report, not a rule to invent.

## What to check

Run `mise run bundle:check`, `mise run bundle:lint`, and `mise run bundle:test` first. They cover tags,
description punctuation, bundle-absolute paths, log structure, index drift, and the equality of source IDs
and footnote labels. A pass there is the starting point, not the result.

Then check what they do not enforce:

- **Mechanical rules.** Run `scripts/audit_unenforced.py` from the repository root. It reports frontmatter
  field order, source-entry order, block-style `generated`, and `generated.at` more than an hour older
  than the last commit that changed the body.
- **Whether each source supports its claim.** The checker only joins labels. For every decision and every
  evidence paragraph, confirm that the footnote on a claim leads to material for that claim, and that
  material the text derives from appears in `sources` instead of only as a body link. Newer decisions that
  amend older ones are where this goes wrong: the amended text keeps the older decision's footnote.
- **Resource binding.** A concept bound to an asset carries top-level `resource`; derivation material
  belongs in `sources`. This is the operator's judgement, so report a doubtful case; do not move it.
- **Lifecycle claims.** A non-draft `status` or a `verified` entry needs a recorded decision or event behind
  it. Standing lines that no longer match merged history are worth reporting, not rewriting.

## Fixing

- Correct a stale `generated` only with evidence. Take the time from the last body-changing commit and the
  producer from that commit's `Entire-Checkpoint` trailer (`entire checkpoint explain <id> --json` lists
  agent and model). When the checkpoint lists more than one session, leave the stamp and report it.
- Editing a body is itself a content change: set `generated` to your own harness and model and the current
  time in the house form, for example `claude_agent/Opus 5.5` or `codex_agent/GPT 6.1 Sol`.
- Never write an evidence record for an approval or selection you did not witness. Cite what is
  addressable, say in the footnote what has no capture, and report the gap.
- A source that lives in this repository outside `bundle/` and `sources/` (for example `research/`) passes
  the real check but fails `bundle:test`, whose fixtures copy only those two trees. Cite it by a
  commit-pinned GitHub URL, and do not edit the tests to make a local path pass.
- Footnote definitions must appear in order of first reference, and authored lines stay within 120
  characters; `bundle:lint` rejects both.
- Add one `**Update**` entry to `bundle/log.md` for the audit, at the top of today's date group.
- `AGENTS.md` governs everything else: never touch a governed `index.md`, never change the checker or
  generator to make content pass, and commit through the hooks.

Keep fixes inside `bundle/`. Findings elsewhere, such as authored records in `sources/evaluate/`, are
reported unless the operator widened the scope.

## Review

After committing, start one Codex review in its own thread in this worktree and wait for it:

```bash
bb thread spawn --json --project "$BB_PROJECT_ID" --environment "$BB_ENVIRONMENT_ID" --parent-self \
  --provider codex --model gpt-6.1-sol --title "Review: bundle conformance audit" --prompt-file <file>
bb thread wait <thread-id>
bb thread output <thread-id>
```

The prompt names the base commit, asks for a read-only review that lists each issue as serious or minor
with file and line, and asks for two things: whether each change is correct, and an independent sweep of
`bundle/` for what the audit missed, with attention to whether sources support their claims. List the gaps
you are deliberately leaving so they are not re-reported. If a finding is unclear, ask with
`bb thread tell` and read the answer; do not request a second review. Fix every serious issue, commit, and
leave the thread open.

If you are running as Codex, a Codex reviewer is not an independent read; ask the operator which agent
should review instead.

## Report

Lead with what was fixed and what the review found. Then list every gap left for the operator, each with
the file and the reason it was not fixed. Do not push or open a pull request without approval.
