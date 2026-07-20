---
schema_version: research-idea-editorial-repair-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-v051-to-v052
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v051-to-v052
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/revision-delta-v051-to-v052.md
source_artifact:
  artifact_id: idea-dossier-I01-001-v051
  version: v051
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md
target_artifact:
  artifact_id: idea-dossier-I01-001-v052
  version: v052
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/idea-dossier-v052.md
based_on:
  - artifact_id: editorial-repair-writer-brief-I01-001-r110
    version: r110
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/editorial-repair-writer-brief-r110.yaml
  - artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
source_skill: multi-path-idea-generator
created_round: 110
change_type: editorial_repair_delta
frozen: true
---

# Revision delta: v051 to v052

## Scope and result

This was one bounded editorial repair of the complete dossier. It implemented only
`LANG-R108-001` through `LANG-R108-004`. The 14 omitted minor items in the writer
brief were not converted into a second repair list. The study identity, scientific
claims, methods, feasibility findings, evidence status, conditionality, numerical
rules, and protected content remain unchanged.

The complete target dossier was finished, checked, linted, and frozen before this
delta was created. No later dossier edit was made.

## Included repair actions

| Repair item | Operation | Revised locator and text-grounded result | Acceptance-test result |
|---|---|---|---|
| `LANG-R108-001` | Define and replace | `Structured abstract > Objective and hypothesis` (line 45) defines the common physiological anchors as measured physiological variables that pass unit, measurement-semantics, timestamp, and visibility audits in both intensive-care databases; the same sentence distinguishes anchor observations from anchor predictions. Subsequent variable, observed-value, and predicted-value uses are separated in the resource audit, Methods, trial mapping, implementation table, evidence chains, required analyses, falsification criteria, and section 14. | Every reader-facing occurrence containing “锚点” was reopened. Variable uses are named “共同生理锚点变量” (or the fully defined term), measured values are “锚点观测值,” and model outputs are “锚点预测值.” The former competing forms “观测锚点” and “实测锚点” are absent. All qualification rules, observation equations, loadings, scales, coverage criteria, and trial-mapping thresholds remain in place. |
| `LANG-R108-002` | Replace | `Structured abstract > Expected result` (line 47) first names the two secondary representation diagnostics as the pseudo-masking reconstruction diagnostic on originally measured physiological values and the future-trajectory prediction diagnostic. `Objectives > Objective 3` (line 82) applies the same names in the single combined edit; the work-package row, protocol lock, diagnostic authority, evidence chain, required analyses, planned outputs, contribution ladder, and feasibility section use the stable names. | The two diagnostics remain distinct and secondary. “表示诊断,” “部分状态重建,” and “未来轨迹诊断” are absent. The pseudo-masking diagnostic still acts only on originally measured physiological values; its metrics, the future-trajectory metrics, stratified reporting, and inability to alter primary-task or stage-II decisions are unchanged. |
| `LANG-R108-003` | Define and replace | `Research content and work packages > 24 个月最低交付与时间节点` (line 97) defines proper scoring rules and identifies Brier or multicategory Brier scores as the planned instances. The analysis-freeze milestone, WP3, required analyses, and external falsification criterion use “恰当评分规则” or the already specified Brier metric. | The undefined phrase “适当评分” is absent. All Brier non-inferiority bounds, calibration slope and intercept or absolute-risk-error criteria, confidence bounds, and final-test authorization rules are unchanged. |
| `LANG-R108-004` | Replace | `Objectives > Objective 3` (line 82) distinguishes checking whether a zero-edge mechanism produces spurious structure from checking whether model misspecification still yields an erroneous high-confidence structural conclusion. The recovery milestone, absolute-recovery table (lines 242–243), implementation table, evidence chain, required analyses, and falsification criteria use the corresponding stable names. | The two check objects remain independent. The unqualified “假置信检查” form is absent. The spurious-edge proportion, misspecification-identification proportion, erroneous high-confidence proportion, complex-candidate rejection, and no-post-hoc-threshold-change rules are unchanged. |

`Objective 3` was edited once to satisfy `LANG-R108-002` and `LANG-R108-004`
together: absolute recovery, the two distinct structural checks, and the two named
secondary representation diagnostics remain separate scientific roles.

## Identity and scientific-role concordance

### Frozen identity anchor

All five values were copied verbatim:

- `primary_research_question`: "can a knowledge-constrained, uncertainty-aware dynamic system representation of ICU patients cover the sepsis-centered pre-onset, onset, post-onset, and outcome continuum, demonstrate cross-database state/structure validity, and then test limited randomized intervention perturbations without conflating prediction with causality?"
- `primary_objective`: "construct and validate the sepsis complex-system model, with stage II completed within 24 months."
- `study_object`: "the longitudinal sepsis-centered ICU patient system, including comparable at-risk non-onset intervals and post-onset trajectories."
- `core_data_or_evidence_base`: "literature/expert priors; longitudinal public ICU data; conditionally available EXIT-SEP and XBJ-SCAP individual-level RCT data."
- `primary_unit_of_inference`: "patient-time state and state transition, with patient and hospital clustering respected."

