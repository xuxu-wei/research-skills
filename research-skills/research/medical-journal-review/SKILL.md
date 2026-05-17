---
name: medical-journal-review
description: "Use when review a medical research design, protocol, or manuscript from the perspective of top-tier journal editors (JAMA/BMJ/Lancet/Nature Medicine). Assess design quality, identify fatal flaws, and suggest redesign strategies."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, medical-review, clinical-trial, editorial, study-design, journal, peer-review]
    related_skills: [pubmed]
---

# Medical Journal Research Design Review

Simulate the editorial review process of top-tier general medical journals (JAMA, BMJ, Lancet, Nature Medicine, NEJM). Assess research questions, study design, evidence quality, and publication readiness. Identify fatal flaws and propose redesign strategies.

## When to Use

Use this skill when the user asks you to:

- Review a medical research design, protocol, or manuscript
- Assess whether a study has top-journal potential
- Optimize research question, primary outcome, comparator, analysis strategy, or submission narrative
- Simulate editorial or reviewer feedback from top-tier journals
- Reconstruct a higher-impact design based on existing data
- Select a target journal tier (JAMA/BMJ/Lancet/NEJM/Nature Medicine vs. specialty top vs. open-access)

Do NOT use for: general medical Q&A, individual patient care advice, pure language polishing, or fabricating research content.

## Core Principles

You are a simulated top-journal editor, clinical epidemiologist, statistical reviewer, and policy impact assessor. Your task is to scrutinize research materials (study question, design, protocol, draft, data source, or preliminary results) and deliver actionable design optimization advice.

Core objectives:

1. Judge whether the research question is important
2. Judge whether the current design can answer the question
3. Judge whether available materials support the claimed conclusions
4. Identify fatal flaws, bias, confounding, and statistical risks
5. Reconstruct a more important, credible, and impactful design using the same materials
6. Recommend target journal tier and pre-submission action checklist

**Do NOT:** promise publication, fabricate data/literature/results, engage in HARKing, p-hacking, fake pre-registration, or conceal negative/safety results.

## Input Requirements

Extract as much as possible from user-provided materials. If information is missing, do NOT halt — explicitly state the uncertainty and its impact.

**Supplementary materials discovery — always check before reviewing.** When a manuscript is provided (e.g., as a `.docx` file), the supplementary materials are often a separate file in the same session batch. Search the cache for matching filenames:
- Pattern: `<manuscript_name>supplementary<...>.docx` or similar
- Use `search_files` targeting `/home/ubuntu/.hermes/cache/documents/` and broader `~/.hermes/cache/`
- Check `ls` in the cache documents directory for files uploaded close together in time
- If the manuscript mentions "Supplementary Methods," "Table S1," or "Figure S1," but no supplement file is found, state this explicitly in the review as missing information

When loading a supplementary `.docx`, use the same extraction approach as the main manuscript. If the document is large, the `unzip` + XML `iterparse` fallback from `office-toolkit` is the most reliable method.

```json
{
  "research_topic": "Research topic",
  "research_question": "Current research question",
  "study_type": "Study type",
  "population": "Study population",
  "data_source": "Data source",
  "exposure_or_intervention": "Exposure, intervention, test, or predictor",
  "comparator": "Control group or comparison strategy",
  "primary_outcome": "Primary outcome",
  "follow_up_or_time_window": "Follow-up or observation window",
  "sample_size": "Sample size",
  "analysis_plan": "Current analysis plan",
  "preliminary_results": "Preliminary results",
  "registration_ethics": "Registration, ethics, and data use information",
  "target_journal": "Target journal or tier"
}
```

When information is insufficient, first output:

- What can be judged given current information
- What cannot be judged
- The most critical missing pieces
- How missing information affects judgment reliability

## Two Review Frameworks

This skill supports two complementary frameworks. Choose based on the user's goal:

| Framework | When to Use | Focus |
|-----------|-------------|-------|
| **10-step Design Review** (below) | Redesign, methodology reconstruction, protocol optimization | "How can this design be improved?" |
| **12-step Editorial Review** ([`references/12-step-editorial-review.md`](references/12-step-editorial-review.md)) | Editorial judgment, publishability, journal competitiveness | "Would BMJ/Nature Medicine/JAMA publish this?" |

The 10-step process is the default. The 12-step process has been used in practice for reviewing postdoc research proposals (I201, I202) and paired-paper strategies. The two frameworks use different scoring rubrics — use the one that matches the review's goal.

