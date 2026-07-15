---
name: article-cover-letter
description: "Draft a source-bound Cover Letter and mechanical check for a qualifying Article or Perspective."
---

# article-cover-letter

## Purpose

Draft an editor-facing triage memo for a qualifying Article or Perspective. State the problem, knowledge delta or core argument, contribution type, outlet fit, and credibility without repeating the abstract or changing the source work.

This is a writer role. Its quality check is mechanical and does not replace independent `medical-journal-review` when that review is part of the workflow.

## Workflow Profile

The orchestrator must set exactly one:

```yaml
workflow_profile: article | perspective
```

- `article`: use the qualifying manuscript and contribution statement.
- `perspective`: use the qualifying Perspective and its frozen core argument.

Do not use this skill for a non-qualifying draft, a language-polishing request, or submission-package assembly.

## Input and Output Contract

```yaml
inputs:
  required:
    - workflow_profile
    - qualifying_main_artifact_ref
    - qualifying_main_artifact_digest
    - contribution_statement_or_core_argument
    - target_journal_or_outlet
  optional:
    - article_type
    - frontmatter
    - evidence_or_claim_ledger
    - verified_outlet_facts
    - disclosures
outputs:
  - versioned_cover_letter
  - versioned_cover_letter_quality_check
```

Freeze all inputs before drafting. Every factual or comparative claim must trace to the qualifying main artifact, allowed evidence, or a verified outlet fact. Mark missing disclosure facts as unresolved; do not invent them.

## File Scope

```yaml
article:
  may_write:
    - "11_cover-letter/cover-letter-vNNN.md"
    - "11_cover-letter/cover-letter-quality-check-vNNN.md"
perspective:
  may_write:
    - "08_cover-letter/cover-letter-vNNN.md"
    - "08_cover-letter/cover-letter-quality-check-vNNN.md"
must_not_write:
  - qualifying main artifact
  - workflow state or evaluation reports
  - final package directories
may_call: []
```

The writer never edits its source artifact and never writes an independent review report.

## Procedure

### 1. Validate the frozen basis

Confirm the source ID, version, path, digest, qualifying decision, target outlet, and profile. If the source is stale, incomplete, or not qualifying, stop with `cover_letter_blocked` and list the missing basis.

### 2. Build the editorial case

Read `references/cover-letter-principles.md`. Extract only source-supported statements for:

1. the important problem;
2. the current knowledge or argument gap;
3. what this work changes;
4. the contribution type and strongest credible evidence;
5. why the named outlet and audience fit;
6. relevant declarations and disclosures.

Do not overclaim novelty, impact, generalizability, causality, or journal fit.

### 3. Draft the letter

Use `templates/cover-letter.md` as a drafting aid. Prefer a short opening with the submission identity, a compact problem–delta–contribution argument, an outlet-fit paragraph, and a factual declaration close. Adapt the structure when the outlet requires a different form.

The letter must stand on its own but must not reproduce the abstract mechanically. Perspective letters should foreground the importance, timeliness, synthesis or argument contribution, and intended readership rather than implying original empirical results that the source does not contain.

### 4. Record the mechanical quality check

Write the matching versioned check:

```yaml
cover_letter_quality_check:
  workflow_profile: article | perspective
  source_artifact_id:
  source_version:
  source_digest:
  target_outlet:
  word_count:
  structure_complete: true | false
  target_outlet_matches: true | false
  problem_delta_fit_present: true | false
  repeats_abstract_mechanically: true | false
  unsupported_claims: []
  missing_disclosures: []
  inputs_sufficient: true | false
```

This check reports observable completeness only. Return both frozen artifacts to the orchestrator, which owns any independent review and downstream routing.

## Versioning and Staleness

- A changed qualifying main artifact, digest, target outlet, or core contribution makes the letter and its review stale.
- Any content change creates the next `vNNN` pair; never overwrite an older frozen pair.
- A Perspective final compositor may faithfully copy the frozen letter to `08_final/cover-letter.md`; all content changes must return here as a new version.

## Completion Check

Confirm profile and paths agree, the source is qualifying and digest-bound, problem/delta/fit are present, claims and outlet facts are traceable, disclosures are accurate or visibly unresolved, the letter is not an abstract copy, and the quality check contains no promotion decision.

## Conditional Resources

- Read `references/cover-letter-principles.md` while constructing the editorial case.
- Use `templates/cover-letter.md` only while drafting the versioned letter.
- Read `article-orchestrator/references/artifact-review-and-submission-contracts.md` when validating Article handoff or package references.
- Read `perspective-orchestrator/references/io-contracts.md` when validating Perspective handoff or final-copy references.
