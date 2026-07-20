---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-r008
review_id: narrative-review-I01-001-r008
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: v009-narrative-assessor-r008
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r008
input_artifact_ids:
  - idea-dossier-I01-001-v009
  - reader-handoff-forward-001
input_versions:
  - v009
  - v001
input_dossier:
  artifact_id: idea-dossier-I01-001-v009
  version: v009
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: minor_narrative_revision
findings:
  - finding_id: NAR-001
    severity: minor
    category: progressive_disclosure
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "Three-stage map: 阶段 I 为月 0–6 的资源准备"
    observed_evidence: "标题之后首先出现完整的三阶段排期和准入条件，早于完整构想摘要、受众定位与概念桥；该条目首次引入 WP1–WP5、五类必要证据、状态对齐、预设结构稳定性和共同观测映射资格，其中多项概念要到后文才获得解释。"
    current_reader_effect: "具备一般重症研究与纵向数据背景、但并非精通全部参与学科的读者，需要先记住项目缩写、技术对象和多重条件，之后才能得知研究究竟要回答什么、主要贡献是什么以及阶段 III 为何只是条件性延伸。"
    target_function: "开篇应先建立研究问题、24 个月核心边界、贡献定位和最低限度的跨学科概念，再提供阶段级导航；工作包对应关系和完整准入条件应在其专门章节中承担权威说明功能。"
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

结论为 `minor_narrative_revision`。当前 dossier 已经建立了可跟随的主要论证路线：研究背景说明电子健康记录中的脓毒症发病时刻为何需要可追溯定义；现状概括了已有纵向、多状态、动态表型、跨数据库验证和随机试验次要分析；缺口明确区分状态与结构恢复、跨数据库稳定性以及条件性试验观测连接；意义说明这些证据层级为何需要分开评价；设计依据随后逐项连接时间规则、变量角色分离、模拟恢复、隔离外部验证和冻结观测映射。主要问题不在论证链缺项，而在开篇披露顺序。

标题下的长篇三阶段条目先于完整构想摘要和概念桥，使读者在尚未掌握研究主线时先处理工作包编号、五类准入证据及数个跨学科技术对象。这个负担局限在开篇，可通过重新排序并把详细门槛集中到既有的研究内容与工作包章节解决；无需改变主要研究问题、目标、假设、数据、方法、阈值或解释边界。

## Findings

### NAR-001 — 开篇阶段图早于研究主线和必要定义

“Three-stage map”在标题后立即给出阶段 I–III、WP1–WP5、阶段 II 五类必要证据以及试验语义和观测映射资格。读者要到随后的完整构想摘要、概念桥、结构化摘要和方法章节，才依次获得研究对象、四类证据的区别以及状态对齐、预设结构稳定性和观测映射的含义。对所声明的跨学科受众而言，这形成了不必要的前置概念负担和短距离回读。

修订应保持同一必需 H2 章节及全部阶段事实，但让完整构想摘要、受众与贡献定位以及概念桥先发挥导向作用。开篇只需承担阶段级导航；工作包编号、五类必要证据的完整枚举和技术准入条件继续由“Research content and work packages”及其后相关专门章节权威承载。

## Preserved strengths

- “Background / Current state / Gap / Significance / Rationale”五个功能均存在、非空且彼此有明确分工；尤其是 Rationale 已把每个缺口连接到相应设计选择。
- 标题、完整构想摘要、主要研究问题、四项目标和核心假设围绕同一全病程对象与阶段 II 主线；阶段 III 始终被标为阶段 II 成功后的条件性延伸。
- 开篇概念桥及后续首次使用处的括注，为状态占用概率、共同生理锚点预测和状态对齐提供了跨学科入口；修订时应保留这些定义功能。
- Evidence chains、Required analyses、Planned outputs、Contribution ladder 和 Claim-Support 表分别承担来源追踪、验收、产物、贡献解释和主张审计功能，不应因压缩开篇而合并或删除。
- “Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions”已经形成唯一的完整限制与停止条件位置；其他章节中直接解释局部设计选择的必要边界可以保留。

## Handoff

See the paired `narrative-repair-plan-r008.yaml` for executable actions.
