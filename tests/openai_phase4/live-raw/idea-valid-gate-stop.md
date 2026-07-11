## PI-review portfolio

Workflow `RID-K57-20260712-01` produced one versioned candidate after a genuine independent critique-and-revision cycle. The candidate passed fresh independent evaluation, but the adversarial panel did not reach consensus. Methodology and PI-strategy reviewers identified blocking specification issues; therefore the candidate is appropriate for PI review but is **not yet ready for proposal drafting or proposal-orchestrator handoff**.

### 1. Context and evidence-limitation record

**Purpose:** Establish an internal operational baseline for follow-up after mild outpatient hyperkalemia.

**Available data:** Enterprise laboratory warehouse, 2019–2025; approximately 1.2 million adult outpatient potassium results from 14 clinics; 45,380 eligible episodes before dialysis and transplant exclusions. Required cohort fields are at least 99.5% complete, units are normalized, and dialysis/transplant status is available at index.

**Permitted claims:**

- Proportions and timing of **network-captured** repeat testing.
- Descriptive annual and clinic-level variation.
- Internal operational value and whether further workflow-design discussion is justified.

**Prohibited claims:**

- Absence of captured testing means no testing occurred.
- Clinic differences represent performance or quality differences.
- Causal effects of clinic workflows.
- Normalization among repeated episodes generalizes to all eligible episodes.
- External novelty, publication priority, or guideline alignment.

**Evidence status:** User-supplied internal data audit only. No browsing or external novelty verification was performed. External novelty and guideline alignment remain `unverified`.

### 2. Candidate

**ID:** `I01-001-R01@v002`
**Parent:** `I01-001@v001`
**Title:** *Seven-day network-captured follow-up after first mild outpatient hyperkalemia: a 2019–2025 internal baseline*

**Research question:** Among adults with an eligible first non-hemolyzed outpatient potassium result of 5.5–5.9 mmol/L, what proportion has a potassium collection captured in the network strictly after index through 168 hours inclusive; how quickly is the first repeat captured; and, among episodes with a captured repeat, what proportion has a first repeat below 5.5 mmol/L?

**Cohort and analysis:**

- Adults aged at least 18 at collection.
- No eligible index result during the preceding 90 days.
- Exclude maintenance dialysis and prior kidney transplant at index.
- Collapse same-timestamp aliquots using the maximum reported potassium.
- Primary endpoint: any network-captured repeat potassium in `(index, index + 168 hours]`.
- Secondary endpoints:
  - Hours to first captured repeat.
  - First repeat below 5.5 mmol/L among captured-repeat episodes, with that conditional denominator displayed prominently.
  - Internally captured ED visit or admission within seven days, descriptively.
- Report overall and index-calendar-year estimates with Wilson 95% confidence intervals.
- Report clinic-specific primary rates only for clinics with at least 200 eligible episodes; pool smaller clinics.
- No adjustment, ranking, performance attribution, or causal interpretation.
- Use complete cases and report exclusions and missing counts explicitly.

**Value claim:** A reproducible internal baseline can determine whether captured follow-up is sufficiently incomplete or variable to warrant a separate PI decision about targeted workflow design. The study itself does not design or evaluate an intervention.

### 3. Methodology/statistics preflight

The independent preflight judged the concept feasible in broad terms but not fully implementation-ready. Its principal unresolved areas were:

- Exact episode/unit-of-analysis implementation.
- Ordered exclusion and missingness accounting.
- Repeat-result validity, duplicate, corrected-result, and simultaneous-result handling.
- Follow-up observability and internal-capture interpretation.
- Clinic and calendar-year attribution.
- Secondary-outcome denominators and summaries.
- ED/admission linkage rules.
- Potential within-person clustering if multiple episodes per adult are allowed.

Some requested details exceed the frozen supplied facts. They were therefore not invented.

### 4. Independent critique and revision

Round 1 evaluator `/root/evaluator_r1` scored the original candidate:

| Dimension | Score |
|---|---:|
| Novelty | 2 |
| Feasibility | 5 |
| Impact | 3 |
| Relevance | 4 |
| Clarity | 5 |
| Completion | 4 |
| Mean | 3.83 |

All hard gates passed. Nevertheless, a fresh writer—shown only anonymized actionable findings—created `I01-001-R01@v002`. The revision:

- Standardized “network-captured repeat” terminology.
- Separated the captured-repeat normalization denominator from the full cohort.
- Strengthened the descriptive, unadjusted, non-ranking clinic language.
- Made possible differential outside-network ascertainment by clinic and year explicit.
- Limited novelty and value claims to internal operations.

The first Round 2 evaluation was invalid because it substituted a noncanonical scoring dimension for required `impact`. It was retained in the audit trail but not used.

A new blind evaluator, `/root/evaluator_r2_retry`, assessed the revised candidate:

| Dimension | Score |
|---|---:|
| Novelty | 2 |
| Feasibility | 4 |
| Impact | 3 |
| Relevance | 4 |
| Clarity | 4 |
| Completion | 4 |
| Mean | 3.50 |

