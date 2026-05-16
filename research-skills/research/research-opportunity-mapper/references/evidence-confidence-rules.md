# Evidence Confidence Rules

Use this file to assign evidence confidence, novelty verification, and guideline alignment.

## Confidence Labels

### high
Multiple reliable sources support the claim, including at least one high-priority source such as a guideline, consensus statement, systematic review, or strong repeated finding.

### moderate
Multiple sources support the claim, but evidence is indirect, heterogeneous, or partially disputed.

### low
Evidence is sparse, indirect, dated, single-domain, small-scale, or methodologically limited.

### speculative
The claim mainly comes from a single paper, author interpretation, emerging preprint, commentary, or unvalidated inference.

### not_verified
The claim has not been checked against accessible evidence or user-provided material.

## Novelty Verification

Novelty must not be asserted from one research article alone, one preprint alone, absence of easily accessible search results, inaccessible Chinese databases, or memory.

Use:
- `verified`
- `partially_verified`
- `unverified`
- `disputed`

## Guideline Alignment

For clinical/medical topics:
- `aligned`: consistent with current guideline/consensus evidence.
- `partially_aligned`: compatible but not directly addressed.
- `conflicting`: appears inconsistent with guideline or consensus evidence.
- `not_applicable`: not a clinical/guideline-relevant claim.
- `unverified`: no retrieved or user-provided evidence.

## Clinical Evidence Rule

Clinical/medical ideas require retrieved evidence or user-provided evidence before making novelty or guideline-alignment claims. If neither is available, novelty and guideline alignment must remain `unverified`.

## Contradictions

When sources conflict, record both positions, prefer newer high-quality evidence only when appropriate, and label opportunity confidence no higher than `moderate` unless conflict is resolved.
