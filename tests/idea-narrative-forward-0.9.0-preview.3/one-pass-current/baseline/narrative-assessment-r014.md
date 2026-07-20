---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-r014
review_id: narrative-review-r014
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-raw-narrative-r014
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r014
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - reader-handoff-forward-001
input_versions:
  - v003
  - v001
input_dossier:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: major_narrative_revision
findings:
  - finding_id: NAR-001
    severity: major
    category: reader_reasoning_chain
    dossier_locator:
      section_heading: "Background, current state, gap, significance, and rationale"
      subsection_heading: null
      content_anchor: "最近近邻使‘单个模块新颖’不可成立"
    observed_evidence: "该节以连续段落交织背景、既有研究、候选缺口和设计说明，但没有把 significance 作为独立、非空的读者功能展开；读者能看到拟议整合的组成，却难以直接辨认解决这一缺口为何会改善跨数据库科学解释、可重复性或后续转化判断。"
    current_reader_effect: "目标读者必须从贡献、验证规则和后文限制中自行重建‘为什么值得做’，因而问题—缺口—意义—设计依据的主链在进入研究问题前没有闭合。"
    target_function: "在同一必需章节内明确分开并依次完成 Background、Current state、Gap、Significance 和 Rationale 五项功能，使意义先回答为何该缺口对目标读者重要，再由设计依据解释拟议研究为何是合适回应。"
  - finding_id: NAR-002
    severity: major
    category: progressive_disclosure_and_concept_burden
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary"
    observed_evidence: "一句话摘要在解释研究问题之前同时引入‘绝对模拟恢复门’、‘真正未触碰的跨数据库检验’、‘冻结观测投影门’、‘投影可观测状态摘要’、‘death-ranked SOFA’以及阶段编号；Structured abstract 随即继续使用这些概念和若干英文技术缩写，而多数概念的操作含义到后续方法章节才出现。"
    current_reader_effect: "虽具备重症研究或纵向分析背景但不熟悉本项目标签的读者，需要先记住多层条件和分支，再向后查找定义，因而无法在开篇稳定把握研究所问、为何重要以及主要设计逻辑。"
    target_function: "让标题、一句话摘要和结构式摘要先以跨学科可理解的语言给出问题、缺口、意义、主要设计与条件性贡献；必要的专门概念在首次使用时用其科学功能解释，具体阈值、分支名称和技术实现按需要后置。"
  - finding_id: NAR-003
    severity: major
    category: narrative_balance_and_limitation_authority
    dossier_locator:
      section_heading: "Evidence chains"
      subsection_heading: "Evidence chain: 可用性时钟、风险集与互斥病程"
      content_anchor: "Limits and failure conditions"
    observed_evidence: "五条证据链各自增加了独立的‘Limits and failure conditions’字段；与此同时，因果解释边界、外部检验失败、RCT 投影失败、数据与语义缺口等完整限制又在摘要、核心非假设、方法、预期结果、解释矩阵、贡献表和可行性章节反复陈述。"
    current_reader_effect: "限制性陈述多次中断正向论证，读者难以判断哪一处是完整权威版本，并需要跨节核对相似但粒度不同的表述；证据链的四项可审计功能也被额外字段稀释。"
    target_function: "由第 14 节承担完整限制与假设的唯一权威陈述；其他章节只保留为理解紧邻科学选择不可缺少、且能独立成立的最小边界。每条证据链仅保留 Input、Method / analysis / processing、Output 和 Supports，不保留或重建链级限制字段，也不用跨节指针替代删除内容。"
  - finding_id: NAR-004
    severity: minor
    category: repetition_and_navigation
    dossier_locator:
      section_heading: "Required analyses and evidence"
      subsection_heading: null
      content_anchor: "阶段 II 主张前必须完成"
    observed_evidence: "日期顺序、准入条件、外部检验次序、RCT 分支和失败后果已在 Research content and work packages 与 Research design and methods 中说明，随后在 Required analyses and evidence、Expected outputs, falsification criteria, and interpretations 以及风险矩阵中以接近完整的形式再次出现。"
    current_reader_effect: "读者需要反复比较多份相似清单，才能确认它们是同一研究路线的不同功能说明，而不是新增或冲突的要求；主要问题和贡献因此被操作细节压低。"
    target_function: "在不删除任何必需章节的前提下，使研究内容章节负责范围与顺序、方法章节负责实施、所需分析章节负责可核验交付、预期结果章节负责可证伪结果与解释、可行性章节负责风险和完整限制；删除无新增功能的重复句。"
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