## Review Process (10-Step Design Review)

Execute in order. **Before forming any conclusions about missing analyses, examine all supplementary materials provided.** Many analyses that appear absent from the main manuscript — calibration plots, sensitivity analyses, detailed subgroup results — are often in the supplement. Never declare an analysis "missing" based on the main text alone.

### Step 1: Identify Study Type and Claim Type

Identify study type: RCT, non-randomized intervention, cohort, case-control, cross-sectional, diagnostic study, prediction model, medical AI, real-world study, systematic review/meta-analysis, mechanism study, economic evaluation, etc.

Identify claim type: descriptive, associative, causal, predictive, diagnostic, efficacy, safety, mechanistic, or policy claim.

**Must state:** what claims the current design actually supports, and whether overclaiming exists.

### Step 2: Structured Design Summary

Extract: research question, PICO/PECO/PICOTS, data source, population, exposure/intervention, comparator, primary outcome, follow-up, sample size, analysis plan, target journal.

### Step 3: Editorial Desk Review

Simulate top-journal desk review:

- Whether to send for external review
- Most likely current editorial decision
- Greatest strength
- Greatest fatal weakness
- Most likely rejection reason
- Whether the research question needs reconstruction

### Step 4: Scientific Importance

Assess:

- Whether it addresses a major clinical, public health, or policy problem
- Whether a clear evidence gap exists
- Whether it could influence clinical practice, guidelines, reimbursement, screening, care pathways, or policy
- Whether it holds value for general medical journal readers
- Why it's worth studying now

Grade:

| Grade | Description |
|-------|-------------|
| **A** | May change practice or policy |
| **B** | May change specialty understanding |
| **C** | Primarily supplementary evidence |
| **D** | Mainly local experience or descriptive |
| **E** | Insufficient top-journal value |

### Step 5: Design-Material Fit

Judge whether the question the user wants to answer matches what the data can actually answer.

Key checks:

- Are descriptive data being packaged as causal conclusions?
- Is a cross-sectional study attempting to infer temporal order?
- Is an observational study overusing efficacy language?
- Is a prediction model misrepresented as a causal study?
- Does a real-world study need target trial emulation?
- Can existing data support the primary outcome and comparison strategy?

### Step 6: Fatal Flaw Check

Must explicitly determine whether fatal flaws exist.

Common fatal flaws:

- Research question is unimportant
- Design cannot answer the question
- Primary outcome is post-hoc selected and unjustifiable
- Time zero, exposure, comparator, or outcome definitions are unclear
- Necessary control group is missing
- Key confounders are entirely absent
- Sample size is clearly insufficient
- Data quality is unverifiable
- Ethics, registration, or data access has hard issues
- Selective reporting of negative or safety results
- AI/prediction models lack external validation but claim clinical applicability

Output: existence, fixability, impact on submission, handling strategy.

### Step 7: Methodological Review

Focus areas by study type. For detailed statistical review standards — including missing data handling, subgroup analysis pitfalls, calibration requirements for prediction models, and variable selection guidance — consult [`references/bmj-statistical-review-standards.md`](references/bmj-statistical-review-standards.md) (Riley et al., BMJ 2022).

| Study Type | Key Focus |
|------------|-----------|
| **RCT** | Registration, protocol, SAP, randomization, allocation concealment, blinding, sample size, ITT, primary outcome, safety, CONSORT/SPIRIT |
| **Observational** | Time zero, confounding by indication, immortal time bias, selection bias, information bias, missing data, sensitivity analysis, STROBE/RECORD |
| **Diagnostic** | Index test, reference standard, threshold, verification bias, clinical use scenario, STARD |
| **Prediction model / Medical AI** | Prediction time point, data leakage, internal/external validation, calibration, decision curve, fairness, TRIPOD/TRIPOD-AI |
| **Systematic review / Meta-analysis** | Evidence gap, pre-registration, search strategy, risk of bias, heterogeneity, publication bias, GRADE, PRISMA |
| **Real-world study** | Data auditability, comparison group, time zero, treatment switching, detection frequency differences, target trial emulation, causal language boundaries |

### Step 8: Design Reconstruction

Provide at least 3 design alternatives:

1. **Maximize top-journal impact**
2. **Maximize methodological credibility**
3. **Maximize feasibility with current materials**

Each alternative includes:

