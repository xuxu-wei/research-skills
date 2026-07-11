The Standard workflow stopped at the mandatory independent-evaluation gate. A second textual revision would provide no substantive gain because every remaining critical issue requires source information excluded from the frozen artifacts.

Therefore:

- No three-role panel was convened.
- No frontmatter/cover-letter promotion occurred.
- No submission compositor/verifier was commissioned.
- No package was labeled submission-ready or source-text independently verified.
- Nothing was submitted externally.
- No repository or project files were written.

## Human-review package

### Workflow disposition

```yaml
workflow:
  id: wf-telehf90-20260712
  mode: standard
  status: stopped
  stop_condition: stop_no_gain
  current_gate: independent_evaluation
  current_manuscript: manuscript-v002@v002
  current_supplement: supplementary-v002@v002
  claim_audit: pass
  language_assessment: pass
  latest_evaluation:
    decision: revise
    readiness: major_revision
    fatal_scientific_flaw: false
    evidence_claim_alignment: pass
    reporting_completeness: fail
  panel_status: not_started_gate_not_met
  submission_verification: not_started_gate_not_met
  external_submission: prohibited
  next_required_action: human_author_source_completion
```

### Blueprint

TELE-HF90 is framed as a pragmatic, multicenter, individually randomized trial estimating the effects of a specific 90-day remote-monitoring implementation after acute heart-failure hospitalization.

The permitted central conclusion is:

> The primary estimate favored connected monitoring, but the 95% confidence interval included no difference and the result was inconclusive at the conventional statistical threshold. Secondary, patient-reported, implementation, and safety findings were mixed and do not establish benefit, equivalence, or harm.

The blueprint prohibits:

- Proof-of-benefit, equivalence, or harm claims.
- A global novelty or “first” claim.
- Treating favorable secondary estimates as resolving the inconclusive primary result.
- Comparative safety inference from descriptive counts.
- Subgroup-effect claims.

Planned principal displays are the CONSORT flow, baseline table, primary and secondary outcome table, descriptive safety table, missing-data sensitivities, KCCQ sensitivity results, and exploratory interaction results. Displays lacking frozen source data remain placeholders.

### Methods/statistics audit

Decision: `conditionally_pass_with_author_verification`.

The independent auditor found no supplied methodological defect requiring reanalysis. The randomized design, concealed allocation, stratification, blinded outcome assessment, ITT estimand, adjusted risk-ratio model, and missing-data sensitivities support drafting.

Required author verification remains:

- Sample-size calculation and assumptions.
- Exact endpoint definitions and ascertainment.
- Full protocol and statistical analysis plan.
- Imputation variables, number of imputations, pooling, and diagnostics.
- Exact complete-case and delta-MNAR outputs.
- Multiplicity hierarchy.
- KCCQ model and worst-rank sensitivity details.
- Baseline characteristics and full participant flow.
- Safety definitions, denominators, severity, and relatedness.

### Current manuscript: v002

**Working title**

Connected Weight and Symptom Monitoring After Hospitalization for Acute Heart Failure: The TELE-HF90 Randomized Trial

**Structured abstract**

**Importance:** Prior remote-monitoring trials were described in the supplied evidence summary as heterogeneous, and implementation intensity may influence effects. No literature references were supplied or independently searched.

**Objective:** To compare 90 days of connected weight and symptom monitoring reviewed by a centralized pharmacist-nurse team using a prespecified escalation algorithm with usual care without study-provided monitoring among adults discharged home after acute heart-failure admission.

**Design, setting, and participants:** TELE-HF90 was a pragmatic, parallel, individually randomized trial at six hospitals using existing devices and electronic health record integration. Of 1,246 adults screened, 1,204 were randomized before discharge, with 602 assigned to each group.

**Interventions:** Connected weight and symptom monitoring with centralized pharmacist-nurse review and prespecified escalation, or usual care without study monitoring.

**Main outcomes and measures:** The primary outcome was readmission or death by day 90. The prespecified primary analysis estimated an intention-to-treat risk ratio using a log-binomial model adjusted for hospital and LVEF stratum, with modified Poisson robust regression as fallback. Missing readmission status was multiply imputed under MAR.

