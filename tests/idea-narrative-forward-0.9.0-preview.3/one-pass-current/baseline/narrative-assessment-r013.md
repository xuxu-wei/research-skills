---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-r013
review_id: narrative-review-I01-001-r013
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-narrative-assessor-r013
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r013
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
      content_anchor: "从“脓毒症随时间形成”到“任何结果均不支持无条件国际临床推广”的五段正文"
    observed_evidence: >-
      本节说明了脓毒症标签与照护过程的复杂性，概述了近邻工作，并给出观察性建模和试验投影的设计理由；但没有单独说明，当前证据缺口若被弥合，将如何改善这些跨学科读者对全病程表示、跨数据库稳定性或后续研究决策的认识。五项承诺的功能也没有以五个 H3 小节显式区分，第三段从近邻工作直接转入“本项目的可辩护空间”，把科学缺口、贡献定位和方案概述压在同一段中。
    current_reader_effect: >-
      读者可以辨认研究对象和若干方法动机，却必须自行推断为什么这个尚未解决的问题值得投入，以及所提设计如何逐项回应该问题；论证从“已有工作”到“为何重要”再到“为何采用此设计”的关键连接不完整。
    target_function: >-
      以明确且相互区分的 Background、Current state、Gap、Significance 和 Rationale 五个 H3 功能建立完整推理链，并在不新增科学主张的前提下明确研究意义及缺口到设计的对应关系。
  - finding_id: NAR-002
    severity: major
    category: core_element_alignment
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "Title、One-sentence complete-Idea summary 与 Positioning and contribution frame 三个条目"
    observed_evidence: >-
      标题、单句摘要和定位均把 24 个月阶段 I–II 的候选表征与跨数据库检验，同 24 个月后、需要额外语义与投影条件的 RCT 次要再分析并列呈现。相同的并列结构延续到主研究问题的第三分句和第四项目标，而后文才说明阶段 III 不属于 24 个月最低交付，也不能补足阶段 II 失败。
    current_reader_effect: >-
      在最需要建立研究身份的位置，读者难以迅速判断主要研究究竟是 24 个月的全病程表征与跨数据库检验，还是还包括一个共同定义研究成功的 RCT 分析；条件性扩展占据的叙事权重超过其在计划中的依赖地位。
    target_function: >-
      让标题、摘要、主问题和目标首先一致地呈现阶段 I–II 的核心研究，再把阶段 III 标示为依赖核心结果、位于最低交付之外且不参与阶段 II 成功判定的后续扩展，同时保留两项试验及其分支的全部科学内容。
  - finding_id: NAR-003
    severity: major
    category: narrative_balance_and_repetition
    dossier_locator:
      section_heading: "Evidence chains"
      subsection_heading: "五条 Evidence chain"
      content_anchor: "每条证据链末尾的“Limits and failure conditions”字段，以及前后章节重复出现的因果、控制、数字孪生、投影失败和零更新边界"
    observed_evidence: >-
      因果识别、控制或数字孪生不成立，RCT 失败分支不得验证阶段 II，有限更新不得替代零更新等边界，在标题摘要、结构化摘要、核心非假设、方法、五条证据链、必需分析、否证标准、解释矩阵、贡献阶梯、主张支持表和风险矩阵中反复陈述。五条证据链还各自包含独立的链级限制字段，而完整限制本应由第 14 节统一承担。
    current_reader_effect: >-
      否定性边界持续打断问题、设计和预期贡献的正向推进，读者必须反复处理相同警示，且难以判断哪一处是完整且权威的限制说明；证据链的 Input、Method、Output、Supports 四个审计功能也被额外的限制字段稀释。
    target_function: >-
      将完整限制、假设和停止边界集中到第 14 节；其他必需章节只保留为理解紧邻设计选择所不可缺少的一句局部边界，并移除五条证据链的独立限制字段，同时保持每个必需章节及证据链的独特功能。
  - finding_id: NAR-004
    severity: major
    category: progressive_disclosure_and_concept_burden
    dossier_locator:
      section_heading: "Structured abstract"
      subsection_heading: null
      content_anchor: "Objective and hypothesis、Approach 与 Contribution and impact 条目首次集中出现 recovery、G1、zero update、observation-layer update 和 projection 等概念"
    observed_evidence: >-
      开篇摘要在解释研究问题和设计轮廓之前，集中使用“绝对恢复/假置信门”“G1”“landmark”“zero update”“仅观测层更新”“冻结观测投影”“death-ranked SOFA”等跨学科读者未必共享的概念。部分术语到 Data 或 Methods 章节才获得操作性说明，G1、R0、R1 等标签还承担了主要导航作用。
    current_reader_effect: >-
      读者需要越过多个尚未定义的机制和项目标签才能识别研究的基本路线，并需在后文查找定义后再回到摘要解释早期主张；这增加了不必要的回读，也使核心问题被实现细节遮蔽。
    target_function: >-
      在首次使用时以跨学科可理解的语言定义确有必要的核心概念，或在开篇先使用其科学功能描述、到相应方法节再引入缩写和技术标签；阈值、映射和实现细节仍完整保留在后续专门章节。
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

