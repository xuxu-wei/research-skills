---
name: research-opportunity-mapper
description: 当研究方向、raw idea、proposal context、funding call、文献材料、指南、共识、research article、临床/实践问题或数据机会需要被证据化和机会化时使用。本 skill 负责检索、证据筛选、证据验证、Evidence Map 和 Opportunity Map；不生成 idea，不评价 idea/proposal/SAP，不写 proposal/SAP/protocol。
version: 2.0.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research, evidence-mapping, opportunity-mapping, retrieval, source-verification, deepsearch]
    category: research
    related_skills:
      - arxiv
      - pubmed
      - research-paper-writing
      - llm-wiki
      - research-context-builder
      - proposal-context-brief-builder
      - multi-path-idea-generator
      - methodology-statistics-preflight
      - idea-evaluator
      - proposal-evaluator
---

# Research Opportunity Mapper

## Purpose

`research-opportunity-mapper` 是通用 evidence mapping skill。它接收用户材料、研究主题、Research Context Brief、Proposal Context Brief、funding call、数据机会或已有 Evidence Map，完成必要检索和证据验证，并输出下游可用的 evidence / opportunity artifacts。

检索职责属于本 skill。Orchestrator 只传入任务范围、用户材料、目标产出、约束和已有证据；不直接调用检索工具替代 mapper。

本 skill 不生成候选 idea，不给 idea/proposal/SAP 打分，不写正文，不做 clinical decision support，也不把 evidence mapping 扩展成 systematic review 或 meta-analysis。

## When to Use

使用本 skill：

- idea generation 需要 evidence / opportunity grounding；
- proposal readiness、drafting 或 evaluation 依赖 novelty、gap、guideline alignment、funding-call fit 或 evidence strength；
- 用户提供 research article、综述、指南、共识、funding call、数据机会或宽泛主题；
- 临床、政策、高风险或前沿问题需要验证来源；
- 下游 evaluator 或 drafter 需要 evidence packet。

不要使用本 skill 处理单纯写作、评分、SAP 撰写、完整系统综述、meta-analysis 或临床建议。

## Core Rules

- 用户材料优先；单篇 research article 只能作为 clue source，不是 gap proof。
- 检索必须与任务范围匹配；证据不足、冲突、过期或高风险时才扩大检索。
- 可复用已有 Evidence Map 时不要重复检索。
- Evidence Map 记录证据；Opportunity Map 记录由证据支持或限制的研究机会。
- 无法验证的 novelty、gap 或 guideline alignment 必须标为 `unverified` 或低置信。
- 检索失败、访问限制或工具不可用必须写入 evidence limitation；不得凭记忆补证据。
- 任何时候不替用户做 DeepSearch 检索——DeepSearch 只在用户选择路径 B 时由用户操作。

---

## Workflow: Strategy and Route Selection (必须首先执行)

本 skill 启动后，**必须先向用户提出探索策略和检索路径选择**，不可默认选取。

### 呈现格式

向用户一次性呈现以下内容（用中文）：

```
## 探索策略与检索路径

请选择探索策略和检索路径。可直接用简写（如 SA、DB、FA）。

### 探索策略

**Standard (S) — 标准探索**
沿用当前策略。检索范围与方向自然匹配，允许边缘发现但不刻意拓宽。
机会类型以 gap、method、data 为主。如不确定，选此。

**Divergent (D) — 发散探索**
更大范围搜索，纳入相邻领域、不同方法角度、可类比的研究范式。
机会类型包括 analogy、tension、reframing、trend 等 speculative 类型。
置信度门槛更低，输出的 opportunity 数量更多、更 speculative。

**Focused (F) — 聚焦验证**
严格检索直接相关证据，每条 opportunity 需有证据支撑。
置信度门槛更高，opportunity 数量更少、更 solid。

### 检索路径

**Path A — 我直接规划并执行检索**
我会展示《检索规划路径》，你确认后执行。

**Path B — 我提供提示词，你委托外部 DeepSearch**
我生成专业提示词，你复制到 ChatGPT/Gemini 等执行，返回报告后我完成 mapping。

### 简写输入

| 简写 | 含义 | 简写 | 含义 |
|------|------|------|------|
| SA | Standard + Path A | SB | Standard + Path B |
| DA | Divergent + Path A | DB | Divergent + Path B |
| FA | Focused + Path A | FB | Focused + Path B |

也可输入 "Standard, A"、"Divergent, B" 等。如只输入 "S"/"D"/"F"，我会追问路径。

### 默认行为

如用户说"自主决定"/"你来定"/"默认" → 自动选择 **SA（Standard + Path A）**。
```

