---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-v043-r071
review_id: narrative-review-I01-001-v043-r071
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-narrative-v043-r071
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r071
input_artifact_ids:
  - idea-dossier-I01-001-v043
  - reader-handoff-forward-001
input_versions:
  - v043
  - v001
input_dossier:
  artifact_id: idea-dossier-I01-001-v043
  version: v043
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v9/idea-dossier-v043.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v9/idea-dossier-v043.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: major_narrative_revision
findings:
  - finding_id: NAR-001
    severity: major
    category: "条件性扩展权重失衡"
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "标题和以“本研究计划在 24 个月内”开头的 One-sentence complete-Idea summary，以及后续各节反复展开的阶段 III 规则"
    observed_evidence: "随机对照试验次要分析被明确界定为 24 个月主体研究之外的条件性阶段 III，但其资格条件、替代分析路径和解释边界在标题、摘要、研究问题、目标、工作包、数据说明、方法、必需分析、产物、贡献、主张支持表、资源、待定规范、限制和风险中反复展开；完整技术逻辑没有只由一个技术位置承担。"
    current_reader_effect: "读者会把条件性阶段 III 视为与阶段 I–II 并列的主体研究，并需要在多个章节之间往返核对何处才是资格、实施、替代和解释规则的权威陈述；24 个月内关于候选表征的数据支持、模拟重建与跨数据库检验因此失去应有的叙事中心。"
    target_function: "让阶段 I–II 成为明确的主线，在一个技术权威位置保留阶段 III 的完整规则，其余必需章节只保留完成各自问题、目标、证据链、产物或主张审计功能所需的最短陈述。"
  - finding_id: NAR-002
    severity: minor
    category: "摘要限定语堆叠"
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary 中从“本研究计划在 24 个月内”到“两项试验访视摘要差异”的整句"
    observed_evidence: "单句同时承载数据来源、候选表征定义、四段病程范围、模拟与跨数据库检验、证据与论文及资源交付，以及两项试验的访视日、稀疏测量和一维摘要比较。"
    current_reader_effect: "跨学科读者虽能找到所有要素，却难以在一次阅读后复述主体问题与主要贡献；交付物和下游条件在主目标完成前占用了注意力。"
    target_function: "先直接陈述 24 个月主体研究要学习和检验什么，再以一个从属短语标示条件性阶段 III，把交付物清单和试验操作细节留给各自章节。"
  - finding_id: NAR-003
    severity: minor
    category: "核心概念首次定义顺序"
    dossier_locator:
      section_heading: "Structured abstract"
      subsection_heading: null
      content_anchor: "Objective and hypothesis 与 Contribution and impact 中首次出现的“锚定规则”和“合取证据框架”"
    observed_evidence: "“模拟重建性能”在总述和摘要中先于 Rationale 的解释出现；“锚定规则”在摘要中承担核心假设条件但没有面向跨学科读者的首用解释；“合取证据框架”直到后文“阶段 II 的合取成功定义”才明确为所有组成项必须同时满足且不能互相补足。"
    current_reader_effect: "重症医学、临床流行病学或其他非系统辨识读者必须暂存这些项目特定概念，随后向后寻找其含义，才能完整理解摘要中的假设和贡献。"
    target_function: "在首次承担核心推理功能时，用简短自然语言说明模拟重建、锚定和合取判定各自意味着什么；后文技术定义再增加精度，而不是补上先前缺失的前提。"
  - finding_id: NAR-004
    severity: minor
    category: "限制重复与章节功能偏移"
    dossier_locator:
      section_heading: "Required analyses and evidence"
      subsection_heading: null
      content_anchor: "分析清单之后以“最接近工作综合已经更新至 2026-07-17”开头的段落"
    observed_evidence: "最接近工作检索的边界出现在必需分析章节，随后又在贡献比较、主张支持表和完整限制章节中陈述；“结果尚未生成”、阶段 III 不能补足阶段 II、以及不能提高为因果或整体表征验证等边界，也在不承担新增局部功能的资源或收束段落中重复。"
    current_reader_effect: "必需分析、资源和风险章节被防御性说明打断，完整限制的权威位置变得不够唯一；读者需要分辨哪些重复句是新规则，哪些只是已有边界的再次陈述。"
    target_function: "让每个非限制章节只保留直接支持其局部设计或解释所必需的自足边界，并让 Limitations and boundary conditions 成为唯一完整的限制与假设权威位置，不用指针替代任何确有必要的局部边界。"
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

