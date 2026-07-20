# Perspective Journal Matching and Medical Review

Use this route only after the final Perspective version has passed its blind final
evaluation. Keep journal matching and medical review independent from evaluator
scores, findings, gates, decisions, and repair history.

## Concrete outlet facts

If the user selected a journal, verify its current official scope, article type,
audience, length, reference, abstract, figure, submission, and eligibility rules.
Record official URLs and last-checked dates. If no journal is selected and outlet
targeting is requested, prepare an unscored, unranked candidate brief with a bounded
set of concrete journals and one evidence-based fit rationale and uncertainty for
each. Do not present generic profiles as concrete matches.

Save the clean brief under `08_journal/candidate-journal-match-brief-vNNN.yaml`.
It contains no evaluator or panel material, publication-probability estimate, score,
rank, or recommendation inherited from another reviewer.
Use `../templates/candidate-journal-match-brief.yaml` for its schema.

## Medical-journal-review

Dispatch one fresh `medical-journal-review` when the Perspective is biomedical or
clinical, when medical editorial review is requested, or when a supportable
publication-probability assessment is explicitly requested. Use its editorial route
unless its own contract requires another route.

Allowed project inputs are the final frozen Perspective, verified target-outlet facts
or clean candidate brief, and an optional current cover letter. Forbid every evaluator,
panel, narrative/language assessment, repair brief, delta, readiness report, score,
finding, gate, and decision. Require `prior_scores_visible: false`.

Save the report under `08_journal/medical-journal-review-vNNN.md`. A finding that
requires manuscript change routes back to the owning scientific or editorial stage;
the changed version repeats applicable preservation, reassessment, and final
evaluation. The medical review cannot override a fatal or final-evaluation gate.
If a cover letter is created or changed after this review, the review is stale and a
fresh medical review is required before final composition.

For non-biomedical work with no requested specialist review, record `not_applicable`
in state and proceed without fabricating a medical opinion.
