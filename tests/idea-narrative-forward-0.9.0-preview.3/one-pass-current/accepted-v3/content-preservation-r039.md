---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-v027-r039
review_id: content-preservation-r039
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-r039
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r039
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v027
  - protected-content-register-I01-001-v003-r003
  - revision-delta-I01-001-v003-to-v027
input_versions:
  - v003
  - v027
  - r003
  - v003-to-v027
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v027
    version: v027
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v3/idea-dossier-v027.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v027
    version: v003-to-v027
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v3/revision-delta-v003-to-v027.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v3/idea-dossier-v027.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v3/revision-delta-v003-to-v027.md
scope:
  project_inputs: exactly_the_four_declared_files
  prohibited_project_artifacts_read: false
  assessor_resources_read:
    - AGENTS.md
    - research-skills-openai/skills/idea-narrative-assessor/SKILL.md
    - research-skills-openai/skills/idea-narrative-assessor/references/content-preservation-contract.md
    - research-skills-openai/skills/idea-narrative-assessor/templates/content-preservation-check.md
    - research-skills-openai/skills/idea-narrative-assessor/templates/protected-content-register.yaml
    - research-skills-openai/skills/idea-narrative-assessor/scripts/validate_narrative_outputs.py
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    semantic_status: preserved
    evidence: "发病前在险时段、首次发病、发病后演化与结局的连续体及候选动态系统表征仍是核心问题；文本没有退化为普通预测或泛 ICU 风险分层。"
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; Research content and work packages; Required analyses and evidence（无高水平论文交付方向的对应位置）"
    semantic_status: changed
    evidence: "24 个月阶段 I–II、文献与专家知识约束、公共 ICU 数据、系统辨识和跨数据库验证均被保留；但冻结登记表明确保护的高水平论文交付方向在 v027 中没有对应表述。revision delta 所引第 5 节和第 12 节仅保留研究顺序、可核验分析记录和可复用资源，不能替代该交付目的。"
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods > Protocol specifications for the two primary clinical tasks; Observational estimand, anchoring and abstention"
    semantic_status: preserved
    evidence: "纵向脓毒症 ICU 系统、可比较的未发病在险时段、发病后轨迹，以及按患者和医院聚类的患者—时间状态与状态转移均保持不变。"
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and dual-database support audit; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions"
    semantic_status: preserved
    evidence: "文献与专家知识、MIMIC-IV、eICU-CRD 及预指定 HiRID 或 AmsterdamUMCdb 备份均保留；数据库存在和版本仍是已核验，而访问凭证、数据使用协议、可运行提取、项目队列支持、具名人员和模型结果仍分别为尚未核验或尚未生成。"
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Existing randomized-trial derivative evidence; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 6"
    semantic_status: preserved
    evidence: "EXIT-SEP 与 XBJ-SCAP 仍仅是条件性阶段 III 的潜在个体级来源；本地衍生报告没有被提升为个体数据授权或原始 CRF/SAP、随机化、中心、访视及结局语义的核验证据。"
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring and abstention"
    revised_locator: "Research content and work packages > Work packages and minimum route; Research design and methods > Variable-use rules; Observational estimand, anchoring and abstention; Absolute simulation and semi-synthetic recovery criteria"
    semantic_status: preserved
    evidence: "审计、标签与状态和医院拆分、简单基线、模拟恢复、至多一个复杂候选、两项主要任务和两项次要诊断、开发方案确定、隔离外部验证、条件性试验分析的顺序不变。生理状态、治疗行动和观测过程仍分离；20 个随机种子对齐 90%、bootstrap 保留 80%、外部符号一致 80%、状态对齐 0.70 和区间校准的删除、合并或限定规则均保留，预测优势仍不能替代结构证据。"
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary cross-database validation; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, items 5 and 10"
    semantic_status: preserved
    evidence: "阶段 II 仍要求数据支持、绝对恢复、两项主要任务的 Brier/proper score 与校准、泄漏清零、不更新参数的隔离外部表现、状态对齐和结构符号稳定同时成立；适配集上的有限更新单独报告且不能替代不更新参数的失败，阶段 III 也不能补足阶段 II。"
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol specifications for the two primary clinical tasks; Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: "两项主要任务、临床事件与标签可用双时间、72 小时与 24 小时培养—抗菌药配对、baseline SOFA、滚动 24 小时计算、首次可排序发病、首次发病限定、重叠时点每次住院总权重 1、延迟进入、互斥状态、竞争终止、A_t 顺序、同时间戳排除、概率校准、患者和医院聚类及未来信息泄漏检查均保持原值和原义。"
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Representative related-work comparison; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: "候选模型、模拟恢复、外部验证及试验新分析仍是计划产物而非现有结果；贡献仍限于条件性的整合、验证和可复用基准资源。各模块已有先例，完整组合缺口仍只有低至中等置信度，未强化为新算法或全球首次。"
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions; Limitations and boundary conditions; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: "第 14 节集中保留资源与访问、人员、样本支持、标签和泄漏、状态可识别性、缺失与低重叠、不更新参数的外部验证、时间、试验授权和语义、共同指标与映射、文献不确定性，以及对应替代和停止后果。临床尺度到模拟参数、多类别校准估计量与置信界和登记形式仍未确定；事件或参数筛选下限仍不能替代经验有效样本量和模拟稳定性；试验不一致或不精确时仍禁止以亚组选择挽救结论。"
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 10; Risks, alternatives, and stop conditions > Time overrun"
    semantic_status: preserved
    evidence: "阶段 I–II 的 24 个月期限、阶段 III 位于最低交付之外且须满足阶段 II、试验数据、语义和观测映射条件，以及试验结果不得弥补阶段 II 失败的边界均完整保留。"
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 8"
    semantic_status: preserved
    evidence: "观察性数据和预测表现仍不支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生；试验次要分析仍不验证未测潜在动力学、转移边或整个系统模型，且当前计划仍不是已验证模型、临床决策工具、药物平台或无条件推广依据。"
