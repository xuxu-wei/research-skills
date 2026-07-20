# Handoff Validation

## Contents

Context to mapper; mapper to orchestrator/writer; writer to preflight or
editorial readiness; preflight/editorial readiness to writer; evaluator to
orchestrator; orchestrator to medical reviewer or assembler.

Use these checks before passing Idea workflow artifacts.

## Context to mapper

- Goal, intended output, domain, direction clarity, and proceed status exist.
- Unknown data/method/endpoint facts are explicit; assumptions are separated.
- Target-reader profile, prior-knowledge baseline, five-part reasoning chain,
  and gap type are present.

## Mapper to orchestrator and writer

- Evidence and Opportunity Maps exist or absence is justified.
- Direction value, confidence, and supported-direction signals are present.
- Scientific gap and novelty positioning are separate, and a reader-reasoning
  handoff is present.
- Material claims have readable labels, source locators, and limitations.
- The mapper does not send maps directly to `idea-evaluator`.

## Writer to preflight or editorial readiness

- Each Idea is one complete v3 dossier with all 15 sections, complete evidence
  chains, a Claim-Support table, references, node pointer, ledger, index entry,
  and complete logical references.
- No patch/delta is current and the writer has not scored or promoted the Idea.

## Preflight to writer

- Method facts, blockers, and repair directions are explicit.
- The preflight did not score novelty/impact or edit the dossier.
- Required repairs are incorporated into a new complete dossier before
  evaluation; the preflight report is never evaluator input.
- A `proceed_with_assumptions` handoff contains only bounded assumptions, each
  recorded once in the dossier's authoritative Assumptions subsection.

## Editorial readiness to writer

- Narrative and language reviewers were fresh and assessed the same complete
  current dossier with the reader handoff.
- Every critical or major finding and every included non-blocking finding maps
  to one complete normalized action; terminology actions include a locatable
  replacement or definition.
- The writer-brief validator passed with the narrative assessment, narrative
  plan, language assessment, and protected register supplied as
  orchestrator-only audit inputs; the register's `source_artifact` equals the
  current dossier, and an internal-consistency-only pass is not sufficient.
- Overlapping narrative and language actions have one compatible disposition;
  unresolved scientific conflicts route to clarification before writing.
- The repair writer receives only the current dossier, approved normalized
  writer brief, protected register, and output paths. It does not read either
  assessment report or the assessor repair plan, and writes one complete next
  dossier plus delta.
- The delta maps every frozen included repair item ID to text-grounded acceptance
  evidence; no included ID is omitted or added by the writer.
- Every element enumerated in each protected item is present at a cited revised
  dossier locator; a delta assertion or section-level topic is not evidence.
- When repair occurred, preservation returns `scientific_content_preserved` and
  fresh reassessment closes all major findings before evaluation.

## Evaluator to orchestrator

- Isolation is valid and `files_read` contains exactly the current dossier.
- `reviewed_dossier_ref`, `complete_dossier_confirmed`, and
  `dossier_only_input_confirmed` match the current node.
- Six scores, hard gates, evidence-chain/claim-support checks, readable findings
  with `title` and `dossier_locator`, decision, and limitations are present.
- Prior artifacts were hidden and source files were unchanged.
- `historical_identity_drift_assessed` is false; the orchestrator separately
  compares the current anchor with the prior sealed node state.

## Orchestrator to medical journal reviewer

- The current-version Idea evaluation is final for this loop, structurally
  valid, and sealed; the dossier is biomedical or clinical based on its own
  domain and study setting.
- The candidate journal-match brief binds the same dossier by artifact ID,
  version, and path; candidates are unranked and supported by current public
  scope/article-type sources.
- The brief records `matching_source_skill: idea-evaluator` and
  `materialized_by_skill: research-idea-orchestrator`. It contains no score,
  publication probability, evaluator-report reference, evaluator finding,
  evaluator decision, repair direction, limitation, or material derived from
  those evaluation fields.
- The fresh reviewer may read exactly the dossier and candidate brief and may
  write only one medical journal review report. The evaluator report and all
  earlier workflow artifacts remain unavailable.
- The report binds both logical references, lists exactly those two project
  files in `files_read`, confirms fresh isolation and evaluator-report
  invisibility, and does not request or persist a SHA or digest.

## Orchestrator to assembler

- Every displayed Idea links a current complete dossier with a qualifying
  evaluation of the same artifact ID/version/path.
- Every applicable biomedical or clinical Idea also links its current unscored
  candidate journal match and fresh medical journal review beside, not inside,
  the evaluator result. Non-applicability is explicit.
- Narrative and full-dossier language readiness links and unresolved editorial
  issues are visible.
- Lineage, ledger, fatal/blocking findings, and dissent are indexed.
- The portfolio links rather than rewrites dossier prose.
- Bounded exploration stops at `human_direction_selection_required` without
  ranking a winner or entering Proposal.
- A focused Proposal handoff candidate has all required adversarial reports and
  no unresolved blocking objection.
