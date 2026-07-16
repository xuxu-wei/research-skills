# Idea Evaluation Rubric

Use this canonical rubric for one frozen, complete v3 dossier. Score only the
dossier; do not browse, retrieve project context, or reconstruct missing facts.

## Scale

Use integer scores from 1 to 5:

- `1`: invalid or critically deficient;
- `2`: major weaknesses;
- `3`: defensible but requires repair;
- `4`: strong and ready for the next gated step;
- `5`: unusually strong, coherent, and well supported.

Compute the unweighted mean of all six dimensions.

## Dimensions

- **Novelty:** The stated contribution is distinguishable from closest work and
  supported by citations and evidence chains. Honest replication, validation,
  application, translation, integration, resource, or audience value may be
  strong without a novel method or dataset.
- **Feasibility:** Inputs, access, methods, resources, dependencies, and stop
  conditions make every major work package executable.
- **Impact:** The supported outputs could create meaningful scientific,
  practical, methodological, translational, or dissemination value. Audience
  breadth counts only when the implementation supports the positioning claim.
- **Relevance:** The question, contribution, audience, and output align with the
  user's stated goal and constraints.
- **Clarity:** Question, objectives, hypothesis, design, evidence chains,
  expected outputs, and claim boundaries are precise and mutually consistent.
- **Completion:** The dossier is self-contained, all 15 sections are substantive,
  references resolve, evidence chains close, and risks and required work are explicit.

## Hard gates

Feasibility, Relevance, Clarity, and Completion must each be at least `3.0`.
Any fatal flaw overrides the mean. Fatal examples include an unanswerable
question, unusable core input, method-question mismatch, unsupported primary
title/positioning claim, irreparable evidence-chain break, or infeasible
dependency.

## Decision anchors

- `promote`: mean >= 4.2 and every gate passes.
- `revise_then_promote`: mean >= 3.6 and < 4.2, every gate passes, and repairs are bounded.
- `revise` or `reframe`: mean >= 3.0 and < 3.6, or a fixable gate failure.
- `keep_as_backup`: mean >= 2.5 and < 3.0 with a defensible non-priority route.
- `reject`: mean < 2.5 or an unfixable/fatal flaw.

Under dossier-only v3 evaluation, do not choose `merge`: no other Idea is an
allowed input. If a proposed repair would replace an identity anchor, set
`identity_drift_detected: true`; the orchestrator returns `new_idea_required`
and must not auto-fork or merge.

Each score and finding must cite a human-readable dossier heading, table row,
or evidence-chain title. Do not use internal markers as evidence. Record a
finding `title`, `dossier_locator`, severity, and rationale, then provide bounded
repair directions without replacement prose.
