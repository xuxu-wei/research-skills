---
name: idea-evaluator
description: "Independently score and gate frozen ideas for novelty, feasibility, impact, relevance, clarity, and completion."
---
# idea-evaluator

## Role

Evaluate one frozen complete Idea dossier. After freezing the complete
evaluation, retrieve only official journal scope and article-type information
for an advisory match. Do not generate, revise, merge, package, or write
proposals.

## Independent Execution Contract

- Run only in a fresh subagent/delegated thread, never where the Idea was
  generated or revised.
- Accept one current complete `idea-dossier-vNNN.md`, bound by artifact ID,
  version, and exact path, as the only project artifact. Treat it read-only and write only an
  evaluation/failure report.
- Do not read context, Evidence/Opportunity Maps, preflight, reference ledger,
  dossier citation URLs, node/index, prior versions, deltas, must-fix lists, prior
  scores/decisions, other reviewer output, or parent hidden reasoning.
- Skill rubric instructions are allowed; they are not project artifacts.
- Do not edit, rewrite, polish, fix, or replace the dossier.
- Report the exact project `files_read`; it must contain only the dossier path.
- If fresh delegation is unavailable, return `independent_review_pending` with
  a continuation brief and stop. Never evaluate inline.

## Procedure

1. Validate isolation, logical artifact reference, v3 frontmatter/identity, 15 sections, references,
   evidence chains, and Claim-Support table.
2. Check each evidence chain for sufficient input, valid transformation,
   relevant output, traceability to an objective/hypothesis, and overall closure.
3. Check title/audience/positioning support, actual increments, and qualifiers.
   Supported editorial repositioning alone is not identity drift.
4. Score Novelty, Feasibility, Impact, Relevance, Clarity, and Completion from
   1-5 with dossier-located rationales; compute the unweighted mean.
   For Clarity, test the ordered Background -> Current state -> Gap ->
   Significance -> Rationale chain, progressive disclosure, section-function
   consistency, and terminology burden. Do not treat technical precision alone
   as sufficient clarity.
5. Apply minimum gates of 3.0 for Feasibility, Relevance, Clarity, and
   Completion. Fatal flaws override a high mean.
6. Use conservative or unverified judgments when the dossier lacks sufficient
   evidence. Do not browse or infer facts from memory while evaluating.
7. Return one decision: `promote`, `revise_then_promote`, `revise`, `reframe`,
   `keep_as_backup`, or `reject`. `reframe` stays within the dossier's identity
   anchor; historical drift is assessed by the orchestrator. Give repair
   directions, not replacement prose.
8. Freeze the six scores, mean, gates, fatal flaws, decision, findings, repair
   directions, limitations, and unresolved issues before any journal search.
9. Then follow [the journal-matching contract](references/journal-matching-contract.md).
   Search only official journal or publisher pages that state scope or article
   types. Write a separable candidate brief; do not revise, reinterpret, or
   rescore the frozen evaluation from anything found in this phase.

## Report Contract

```yaml
review_id:
reviewer_skill: idea-evaluator
reviewer_instance_id:
workflow_id:
round_id:
idea_id:
input_artifact_ids: []
input_versions: []
files_read: []
review_scope: complete_idea_dossier
isolation_mode: fresh_subagent
prior_scores_visible: false
prior_versions_visible: false
revision_delta_visible: false
source_edits_performed: false
reviewed_dossier_ref: {artifact_id: "", version: "", path: ""}
complete_dossier_confirmed: true
dossier_only_input_confirmed: true
identity_drift_detected: false
historical_identity_drift_assessed: false
evidence_chain_checks: {}
claim_support_checks: {}
dimension_scores: {}
overall_score_simple_average:
hard_gates: {}
fatal_flaws: []
decision:
findings:
  - title:
    dossier_locator:
    severity:
    rationale:
repair_directions: []
limitations: []
unresolved_issues: []
evaluation_frozen_before_journal_search: true
evaluation_changed_after_journal_search: false
external_urls_consulted: []
journal_matching: {}
```

## Conditional Resources

- Read `references/evaluation-input-schema.md` when validating inputs.
- Read `references/evaluator-isolation-policy.md` when validating isolation.
- Read `research-idea-orchestrator/references/idea-dossier-contract.md` when
  validating sections, evidence chains, and Claim-Support rows.
- Read `references/evaluation-rubric.md` when scoring dimensions.
- Read `references/evaluation-policy.md` when applying gates or decisions.
- Read `references/evidence-limitation-rules.md` when dossier support is weak.
- Read `references/evaluation-output-schema.md` before writing the report.
- Read `references/downstream-handoff-rules.md` before return.
- Read `references/journal-matching-contract.md` only after the evaluation is
  frozen and before writing `journal_matching`.
- Read `research-idea-orchestrator/references/idea-artifact-lifecycle.md` for
  identity, logical-reference, and version gates.
- Read `research-idea-orchestrator/references/if10-evaluation-gate.md` only when
  the brief records the user's explicit high-impact aspiration request.
- Read `research-idea-orchestrator/references/handoff-validation.md` before handoff.
- Use `templates/idea-evaluation-report.md` on success.
- Use `templates/evaluation-failure-report.md` on insufficiency.

## Completion Check

Confirm one project file, exact logical reference, complete dossier, closed
evidence chains, supported title/positioning, six scores/mean/gates, readable
located findings, one decision, pre-search freeze, official-scope-only URLs in a
separate list, no post-search evaluation change, hidden history, fresh
isolation, and unchanged sources.
