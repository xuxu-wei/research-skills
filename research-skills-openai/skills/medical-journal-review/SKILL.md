---
name: medical-journal-review
description: "Independently review research rigor, journal fit, and supportable publication probability."
---
# Medical Journal Research Design Review

## Purpose

Independently assess a medical study, protocol, proposal, manuscript, or submission artifact from editorial, clinical-epidemiology, and statistical perspectives. Identify fatal flaws, weaknesses, defensible claims, journal fit, and repair priorities. When the target outlet and available material support it, append a scoped publication-probability assessment to this same review report.

The substantive rigor review is medical-domain work. A requested probability assessment may cover a non-medical artifact, but must state its domain limits. This skill evaluates frozen artifacts; it does not draft, rewrite, polish, repair, or promise publication.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread, never in the context that generated, drafted, or revised the artifact.
- Receive artifact IDs, paths, versions, and digests as applicable;
  Idea matching uses `{artifact_id, version, path}` without a required digest.
  Treat inputs as read-only and write only this review report.
- Do not edit, rewrite, polish, repair, or modify the reviewed design, protocol, proposal, manuscript, cover letter, tables, figures, or supplements.
- Do not use parent hidden reasoning, expected conclusions, prior reviewer outputs, or prior scores. Use only frozen allowed inputs and the declared rubric.
- Idea matching must not read an evaluator report or receive its scores, gates,
  decision, findings, or repairs; require a clean candidate brief.
- Report exact files read, sections reviewed, missing materials, scope limits, and reviewer instance ID.
- If a fresh subagent is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop; never fall back to inline review.

## Inputs

Accept the available subset of:

- research question, intended claim, and contribution statement;
- study type, population, exposure/intervention, comparator, outcomes, and time window;
- data source, sample size, protocol/SAP, analysis plan, and results;
- manuscript, Perspective, cover letter, tables, figures, appendices, and supplements;
- target outlet, article type, supplied benchmark facts, and frozen artifact identity.
- for Idea matching, one current dossier logical reference and one matching
  embedded or file-backed `research-idea-journal-candidate-brief.v1`.

When a manuscript cites supplementary material, inspect supplied task files and the artifact manifest. Do not infer association from upload proximity or search product caches; verify title, author, identifier, or manifest linkage. Distinguish what can and cannot be judged when inputs are incomplete.

## Review Route

Choose and record one route:

- **Design review**: question–design fit, endpoint, comparator, bias, confounding, analysis, and redesign.
- **Editorial review**: importance, gap, claim support, completeness, fit, and revision priority. Load `references/12-step-editorial-review.md`.
- **Statistical review**: estimand, model–data fit, missingness, multiplicity, uncertainty, validation, sensitivity, and interpretation. Load `references/bmj-statistical-review-standards.md`.
- **Cover-letter-only review**: editorial triage case, source-bounded claims, outlet fit, and limitations visible from the letter alone. Do not infer manuscript quality from unavailable material.
- **Idea journal-match editorial review**: confirm, reject, or replace score-free
  candidates under `references/idea-journal-match-editorial-route.md`; do not
  load the 12-step or publication-probability frameworks.

## Workflow

For `idea_journal_match_editorial_review`, follow its dedicated reference and
template, return its decision, and stop without scoring the Idea or estimating
publication probability.

For every other route, continue with the established workflow:

1. Record frozen inputs, route, target outlet, article type, requested assessment scope, and limitations.
2. Identify the study and claim type plus the decision the evidence is meant to support.
3. Summarize the available population, data, intervention/exposure, comparator, outcomes, timing, and analysis.
4. Check design–question fit and whether the evidence supports the claims.
5. Check endpoints, bias, confounding, missingness, multiplicity, validation, and uncertainty as applicable.
6. Inspect supplied tables, figures, and supplements before declaring an analysis absent.
7. Separate fatal, major, and minor findings; identify claims requiring downscaling.
8. Give feasible repair or redesign routes when defects are reparable.
9. Assess target-outlet fit. When probability is explicitly requested or the current medical-review call has adequate target and artifact inputs, load `references/publication-probability-assessment.md` and append its block to this report. Use built-in Search only for current public benchmark facts.
10. Produce one structured report using `templates/review-report.md`; never create a separate probability artifact.

## Decision Labels

- `support`
- `support_with_minor_revision`
- `major_revision_required`
- `redesign_required`
- `not_reviewable_with_current_materials`
- `fatal_flaw`

The Idea journal-match route instead returns exactly one of:

- `journal_candidates_confirmed`
- `journal_candidates_revised`
- `no_supported_journal_candidate`
- `not_reviewable_with_current_materials`

## Report Contract

Every report includes:

```yaml
review_id:
reviewer_skill: medical-journal-review
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids:
input_versions:
files_read:
review_route:
review_scope:
scope_limitations:
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
fatal_flaws:
major_findings:
minor_findings:
claim_adjustments:
repair_or_redesign_options:
journal_fit:
publication_probability_assessment: null | object
unresolved_issues:
```

The optional object follows the conditional probability contract. Its absence
never creates a separate workflow state.

## Boundaries

- Do not draft or revise the reviewed artifact.
- Do not infer unreported analyses from filenames or narrative hints.
- Check supplied supplements before declaring an analysis missing.
- Do not present observational or predictive findings as causal, or method novelty as proof of importance.
- Do not let a probability estimate override fatal, blocking, stale-input, or reviewer-isolation gates.
- Preserve dissent, uncertainty, missing evidence, scope limits, and fatal flaws.
- Evaluator-supplied candidates have no privileged status and reveal no hidden
  evaluation.

## Verification

- Review ran in a fresh independent subagent against frozen reported inputs; all files read are listed and source artifacts are unchanged.
- Study and claim type, checked supplements, fatal findings, scope limits, and traceable recommendations are visible.
- When probability is assessed, it remains in this report, scope and benchmark status are explicit, Search sources record URL/date/type/applicability, stage and overall estimates are coherent, and unsupported cases use `not_estimable`.
- Idea matching binds the dossier and clean brief, separates URLs from files,
  hides evaluator output, and disposes every candidate.

## Conditional Resources

- Read `references/12-step-editorial-review.md` only for an editorial route.
- Read `references/bmj-statistical-review-standards.md` only for a statistical route.
- Read `references/publication-probability-assessment.md` only when producing or validating the optional probability block.
- Use `templates/review-report.md` only when writing the review report.
- Read `references/idea-journal-match-editorial-route.md` only for
  `idea_journal_match_editorial_review`.
- Use `templates/idea-journal-match-review.md` only for
  `idea_journal_match_editorial_review`.
