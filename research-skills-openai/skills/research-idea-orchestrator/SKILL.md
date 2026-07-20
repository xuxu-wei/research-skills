---
name: research-idea-orchestrator
description: "Orchestrate a topic, evidence, call, problem, or data asset into independently evaluated ideas and a PI-review portfolio."
---
# research-idea-orchestrator

## Role

Control state, routing, delegation, stops, and handoff; never perform delegated
work.

## Invariants

- In v3, one complete versioned dossier is the sole Idea; one writer owns each
  version, and every substantive or positioning change creates a new version.
- Use fresh independent subagents for preflight, editorial review,
  preservation, evaluation, specialist review, and adversarial review. Never
  permit concurrent writes or inline reviewer fallback.
- Preserve lineage, limits, blocking findings, conflicts, and dissent. Bind
  Idea artifacts by ID, version, and path; do not require hashes.
- Run narrative and complete-dossier language readiness after scientific
  revision. Give `idea-evaluator` only the final reassessed dossier—never maps,
  ledger, preflight, history, deltas, repair artifacts, or prior reports.
- After evaluation, send a biomedical/clinical Idea and its unscored, unranked candidate
  brief to fresh `medical-journal-review`; hide evaluator judgments and report.
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
    - latest_version_editorially_ready
    - latest_version_independently_evaluated
    - biomedical_journal_review_complete_or_not_applicable
    - dissent_and_fatal_findings_indexed
entry_gates_by_route:
  focused_optimization:
    - adversarial_reports_complete_when_proposal_handoff_candidate
  bounded_exploration:
    - evidence_and_opportunity_remap_complete
    - fresh_evaluation_complete_for_each_current_dossier
non_bypass_gates:
  - current_dossier_editorial_readiness_complete
  - latest_version_independently_evaluated
  - biomedical_journal_review_complete_or_not_applicable
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

`standard` freezes inputs; resume validates scope; portfolio-only requires
current reviews. A substantive change invalidates them.

## Workflow Kernel

1. **Initialize.** Record scope, constraints, sources, schema, and pointers;
   return `layout_migration_required` for read-only v1/v2 projects.
2. **Ground and route.** Dispatch `research-context-builder`, then
   `research-opportunity-mapper`; freeze an unscored routing decision.
3. **Write.** Produce one focused dossier or two/three evidence-supported
   directions with complete chains, claim table, metadata, and structural lint.
4. **Preflight and revise science.** When methods are material, put required
   repairs in a new complete dossier. Record an accepted bounded working
   assumption once in section 14; never give preflight to the evaluator.
5. **Establish editorial readiness.** Run fresh `research-narrative-assessor` and
   `academic-language-assessor` instances in parallel. Normalize their included
   actions into one validated writer brief, repair from it and the protected
   register, then require preservation and fresh reassessment.
6. **Evaluate.** Give a fresh `idea-evaluator` only the eligible current dossier.
7. **Apply the route loop.** Focused revisions repeat preflight/readiness/
   evaluation within stop limits. Bounded directions receive one optimization,
   remap, synchronization, readiness pass, and terminal evaluation.
8. **Review journal fit.** Persist the evaluator's frozen score-free candidate
   payload; send it and the dossier to fresh `medical-journal-review`. Do not rematch.
9. **Run adversarial handoff.** For a focused Proposal candidate, dispatch the
   fresh `idea-adversarial-review-panel` roles concurrently and retain dissent.
10. **Assemble.** Link dossiers, evaluations, journal matches/reviews, and open
    issues without rewriting or ranking; update README and return human state.

## State and Stop Rules

- Review wait -> `pending_review`; unavailable reviewer ->
  `independent_review_pending`; fatal -> `blocked`; no defensible direction ->
  `no_defensible_direction`; no gain -> `stopped`.
- An applicable biomedical/clinical Idea awaiting its fresh medical review uses
  the existing `specialist_review_pending` state. Missing, stale, scored, or
  evaluator-contaminated candidate briefs cannot satisfy packaging.
- Focused verified handoff -> `human_signoff_required`; bounded exploration ->
  `human_direction_selection_required`.
- Incomplete artifacts/chains, blocking editorial findings, unsupported title
  claims, stale reviews, identity drift, or unresolved blockers prevent ready.
- A selected direction resumes as focused work, not direct Proposal handoff.

## Conditional Resources

- On finish/pause/stop read `references/project-readme-contract.md`.
- For persistence read `references/idea-artifact-lifecycle.md`,
  read `references/idea-dossier-contract.md` and `references/artifact-contracts.md`,
  read `references/artifact-naming-and-directory-rules.md`,
  read `references/idea-id-and-lineage-rules.md` and `references/workflow-manifest.md`,
  and use `templates/idea-index.yaml` and `templates/round-manifest.md`.
- For downstream artifacts read `references/journal-review-and-portfolio-artifacts.md`.
- For evidence/routing read `references/evidence-confirmation-and-routing.md`,
  read `references/adaptive-direction-routing.md`, and
  read `references/reference-ledger-contract.md`.
- Before delegation/loops read `references/delegate-brief-templates.md`,
  read `references/runtime-delegation.md`, and
  read `references/loop-control-and-stop-rules.md`.
- Before editorial work read `references/editorial-readiness-and-preservation.md`.
- Before freezing a writer brief, run `scripts/validate_editorial_repair_writer_brief.py`
  with reviews and exact-source register.
- Run `scripts/test_validate_editorial_repair_writer_brief.py` after changing
  that contract or validator.
- When applicable read `references/evaluation-rubric.md`,
  read `references/if10-evaluation-gate.md` only for an explicit IF>10 request,
  and read `references/handoff-validation.md` and `references/proposal-handoff-rules.md`.

## Completion Check

Confirm v3 dossier/index/ledger, identity, chains, claims, logical references,
route-specific fresh reviews, editorial readiness, dissent, gates, README, and
human state.

Delegates return a phase summary and artifact pointers.
