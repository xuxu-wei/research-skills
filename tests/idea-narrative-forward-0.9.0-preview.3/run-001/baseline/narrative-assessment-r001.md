---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-r001
review_id: narrative-review-I01-001-r001
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-baseline-narrative-r001
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r001
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
      content_anchor: "最近近邻使“单个模块新颖”不可成立。"
    observed_evidence: >-
      该段先以各单项模块已有先例界定可辩护的整合空间，后续段落随即进入因果边界、缺失机制、弃权规则和试验投影条件。正文没有把“现有证据仍不能回答什么”与“解决这一问题为何对声明的读者重要”分别说清，整合架构的缺位因而承担了科学问题与价值说明两种功能。
    current_reader_effect: >-
      读者能够辨认项目准备组合哪些模块，却必须自行推断该组合要消除的具体证据障碍及其后果；后续设计更像一组谨慎措施，而不是由明确问题、意义和理由依次推出的研究方案。
    target_function: >-
      依次陈述现有工作能回答的范围、仍无法回答的科学或证据问题、该问题对目标读者的意义，以及每个主要设计层为何是回应这一问题所必需的。
  - finding_id: NAR-002
    severity: major
    category: section_function_fit
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary"
    observed_evidence: >-
      单句摘要同时承载 24 个月阶段、两个公共数据库、绝对恢复条件、未触碰外部检验、两个试验的 D7/D8 投影、失败后的独立端点以及多项禁止性解释。多数条件在句中首次出现，其作用尚未建立。
    current_reader_effect: >-
      读者第一次接触研究时需要先解析多层条件和例外，才能找出正面的研究问题与贡献；即使各限定准确，摘要也没有先完成“研究要做什么、为什么值得做”的概括功能。
    target_function: >-
      用一次阅读即可复述的顺序先给出研究对象、核心问题、阶段 II 的主要贡献和阶段 III 的从属关系，只保留会改变研究身份的限定，把执行细节和失败分支交给相应章节。
  - finding_id: NAR-003
    severity: major
    category: progressive_disclosure_and_reader_baseline
    dossier_locator:
      section_heading: "Structured abstract"
      subsection_heading: null
      content_anchor: "Approach: 主发病前任务采用每 12 小时 landmark"
    observed_evidence: >-
      摘要在说明各设计环节的通俗功能之前连续使用 landmark、累积发生风险、绝对 Monte Carlo 条件、zero update、observation-layer update、冻结观测投影、death-ranked SOFA、proper score 等跨学科或项目特定表达；其中若干要到后文的方法、外部检验或试验投影章节才获得足够解释。
    current_reader_effect: >-
      读者交接仅允许假定对重症研究、纵向数据、验证和观察性与干预性证据的一般熟悉度。当前顺序要求不同专业的读者临时接受未解释概念，并在后文寻找含义后返回摘要，增加了不必要的回读。
    target_function: >-
      先说明每个设计环节解决哪一个读者已知的问题，再引入必要的专业概念；在首次使用处给出跨学科可理解的简短定义，并将阈值、代码式名称和条件分支细节后移。
  - finding_id: NAR-004
    severity: major
    category: repetition_and_navigation
    dossier_locator:
      section_heading: "Expected outputs, falsification criteria, and interpretations"
      subsection_heading: "Falsification and stop criteria"
      content_anchor: "RCT 投影：共同锚点/单位/时序、SVD 低维性"
    observed_evidence: >-
      对观察性结果不作因果解释、有限更新不能替代零更新、试验备用端点不验证阶段 II 表征、项目不主张数字孪生或全球首次等边界，已在摘要、核心假设、日期条件、方法、证据链、解释矩阵、贡献表和风险矩阵中多次完整重述。停止条件也分别出现在多个表格和列表中。
    current_reader_effect: >-
      重复的防御性说明持续打断正面论证，读者难以判断哪一处是完整且权威的限制说明，也难以区分真正不同的边界与同一边界的改写。
    target_function: >-
      建立一个权威的限制与停止条件位置，完整保留所有独特边界；其他章节只保留为理解紧邻设计选择所必需的局部限定，并删除不承担新功能的重复表述。
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

判定为 `major_narrative_revision`。标题、研究问题、目标和主要证据基础指向同一个研究对象，阶段 II 与条件性阶段 III 的边界也保持一致；问题不在科学内容是否齐全，而在读者必须自行重建其顺序。当前开头先堆叠限定和专业表达，背景部分又用“组合尚未出现”代替了独立的证据缺口与意义说明，最清楚的设计理由散落在后续方法和证据链中。与此同时，同一限制在多个章节反复出现，压低了正面研究动机和贡献的可见度。

这些问题不能只靠局部润色解决。需要重新安排开头、背景论证、摘要中的概念引入，并把重复边界收束到一个权威位置，才能让声明的跨学科读者依次理解问题、现状、缺口、意义和设计理由。

## Findings

### NAR-001：证据缺口与意义没有形成独立环节

“Background, current state, gap, significance, and rationale” 已提供充分的背景事实、近邻工作和方法边界，但其核心转折是从“单个模块不新颖”走向“条件性整合这些模块”。这说明了项目可能占据的贡献位置，却没有直接说明现有证据为何不能回答全病程表征在跨数据库条件下是否可恢复、可运输，以及这一不确定性会给重症研究、临床流行病学和系统辨识研究带来什么后果。后续的行动过程、测量过程、外部检验和试验投影设计都有可理解的理由，但这些理由没有被一个明确的缺口—意义桥梁统领。

### NAR-002：单句摘要被条件和例外挤占

“One-sentence complete-Idea summary” 包含了几乎全部执行条件和解释禁区。完整性因此转化为理解负担：读者尚未抓住正面研究目标，就要同时处理阶段编号、多个数据库、恢复条件、外部检验层级、两个试验访视、投影失败分支和禁止性主张。摘要应保留会改变研究身份的边界，但不需要在第一句复现所有保护措施。

### NAR-003：关键概念早于其功能出现

结构化摘要具有背景、目标、方法、结果和贡献的外形，但方法条目用多个学科的压缩表达直接描述实现。读者交接明确不假定每位读者熟悉所有参与学科，也不假定其熟悉项目特定名称。当前顺序使读者先遇到方法标签和检验层级，之后才在数十至数百行后的协议与方法章节理解它们的作用。需要保留技术精度，同时按“问题—功能—概念—细节”的依赖关系重新排序。

### NAR-004：限制分散且反复重述

该研究文档对因果解释、外部更新、试验投影、备用端点、数据状态和创新定位的边界都写得清楚，这是重要优点；但同一完整边界在多个章节反复出现，没有形成唯一权威位置。结果是限制比研究动机更醒目，并且停止条件散布在日期表、方法、证据链、解释矩阵和风险矩阵中。修复应以合并和删除重复为主，而不是再增加一组总结。

## Preserved strengths

- 标题、研究问题、四项目标和身份锚点共同保留了发病前、首次发病、发病后与结局的全病程范围。
- 阶段 II 的公共 ICU 数据路线与阶段 III 的条件性试验再分析被明确区分，后者不会补足前者的失败。
- 观察性预测或表征与因果、控制和临床工具主张之间的边界清楚，应在合并后完整保留。
- 数据访问、可观测性、恢复、外部检验和试验语义均有可执行的停止或降级条件；修复只应改变这些内容的位置和重复程度。
- 证据链把输入、方法、输出、支持范围和失败条件对应起来，可作为重排设计理由时的内容来源。

## Handoff

See the paired `narrative-repair-plan-r001.yaml` for executable actions.
