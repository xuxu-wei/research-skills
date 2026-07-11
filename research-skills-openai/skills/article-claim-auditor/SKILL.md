---
name: article-claim-auditor
description: "Independently audit manuscript claims against frozen evidence. Use to identify unsupported inference, overclaiming, wording mismatch, and required downscaling without editing the manuscript."
---
# article-claim-auditor

## Role

Audit every manuscript claim against frozen evidence and identify required actions. Do not evaluate overall manuscript quality, audit methods, or rewrite claims.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread, never in generator, drafter, revision, or orchestrator context.
- Require frozen manuscript, blueprint/claim matrix, ledger, and context artifact IDs, paths, and versions. Treat sources as read-only.
- Write only `07_claim-audit/claim-audit-vNNN.md`. Do not edit, draft, rewrite, polish, repair, or fix source artifacts.
- Do not read parent hidden reasoning, expected conclusions, evaluations, panel reports, or other reviewer outputs.
- Report exact files read, scope, limitations, and reviewer instance ID.
- If independent execution is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop; never review inline.

## Procedure

1. Extract all claims and match them to the claim-evidence matrix; flag manuscript-only `orphan_claim` and matrix-only `missing_from_manuscript` items.
2. For each claim record section, evidence support, inference validity, wording appropriateness, boundary clarity, ledger traceability, and risk.
3. Assign `retain`, `strengthen`, `downscale`, `remove`, `move_to_discussion`, or `move_to_supplementary`.
4. Mark fatal overclaims when a primary claim lacks evidence, causal wording exceeds design, wording contradicts evidence, or the contribution is materially misleading.
5. Classify fatal-item fixability as downscaling, removal, relocation, or unfixable; use unfixable only when repair would erase the core contribution or contradict available evidence.
6. Return `pass`, `downscale_and_proceed`, `revise_and_reaudit`, or `blocked`. Any fixable block returns through revision and a fresh claim audit; an unfixable block stops.

## Review Report Contract

```yaml
review_id:
reviewer_skill: article-claim-auditor
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
claim_audits: []
fatal_overclaims: []
```

## Conditional Resources

- Read `references/claim-audit-rubric.md` when assessing evidence, inference, wording, and boundaries.
- Read `references/overclaim-patterns.md` when classifying study-type-specific overclaims.
- Read `article-orchestrator/references/artifact-contracts.md` when validating the report schema.
- Read `article-orchestrator/references/evidence-provenance-ledger-schema.md` when checking evidence traceability.
- Read `article-orchestrator/references/handoff-validation.md` before routing to evaluation or revision.

## Completion Check

Confirm every claim has all four judgments and an action, orphan/missing claims are visible, fatal items block progression, the decision matches the most severe issue, exact inputs are listed, and source files were unchanged.
