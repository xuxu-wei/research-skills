# Downstream Handoff Rules

## General Rule

`research-context-builder` does not execute downstream tasks. It marks downstream needs so the orchestrator can route the workflow.

## Evidence / Opportunity Mapping

Mark `evidence_opportunity_mapping: required` when:

- the user asks to generate or refine ideas;
- novelty, guideline alignment, or evidence grounding matters;
- literature materials are provided;
- the task is clinical, biomedical, or rapidly changing;
- the context includes a broad direction rather than a mature idea.

Mark `optional` when the user only needs context normalization.

## Multi-Path Idea Generation

Mark `multi_path_idea_generation: required` when:

- the user requests new ideas;
- the input is a broad direction or problem space;
- existing ideas are too few or too vague.

Mark `optional` when the user provides a concrete raw idea.

## Methodology / Statistics Preflight

Mark `methodology_statistics_preflight: required` when:

- endpoint/metric status is unclear or partially clear;
- the data source is uncertain;
- the idea involves clinical, biomedical, observational, causal, predictive, experimental, or statistical analysis;
- method-data fit is likely to determine feasibility.

## Isolated Independent Evaluation

Mark `isolated_independent_evaluation: required` when:

- the user asks whether an idea is worth pursuing;
- the user asks for scoring, ranking, triage, promote/reject, reviewer objections, or feasibility judgment;
- an orchestrator needs a gate decision.

Evaluation must be assigned by the orchestrator to an isolated, independent `idea-evaluator` subagent. The context-building agent must not evaluate.

## Proposal-Orchestrator Triage

Mark `proposal_orchestrator_triage: required` when:

- the user asks to write a proposal, SAP, protocol, or grant;
- the user provides a promoted idea package;
- the user wants to determine proposal readiness.

If the idea is raw or vague, route through research-idea workflow before proposal drafting.
