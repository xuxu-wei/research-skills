---
name: multi-path-idea-generator
description: "Generate or revise one focused Idea or a bounded set of evidence-supported directions; do not evaluate or rank."
---
# Multi-Path Idea Generator

## Role

Write complete Idea dossiers from frozen context, evidence, route, and
constraints. Do not evaluate, rank, run methods review, or write proposals.

## Invariants

- The complete `idea-dossier-vNNN.md` is the Idea; patches, deltas, maps, and
  indexes are not. Include evidence chains, Claim-Support, and normal references;
  never use internal IDs as dossier evidence.
- Return node/index/ledger metadata and the external SHA-256; the orchestrator
  is the sole writer of navigation/state metadata.
- Keep revisions in the same node. Title/audience/editorial repositioning is not
  identity drift, but it creates a new dossier version. A new primary problem,
  objective, object, evidence base, or unit of inference returns
  `new_idea_required`.
- Return every frozen dossier for fresh dossier-only review; never self-review.

## Procedure

1. **Validate.** Confirm inputs, route, nodes, and digests; v1/v2 are read-only.
2. **Apply route.** For `focused_optimization`, create or revise one dossier. For
   `bounded_exploration`, create two or three only when each direction has
   moderate/high support; never fill a quota.
3. **Write.** Make every claim traceable to a chain output, existing result, or
   normal citation.
4. **Position honestly.** Supported title/audience reframing is allowed. Similar
   work may offer validation, application, integration, resource, or benchmark
   value; scientific/data/method novelty requires a real increment.
5. **Control overlap.** A title-only variant is the same Idea/version lineage,
   not another direction. Keep only substantively different research identities
   in bounded exploration.
6. **Persist content.** Write the dossier and separate delta; return proposed
   node/index/ledger entries and digest for orchestrator persistence.
7. **Bounded remap.** After one optimization per direction, remap each. Integrate
   evidence/claim sync in a new dossier; structural change returns
   `revision_required`.
8. **Handoff.** Return pointers/digests, route, uncertainty, preflight needs, and
   `evaluation_needed: true`, never a verdict.

## Stops

Return `generation_blocked` for inadequate support,
`direction_route_confirmation_required` for unresolved routing,
`new_idea_required` for identity drift, `revision_required` for structural
post-remap change, or `layout_migration_required` for v1/v2 layouts.

## Conditional Resources

- Read `research-idea-orchestrator/references/idea-artifact-lifecycle.md` for node
  or version work.
- Read `research-idea-orchestrator/references/idea-dossier-contract.md` for dossier work.
- Read `research-idea-orchestrator/references/adaptive-direction-routing.md` for
  route selection or remapping.
- Read `research-idea-orchestrator/references/reference-ledger-contract.md` for
  internal IDs or ledger updates.
- Use `templates/idea-dossier.md` when producing a Dossier.
- Read `references/idea-schema.md` for node and index fields.
- Read `references/generation-paths.md` for an assigned path.
- Read `references/path-selection-rules.md` when recommending one.
- Read `references/novelty-claim-rules.md` for novelty claims.
- Read `references/duplicate-control-rules.md` for overlap checks.
- Read `references/generation-quality-gates.md` before persistence.
- Read `references/downstream-handoff-rules.md` before return.
- Use `templates/generation-failure-report.md` on failure.

## Completion Check

Confirm route-compliant count, complete dossiers/chains/claims/references,
stable identity, matching navigation metadata/digest, visible limits, no
evaluation, and dossier-only downstream review.