- Reconstructed research question
- Suitable journal tier
- Recommended study design
- Recommended primary outcome
- Recommended comparison strategy
- Recommended primary analysis
- Expected editorial interest
- Primary risks
- Minimum supplementary materials needed

### Step 9: Simulated Reviewer Comments

Simulate from three perspectives:

1. **Clinical expert**
2. **Methodological/statistical expert**
3. **Editorial/policy reviewer**

For each: most likely criticism, fatality, design-level prevention strategy, manuscript response strategy.

### Step 10: Target Journal Fit and Action Checklist

Recommend tier and examples:

| Tier | Description |
|------|-------------|
| **Tier 1** | JAMA / BMJ / Lancet / Nature Medicine level — worth attempting |
| **Tier 2** | Specialty top journal — more appropriate |
| **Tier 3** | General medical open-access or methodology journal |
| **Tier 4** | Requires major reconstruction before submission |
| **Tier 5** | Current materials do not support high-level publication |

Final output: Must do / Should do / Optional enhancement / Do not invest.

## Scoring Rubric

Scores represent structured quality assessment, NOT publication probability.

| Dimension | Score |
|-----------|------:|
| Scientific question importance | 20 |
| Evidence gap and originality | 15 |
| Design-question fit | 20 |
| Clinical/public health/policy significance of outcome | 15 |
| Bias control and statistical credibility | 15 |
| Transparency, ethics, registration, reporting standards | 10 |
| Top-journal narrative and journal fit | 5 |
| **Total** | **100** |

Interpretation:

- **85–100**: Has the foundation to target general medical top journals or equivalent specialty tops
- **70–84**: Suitable for specialty top journals, or general tops after significant strengthening
- **55–69**: Publishable value, but low top-journal competitiveness
- **40–54**: Design is clearly inadequate; reconstruction needed
- **<40**: Current materials and design do not support high-impact publication

## Standard Output Template

Use the template at [`templates/review-report.md`](templates/review-report.md) for structured output.

## Safety and Research Integrity Boundaries

Must refuse requests to:

- Fabricate data, results, figures, tables, or literature
- Forge ethics approval, pre-registration, SAP, data sharing, or conflict of interest declarations
- Conceal negative results, adverse events, or safety outcomes
- Selectively report favorable results
- Disguise exploratory analyses as pre-specified analyses
- Present observational associations as definitive causal conclusions
- Circumvent informed consent, ethics approval, privacy protection, or data use licenses

Compliant alternatives:

- Clearly distinguish pre-specified from exploratory analyses
- Transparently report negative and safety results
- Reframe research questions to what existing data can support
- Add sensitivity analyses and limitations statements
- Adjust target journal and manuscript positioning

## Output Quality Requirements

Before each output, self-check:

- Are facts, inferences, and recommendations clearly distinguished?
- Is uncertainty explicitly noted?
- Are fatal flaws identified?
- Is top-journal likelihood exaggeration avoided?
- Is excessive causal language avoided?
- Are actionable revision plans provided?
- Does it cover: question, design, outcome, analysis, bias, submission strategy?
- Does it comply with research integrity and reporting transparency?

## Common Pitfalls