该 dossier 的科学边界和实施条件记录充分，但当前阅读路径需要实质性重组。读者能够找到研究问题、两项主要任务、跨数据库检验和条件性试验扩展，却不能在开篇顺畅完成“问题—现状—缺口—意义—设计理由”的推理：意义功能没有明确承担者，阶段 III 在标题与摘要中的权重又使核心研究身份变得含混。与此同时，大量重复限制和提前出现的项目标签，使读者在理解正向论证前先处理实现条件与否定性边界。

因此，本次判定为 `major_narrative_revision`。修订应调整信息层级、恢复五项论证功能、集中限制说明并前置必要定义；不需要改变研究问题、数据来源、设计、阈值、分析分支或科学边界。

## Findings

### NAR-001 — 研究意义及缺口到设计的连接不完整

第 3 节的前两段能够建立脓毒症时间性问题和跨数据库差异，第三段能够说明单个模块已有近邻，后两段能够解释为何需要观察过程建模和受限的试验投影。但本节没有回答“若解决所述缺口，相关读者将获得什么目前缺失的判断能力或证据”，也没有把每项设计选择明确回连到一个先前陈述的缺口。由于五个功能未被显式分开，贡献定位代替了意义说明，方法理由则与限制交织。修订应恢复五个 H3 功能，并使每个设计理由都有可辨认的缺口来源。

### NAR-002 — 核心研究与条件性扩展的叙事层级不一致

后文对阶段边界的说明是清楚的：阶段 I–II 构成 24 个月最低交付，阶段 III 位于其后且不能补救阶段 II 失败。然而，标题、单句摘要、主问题和目标把两者并列，读者直到工作包和日期门才获知真实依赖关系。这不是删除 RCT 内容的理由；需要调整的是出现顺序和权重，使核心研究身份先稳定，再介绍有条件的后续用途。

### NAR-003 — 重复限制压过正向论证，且缺少单一权威位置

多处边界对于科学解释是必要的，但目前同一边界在许多必需章节中完整重述。尤其是五条证据链的独立限制字段，与后续否证标准、解释矩阵和风险矩阵承担了重叠功能。修订应保留各必需章节的合同功能，例如方法规范、证据可追溯、分析验收、计划产物和主张审计，不能用一个总表替代；可以删除的是这些功能内部重复的完整限制说明。第 14 节应成为完整限制与假设的唯一权威位置，局部只保留直接解释紧邻设计决策所需的边界。

### NAR-004 — 核心概念的解释顺序要求读者回读

该 dossier 面向多个学科，不宜假定每位读者都熟悉所有纵向建模、系统辨识和试验再分析术语。摘要目前同时承担技术协议浓缩与研究导航，导致核心路线被缩写、门槛标签和映射名称包围。修订不需要替换或裁定术语是否标准，而应解决理解顺序：开篇先说明各步骤的科学功能，在首次必要使用时给出简明定义，再把完整参数化与阈值留给 Data、Methods 和 Required analyses。

## Preserved strengths

- 研究对象、推断单位、两项主要临床任务和 24 个月阶段 I–II 边界保持一致。
- 观察性预测与因果推断、冻结外部检验与后续适配、阶段 II 与试验扩展之间的科学边界明确，修订只需减少重复并改善放置位置。
- 日期门、降级路线、跨数据库隔离、试验投影失败分支和停止条件均具有可审计性，应完整保留其科学内容。
- 五条证据链已有明确的 Input、Method / analysis / processing、Output 和 Supports，可在移除链级重复限制后继续承担可追溯功能。
- 贡献定位保持克制，未把计划性工作写成已获得的结果，也未依赖“首次”主张。

## Handoff

See the paired `narrative-repair-plan-r013.yaml` for executable actions.
