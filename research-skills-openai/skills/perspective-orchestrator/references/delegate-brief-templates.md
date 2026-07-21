# Delegate Brief Templates

## Contents

<!-- toc:start -->
- [Input Builder Brief](#input-builder-brief)
- [Evaluator Brief](#evaluator-brief)
- [Final Evaluator Brief](#final-evaluator-brief)
- [Counter-Position Reviewer Brief](#counter-position-reviewer-brief)
- [Evidence Reviewer Brief](#evidence-reviewer-brief)
- [Target Reader Outlet Simulation Brief](#target-reader-outlet-simulation-brief)
- [Methodology / Statistics Reviewer Brief](#methodology-statistics-reviewer-brief)
- [Practicing-Clinician Reviewer Brief](#practicing-clinician-reviewer-brief)
- [Narrative And Language Assessment Briefs](#narrative-and-language-assessment-briefs)
- [Content Preservation Brief](#content-preservation-brief)
- [Medical Journal Review Brief](#medical-journal-review-brief)
- [Final Compositor Brief](#final-compositor-brief)
<!-- toc:end -->

本文件包含 orchestrator 派发所有 delegate 子 agent 时使用的 brief 模板。

Every evaluator, reviewer, assessor, and final verifier brief must identify the reviewer skill/role, reviewer instance ID, workflow/round IDs, frozen artifact IDs/exact paths/versions, allowed and prohibited files, review scope, and output path. Run each brief in a fresh independent subagent/delegated thread. If that is unavailable, return `independent_review_pending` with the completed brief and stop; never run inline.

Every completed review artifact must report `files_read`, `review_scope`, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, and `source_edits_performed: false`. Fresh re-evaluation must not receive prior scores or prior decisions. Panel reviewers must not receive evaluator reports or other reviewer outputs.

Use logical artifact identity (`artifact_id`, `version`, `path`) and exact file
whitelists. New LLM-facing briefs and reports never require or generate SHA, content
hashes, or digests. Legacy digest metadata may be ignored on read.

Initial Standard/Full curator briefs must cite the staged write order in `perspective-claim-evidence-curator/SKILL.md`, serialize one writer, persist row-dense files as a header plus bounded stable-ID groups plus a final read-only check, retry only an idle/interrupted or non-progressing current file/batch once, preserve completed batches, treat a passing artifact check as sufficient without waiting for delegate final text, and never ask for hashes or digests.
---

## Input Builder Brief

```
Normalize the one whitelisted user input for Perspective STEP 1. Do not research,
evaluate, design the argument, or draft article prose.

Allowed project file: {exact user-input path}.
Installed resources: perspective-input-builder/SKILL.md, its template, and Generic outlet profiles.
Required outputs: 00_input/01-input-brief.md, 00_input/target-outlet-profile.md, and 00_input/assumption-log.md.

Create these three files immediately after reading the allowed input, then fill and validate them.
Mark unknowns `provisional`; do not delay the first write to elaborate all fields in memory.
Generate `00_input/00-perspective-input-template.md` only if the input must be returned to the user.
In that branch, do not create the three normal outputs; pause and return `next_route: clarification_required`.
Write nowhere else.
```

---

## Evaluator Brief

```
## Your Role
Independent scientific evaluator. Evaluate the Perspective draft against the stable eight-dimension rubric. Do NOT revise, rewrite, or broaden scope.

## Allowed Files (whitelist)
- input-brief.md / argument-skeleton.md / perspective-v{N}.md / perspective-v{N}-paragraph-map.md / claim-ledger.md / claim-evidence-matrix.md / target-outlet-profile.md / existing-discourse-baseline.md

## Procedure
1. FIRST PASS: Read draft alone. Score Thesis Clarity, Narrative Coherence, Stance Calibration, Contribution Sufficiency, Audience Fit, Novelty. Do NOT consult paragraph-map.
2. SECOND PASS: Read paragraph-map. Score Argument Integrity, Evidence-Claim Match.
3. ANTI-PATTERN: Scan all 12 patterns.
4. SYNTHESIZE + decision.

## Required Output
evaluation-report-v{N}.md: eight scores with paragraph references, hard gate status, anti-pattern findings, fatal flaws, decision.

## Constraints
Do NOT revise. Cite specific paragraph numbers. If discourse baseline missing, mark Novelty provisional. For re-evaluation, read only the latest frozen draft, stable rubric, necessary facts, and an optional anonymous must-fix list; do not provide a prior draft, revision delta, prior score, or decision.
```

---

## Final Evaluator Brief

```
## Your Role
Fresh final evaluator. Judge only the final frozen Perspective against the installed stable rubric and clean facts. Do not revise or infer a hidden plan.

## Allowed Project Files (exact whitelist)
- perspective-v{N}.md
- minimal-evidence-outlet-facts-v{N}.yaml

## Installed Contract
- ../../perspective-evaluator/references/stable-evaluation-rubric.md
- ../../perspective-evaluator/references/anti-pattern-checklist.md

## Prohibited
Input brief, skeleton, paragraph map, claim ledger/matrix, readiness report, repair brief, conformance/preservation output, revision delta, narrative/language report, prior review/evaluation, panel, artifact index, workflow state, score, finding, gate, or decision.

## Required Output
final-evaluation-report-v{N}.md with `evaluation_stage: final`, exact files read, eight scores, hard gates, anti-pattern scan, findings, unresolved issues, and decision.

## Isolation
Run in a fresh instance. `prior_scores_visible: false`; `source_edits_performed: false`. The deterministic pre-evaluation checks remain outside this package.
```

---

## Counter-Position Reviewer Brief

```
## Your Role
Hold OPPOSITE academic position. Attack core thesis and each argument chain step. Find weakest link.

## Allowed Files
draft-current.md, argument-skeleton.md

## Required Output
Resistance score (1-5) per step, weakest link, overall recommendation.
STATEMENT: Would recommendation change if outlet were broader/narrower?

## Constraints
Use STRONGEST counter-arguments. No strawmen. Do NOT revise.
```

---

## Evidence Reviewer Brief

```
## Your Role
Audit evidence-claim mapping. Check strongest claims vs. strongest evidence, contrary evidence addressed, over-interpreted citations.

## Allowed Files
draft-current.md, claim-evidence-matrix.md, claim-ledger.md, contrary-evidence-log.md

## Required Output
Evidence sufficiency (1-5) per step, gaps, overclaim risks.
STATEMENT: Would recommendation change if outlet were broader/narrower?

## Constraints
Focus on claim-evidence MATCH, not evidence quality alone.
```

---

## Target Reader Outlet Simulation Brief

Use only when the declared reader baseline is uncertain, a concrete outlet simulation
would change routing, or the user explicitly requests it. New briefs use
`target_reader_outlet_simulation`; legacy narrative/outlet-editor labels are read-only
aliases.

```
## Your Role
Read as one named target reader or outlet editor. NO skeleton, evidence package, or readiness history is provided; report only what that reader can understand on the page.

## Allowed Files
draft-current.md, embedded reader-reasoning handoff, and target-outlet-profile.md only when simulating a concrete outlet

## Required Output
Locatable comprehension breaks, concept burden, likely misreadings, and outlet-sensitive reactions.
STATEMENT: How would the observations change for a broader/narrower reader or outlet?

## Constraints
Do NOT infer author intent from missing files. Do not issue narrative readiness, language readiness, publication readiness, or a duplicate evaluator decision. Route full narrative assessment to research-narrative-assessor.
```

---

## Methodology / Statistics Reviewer Brief

Use only when method-heavy, causal, predictive, statistical, benchmark, or design-quality claims are central.

```
## Your Role
Audit methodological and statistical claim discipline. Do NOT revise, rewrite, or broaden scope.

## Allowed Files
draft-current.md, claim-evidence-matrix.md, claim-ledger.md, anonymous-methods-facts.md if needed

## Required Output
Method/claim fit assessment, overreach risks, causal/statistical language risks, recommendation.
STATEMENT: Would recommendation change if outlet were broader/narrower?

## Constraints
The methods facts file must contain source facts only, without reviewer identity,
scores, decisions, routes, or report paths. Do NOT write methods text or a
statistical analysis plan. Return route recommendations only.
```

---

## Practicing-Clinician Reviewer Brief

Use only for clinical medicine, public health practice, patient care, guideline interpretation, screening, diagnosis, treatment, or implementation in care settings.

```
## Your Role
Read as a frontline clinician. Audit clinical plausibility, endpoint relevance, practice-facing implications, and credibility.

## Allowed Files
draft-current.md, target-outlet-profile.md, clinical-evidence-subset.md if available

## Required Output
Clinical credibility assessment, endpoint relevance concerns, actionability concerns, recommendation.
STATEMENT: Would recommendation change if outlet were broader/narrower?

## Constraints
Do NOT provide clinical decision support. Evaluate article framing only.
```

---

## Narrative And Language Assessment Briefs

Dispatch both briefs concurrently to different fresh instances against the same frozen
Perspective version. They do not see each other, evaluator/panel material, or repair
history.

```
Narrative allowed project input: perspective-v{N}.md plus an embedded or file-backed reader-reasoning handoff.
Narrative route: research-narrative-assessor, profile perspective, assessment mode.

Language allowed project input: perspective-v{N}.md plus target language, discipline, declared readers, and concrete journal name if known.
Language route: academic-language-assessor, complete_artifact scope.

Required outputs: narrative assessment + YAML narrative repair plan; language assessment report.
Prohibited: writing prose, scientific judgment, other reports, evaluator material, scores, decisions, prior versions, or deltas.
```

---

## Content Preservation Brief

```
## Your Role
Fresh research-narrative-assessor in content-preservation mode. Check editorial preservation only; do not assess narrative quality or scientific correctness.

## Allowed Files (exact whitelist)
prior-perspective.md, revised-perspective.md, protected-content-register.yaml, editorial-revision-delta.yaml

## Prohibited
Repair brief, evaluator/panel/language/narrative assessment, claim ledger, skeleton, paragraph map, readiness, workflow state, or parent reasoning.

## Required Output
One content-preservation report with exactly one disposition per protected item and one contract decision.
```

---

## Medical Journal Review Brief

Use only after blind final evaluation when the Perspective is biomedical/clinical,
medical editorial review is requested, or publication probability is explicitly in
scope.

```
## Allowed Files
04_drafts/perspective-v{N}.md, verified target-outlet facts or clean candidate-journal-match-brief.yaml, optional current 08_cover-letter/cover-letter-v{M}.md

## Prohibited
Evaluator, panel, narrative/language assessment, repair brief, delta, readiness report, scores, findings, gates, and decisions.

## Required Route
Fresh medical-journal-review using its applicable editorial route; `prior_scores_visible: false`.

## Required Output
08_journal/medical-journal-review-v{N}.md. Keep any probability assessment inside that same report.
```

---

## Final Compositor Brief

```
## Your Role
Independent final compliance verifier and package compositor. Copy the latest evaluated source text byte-for-byte; find issues and return routes, but do not fix source text.

## Allowed Files
draft-final.md, claim-ledger.md, claim-evidence-matrix.md, citation-risk-log.md, contrary-evidence-log.md, evidence-limitations.md, target-outlet-profile.md, panel-summary.md, reference-list.md, 09_state/artifact-index.md, and any frozen Cover Letter, mechanical check, candidate-journal brief, or medical-journal-review report selected for the package

## Allowed Inline Receipt
A score-free qualifying-final-evaluation receipt containing the final evaluator review and instance IDs, final-evaluation report `{artifact_id, version, path}`, evaluated Perspective `{artifact_id, version, path}`, `evaluation_stage: final`, and `qualification: passed`. Omit scores, findings, gates, and narrative.

## Five Audits
1. Journal fit 2. Citation accuracy 3. Title/abstract 4. Anti-pattern final scan 5. Claim-consistency

## Required Output
08_final/final-perspective.md, optional cover-letter.md, package-manifest.md, final-edit-log.md, final-compositor-report.md, submission-readiness-report.md

## Permitted
Create package directories, copy the evaluated source and any frozen Cover Letter unchanged, compare exact text directly, and write only package copies, a package manifest, proposed canonical-index entries, edit/verification log, compositor report, and readiness report under `08_final/`. The orchestrator alone writes `09_state/artifact-index.md`. Carry any medical-review probability block unchanged. Do not calculate or persist digests.

## Prohibited
Any formatting, title, abstract, grammar, citation, heading, deduplication, terminology, claim, evidence, caveat, or prose change. If any text change is needed, return it to the owning drafter/curator, create a new version, and require fresh evaluation.

## Return Routes
unsupported claim → return_to_curator, unregistered claim → return_to_drafter, citation mismatch → return_to_curator, outlet mismatch → outlet_retarget, multiple → return_to_refinement

## Readiness
Return `packaging_pending` only if no unresolved substantive issue remains, the
packaged manuscript is text-identical to the frozen evaluated source, and all
proposed canonical-index entries are complete. The orchestrator sets
`human_signoff_required` only after registering and verifying those entries. Use
`outlet_targeting_only` rather than a sign-off route when the outlet profile is generic.
```