undeclared_scientific_changes:
  - "PCR-002：冻结登记表所保护的高水平论文交付方向在 v027 中被省略，revision delta 未申报该保护目的的变化。"
findings:
  - finding_id: CP-R039-001
    protected_id: PCR-002
    observation: "v027 保留阶段 I–II 的科学目标和可审计证据与资源产物，但没有保留高水平论文这一受保护交付方向。"
    consequence: "该未申报遗漏超出仅作编辑改写的授权范围，但没有改变核心研究身份。"
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

`editorial_scope_violation`。PCR-001、PCR-003 至 PCR-012 的研究身份、对象与范围、输入状态、设计与验证承诺、数值规则、主张强度、限制、替代方案和停止条件均可在 v027 中以相同含义追踪。PCR-002 仅部分保留：24 个月阶段 I–II 目标及其科学路线仍在，但冻结登记表明确保护的“高水平论文”交付方向没有修订后位置；revision delta 仍声明没有科学目标或主张变化，因而这一遗漏属于未申报的编辑范围越界，而非已声明的科学变更或研究身份漂移。

## Protected-content trace

主要的非平凡移动是将完整的假设、限制、替代方案和停止条件集中到第 14 节；这些内容的含义与强度保持不变。唯一未闭合的追踪是 PCR-002 中的高水平论文交付方向：v027 的研究内容与工作包、必要分析与证据、计划产物及贡献定位均未出现等价表述。

## Required routing

v027 目前不得进入新的叙事或学术语言评估。应在后续编辑版本中恢复 PCR-002 所保护的交付方向，并由新的独立实例重新进行内容保全核验；若省略是有意改变研究目的，则须先明确申报并返回科学审查。

## Validator results

- Protected-content register: `PASS: protected-content register is valid`.
- Content-preservation report: `PASS: content-preservation output is valid and covers the frozen register`.
