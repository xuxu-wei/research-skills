---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-r003
review_id: narrative-review-I01-001-r003
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: idea-narrative-assessor-fresh-r003
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r003
input_artifact_ids:
  - idea-dossier-I01-001-v005
  - reader-handoff-forward-001
input_versions:
  - v005
  - v001
input_dossier:
  artifact_id: idea-dossier-I01-001-v005
  version: v005
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/idea-dossier-v005.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/idea-dossier-v005.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: major_narrative_revision
findings:
  - finding_id: NAR-001
    severity: major
    category: progressive_disclosure_and_reader_baseline
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary"
    observed_evidence: >-
      标题、完整 Idea 摘要和结构式摘要在首次出现时即依赖“候选动态系统模型”、
      “患者—时间状态及其转移”、“可恢复的状态与结构量”、“状态对齐”、
      “结构稳定性”和“冻结观测映射”等核心构念；它们的技术含义或彼此区别主要到
      “Observational model target, anchoring, and reporting”及随机试验观测映射小节才展开。
    current_reader_effect: >-
      reader handoff 只允许假定对重症研究、纵向数据、验证和观察性/干预性证据有一般了解，
      不允许假定每位读者掌握系统辨识的隐含词汇。重症医学或临床流行病学读者在首次阅读
      摘要时难以区分研究对象、模型输出、模拟恢复检验、跨库稳定性检验和条件性试验摘要，
      必须到后文寻找定义后再回读中心问题与贡献。
    target_function: >-
      在开篇首次使用处，以跨学科读者可直接理解的语言说明候选模型表示什么、
      患者—时间状态与结构量分别指什么，并预告任务表现、模型量恢复、跨数据库稳定性和
      条件性试验摘要是四个不互相替代的证据层级；后续技术小节只增加数学和实施细节。
  - finding_id: NAR-002
    severity: major
    category: repetition_navigation_and_section_function
    dossier_locator:
      section_heading: "Key techniques and implementation"
      subsection_heading: null
      content_anchor: "基于信息可用时间的标签引擎"
    observed_evidence: >-
      完整方法之后，“Key techniques and implementation”再次列出十项方法，五条
      “Evidence chains”再次列出输入、方法、输出与目标，“Required analyses and evidence”
      再次列出执行要求，“Planned outputs”再列一次产物；随后“Contribution and evidence
      ladder”与“Title and positioning claim-support table”又以两张表重述相同的研究层级、
      证据路线、输出和贡献。多个位置各自含少量独有信息，但没有一个统一的追踪入口。
    current_reader_effect: >-
      读者在已完成方法阅读后仍需多次重读同一条研究路线，并比较多个近似清单才能判断
      哪一处是方法细节、哪一处是交付要求、哪一处是贡献解释。重复不再承担新的阅读功能，
      反而掩盖了从问题到设计、证据和贡献的单一路径。
    target_function: >-
      保留一处完整方法说明和一处整合后的问题—设计—证据—输出—贡献追踪表，
      将其余清单中的独有信息迁入相应权威位置后删除重复表述，使每一节先完成标题承诺的
      唯一功能，且读者无需横向比对多个版本。
  - finding_id: NAR-003
    severity: major
    category: caveat_saturation_and_narrative_balance
    dossier_locator:
      section_heading: "Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
      content_anchor: "本小节是全文关于当前可行性、限制、解释边界、替代方案和停止条件的唯一权威位置"
    observed_evidence: >-
      dossier 虽声明该小节是限制与解释边界的唯一权威位置，但“阶段 III 不属于 24 个月最低交付且
      不能补足阶段 II 失败”、“预测或随机分组差异不等于完整因果系统”、“不主张新算法、
      数字孪生或控制模型”以及“不更新模型的外部验证不能由再校准替代”等边界，仍在摘要、
      rationale、研究问题与目标、工作包、试验方法、证伪标准、解释、贡献表、主张支持表和
      最终边界中以完整或近完整形式反复出现。
    current_reader_effect: >-
      某些短限定确实保护紧邻主张，但跨多节的完整复述使负面边界占据过多阅读注意力，
      削弱了“全病程表示—恢复检验—外部验证—条件性试验连接”的正面贡献路线，也使读者
      不易确认哪一处才是每项限制的完整权威表述。
    target_function: >-
      每项限制只保留一处完整权威说明；在标题、摘要、问题或具体设计选择旁，仅保留若删除
      就会改变紧邻主张含义的最短限定。先让读者一遍读清研究要问什么、为何重要和能贡献什么，
      再在权威小节获得完整边界、触发条件与后果。
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