结论为 `major_narrative_revision`。研究题目、主要问题、四项目标、患者时间状态与状态转移这一推断单位，以及阶段 II 与条件性 RCT 再分析之间的边界总体一致；读者不会被引向另一项研究。但是，开篇推理链没有把研究意义作为独立环节说清，且在读者理解问题之前加载了大量后文才解释的条件、缩写和项目标签。修复需要重新组织读者的主路线，而不只是局部润色。

限制性内容的分布进一步放大了这一问题。当前多处重复完整的因果、运输性、数据可用性和 RCT 解释边界，五条证据链还各有一个不属于当前 dossier 合同的独立限制字段。完整限制应集中在第 14 节；局部只保留对紧邻设计选择不可缺少的最小边界，不应以“参见第 14 节”一类指针替代删除的内容。

## Findings

### NAR-001 — 意义环节没有独立闭合

背景章节提供了脓毒症标签不唯一、数据库异质性、相邻研究和观察性推断边界，也给出了若干“因此/为此”的设计回应，但从“尚缺少怎样的综合证据”直接进入“本项目如何组织五层证据”。对目标读者而言，尚缺一段明确回答：若这一缺口得到解决，为什么会改善科学判断或后续研究决策。应把五项读者功能拆开并按顺序完成，而不增加新的科学主张。

### NAR-002 — 开篇概念负担超过读者基线

一句话摘要实际承担了完整流程、多个判定条件、两条 RCT 分支和禁止性解释，结构式摘要又沿用未先解释的名称。后文方法本身给出了这些概念的操作定义，问题主要在披露顺序，而不是术语是否标准。开篇应先帮助跨学科读者理解研究问题、意义和总体响应，再逐步引入必要的统计与系统表征概念。

### NAR-003 — 完整限制没有单一权威位置

“预测不等于因果”“有限更新不替代零更新”“RCT 投影或独立 SOFA 分支不能验证整个系统”等重要边界被完整重述多次。部分局部边界确实直接支撑紧邻设计，例如观测目标旁需要说明不估计治疗因果作用；但完整限制清单应只在第 14 节出现。五条证据链的独立限制字段必须删除，同时保留其 Input、Method / analysis / processing、Output 和 Supports 四项功能及其中的科学内容血缘。

### NAR-004 — 必需章节之间存在可避免的操作性复述

研究内容、方法、所需分析、预期结果和风险章节具有不同合同功能，因此不能合并成一张表。但当前若干日期、阈值和失败路线在各节重复到接近完整版本。应保留各节独有的最低内容，只删除不能增加该节功能的复述，使读者不必反复核对同一规则。

## Preserved strengths

- 标题、主要研究问题、目标、核心假设和研究对象围绕同一全病程候选表征，没有核心元素漂移。
- 背景材料已经包含构成完整推理链所需的事实基础，修复主要是分工、排序和意义说明，而不是补造证据。
- 观察性研究、跨数据库检验和条件性 RCT 再分析的科学边界明确，且 RCT 投影失败后与阶段 II 独立的临床状态再分析分支区分清楚。
- 研究设计的时钟、状态、数据角色、外部检验和停止条件具有较强可审计性；编辑修复应保留这些内容及五条证据链的四项必需功能。

## Handoff

See the paired `narrative-repair-plan-r014.yaml` for executable actions.