**Results:** All 1,204 randomized participants were included in the intention-to-treat analysis. Primary-outcome status was observed for 1,188 participants and unobserved for 16 overall; group-specific missing-status counts were not supplied. Death-registry status was complete. Readmission or death occurred in 151 of 602 intervention participants and 181 of 602 usual-care participants (adjusted RR, 0.84; 95% CI, 0.70–1.01; two-sided P=.067). Complete-case and delta-adjusted MNAR estimates ranged from 0.83 to 0.87, and all confidence intervals included 1. The adjusted mean difference in days alive and out of hospital was 2.4 days (95% CI, 0.3–4.5). Heart-failure readmission occurred in 96 versus 118 participants (adjusted RR, 0.82; 95% CI, 0.64–1.04), and mortality occurred in 31 versus 29 (adjusted RR, 1.07; 95% CI, 0.65–1.76). The between-group KCCQ change difference was 2.1 points (95% CI, 0.4–3.8), below the prespecified clinically important difference of 5 points. Intervention-triggered emergency-department visits numbered 49 versus 31, documented hypotension 18 versus 15, and acute kidney injury 14 versus 13. These safety findings are descriptive. Among intervention participants, 74% transmitted data on at least 70% of assigned days. No subgroup interaction met the prespecified exploratory threshold.

**Conclusions and relevance:** The primary estimate favored connected monitoring, but its confidence interval included no difference and the result was inconclusive at the conventional statistical threshold. Secondary findings are supportive rather than confirmatory pending verification of the prespecified hierarchy and multiplicity approach; they cannot resolve the primary uncertainty. The findings do not establish benefit, equivalence, or harm.

**Trial registration:** `[REGISTRY AND IDENTIFIER REQUIRED]`

The full manuscript contains Introduction, Methods, Results, Discussion, Conclusions, three outcome tables, declarations, and supplementary sections. Missing information is marked `AUTHOR/SOURCE VERIFICATION BLOCKER`; no values or citations were reconstructed.

### Revision record

Round 000 was an evidence-relinking action and did not consume a substantive revision round. It retained the supplied phrase “intervention-triggered ED visits” and made its provenance explicit. The original auditor’s contrary concern is preserved below.

Round 001 created manuscript and supplement v002. It:

- Reported that 16 of 1,204 primary statuses were unobserved overall.
- Did not invent group-specific missingness.
- Labeled secondary findings consistently as supportive and nonconfirmatory.
- Stated that secondary estimates cannot resolve the inconclusive primary result.
- Preserved every missing source-dependent field as a blocker.
- Made no numerical changes.

### Claim audits

The first substantive claim audit requested removal or substantiation of “intervention-triggered,” judging its ledger provenance insufficiently explicit.

That recommendation was declined because “intervention-triggered ED visits 49 versus 31” was an exact frozen user fact. The evidence ledger was relinked without changing manuscript text.

A fresh isolated auditor then verified the phrase and passed C007. After revision round 1, another fresh claim auditor passed all C001–C011 with no fatal overclaims.

Preserved limitations:

- All evidence remains user-supplied and independently unverified.
- Exact missing-data sensitivity outputs are unavailable.
- KCCQ death-sensitivity output is unavailable.
- Safety definitions and denominators are unavailable.
- Literature claims lack verified citations.

### Independent evaluations

Evaluation v001 found:

- No fatal scientific flaw.
- Strong claim–evidence alignment.
- Acceptable structure and academic language.
- Failed reporting-completeness, governance/declaration, literature-grounding, and journal-compliance gates.
- Decision: `revise / major_revision`.

Language assessment v001 independently passed without a language hard-gate failure.

Evaluation v002, blind to evaluation v001, again found:

- Scientific validity: pass.
- Evidence–claim alignment: pass.
- Genre/rhetoric: pass.
- Language baseline: pass.
- Minimum reporting completeness: fail.
- Submission verification: not checked.
- Decision: `revise / major_revision`.

Because the unresolved critical findings were materially unchanged and cannot be resolved from the frozen facts, the workflow invoked `stop_no_gain`.

### Preserved dissent

```yaml
dissent:
  - id: dissent-claim-001
    source: claim-auditor-v001
    finding: "'intervention-triggered' was insufficiently supported in the initial ledger"
    severity: major_nonfatal
    disposition: declined_after_evidence_relink
    preserved: true
    rationale: exact frozen user wording supported the classification
  - id: dissent-eval-001
    source: evaluator-v001
    finding: manuscript scientifically coherent but not peer-review ready
    severity: critical_reporting
    disposition: unresolved
    preserved: true
  - id: dissent-eval-002
    source: evaluator-v002
    finding: reporting-completeness gate still fails after targeted revision
    severity: critical_reporting
    disposition: workflow_stop_no_gain
    preserved: true
```

### Frontmatter and cover placeholders

```text
Authors: [REQUIRED]
Affiliations: [REQUIRED]
Corresponding author: [REQUIRED]
Trial registration: [REQUIRED]
Ethics approval: [REQUIRED]
Consent: [REQUIRED]
Funding: [REQUIRED]
Conflicts of interest: [REQUIRED]
Author contributions: [REQUIRED]
Data availability: [REQUIRED]
Code availability: [REQUIRED]
Acknowledgments: [REQUIRED]
Target journal: [REQUIRED]
Cover letter: BLOCKED pending target journal, authorship, declarations, and verified literature context
References: No references supplied; must be completed and verified before submission
```

