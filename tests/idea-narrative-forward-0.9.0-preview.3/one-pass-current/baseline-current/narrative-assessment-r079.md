---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-r079
review_id: narrative-review-I01-001-r079
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh_raw_narrative-r079
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r079
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
      content_anchor: "最近近邻使‘单个模块新颖’不可成立。"
    observed_evidence: >-
      本节依次给出脓毒症标签问题、数据库差异、相邻研究、观察性偏倚和试验数据限制，但把核心差距主要写成现有研究尚未采用同一组合；没有独立说明解决该证据差距将为所列读者带来什么科学判断或研究能力，设计选择与该意义之间的连接也分散在后续两段。
    current_reader_effect: >-
      读者能看出方案与相邻工作的差别，却需要自行推断尚不能回答的科学或证据问题、解决它的价值，以及为什么阶段 I–II 的设计正好回应这一问题。
    target_function: >-
      在本节内分别完成 Background、Current state、Gap、Significance 和 Rationale 五项功能：差距应是尚缺的知识或证据，意义应说明其对既定读者的后果，理由应把该差距直接连接到阶段 I–II 的设计。
  - finding_id: NAR-002
    severity: major
    category: progressive_disclosure_and_reader_baseline
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary"
    observed_evidence: >-
      一句话摘要在完成正向研究目标之前，同时装入绝对模拟恢复、未触碰跨数据库检验、阶段编号、冻结观测投影、访视特异随机化分析、失败后的临床状态分析以及多类禁止性解释；结构化摘要又在读者接触详细方法前使用 proper score、zero update、观测层更新等跨学科概念。
    current_reader_effect: >-
      按 handoff 所界定的跨学科读者并不共享这些概念的全部背景知识。读者第一次阅读难以复述核心问题与主要贡献，必须前往后文寻找定义后再返回标题、摘要和研究问题。
    target_function: >-
      开篇先用跨学科读者可直接理解的顺序交代问题、24 个月主要目标、价值和总体设计；只保留改变研究身份所必需的边界，把计算细节与条件分支放到首次需要它们的方法位置，并在首次必要使用时解释跨学科概念。
  - finding_id: NAR-003
    severity: major
    category: conditional_extension_prominence
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "标题和一句话摘要均把条件性稀疏 RCT 次要再分析与主要阶段并列。"
    observed_evidence: >-
      阶段 III 明确位于 24 个月最低交付之后并取决于阶段 II、试验语义和投影可用性，但其资格条件、投影分析、失败后替代分析及解释边界仍在标题、摘要、背景、研究问题、目标、时间表、数据、方法、证据链、必需分析、预期产物、证伪标准、贡献、主张核对和风险部分反复展开。
    current_reader_effect: >-
      一个后续且高度条件化的次要分析获得了与阶段 I–II 主研究近似相同的叙事重量，打断了从全病程问题到构建、恢复检验和跨数据库检验的主路线，也让读者反复核对多个版本的同一分支逻辑。
    target_function: >-
      形成清楚的阶段层级：各必需部分只保留与自身功能相关的一句或最小说明，完整的试验资格、投影、分析、替代方案和解释范围集中在 Research design and methods 的相应小节。
  - finding_id: NAR-004
    severity: major
    category: caveat_saturation_and_repetition
    dossier_locator:
      section_heading: "Evidence chains"
      subsection_heading: "Evidence chain: 可用性时钟、风险集与互斥病程"
      content_anchor: "五条证据链均设有独立的 Limits and failure conditions 字段。"
    observed_evidence: >-
      因果、机制、控制、数字孪生和临床推广边界，以及零更新失败、试验投影失败和数据语义失败的后果，在摘要、背景、非假设、方法、五条证据链、证伪标准、解释矩阵、贡献阶梯、主张核对表和风险表中多次重述。五条证据链还额外保留完整的限制字段，而第 14 节已经承担限制、风险、替代方案和停止条件的完整说明。
    current_reader_effect: >-
      防御性信息占据了本应建立动机、贡献和证据关系的空间；读者难以判断哪一处是完整限制说明，也难以区分真正不同的边界与措辞不同的重复内容。
    target_function: >-
      第 14 节完整保留所有独特限制、假设和停止条件；其他部分仅在省略会扭曲紧邻科学推理时保留自足的最小边界。证据链只保留 Input、Method / analysis / processing、Output 和 Supports 四项功能。
  - finding_id: NAR-005
    severity: minor
    category: section_function_fit
    dossier_locator:
      section_heading: "Key techniques and implementation"
      subsection_heading: null
      content_anchor: "As-of 标签引擎"
    observed_evidence: >-
      本节以十个工具或控制隐喻组织内容，主要再次概括第 7 节的科学规则；虽然零散提到若干输出，但没有稳定地区分每项分析所需的数据来源、计算关系、生成记录和复现检查。
    current_reader_effect: >-
      研究读者可以再次读到方法原则，却不能从本节单独辨认如何把时钟、队列、变量、模拟、医院分组、试验投影和不确定性分析落实为可复查的科学记录。
    target_function: >-
      以具体科学功能说明每项可复现性内容的输入、计算、输出及核查用途，使本节补充而不是复述 Research design and methods。
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