### Central scientific content

| Role | Preserved reader-facing content | Locator |
|---|---|---|
| Central study object | The longitudinal, sepsis-centred intensive-care patient system, including comparable at-risk non-onset intervals and post-onset trajectories | `Research design and methods > Observational target, anchoring, and evidence-qualified interpretation` (line 226) |
| Primary question | Whether the knowledge-constrained, uncertainty-aware candidate dynamic-system representation can cover the pre-onset, first-onset, post-onset, and outcome continuum and support hospital- and database-level testing without conflating prediction, observational representation, and causality | `Research question, objectives, and core hypothesis > Primary research question` (line 76) |
| Primary clinical outcomes | Future 12-hour first-onset cumulative incidence and day-7 favourable-state occupancy | `Research design and methods > Protocol locks for the two primary clinical tasks` (lines 193–207) |
| Contribution | Conditional evidence integration, planned cross-database validation, a reusable benchmark or research resource, and falsifiable analytical governance; no new-algorithm claim | `Title, summary, audience, and positioning` (lines 37–40) and `Contribution and evidence ladder` (lines 402–412) |

### Four repaired scientific roles

| Scientific role | Unique reader-facing name(s) | First occurrence | Competing-form disposition and whole-dossier scan |
|---|---|---|---|
| Physiological anchor roles | `共同生理锚点变量`; `锚点观测值`; `锚点预测值` | Complete three-role definition at line 45 | `观测锚点`, `实测锚点`, and bare `锚点预测` were removed. Every remaining occurrence identifies a variable, measured value, or model output. |
| Secondary representation diagnostics | `伪遮蔽重建诊断`; `未来轨迹预测诊断` | Both named at line 47 | `表示诊断`, `部分状态重建`, and `未来轨迹诊断` were removed. The two stable names occur in the abstract, Objective 3, WP3, diagnostic authority, and evidence chain. |
| Primary-task probabilistic evaluation | `恰当评分规则（proper scoring rules）`; `Brier 分数`; `多类别 Brier 分数` | Definition and planned instances at line 97 | `适当评分` was removed. Later decision points use the standard term or an already specified Brier metric. |
| Structural simulation checks | `零边机制下的虚假结构检查`; `模型错设下错误高置信结构结论的检查` | Objects stated directly in Objective 3 at line 82 | The subjectless `假置信检查` family was removed. The two objects remain separate in the recovery table, implementation, evidence chain, required analyses, and falsification criteria. |

## Protected-content dispositions

