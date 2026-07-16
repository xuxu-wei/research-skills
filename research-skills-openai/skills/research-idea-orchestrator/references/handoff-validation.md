# Handoff Validation

Use these checks before passing Idea workflow artifacts.

## Context to mapper

- Goal, intended output, domain, direction clarity, and proceed status exist.
- Unknown data/method/endpoint facts are explicit; assumptions are separated.

## Mapper to orchestrator and writer

- Evidence and Opportunity Maps exist or absence is justified.
- Direction value, confidence, and supported-direction signals are present.
- Material claims have readable labels, source locators, and limitations.
- The mapper does not send maps directly to `idea-evaluator`.

## Writer to preflight or evaluator

- Each Idea is one complete v3 dossier with all 15 sections, complete evidence
  chains, a Claim-Support table, references, node pointer, ledger, index entry,
  and matching digest.
- No patch/delta is current and the writer has not scored or promoted the Idea.
- The evaluator brief names exactly one allowed project file: the dossier.

## Preflight to writer

- Method facts, blockers, and repair directions are explicit.
- The preflight did not score novelty/impact or edit the dossier.
- Required repairs are incorporated into a new complete dossier before
  evaluation; the preflight report is never evaluator input.

## Evaluator to orchestrator

- Isolation is valid and `files_read` contains exactly the current dossier.
- `reviewed_dossier_digest`, `complete_dossier_confirmed`, and
  `dossier_only_input_confirmed` match the current node.
- Six scores, hard gates, evidence-chain/claim-support checks, readable findings
  with `title` and `dossier_locator`, decision, and limitations are present.
- Prior artifacts were hidden and source files were unchanged.
- `historical_identity_drift_assessed` is false; the orchestrator separately
  compares the current anchor with the prior sealed node state.

## Orchestrator to assembler

- Every displayed Idea links a current complete dossier with a qualifying
  evaluation of the same digest.
- Lineage, ledger, fatal/blocking findings, and dissent are indexed.
- The portfolio links rather than rewrites dossier prose.
- Bounded exploration stops at `human_direction_selection_required` without
  ranking a winner or entering Proposal.
- A focused Proposal handoff candidate has all required adversarial reports and
  no unresolved blocking objection.
