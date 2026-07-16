# Delegate Brief Templates

## Contents

<!-- toc:start -->
- [Evaluator Brief](#evaluator-brief)
- [Counter-Position Reviewer Brief](#counter-position-reviewer-brief)
- [Evidence Reviewer Brief](#evidence-reviewer-brief)
- [Narrative Reviewer Brief](#narrative-reviewer-brief)
- [Methodology / Statistics Reviewer Brief](#methodology-statistics-reviewer-brief)
- [Practicing-Clinician Reviewer Brief](#practicing-clinician-reviewer-brief)
- [Outlet-Fit Editor Reviewer Brief](#outlet-fit-editor-reviewer-brief)
- [Final Compositor Brief](#final-compositor-brief)
<!-- toc:end -->

本文件包含 orchestrator 派发所有 delegate 子 agent 时使用的 brief 模板。

Every evaluator, reviewer, assessor, and final verifier brief must identify the reviewer skill/role, reviewer instance ID, workflow/round IDs, frozen artifact IDs/exact paths/versions, allowed and prohibited files, review scope, and output path. Run each brief in a fresh independent subagent/delegated thread. If that is unavailable, return `independent_review_pending` with the completed brief and stop; never run inline.

Every completed review artifact must report `files_read`, `review_scope`, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, and `source_edits_performed: false`. Fresh re-evaluation must not receive prior scores or prior decisions. Panel reviewers must not receive evaluator reports or other reviewer outputs.

---

## Evaluator Brief

```
## Your Role
Independent evaluator. Evaluate the Perspective draft against an eight-dimension rubric. Do NOT revise, rewrite, or broaden scope.

## Allowed Files (whitelist)
- input-brief.md / argument-skeleton.md / perspective-v{N}.md / perspective-v{N}-paragraph-map.md / claim-ledger.md / claim-evidence-matrix.md / target-outlet-profile.md / existing-discourse-baseline.md

## Procedure
1. FIRST PASS: Read draft alone. Score Thesis Clarity, Narrative Coherence, Stance Calibration, Contribution Sufficiency, Audience Fit, Novelty. Do NOT consult paragraph-map.
2. SECOND PASS: Read paragraph-map. Score Argument Integrity, Evidence-Claim Match.
3. ANTI-PATTERN: Scan all 10 patterns.
4. SYNTHESIZE + decision.

## Required Output
evaluation-report-v{N}.md: eight scores with paragraph references, hard gate status, anti-pattern findings, fatal flaws, decision.

## Constraints
Do NOT revise. Cite specific paragraph numbers. If discourse baseline missing, mark Novelty provisional. For re-evaluation, read only the latest frozen draft, stable rubric, necessary facts, and an optional anonymous must-fix list; do not provide a prior draft, revision delta, prior score, or decision.
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

## Narrative Reviewer Brief

```
## Your Role
Read as real reader. NO skeleton provided — judge only what is on the page.

## Allowed Files
draft-current.md, target-outlet-profile.md

## Required Output
Narrative coherence (1-5), anti-pattern findings. "Does reader emerge with changed understanding?"
STATEMENT: Would recommendation change if outlet were broader/narrower?

## Constraints
Do NOT infer author intent from missing files. Judge only ON THE PAGE.
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

## Outlet-Fit Editor Reviewer Brief

Use only when a concrete target journal, outlet, article type, or commissioned format is specified.

```
## Your Role
Read as an editor for the target outlet. Audit genre fit, audience fit, stance strength, structure, title/abstract fit, and likely editor objections.

## Allowed Files
draft-current.md, target-outlet-profile.md, title-abstract.md if separate

## Required Output
Outlet-fit assessment, likely desk-reject risks, required fit changes, recommendation.
STATEMENT: Would recommendation change if outlet were broader/narrower?

## Constraints
Do NOT rewrite title, abstract, or manuscript. Return route recommendations only.
```

---

## Final Compositor Brief

```
## Your Role
Independent final compliance verifier and package compositor. Copy the latest evaluated source text byte-for-byte; find issues and return routes, but do not fix source text.

## Allowed Files
draft-final.md, claim-ledger.md, claim-evidence-matrix.md, citation-risk-log.md, contrary-evidence-log.md, evidence-limitations.md, target-outlet-profile.md, panel-summary.md, reference-list.md, and any frozen Cover Letter, mechanical check, or medical-journal-review report selected for the package

## Five Audits
1. Journal fit 2. Citation accuracy 3. Title/abstract 4. Anti-pattern final scan 5. Claim-consistency

## Required Output
08_final/final-perspective.md, optional cover-letter.md, final-edit-log.md, final-compositor-report.md, submission-readiness-report.md

## Permitted
Create package directories, copy the evaluated source and any frozen Cover Letter unchanged, calculate digests, and write only package copies, manifest/index, edit/verification log, compositor report, and readiness report. Carry any medical-review probability block unchanged.

## Prohibited
Any formatting, title, abstract, grammar, citation, heading, deduplication, terminology, claim, evidence, caveat, or prose change. If any text change is needed, return it to the owning drafter/curator, create a new version, and require fresh evaluation.

## Return Routes
unsupported claim → return_to_curator, unregistered claim → return_to_drafter, citation mismatch → return_to_curator, outlet mismatch → outlet_retarget, multiple → return_to_refinement

## Readiness
"ready for human review and sign-off" only if NO unresolved substantive issues. "ready for outlet targeting" if Generic Profile.
The packaged manuscript digest must equal the frozen evaluated source digest.
```