| Protected ID | Disposition | Revised locator(s) and item-level preservation evidence |
|---|---|---|
| `PCR-001` | `retained_same_meaning` | Frontmatter `identity_anchor`; `Primary research question` (line 76); `Observational target, anchoring, and evidence-qualified interpretation` (line 226). The sepsis-centred pre-onset, first-onset, post-onset, and outcome continuum remains the study identity, not generic intensive-care risk prediction. |
| `PCR-002` | `retained_same_meaning` | Frontmatter `primary_objective`; structured objective (line 45); Objectives and delivery direction (lines 80–85); 24-month milestones and work packages (lines 93–130). Stage I–II remains due within 24 months, the work still uses literature/expert constraints and public intensive-care data for system identification and cross-database testing, and the deliverable remains high-level papers plus auditable scientific evidence rather than only a prediction tool. |
| `PCR-003` | `retained_same_meaning` | Frontmatter `study_object` and `primary_unit_of_inference`; Methods observational target (line 226). The object remains the longitudinal sepsis-centred intensive-care system with comparable at-risk non-onset intervals and post-onset trajectories; inference remains at patient-time states and transitions with patient and hospital clustering. |
| `PCR-004` | `retained_same_status` | `Current resource and result status` (lines 134–147) and `Public intensive-care database roles and support audit` (lines 149–173). Literature/expert priors, MIMIC-IV, eICU-CRD, and the prespecified HiRID or AmsterdamUMCdb backup remain; database existence/version is verified, while access, agreements, executable extraction, project support, named personnel, and model results remain unverified or ungenerated. |
| `PCR-005` | `retained_same_status` | Trial-resource rows (lines 141–143) and `Local randomized-trial evidence status` (lines 185–187). EXIT-SEP and XBJ-SCAP remain only conditional individual-level sources; derived reports still do not substitute for authorization, original forms or analysis plans, randomization, centre, visit timing, or survival/hospital semantics. |
| `PCR-006` | `retained_same_meaning_at_method_authority` | Minimum route (line 130) and Methods authorities (lines 193–296). Audit, protocol locks, simple baselines, absolute recovery, at most one complex candidate, two primary tasks, two secondary diagnostics, development freeze, untouched external testing, and only then conditional trial analysis remain in order. State, treatment, and measurement processes remain separate. The 90%, 80%, 80%, 0.70, and interval-calibration rules and their delete, merge, or database/care-policy-specific consequences remain unchanged. |
| `PCR-007` | `retained_same_meaning_at_method_authority` | `Conjunctive minimum success definition` (lines 108–118) and `Hospital-primary cross-database validation` (lines 248–267). Data support, absolute recovery, proper-score and calibration performance for both primary tasks, leakage clearance, zero-update untouched external performance, alignment, and structural stability remain conjunctive. Limited adaptation remains separate and cannot rescue zero-update failure; stage III cannot complete stage II. |
| `PCR-008` | `retained_same_meaning_at_method_authority` | `Protocol locks for the two primary clinical tasks` (lines 193–209) and `Mutually exclusive post-onset state and event system` (lines 211–220). Both tasks, event/availability clocks, infection pairing windows, SOFA baseline and rolling-window rules, first sortable onset, first-onset analysis, delayed entry, total overlapping-landmark weight of one, mutually exclusive states, competing termination, as-of features, calibration and Brier targets, clustering, within-window ordering, unsortable-edge exclusion, and leakage checks remain unchanged. |
| `PCR-009` | `retained_same_strength` | Structured abstract (lines 44–48), resource status (line 146), and `Contribution and evidence ladder` plus closest-work comparison (lines 402–424). The dossier still describes planned work with no existing model, recovery, external-validation, or new trial-analysis result. Contribution remains conditional integration, validation, benchmark, or resource value; modules have precedents and the complete-combination gap remains low-to-moderate confidence, with no global-first or new-algorithm claim. |
| `PCR-010` | `retained_once_at_respective_authority_locations` | Methods decision authorities (lines 193–296), falsification and interpretation authorities (lines 377–398), and section 14 (lines 438–475). Section 14 retains the complete access, team, support, label/leakage, recoverability, nonrandom-missingness, overlap, external-validation, timing, trial-semantic, anchor-mapping, and closest-work limitations, plus the two unresolved specifications. Methods alone retains eligibility and mutually exclusive branch logic; section 11 alone retains result-dependent falsification and interpretation. |
| `PCR-011` | `retained_once_at_respective_authority_locations` | 24-month milestones and WP5 (lines 93–130); stage-III Methods authority (lines 269–292); section-14 timing, trial, and mapping limitations and operational risks (lines 458–475). Stage III remains outside minimum delivery and requires stage-II success, usable individual data, and verified core semantics. The mapping and independent branches remain parallel after the common prerequisites; core-semantic failure still stops new visit-outcome analysis, and later trial results cannot rescue stage II. |
| `PCR-012` | `retained_once_at_section_14_authority` | `Core hypothesis and evidence boundary` (lines 87–89), interpretation matrix (lines 388–398), and the complete prohibited-claims authority in section 14 (line 465). Observational evidence and prediction still do not support causal networks, treatment effects, counterfactual policy, mechanism, mediation, control, or digital-twin claims; conditional trial analyses still cannot validate unmeasured dynamics, transition edges, or the entire system, and the plan is not an already validated model, decision tool, drug platform, or unconditional clinical basis. |

## Whole-dossier mechanical checks

- The five `identity_anchor` values are byte-for-byte textually identical between
  the two frontmatters.
- The body contains the same ordered sequence of 702 numeric tokens in v051 and
  v052.
- Both versions contain 15 H2 sections and 137 table rows.
- The complete References section is textually identical.
- The 15 required H2 sections, the five ordered H3 reader-chain functions,
  evidence chains, claim-support table, section-14 authorities, and frozen target
  metadata are present.

## Required command records

### Structural linter

Command (run exactly):

```text
python -B research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py --expected-plugin-version 0.9.0-preview.3 tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/idea-dossier-v052.md
```

Exit result: `0` (`PASS`). The linter emitted one advisory at line 45 covering
the defining phrases for `锚点观测值` and `锚点预测值`, followed by `OK` for the
target path. Disposition: both are standard scientific-role terms defined in the
same sentence; `standard_and_defined`.

### Reader-facing short-form advisory diff

Command (run exactly, read-only):

```text
python -B research-skills-openai/skills/academic-language-assessor/scripts/diff_reader_facing_short_forms.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/idea-dossier-v052.md
```

Exit result: `0` (`PASS`). Complete output:

```text
[new-reader-facing-short-form]
explicit-label	锚点观测值	45,102,140,168,279,289
explicit-label	锚点预测值	45,89,226,228,305
```

### Candidate dispositions

| Candidate | All returned revised locations | Semantic basis | Disposition |
|---|---|---|---|
| `锚点观测值` | Lines 45, 102, 140, 168, 279, 289 | Line 45 defines this as an actually measured value of a common physiological anchor variable. Lines 102, 140, and 168 concern observed-value density; line 279 applies the physiological-range check to observed values; line 289 concerns observed values required to calculate the proxy. | `standard_and_defined` |
| `锚点预测值` | Lines 45, 89, 226, 228, 305 | Line 45 defines this as the model output for a common physiological anchor variable. The remaining occurrences consistently denote that model output in the core hypothesis, observational target, recoverable-invariant definition, and implementation record. | `standard_and_defined` |

No other candidate was returned.

## Handoff boundary

The frozen v052 dossier and this delta are ready only for an independent
content-preservation review followed by fresh narrative and language reassessment.
This editorial repair does not itself establish editorial readiness or scientific
evaluation.
