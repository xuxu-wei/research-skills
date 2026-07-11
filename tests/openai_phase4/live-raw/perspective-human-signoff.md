## Final human-review package

Workflow stopped at the required human-review/signature gate. Nothing was written to the repository or submitted externally.

Status: `outlet-targeting-only`

Reasons:

- No named outlet was selected.
- Seven `[AUTHOR TO VERIFY]` locations remain.
- Human author approval and source verification are still required.

### Final manuscript — frozen v004

# Clinical AI Oversight Should Be Risk-Proportionate

Clinical AI oversight should be organized around risk, not around a universal demand for the same monitoring intensity everywhere. Practical quality can change even when the model itself is unchanged because patient mix, documentation style, prompts, interfaces, and workflows can change [AUTHOR TO VERIFY]. The relevant question is therefore not whether a model once met an aggregate standard, but whether a defined use remains acceptable under the conditions in which it is actually used. A proportionate framework should assess five dimensions: consequence, autonomy, volume, detectability, and reversibility. Higher consequence, greater autonomy, larger volume, lower detectability, or weaker reversibility can justify greater oversight, while the opposite pattern can justify less frequent review, provided the monitoring loop remains available.

Aggregate performance is an inadequate organizing principle because it can hide failure in a clinical task, site, language, or subgroup [AUTHOR TO VERIFY]. Oversight should therefore cover at least five domains: model-output quality, workflow reliability, human-review performance, subgroup/site equity, and downstream clinical/process outcomes. These domains are a minimum conceptual set, not a validated or exhaustive taxonomy. The domains should be interpreted together: acceptable model-output quality does not establish workflow reliability, and review activity does not establish favorable downstream clinical/process outcomes. Where data support it, subgroup/site equity should be examined rather than inferred from an aggregate. Selection should remain anchored to the use case, the five risk dimensions, and decisions that can follow from observed deterioration.

Human review deserves a central but limited place in this framework. It is important, yet it does not guarantee that problems will be detected. Time pressure, automation bias, ambiguous accountability, and poor interface design can all weaken review in practice [AUTHOR TO VERIFY]. Monitoring human-review performance is therefore distinct from merely recording that a person was present. The oversight question is whether review functions as expected for the scoped use case and whether failures would be observable soon enough to support action. The framework does not assume that more review is always better. Review imposes costs and may itself become unreliable. Its form and frequency should correspond to consequence, autonomy, volume, detectability, and reversibility, with explicit ownership rather than an undefined expectation that someone will notice.

A complete loop begins with a scoped use case and owner; baseline; event/version logging; sentinel and sampled review; subgroup/site review where data support it; action thresholds; incident response/rollback; and periodic retirement. Continuous monitoring means that this loop remains available, not that every measure is inspected at every moment. Cadence may be periodic, event-triggered, or risk-based. The loop creates distinct functions that should not be collapsed. Event/version records support traceability and reproducibility. Sentinel and sampled review support observability. Predefined action thresholds support response reproducibility. Rollback supports response capability. Prospective logging of use, sampled outcome review, predefined escalation thresholds, version/change records, and rollback capability can make deterioration more observable and responses more reproducible [AUTHOR TO VERIFY]. None of these elements alone establishes safety; their value lies in connecting observation to accountable action for a defined use.

The strongest counterposition is that continuous monitoring can become costly theater: attribution is weak, samples are small, and the resulting activity may look rigorous without producing dependable conclusions. This objection is especially important because monitoring consumes staffing, data, governance, and opportunity costs [AUTHOR TO VERIFY]. Universal high-frequency review can be disproportionate for low-risk or low-volume uses. A framework that ignores those burdens may divert capacity from uses with greater consequence, autonomy, volume, low detectability, or weak reversibility. Risk proportionality is therefore not an excuse for minimal oversight; it is a method for deciding where intensity earns its cost. The response to the costly-theater critique is not to claim that monitoring proves causation. It is to define what is being observed, why it matters, who owns the response, and what action follows a threshold, while retiring measures or the tool when continued monitoring is not justified.

