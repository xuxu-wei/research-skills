---
name: perspective-final-compositor
description: "Independently verify and assemble a text-identical Perspective package for human review from current qualifying review artifacts."
---
# perspective-final-compositor

## Role

Assemble and verify the exact frozen Perspective version that passed required evaluation and panel gates. Do not change source prose, claims, title, abstract, headings, citations, grammar, formatting, or terminology.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread, never in the context that generated, drafted, revised, or evaluated the Perspective.
- Require frozen artifact IDs, exact paths, versions, complete logical index entries, and the latest qualifying final-evaluator/panel identities. Treat every source as read-only.
- Write only package copies, a package manifest, proposed canonical-index entries, audit reports, risk/dissent records, and human sign-off artifacts under `08_final/**`. Never write `09_state/**`; the orchestrator registers returned package outputs in the canonical artifact index.
- Do not edit, draft, rewrite, polish, repair, fix, or substantively/non-substantively modify source or copied prose. `final-perspective.md` must be text-identical to the latest evaluated source version.
- Read only the frozen panel summary needed to preserve findings; do not read individual evaluator/panel reports or parent hidden reasoning.
- Report exact files read, scope, limitations, and reviewer instance ID.
- If independent execution is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop; never verify inline or emit a ready state.
- Never require, calculate, or persist SHA/content digests for new LLM-facing artifacts. Accept legacy digest metadata as optional read-only input and ignore it as a gate.

## Required Inputs

Frozen latest Perspective, claim ledger/matrix, citation-risk and contrary-evidence logs, evidence limitations, outlet profile, reference list, panel summary, complete read-only artifact index, and a score-free qualifying-final-evaluation receipt binding the evaluator/report and evaluated Perspective identities/versions. When applicable, also receive the clean candidate-journal brief, frozen versioned Cover Letter and mechanical check, and isolated `medical-journal-review` report. Do not receive raw editorial repair history; receive only indexed references to unresolved risks that must be preserved. Never expose compositor inputs to the final evaluator.

## Procedure

1. Verify source version, artifact ID, logical current pointer, and direct text identity against the latest qualifying final-evaluator identity. Do not use a digest.
2. Copy the source unchanged to `08_final/final-perspective.md`; record `source_edits_performed: false`.
3. If a Cover Letter is present, verify its logical source identity/current pointer and copy it text-identically to `08_final/cover-letter.md`. Preserve any probability block in the medical review unchanged; do not calculate, reinterpret, or adjust it.
4. Audit journal/outlet fit, citation support/identity, title/abstract requirements without editing them, anti-patterns, and claim-ledger consistency.
5. Preserve every panel dissent, fatal/blocking finding, unresolved issue, and accepted risk with stable source references.
6. If any text or formatting change is needed, return a change request to the owning writer; the changed artifact must receive a new version and required fresh review before composition restarts.
7. Map unresolved fatal/blocking findings to `blocked`; unavailable review to `independent_review_pending`; unfixable/no-gain route to `stopped`; a verified unchanged package with complete proposed index entries to `packaging_pending`. The orchestrator alone promotes it after canonical registration.
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
workflow_state: blocked | stopped | independent_review_pending | packaging_pending
source_version:
evaluated_version:
logical_identity_verified: false
source_artifact_index_complete: false
proposed_package_index_entries_complete: false
text_identity_verified: false
```

## Outputs

- `08_final/final-perspective.md`: unchanged copy of the latest evaluated source.
- `08_final/cover-letter.md`: optional unchanged copy of the current frozen Cover Letter.
- `08_final/package-manifest.md`: package members, source identities/versions, and proposed canonical-index entries for the orchestrator to register.
- `08_final/final-edit-log.md`: states no source edits; lists proposed return-route changes only.
- `08_final/final-compositor-report.md`: five audit results, findings, dissent, fatal items, logical identity/index completeness, and direct text-identity verification.
- `08_final/submission-readiness-report.md`: workflow state, remaining risks, required author checks, and outlet-targeting limitation.

## Status Gates

- `packaging_pending` requires current/evaluated version equality, direct text identity, complete source identities/index entries, complete proposed package-index entries, completed editorial/final/specialist gates, no unresolved fatal/blocking finding, and preserved dissent.
- Only the orchestrator may set `human_signoff_required`, after it writes and verifies the package entries in the canonical artifact index and confirms a concrete qualifying outlet. A generic profile routes to `outlet_targeting_only` instead.
- Generic outlet profile can reach only an outlet-targeting handoff, not human sign-off.
- Any changed manuscript copy is invalid and routes back for a new version plus fresh evaluation. Any changed Cover Letter copy routes back for a new version and refreshed medical review when that review applies.

## Conditional Resources

- Read `references/journal-fit-checklist.md` when auditing outlet requirements.
- Read `references/citation-audit-checklist.md` when auditing citation identity and support.
- Read `references/final-anti-pattern-scan.md` when checking the frozen final text.
- Read `references/permitted-edits.md` when distinguishing packaging operations from prohibited source edits.

## Completion Check

Confirm source/evaluated version equality, unchanged final text, logical identity/index completeness, optional Cover Letter identity, unchanged carried probability, complete provenance, visible dissent/fatal findings, justified `packaging_pending` handoff, no source edits or new digests, and no canonical state write.