All hard gates passed; no fatal flaw was found. Recommendation: `promote`, limited to an internal operational analysis.

### 5. Mutually blind adversarial panel

Actual dissent is preserved:

- **Novelty/gap skeptic:** Conditional continuation is defensible only as a local operational baseline. Any external novelty, clinical-gap, or guideline claim would be blocking. The reviewer also warned that this could remain a routine descriptive audit.

- **Feasibility/method skeptic:** `blocked`. Requested locked operational definitions for episode construction, qualifying repeats, corrected or hemolyzed repeats, authoritative timestamps, encounter linkage, registry timing, complete-case denominators, clinic threshold application, clustering, and calendar-year assignment.

- **PI-strategy reviewer:** `blocked`. Found that the PI-facing decision rule is unspecified: the portfolio does not predeclare what pattern of overall or clinic variation would justify workflow-design work, or what result would terminate that rationale. The reviewer also regarded differential outside-network capture as strategically important.

The evaluator’s promotion decision remains valid as an evaluation result, but it does not override later blocking panel findings.

### 6. PI decision requested

**Portfolio status:** `blocked_pending_PI_review`
**Proposal handoff:** `not_ready`

Before proposal handoff, the PI should determine:

1. Whether this is strictly an internal measurement project, with no external novelty claim.
2. The precise operational definitions that can be supported by the warehouse.
3. Whether multiple eligible episodes per adult are allowed and how dependence will be handled.
4. The decision rule for concluding that targeted workflow design is justified.
5. The stop rule for concluding that the baseline does not justify further workflow work.
6. Whether uncertainty from outside-network testing makes clinic-targeted interpretation unacceptable.

No proposal was drafted and no external submission or handoff occurred.

```yaml
receipt:
  workflow_id: RID-K57-20260712-01
  registry_state: blocked
  final_artifact: portfolio-package-001@v001
  current_candidate: I01-001-R01@v002
  lineage:
    - I01-001@v001
    - I01-001-R01@v002
  event_order:
    - "01 initialize workflow"
    - "02 read orchestrator skill and conditional references"
    - "03 initial dispatch failed before instance creation"
    - "04 create context-001@v001, evidence-001@v001, I01-001@v001"
    - "05 independent methods preflight"
    - "06 independent evaluation R001"
    - "07 blind targeted revision to v002"
    - "08 invalid R002 evaluation retained but excluded"
    - "09 fresh blind re-evaluation R002B"
    - "10 three mutually blind adversarial reviews"
    - "11 portfolio assembly"
    - "12 stop at PI review"
  instances:
    initial_writer:
      actual_id: /root/initial_writer
      canonical_task_id: /root/initial_writer
    preflight:
      actual_id: /root/preflight_r1
      canonical_task_id: /root/preflight_r1
      fresh: true
      prior_scores_visible: false
    evaluator_round_1:
      actual_id: /root/evaluator_r1
      canonical_task_id: /root/evaluator_r1
      fresh: true
      prior_scores_visible: false
    revision_writer:
      actual_id: /root/revision_writer_r2
      canonical_task_id: /root/revision_writer_r2
      evaluator_identity_visible: false
      evaluator_scores_visible: false
      actionable_findings_only: true
    evaluator_round_2_invalid:
      actual_id: /root/evaluator_r2
      canonical_task_id: /root/evaluator_r2
      excluded_reason: required_impact_dimension_missing
    evaluator_round_2_valid:
      actual_id: /root/evaluator_r2_retry
      canonical_task_id: /root/evaluator_r2_retry
      fresh: true
      prior_scores_visible: false
      prior_decisions_visible: false
    panel:
      mutually_blind: true
      peer_reports_visible: false
      roles:
        novelty_gap:
          actual_id: /root/panel_novelty
          decision: conditional
        feasibility_method:
          actual_id: /root/panel_method
          decision: blocked
        pi_strategy:
          actual_id: /root/panel_pi
          decision: blocked
    assembler:
      actual_id: /root/portfolio_assembler
      canonical_task_id: /root/portfolio_assembler
      rescored: false
  isolation:
    independent_instances_used: true
    evaluators_involved_in_writing: false
    panel_prior_scores_visible: false
    panel_peer_reports_visible: false
    source_edits_performed: false
  files_read:
    - research-idea-orchestrator/SKILL.md
    - references/artifact-naming-and-directory-rules.md
    - references/workflow-manifest.md
    - templates/round-manifest.md
    - references/idea-id-and-lineage-rules.md
    - references/artifact-contracts.md
    - references/evidence-confirmation-and-routing.md
    - references/delegate-brief-templates.md
    - references/loop-control-and-stop-rules.md
    - references/evaluation-rubric.md
    - references/handoff-validation.md
    - references/proposal-handoff-rules.md
  files_written: []
  browsing_performed: false
  external_actions: []
  dissent:
    consensus: false
    novelty_gap: conditional_internal_baseline_only
    feasibility_method: blocked
    pi_strategy: blocked
  terminal_condition: PI_review_and_specification_clarification
  proposal_drafted: false
  submitted_externally: false
```