Small sites present a specific proportionality problem. Their observations may be too sparse to support stable local conclusions [AUTHOR TO VERIFY]. Pooled surveillance combined with local sentinel review is a proposed proportional approach, not an established solution. Pooling may make shared deterioration more observable, while local sentinel review preserves attention to a site's own clinical task, language, patient mix, documentation style, interfaces, and workflows. Neither component removes the limitations of the other. Pooled results can still hide site variation, and local review can remain too sparse for confident interpretation. The design implication is modest: do not require a small site to imitate the review frequency of a high-volume setting merely for consistency. Instead, keep the common loop available, specify local ownership and escalation, and use the cadence that the five risk dimensions and available data can support.

Metrics are useful only when they are linked to risk and action. Poorly risk-linked metrics can produce alert fatigue or false reassurance [AUTHOR TO VERIFY]. A metric that changes frequently but has no clear relationship to consequence, autonomy, volume, detectability, or reversibility may consume attention without improving response. Conversely, a stable metric may reassure users while failure remains hidden in another domain. The five-domain minimum helps expose this problem, but it does not solve metric selection automatically. Each measure should have a stated domain, use-case scope, owner, cadence, and action threshold. The threshold should identify an escalation response without pretending that a single number captures safety. When a measure repeatedly fails to inform action, its cost and risk linkage should be reconsidered. The framework permits stopping or retiring a measure, and it permits stopping or retiring the tool, particularly where costs are disproportionate or metrics create alert fatigue or false reassurance.

This proposal makes deliberately limited claims. There is no proof that continuous monitoring eliminates harm, that the same cadence is appropriate for all uses, or that one metric establishes safety. The framework instead offers a reproducible structure for observing change and responding under uncertainty. Its proportionality depends on explicit judgments, not hidden assumptions: what consequences matter, how much autonomy exists in practice, how much volume magnifies exposure, how detectable deterioration is, and how reversible its effects or deployment are. Those judgments should shape periodic, event-triggered, or risk-based cadence across model-output quality, workflow reliability, human-review performance, subgroup/site equity, and downstream clinical/process outcomes. Because the five domains are conceptual rather than validated or exhaustive, users should not treat completion of a checklist as evidence of acceptable performance. The loop is an accountability structure, not a guarantee.

The practical recommendation is to replace universal monitoring schedules with a documented, risk-proportionate loop. Define the scoped use case and owner, establish a baseline, log events and versions, conduct sentinel and sampled review, examine subgroup/site performance where data support it, set action thresholds, maintain incident response and rollback, and periodically consider retirement. Recordkeeping should preserve traceability and reproducibility; review should preserve observability; thresholds should make responses reproducible; rollback should preserve response capability. Allocate intensity according to consequence, autonomy, volume, detectability, and reversibility, while recognizing staffing, data, governance, and opportunity costs. For small sites, pooled surveillance plus local sentinel review may be proposed with its limitations stated. For every setting, the endpoint is not more monitoring by default, but a loop that remains available, produces interpretable signals, supports accountable response, and can stop or retire measures or the tool when continued use or observation is not justified.

Word count: 1,207.

## Claim ledger

| Claim | Authorized formulation | Boundary |
|---|---|---|
| C1 | Govern deployed clinical generative AI as a continuously measured sociotechnical intervention. | Normative; monitoring does not guarantee safety. |
| C2 | Contextual changes can alter practical quality without a model-version change. | No claim of inevitable deterioration. |
| C3 | Aggregates can conceal task-, site-, language-, or subgroup-specific failure. | Disaggregate only where data support interpretation. |
| C4 | Human review is important but insufficient as the sole control. | Does not imply that human review is ineffective. |
| C5 | Logging, review, thresholds, records, and rollback improve observability or response reproducibility. | No claim that they prevent harm or prove causation. |
| C6 | Monitoring intensity should be risk-tiered. | No universal cadence or “more is better” rule. |
| C7 | Small sites may use pooled surveillance plus local sentinels. | Proposal only; pooling does not solve sparse or local inference. |
| C8 | Monitor five distinct domains. | Minimum conceptual decomposition, not a complete safety metric. |
| C9 | Use an accountable governance loop through retirement. | Proposed framework, not a validated checklist. |
| C10 | Predeployment validation is necessary but insufficient. | It remains essential. |
| C11 | Monitoring can itself cause burden, alert fatigue, false reassurance, or theater. | Possibility, not a claim that monitoring is generally ineffective. |
| C12 | Supplied evidence does not prove harm elimination, one cadence, or one safety metric. | Absence of proof is not proof of impossibility. |

