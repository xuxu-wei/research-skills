# DeepSearch Prompt Rules

When generating a prompt for the user to delegate to ChatGPT Deep Research, Gemini Deep Research, or equivalent external DeepSearch agents, these rules apply.

## Core Principles

1. **Mapper owns the question; DeepSearch owns the search.** The prompt defines what evidence is needed and why. It does not micromanage the search process — the DeepSearch agent is better at search execution than the mapper.
2. **Structure the search, don't script it.** Give phases and priorities, not a fixed query list. DeepSearch agents perform iterative, multi-turn exploration; the prompt should guide this exploration, not constrain it.
3. **Format drives quality.** A structured output format forces the DeepSearch agent to organize findings systematically rather than producing a free-form essay.
4. **Uncertainty annotation is mandatory.** The prompt must require the DeepSearch agent to label uncertainty, conflicting evidence, and evidence gaps.

## Prompt Structure Requirements

Every generated prompt must contain these sections:

### 1. Research Objective (研究目标)

- One or two sentences stating the core question.
- Context: why this question matters (domain significance, downstream use).
- Explicit statement: "你只需要做检索，不需要生成 idea，不需要评价研究价值，不需要写 proposal。"

### 2. Retrieval Strategy (检索规划)

Give a phased approach the DeepSearch agent should follow:

- **Phase 1 — Breadth scan (广度扫描)**：Identify the landscape — key papers, reviews, guidelines, consensus documents, major debates. Goal: understand what's known and who says what.
- **Phase 2 — Depth tracing (深度追踪)**：Follow citation trails, find the evidence behind major claims, identify primary sources. Goal: verify key claims, find contradictions, assess evidence strength.
- **Phase 3 — Gap filling (缺口补全)**：Target specific types (e.g., clinical trials for a clinical question, benchmarks for an ML question, non-English literature for a regional question). Goal: fill identified gaps from Phase 1-2.

For each phase, specify:
- Evidence types to prioritize (e.g., systematic reviews > RCTs > observational for clinical; arxiv preprints + conference proceedings for ML);
- Time window if relevant (e.g., last 5 years, or all time for foundational work);
- Language or geography constraints.

### 3. Content Requirements (内容要求)

A bullet list of exactly what information fields to extract for each relevant source. Examples:

- Study design / method type
- Population / sample / dataset
- Key findings and effect sizes
- Endpoints / metrics used
- Limitations as stated by authors
- Conflicts with other sources
- Evidence level (systematic review, RCT, observational, expert opinion, etc.)

### 4. Output Format (输出格式)

Provide a concrete output template. Prefer tables over prose. Example:

```
## 检索过程摘要
[简要描述每个阶段的检索过程、主要来源、遇到的困难]

## 核心证据表
| 主题/问题 | 证据摘要 | 证据类型 | 来源（含引用）| 证据强度 | 冲突/不确定性 |
|-----------|---------|---------|-------------|---------|-------------|

## 关键 gap 和争议
- [gap 1]
- [gap 2]

## 检索局限
- [未覆盖的领域/来源/语言]
- [时效性限制]
```

Use `templates/deepsearch-prompt-template.md` as the base and adapt per task.

### 5. Constraints (禁止事项)

- 不要生成 research idea；
- 不要评价研究价值或可行性；
- 不要写 proposal、SAP 或 protocol；
- 不要超出证据做推断；
- 不要把观点当作事实呈现；
- 不确定的信息必须标注不确定性。

## Domain-Specific Adjustments

### Clinical / Medical

- Require practice guidelines (if available for the domain) and systematic reviews.
- Require study design classification (RCT / cohort / case-control / case series / expert opinion).
- If safety or efficacy claims are involved, require adverse event / safety signal data.
- For Chinese clinical topics, require explicit search of CNKI / Wanfang / Sinomed mentions (even if DeepSearch agent may have variable access).

### AI / ML / Engineering

- Require benchmark results where applicable.
- Require conference venue + year for preprints.
- If model claims are involved, require training data, evaluation protocol, and reproducibility notes.

### Broad / Exploratory

- Use the three-phase approach with wider Phase 1 boundaries.
- Require the DeepSearch agent to identify sub-topics or sub-questions for further narrowing.

## Quality Gates

Before delivering the prompt to user, verify:

- [ ] All six sections present (Objective, Strategy, Content, Format, Constraints, Output)
- [ ] Strategy uses phased approach (not a flat list of queries)
- [ ] Output format is structured (tables preferred)
- [ ] Uncertainty annotation is required
- [ ] The prompt explicitly forbids idea generation, proposal writing, and evaluation
- [ ] Domain-specific adjustments applied where relevant

## Post-Report Processing

When user returns the DeepSearch report:

- Map the report's evidence table entries to Evidence Map format (`templates/evidence-map.md`).
- Extract gaps from the report's "关键 gap" section into Opportunity Map entries.
- All claims from the report that cannot be independently verified are labeled `deepsearch-derived` with the report as the sole source.
- Evidence limitations in the downstream handoff must note: DeepSearch agent type, any evidence types the report explicitly states it could not access, and the mapper's own assessment of the report's coverage against the original prompt.

## Level-Specific Adjustments

When generating DeepSearch prompts, apply the following adjustments based on the selected Exploration Level.

### Standard (S)

Use the default template without modification. Three-phase strategy (breadth → depth → gap fill) as defined in this document.

### Divergent (D)

- **Objective**: Remove tight scope boundaries. Frame the question as "what is the landscape around X?" rather than "what evidence supports Y for X?"
- **Phase 1 — Breadth**: Double the source types. Include adjacent fields explicitly. Add: "identify methods and paradigms from other fields that address structurally similar problems."
- **Phase 2 — Depth**: Select 5-8 threads to follow instead of 2-3. Include threads from adjacent fields.
- **Phase 3 — Gap fill**: Add a round for "unexpected discoveries" — re-scan with different keyword combinations, different databases, different perspectives.
- **Timeliness**: Relax to 10 years (unless domain moves faster). Include foundational work regardless of age.
- **Content requirements**: Add fields for: "methods that could transfer from other domains", "analogous problems in different fields", "emerging trends (even if unvalidated)".
- **Confidence labels**: Allow "speculative", "preliminary", and "low-confidence" more freely. Do not penalize for lack of direct evidence.

### Focused (F)

- **Objective**: Tighten the scope. Frame as "what is the strongest evidence for/against X in context Y?"
- **Strategy**: Single-stage targeted retrieval. Skip breadth scan and gap fill phases. Start with highest-quality sources and stop when sufficient evidence is found.
- **Sources**: Exclude preprints, conference abstracts, opinion pieces. Require peer-reviewed published work with DOI.
- **Timeliness**: Maximum 5 years (unless domain moves slower). Exclude foundational/classic work unless it directly supports a claim.
- **Content requirements**: Strip speculative content fields. Add: "for each claim, state evidence level (systematic review / RCT / observational / etc.) and direct relevance score."
- **Confidence labels**: Require "supported" or "likely" for inclusion. Mark anything uncertain as "excluded — insufficient evidence".
- **Output**: Shorter, denser report. 证据表 with fewer rows, higher per-row confidence.
