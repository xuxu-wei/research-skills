---
schema_version: research-idea-content-preservation-check.v1
check_id: "content-preservation-check-I01-001-r005"
review_id: "content-preservation-I01-001-r005"
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: "fresh-content-preservation-reviewer-r005"
workflow_id: "RID-SEPSIS-CSM-20260717-001"
round_id: "r005"
input_artifact_ids:
  - idea-dossier-I01-001-v007
  - idea-dossier-I01-001-v008
  - protected-content-register-I01-001-v007
  - revision-delta-I01-001-v007-to-v008
input_versions:
  - v007
  - v008
  - v007
  - v008
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v007
    version: v007
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/idea-dossier-v007.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v008
    version: v008
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/idea-dossier-v008.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v007
    version: v007
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/protected-content-register-v007.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v007-to-v008
    version: v008
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/revision-delta-v007-to-v008.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/idea-dossier-v007.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/idea-dossier-v008.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/protected-content-register-v007.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/revision-delta-v007-to-v008.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-V007-001
    prior_locator: "YAML identity_anchor; Title, summary, audience, and positioning; Research question, objectives, and core hypothesis > Primary research question; Research content and work packages > Twenty-four-month minimum deliverable and dated milestones"
    revised_locator: "YAML identity_anchor; Title, summary, audience, and positioning; Research question, objectives, and core hypothesis > Primary research question; Research content and work packages > Twenty-four-month minimum deliverable and dated milestones"
    semantic_status: preserved
    evidence: >-
      v007 与 v008 的 identity_anchor 五个字段逐项相同；标题、主要问题和目标仍指向覆盖发病前、首次发病、发病后和结局的脓毒症候选动态系统模型，以阶段 I–II 的 24 个月最低交付为界。v008 在一句话摘要中展开阶段 II 的既有工作范围，并继续把阶段 III 置于全部必要证据满足之后；“Research identity and final boundary”仍明确取消全病程对象或改为普通临床预测即构成另一项研究。
  - protected_id: PCR-V007-002
    prior_locator: "YAML identity_anchor; Data, materials, and existing evidence base > Variable-role separation; Research design and methods > Protocol locks for the two primary clinical tasks; Research design and methods > Mutually exclusive post-onset state and event system"
    revised_locator: "YAML identity_anchor; Data, materials, and existing evidence base > Variable-role separation; Research design and methods > Protocol locks for the two primary clinical tasks; Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      纵向脓毒症 ICU 患者系统、患者—时间状态和状态转移的推断单位，以及患者与医院层级聚类均保持不变。v008 仅将生理测量的并列项和跨数据集合的记录单位写得更明确；两项任务的人群、风险集、延迟进入、互斥状态、患者与医院层级不确定性处理和跨分区患者规则未变。
  - protected_id: PCR-V007-003
    prior_locator: "Data, materials, and existing evidence base > Public ICU databases and planned roles; Data, materials, and existing evidence base > Trial data considered for conditional stage III analyses; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions > Current feasibility and evidence status"
    revised_locator: "Data, materials, and existing evidence base > Public ICU databases and planned roles; Data, materials, and existing evidence base > Trial data considered for conditional stage III analyses; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: >-
      文献与专家先验、MIMIC-IV、eICU-CRD、备份数据库及条件性 EXIT-SEP 和 XBJ-SCAP 数据来源均未改变。v008 继续把访问凭证、协议、提取记录和双数据库实际支持列为未核验或尚未生成，把本地试验材料限定为不能替代授权与原始试验文件，并保留全部试验样本与访视信息；没有把待审计、未核验或计划状态改写成已经具备或完成。
  - protected_id: PCR-V007-004
    prior_locator: "Research content and work packages; Research design and methods; Expected outputs, falsification criteria, and interpretations > Scientific falsification criteria; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions > Operational thresholds, alternatives, and stop conditions"
    revised_locator: "Research content and work packages; Research design and methods; Expected outputs, falsification criteria, and interpretations > Scientific falsification criteria; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions > Operational thresholds, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      阶段顺序、五个工作包、两项主要任务、状态占用概率与转移概率等估计目标、模拟恢复、按医院隔离的跨数据库验证、条件性试验分析及阶段依赖均保持。逐行核对后，时间窗、事件与转移支持、状态维度与切换机制、随机种子、恢复率、校准、外部对齐、观测映射和试验分析的全部数值阈值、触发条件与后果均未改变。v008 对状态对齐、关系系数正负号、第一奇异轴选定对象和表格层级的说明，均展开 v007 已有的排列与符号变换、结构边与符号分离以及既定映射规则；未增加或删除方法承诺。
  - protected_id: PCR-V007-005
    prior_locator: "Structured abstract; Expected outputs, falsification criteria, and interpretations > Planned outputs; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions > Current feasibility and evidence status"
    revised_locator: "Structured abstract; Expected outputs, falsification criteria, and interpretations > Planned outputs; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: >-
      v008 仍将模型、恢复、临床任务、外部验证和试验分析表述为计划产物或尚未生成的结果，并保留对有界整合、验证、研究基准和资源建设的限定。将“任务效度”改为“任务级预测表现”没有提升证据层级；标题支持状态、最接近工作置信限定、现有证据状态和所有条件性表述均未加强。
  - protected_id: PCR-V007-006
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      v008 继续规定该小节为当前可行性、限制、解释边界、替代方案和停止条件的统一依据。该权威位置中的资源状态、七项科学与解释边界、人员与模型范围，以及操作表的每一项阈值、风险、替代方案和停止后果均保留。v007 最终身份段重复的“阶段 III 不能补足阶段 II 失败”一句在 v008 删除，但同一权威位置的“Scientific and interpretive boundaries”第 7 项完整保留该限制，且摘要仍保持阶段 III 的条件性，因此限制只在权威位置保留一次而未被弱化。
  - protected_id: PCR-V007-007
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions > Scientific and interpretive boundaries; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions > Research identity and final boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions > Scientific and interpretive boundaries; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions > Research identity and final boundary"
    semantic_status: preserved
    evidence: >-
      观察性关联和预测表现仍明确不识别治疗因果效应、真实反馈网络或反事实策略；随机试验分支仍不验证未测潜在动力学、状态转移边、中介机制、个体控制或完整动态系统，也不支持无条件临床推广。新算法、全球首次、数字孪生、控制模型、已验证临床决策工具和药物平台等禁止主张，以及试验数据语义与外部适用性边界均保持不变；v008 未新增这些范围外的主张。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

七个受保护条目在 v008 中均可追溯，并保持 v007 的研究身份、对象与范围、输入和资源状态、设计与分析承诺、证据状态、主张强度、限制、替代方案、停止条件和禁止主张。修订差异均属于定义澄清、术语替换、局部展开、表格重排或重复限制的集中保留；修订说明未声明科学变化，逐项比较也未发现未声明的科学变化。因此决定为 `scientific_content_preserved`。

## Protected-content trace

主要非平凡移动或合并发生在第 14 节的限制表达：v007 最终身份段中重复的阶段 II—III 失败边界被删除，但其完整含义仍在同一权威小节的“Scientific and interpretive boundaries”第 7 项保留。其余变化没有移动受保护内容：阶段标签在摘要中展开；状态占用概率、状态对齐、观测方程和关系正负符号在首次使用处定义；操作阈值表只拆分触发条件与对应后果。七个条目的修订后位置已在前述逐项检查中记录。

## Required routing

该 dossier 可进入全新的叙事评估与语言评估实例；本报告只确认受保护科学内容的保留，不对科学设计正确性作判断。
