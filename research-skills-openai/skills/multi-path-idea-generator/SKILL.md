---
name: multi-path-idea-generator
description: "Generate or revise one focused Idea or a bounded set of evidence-supported directions; do not evaluate or rank."
---
# Multi-Path Idea Generator

## Role

Write complete Idea dossiers from frozen context, evidence, route, and
constraints. Do not evaluate, rank, run methods review, or write proposals.

## Invariants

- The complete dossier is the Idea; include its chains, Claim-Support, and normal
  references. Internal IDs are not evidence.
- Return proposed navigation metadata by artifact ID, version, and path; only the
  orchestrator writes state. Require complete index membership; every `based_on`
  is mapped, and a path-only lineage entry is invalid.
  Do not compute, request, report, or persist SHA/content hashes.
  Bind the delegated plugin version; Never inherit a legacy input artifact's plugin version.
- Keep revisions in the same node. Title/audience/editorial repositioning is not
  identity drift, but it creates a new dossier version. A new primary problem,
  objective, object, evidence base, or unit of inference returns
  `new_idea_required`.
- After preflight repair, return the current dossier for fresh narrative/language
  review before dossier-only evaluation; never declare it ready.
- Scientific revision uses only complete `working_assumption` objects supplied by
  preflight. Never invent the assumed value, basis, verification point, or
  affected component.

## Procedure

1. **Validate.** Confirm inputs, route, nodes, references, and any approved
   assumption objects; v1/v2 are read-only. Incomplete assumptions return
   `clarification_required`.
2. **Apply route.** For `focused_optimization`, create or revise one dossier. For
   `bounded_exploration`, create two or three only when each direction has
   moderate/high support; never fill a quota.
3. **Establish the reader chain.** Before technical detail, write the entry and
   five ordered background functions. Introduce the problem before specialized
   concepts; make the summary identify object/question, approach/test, and
   positive contribution. Mention contingent work only by purpose and condition,
   without its decision tree or unexplained project labels.
4. **Add the technical design.** Make every claim traceable to a chain output,
   existing result, or normal citation.
5. **Position honestly.** Supported title/audience reframing is allowed. Similar
   work may offer validation, application, integration, resource, or benchmark
   value; scientific/data/method novelty requires a real increment.
6. **Control overlap.** A title-only variant is the same Idea/version lineage,
   not another direction. Keep only substantively different research identities
   in bounded exploration.
7. **Run the mechanical editorial pass.** Check first-use explanations, remove
   repeated caveats/internal workflow language, enforce authority locations,
   and flag uncertain terms for language review.
8. **Persist content.** Write the dossier and separate delta; return proposed
   node/index/ledger entries for orchestrator persistence.
9. **Bounded remap.** After one optimization per direction, remap each. Integrate
   evidence/claim sync in a new dossier; structural change returns
   `revision_required`.
10. **Handoff.** Return logical pointers, route, uncertainty, preflight needs,
    and `editorial_assessment_needed: true`; never return a verdict.

## Stops

Return `generation_blocked` for inadequate support,
`direction_route_confirmation_required` for unresolved routing,
`new_idea_required` for identity drift, `revision_required` for structural
post-remap change, or `layout_migration_required` for v1/v2 layouts.

## Conditional Resources

- Read orchestrator `idea-artifact-lifecycle.md` for node/version work and
  `idea-dossier-contract.md` for dossier work.
- Read `research-idea-orchestrator/references/adaptive-direction-routing.md` for
  route selection or remapping.
- Read orchestrator `reference-ledger-contract.md` for internal IDs/ledger work.
- Read preflight `working-assumption-rules.md` for `proceed_with_assumptions`.
- Use `templates/idea-dossier.md` when producing a Dossier.
- Read `references/idea-schema.md` for node and index fields.
- Read `references/generation-paths.md` for an assigned path.
- Read `references/path-selection-rules.md` when recommending one.
- Read `references/novelty-claim-rules.md` for novelty claims.
- Read `references/duplicate-control-rules.md` for overlap checks.
- Read `references/generation-quality-gates.md` before persistence.
- Run `scripts/lint_idea_dossier.py <dossier> --expected-plugin-version
  <version>` before persistence; it checks structure/version, not readiness.
- Run `scripts/test_lint_idea_dossier.py` only when changing the deterministic
  dossier lint contract.
- Read `references/downstream-handoff-rules.md` before return.
- Use `templates/generation-failure-report.md` on failure.

## Completion Check

Confirm route-compliant count, complete dossiers/chains/claims/references, the
ordered five-function reader chain, section-14 limitation authority, stable
identity, matching logical navigation metadata, a passing structural lint, no
self-declared readiness/evaluation, and isolated downstream review.