### Human actions required to resume

Supply:

1. Target journal and current author instructions.
2. Author list, affiliations, and corresponding-author details.
3. Registration identifier, ethics approval, and consent information.
4. Funding, conflicts, contributions, data/code availability, and acknowledgments.
5. Baseline table and complete CONSORT flow.
6. Full eligibility, study dates, sample-size calculation, intervention/comparator details, and endpoint definitions.
7. Full protocol/SAP and exact statistical outputs.
8. Safety definitions and denominators.
9. A permitted, verifiable literature set.

After these are frozen, the workflow must create a new manuscript version, run a fresh claim audit and evaluator, and only then—if accepted—convene the three-role panel and independent submission compositor.

## Execution receipt

```json
{
  "workflow_id": "wf-telehf90-20260712",
  "plugin_version": "0.5.0-preview.1",
  "entry_mode": "standard",
  "final_status": "stopped",
  "stop_condition": "stop_no_gain",
  "human_review_required": true,
  "external_submission_performed": false,
  "files_written": [],
  "files_read": [
    "article-orchestrator/SKILL.md",
    "references/workflow-state-schema.md",
    "references/artifact-naming-and-directory-rules.md",
    "references/artifact-contracts.md",
    "references/artifact-review-and-submission-contracts.md",
    "references/handoff-validation.md",
    "references/delegate-brief-templates.md",
    "references/delegation-rules-pattern.md",
    "references/loop-control-rules.md",
    "references/evidence-confirmation-and-routing.md",
    "references/evidence-provenance-ledger-schema.md",
    "templates/round-manifest.md"
  ],
  "artifacts": {
    "blueprint": "blueprint-001@v1",
    "evidence_ledger": "evidence-ledger-002@v2",
    "methods_audit": "methods-audit-001@v1",
    "manuscripts": ["manuscript-v001@v001", "manuscript-v002@v002"],
    "supplements": ["supplementary-v001@v001", "supplementary-v002@v002"],
    "claim_audits": [
      "claim-audit-v001-blocked-input-attempt",
      "claim-audit-001",
      "claim-audit-evidence-relink-001",
      "claim-audit-v002"
    ],
    "evaluations": ["evaluation-v001", "evaluation-v002"],
    "language_assessments": ["language-assessment-v001"],
    "revision_rounds": ["round-000-evidence-relink", "round-001"],
    "panel": null,
    "submission_package": null
  },
  "instances": [
    {"canonical": "/root/readiness_telehf90", "actual": "readiness_telehf90", "role": "readiness", "fresh": true},
    {"canonical": "/root/methods_audit_telehf90", "actual": "methods-auditor-wf-telehf90-20260712-001", "role": "methods_statistics_audit", "fresh": true},
    {"canonical": "/root/claim_audit_v001", "actual": "/root/claim_audit_v001", "role": "claim_audit_blocked_attempt", "fresh": true},
    {"canonical": "article-claim-auditor", "actual": "article-claim-auditor-telehf90-002", "role": "claim_audit_v001", "fresh": true},
    {"canonical": "article-claim-auditor", "actual": "article-claim-auditor-telehf90-relink-7f3c91", "role": "claim_reaudit", "fresh": true},
    {"canonical": "article-claim-auditor", "actual": "claim-auditor-v002-fresh-01", "role": "claim_audit_v002", "fresh": true},
    {"canonical": "article-evaluator", "actual": "article-evaluator-telehf90-v001-7f3c", "role": "evaluation_v001", "fresh": true},
    {"canonical": "academic-language-assessor", "actual": "language-assessment-telehf90-20260712-v001", "role": "language_v001", "fresh": true},
    {"canonical": "article-evaluator", "actual": "eval-v002-fresh-telehf90-20260712", "role": "evaluation_v002", "fresh": true}
  ],
  "isolation": {
    "reviewers_fresh": true,
    "prior_scores_visible": false,
    "source_edits_by_reviewers": false,
    "peer_reports_cross_exposed": false
  },
  "event_order": [
    "initialize",
    "readiness",
    "context",
    "constrained_grounding",
    "blueprint",
    "methods_audit",
    "draft_v001",
    "claim_audit_blocked_input_attempt",
    "claim_audit_v001",
    "evidence_relink",
    "fresh_claim_reaudit",
    "evaluation_v001_and_language_assessment",
    "revision_round_001",
    "claim_audit_v002",
    "evaluation_v002",
    "stop_no_gain"
  ],
  "panel_roles": [],
  "preserved_dissent": [
    "initial C007 provenance objection",
    "evaluation-v001 reporting-completeness failure",
    "evaluation-v002 reporting-completeness failure"
  ],
  "source_text_identical_submission_verification": false,
  "reason_verification_not_run": "Evaluator acceptance gate was not met"
}
```