# Reviewer Role Definitions

## Counter-position Reviewer

Task: attack the thesis and argument chain from the strongest plausible opposing position.

Allowed focus: missing counterarguments, weak transitions, strawman treatment, hidden assumptions.

## Evidence Reviewer

Task: audit whether claims are supported by the evidence matrix and contrary evidence log.

Allowed focus: unsupported claims, citation mismatch, overclaiming, missing boundary conditions.

## Optional Target-Reader / Outlet Simulation

Trigger: uncertain reader baseline, a concrete outlet simulation that would change routing, or an explicit user request.

Task: simulate one named reader or editor's on-page understanding without seeing the argument skeleton, scientific reviewer outputs, or readiness history.

Allowed focus: comprehension breaks, concept burden, likely misreadings, title/abstract expectations, and outlet-sensitive reactions.

Output boundary: locatable observations only. Do not issue narrative readiness, language readiness, publication readiness, or a duplicate evaluator decision. Route full narrative assessment to `research-narrative-assessor`.

Required and conditional scientific reviewers state whether their recommendations
would change under a wider or narrower target outlet. The optional simulation states
how its observations would change, without issuing a recommendation or readiness
decision.

## Conditional Reviewers

Conditional reviewers are additive. Use them only when the trigger is present.

### Methodology / Statistics Reviewer

Trigger: method-heavy, causal, predictive, statistical, benchmark, or study-design claims.

Task: audit whether methodological or statistical claims are properly bounded and whether the article overstates what the methods can establish.

Allowed focus: endpoint-method fit, causal language, benchmark comparability, statistical overreach, design limitations.

### Practicing-Clinician Reviewer

Trigger: clinical medicine, public health practice, patient care, guideline interpretation, screening, diagnosis, treatment, or implementation in care settings.

Task: audit clinical plausibility, endpoint relevance, practice-facing implications, and credibility to a frontline clinician.

Allowed focus: real-world clinical importance, patient/clinician relevance, guideline interpretation risks, actionability.

Legacy `narrative_reviewer` and `outlet_fit_editor_reviewer` labels are read-compatible aliases for `target_reader_outlet_simulation`; do not dispatch both.
