# Research Article Clue Extraction

A research article is a clue source, not direct proof of a research gap.

## Sections to Examine

1. Introduction: background framing, stated gap, motivation, unresolved need, limitation of existing work.
2. Discussion: interpretation, future work, limitations, unresolved questions.
3. Methods / Results: whether the clue depends on design limitations or limited generalizability.

## Clue Handling

For each clue:
- write the claim;
- identify where it appears;
- identify whether it is author-stated or evidence-supported;
- require external verification through reviews, guidelines, consensus, later studies, or citation graph.

If the article or supplied material alludes to another work without a complete
reference, infer possible single-work or series matches from the available
identity clues and record the result through `citation-record-contract.md`.
Never treat an ambiguous inference as a verified citation.

## Confidence Rule

Until externally verified, extracted article clues must be labeled `clue_only`, `unverified`, or low confidence.

Do not promote article-derived claims to high-confidence opportunities without corroboration.
