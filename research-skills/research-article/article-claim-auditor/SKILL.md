---
name: article-claim-auditor
description: Audit every claim in the manuscript against its evidence source. Verify evidence support, inference validity, wording appropriateness, and boundary clarity. Determine whether claims must be retained, strengthened, downscaled, moved, or removed.
version: 0.1.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-article, claim, audit, evidence, inference, overclaim]
    related_skills:
      - article-orchestrator
      - article-architect
      - article-drafter
      - article-evaluator
---

# article-claim-auditor

## Purpose

Audit every claim in the manuscript against its evidence source. Answer for each claim: is the evidence sufficient? Is the inference valid? Is the wording appropriate to the evidence strength? Are the boundaries clear?

This skill does NOT evaluate overall manuscript quality (that is `article-evaluator`'s job), rewrite claims (that is `article-drafter`'s job via refinement), or audit methods (that is `article-methods-statistics-auditor`'s job).

## Core Rules

- Audit claim by claim. No summary judgment.
- Evidence sufficiency is the primary criterion. A well-written claim with no evidence is still unsupported.
- Downscaling is the default remedy for overclaim — removal is for unsalvageable claims.
- Distinguish between "evidence exists but is not in the manuscript" and "evidence does not exist."
- The claim audit is a gate: `blocked` means do not proceed to evaluation. If the fatal overclaim is fixable by downscaling, removal, or moving the claim, route to refinement and re-audit; if unfixable, stop.
- Execute as an isolated subagent via `delegate_task`. Do not depend on parent session context.

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - manuscript_draft
    - article_blueprint (claim_evidence_matrix, EPL)
    - article_context_brief
  required_outputs:
    - claim_audit_report
  may_read:
    - "06_drafts/**"
    - "04_blueprint/**"
    - "02_context/**"
  may_write:
    - "07_claim-audit/claim-audit-v*.md"
  must_not_read:
    - "08_evaluations/**"
    - "10_panel/**"
  must_not_write:
    - "06_drafts/**"
    - "04_blueprint/**"
  may_call: []
  must_not_call:
    - article-evaluator
    - article-drafter
  failure_modes:
    - "manuscript claims cannot be matched to CEM claims → flag as orphan_claim, audit independently"
    - "EPL verification_status = missing for a primary claim → flag as evidence_support: absent"
  escalation_route: "article-orchestrator"
```

## Procedure

### Step 1: Extract Claims

Extract all claims from the manuscript. Match each to the Claim-Evidence Matrix from the blueprint. Flag claims present in manuscript but absent from CEM as `orphan_claim`. Flag CEM claims absent from manuscript as `missing_from_manuscript`.

### Step 2: Audit Each Claim

For each claim, assess four dimensions:

```yaml
claim_audit:
  - claim_id: "C001"
    claim_text: ""
    section: Introduction | Methods | Results | Discussion
    evidence_support: sufficient | partial | absent | not_applicable
    inference_validity: valid | borderline | invalid | cannot_assess
    wording_appropriateness: appropriate | overclaimed | underclaimed | vague
    boundary_clarity: clear | unclear | missing
    evidence_source_mapped: true | false   # traceable to EPL entry
    risk_level: low | medium | high | critical
```

### Step 3: Determine Claim Action

For each claim with issues, determine the action:

```yaml
claim_action:
  retain:         # claim is well-supported, keep as is
  strengthen:     # evidence supports stronger wording
  downscale:      # wording exceeds evidence → soften
  remove:         # claim is unsupported and cannot be salvaged
  move_to_discussion:     # claim is interpretive, not a result
  move_to_supplementary:  # claim is valid but secondary
```

### Step 4: Identify Fatal Overclaims

A claim is a **fatal overclaim** when:
- Primary claim has `evidence_support: absent`
- Causal language used for observational design without justification
- Claim directly contradicts the evidence provided
- Claim would mislead a reader about the study's contribution

Fatal overclaims are `blocked` — manuscript must be fixed before evaluation.

Classify every fatal overclaim by fixability:

```yaml
fatal_overclaim:
  fixability: fixable_by_downscaling | fixable_by_removal | fixable_by_relocation | unfixable
  route: refinement_then_reaudit | stop
  rationale: ""
```

Use `unfixable` only when the primary evidence is absent, the evidence contradicts the claim, the required downscaling would remove the manuscript's core contribution, or the author refuses required downscaling.

### Step 5: Determine Overall Recommendation

```yaml
recommendation:
  pass                    # all claims adequately supported
  downscale_and_proceed   # non-fatal overclaims identified, downscaling needed
  revise_and_reaudit      # claims need revision then re-audit
  blocked                 # fatal overclaims present, must fix before proceeding
```

## Route Decision

| Recommendation | Route |
|---------------|-------|
| `pass` | Proceed to evaluation |
| `downscale_and_proceed` | Route to refinement (claim downscaling), then evaluate |
| `revise_and_reaudit` | Route to refinement, then re-audit |
| `blocked` fixable | Route to refinement, then re-audit. |
| `blocked` unfixable | **Stop**. Writing cannot responsibly repair the claim. |

## Output

Write `07_claim-audit/claim-audit-vNNN.md` containing the full audit with per-claim assessments, claim actions, fatal overclaim list, and overall recommendation.

## Pitfalls

- Do not audit only primary claims. All claims must be checked.
- Do not confuse "claim is modest" with "claim is well-supported." Check the evidence.
- Do not downscale claims that are already appropriately cautious.
- Do not pass a manuscript with fatal overclaims just to keep the workflow moving.
- Do not merge this with the evaluator. Claim audit is claim-level; evaluation is manuscript-level.

## Verification

- Every claim in the manuscript has an audit entry
- Every claim has `evidence_support`, `inference_validity`, `wording_appropriateness`, and `boundary_clarity` assessed
- Every issue has a corresponding `claim_action`
- Fatal overclaims are explicitly listed and block progression
- Orphan claims and missing claims are flagged
- Recommendation matches the most severe unresolved finding

## References

- `references/claim-audit-rubric.md`: Detailed scoring anchors for evidence support, inference validity, wording, and boundary clarity.
- `references/overclaim-patterns.md`: Common overclaim patterns by study type and how to detect them.
- `article-orchestrator/references/artifact-contracts.md`: Canonical claim audit report schema.
- `article-orchestrator/references/evidence-provenance-ledger-schema.md`: EPL usage for claim-audit verification.
- `article-orchestrator/references/handoff-validation.md`: Claim audit → evaluator handoff gates.