判定为 `major_narrative_revision`。这份 dossier 已经建立了可辨认且完整的读者推理链：
Background 说明脓毒症的时间演变与电子健康记录发病时刻的不唯一性；Current state 区分公共
数据库、纵向模型、跨库验证和随机试验次要分析目前分别能做什么；Gap 明确提出状态与结构能否
恢复、运输并连接到稀疏试验观测；Significance 解释为何预测分数不足以及该证据对后续研究决策
的价值；Rationale 再把双时间规则、角色分离、模拟恢复、隔离外部验证和条件性试验映射逐项接回
缺口。这五个功能均非空、彼此有别，gap-to-rationale 连接也成立。

主要问题不在科学内容，而在完整稿的阅读顺序与重复结构。开篇依赖尚未按跨学科基线解释的核心
构念，迫使部分目标读者到方法段落取得定义后回读；完整方法之后又出现多组相互重叠的技术、证据、
分析、产物和贡献清单；同一组解释边界还在权威限制小节之外多次完整复述。修复需要跨节合并与删减，
而不是局部润色，因此达到重大叙事修订的程度。本评估不判断方法是否正确、证据是否充分、创新性、
影响力或可行性。

## Findings

### NAR-001 — 核心构念的首次解释晚于中心主张

开篇能够说明研究覆盖何种病程和数据层次，但“模型究竟表示什么”与“验证的不同层级为何不能互相
替代”仍需要系统辨识或潜变量建模背景才能直接解析。形式化观测方程、锚定、状态对齐和试验投影在
后文安排合理；问题在于摘要层没有先提供足以独立理解的概念桥。修复应增加早期的功能性定义，
而不把后文公式和阈值提前，也不改变任何研究对象、目标或解释边界。

### NAR-002 — 方法之后的追踪材料形成多套近似目录

“Key techniques”“Evidence chains”“Required analyses”“Planned outputs”、贡献阶梯和主张支持表
都包含有价值的追踪信息，但目前各自重述同一条路线。叙事上的问题不是篇幅本身，而是读者必须比较
多个版本才能完成一次“问题—设计—证据—输出—贡献”的映射。修复应先迁移独有信息，再删除已被
详细方法或统一追踪表覆盖的清单；不能仅再加一张总表而保留现有重复。

### NAR-003 — 完整边界在权威位置之外反复出现

阶段 III 的条件性、观察性模型的非因果边界、外部验证与更新的区别及当前定位边界都需要保留，
而且标题、摘要或具体方法旁可能需要短限定。问题在于多个章节重复了完整警示及后果，使局部功能从
解释设计转为再次防御主张。修复应保留开篇的有界正面主张、方法处直接决定设计的短条件，以及权威
限制小节中的完整版本；其余重复应删除或并入权威位置。

## Preserved strengths

- Background、Current state、Gap、Significance 与 Rationale 已形成完整且显式的五段逻辑，修订时应保持其顺序和各自功能。
- 标题、完整 Idea 摘要、主要研究问题、目标、贡献阶梯与定位主张围绕同一研究对象：脓毒症全病程患者—时间状态及转移、阶段 II 的恢复与跨库稳定性检验，以及阶段 II 成功后的条件性试验扩展。核心元素没有相互冲突。
- 摘要明确区分拟生成结果与现有发现，并已给出正面的贡献框架；修订应保留这一证据层级区分。
- 详细方法总体位于读者面对的核心问题、缺口、意义和 rationale 之后，技术深度本身适合所声明的研究受众。
- 已设立单一权威限制位置并将停止后果集中成表，这为后续去重提供了清楚的保留目标。

## Handoff

See the paired `narrative-repair-plan-r003.yaml` for executable actions.
