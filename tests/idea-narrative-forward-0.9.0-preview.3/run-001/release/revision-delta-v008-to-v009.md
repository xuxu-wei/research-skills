---
artifact_id: revision-delta-I01-001-v008-to-v009
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
from_artifact_id: idea-dossier-I01-001-v008
from_version: v008
to_artifact_id: idea-dossier-I01-001-v009
to_version: v009
change_type: editorial_repair
---

# Revision delta: v008 to v009

## Scope and lineage

This delta records one concentrated editorial-only revision of `idea-dossier-I01-001-v008`. The revised dossier is based only on:

- `idea-dossier-I01-001-v008` / `v008` / `tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/idea-dossier-v008.md`
- `narrative-repair-plan-I01-001-r007` / `r007` / `tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/narrative-repair-plan-r007.yaml`
- `language-assessment-I01-001-r007` / `r007` / `tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/language-assessment-r007.md`
- `protected-content-register-I01-001-v008` / `v008` / `tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/protected-content-register-v008.yaml`

No evidence, method, result, threshold, feasibility claim, or new scientific object was added.

## Narrative-plan actions

### NRP-001 / NAR-001 — define the three-stage map

- **Location:** “Title, summary, audience, and positioning”; “Twenty-four-month minimum deliverable and dated milestones”.
- **Operation:** Added a compact three-stage map before the one-sentence summary. It maps stage I to months 0–6 and WP1, stage II to months 3–24 and WP2–WP4, and stage III to post-month-24 WP5. The month 3–6 overlap is stated only to make the existing WP2 schedule explicit.
- **Retained:** The 24-month minimum-deliverable boundary; all existing months; WP1–WP5 content; the fixed execution order; the five required stage II evidence classes; all trial-eligibility checks; the rule that stage III cannot compensate for a stage II failure.
- **Deleted or moved:** No stage, month, work package, condition, threshold, or stop consequence was deleted. A repeated stage-II/stage-III clause in the one-sentence summary was compressed after the full map was placed immediately above it.
- **Scientific meaning changed:** No.
- **Protected-content disposition:** PCR-V008-001 retained with the same identity and question; PCR-V008-004 retained with the same design sequence and stage dependencies; PCR-V008-006 retained at the authoritative section 14 location without weakening any condition.
- **Unexecuted portion:** None.

### NRP-002 / NAR-002 — split the top concept bridge and relocate technical definitions

- **Location:** “Title, summary, audience, and positioning”; “Structured abstract”; “Background, current state, gap, significance, and rationale”; “Research design and methods > Observational model target, anchoring, and reporting”.
- **Operation:** Reduced the top concept bridge to ordinary-language orientation: the candidate dynamic model, separation of physiological state from treatment action and measurement process, and the distinction between state-occupancy probability and observed state proportion. Kept the four evidence classes at the top and stated that they do not substitute for one another. Added short explanations at the first abstract or gap use of physiological-anchor prediction, state alignment, relation sign and lag, and the observation equation. Moved the full operational definitions to immediately before the observational-model formula and anchoring rules.
- **Retained:** The distinction between state-occupancy probability and observed proportion; the relation among common observations, common physiological anchors, and anchor predictions; allowed latent-dimension permutations and sign transformations for state alignment; the observation equation as the source of the frozen stage III mapping; the distinction among relation sign, lag, and edge direction; the collective “pre-specified state and structure objects” definition; the four non-interchangeable evidence classes.
- **Deleted or moved:** The dense technical-definition chain was removed from the top concept bridge and moved intact, with shorter sentences, to the observational-model section. No protected distinction was deleted.
- **Scientific meaning changed:** No.
- **Protected-content disposition:** PCR-V008-002 retained with the same study object and inference unit; PCR-V008-004 retained with the same model and validation objects; PCR-V008-006 retained with the same stage III dependency; PCR-V008-007 retained with the same causal and mechanistic boundaries.
- **Unexecuted portion:** None.

