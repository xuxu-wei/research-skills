---
name: research-idea-orchestrator
description: "Orchestrate a topic, evidence, call, problem, or data asset into independently evaluated ideas and a PI-review portfolio."
---
# research-idea-orchestrator

## Role

Control state, routing, delegation, stops, and human handoff. Do not retrieve,
author/revise Ideas, review methods, score, or draft proposals.

## Invariants

- In `research-idea.v3`, a complete `idea-dossier-vNNN.md` is the sole Idea;
  deltas, maps, indexes, and portfolios never substitute for it.
- Keep one writer per version; every substantive or positioning change creates
  a new dossier version.
- Delegate preflight, `idea-evaluator`, each adversarial role, and language
  assessment to fresh independent subagents.
- Give `idea-evaluator` exactly the current dossier as its only project artifact.
  It must not read maps, ledger, preflight, history, deltas, must-fix lists, or
  prior reports.
- Preserve lineage, limits, fatal/blocking findings, conflicts, and dissent;
  forbid concurrent writes and inline reviewer fallback.
- Stop at human review or Proposal handoff; do not draft a proposal.

## Entry Modes and Gates

<!-- idea-entry-mode-contract:start -->
```yaml
entry_modes:
  - standard
  - resume_candidates
  - portfolio_only
entry_gates:
  standard:
    - context_frozen
    - evidence_map_frozen
    - routing_decision_frozen
    - idea_dossier_versioned
  resume_candidates:
    - context_scope_validated
    - evidence_scope_validated
    - routing_decision_frozen
    - idea_dossier_versioned
  portfolio_only:
    - latest_version_independently_evaluated
    - dissent_and_fatal_findings_indexed
entry_gates_by_route:
  focused_optimization:
    - adversarial_reports_complete_when_proposal_handoff_candidate
  bounded_exploration:
    - evidence_and_opportunity_remap_complete
    - fresh_evaluation_complete_for_each_current_dossier
non_bypass_gates:
  - latest_version_independently_evaluated
  - dissent_and_fatal_findings_indexed
  - idea-portfolio-assembler
non_bypass_gates_by_route:
  focused_optimization:
    - adversarial_reports_complete_when_proposal_handoff_candidate
  bounded_exploration:
    - evidence_and_opportunity_remap_complete
    - fresh_evaluation_complete_for_each_current_dossier
```
<!-- idea-entry-mode-contract:end -->

`standard` freezes inputs; resume validates scope/digests; portfolio-only needs
current dossier reviews. Substantive change invalidates review.

## Workflow Kernel

1. **Initialize.** Record goal, constraints, sources, issues, schema, and pointers.
   Treat v1/v2 projects as read-only and return
   `layout_migration_required`.
2. **Build context.** Route normalization and direction clarity to
   `research-context-builder`.
3. **Map.** Route retrieval, value/confidence, and direction signals to
   `research-opportunity-mapper`.
4. **Choose route.** Apply `references/adaptive-direction-routing.md` without
   scoring. Record an `idea_routing_decision`.
5. **Write dossiers.** Use one focused node or two/three supported exploration
   nodes; require complete dossiers, chains, claim tables, metadata, and digests.
6. **Preflight if needed.** Delegate method-sensitive Ideas. Focused repairs use
   a new dossier; bounded repairs join its sole optimization. Never expose
   preflight to the evaluator.
7. **Focused evaluation.** Only on `focused_optimization`, delegate one fresh
   `idea-evaluator` for the current dossier, bound to exact ID/version/path/digest.
8. **Focused loop.** Route findings to the writer; write a complete new dossier
   plus delta, then use a fresh dossier-only evaluator. Compare sealed reports
   after return. Keep three-round/no-gain stops; drift returns `new_idea_required`.
9. **Bounded exploration loop.** Do not evaluate the initial drafts. Apply
   exactly one bounded optimization per direction, remap each evolved direction,
   write a complete synchronized dossier, then run one terminal fresh evaluator
   per dossier. Stop at
   `human_direction_selection_required`; do not auto-select or enter Proposal.
10. **Adversarial handoff.** For a focused Proposal candidate, dispatch
    novelty/gap, feasibility/method, and PI-strategy roles concurrently in fresh
    instances. Aggregate after all return and retain dissent.
11. **Assemble.** Link qualifying dossiers, reports, and sealed decisions without
    copying, rescoring, or choosing a winner.
12. **Finish.** Language-check navigation only; update the project README on
    finish/pause/stop and return the human state.

Delegated returns contain a concise phase summary, artifact pointers, decisions,
unresolved issues, and `next_route`, not raw traces.

## State and Stop Rules

- Review wait -> `pending_review`; unavailable reviewer ->
  `independent_review_pending`; fatal -> `blocked`; no defensible direction ->
  `no_defensible_direction`; no gain -> `stopped`.
- Focused verified handoff -> `human_signoff_required`; bounded exploration ->
  `human_direction_selection_required`.
- A digest mismatch, incomplete dossier/evidence chain, unsupported title claim,
  stale review, identity drift, or unresolved blocking finding prevents ready.
- A human-selected direction resumes as focused work; never enter Proposal directly.

## Conditional Resources

- Read `references/project-readme-contract.md` on finish/pause/stop.
- Read `references/idea-artifact-lifecycle.md` for persistence, review, packaging,
  resume, or location.
- Read `references/idea-dossier-contract.md` for dossier, chain, or positioning work.
- Read `references/adaptive-direction-routing.md` after mapping and during remap.
- Read `references/reference-ledger-contract.md` for internal IDs or navigation.
- Read `references/artifact-naming-and-directory-rules.md` for names and indexes.
- Read `references/workflow-manifest.md` and use `templates/round-manifest.md`
  when recording a round.
- Use `templates/idea-index.yaml` when freezing an Idea index version.
- Read `references/idea-id-and-lineage-rules.md` when assigning or deriving IDs.
- Read `references/artifact-contracts.md` for cross-skill artifact fields.
- Read `references/evidence-confirmation-and-routing.md` for supplied evidence.
- Read `references/delegate-brief-templates.md` before delegation.
- Read `references/runtime-delegation.md` only when dispatch is unavailable.
- Read `references/loop-control-and-stop-rules.md` for sealed-round comparison.
- Read `references/evaluation-rubric.md` only when freezing the rubric.
- Read `references/if10-evaluation-gate.md` only on an explicit IF>10 request.
- Read `references/handoff-validation.md` before handoff.
- Read `references/proposal-handoff-rules.md` before Proposal status.

## Completion Check

Confirm v3 dossier/index/ledger, route, identity, complete chains and claim
support, matching digest, route-specific fresh reviews, visible dissent, passed
gates, project README, and justified human state.