**Decision: `major_narrative_revision`.** 研究对象、24 个月阶段 I–II 目标、观察性与因果解释边界以及主要设计顺序均可辨认；问题不在科学内容缺失，而在读者必须从大量条件、限制和重复技术说明中重建主论证。当前开篇先呈现复杂条件，背景部分没有把“现有状态—未解证据问题—为什么重要—为什么采用该设计”分成可直接跟随的链条，24 个月后的条件性试验分析又在全篇获得过高且重复的篇幅。解决这些问题需要跨多个必需部分重新排序、压缩和集中，而非局部润色。

## Findings

### NAR-001 — 核心推理链没有把科学差距、意义和设计理由分开

背景部分准确提供了标签不确定性、数据库异质性、既有研究和观察性偏倚等材料，但“差距”主要落在尚未发现同一五层组合的定位上。读者仍需要补出两个关键步骤：当前证据究竟无法支持什么判断，以及得到跨数据库、可恢复的全病程表示会怎样改变后续科学判断或研究设计。本节随后直接进入模型边界和试验条件，因而方法说明部分替代了明确的意义陈述。该缺口按 rubric 属于主要问题。

### NAR-002 — 开篇把技术条件放在问题和价值之前

标题后的单句摘要试图一次容纳主要研究、所有准入条件、后续试验分支、替代端点和禁止性解释。每个限定都可能科学上必要，但它们的披露顺序使正向目标淹没在条件之中。结构化摘要继续提前使用若干仅在方法部分才能理解的跨学科概念。对于 handoff 中所列的重症医学、流行病学、纵向统计、系统辨识、医学 AI 和转化研究读者，这要求每个领域的读者默认掌握其他领域的惯例，造成明显回读。

### NAR-003 — 后续条件性试验分析挤占主要研究

全文已经明确阶段 III 不属于 24 个月最低交付，但仍多次完整解释试验资格、投影、替代端点和解释范围。研究问题、目标、时间表、证据链、输出和主张核对各自需要简短说明这一延伸如何与主要研究相连；它们不需要再次呈现完整运行逻辑。完整细节可保留在方法部分的试验小节，其余部分只保留各自不可替代的功能。

### NAR-004 — 限制和停止条件的重复削弱正向论证

对因果、机制、控制、数字孪生、临床推广、跨数据库失败和试验失败的限制在多处重复。部分边界直接支持邻近设计选择，应当留在原处；但多数重复只是再次防御同一误解。尤其是五条证据链中的独立限制字段既增加重复，也挤压 Input、Method、Output 和 Supports 的可审计关系。完整限制应集中在第 14 节，其他部分保留的每一条边界都应对紧邻推理具有不可替代作用。

### NAR-005 — 实施部分没有形成独立的复现功能

第 8 节的十项列表多数是第 7 节方法原则的改名重述。编辑修复应把这一节转换为具体可复查内容：事件时刻与信息可用时刻如何记录，变量及单位如何对应，队列与状态如何派生，模拟情景和判定标准如何保存，医院分组与跨院患者如何记录，试验锚点投影和不确定性分析如何复现。这里只要求改善读者功能，不评价这些方法是否充分。

## Preserved strengths

- 标题、研究问题、目标和核心假设对“脓毒症发病前—首次发病—发病后—结局”研究对象保持一致，修订时应保留这一主轴。
- 阶段 I–II 的时间顺序、主要任务、跨数据库检验和失败后的科学解释边界已经明确，重新排序时不应改变这些关系。
- 观察性预测或表示、随机分配比较与因果机制之间的界线清楚且重要；需要减少重复，而不是删除其科学边界。
- 两项试验分开分析、投影失败后的独立临床状态分析以及核心语义不足时停止，构成完整的条件性科学内容，应在方法部分保留。
- 五条证据链已经具备 Input、Method / analysis / processing、Output 和 Supports 四项可审计功能，压缩限制字段时应保留这四项关系。

## Handoff

See the paired `narrative-repair-plan-r079.yaml` for executable actions.