Reference ledger: no fabricated references. Seven manuscript locations remain marked `[AUTHOR TO VERIFY]`.

## Argument architecture

1. Establish why unchanged models can perform differently in changing clinical contexts.
2. Preserve predeployment validation but reject its use as a permanent certificate.
3. Tier monitoring by consequence, autonomy, volume, detectability, and reversibility.
4. Separate the five measurement domains.
5. Place human review inside the measured sociotechnical system.
6. Connect ownership, baselines, records, sampling, thresholds, rollback, and retirement.
7. Address sparse small-site evidence using a qualified pooled-plus-local proposal.
8. Present costly compliance theater as the strongest counterposition.
9. Answer through proportionality, uncertainty, shared capacity, and explicit stopping—not maximal measurement.

## Manuscript lineage and revision record

| Version | Status | Evaluation/route |
|---|---|---|
| v001 | Superseded | 1,218 words; independently accepted; panel requested substantive clarification. |
| v002 | Superseded | Clarified mechanism functions and panel concerns but expanded beyond the word target; fresh evaluation required revision. |
| v003 | Blocked | Met length but introduced unregistered claims and altered required risk dimensions; never promoted. |
| v004 | Final frozen source | 1,207 words; restored P1–P8-only scope; fresh evaluator accepted. |

Three targeted revision rounds were used. No further textual revision is authorized without creating v005 and obtaining a new independent evaluation.

## Independent evaluations

- v001 evaluator: accepted; hard-gate scores 4–5. Novelty remained provisional.
- v002 evaluator: revision required because the estimated length exceeded the target by approximately 29%; substantive calibration was otherwise strong.
- v004 evaluator: accepted, overall 4.63/5.

Final v004 scores:

| Dimension | Score |
|---|---:|
| Thesis clarity | 5 |
| Argument integrity | 5 |
| Evidence–claim match | 4 |
| Narrative coherence | 5 |
| Stance calibration | 5 |
| Contribution sufficiency | 4 |
| Audience/outlet fit | 5 |
| Novelty | 4, provisional |

Medical-journal review: pass; no blocking substantive finding.

Language assessment: `pass_no_change`; no source text was modified.

## Panel report and preserved dissent

Panel roles:

- Counter-position
- Evidence
- Narrative
- Practicing clinician

Recurring panel concerns addressed in v004:

- Pooled surveillance is now explicitly a proposal, not an established solution.
- Records, review, thresholds, and rollback have distinct bounded functions.
- “Continuous” denotes maintained governance capacity, allowing periodic or event-triggered cadence.
- The five domains are conceptual, nonvalidated, and nonexhaustive.
- Stopping and retirement are explicit outcomes.

Preserved minority position:

> Periodic or event-triggered reassessment should be the baseline unless continuous governance capacity demonstrates decision-relevant incremental value.

Preserved evidence dissent:

> Small-site pooled surveillance plus local sentinel review is not established as effective and must remain proposal-only.

Additional clinician requests for new endpoint, fallback-workflow, intersectional, staffing, and patient-reporting claims were not incorporated because they exceeded the frozen ledger.

## Final verification and readiness

The independent compositor reported:

- source edits: none;
- title changes: none;
- claim changes: none;
- placeholder changes: none;
- source-text identity: pass;
- P1–P8 scope: pass;
- anti-pattern scan: pass;
- medical review: pass;
- language review: pass without change.

A hexadecimal SHA-256 was not invented because no file was materialized. Identity was verified against the same canonical in-memory UTF-8/LF payload.

Before submission:

1. Select and verify a named outlet.
2. Resolve all seven author-verification placeholders.
3. Add verified citations without strengthening claims.
4. Obtain author approval, disclosures, and signature.
5. Re-evaluate and re-verify if any prose changes.

## Machine-readable execution receipt

