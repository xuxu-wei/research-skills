---
name: proposal-drafter
description: "Draft and maintain a proposal file from a proposal-ready context brief."
---
# proposal-drafter

## When to Use

当 proposal 已通过 readiness triage，并需要生成或修订 proposal 文件时，使用本 skill。

本 skill 负责创建、维护和更新 proposal 文件。它不判断 idea 是否 proposal-ready，不评价 proposal 质量，不执行 peer review，也不撰写 SAP。

## Core Principles

- 以 proposal 文件为中心工作，所有生成和修订都必须绑定明确的 `proposal_file_path`。
- 初稿必须基于 context brief、用户目标、已知约束和可用证据生成。
- 若用户显式指定 proposal 结构，优先按用户结构撰写；否则遵循 proposal 核心结构：立项依据（1.1 研究意义 → 1.2 国内外现状 → 1.3 应用前景）→ 研究目标与内容（2.1 目标 → 2.2 内容 → 2.3 关键科学问题）→ 研究方案与技术路线（3.1 方案 → 3.2 技术路线 → 3.3 可行性）→ 创新点。研究基础为可选章节，仅在用户提供相关信息且明确要求撰写时才纳入。
- 创新点应有层次，不能仅停留在"首次应用"层面。每个创新点应能说明所在层次（范式/系统/方法/应用）及差异化价值。
- 当项目类型明示或隐含可量化目标（RCT、benchmark、预测模型），研究目标需包含量化考核指标。当项目是纯方法学/理论/框架构建类，产出本身即为考核标准，不需要强行量化。项目类型从 context brief 读取。
- 修订必须响应 proposal-evaluator 的具体意见，而不是无目标全文重写。
- 语言润色模式只能处理 `academic-language-assessor` 或 revision plan 指定的语言问题；必须保存 `language-change-log-rNNN.md`，不得改变实质内容或 claim strength。
- 不补造关键事实、数据、endpoint、sample size、文献结论或 feasibility 条件。
- 不将不确定性写成确定结论。
- 不评价自己生成或修订的 proposal。
- 每个新增段落必须服务于核心论点，而非降低理解门槛。优先用简洁陈述句，禁止教学式修辞问句和叙事化临床场景。

## Inputs

通常由 `proposal-orchestrator` 提供：

- proposal context brief；
- readiness report；
- 用户目标和目标产出；
- 用户指定的 proposal 结构，如有；
- 已知约束；
- evidence summary，如有；
- funding call 或格式要求，如有；
- 当前 `proposal_file_path`，如为修订任务；
- 当前 `proposal_version`，如为修订任务；
- proposal evaluation report，如为修订任务；
- revision plan，如由 refinement controller 提供。

## Outputs

本 skill 输出：

- new or updated `proposal_file_path`；
- `proposal_version`；
- concise change summary；
- **在 revision 模式下**：独立的审稿回应文件（`06_revisions/round-NNN/response-to-reviewers-rNNN.md`），逐条引用 evaluator/reviewer 意见，说明做了哪些修改、哪些未修改及理由；
- assumptions and unresolved drafting issues；
- handoff note for proposal evaluation or re-evaluation。

不得输出 proposal evaluation decision。proposal 正文中不得包含审稿回应语言（如"根据审稿人建议……""回应XX的质疑……"等）。

## Procedure

### 1. Confirm Drafting Mode

先判断任务类型：

- initial draft：创建新 proposal 文件；
- targeted revision：根据 evaluator 意见修订既有 proposal 文件；
- structural rewrite：在保留 lineage 的前提下重构 proposal；
- formatting pass：按指定模板整理，但不改变核心主张。

若没有 readiness report 或 context brief，应返回缺口说明，交由 orchestrator 决定是否补齐。

### 2. Establish Proposal File State

初稿任务必须创建并返回 `proposal_file_path`。

修订任务必须读取并维护现有 `proposal_file_path`，或生成带版本 lineage 的新文件路径。

必须记录：

- `proposal_file_path`
- `proposal_version`
- source context
- change summary
- unresolved issues

不得让后续流程只能依赖会话摘要。

### 3. Select Proposal Structure

若用户显式指定 proposal 结构、funding call 结构、机构模板或期刊/基金格式，优先使用用户指定结构。

若用户未指定结构，使用 `templates/template-proposal.md` 的推荐结构。

若用户指定结构与可用信息冲突，应保留结构并标记 unresolved drafting issues，不得补造缺失内容。

根据 context brief 中的项目类型字段匹配各部分篇幅。默认（未知类型或信息缺失时）按青年基金比例：立项依据约 30-35%，研究方案约 35-40%，其余部分约 25-30%。如用户指定类型，参照对应比例。

### 4. Draft Initial Proposal

各章的表达目的、小节结构与撰写要求。

#### 4.1 立项依据

目的：让评审相信缺口真实存在、且非解决不可。

