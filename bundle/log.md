# Repository knowledge change log

## 2026-10-09

* **Update**: Recorded the hosted canary result in
  [D016](/decisions.md#2026-10-09--d016-replace-runner-manual-merge-with-automerge). Zammad-MCP #394 confirmed
  approval and automerge for a real runner update, and #396 merged on required checks while a non-required check was
  still running, most likely through GitHub-native auto-merge. The [runner policy](/github-hosted-runner-policy.md) now states the observed gating
  ([Zammad-MCP #392](https://github.com/basher83/Zammad-MCP/issues/392)).

* **Update**: The operator replaced runner manual merge with automerge after dashboard approval in
  [D016](/decisions.md#2026-10-09--d016-replace-runner-manual-merge-with-automerge). A default-branch survey found
  one pinned-runner consumer among 33; the [runner policy](/github-hosted-runner-policy.md) now records it.
  Strict validation passes; hosted automerge after approval remains unobserved.

* **Update**: Addressed both operator-endorsed CodeRabbit findings on PR #125. A new
  [D016 replay receipt](../sources/evaluate/2026-10-09-d016-automerge-receipt.json) supplies representative-consumer
  evidence with automerge enabled. It also traces the missing branch `groupName` to Renovate's single-update
  ungrouping rather than to receipt generation. D016 records both; earlier receipts are unchanged.

* **Update**: Addressed both CodeRabbit findings on PR #125: title-case `GitHub-Hosted Runners`
  while retaining its branch slug, and distinguish the runner implementation from paused action-input policy
  in README. Maintained guidance now states the selected policy directly. The
  [review receipt](../sources/evaluate/2026-10-09-runner-review-receipt.json) records a successful replay
  against the corrected preset; the original evidence remains unchanged. Publication and operator merge
  acceptance remain separate.

* **Creation**: Added a pull request template at the operator's request. Renovate configuration PR bodies must state concrete
  consumer blast radius, required consumer changes, and operator attention cost, judged against central
  management with low attention and fast security updates. AGENTS.md requires agents to use it.
  Prompted by PR 125: its body omitted that only one of about twenty-five workflow-bearing consumers pins a runner.

## 2026-10-08

* **Update**: Finalized the runner implementation candidate through mise. All 33 bundle regressions,
  20 authored-document and seven generated-index lint checks, strict validation of two root and ten preset
  configs, and all 16 hooks passed. The behavior receipt retains 204 actual-input update-type controls,
  40 fixture comparisons, real runner lookup/grouping, and an explicit approval-disposition control.
  Imported reports initially failed local prose lint and Git would normalize CSV line endings; the
  [source capture](../sources/evaluate/2026-10-08-policy-source-capture.json) instead preserves all four inputs
  byte-for-byte as UTF-8 JSON strings. Exact-input hashes and JSON round trips pass; original operator files
  remain untouched. Existing hooks and enforcement machinery are unchanged. Publication and acceptance remain pending.

## 2026-10-07

* **Update**: The operator selected runner option C and authorized implementation preparation in
  [D015](/decisions.md#2026-10-07--d015-select-runner-approval-policy-c). Added the final runner-specific
  preset rule and [runner policy](/github-hosted-runner-policy.md): separate grouping, dashboard approval,
  and no automerge. The [behavior evaluation](../sources/evaluate/2026-10-08-runner-behavior-evaluation.md)
  distinguishes fresh consumers, a preserved-input real lookup, and explicit controls. Personal-computing
  already upgraded through bot-merged PR #39; replay still demonstrates C. Publication and merge acceptance
  remain pending; action-input policy and consumer edits are separate.
* **Update**: Recorded the operator's repository-bound reference ruling in
  [D014](/decisions.md#2026-10-07--d014-bound-local-references-to-this-repository).
  Standalone bundle distribution is not required. Local references may leave `bundle/` but stay inside this
  repository; other checkouts use Git-hosted URLs. The existing checker already enforces local containment.
* **Update**: Finalized and checked the isolated D014 candidate through mise. All 33 bundle regression tests,
  authored and generated Markdown lint, strict validation of two root and ten preset configs, all 16
  configured hooks, and receipt JSON parsing passed. Ten pinned captures remain unchanged. The initial hook
  cache could not run Renovate; a fresh task-local cache passed. Review and operator merge acceptance remain
  pending; passing checks do not accept this revision.
* **Update**: Clarified pending intake for authored decision proposals under
  [D013](/decisions.md#2026-10-07--d013-place-decision-proposals-in-pending-evaluation).
  Moved the runner policy candidate from exploratory research to `sources/evaluate/`, keeping its proposal
  type, draft standing, and supporting evidence distinct. Updated references and entry-point guidance;
  navigation is finalized through mise. This placement agreement does not select the runner policy.
* **Update**: Reconciled the supplied adversarial review in the
  [review record](../sources/evaluate/2026-10-07-runner-candidate-review-reconciliation.md).
  The runner candidate now leads with the policy and evidence-path choices, distinguishes alias migration
  timing from pinned-runner eligibility, identifies retirement responsibility and single-input coverage,
  and preserves the wider preset-splitting questions. The receipt now captures current drafting authority;
  #122 implementation remains paused. No dependency policy, evidence exception, or consumer edit was selected.
* **Creation**: Evaluated four preserved portfolio sources and drafted one
  [runner approval policy candidate](../sources/evaluate/2026-10-07-runner-update-policy-candidate.md).
  The [evaluation](../sources/evaluate/2026-10-07-policy-evidence-evaluation.md) records proposed source roles,
  conflicting consumer classifications, unavailable original run artifacts, and historical scope.
  The [receipt](../sources/evaluate/2026-10-07-policy-evidence-receipt.json) retains input hashes, structural
  checks, issue #122, and three consumer files fetched at immutable revisions. This is authorized evaluation
  and provisional synthesis, not policy selection, human verification, implementation, or publication.

## 2026-10-06

* **Update**: Addressed both findings in the [follow-up review](https://github.com/basher83/renovate-config/pull/123#issuecomment-6029851923).
  Generator and checker defaults retain the lexical bundle root until symlink validation, so supported mise
  invocations reject a linked root. Markdown parsing now recognizes labeled footnotes and validates their
  embedded links without interpreting their definitions as ordinary reference-link destinations.
* **Update**: This separate follow-up run passed thirty-three regressions. New tests reproduced both failures
  before the fixes, then exercised actual mise generation, checking, finalization, and lint in owned checkout
  fixtures. Linked roots leave both checkout copies unchanged; valid plain, titled, and reference links in
  footnotes pass, while broken paths, relative bundle paths, and broken anchors still fail.
  All ten capture pins, strict root/preset validation, authored Markdown lint, Python parsing, and full hooks
  passed. Prior verification, acceptance, and validation receipts remain historical records.
* **Update**: Addressed the five findings in the [PR review](https://github.com/basher83/renovate-config/pull/123#issuecomment-6028352636).
  Generation rejects symlinks throughout both governed trees and reads all destinations before writing;
  concept and log links use CommonMark parsing, including titles and reference forms. History validates
  unordered and numbered entry markers for flatness, date grouping, and accepted labels. Usage windows
  require both endpoints, source counts are nonnegative integers, and expiration timestamps require offsets
  while allowing future expiration. Root concept generation dates now identify their last persisted content
  revision; formatting uses this correction's authoring time. Historical verification and acceptance remain intact.
* **Update**: A separate remediation run passed thirty regressions, including YAML round-trip preservation,
  code-example link handling, and symlink failures that preserve every earlier index and external sentinel.
  Original-revision controls reproduced the reported bypasses in owned temporary fixtures. Strict root and
  preset validation and authored Markdown lint passed; all ten capture pins remained valid.
  All sixteen configured hooks passed through mise using a fresh task-local cache, with no skips.
* **Update**: Corrected history validation to process date headings and entries in document order and
  reject entries before the first dated group. The new regression reproduced the gap before the fix;
  this follow-up run passed all nineteen regressions, including that ordering case.
* **Update**: Applied operator PR verdicts on descriptions, locked tags, resource binding, provenance,
  bundle-absolute links, accepted history labels, and complete generated index coverage.
  [Decision D012](/decisions.md#2026-10-06--d012-apply-reviewed-local-okf-extensions) records authority and scope.
  All eighteen regressions and full hooks passed; fifteen authored documents and seven generated indexes
  passed lint. The [verdict receipt](../sources/evaluate/2026-10-06-pr-verdict-receipt.json) records this separate run.
* **Update**: Extended the checker to validate authored pending-evaluation Markdown with the same
  metadata, source-pointer, and footnote checks as concepts, excluding pinned captures by `SNAPSHOTS` paths.
  Added regressions for broken source pointers and unmatched footnotes that leave index metadata unchanged;
  a separate follow-up run for commit `d3d5d61` passed all eleven regressions, including the two added tests,
  along with bundle checks and authored Markdown lint. The earlier receipt below records its nine-test run.
* **Update**: Reconciled capture-preserving hook exclusions, added complete authored-document
  lint through mise, and isolated the source-escape regression fixture inside its owned temporary directory.
  [D011](/decisions.md#2026-10-06--d011-reconcile-the-complete-pre-commit-boundary) records authority and scope.
* **Update**: Full hooks passed without bypasses in an isolated staged repository; all ten pinned captures
  matched the starting revision. A concept-title change regenerated navigation and stopped the hook attempt;
  including the output made retry pass, and repeat finalization was idempotent. Nine regressions, authored
  Markdown lint, and strict root/preset validation passed. The
  [validation receipt](../sources/evaluate/2026-10-06-remediation-receipt.json) records scope and limitations.
  No commit, push, PR edit, or acceptance occurred.
* **Update**: Drafted the exemplar purpose and [enforcement ownership model](/enforcement.md), following
  operator concurrence with the gap review.
  [D010](/decisions.md#2026-10-06--d010-capture-exemplar-intent-and-separate-the-trail)
  records scope and the selected operator-merge acceptance event. This is a documentation candidate, not a PR
  acceptance event.
* **Update**: Configured mise index finalization at pre-commit; a temporary-repository exercise showed
  regeneration stopping the first attempt and passing after generated output was included. See
  [D009](/decisions.md#2026-10-06--d009-finalize-indexes-through-mise-before-commit). No commit or publication occurred.
* **Update**: Assigned governed indexes to their generator and moved root reference records into pending
  `sources/evaluate/`. [D007](/decisions.md#2026-10-06--d007-separate-knowledge-from-sources-pending-evaluation) and
  [D008](/decisions.md#2026-10-06--d008-govern-indexes-through-their-generator) retain rationale and scope.
