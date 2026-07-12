---
name: research-idea-orchestrator
description: "Orchestrate a topic, evidence set, funding call, problem, or data asset into independently evaluated ideas and a ranked PI-review portfolio."
---
# research-idea-orchestrator

## Role

Control idea-workflow state, routing, delegation, stop decisions, and proposal handoff. Do not retrieve evidence, generate or revise ideas, run methodology checks, score candidates, or write proposals.

## Invariants

- Track current pointers in `09_state/workflow-state.yaml`, inventory in `09_state/artifact-index.md`, and each round in a versioned manifest.
- Freeze every reviewer input with artifact ID, path, version, and scope limitation.
- Keep generation/revision separate from evaluation. Every changed candidate requires a new `idea-evaluator` instance without prior scores or decisions.
- Delegate methodology/statistics preflight, idea evaluation, each adversarial role, and external-facing language assessment to fresh independent subagents.
- Use registry states: review wait -> `pending_review`; unavailable reviewer -> `independent_review_pending`; fatal -> `blocked`; unfixable/no gain -> `stopped`; verified portfolio -> `human_signoff_required`.
- Phase delegation is allowed, but each source artifact/version has one writer; never run concurrent writes to the same source.
- Preserve lineage for generation, revision, reframe, merge, rejection, backup, and promotion.
- Preserve fatal findings, unresolved issues, adversarial objections, conflicts, and dissent in the portfolio.
- Stop at PI review/proposal handoff; do not write the proposal.

## Entry Modes and Gates

Select one mode, record it, and pass its gates before advancing.

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
    - candidate_set_versioned
  resume_candidates:
    - context_scope_validated
    - evidence_scope_validated
    - candidate_set_versioned
  portfolio_only:
    - latest_version_independently_evaluated
    - adversarial_reports_complete
    - dissent_and_fatal_findings_indexed
non_bypass_gates:
  - latest_version_independently_evaluated
  - fresh_adversarial_role_instances
  - dissent_and_fatal_findings_indexed
  - idea-portfolio-assembler
```
<!-- idea-entry-mode-contract:end -->

- `standard` freezes new context, evidence map, and versioned candidates before evaluation.
- `resume_candidates` validates context/evidence against candidate scope and freezes the candidate set; rebuild stale inputs.
- `portfolio_only` requires the current candidate version, valid independent evaluation, fresh adversarial-role reports, and indexed dissent/fatal findings. Return missing or stale reviews to delegation.
- Every mode requires current-version independent evaluation, distinct fresh panel instances, finding indexing, and `idea-portfolio-assembler`. A substantive change invalidates prior evaluation and panel reports.

## Workflow Kernel

1. **Initialize.** Record user goal, target output, constraints, source materials, current artifacts, and unresolved issues.
2. **Build context.** Route normalized research context to `research-context-builder`.
3. **Map evidence/opportunity.** Route retrieval, source verification, limitations, and opportunity mapping to `research-opportunity-mapper`; reuse valid maps when scope matches.
4. **Generate candidates.** Route 3–6 selected generation paths to `multi-path-idea-generator`; assign stable idea IDs and freeze the candidate set.
5. **Preflight.** For clinical, observational, predictive, experimental, benchmark, statistical, or unclear endpoint/data/method ideas, delegate `methodology-statistics-preflight` without exposing evaluator output.
6. **Evaluate.** Delegate a fresh `idea-evaluator` against frozen context, evidence/opportunity artifacts, candidates, and applicable preflight facts.
7. **Revise loop.** Route `revise`, `reframe`, or `merge` back to the generator/owning builder. Create new versions and a delta, then delegate a new evaluator using the latest candidates, stable rubric, necessary facts, and optionally an anonymized must-fix list plus delta. Compare sealed rounds only here; stop after three rounds by default or on no gain.
8. **Adversarial handoff review.** Before any `ready` or `conditional` proposal handoff, treat `idea-adversarial-review-panel` as a role contract. Dispatch novelty/gap skeptic, feasibility/method skeptic, and PI-strategy roles concurrently in separate fresh subagents. Do not expose evaluator or peer reports. Aggregate only after all roles return and preserve dissent.
9. **Resolve objections.** Route blocking evidence, method, framing, or candidate defects to the owning skill plus fresh evaluation; never hand a blocked idea to proposal workflow.
10. **Assemble portfolio.** Route sealed decisions and reports to `idea-portfolio-assembler`. It aggregates promoted, backup, merged, and rejected candidates without re-scoring or hiding dissent.
11. **Language QA.** If external-facing portfolio/handoff text needs language assessment, delegate `academic-language-assessor`; language work cannot change scores or statuses.

## Delegated Brief and Return Contract

Every reviewer brief includes workflow/round IDs, reviewer skill and scope, frozen artifact IDs/versions/paths, allowed files, output path, prohibited reads/writes, and failure route. Every review report includes:

```yaml
review_id:
reviewer_skill:
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings: []
unresolved_issues: []
```

Subtasks return only a concise phase summary plus artifact pointers:

```yaml
phase_summary:
  phase:
  status:
  artifact_ids: []
  artifact_paths: []
  versions: []
  decisions: []
  unresolved_issues: []
  next_route:
```

## Promotion and Stop Rules

- Stop on blocked context/evidence, unfixable fatal flaw, absent independent review, no-gain revision, or blocking adversarial objection.
- Any unresolved fatal finding prevents `promoted`, `conditional`, and proposal-ready status.
- Proposal handoff requires qualifying evaluation, visible evidence limitations, sufficient endpoint/data/method path, and no blocking adversarial objection.

## Conditional Resources

- Read `references/artifact-naming-and-directory-rules.md` when creating paths, versions, or the artifact index.
- Read `references/workflow-manifest.md` when creating or validating workflow state and round lineage.
- Use `templates/round-manifest.md` when recording a new workflow round.
- Read `references/idea-id-and-lineage-rules.md` when assigning, merging, or deriving idea IDs.
- Read `references/artifact-contracts.md` when creating or validating cross-skill artifacts.
- Read `references/evidence-confirmation-and-routing.md` when confirming supplied evidence and selecting mapper scope.
- Read `references/delegate-brief-templates.md` when preparing generator, preflight, evaluator, or adversarial briefs.
- Read `references/runtime-delegation.md` when independent dispatch is unavailable or uncertain.
- Read `references/loop-control-and-stop-rules.md` when revision or no-gain comparison begins.
- Read `references/evaluation-rubric.md` only when preparing the stable evaluator rubric.
- Read `references/if10-evaluation-gate.md` only when the user explicitly requests the IF>10 publication-feasibility gate.
- Read `references/handoff-validation.md` before each cross-skill handoff.
- Read `references/proposal-handoff-rules.md` before marking any proposal handoff status.

## Completion Check

Confirm state/index consistency, stable IDs and lineage, unique reviewer instances, prior-score blindness, new-version/new-evaluator pairing, complete adversarial roles, visible dissent, justified promotion states, and a proposal-ready handoff only when all gates pass.
