---
schema_version: research-idea.v3
plugin_version: "0.10.0"
artifact_id: research-idea-portfolio-v001
version_id: v001
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: round-001
path: 04_portfolio/research-idea-portfolio-v001.md
source_skill: idea-portfolio-assembler
created_by_instance_id: fresh-idea-portfolio-assembler-v001
based_on:
  - artifact_id: idea-dossier-I01-001-v006
    version: v006
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
  - artifact_id: evaluation-I01-001-r008
    version: r008
    path: 03_ideas/nodes/I01-001/reviews/evaluation-r008.md
  - artifact_id: candidate-journal-match-I01-001-r008
    version: r008
    path: 03_ideas/nodes/I01-001/reviews/candidate-journal-match-r008.yaml
  - artifact_id: medical-journal-review-I01-001-r008
    version: r008
    path: 03_ideas/nodes/I01-001/reviews/medical-journal-review-r008.md
change_type: assemble
status: revision_required
frozen: true
---

# Research Idea Portfolio

## Executive navigation

- **Route profile:** `focused_optimization`。这是现有单节点链条的工作流路由，不是对未物化方向的重新比较或排序。
- **Current human state:** `revision_required`；负责人需决定是否组织下一版完整 dossier，并在任何实质性修订后安排全新的保真、叙事、语言、独立评价与适用的期刊审查。
- **Number of Ideas:** 1。
- **Stop/pause reason:** 封存评价决定为 `revise_then_promote`，不是 `promote`；当前核心实施依赖尚未实证落实，并且 r007 保留 12 项非阻断 minor readiness finding。
- **Next human action:** 审阅本导航包和 [current dossier](../03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md)，决定是否授权把评价要求和 12 项 minor readiness finding 纳入新的完整 dossier。不得把本 portfolio 当作 Idea 正文或 Proposal。

## Idea navigation

### 受约束的脓毒症全病程动态状态模型：在一个数据库中开发并在异质数据库中外部验证

- **Idea ID:** `I01-001`（受约束的脓毒症全病程动态状态模型：在一个数据库中开发并在异质数据库中外部验证）。
- **Current dossier artifact ID / version / path:** `idea-dossier-I01-001-v006` / `v006` / `03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md`。
- **Relative dossier link:** [idea-dossier-v006.md](../03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md)。
- **Evaluation report link:** [evaluation-r008.md](../03_ideas/nodes/I01-001/reviews/evaluation-r008.md)。
- **Candidate journal-match link:** [candidate-journal-match-r008.yaml](../03_ideas/nodes/I01-001/reviews/candidate-journal-match-r008.yaml)。该简报不含评价字段、评分、排名或发表概率。
- **Medical journal review link:** [medical-journal-review-r008.md](../03_ideas/nodes/I01-001/reviews/medical-journal-review-r008.md)。
- **Journal review applicability:** `applicable`；当前独立审查决定为 `journal_candidates_confirmed`。
- **Narrative readiness link:** [narrative-assessment-r007.md](../03_ideas/nodes/I01-001/reviews/narrative-assessment-r007.md)；判定 `minor_narrative_revision`。
- **Narrative repair-plan link:** [narrative-repair-plan-r007.yaml](../03_ideas/nodes/I01-001/reviews/narrative-repair-plan-r007.yaml)。
- **Language readiness link:** [language-assessment-r007.md](../03_ideas/nodes/I01-001/reviews/language-assessment-r007.md)；判定 `minor_language_revision`。
- **Content-preservation link:** [content-preservation-r007.md](../03_ideas/nodes/I01-001/reviews/content-preservation-r007.md)；判定 `scientific_content_preserved`。
- **Methodology preflight link:** [preflight-r005.md](../03_ideas/nodes/I01-001/reviews/preflight-r005.md)；该报告评估 v005，v005→v006 的科学内容保真由 r007 单独确认。
- **Reference ledger link:** [reference-ledger.md](../03_ideas/nodes/I01-001/references/reference-ledger.md)。
- **Evidence and opportunity links:** [evidence-map-v001.md](../02_evidence/evidence-map-v001.md)；[opportunity-map-v001.md](../02_evidence/opportunity-map-v001.md)。
- **Status:** `revision_required`，封存分组为 `revise-then-promote`。
- **Evaluator scores and gates:** Novelty 4；Feasibility 3；Impact 4；Relevance 4；Clarity 4；Completion 4；简单平均 3.83；硬门均通过。
- **Fatal / blocking findings:** fatal flaw 为无，评价硬门失败为无，当前报告也未登记 unresolved blocking finding。不能晋级的原因是封存决定仍为 `revise_then_promote`，且 major finding“核心实施依赖仍待实证落实”尚未关闭；本项不被重分类为 fatal 或 blocking finding。
- **Dissent:** 当前允许输入没有记录 reviewer dissent；本节点尚未进入 focused Proposal handoff，因此没有 adversarial panel 决定可供替代。
- **Next human action:** 决定是否以项目级证据关闭两库许可与字段映射、事件和有效转移审计、约束表、团队与计算基准等实施依赖，并在需要修改 dossier 时创建新完整版本；新版本不得沿用 r007/r008 的 readiness、评价或期刊审查结论。

#### Unresolved editorial issues — narrative readiness

以下四项均来自 r007，严重度保持为 `minor`，不作静默修复或重分类：

