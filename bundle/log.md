# Repository knowledge change log

## 2026-10-06

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
