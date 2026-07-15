---
name: perspective-final-compositor
description: "Independently verify and assemble a text-identical Perspective package for human review from current qualifying review artifacts."
---
# perspective-final-compositor

## Role

Assemble and verify the exact frozen Perspective version that passed required evaluation and panel gates. Do not change source prose, claims, title, abstract, headings, citations, grammar, formatting, or terminology.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread, never in the context that generated, drafted, revised, or evaluated the Perspective.
- Require frozen artifact IDs, exact paths, versions, and the latest qualifying evaluator/panel identities. Treat every source as read-only.
- Write only package copies, manifest/index, audit reports, risk/dissent records, and human sign-off artifacts under `08_final/**`.
- Do not edit, draft, rewrite, polish, repair, fix, or substantively/non-substantively modify source or copied prose. `final-perspective.md` must be text-identical to the latest evaluated source version.
- Read only the frozen panel summary needed to preserve findings; do not read individual evaluator/panel reports or parent hidden reasoning.
- Report exact files read, scope, limitations, and reviewer instance ID.
- If independent execution is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop; never verify inline or emit a ready state.

## Required Inputs

Frozen latest Perspective, claim ledger/matrix, citation-risk and contrary-evidence logs, evidence limitations, outlet profile, reference list, panel summary, artifact index, and latest evaluation report identity/version. When present, also receive the frozen versioned Cover Letter, its mechanical check, and the existing `medical-journal-review` report.

## Procedure

1. Verify source version, artifact ID, and checksum/text identity against the latest qualifying evaluator report and current state pointer.
2. Copy the source unchanged to `08_final/final-perspective.md`; record `source_edits_performed: false`.
3. If a Cover Letter is present, verify its current source digest and copy it text-identically to `08_final/cover-letter.md`. Preserve any probability block in the medical review unchanged; do not calculate, reinterpret, or adjust it.
4. Audit journal/outlet fit, citation support/identity, title/abstract requirements without editing them, anti-patterns, and claim-ledger consistency.
5. Preserve every panel dissent, fatal/blocking finding, unresolved issue, and accepted risk with stable source references.
6. If any text or formatting change is needed, return a change request to the owning writer; the changed artifact must receive a new version and required fresh review before composition restarts.
7. Map unresolved fatal/blocking findings to `blocked`; unavailable review to `independent_review_pending`; unfixable/no-gain route to `stopped`; a verified unchanged package to `human_signoff_required`.
8. Never infer author approval, signature, or external submission.

## Review Report Contract

```yaml
review_id:
reviewer_skill: perspective-final-compositor
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
review_scope: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings: []
unresolved_issues: []
workflow_state: blocked | stopped | independent_review_pending | human_signoff_required
source_version:
evaluated_version:
text_identity_verified: false
```

## Outputs

- `08_final/final-perspective.md`: unchanged copy of the latest evaluated source.
- `08_final/cover-letter.md`: optional unchanged copy of the current frozen Cover Letter.
- `08_final/final-edit-log.md`: states no source edits; lists proposed return-route changes only.
- `08_final/final-compositor-report.md`: five audit results, findings, dissent, fatal items, and version/checksum verification.
- `08_final/submission-readiness-report.md`: workflow state, remaining risks, required author checks, and outlet-targeting limitation.

## Status Gates

- `human_signoff_required` requires current/evaluated version equality, text identity, completed required reviews, no unresolved fatal/blocking finding, and preserved dissent.
- Generic outlet profile can reach only an outlet-targeting handoff, not human sign-off.
- Any changed manuscript copy is invalid and routes back for a new version plus fresh evaluation. Any changed Cover Letter copy routes back for a new version and refreshed medical review when that review applies.

## Conditional Resources

- Read `references/journal-fit-checklist.md` when auditing outlet requirements.
- Read `references/citation-audit-checklist.md` when auditing citation identity and support.
- Read `references/final-anti-pattern-scan.md` when checking the frozen final text.
- Read `references/permitted-edits.md` when distinguishing packaging operations from prohibited source edits.

## Completion Check

Confirm source/evaluated version equality, unchanged final text, optional Cover Letter identity, unchanged carried probability, complete provenance, visible dissent/fatal findings, justified canonical state, no source edits, and human-signoff-only handoff.
