---
name: multi-path-idea-generator
description: "Generate a diverse, non-duplicative research-idea set from approved context and opportunity maps; do not evaluate or rank it."
---
# Multi-Path Idea Generator

## Role

Generate or revise candidate Ideas from frozen context, opportunity maps, user
constraints, and assigned generation paths. Do not evaluate, score, rank,
promote, reject, run methodology review, or write a proposal.

## Invariants

- Ground every novelty/value claim in supplied evidence; mark unsupported scope
  `unverified` rather than inventing support.
- Keep candidates substantively distinct and preserve opportunity/path lineage.
- Write each Idea as a complete Markdown snapshot in one flat node. A patch,
  changed-section list, or delta is never the current Idea.
- Keep revisions in the same node. Identity drift to a different research
  problem returns `new_idea_required`; never create a child without explicit
  user authorization.
- Return every frozen snapshot to the orchestrator for fresh independent
  preflight/evaluation; never self-review.

## Procedure

1. **Validate.** Confirm context, opportunity/evidence limits, constraints,
   requested paths, and existing nodes. Return a generation failure report when
   the material cannot support a complete Idea.
2. **Select paths.** Use assigned paths or recommend a bounded set based on the
   opportunity type and constraints; the orchestrator retains routing control.
3. **Generate.** Create a small diverse set. Each snapshot must state the whole
   current Idea: summary, question/objectives, work packages, hypothesis,
   significance, impact/innovation, applications, evidence base, methods,
   required analyses/evidence, feasibility/resources, and risks/stops.
4. **Control duplicates.** Merge only equivalent candidates at generation time;
   otherwise keep meaningful variants distinct. Never disguise a title change
   as a new Idea.
5. **Persist.** Create/update node pointers and identity anchors, compute each
   snapshot SHA-256 outside the snapshot, and write an immutable concise
   candidate-set index without copied prose.
6. **Handoff.** Return node IDs, snapshot paths/versions/digests, paths,
   opportunity IDs, uncertainties, and downstream preflight needs. Do not return
   a verdict.

## Outputs and Stops

- Write complete snapshots and the candidate-set handoff template on success.
- Return `generation_blocked` for missing support, `new_idea_required` for
  identity drift, or `layout_migration_required` for a legacy project layout.
- Mark `evaluation_needed: true`, `handoff_to: idea-evaluator`, and
  `must_be_isolated: true` for every current snapshot.

## Conditional Resources

- Read `research-idea-orchestrator/references/idea-artifact-lifecycle.md` whenever creating or revising an Idea node or snapshot.
- Read `research-idea-orchestrator/references/artifact-contracts.md` for shared fields.
- Read `research-idea-orchestrator/references/handoff-validation.md` before handoff.
- Read `references/idea-schema.md` for node and candidate-index outputs.
- Read `references/generation-paths.md` when applying the ten generation paths.
- Read `references/path-selection-rules.md` when selecting paths.
- Read `references/novelty-claim-rules.md` when limiting novelty claims.
- Read `references/duplicate-control-rules.md` when candidates overlap.
- Read `references/generation-quality-gates.md` before persistence.
- Read `references/downstream-handoff-rules.md` before preflight/evaluation.
- Use `templates/generated-idea-set.md` for the concise candidate-set handoff.
- Use `templates/generation-failure-report.md` when generation cannot proceed.

## Completion Check

Confirm complete snapshots, whole-Idea summaries, stable nodes/identity, matching
digests and indexes, distinct paths, evidence limits, no evaluation, and an
isolated downstream route.
