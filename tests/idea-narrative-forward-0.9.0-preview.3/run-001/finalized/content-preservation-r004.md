---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-check-I01-001-r004
review_id: content-preservation-I01-001-r004
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: idea-narrative-assessor-preservation-v007-r004
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r004
input_artifact_ids:
  - idea-dossier-I01-001-v006
  - idea-dossier-I01-001-v007
  - protected-content-register-I01-001-v006
  - revision-delta-I01-001-v006-to-v007
input_versions:
  - v006
  - v007
  - v006
  - v001
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/idea-dossier-v006.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v007
    version: v007
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/idea-dossier-v007.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/protected-content-register-v006.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v006-to-v007
    version: v001
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/revision-delta-v006-to-v007.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/idea-dossier-v006.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/idea-dossier-v007.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/protected-content-register-v006.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/revision-delta-v006-to-v007.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-V006-001
    prior_locator: >-
      YAML identity_anchor; Title, summary, audience, and positioning;
      Research question, objectives, and core hypothesis > Primary research question
    revised_locator: >-
      YAML identity_anchor; Title, summary, audience, and positioning;
      Research question, objectives, and core hypothesis > Primary research question
    semantic_status: preserved
    evidence: >-
      v006 与 v007 的 primary_research_question、primary_objective、study_object、
      core_data_or_evidence_base 和 primary_unit_of_inference 完全一致，H1、标题、
      24 个月内完成阶段 I–II 的摘要表述及候选动态系统模型定位也未改变。v007
      仅将主要问题拆句，并把原有“锚点预测”统一为已定义的“共同生理锚点预测”；
      发病前、首次发病、发病后至结局的连续体、跨数据库检验和阶段 III 条件性均保留。
  - protected_id: PCR-V006-002
    prior_locator: >-
      YAML identity_anchor; Research design and methods > Protocol locks for the two
      primary clinical tasks; Research identity and final boundary
    revised_locator: >-
      YAML identity_anchor; Research design and methods > Protocol locks for the two
      primary clinical tasks; Research identity and final boundary
    semantic_status: preserved
    evidence: >-
      v007 原样保留 longitudinal sepsis-centered ICU patient system、患者—时间状态与
      状态转移的主要推断单位，以及患者和医院聚类要求。两项主要任务的人群、风险集、
      事件时间、信息可用时间、预测时点、重复窗口和聚类处理均未改变；事件时间单元格
      仅拆句和换行。最终边界仍规定改变研究对象、核心证据基础或主要推断单位即构成另一项研究。
  - protected_id: PCR-V006-003
    prior_locator: >-
      Data, materials, and existing evidence base; Feasibility, resources, risks,
      alternatives, and stop conditions > Authoritative limitations, feasibility
      findings, interpretation boundaries, alternatives, and stop conditions >
      Current feasibility and evidence status
    revised_locator: >-
      Data, materials, and existing evidence base; Feasibility, resources, risks,
      alternatives, and stop conditions > Authoritative limitations, feasibility
      findings, interpretation boundaries, alternatives, and stop conditions >
      Current feasibility and evidence status
    semantic_status: preserved
    evidence: >-
      文献与专家先验、MIMIC-IV、eICU-CRD、备份数据库及条件性 EXIT-SEP、XBJ-SCAP
      数据角色和数值记录保持不变。v007 仍将访问凭证与协议列为“未核验”、双数据库
      实际支持列为“尚未生成”、试验共同生理观测指标列为“未核验”，并继续说明本地
      衍生材料不能替代授权、原始表格、统计分析计划和关键语义核验；没有把候选或条件性
      资源写成已经具备。
  - protected_id: PCR-V006-004
    prior_locator: >-
      Research content and work packages; Research design and methods; Expected
      outputs, falsification criteria, and interpretations > Scientific falsification criteria
    revised_locator: >-
      Research content and work packages; Research design and methods; Expected
      outputs, falsification criteria, and interpretations > Scientific falsification criteria
    semantic_status: preserved
    evidence: >-
      阶段 I–II 的 24 个月顺序、阶段 III 的后置依赖、五个工作包、两项主要任务和两项
      次要表征诊断均保持。v007 保留同一估计对象、模拟机制、跨数据库按医院隔离验证、
      条件性试验映射、科学证伪标准及全部数值阈值；“自助法保留率”只被展开为预设状态
      或结构边在全部重复中的保留比例，80% 阈值未变。缺失随机基线与选择模型基线的
      并列表述消除了原句歧义，原有两类模型、偏移网格、选择模型临界点和报告要求均未增删。
  - protected_id: PCR-V006-005
    prior_locator: >-
      Structured abstract; Expected outputs, falsification criteria, and interpretations >
      Planned outputs; Contribution, innovation, impact, application, and closest-work
      comparison > Contribution and evidence ladder; Current feasibility and evidence status
    revised_locator: >-
      Structured abstract; Expected outputs, falsification criteria, and interpretations >
      Planned outputs; Contribution, innovation, impact, application, and closest-work
      comparison > Contribution and evidence ladder; Current feasibility and evidence status
    semantic_status: preserved
    evidence: >-
      v007 仍把标签、审计、模型、模拟恢复、主要任务、外部验证和试验分析全部标为
      “计划生成”或“尚未生成”，摘要也明确“这些均为拟生成的结果”。贡献继续限定为
      有界的证据整合、验证、研究基准和资源建设，五层证据及支持状态未提升；有界检索
      对完整组合缺口仍仅为低至中等置信。术语和参考文献注释改写没有把有限核验写成完整核验。
  - protected_id: PCR-V006-006
    prior_locator: >-
      Feasibility, resources, risks, alternatives, and stop conditions > Authoritative
      limitations, feasibility findings, interpretation boundaries, alternatives, and
      stop conditions
    revised_locator: >-
      Feasibility, resources, risks, alternatives, and stop conditions > Authoritative
      limitations, feasibility findings, interpretation boundaries, alternatives, and
      stop conditions
    semantic_status: preserved
    evidence: >-
      v007 原样声明该小节是当前可行性、限制、解释边界、替代方案和停止条件的唯一完整
      权威位置。资源风险、所有触发阈值和对应后果均保留；若试验语义、共同观测变量或
      观测映射资格失败，停止一维状态摘要分析、转入合格的独立 SOFA 分析或停止两者的
      路径被写得更明确，但没有删除或弱化条件。阶段 III 仍位于 24 个月最低交付之外，
      且不能补足阶段 II 的任何失败。
  - protected_id: PCR-V006-007
    prior_locator: >-
      Feasibility, resources, risks, alternatives, and stop conditions > Authoritative
      limitations, feasibility findings, interpretation boundaries, alternatives, and
      stop conditions > Scientific and interpretive boundaries; Research identity and final boundary
    revised_locator: >-
      Feasibility, resources, risks, alternatives, and stop conditions > Authoritative
      limitations, feasibility findings, interpretation boundaries, alternatives, and
      stop conditions > Scientific and interpretive boundaries; Research identity and final boundary
    semantic_status: preserved
    evidence: >-
      七条科学与解释边界在 v007 中完整保留：观察性关联和预测不识别治疗因果效应、真实
      反馈网络或反事实策略；试验分支不验证未测动力学、状态转移边、中介机制、个体控制
      或完整动态系统，也不支持无条件临床推广。新算法、全球首次、数字孪生、控制模型、
      已验证临床决策工具和药物平台仍明确不作主张；最终边界仅拆句，禁止主张范围未改变。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

7 个冻结保护项在 v007 中均可按同一含义、状态或主张强度追溯。修订差异声明本轮没有科学内容、方法、阈值或主张强度变化；逐项比较亦确认改动限于术语定义与统一、句法拆分、自然语言替换、表格换行以及既有条件和后果的显式化。未发现研究身份漂移、未声明的科学变化、已完成状态的虚增、限制弱化或条件性关系改变。

## Protected-content trace

- “锚点预测”“锚点层预测”和相关泛称统一为“共同生理锚点预测”，并在概念桥中说明其与共同观测指标的关系；恢复对象和评价对象未变。
- “运输性”等表达改为模型跨数据库可迁移性或外部适用性；按医院隔离、不更新模型的主要外部验证及有限更新层级未变。
- 独立临床状态分支明确写为独立 SOFA 临床状态分析，且停止条件逐一指明一维状态摘要与独立 SOFA 分支；原有资格、替代路径和停止后果未变。
- 第 14 节继续集中承载完整限制、可行性状态、解释边界、替代方案和停止条件，没有把这些内容移出权威位置。

## Required routing

科学内容保真检查通过。v007 可进入新的叙事与学术语言评估；本报告不评价其科学设计是否正确，也不评价叙事或语言质量。