### 选择后执行

用户选择后，按 `references/exploration-strategy-rules.md` 加载对应策略参数（检索路由规则、opportunity 类型偏好、置信度阈值、DeepSearch 提示词调整），然后进入对应路径的 workflow。

### 模式切换

一次 session 内，如用户对输出不满意：

- "太窄了，换个更发散的模式" → 切换到 Divergent，基于已有 Evidence Map 扩大 opportunity 提取，不重新检索
- "太多了，帮我聚焦" → 切换到 Focused，过滤 opportunities 至 core types，收紧置信度
- 如用户要求重新检索，则按新模式完整重跑

---

## Path A: Direct Retrieval Workflow

### A1. Intake

识别输入类型、目标产出、领域边界、用户约束、已有 evidence artifacts。

### A2. Retrieval Planning

向用户展示《检索规划路径》，至少包含：

- 每轮检索的查询策略（query / MeSH / 关键词组合）；
- 目标来源及路由理由（按当前 Exploration Level 对应的路由规则文件：Standard → `references/search-routing-rules.md`，Divergent → `references/divergent-search-routing.md`，Focused → `references/focused-search-routing.md`）；
- 检索深度（targeted / expanded / stop）；
- 优先级和顺序。

用户确认后执行。如用户要求调整，修改后重新展示。

### A3. Retrieve or Reuse

复用有效 Evidence Map，或按规划调用合适检索来源/技能（`arxiv`、`pubmed`、官方来源、用户提供 wiki 等）。

详细规则见当前 Exploration Level 对应的路由规则文件。Standard 模式下行为与之前完全一致。

### A4. Triage Sources

按相关性、权威性、时效性、研究类型和冲突状态筛选来源。

### A5. Verify Claims

标注 supported、weak、conflicting、single-source、unverified、access-limited。详细规则见 `references/evidence-confidence-rules.md`。

### A6. Map Opportunities

按当前 Exploration Level 提取 opportunity：

- Standard：以 core types 为主（gap、method、data、metric 等）；exploration types 仅在证据自然支持时出现。
- Divergent：core types + exploration types（analogy、cross-domain、tension、trend、reframing、wildcard）；数量更多、标注更 speculative。
- Focused：仅 core types；要求每条 opportunity 有直接证据支撑。

机会分类和置信度规则见 `references/opportunity-type-taxonomy.md` 和 `references/exploration-strategy-rules.md`。

### A7. Handoff

生成 Evidence Map、Opportunity Map、Evidence Limitations、Handoff Notes，交给下游。

---

## Path B: DeepSearch Delegation Workflow

### B1. Intake

同 Path A1。额外记录：

- 用户的目标 Agent（ChatGPT / Gemini / 其他）及其已知能力边界；
- 用户是否已有该 Agent 的使用经验或偏好格式；
- 检索是否需要访问特定付费/登录源（如果 DeepSearch Agent 有权限）。

### B2. 生成 DeepSearch 提示词

按 `references/deepsearch-prompt-rules.md` 和 `templates/deepsearch-prompt-template.md` 生成提示词。根据 Exploration Level 调整：

- **Standard**：使用默认模板，三阶段检索策略。
- **Divergent**：Phase 1 拓宽检索范围至相邻领域，降低时效性限制，增加跨领域来源要求。提示词中增加 exploration types 对应的内容提取要求。
- **Focused**：缩减至单阶段 targeted retrieval，提高时效性要求（默认 ≤5 年），增加验证性要求（每项声明需标注证据等级）。

详细调整规则见 `references/deepsearch-prompt-rules.md` 的 Level-specific adjustments 章节。

提示词必须包含以下部分：