These are the most frequent reasons top-tier medical journal editors reject manuscripts — distilled from editorial experience rather than statistical review alone. They address Impact, Novelty, Relevance, and Robustness at the level editors actually evaluate. For detailed statistical review standards, see [`references/bmj-statistical-review-standards.md`](references/bmj-statistical-review-standards.md) (BMJ statistical editors' 12 most common findings; Riley et al., BMJ 2022).

### Impact & Importance

**1. Interesting methods, uninteresting question.** The single most common editorial rejection. No amount of methodological sophistication can rescue a question that doesn't matter. Ask: would a practicing clinician, guideline committee, or health policymaker change anything based on this answer? If the answer is "no" or "maybe, if replicated 5 more times," the question needs reframing.

**2. Incremental contribution without clear advance.** "First study to apply X method to Y disease" is not a contribution unless the method reveals something previous approaches could not. The editor's question is not "is this new?" but "does this change what we know or what we do?"

### Novelty & Evidence Gap

**3. Failure to articulate the evidence gap.** Many manuscripts dive into methods without establishing what is already known and what critical uncertainty remains. The introduction should answer: "What specific gap does this study fill, and why does that gap matter now?" A vague "more research is needed" is not a gap.

**4. Overclaimed novelty — rediscovering known findings with fancier methods.** Producing the same answer as a simpler, cheaper, or already-published study, but with a more complex model, is rarely publishable in a top-tier journal. Novelty of method does not compensate for absence of novel insight.

### Relevance & Framing

**5. Poor journal fit.** The study may be excellent for a specialty journal but inappropriate for a general medical journal. General journals ask: does this matter to physicians across specialties? Is the problem common, the intervention broadly applicable, the implications generalisable? A perfect nephrology study may not belong in *Lancet*.

**6. Weak narrative — failure to answer "why now" and "so what."** Editors read for story, not just methods. A strong manuscript answers: Why is this question urgent right now? What decision does the evidence inform? What would be lost by not knowing the answer? Manuscripts that read like expanded checklists lose editorial interest regardless of statistical rigour.

**7. Ignoring the patient and public health perspective.** Outcomes that matter to statisticians (AUC, calibration slope, P values) may not matter to patients (symptoms, function, survival, quality of life). Top general journals prioritise patient-centred outcomes. A study demonstrating a statistically significant improvement in a biomarker without clinical outcome data will struggle at the desk review stage.

### Robustness & Credibility

**8. Design-question mismatch.** The most fundamental credibility problem. An observational study cannot answer "does this treatment work?" A cross-sectional survey cannot answer "what causes this outcome?" A prediction model validated only internally cannot claim clinical readiness. The question and the design must be aligned — misalignment is a desk-reject criterion, not a revision point.

**9. Causal overreach.** Using causal language (reduces, improves, prevents, causes, impacts) from non-causal designs (cross-sectional, predictive, associative) is the most common overclaim in medical research. Descriptive or predictive studies must use descriptive or predictive language. If the study design does not support causal inference, neither should the abstract.

**10. Transparency and reproducibility failures.** Missing trial registration, undisclosed protocol deviations, unregistered outcome switching, inaccessible data or code, and vague analytic plans all erode editorial trust. Top journals increasingly require data sharing statements, pre-registration, and adherence to reporting guidelines as preconditions for review — not as post-acceptance formalities.

### Generalizability & Ethics

**11. Overclaimed generalizability.** Findings from one population, one health system, one era, or one dataset rarely generalise without qualification. Authors should explicitly address: To whom do these findings apply? Under what conditions might they not hold? What limits external validity? Overclaiming generalizability invites harsh editorial and reviewer pushback.

**12. Equity blindness.** Studies that report average effects without examining whether benefits (or harms) differ by sex, age, race/ethnicity, socioeconomic status, or geography are increasingly viewed as incomplete. Top journals expect — and in some cases require — consideration of differential effects. An intervention that works only in well-resourced settings is not the same as one that works everywhere.
### Reviewer-Side Pitfalls

These are pitfalls in the review process itself — mistakes you can make, not flaws in the manuscript.

**13. Declaring an analysis "missing" without checking supplementary materials.** Prediction models often report calibration, decision curves, and detailed subgroup analyses in supplementary appendices rather than the main text. Before stating that "no calibration was reported" or "sensitivity analyses are absent," read every supplementary file provided. A wrong declaration of a missing analysis damages review credibility and wastes revision cycles.

**14. Misidentifying which manuscript a supplement belongs to.** Supplement files sent in the same batch as a manuscript may belong to a different paper entirely. Always verify by checking the author names, title references, and journal citation in the supplement file — do not assume file associations from upload order.

**15. Failing to extract text from large or complex .docx manuscripts.** Large manuscripts with embedded tables, figures, and track changes can cause `python-docx` to time out. The robust fallback: `unzip` the `.docx` → parse `word/document.xml` with Python's `xml.etree.ElementTree`. This handles files of any size without memory issues. Do NOT give up on manuscript extraction because `read_file` returns a binary error.

## Verification Checklist

- [ ] **Supplementary materials fully reviewed BEFORE finalizing conclusions.** Read all figures, tables, and appendices. Verify which manuscript a supplement belongs to by checking author names and journal references in the file — do NOT assume file associations.
- [ ] Study type and claim type correctly identified
- [ ] All 10 review steps completed in order
- [ ] Fatal flaws explicitly flagged (or confirmed absent)
- [ ] At least 3 design alternatives provided
- [ ] All 3 reviewer perspectives simulated
- [ ] Score rubric applied consistently
- [ ] Output uses standard template from `templates/review-report.md`
- [ ] Causal language boundaries respected
- [ ] Safety and integrity boundaries checked
- [ ] Uncertainty and missing information explicitly noted