## Language findings

### LANG-001 — opaque “pseudo-masking reconstruction” label

- **Location:** WP3; “Secondary representation diagnostics”; corresponding evidence chain.
- **Operation:** Replaced the short label with “遮蔽后重建检验” and defined it at first occurrence as artificially hiding part of the observed values and evaluating reconstruction error and interval coverage. Later mentions use the same direct label.
- **Retained:** The masked values, reconstructed values, error metrics, interval coverage, stratification, and separation from the two primary clinical tasks.
- **Deleted or moved:** The opaque term “伪遮蔽” was removed; no diagnostic content was removed.
- **Scientific meaning changed:** No.
- **Protected-content disposition:** PCR-V008-004 retained with the same diagnostic operation and evaluation targets.
- **Unexecuted portion:** None.

### LANG-002 — undefined “failure figure”

- **Location:** Month 21–24 milestone.
- **Operation:** Replaced “失败图” with a descriptive name: a database- and hospital-stratified distribution plot of items that do not meet pre-specified stage II standards.
- **Retained:** The same pre-specified standards, database and hospital validation context, clustering uncertainty, state alignment, and milestone decision.
- **Deleted or moved:** Only the project-internal short label was removed.
- **Scientific meaning changed:** No.
- **Protected-content disposition:** PCR-V008-004 retained; no criterion or consequence changed.
- **Unexecuted portion:** None.

### LANG-003 — ambiguous uses of “support”

- **Location:** Structured abstract; objective 2; WP3; dual-database audit and audit table; cross-database evidence chain; section 14 operational thresholds.
- **Operation:** Replaced ambiguous compounds with their observable objects: variable coverage, sample and event sufficiency, allowed-transition counts, treatment-action coverage and overlap, and external sample/event/transition/hospital coverage. The dual-database audit now lists the quantities it checks.
- **Retained:** All existing audit objects, coverage requirements, event and transition requirements, treatment-action overlap checks, and operational thresholds.
- **Deleted or moved:** The ambiguous word stem “支持度” was removed from reader-facing uses; no audit item was deleted.
- **Scientific meaning changed:** No.
- **Protected-content disposition:** PCR-V008-003 retained with the same data status; PCR-V008-004 retained with the same audit and model-admission role.
- **Unexecuted portion:** None.

### LANG-004 — “structural consistency” versus “structural stability”

- **Location:** Structured abstract and later core-design sections.
- **Operation:** Unified the same cross-database evaluation object under “预设结构稳定性” and defined it as cross-database retention of the signs and time lags of pre-specified relations.
- **Retained:** The relation-sign and time-lag objects, all comparison thresholds, state-alignment criteria, and the distinction from edge direction.
- **Deleted or moved:** The isolated synonym “结构一致性” was removed. Other uses of “一致” that denote matching rates or coefficients were retained because they are different metrics.
- **Scientific meaning changed:** No.
- **Protected-content disposition:** PCR-V008-004 retained with identical structural targets and thresholds.
- **Unexecuted portion:** None.

### LANG-005 — three local syntax problems

- **Location:** Background; external projection fidelity assessment; trial-analysis table.
- **Operation:** Reordered the Sepsis-3 definition sentence to make the host-response relation explicit; changed “相关” to “相关系数” both in the method description and corresponding threshold; separated EXIT-SEP target population from estimand and visit information.
- **Retained:** The Sepsis-3 scientific definition, the same correlation threshold, all trial populations, estimands, visits, and analysis rules.
- **Deleted or moved:** No scientific content was deleted; the EXIT-SEP estimand phrase moved to its own table column.
- **Scientific meaning changed:** No.
- **Protected-content disposition:** PCR-V008-004 retained, including estimands and numerical thresholds.
- **Unexecuted portion:** None.

### LANG-006 — English status labels in a Chinese reader table

