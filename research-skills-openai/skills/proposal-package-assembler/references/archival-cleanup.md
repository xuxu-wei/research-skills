# Archival Cleanup (Proposal Pre-Packaging)

## Scope and ownership

Use this guide when a submission-guard report identifies proposal-body residue before packaging. The package assembler may summarize the findings but never performs cleanup. The orchestrator routes accepted actions through `proposal-refinement-controller` and one `proposal-drafter` writer.

Cleanup removes or functionally rewrites process residue without changing scientific meaning, methods, endpoints, evidence strength, novelty/impact claim strength, feasibility, or risk posture. Every saved change creates a new complete proposal version and must pass the normal action-validation, preservation, reassessment, and final-evaluation gates.

## Classify findings by function

Process residue should be removed when present:

- reviewer-response marks such as “回应 Review Panel”；
- version tags or version metadata inside the proposal body;
- internal workflow, panel-count, or revision-process references that carry no scientific meaning;
- stale cross-references created by an accepted removal or relocation.

The following forms require functional review, not automatic deletion or conversion:

- rhetorical questions or question-form headings;
- explanatory reader guides;
- terminology mappings or standalone definition aids;
- clinical or implementation scenarios.

Keep one of these forms when a binding format requires it or when it materially advances the target reader’s reasoning with less burden than a direct alternative. Otherwise condense, relocate, or replace it. Record the local function and observable acceptance criterion for every action.

## Workflow

### 1. Bind source and target

Record the source proposal’s `{artifact_id, version, path}`, the submission-guard finding IDs, protected-content register, and a new target proposal identity. Never overwrite the frozen source.

### 2. Plan changes in document order

Group actions by actual proposal section so locators remain reviewable. Include the authoritative `Assumptions, feasibility, and risks` location when affected. Do not create or expect a reader-facing `Unresolved Issues` section.

Each action should name its finding ID, locator, operation, protected meaning, intended reader effect, and acceptance criterion. A process-residue removal may be subtractive; a functional rewrite may replace wording but cannot make a substantive scientific choice.

### 3. Route editing through the writer contract

Give the writer only the normalized repair brief, current complete proposal, and protected-content register. Use the OpenAI/Codex file-editing mechanism available to the task—`apply_patch` for repository edits—and inspect the resulting diff after each bounded group of changes. Do not invoke operations that are absent from the current OpenAI/Codex runtime, and do not create the next version with an unregistered shell copy.

One writer may make sequential section passes, but it owns one complete target proposal. Record every executed or blocked action in the editorial action-execution artifact.

### 4. Check cross-references

After removing or relocating material, search the complete target for references to old headings, tables, sections, or process labels. Use repository text search (`rg -n` when available) against the target proposal and inspect every match; do not rely on remembered line numbers.

Typical checks include references to a removed terminology table, an old appendix title, a former section number, or a reader guide that points backward to deleted content.

### 5. Verify residue and functional exceptions

Verify that identified reviewer-response marks, version metadata, and non-substantive process references are absent. Search both Chinese and English variants where applicable.

Separately inspect remaining questions, reader guides, terminology aids, and scenarios. Their count need not be zero. Each retained instance must have a documented reader or binding-format function and must not displace decision-relevant argument, break progressive disclosure, or duplicate the authoritative assumptions/feasibility/risks location.

Confirm that:

- every included action is executed or explicitly blocked;
- no stale cross-reference remains;
- the target is a complete proposal;
- protected meanings and claim strength are unchanged;
- no version or review-process metadata was reintroduced into the body.

Only then freeze the target and run fresh preservation, narrative reassessment, language reassessment, and final scientific evaluation as required by the orchestrator.

### 6. Record lineage

Create the next registered proposal version through the normal drafter/refinement route. Write a revision delta that records the source and target logical identities, finding/action IDs, operations, blocked items, protected-content result, and whether any functional form was retained with justification. Do not use line-count change or residue counts as evidence of quality.

## Pitfalls

- **Stale cross-references:** a removed definition aid can leave later sections pointing to a dead target.
- **Over-cleaning:** a question, scenario, or terminology aid may be necessary for the stated reader or binding genre; judge its function rather than its form.
- **Under-cleaning:** version labels and reviewer-response language can survive in captions, tables, or risk descriptions.
- **Scientific drift:** a “cleanup” that changes a method, endpoint, assumption, feasibility claim, risk, or contribution belongs in scientific revision and restarts scientific review.
- **Unregistered copies:** every saved target must have a new logical identity, complete artifact-index row, and lineage to the frozen source.
