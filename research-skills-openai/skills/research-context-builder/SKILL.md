---
name: research-context-builder
description: "Normalize a research direction, problem, evidence set, funding call, or data asset into a structured brief for idea generation."
---
# research-context-builder

## Role

Normalize a direction, raw Idea, problem, data/method asset, call, or literature
set into a Research Context Brief. Characterize how clearly the initial
direction is specified. Do not search evidence, judge value, generate Ideas,
run methods review, score, rank, or decide promotion.

## Procedure

1. Classify the input using `references/context-extraction-rules.md`.
2. Extract goal, output, target-reader profile and prior knowledge, research
   object, setting, data, methods, endpoint/metric, resources, constraints,
   known facts, and uncertainties using `references/context-brief-schema.md`.
3. Record the reader's needed `background -> current state -> gap ->
   significance -> rationale` reasoning chain and `gap_type`. This is a
   non-evaluative handoff: mark unknown links explicitly rather than inventing
   evidence, importance, or novelty.
4. Separate facts from assumptions; record confidence, impact if wrong, and
   whether user confirmation is required.
5. Set `direction_clarity`:
   - `clear`: primary question, object, and intended contribution are usable;
   - `underdefined`: one plausible direction exists but key scope is missing;
   - `ambiguous`: several materially different interpretations remain.
   This is descriptive context, not a value or novelty judgment.
6. Ask only essential questions. Otherwise proceed with explicit assumptions.
7. Mark downstream mapping, routing, dossier generation, preflight, independent
   evaluation, and Proposal-triage needs; return control to the orchestrator.
8. Validate the handoff against
   `research-idea-orchestrator/references/handoff-validation.md`.

## Evaluation Isolation

If asked whether an Idea is strong, novel, feasible, publishable, fundable, or
worth pursuing, only prepare context and mark independent evaluation required.
Never assign scores, findings, fatal flaws, or promotion decisions. Evaluation
belongs to a fresh `idea-evaluator` after a complete dossier exists.

## Outputs

- Use `templates/research-context-brief.md` for a valid brief.
- Use `templates/clarification-request.md` when an essential ambiguity blocks
  defensible mapping.
- Use `templates/context-insufficiency-report.md` when reliable normalization is
  impossible.

## Conditional Resources

- Read `references/context-brief-schema.md` when writing or validating the brief.
- Read `references/context-extraction-rules.md` during input extraction.
- Read `references/assumption-handling-rules.md` when facts are incomplete.
- Read `references/clarification-policy.md` before stopping for clarification.
- Read `references/downstream-handoff-rules.md` before returning route needs.
- Read `research-idea-orchestrator/references/artifact-contracts.md` for shared
  v3 fields.
- Read `research-idea-orchestrator/references/handoff-validation.md` before handoff.
- Use an output template only when producing its named artifact.

## Completion Check

Confirm `input_type: problem`, subtype, goal, output, object, data/method/endpoint,
target-reader profile and prior knowledge, all five reader-reasoning functions,
gap type, constraints, separated facts/assumptions, direction clarity with
rationale, proceed status, and downstream needs without evaluation.