```yaml
workflow_id: PVO-20260712-001
mode: full
plugin_version: 0.5.0-preview.1
final_state: human_signoff_required
readiness: outlet-targeting-only
external_submission: false

artifacts:
  claim_ledger: CL-PVO-20260712-001-v001
  claim_matrix: CEM-PVO-20260712-001-v001
  architecture: PVO-20260712-001-ARGSKEL-001
  drafts:
    - {version: v001, status: superseded}
    - {version: v002, status: superseded}
    - {version: v003, status: blocked_unregistered_claims}
    - {version: v004, status: final_frozen, words: 1207}
  final_manuscript: 08_final/final-perspective.md

instances:
  input_builder:
    actual: /root/input_builder
    canonical: perspective-input-builder
  claim_curator:
    actual: /root/claim_curator
    canonical: PCEC-PVO-20260712-001-01
  argument_architect:
    actual: /root/argument_architect
    canonical: perspective-argument-architect
  drafter_v001:
    actual: /root/drafter_v001
    canonical: perspective-drafter-v001
  evaluator_v001:
    actual: /root/evaluator_v001
    canonical: perspective-evaluator-v001-fresh-20260712
  panel_counter:
    actual: /root/panel_counter
    canonical: perspective-panel-counter-20260712-001-r001-i01
  panel_evidence:
    actual: /root/panel_evidence
    canonical: evidence-reviewer-7f3c1a92
  panel_narrative:
    actual: /root/panel_narrative
    canonical: narrative-reviewer-r001
  panel_clinician:
    actual: /root/panel_clinician
    canonical: clinician-PVO-20260712-001-r001-7f3c
  revision_v002:
    actual: /root/revision_v002
    canonical: perspective-refinement-drafter-r001
  evaluator_v002:
    actual: /root/evaluator_v002
    canonical: perspective-evaluator-20260712-v002-fresh-01
  revision_v003:
    actual: /root/revision_v003
    canonical: perspective-refinement-drafter-r002
  revision_v004:
    actual: /root/revision_v004
    canonical: perspective-refinement-drafter-r003
  evaluator_v004:
    actual: /root/evaluator_v004
    canonical: perspective-evaluator-v004-final-20260712
  medical_review:
    actual: /root/medical_review_v004
    canonical: medical_review_v004
  language_review:
    actual: /root/language_v004
    canonical: language-v004-20260712-01
  final_compositor:
    actual: /root/final_compositor
    canonical: perspective-final-compositor-PVO-20260712-001-fresh-01

event_order:
  - initialize
  - input_normalize
  - curate_claims
  - architect
  - draft_v001
  - evaluate_v001_accept
  - panel_counter_evidence_narrative_clinician
  - revise_v002
  - evaluate_v002_revision_required
  - revise_v003_blocked
  - revise_v004
  - evaluate_v004_accept
  - medical_review_pass
  - language_review_pass_no_change
  - final_compose_verify
  - stop_at_human_signature

isolation:
  reviewer_mode: fresh_subagent
  prior_scores_visible_to_reviewers: false
  panel_peer_outputs_visible: false
  hidden_orchestrator_reasoning_visible: false
  source_edits_by_reviewers: false
  final_compositor_repairs: false

panel_roles:
  - counter-position
  - evidence
  - narrative
  - practicing-clinician

preserved_dissent:
  - periodic/event-triggered reassessment may be the preferable default
  - small-site pooled surveillance remains an unvalidated proposal

filesystem:
  repository_files_written: []
  project_files_written: []
  virtual_artifacts_only: true
  skill_files_read:
    - perspective-orchestrator/SKILL.md
    - references/workflow-modes.md
    - references/workflow-manifest-schema.md
    - references/decision-log-schema.md
    - references/artifact-naming-and-directory-rules.md
    - references/io-contracts.md
    - references/delegate-brief-templates.md
    - references/loop-control-rules.md
    - references/panel-decision-routing.md
    - references/generic-outlet-profiles.md
    - references/anti-patterns.md

verification:
  final_source_version: v004
  latest_evaluator_version: v004
  source_text_identical: true
  fabricated_references: false
  author_verification_markers: 7
  medical_blocker: false
  language_change_saved: false
  human_signature_required: true
```