---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-r043
review_id: narrative-review-r043
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-narrative-r043
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r043
input_artifact_ids:
  - idea-dossier-I01-001-v029
  - reader-handoff-forward-001
input_versions:
  - v029
  - v001
input_dossier:
  artifact_id: idea-dossier-I01-001-v029
  version: v029
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/idea-dossier-v029.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/idea-dossier-v029.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: minor_narrative_revision
findings:
  - finding_id: NAR-043-001
    severity: minor
    category: qualifier-stacked summary
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary: 本研究拟在 24 个月内整合文献、专家知识"
    observed_evidence: "单句摘要同时承载研究期限、证据来源、全病程对象、三类跨数据库检验、模拟恢复检验的行内定义、阶段 II 的五类达标条件以及后续 RCT 次要分析的启动条件。"
    current_reader_effect: "跨学科读者第一次接触研究时，需要在一句话内区分主要研究问题、24 个月最低交付和条件性后续分析，正向研究目标因多层条件和技术细节而不易在一遍阅读后复述。"
    target_function: "单句摘要应先让读者识别研究对象、主要问题、24 个月验证目标和条件性 RCT 层级；详细阈值、审计项目和阶段 II 判定留在紧随其后的摘要与专门章节。"
  - finding_id: NAR-043-002
    severity: minor
    category: reader-baseline mismatch and avoidable backtracking
    dossier_locator:
      section_heading: "Structured abstract"
      subsection_heading: null
      content_anchor: "Objective and hypothesis: 目标是在 24 个月内完成数据审计、恢复检验"
    observed_evidence: "标题、单句摘要和结构式摘要在提出主要结论路径时使用“候选动态表征”“锚定约束”“可恢复量”和“预设不变量”等核心概念；患者状态与状态转移、跨数据库锚点及恢复标准的具体含义主要到研究问题、可观测性审计、锚定与模拟恢复检验部分才逐步显现。"
    current_reader_effect: "读者交接明确不假定每位读者精通所有参与学科。临床、流行病学或转化研究读者需暂存这些未解释概念，并在后文寻找其作用后再回读早期假设。"
    target_function: "在首次承担论证作用的位置，用跨学科读者可理解的功能性说明交代候选表征、跨数据库锚点和可恢复不变量各自解决什么问题；公式、载荷约束和数值标准仍在方法部分展开。"
  - finding_id: NAR-043-003
    severity: minor
    category: caveat saturation and repetition
    dossier_locator:
      section_heading: "Contribution, innovation, impact, application, and closest-work comparison"
      subsection_heading: "Representative related research comparison"
      content_anchor: "截至 2026-07-17 的有界代表性检索对“各单项模块已有先例”给出高置信判断"
    observed_evidence: "有界检索不能支持全球首创或全球不存在性主张这一完整边界，已在 Gap 中直接限定缺口陈述，在 Limitations and boundary conditions 中作为完整限制说明，并在 claim-support 与风险停止条件中承担审计或决策功能；此外，“Required analyses and evidence”末尾和相关研究比较表后又各有一段独立复述。"
    current_reader_effect: "两处没有新增局部功能的完整复述减慢从必需证据到预期产物、以及从相关工作比较到正向贡献的推进，使同一防御性边界比研究增量更突出。"
    target_function: "保留与缺口陈述直接相连的必要限定、claim-support 的可审计状态、风险停止条件及第 14 节完整限制；删除不承担新增局部功能的独立复述，不添加指向限制章节的替代语句。"
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

该 dossier 的主读者推理链已经成立。背景从电子健康记录中的脓毒症发病时刻不唯一切入；当前状态说明可用数据库、相邻研究路线以及治疗和观测过程带来的解释问题；缺口明确询问一个区分生理状态、治疗行动与观测过程的候选表征能否覆盖全病程、跨数据库保持稳定，并在前置证据成立后支持试验次要分析；意义部分说明这一区分为何影响纵向研究的可重复性和后续转化判断；理由部分再把双时刻设计、互斥状态、变量分工、模拟恢复检验、隔离外部验证与条件性 RCT 分析逐项连回缺口。标题、研究问题、目标、核心假设、主要任务和贡献也指向同一个研究对象。

因此不需要重排主论证或改变章节结构。当前问题是局部的读者负担：首个单句摘要把几乎全部条件压入一处，若干跨学科核心概念在承担早期论证任务时尚未获得功能性解释，且文献定位边界有两处不必要的完整复述。这些问题可通过局部编辑解决，不涉及方法、证据强度、术语标准性、创新性、影响或可行性的判断。

## Findings

### NAR-043-001 — 单句摘要中的条件堆叠

单句摘要能够找到完整研究内容，但其读者功能没有优先级：主要研究对象、24 个月验证路线、模拟恢复检验定义、阶段 II 全部闸门和后续 RCT 条件连续嵌套。读者必须先解析内部定义和多层条件，才能确认主要研究究竟要完成什么。修订应压缩此处的技术与判定细节，同时保留全病程对象、跨数据库验证和 RCT 仅为条件性后续层级这三个身份要素。

### NAR-043-002 — 核心概念的解释晚于其论证用途

“候选动态表征”“锚定约束”和“可恢复不变量”是问题、假设与设计理由之间的连接件，不只是方法细节。现稿到后续患者状态与状态转移、锚点审计、锚定模型和恢复标准处才使这些概念的功能充分可见。对读者交接所述的多学科受众，早期需要的是简短的功能性解释，而不是提前引入公式或阈值；这样后续方法细节才能作为加深理解，而不是补回先前缺失的前提。

### NAR-043-003 — 文献定位边界的无功能重复

缺口段落中的限定直接约束缺口陈述，第 14 节保留完整限制，claim-support 表和风险表也分别承担追溯与停止条件功能。这些位置有明确局部作用。相比之下，“Required analyses and evidence”之后以及相关研究比较表之后的独立段落再次完整说明同一有界检索边界，没有推进相邻章节承诺的功能。删除这两处复述即可恢复从证据要求到产物、从比较到贡献的顺向推进；不应以跨章节指针替代被删内容。

## Preserved strengths

- Background、Current state、Gap、Significance 和 Rationale 五个功能均非空、彼此可区分，且理由逐项回应已陈述的缺口。
- 主要研究问题、四项目标、两项主要任务、外部验证和条件性 RCT 分析的层级一致；RCT 结果不会反向替代 24 个月验证阶段的判定。
- 方法细节总体遵循由研究问题到设计再到实现的披露顺序；证据链保留 Input、Method / analysis / processing、Output 和 Supports 四项可审查功能。
- 必需章节中的时间计划、工作包、方法规范、证据链、计划产物、Claim-Support 和风险停止条件承担不同功能，修订时不应因主题相同而合并或删除。
- “Limitations and boundary conditions”应继续作为完整限制与假设的唯一权威位置；其他位置仅保留直接推动相邻推理所必需的自足边界。

## Handoff

See the paired `narrative-repair-plan-r043.yaml` for executable actions.