小节结构：
- 1.1 研究意义：从大图景逐层聚焦到具体缺口。结尾应让读者清楚"如果不管这个缺口，代价是什么"。
- 1.2 国内外研究现状：分 3-4 类评述，而非按时间线罗列。每类先简述方法原理，再指出缺陷，缺陷必须指向本方案的切入点。
- 1.3 应用前景/科学意义（可选）：成功后能改变什么。

撰写要求：
- 文献综述是 gap 的论证书，不是知识展示。每一段引文的存在理由是被它支撑的 gap。
- 不需要教科书式的历史回顾——评审不需要你解释基础概念。
- 紧迫性应在 gap 论证中自然浮现，不需要"为什么是现在"的独立叙事段。

#### 4.2 研究目标与内容

目的：用最少的文字让评审精确理解"你要干什么"。

小节结构：
- 2.1 研究目标：2-3 句话的高度浓缩。目标是内容的抽象表达——不额外陈述内容之外的目标。
- 2.2 研究内容：3-5 个模块。每个模块在叙述中自然交代它的输入、处理和输出，让模块之间的关系（谁依赖谁、谁与谁并行）从内容本身浮现，而非依赖显式标注。
- 2.3 拟解决的关键科学问题：2-3 个。是"突破什么瓶颈"，不是"完成什么任务"。正确示例："如何从小样本研究设计的不均匀信息中提取可靠的效应估计？"错误示例："完成仿真验证。"（这是研究内容，不是科学问题）

#### 4.3 研究方案与技术路线

目的：让评审相信方法可行、细节无遗漏。

小节结构：
- 3.1 研究方案：与 2.2 研究内容一一对应。每个内容模块有一个对应的方案子节（3.1.1 对应 2.2.1）。
- 3.2 技术路线：一张总图串联所有模块的数据流和逻辑关系。配文字说明。
- 3.3 可行性分析：从团队经验、设备条件、前期基础三个维度论证。

撰写要求：
- 方案描述应达到"别人照着能复现"的粒度。给出工具名、参数值、样本量公式。
- 方案子节的编号与研究内容子节的编号必须对应——杜绝内容第 3 条在方案中找不到对应小节。

#### 4.4 创新点

目的：2-3 条差异化主张。

撰写要求：
- 每个创新点说明所在层次（范式/系统/方法/应用），回答三个问题：以前为什么没人做？解决了什么困难？差异化价值范围？
- 每个创新点必须在 4.3 研究方案中有具体做法回指。
- 不单独以"首次用 XX 方法做 YY 疾病"作为完整创新点。

#### 4.5 研究基础（可选）

仅在用户提供相关信息且明确要求撰写时才纳入。

撰写要求：
- 按能力域组织（理论基础/数据基础/方法基础/实验基础/临床资源），不按时间罗列。
- 每条基础必须有已发表论文或预实验数据支撑。

---

如信息缺失，应明确标记为 unresolved issue，而不是自行补造。

### 5. Maintain Claim Discipline

所有 claims 必须与已知 evidence、context brief 或用户提供材料一致。

对于不确定内容，应使用谨慎表述，并标记需要人工核查或后续证据支持。

不得声称：

- novelty 已被证明，除非 evidence summary 支持；
- 数据一定可获得，除非用户明确提供；
- endpoint 或 outcome 已确定，除非 context brief 明确；
- 方法一定可行，除非已通过相应检查。

### 6. Perform Targeted Revision

当接收到 proposal evaluation report 或 revision plan 时，只针对明确问题修订。

修订应优先处理：

- research question 不清；
- aims 与方法不一致；
- novelty claim 过强或证据不足；
- feasibility 描述不足；
- methods 无法支撑 hypothesis；
- 用户目标或 funding call 不匹配；
- reviewer defensibility 不足；
- completion 缺口。

**修订产出双文件**：revision 模式下必须同时产出两个文件——

1. **修订后的 proposal 文件**（`proposal-v{N+1}.md`）：正文干净，不含任何审稿回应语言。修改本身（新增/删减/重写）应直接融入正文，不附带解释性前缀。
2. **审稿回应文件**（`06_revisions/round-NNN/response-to-reviewers-rNNN.md`）：逐条引用 evaluator 的具体意见，说明处理方式（已修改 / 未修改及理由 / 交由 controller 决策），并标注每条意见的处理策略（入正文 / 仅入回应 / 不处理）。不能解决的问题诚实标记为 unresolved。

**proposal 正文禁止以下表达式**：
- "根据审稿人建议……""为回应XX的质疑……""对此问题，我们补充……"
- 任何将外部评审意见作为修改理由嵌入正文的表述
- 评价自身修改的元语言（"修改后的表述更清晰地展示了……"）

每轮修订必须输出 change summary，说明哪些 evaluator concerns 已处理，哪些仍未解决。

### 7. Preserve Version Lineage

修订时必须保留版本关系。

不得覆盖式生成无法追踪的全新 proposal。

若产生新文件，应明确：

- previous proposal file path；
- new proposal file path；
- version change；
- main edits；
- remaining issues。

### 8. Handoff

完成后，将 proposal 文件交回 `proposal-orchestrator`。

handoff 内容至少包括：

