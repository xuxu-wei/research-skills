---
name: perspective-orchestrator
description: "Orchestrate Perspective planning, review, reader readiness, and delivery."
---
# perspective-orchestrator

## Role and Gates

Control state/routing; never write prose, score work, edit the ledger, or repair a
package. Keep state/logs in `09_state/`: review waits use `pending_review`, unavailable
independent review uses `independent_review_pending`, fatal work is `blocked`, and
unfixable/no-gain work is `stopped`.

- The curator alone writes the ledger; every text change creates a draft/map version
  and needs fresh qualifying evaluation.
- Use one writer per source version; never allow concurrent source writes. Reviewer
  work runs in fresh independent subagents.
- Register `{artifact_id, version, path}` plus complete index membership. Legacy
  digests are read-only and never gates.
- Preserve unresolved issues, conflicts, fatal findings, and dissent. Never submit.

Select mode with `references/workflow-modes.md`. Lite performs provisional claims/evidence
preprocessing and cannot claim readiness; full reaches STEP 12.

## Core Route

1. **Input.** Initialize state/layout; use `perspective-input-builder` for brief/outlet.
2. **Curate.** Use `perspective-claim-evidence-curator` for ledger, bindings, discourse,
   contrary evidence, citation risks, and limits; standard/full may add broad mapping.
3. **Architect.** Use `perspective-argument-architect`; freeze the complete embedded
   reader-handoff payload and copy it, not the manifest/skeleton, into later briefs.
4. **Draft/check.** Use `perspective-drafter`. Require a registered draft/map, then
   fail-closed plan/ledger/Binding/terminology/authority/map checks outside evaluation.
5. **Evaluate/revise.** A fresh `perspective-evaluator` routes non-accept work upstream.
   Changed versions get fresh evaluation without prior scores/decisions.
6. **Panel.** In full mode, run counter-position and evidence roles in parallel. An
   optional target-reader/outlet simulation is advisory only. Hide peer/evaluator
   reports and preserve dissent.
7. **Route.** Support enters STEP 9; minor edits use STEP 8.5; substantive work returns
   upstream and gets fresh evaluation; unfixable redesign/rejection stops.

### STEP 8.5: Panel Minor Revision Patch

Save the bounded patch/map/delta and require a fresh evaluator. No changed draft goes directly to the compositor.

### STEP 9: Editorial Quality Cycle

After scientific/panel closure: freeze the accepted Perspective, writer, reader
handoff, and protected register; run fresh `research-narrative-assessor`
(`perspective` profile) and `academic-language-assessor` instances in parallel,
mutually isolated from review/history. The
controller creates one YAML brief; the same writer receives only source, brief, and
register. Then run fail-closed conformance, fresh content preservation, and fresh
parallel reassessments with minimal handoffs. Missing writer yields
`editorial_repair_pending`; any scientific change restarts scientific revision. Final
evaluation requires conformance, `scientific_content_preserved`, `narrative_ready`,
and `submission_ready`.

### STEP 10: Final Evaluator

Delegate a fresh final `perspective-evaluator`. Its exact project whitelist is the
final frozen Perspective plus one clean minimal evidence/outlet facts bundle; its only
installed evaluation resources are the stable rubric and anti-pattern checklist. It
must never receive the brief, skeleton, map, ledger/matrix, readiness/state, repair,
delta, conformance/preservation output, narrative/language report, artifact index,
panel/prior review, score, finding, gate, or decision.

### STEP 11: Outlet and Medical Review

Create concrete journal matching from official facts, outside evaluator
scoring. If requested, freeze the `article-cover-letter` pair under `08_cover-letter/`
before medical review. For biomedical/clinical work or an explicit medical or
publication probability request, run a fresh
`medical-journal-review` on only the final Perspective, clean outlet facts/brief, and
optional current letter—never evaluator, panel, repair, readiness, score, finding,
gate, or decision material. Any later text/letter change makes applicable review
stale.

### STEP 12: Final Compositor

Give frozen qualifying sources, the read-only index, a score-free final-evaluation
receipt, optional letter, and applicable specialist report to a fresh compositor. It
copies/verifies only, writes under `08_final/`, and returns `packaging_pending` with
proposed index entries. The orchestrator registers and verifies them; only then set
`human_signoff_required` for a concrete qualifying outlet or
`outlet_targeting_only` for a generic profile.

## Promotion Boundary

Delegates return a concise phase summary with artifact pointers and `next_route`.
Never promote a fatal finding; final draft identity/version must match the blind final
evaluation after conformance, preservation, and reassessment.

## Conditional Resources

- Read `../research-idea-orchestrator/references/project-readme-contract.md` when finishing, pausing, or stopping.
- Read `references/workflow-modes.md` when selecting mode; read `references/workflow-manifest-schema.md` when updating state.
- Read `references/decision-log-schema.md` for decisions; read `references/artifact-naming-and-directory-rules.md` for identity/index.
- Read `references/io-contracts.md` for handoffs; read `references/delegate-brief-templates.md` before delegation.
- Read `references/loop-control-rules.md` for revision/stop; read `references/panel-decision-routing.md` before panel aggregation.
- Before STEP 9, read `../perspective-refinement-controller/references/editorial-repair-contract.md`.
- Before STEP 11, read `references/journal-matching-and-medical-review.md`; use `templates/candidate-journal-match-brief.yaml` for every journal brief.
- Before evaluation, use `templates/pre-evaluation-conformance.yaml` outside the evaluator package.
- Read `references/generic-outlet-profiles.md` when no outlet is selected; read `references/anti-patterns.md` for the final scan.

## Completion Check

Confirm state/log, ledger ownership, version/preservation gates, same-writer repair,
blind final evaluation, dissent, specialist isolation, identity/index completeness,
status caps, and human-only handoff.