1. **任务目标**：要回答什么研究问题、为什么重要；
2. **检索规划**：分阶段检索策略、每阶段的关注重点（按 Level 调整广度和深度）；
3. **内容要求**：证据类型、来源优先级、时效性要求、地域/语言要求、需要提取的具体信息字段（按 Level 调整字段范围）；
4. **格式要求**：输出结构、引用格式、不确定性的标注方式；
5. **禁止事项**：不生成 idea、不评价质量、不写 proposal、不超出检索范围做推断；
6. **输出要求**：结构化报告，含检索过程摘要、核心发现、证据表、冲突或空白标注。

提示词应当：
- 把 mapper 的信息需求翻译为 DeepSearch Agent 可执行的检索指令；
- 足够详细以避免 Agent 自由发挥；
- 明确区分「检索报告」和「解读/建议」的边界。

### B3. 交付提示词并等待

将提示词交付用户，附简要使用说明。**进入等待状态**，不得自行启动检索或补充任何证据。

等待期间可以：
- 提示用户注意报告中需要标注的不确定性；
- 提醒用户返回报告时附带检索过程摘要（如可用）。

### B4. 接收并处理 DeepSearch 报告

用户返回报告后：

1. **检查完整性**：报告中是否覆盖了提示词要求的各类证据和检索阶段；
2. **标记缺口**：报告缺失的证据类型或检索阶段记录为 evidence limitation，不自行补充；
3. **区分来源**：标注报告中的证据来源类型（DeepSearch Agent 检索结果 vs Agent 自身解读），不能直接验证的来源标为 `unverified (deepsearch)`；
4. **提取可映射内容**：从报告中提取证据、gap、冲突、方法线索、数据线索、共识和争议。

### B5. 构建 Evidence Map

基于 DeepSearch 报告构建 Evidence Map（格式同 Path A）。使用 `templates/evidence-map.md` 和 `references/evidence-map-schema.md`。

与 Path A 的区别：
- 来源置信度标注为 `deepsearch-derived` 并附加报告中的检索过程摘要；
- 报告中无法验证的声明标为 `unverified (deepsearch)`；
- 不自行补充报告之外的检索结果。

### B6. 构建 Opportunity Map

基于 DeepSearch 报告中的 evidence 和 gap 构建 Opportunity Map。使用 `templates/opportunity-map.md`、`references/opportunity-map-schema.md` 和 `references/opportunity-type-taxonomy.md`。

### B7. Handoff

同 Path A7。额外在 Evidence Limitations 中记录：
- DeepSearch Agent 类型和提示词版本；
- 报告中未覆盖的证据类型；
- 报告中不可验证的声明数量和类型；
- 是否需要 Path A 补充检索（如报告质量不足）。

---

## Default Outputs

默认只输出会被下游使用或直接交付用户的内容：

- **Evidence Map**：供 `multi-path-idea-generator`、`idea-evaluator`、`proposal-readiness-triage`、`proposal-evaluator` 使用。
- **Opportunity Map**：供 `multi-path-idea-generator`、`idea-portfolio-assembler`、`proposal-context-brief-builder` 使用。
- **Evidence Limitations**：供 evaluator、drafter、readiness triage 防止过度声明。
- **Handoff Notes**：供 orchestrator 决定 next skill。

## Conditional Outputs

仅在触发时输出：

- **Retrieval/Search Log**：Path A 的检索过程摘要（复用判断、检索失败、争议/高风险场景或用户要求审计时）。
- **Source Verification Log**：来源多、冲突、高风险或用户要求可追踪时。
- **Evidence Insufficiency Report**：证据不足导致无法可靠 mapping 或阻断下游判断时。
- **DeepSearch Prompt**：Path B 的选择结果，作为交付物。

不要把条件输出作为默认 artifact。

## Output Format Convention

**所有面向用户的 Evidence Map、Opportunity Map、Evidence Limitations 和 Handoff Notes 必须为人类可读的 `.md` 文档。** 仅当 orchestrator 需要 agent-to-agent state 传递时，才以 `.yaml` 格式保存中间文件——交付用户前必须转换为 `.md` 并清理 `.yaml`。

文件命名遵循编号+描述惯例（如 `02-evidence-map.md`、`02b-evidence-limitations.md`、`03-opportunity-map.md`）。

## Common Pitfalls

### P1: delegate_task timeout on broad multi-direction searches

When mapping evidence across 4+ independent directions, a single `delegate_task` subagent may time out because each direction requires serial PubMed/arXiv/S2 calls with rate-limit delays. The accumulated latency can exceed the timeout budget (currently configured at 2700s in `delegation.child_timeout_seconds` on this system).