五段读者推理链完整且顺序合理：Background 建立脓毒症时间标签问题，Current state 说明现有纵向、动态和跨数据库工作能回答什么，Gap 把未决问题限定为候选表征能否获得数据支持、模拟重建并保持跨数据库稳定，Significance 说明该判断为何影响后续取舍，Rationale 则把双时间、状态—行动—观察分离、模拟检验和隔离的外部检验连接到缺口。标题、摘要、研究问题、目标和贡献也指向同一研究对象、数据基础与患者—时间推断单位。

当前不能判为叙事就绪，原因不是五段逻辑缺失，而是条件性阶段 III 的完整操作和防御逻辑跨多个章节重复展开。它被 dossier 自身界定为 24 个月最低交付之外，却获得了接近主体研究的篇幅与层级权重。要恢复清晰的读者路线，需要跨章节合并和删减，而不是只在一两句上润色，因此决定为 `major_narrative_revision`。

## Findings

### NAR-001 — 条件性阶段 III 获得过高叙事权重

阶段 III 可以出现在标题、问题、目标、证据链、产物和主张审计中，因为它是研究身份的一部分；问题在于这些位置之外还反复重述其共同资格、观测映射是否成立时的两条替代路径、试验语义不足时的停止路径，以及不能反向验证或补足阶段 II 的解释边界。完整方法小节本已具备承担这些规则的条件，其他章节只需保留各自功能所要求的输入、动作、输出或边界。修复必须保留全部科学条件与两项试验的独立性，但应消除重复展开。

### NAR-002 — 顶部总述难以一次提取主旨

One-sentence complete-Idea summary 的每个成分都与 dossier 有关，但它把研究对象、验证路线、产物、发表方向和下游试验细节放在同一个长句中。读者在遇到主要问题之后立即被交付和条件占据，难以形成“先审计支持，再检验可重建性，最后做隔离的跨数据库检验”的主体路线。该问题可通过重排与压缩解决，不需要改变研究身份。

### NAR-003 — 三个核心概念需要在首次使用时获得跨学科解释

候选表征本身在顶部得到了定义，双时间和状态—行动—观察分离也在五段逻辑中及时解释，这是可保留的做法。相较之下，模拟重建性能、锚定规则和合取证据框架在摘要承担推理作用时仍依赖后文说明。修复应补充简短的首次定义，不要求降低后续技术精度，也不涉及术语是否标准或是否需要更换。

### NAR-004 — 少数防御性段落离开了最合适的章节功能

最清楚的例子是 Required analyses and evidence 末尾的最接近工作检索边界：它不是该节要求形成的分析证据，且在贡献比较、主张审计和限制章节已有更合适的位置。类似地，资源或末尾收束位置再次陈述“尚无结果”或“阶段 III 不能补足阶段 II”时，没有总是增加新的资源决定或风险后果。应删除无新增功能的复述，同时保留问题与因果问题的必要区分、方法中的操作性停止规则、解释矩阵、主张审计和风险表各自不可替代的功能。

## Preserved strengths

- Background、Current state、Gap、Significance 和 Rationale 五项功能均非空、相互区分并形成因果顺序；Gap 没有被写成“尚无相同模块组合”的新颖性辩护。
- 标题、摘要、主要研究问题、四项目标和贡献陈述的核心要素相容，均把阶段 I–II 置于公共 ICU 数据、患者—时间状态与状态转移、模拟重建和跨数据库检验之上，并把试验分析写成有条件的后续部分。
- 正向主张是可辨认的：研究希望形成可审计的全病程表征验证路径、基准和可复用资源；限制并未完全取代问题、意义或设计理由。
- Research design and methods 已提供阶段 III 完整技术逻辑的自然权威位置；Evidence chains、Required analyses、Expected outputs、解释矩阵和 Claim-Support 表也分别承担可审计的必要功能，修复时不应合并或删除这些合同功能。
- Limitations and boundary conditions 已作为完整限制章节存在。修复重点是让其他位置只保留真正推动局部推理的边界，而不是再建立第二份完整限制清单。

## Handoff

See the paired `narrative-repair-plan-r071.yaml` for executable actions.