- `proposal_file_path`
- `proposal_version`
- **在 revision 模式下**：`response_to_reviewers_file_path`
- change summary
- unresolved issues
- recommended next step: evaluation or re-evaluation

不得自行宣布 accept、reject、ready for submission 或 reviewer approval。

## Artifact Naming

Use `proposal-orchestrator/references/artifact-naming-and-directory-rules.md` as the source of truth for all proposal artifact paths.

- Initial and revised proposal files should use versioned paths such as `04_drafts/proposal-v001.md`, `04_drafts/proposal-v002.md`, and `04_drafts/proposal-vNNN.md`.
- Substantive revisions create a new proposal file instead of overwriting the previous version.
- Reviewer-response artifacts should live under `06_revisions/round-NNN/response-to-reviewers-rNNN.md`.
- Revision plans and deltas should live under the same revision round directory.
- The drafter should return `proposal_file_path`, `proposal_version`, source path, and change summary so `10_state/workflow-state.yaml` and `10_state/artifact-index.md` can be updated.

## Delegation Rules

本 skill 通常不直接派发 evaluation 子 agent。

若发现需要评价、gate 或 review，应交回 `proposal-orchestrator` 调度相应独立子 agent。

不得自行调用或模拟：

- proposal evaluation；
- SAP evaluation；
- methodology review；
- proposal reviewer panel；
- skeptical review。

## Stop Conditions

以下情况应停止 drafting 或 revision，并返回问题说明：

- 缺少 context brief；
- readiness triage 未通过；
- 用户输入不足以形成最小 proposal；
- 任务要求撰写 SAP，但应改由 `sap-writer` 处理；
- evaluator 指出 fatal flaw，且 orchestrator 未要求继续修订；
- 修订要求与用户目标、证据或约束明显冲突；
- 需要新增关键事实才能继续，但该事实未被用户提供。

## Pitfalls

- 不要替代 readiness triage。
- 不要自评 proposal。
- 不要撰写 SAP。
- 不要补造数据、endpoint、sample size 或文献结论。
- 不要把不确定性包装成确定结论。
- 不要无目标全文重写。
- 不要脱离 `proposal_file_path` 生成独立版本。
- 不要忽略用户显式指定的 proposal 结构。
- 不要删除 evaluator 指出的 unresolved issues，除非修订已实际解决。
- 不要将语言润色冒充实质修订。
- 不要使用教学式修辞问句或叙事化临床场景。
- 不要以降低理解门槛为由添加解释性段落。
- **不要将审稿回应语言写入 proposal 正文**——修改应直接融入正文，审稿回应写入独立的 `response-to-reviewers` 文件。
- 当项目类型要求量化时，不要声明参数改善而不设具体阈值或评判标准。

## Verification

完成前检查：

- 是否存在明确 `proposal_file_path`；
- 是否记录 `proposal_version`；
- 是否基于 context brief 和 readiness report drafting；
- 是否保留用户目标和约束；
- 是否优先遵循用户显式指定的 proposal 结构；
- 若无用户指定结构，是否使用默认 proposal template；
- 是否避免补造关键事实；
- 是否明确 unresolved issues；
- 若为修订，是否响应 evaluator 的具体意见；
- 若为修订，是否保留版本 lineage；
- 是否未输出 evaluation decision；
- 是否已准备好交给 proposal-evaluator 或 re-evaluator。
- 研究内容各条与研究方案各子节之间是否存在一一对应？
- 每个研究目标是否在研究内容中有落地条目？
- 每个创新点是否在研究方案中有具体做法回指？
- 是否已执行 `references/anti-pattern-checklist.md` 的全部条目？

## References

- `proposal-orchestrator/references/artifact-naming-and-directory-rules.md`: source-of-truth naming and directory rules for versioned proposal, revision, panel, SAP, package, state, and artifact-index files.
- `references/proposal-genre-awareness.md`: background genre-awareness rules for avoiding tutorial, narrative, and reviewer-response artifacts in proposal body.
- `references/proposal-writing-principles.md`: background writing principles derived from approved examples; use after core rules, not as a replacement for `rules-proposal-writing.md`.

- `references/rules-proposal-writing.md`：定义 proposal 写作范围、章节要求、默认结构选择、语言边界和不得补造的信息类型。
- `references/rules-literature-integration.md`：定义如何在 proposal 中使用 evidence summary、文献依据和不确定性标注。
- `references/rules-claims-discipline.md`：定义 novelty、feasibility、impact、method claims 的表述约束。
- `references/policy-file-maintenance.md`：定义 `proposal_file_path`、版本 lineage、change summary 和 unresolved issues 的维护规则。
- `templates/template-proposal.md`：定义 proposal 文件的推荐输出结构；当用户显式指定结构时，应优先遵循用户结构。
- `proposal-orchestrator` 的 `references/proposal-writing-methodology.md`：基于 7 份已获批范例的 proposal 撰写方法论。需要时直接读取该引用文件。
- `references/anti-pattern-checklist.md`：proposal 完稿后的 anti-pattern 自检清单。handoff 前直接读取该引用文件并逐条检查。
