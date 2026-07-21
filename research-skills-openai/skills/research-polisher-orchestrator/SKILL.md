---
name: research-polisher-orchestrator
description: "Orchestrate reviewed impact strategies for completed research. Use for reframing or bounded extensions; exclude language editing, drafting, idea generation, and general search."
---
# research-polisher-orchestrator

## Role

Route completed research through independent strategy review, neutral assembly, rigor/publishability review, one continuation, and human selection. Control state and lineage only; never propose, score, revise, or select.

Use `standard` mode. Route language polishing, ordinary drafting, new-idea generation, and general literature search elsewhere.

## Invariants

- Freeze source IDs, paths, versions, SHA-256, claims, resources, and effort ceiling in `research_polisher_dossier-vNNN`.
- Give three fresh strategists the same frozen dossier/evidence and seal their reports from one another.
- Delegate all strategy and methodology/publishability review; never review inline.
- Permit one writer per artifact version; never run concurrent writes.
- A source change creates a new dossier and invalidates all old-digest strategies and evaluations.
- Require all three perspectives and all nine perspective-by-tier cells before assembly.
- Keep raw strategist reports and sealed provenance unavailable to the final reviewer.
- Preserve conflicts, limits, dissent, rejected options, and source-level fatal findings.
- Stop at human strategy selection; do not execute added research work or submit externally.

## Inputs

Accept sources, framing, audience/outlet, constraints, evidence map, and any verified target requirements. Route unstructured material to `article-context-builder`; reference its normalized facts.

Record `evidence_change_assessment` before retrieval. Reuse on `none`; use
Built-in Search or `focused-literature-synthesizer` for a bounded citation,
claim, or 2-5-paper question; call `research-landscape-mapper` only when core
positioning, novelty, the evidence landscape, or a material conflict changes
substantively, using `consumer_workflow: research_polisher` and
`output_profile: evidence_and_opportunity`. Store any deep-research round under
`02_evidence/deep-research/`. Inactive required research pauses at
`deep_research_handoff_required`; raw request/guide/report files stay outside
reviewer input packages.

## Workflow Kernel

1. **Initialize.** Record IDs, plugin version, `standard` mode, paths, state, round, objective, and work ceiling.
2. **Freeze.** Normalize raw material, then create `research_polisher_dossier-vNNN` with source digests and constraints. Stop for blocking clarification.
3. **Ground.** Reuse current evidence or route retrieval. A target adapter is verified only with ID, version, digest, source, and check time.
4. **Strategize.** Start mutually blind `research-polisher-strategy-reviewer` instances for `scientific_significance`, `practical_value`, and `dissemination_editorial`; each covers all effort tiers.
5. **Assemble.** Require an anonymous portfolio plus a separately sealed provenance index.
6. **Evaluate.** Give a fresh final reviewer only dossier, evidence, anonymous portfolio, and any verified target adapter.
7. **Specialist path.** For `specialist_review_required`, dispatch only named questions. The assembler emits a digest-bound sanitized bundle; a fresh final reviewer reads that bundle, not raw reports. This uses the remaining evaluator round.
8. **Revision path.** For `revision_required`, the assembler emits an anonymous must-fix brief using sealed routing. Re-dispatch affected perspectives—or all after a source change—then create a new portfolio version and use a fresh final reviewer. Never exceed two evaluator rounds total.
9. **Deliver.** Assemble `research_polisher_selection_dossier` with an unweighted Pareto view; stop at `human_strategy_selection_required`.

## Gates and States

- Waiting for review -> `pending_review`; missing source facts -> `clarification_stop`; required research continuation -> `deep_research_handoff_required`.
- Any required fresh reviewer unavailable -> `independent_review_pending`; do not partially assemble or review inline.
- Incomplete 3x3, stale lineage/digest, or identity leakage -> `blocked`.
- Evaluation requests repair and a revision round remains -> `revision_required`.
- Bounded specialist check with a round available -> `specialist_review_pending`, then fresh final review of the sanitized bundle.
- No defensible option or no gain after the second evaluator round -> `no_defensible_option` or `stopped`.
- Retained option, full adjudication, and no source-level fatal -> `human_strategy_selection_required`.

Option-level fatal findings reject that option. A source-level fatal finding blocks every option and the human-selection state.

## Revision and Handoff Rules

- Allow at most two evaluator rounds: initial evaluation plus one fresh continuation, whether that continuation follows strategy revision or specialist findings.
- After round two, compare reports only to record improvement, no gain, or the stop route; never expose the comparison to a reviewer.
- New strategists see only current frozen inputs, schema, and anonymous must-fix; new final reviewers see only the latest anonymous portfolio and allowed frozen evidence.
- After human selection, a `reposition_only` option may be handed to `article-architect` as an approved positioning constraint. A `small_extension` or `moderate_extension` option returns `additional_work_required`; it is not executed by this workflow.
- Emit a self-contained continuation package for every pause; portable import awaits its later contract.

## Output

Return a concise phase summary, current state, current artifact pointers, unresolved issues, and the next human action. Do not return raw review traces to the parent context.

## Conditional Resources

- For any finish/pause/stop, apply `research-idea-orchestrator/references/project-readme-contract.md`.
- Read `references/workflow-contract.md` for dossier, dispatch, state, continuation, or handoff artifacts.
- Read `research-polisher-strategy-reviewer/references/effort-tier-rules.md` before validating the 3x3 matrix.
- Read `research-polisher-plan-assembler/references/assembly-contract.md` before accepting a portfolio or selection dossier.
- Read `research-polisher-methodology-publishability-reviewer/references/evaluation-rubric.md` when interpreting evaluator decisions and routes.

## Completion Check

Confirm frozen sources, distinct reviewer IDs, all nine cells, sealed raw reports, fresh evaluation after change, visible dissent, and human selection.
