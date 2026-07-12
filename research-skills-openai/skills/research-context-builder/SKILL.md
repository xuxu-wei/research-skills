---
name: research-context-builder
description: "Normalize a research direction, problem, evidence set, funding call, or data asset into a structured brief for idea generation."
---
## 1. Overview

`research-context-builder` is the context preparation skill for the `research-idea` workflow. It converts broad research directions, raw ideas, clinical or practical problems, data assets, funding calls, literature materials, or mixed inputs into a Research Context Brief for downstream skills.

It answers one question: what is the current research context, what is known, what is assumed, and what must be clarified before downstream work proceeds?

This skill does not evaluate whether an idea is worth pursuing and does not generate research ideas.

## 2. When to Use

Use this skill when:

- the user provides a broad direction, raw idea, clinical problem, data asset, method asset, funding call, literature material, or mixed input;
- an orchestrator needs a Research Context Brief before evidence mapping, idea generation, preflight, or evaluation;
- user goal, intended output, available data, research object, endpoint/metric constraints, or practical limitations are unclear;
- scattered information must be normalized for downstream research skills.

Do not use this skill to:

- generate research ideas;
- search, judge, or synthesize evidence;
- score novelty, feasibility, impact, relevance, clarity, or completion;
- decide promote/reject;
- run methodology/statistics preflight;
- write a proposal, SAP, protocol, or grant application.

## 3. Operating Principles

1. Build context only. Do not score, rank, promote, reject, or judge whether an idea should proceed.
2. Do not replace evidence mapping. Literature search, guideline alignment, evidence confidence, and opportunity mapping belong to `research-opportunity-mapper`.
3. Do not replace methodology/statistics preflight. Endpoint/metric validity, data-method fit, and analysis feasibility belong to `methodology-statistics-preflight`.
4. Ask only necessary clarification questions. If missing information can be handled by explicit assumptions, proceed with assumptions.
5. Keep assumptions auditable. Record confidence, impact if wrong, and whether user confirmation is needed.
6. Protect evaluation isolation. If evaluation is requested, mark the downstream need and return control to the orchestrator so evaluation can be assigned to an isolated, independent `idea-evaluator` subagent.
7. Make the output useful for downstream skills. The Research Context Brief should support evidence mapping, idea generation, methodology/statistics preflight, and independent evaluation.

## 4. Workflow

### Phase 1 — Input Triage

Classify the input type using `references/context-extraction-rules.md`.

### Phase 2 — Context Extraction

Extract research context using `references/context-brief-schema.md` and `references/context-extraction-rules.md`.

### Phase 3 — Assumption Handling

Handle missing or ambiguous information using `references/assumption-handling-rules.md`.

### Phase 4 — Proceed Status Decision

Decide whether to proceed, proceed with assumptions, or stop for clarification using `references/clarification-policy.md`.

### Phase 5 — Downstream Handoff

Mark downstream needs using `references/downstream-handoff-rules.md`.

### Phase 6 — Handoff Validation

Before returning control to the orchestrator, check the brief against `research-idea-orchestrator/references/handoff-validation.md`. Use the shared artifact contract names when writing machine-readable handoff notes.

## 5. Evaluation Isolation Rule

This skill must not perform evaluation. If the user asks whether an idea is strong, worth pursuing, publishable, fundable, novel, feasible, or ready to promote, this skill may only:

- prepare the Research Context Brief;
- mark the need for downstream evaluation;
- return control to `research-idea-orchestrator`;
- require the orchestrator to assign evaluation to an isolated, independent `idea-evaluator` subagent.

Prohibited actions:

- assigning six-dimension scores;
- deciding promote/reject;
- writing reviewer objections or fatal flaw judgments;
- allowing the same agent that built context or generated an idea to evaluate that idea.

## 6. Output

Default output: Research Context Brief using `templates/research-context-brief.md`.

If clarification is required: clarification request using `templates/clarification-request.md`.

If the input is too insufficient for a reliable context: context insufficiency report using `templates/context-insufficiency-report.md`.

## 7. Common Pitfalls

- Quietly evaluating an idea.
- Treating evidence quality or opportunity gaps as context facts.
- Losing assumptions needed to interpret later decisions.

## 8. Verification Checklist

- Input type has been classified.
- User goal, intended output, research object, available data, available methods, and constraints have been extracted when available.
- Endpoint/metric constraints have been captured or marked as unclear.
- Known facts, assumptions, and uncertainties are separated.
- Proceed status is one of: `proceed`, `proceed_with_assumptions`, or `clarification_stop`.
- Clarification questions are limited to essential items.
- Downstream needs are marked.

## References

- `research-idea-orchestrator/references/artifact-contracts.md`：定义 Research Context Brief 的统一字段命名、schema version 和跨 skill 传递约定。
- `research-idea-orchestrator/references/handoff-validation.md`：定义 context brief 交给 mapper、generator、preflight 和 evaluator 前的最小校验规则。
- Read `references/context-brief-schema.md` when its named guidance or contract applies: ：定义 context brief 的结构字段、字段解释和输出格式要求。
- Read `references/context-extraction-rules.md` when its named guidance or contract applies: ：规范从用户输入中提取研究领域、目标、对象、数据、方法、endpoint 和约束的规则。
- Read `references/clarification-policy.md` when its named guidance or contract applies: ：定义何时需要向用户澄清、如何生成最小必要的澄清问题及停等条件。
- Read `references/assumption-handling-rules.md` when its named guidance or contract applies: ：规范合理假设的生成边界、标记方式及与 confirmed facts 的区分规则。
- Read `references/downstream-handoff-rules.md` when its named guidance or contract applies: ：定义 context brief 如何交给下游 skill（evidence mapper、idea generator、proposal workflow）及 handoff 材料要求。
- Use `templates/research-context-brief.md` when producing its named artifact: ：Research Context Brief 的输出模板。
- Use `templates/clarification-request.md` when producing its named artifact: ：向用户请求澄清时的输出模板。
- Use `templates/context-insufficiency-report.md` when producing its named artifact: ：输入材料不足时的问题说明报告模板。
