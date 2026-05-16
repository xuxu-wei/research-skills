---
name: article-cover-letter
description: Draft and evaluate journal cover letters for research-article submissions as editorial triage memos. Builds the cover letter from manuscript-level artifacts without modifying the manuscript or frontmatter. For biomedical manuscripts, delegates cover-letter-only review to medical-journal-review and records the estimated article tier.
version: 0.1.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-article, cover-letter, journal-fit, editorial-triage, submission]
    related_skills:
      - article-orchestrator
      - article-frontmatter-drafter
      - article-submission-compositor
      - medical-journal-review
---

# article-cover-letter

## Purpose

Draft the journal cover letter as an editorial triage memo: a concise case for why the manuscript deserves editorial attention, why it fits the target journal, what knowledge-state change it offers, and what disclosures the editor must know.

This skill does NOT draft abstracts, titles, key points, manuscript text, reviewer responses, or submission packages. It writes and evaluates cover letter artifacts only.

## Core Rules

- Write the editorial case, not a second abstract.
- Lead with the field's unresolved issue and the manuscript's delta.
- State the contribution type: evidence-strengthening, conceptual reframing, practice decision, measurement advance, boundary condition, evidence organization, or research enablement.
- Keep the letter concise: one page; target 350-500 English words unless journal instructions differ.
- Include disclosures and credibility signals: preprint, related submissions, prior communication, conflicts, ethics, author approval, suggested/excluded reviewers if applicable.
- Do not introduce claims not present in the manuscript, blueprint, evaluation, or panel report.
- For biomedical manuscripts, after drafting, run an independent cover-letter-only review through `medical-journal-review` in delegate/subagent style when available.

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - manuscript_draft
    - article_blueprint (contribution_statement, journal_adapter, reviewer_risk_preview)
    - literature_grounding_report
    - evaluation_report
    - panel_report (optional)
    - frontmatter (optional, for consistency only)
  required_outputs:
    - cover_letter
    - cover_letter_quality_check
    - medical_cover_letter_review (for biomedical manuscripts)
  may_read:
    - "03_literature/**"
    - "04_blueprint/**"
    - "06_drafts/**"
    - "08_evaluations/**"
    - "10_panel/**"
    - "11_frontmatter/**"
  may_write:
    - "11_cover-letter/cover-letter.md"
    - "11_cover-letter/cover-letter-quality-check.md"
    - "11_cover-letter/medical-journal-cover-letter-review.md"
  must_not_write:
    - "06_drafts/**"
    - "11_frontmatter/**"
    - "12_package/**"
  may_call:
    - medical-journal-review
  must_not_call:
    - article-drafter
    - article-evaluator
  failure_modes:
    - "contribution delta unclear -> request article-architect clarification via orchestrator"
    - "journal fit unavailable -> draft generic fit cautiously and cap confidence at low"
    - "biomedical review delegate unavailable -> perform no substitute manuscript review; mark cover_letter_review_status: delegate_unavailable"
  escalation_route: "article-orchestrator"
```

## Procedure

### Step 1: Confirm Scope and Inputs

Load the manuscript title, target journal, article type, contribution statement, journal adapter, literature grounding, evaluation decision, and known disclosures. Confirm the cover letter can be written without inventing facts.

### Step 2: Build the Editorial Case

Use `references/cover-letter-principles.md` to identify:

- `problem`: the specific unresolved issue in the field
- `delta`: what changes after this manuscript exists
- `innovation_type`: incremental improvement or 0-to-1 reframing/enabling
- `journal_fit`: why this journal's readers need this delta
- `credibility`: prior work, design strength, evidence boundary, or research-program continuity
- `disclosures`: editor-relevant submission facts

### Step 3: Draft the Cover Letter

Use `templates/cover-letter.md`. Default structure:

1. Submission statement and problem positioning
2. Knowledge delta and contribution type
3. Journal fit and readership value
4. Credibility, boundaries, and disclosures

### Step 4: Self-Check

Produce `cover-letter-quality-check.md`:

```yaml
cover_letter_quality_check:
  repeats_abstract: yes | no
  delta_visible: strong | adequate | weak
  journal_fit_specificity: high | medium | low
  novelty_claim_supported: yes | no | not_applicable
  evidence_boundaries_clear: yes | partial | no
  disclosures_complete: yes | partial | no
  unsupported_claims: []
  recommended_status: ready | revise | blocked
```

### Step 5: Biomedical Independent Review

If the manuscript is biomedical, clinical, public health, translational, health policy, medical AI, epidemiology, diagnostic, prognostic, or life-science medical journal work:

1. Use a fresh delegate/subagent when available.
2. Invoke `medical-journal-review` with a strict cover-letter-only brief.
3. Provide only `11_cover-letter/cover-letter.md` content, not the manuscript, blueprint, context, evaluation, or panel report.
4. Ask the reviewer to judge only the cover letter as an editorial triage document and to explicitly estimate the apparent article tier from the cover letter alone.

Required review output:

```yaml
medical_cover_letter_review:
  review_scope: cover_letter_only
  apparent_article_tier: top_general_medical | top_specialty | solid_specialty | incremental_specialty | low_competitiveness | cannot_judge
  tier_confidence: high | medium | low
  editorial_case_strength: strong | adequate | weak
  main_reason_for_tier: ""
  missing_or_unclear_editorial_value: []
  overclaim_or_fit_risks: []
  revision_recommendations: []
```

If true delegation is unavailable, record `cover_letter_review_status: delegate_unavailable` and cap cover-letter review confidence at low. Do not replace this with a full manuscript review.

## Output

- `11_cover-letter/cover-letter.md`
- `11_cover-letter/cover-letter-quality-check.md`
- `11_cover-letter/medical-journal-cover-letter-review.md` for biomedical manuscripts

## Pitfalls

- Do not repeat the abstract or list methods/results mechanically.
- Do not praise the journal generically.
- Do not use "first", "novel", or "unique" unless literature grounding supports it.
- Do not hide limitations or disclosures the editor needs.
- Do not provide the manuscript to `medical-journal-review` for the cover-letter-only check.

## Verification

- Cover letter is one page or journal-compliant.
- Problem, delta, journal fit, credibility, and disclosure are all present.
- No unsupported novelty or importance claims.
- Biomedical manuscripts have a cover-letter-only `medical-journal-review` output or an explicit delegate-unavailable limitation.
- The apparent article tier is stated when biomedical review is performed.

## References

- `references/cover-letter-principles.md`: Editorial triage memo principles and contribution patterns.
- `templates/cover-letter.md`: Drafting template.
- `article-orchestrator/references/artifact-contracts.md`: Canonical cover letter and submission package contracts.
- `article-orchestrator/references/artifact-naming-and-directory-rules.md`: Directory and naming conventions.