- **Location:** “Title and positioning claim-support table”.
- **Operation:** Replaced row-level English labels with “获得支持” and “限定支持”. The legend preserves each fixed English value once in parentheses. “none” is displayed as “无可主张增量”.
- **Retained:** All status meanings, bounded claims, evidence links, claim strength, and the mapping to `supported`, `qualified`, and `none`.
- **Deleted or moved:** Repeated English labels were removed from reader-facing cells; fixed values and their semantics were not altered.
- **Scientific meaning changed:** No.
- **Protected-content disposition:** PCR-V008-005 retained with the same claim strength and evidence status.
- **Unexecuted portion:** None; no machine frontmatter field or fixed dossier schema value was changed for this language edit.

### LANG-007 — dense definition paragraph and trial table

- **Location:** Top concept bridge; trial-analysis table.
- **Operation:** The concept bridge was split and technical definitions were moved as recorded under NRP-002. The trial table was divided into parallel columns for population/analysis set, estimand/visit, outcome ordering/missingness/inference, and multiplicity/subgroups. Both trial rows now follow the same information order.
- **Retained:** Every named population, analysis-set fallback, visit, baseline restriction, death/discharge ordering, imputation and sensitivity rule, structurally absent variable rule, Holm family, exploratory error control, and subgroup-interaction rule.
- **Deleted or moved:** Content was redistributed across columns; no trial-analysis content was deleted.
- **Scientific meaning changed:** No.
- **Protected-content disposition:** PCR-V008-003 retained with the same trial-data availability; PCR-V008-004 retained with the same estimands and analysis rules.
- **Unexecuted portion:** None; the Markdown table layout is reader-facing and not a fixed machine schema.

### LANG-008 — repeated stage III qualification language

- **Location:** Top summary and rationale, with cross-section checks of the abstract, objectives, milestones, trial methods, and section 14.
- **Operation:** Compressed only adjacent or locally redundant phrases after adding the explicit three-stage map. In the rationale, “stage II completed” was replaced by a sequential bridge. Distinct statements that perform scientific or governance functions remain in their sections.
- **Retained:** The full top-level entry rule; the abstract’s trial-specific qualification; objective 4; dated milestones and WP5; trial-semantics checks; required-analysis registration; and the complete authoritative stage III limitation and stop consequences in section 14.
- **Deleted or moved:** Only non-substantive repeated wording was removed; no condition was deleted.
- **Scientific meaning changed:** No.
- **Protected-content disposition:** PCR-V008-006 retained once in full at the authoritative section 14 location and restated only where a distinct section function requires it.
- **Unexecuted portion:** No scientific condition was removed merely for concision.

## Protected-content summary

| Protected item | v009 disposition |
|---|---|
| PCR-V008-001 | Retained with the same research identity, full-disease-course question, and 24-month stage I–II objective. |
| PCR-V008-002 | Retained with the same longitudinal ICU system, patient-time state and transition units, and patient/hospital clustering. |
| PCR-V008-003 | Retained with the same evidence sources, availability, authorization, semantics, and result status. |
| PCR-V008-004 | Retained with the same staged sequence, tasks, estimands, thresholds, recovery tests, validation design, and falsification criteria. |
| PCR-V008-005 | Retained with the same planned-work status and claim strength. |
| PCR-V008-006 | Retained in full at section 14 as the sole authoritative location for limitations, assumptions, interpretation boundaries, alternatives, and stop conditions. |
| PCR-V008-007 | Retained with the same prohibitions on causal, mechanistic, control, digital-twin, and unconditional clinical claims. |

## Structural preservation and unresolved items

- Preserved `research-idea.v3`, all 15 H2 headings, all five non-empty H3 subsections under the third H2, all evidence-chain sections, and the claim-support table.
- The core question, study object, data, stage dependencies, claim strength, limitations, stop conditions, numerical thresholds, and feasibility status are unchanged.
- No narrative-plan action or language finding with an explicit editorial direction remains unexecuted.
- No readiness judgment is made in this delta.

