---
name: research-idea-orchestrator
description: "Orchestrate a topic, evidence, call, problem, or data asset into independently evaluated ideas and a PI-review portfolio."
---
# research-idea-orchestrator

## Role

Control idea-workflow state, routing, delegation, stop decisions, and proposal handoff. Do not retrieve evidence, generate or revise ideas, run methodology checks, score candidates, or write proposals.

## Invariants

- Track current pointers, inventory, and versioned round manifests under `09_state/`; freeze every reviewer input with artifact ID, path, version, and scope.
- Keep generation/revision separate from evaluation. Every changed candidate requires a fresh `idea-evaluator` without prior scores or decisions.
- Delegate methodology/statistics preflight, idea evaluation, each adversarial role, and external-facing language assessment to fresh independent subagents.
- Use registry states: review wait -> `pending_review`; unavailable reviewer -> `independent_review_pending`; fatal -> `blocked`; unfixable/no gain -> `stopped`; verified portfolio -> `human_signoff_required`.
- Phase delegation is allowed, but each source artifact/version has one writer; never run concurrent source writes.
- Preserve lineage, fatal findings, unresolved issues, adversarial objections, conflicts, and dissent in the portfolio.
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

`standard` freezes new inputs; `resume_candidates` validates scope and rebuilds stale inputs; `portfolio_only` requires current candidates, qualifying evaluation, fresh adversarial reports, and indexed dissent/fatal findings. Every mode requires distinct fresh reviewers and `idea-portfolio-assembler`; substantive change invalidates prior reviews.

## Workflow Kernel

1. **Initialize.** Record user goal, target output, constraints, source materials, current artifacts, and unresolved issues.
2. **Build context.** Route normalized research context to `research-context-builder`.
3. **Map evidence/opportunity.** Route retrieval, source verification, limitations, and opportunity mapping to `research-opportunity-mapper`; reuse valid maps when scope matches.
4. **Generate candidates.** Route selected paths to `multi-path-idea-generator`; assign stable IDs and freeze the set.
5. **Preflight.** For clinical, observational, predictive, experimental, benchmark, statistical, or unclear endpoint/data/method ideas, delegate `methodology-statistics-preflight` without exposing evaluator output.
6. **Evaluate.** Delegate a fresh `idea-evaluator` against frozen context, evidence/opportunity artifacts, candidates, and applicable preflight facts.
7. **Revise loop.** Route `revise`, `reframe`, or `merge` to the owning builder. Version the result and delta, then use a fresh evaluator with latest candidates, stable rubric, necessary facts, and an optional anonymous must-fix list plus delta. Compare sealed rounds only here; stop after three rounds or no gain.
8. **Adversarial handoff review.** Before a `ready` or `conditional` proposal handoff, dispatch the novelty/gap, feasibility/method, and PI-strategy roles of `idea-adversarial-review-panel` concurrently in separate fresh subagents. Keep evaluator and peer reports sealed; aggregate after all return and preserve dissent.
9. **Resolve objections.** Route blocking evidence, method, framing, or candidate defects to the owning skill plus fresh evaluation; never hand a blocked idea to proposal workflow.
10. **Assemble portfolio.** Route sealed decisions and reports to `idea-portfolio-assembler`. It aggregates promoted, backup, merged, and rejected candidates without re-scoring or hiding dissent.
11. **Language QA.** If external-facing portfolio/handoff text needs language assessment, delegate `academic-language-assessor`; language work cannot change scores or statuses.

## Delegated Brief and Return Contract

Every reviewer brief records workflow/round, skill/scope, frozen IDs/versions/paths, allowed files, output path, prohibited reads/writes, and failure route. Reports use the standard review identity, files-read, isolation, prior-score, source-edit, decision, finding, and unresolved-issue fields. Subtasks return only a concise phase summary with artifact pointers, versions, decisions, unresolved issues, and `next_route`.

## Promotion and Stop Rules

- Stop on blocked context/evidence, unfixable fatal flaw, absent independent review, no-gain revision, or blocking adversarial objection.
- Any unresolved fatal finding prevents `promoted`, `conditional`, and proposal-ready status.
- Proposal handoff requires qualifying evaluation, visible evidence limitations, sufficient endpoint/data/method path, and no blocking adversarial objection.

## Conditional Resources

- Read `references/artifact-naming-and-directory-rules.md` for paths, versions, or the artifact index.
- Read `references/workflow-manifest.md` for state and round lineage.
- Use `templates/round-manifest.md` when recording a new workflow round.
- Read `references/idea-id-and-lineage-rules.md` when assigning, merging, or deriving idea IDs.
- Read `references/artifact-contracts.md` for cross-skill artifacts.
- Read `references/evidence-confirmation-and-routing.md` for supplied evidence and mapper scope.
- Read `references/delegate-brief-templates.md` for generator, preflight, evaluator, or adversarial briefs.
- Read `references/runtime-delegation.md` when independent dispatch is unavailable or uncertain.
- Read `references/loop-control-and-stop-rules.md` when revision or no-gain comparison begins.
- Read `references/evaluation-rubric.md` only when preparing the stable evaluator rubric.
- Read `references/if10-evaluation-gate.md` only when the user explicitly requests the IF>10 publication-feasibility gate.
- Read `references/handoff-validation.md` before each cross-skill handoff.
- Read `references/proposal-handoff-rules.md` before marking any proposal handoff status.

## Completion Check

Confirm state/index consistency, stable IDs and lineage, unique reviewer instances, prior-score blindness, new-version/new-evaluator pairing, complete adversarial roles, visible dissent, justified promotion states, and a proposal-ready handoff only when all gates pass.
