<!-- rumdl-disable-file MD041 -->
<!--
Required for PRs that change Renovate configuration: default.json, renovate.json, or presets/*.json.
For other PRs, replace this template with a concise summary and verification.

Write this for the operator at review time. Judge every answer against the purpose of this repository:
central management that keeps operator attention low while getting security updates in fast.
"Latest everything, auto-merged" is not the goal. Use concrete repos and numbers, not abstractions.
-->

## What this actually does

<!-- One or two plain sentences: which updates now behave differently, and how. Name the matchers. -->

## Blast radius

<!--
Survey real consumers on their default branches, not hypotheticals. Say how you found them.
- Consumers whose behavior changes now: list them.
- Consumers the rule matches nothing in today: count them, and say why.
-->

## Changes required in other repos

<!--
What has to change in consumer repos for this rule to do its job, if anything.
If the answer is "nothing, but the rule is mostly inert unless X," say so plainly.
-->

## Attention cost

<!--
Estimate the manual work accepted: approvals, manual merges, and dashboard checks, per repo and
across the portfolio, and how often. Compare that to the current behavior.
Also show the cost if consumers adopt the changes listed above.
-->

## Security gained

<!-- What risk this reduces, for which repos, and what it still leaves uncovered. -->

## Alternatives considered

<!--
At least one lighter option, such as a single gate instead of two, or a narrower match.
Give its attention cost and security effect, and say why this PR's option was chosen.
-->

## Verification and rollback

<!-- What was validated, what remains unverified, and how to revert. Link evidence instead of pasting it. -->