**Remedy**: For broad evidence mapping, use focused, parallel `terminal` calls — one per direction — with a standalone Python script (see `scripts/evidence_search.py`) rather than a single heavy subagent. Reserve `delegate_task` for narrow, well-scoped retrieval tasks (1–2 directions).

### P2: inline Python f-string escaping in shell -c

Embedding Python with f-strings inside `terminal("... -c '...'")` or `execute_code` frequently fails due to nested quote conflicts (`"`, `'`, `{`, `}`). The escaping required to make it work is fragile and error-prone.

**Remedy**: Write Python to a `.py` file first, then execute the file with `terminal("python3 scripts/foo.py")`. Never embed non-trivial Python directly in a `-c` argument.

### P3: arXiv keyword searches lack domain filtering

Broad arXiv queries like `all:causal+inference+AND+all:dynamical+system` return results dominated by quantum physics, condensed matter, and hep-th papers — drowning out the few relevant stat.ML or math.OC results.

**Remedy**: Always add `cat:` filters when searching arXiv for methodology papers. For statistical/ML work, use `cat:stat.ML OR cat:cs.LG OR cat:stat.ME`. For control theory, use `cat:math.OC OR cat:cs.SY OR cat:eess.SY`.

## Strategy and Path Decision Log

无论用户选择哪种策略和路径，在 Handoff Notes 中记录：
- 选择的 Exploration Level（S / D / F）及理由；
- 选择的路径（A 或 B）及理由；
- 若用户说"自主决定"，记录为 `Standard (auto) + Path A (auto)`；
- 若 Path B，记录 DeepSearch Agent 类型和提示词版本；
- 若有过模式切换，记录切换原因和切换后结果。

---

## References

- `references/exploration-strategy-rules.md`：总控文件，定义三种 Exploration Level（Standard、Divergent、Focused）的参数差异和策略切换规则。
- `references/evidence-source-priority.md`：定义不同证据来源（指南、系统综述、RCT、观察性研究、预印本等）的优先级和权重规则。
- `references/search-routing-rules.md`：定义 Standard 模式下的检索源路由规则和检索深度选择（按领域：临床/ML/中文文献等）。
- `references/divergent-search-routing.md`：Divergent 模式下的检索路由规则，包括跨领域探索、更广来源、更低置信度门槛。
- `references/focused-search-routing.md`：Focused 模式下的检索路由规则，包括严格来源筛选、质量门和排除标准。
- `references/iterative-literature-search.md`：定义广度扫描→深度追踪→缺口补全的三阶段迭代检索策略。
- `references/research-article-clue-extraction.md`：定义从单篇 research article 中提取线索的规则，及其作为证据的局限性。
- `references/evidence-confidence-rules.md`：定义证据强度的标注体系（supported、weak、conflicting 等）及标注条件。
- `references/opportunity-type-taxonomy.md`：定义 opportunity 的分类体系（core types 和 exploration types）及按 Exploration Level 的适用规则。
- `references/chinese-literature-access-rules.md`：定义中文文献的检索策略和访问限制处理规则。
- `references/evidence-map-schema.md`：定义 Evidence Map 的结构字段和输出 schema。
- `references/opportunity-map-schema.md`：定义 Opportunity Map 的结构字段和输出 schema。
- `references/downstream-handoff-rules.md`：定义 mapper 输出如何交给下游 skill（generator、evaluator、orchestrator 等）。
- `references/deepsearch-prompt-rules.md`：定义生成 DeepSearch 委托提示词的规范，含六段结构、三阶段检索、质量门和 Level-specific adjustments。
- `templates/evidence-map.md`：Evidence Map 的输出模板。
- `templates/opportunity-map.md`：Opportunity Map 的输出模板。
- `templates/evidence-insufficiency-report.md`：证据不足时的 insufficiency report 输出模板。
- `templates/source-verification-log.md`：来源验证日志的输出模板。
- `templates/deepsearch-prompt-template.md`：DeepSearch 委托提示词的即用型模板，含 Exploration Level 变体标注。
- `scripts/evidence_search.py`：可复用的 PubMed/arXiv/S2 并行检索脚本；用于 focused parallel evidence retrieval，替代内联 Python。