1. `NAR-001`（Background 提前承担 Rationale 的方案选择功能）：方案选择在 Current state、Gap 与 Significance 前出现，使 Background 与 Rationale 的功能边界模糊。
2. `NAR-002`（“持续恢复”的技术含义晚于多次核心使用）：首次读者可见处尚未区分持续恢复、短暂改善与存活出 ICU。
3. `NAR-003`（开篇定义段混合读者入口与方法细节）：跨数据库诊断操作细节与后文不再使用的复杂系统标签增加入口负担。
4. `NAR-004`（Working assumptions 中任务三说明重复且不符合小节功能）：固定设计要素被置于工作假设小节并重复其他权威位置的说明。

#### Unresolved editorial issues — language readiness

以下八项均来自 r007，严重度保持为 `minor`，不作静默修复或重分类：

1. `LANG-001`（外部状态表示相关术语的修饰对象与“占用”含义不够直接）：跨学科读者可能把“开发状态”理解为开发进度。
2. `LANG-002`（任务三预测目标的限定语叠加且角色形式不一致）：输入、遮蔽操作、实测属性和预测动作集中在长修饰语中。
3. `LANG-003`（参数和潜在状态恢复诊断的并列范围有歧义）：名词短语无法立即显示诊断同时覆盖两类恢复。
4. `LANG-004`（“人体开放复杂巨系统”标签不透明且装饰性较强）：标签未承担后续测量或模型角色。
5. `LANG-005`（单句完整构想摘要的从句链负担过重）：多个主干与限定的附着范围需要回读。
6. `LANG-006`（任务三说明泄露对话来源）：读者可见正文中的“用户提出的”不符合自足学术语域。
7. `LANG-007`（条件性后续研究独立性的表达含连续否定与分支隐喻）：两项研究的条件关系不够直接。
8. `LANG-008`（MQTiPSS 与 ARRIVE 2.0 首次使用缺少用途说明）：非动物实验专业读者无法从短称判断两项标准的角色。

#### Other unresolved issues

- **Evaluator major finding:** 两个数据库的项目级许可、真实样例字段适配、核心团队承诺和计算基准仍待实证落实。
- **Evaluator minor finding:** 统一模型的计划增量已有边界，但有界检索和待复核的 2026 年来源不支持优先性主张。
- **Evaluator minor finding:** 读者推理链完整，但跨学科读者仍需承担较高技术密度。
- **Preflight working assumptions:** `WA-01`（核心实证研究能否独立形成论文）与 `WA-02`（第三数据库是否具备资格与资源）尚待各自预定验证点确认。
- **Preflight implementation gates:** 两库共同目标变量、可评分遮蔽块、观测概率权重稳定性、外部可执行性、约束表、团队与计算均须实证确认。
- **Candidate-journal match boundary:** Communications Medicine 的最终适配取决于完成研究后的医学意义与证据强度；约 5,000 词的建议篇幅可能要求压缩技术细节。候选确认不是期刊选择、排名、接受概率或提交授权。
- **Medical review unresolved issues:** 报告登记为无；这不改变其针对预期论文而非完成稿件的适配边界。

## Sealed comparison

| Idea title | Evaluator scores/gates | Evaluator decision/status | Candidate journal match | Medical review decision/status | Fatal/blocking | Dissent | Human action |
|---|---|---|---|---|---|---|---|
| 受约束的脓毒症全病程动态状态模型：在一个数据库中开发并在异质数据库中外部验证 | 4/3/4/4/4/4；平均 3.83；硬门均通过 | `revise_then_promote` / `revision_required` | Communications Medicine — Article；无评分、无排名、无发表概率 | `journal_candidates_confirmed`；独立、未见 evaluator 报告或分数 | fatal 无；blocking finding 未登记；major 实施依赖未关闭 | 未记录 | 决定是否创建新完整 dossier；实质性修订后重新走独立审查链 |

候选期刊简报与医学期刊审查只提供独立的编辑适配导航，不改变 evaluator 分数、硬门、决定或状态。

## Subordinate lineage and non-qualifying outcomes

| Idea title | Current version | Change type | Status | Readable reason |
|---|---|---|---|---|
| 受约束的脓毒症全病程动态状态模型：在一个数据库中开发并在异质数据库中外部验证（`I01-001`） | v006 | editorial_repair | revise-then-promote / revision required | v005→v006 的科学内容由 r007 确认为保留；r008 仍要求先落实核心实施依赖，r007 的 12 项 minor readiness finding 继续公开。 |

- **Parent Idea IDs:** 无。
- **Lineage ID:** `lineage-I01-001`（本节点完整版本链 v001 → v002 → v003 → v004 → v005 → v006）。
- **Generation path:** focused single-node chain；科学修订与编辑修订均保持 `I01-001` 身份，v006 identity status 为 `preserved`。
- **Backup/rejected/evaluation-failed nodes:** 当前链条中无其他物化节点；不据此否定机会地图中的未物化方向。

## Handoff

- **Focused Proposal-handoff status:** `not_eligible`。没有封存 `promote` 决定，也未进入 adversarial Proposal-handoff panel；不得生成 Proposal。
- **Human direction-selection entry:** `not_applicable`；当前路由是 focused single-node revision。
- **Current human handoff:** `revision_required`。负责人可选择停止、保留现状供内部讨论，或授权新完整 dossier；任何新版本都必须重新接受独立审查。

本 portfolio 仅提供导航和人类审阅入口，不复制或替代 dossier 正文。
