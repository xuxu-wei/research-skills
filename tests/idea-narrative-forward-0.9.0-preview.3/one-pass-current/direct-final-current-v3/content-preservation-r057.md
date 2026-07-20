---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r057
review_id: preservation-review-I01-001-r057
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: preservation-reviewer-r057-v036-independent
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r057
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v036
  - protected-content-register-I01-001-v003-r003
  - revision-delta-I01-001-v003-to-v036
input_versions: [v003, v036, r003, v003-to-v036]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v036
    version: v036
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v3/idea-dossier-v036.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v036
    version: v003-to-v036
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v3/revision-delta-v003-to-v036.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v3/idea-dossier-v036.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v3/revision-delta-v003-to-v036.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Feasibility, resources, risks, alternatives, and stop conditions > Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      两版 frontmatter 的五项 identity_anchor 逐字一致。v036 的主问题仍以发病前在险时段、首次发病、发病后状态和结局连续体为对象，并保留医院间、数据库间的状态与结构检验以及条件性 RCT 下游比较；Gap、Core hypothesis、Limitations 和最终身份边界共同明确，预测准确度本身不等于结构识别，观察性任务也不产生治疗因果主张，因而没有改成普通预测或泛 ICU 风险分层。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Structured abstract > Objective and hypothesis; Research content and work packages; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    semantic_status: preserved
    evidence: >-
      v036 保留“阶段 I–II 在 24 个月内完成”的原目标，以文献和专家知识约束候选结构，并用 MIMIC-IV/eICU-CRD 开展数据审计、候选系统表征、模拟恢复和未触碰跨数据库检验。贡献段仍把交付限定为可审计科学证据、基准/资源和据此形成的高水平论文，而非只产出预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods > Protocol locks for the two primary clinical tasks; Observational target, identification, alignment, and abstention"
    semantic_status: preserved
    evidence: >-
      v036 frontmatter 逐字保留纵向、脓毒症中心的 ICU 患者系统、可比较的未发病在险时段和发病后轨迹，以及患者时间状态/转移这一主要推断单位。两项任务继续覆盖未发病风险集与发病后队列，患者总权重、患者/医院聚类 bootstrap 和医院优先外部拆分继续约束推断。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and G1 audit; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      v036 仍以文献/专家先验、MIMIC-IV v3.1 和 eICU-CRD v2.0 为核心输入，并把 HiRID 或 AmsterdamUMCdb 限定为月 0–3 预指定、经同等审计的备份。数据库存在和版本列为已核实；团队凭证、DUA、提取、队列支持、具名人员列为未核实或尚未生成，模型、模拟、外部检验和 RCT 新结果明确为尚未生成，没有把可用性写成已经具备。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Local RCT evidence and present limits; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 在 v036 中仍只为条件性阶段 III 的潜在个体级数据来源。本地材料仍标为项目内衍生清洗/QC 报告，不能替代个体数据授权、原始 CRF/SAP、随机化、中心、访视时序及生存/住院/出院语义核验；SCAP 不等于确诊 Sepsis-3，结构性不存在的字段和未核验单位也未被补写。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring and abstention"
    revised_locator: "Research content and work packages > Twenty-four-month minimum and dated milestones; Research design and methods > Protocol locks for the two primary clinical tasks; Observational target, identification, alignment, and abstention; Absolute simulation and semi-synthetic recovery standards"
    semantic_status: preserved
    evidence: >-
      v036 保留资源/G1、标签/状态/医院拆分、简单基线、绝对模拟恢复与假结构检查、至多一个切换或非线性候选、两项主要任务与两项次要诊断、开发冻结、未触碰外部检验、条件性试验分析的单向顺序。Y_t、A_t、M_t、标签和 B 仍分离；解释仍受识别约束、状态对齐、模拟恢复、跨库表现和弃权约束。20 种子对齐率<90%、bootstrap 保留率<80%、外部符号一致率<80%、状态对齐<0.70 或区间未校准仍触发删除、合并或数据库/照护政策特异分类，良好预测不能替代恢复与稳定性判定。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Protocol locks for the two primary clinical tasks; Absolute simulation and semi-synthetic recovery standards; Hospital-primary genuine cross-database validation; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      v036 的阶段 II 成功仍是两库数据支持、绝对恢复/零边/错设标准、两个主要任务的 proper score 与校准、高严重度泄漏清零、未触碰零更新外部表现、状态对齐和结构稳定性的合取。仅校准或仅观测层更新与零更新分开报告，不能替代零更新不足；全模型重拟合仍是新开发；阶段 III 明确不计入且不能补足阶段 II。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system; Data, materials, and existing evidence base > Candidate variable-role firewall"
    semantic_status: preserved
    evidence: >-
      v036 逐项保留未来 12 小时首次发病 CIF 与第 7 日有利状态占用两项主要任务、event/availability 双时钟、首次发病与 delayed entry、互斥发病后状态、竞争终止、as-of 特征、proper score/校准及患者和医院聚类。标本—抗菌药 72h/24h 配对、baseline SOFA、滚动 24h 和首个可排序 onset、每次住院总权重 1、同时间格 A_t/next-state 次序、同戳不可排序边排除，以及未来测量频率、重复住院和结局驱动变量/网格/阈值的泄漏检查均仍在正文。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Data, materials, and existing evidence base > Current resource and evidence status; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      v036 继续把候选表征、模拟恢复、外部检验和试验分析写为计划产物，并明确当前没有模型或新结果。贡献仍限定为条件性的整合、验证、基准、资源和研究治理；各模块已有先例，完整组合缺口只有低至中等置信；“全球首创”“新算法”以及既有因果网络、数字孪生或临床工具均未获得支持。RCT 措辞改为预设估计目标上的随机组比较，没有增强原有主张。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions; Limitations and boundary conditions; Risks, alternatives, and stop conditions; Remaining execution requirements; Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      v036 第 14 节集中保留访问/资源、人员承诺、G1 支持、标签与泄漏、状态恢复、MNAR/低重叠、零更新外部检验、时间节点、RCT 数据/语义/共同测量、跨数据映射和最接近工作不确定性。风险表逐项给出触发、替代和停止/降级动作；临床尺度到模拟参数，以及精确多类别校准估计量、置信界和 threshold registry 仍未解决，事件/参数筛选下限不替代经验有效样本量或模拟稳定性。两试验方向不一致或区间过宽时仍只能分开报告无支持或适用性有限，不能挑选亚组挽救结论。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > Twenty-four-month minimum and dated milestones; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions; Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      v036 保留阶段 I–II 必须在 24 个月内完成以及月 0–3、4–6、7–12、13–18/20、21–24 的依赖顺序。阶段 III 仍位于最低交付之外，只在阶段 II 成功且相应试验数据、语义和跨数据映射条件成立时开展；月 24 封存阶段 II，任何 RCT 结果不能绕过或补足其失败。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      v036 明确观察性资料、联合建模、负向控制或良好预测不能识别真实因果网络、治疗因果效应、反事实策略、机制、中介或控制。条件性 RCT 也不能验证未测潜在状态、连续动力学、转移边、中介、控制或整个阶段 II 模型。当前计划继续禁止被写成已验证模型、可控系统、数字孪生、临床决策工具、药物平台或无条件临床推广依据。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

判定为 `scientific_content_preserved`。四项输入均按其逻辑标识、版本和路径直接核验；修订说明没有声明科学变更，但本判定不依赖修订说明的自述。v036 正文为 frozen register 的 12 个条目分别提供了可定位证据，研究身份、研究问题、范围、数据状态、估计目标、验证顺序、主张强度、关键限制和条件性分支均与 v003 同义，且未把计划工作写成既有结果。

主要改动属于允许的编辑操作：把背景、现状、缺口、意义和设计理由拆分；把阶段 III 的完整规范集中到单一方法小节；把完整限制、风险、替代和停止条件集中到第 14 节；将实现内容改为输入—输出—记录—接口表；用“随机组访视结局差异”等统计语言替换可能被误解为系统机制的简称。这些改动没有改变估计目标、阈值、失败后果或证据强度。

本检查只判断内容保真，不判断原方案或修订方案的科学正确性。正文保留的未解决事项是研究本身的既有执行限制，不是本次保真检查的未决问题。

## Protected-content trace

### 身份、问题、边界和证据状态

- 五项 frontmatter 身份锚点逐字一致；主问题仍覆盖发病前、首次发病、发病后互斥状态和结局，并以患者时间状态/转移为推断单位，尊重患者和医院聚类。
- MIMIC-IV 与 eICU-CRD 仍是两项核心公共 ICU 数据来源，HiRID/AmsterdamUMCdb 仅能预先指定为备份。数据库存在/版本与团队访问、DUA、可运行提取、项目队列支持和具名人员继续分开陈述。
- EXIT-SEP 与 XBJ-SCAP 的个体级数据仍属阶段 III 条件性来源。衍生材料的样本与缺失概况保持不变：EXIT-SEP 随机 1,817 例、28 日状态明确 1,760 例、死亡 395 例、未知 57 例，SOFA D1/D4/D7 为 1,750/1,542/1,296，乳酸由 855 降至 223；XBJ-SCAP 随机 710 例、FAS 675、PPS 617、操作性 sepsis-like 671、严格重叠 658，SOFA D0/D4/D8 为 703/628/610，WBC 为 704/634/614，CRP 为 579/503/467，28 日状态为 675。原始授权、CRF/SAP 和试验语义仍须另行核验。
- 所有候选模型、模拟恢复、外部验证和 RCT 新分析仍为尚未生成。完整组合缺口仍只有低至中等置信；没有新算法、全球首次、因果网络、数字孪生或临床工具主张。

### 任务、估计目标、方法关系和验证逻辑

- 发病前主要估计目标仍为给定 as-of 历史的未来 12 小时首次发病 CIF；发病后主要估计目标仍为第 7 日“生理恢复或活着出 ICU”有利状态占用概率，并分别报告两种状态。两个次要分析仍是伪遮蔽重建和未来轨迹诊断，不能改变主要任务判定。
- 阶段顺序仍为资源/G1 审计，标签、状态和医院拆分冻结，简单基线，绝对模拟恢复与假结构检查，至多一个附加候选模型，两项主要任务和两项次要诊断，开发冻结，未触碰外部检验，最后才可能进入条件性 RCT 分支。
- 阶段 II 成功仍是数据支持、模拟恢复、主要任务评分与校准、泄漏清零、未触碰零更新表现、状态对齐和结构稳定的合取。仅校准更新或仅观测层更新不能替代零更新，全模型重拟合仍属于新开发。

### 条件分支及失败解释

- 数据访问或 G1 支持不足仍触发预指定备份、时间网格降级、删除模块/边或停止跨库成功判定；跨分区患者不能被重新分配以挽救支持。
- 模拟恢复、零边、错设、状态对齐、外部稳定性或泄漏条件不满足时，仍须删除、合并、降级或停止结构解释；预测排名不能挽救失败。
- 每项 RCT 先核验 R0。共同测量不足两个时不建立跨数据映射；若试验核心语义和 SOFA 可核验，则转入与阶段 II 独立的 SOFA 访视结局分析。R1 任一标准不满足也进入该独立分支；关键 D7/D8、随机化、中心或生存/住院/出院语义无法核验时，停止新访视结局分析。
- 两试验始终分开分析。方向不一致或区间过宽时，只报告无支持或跨场景适用性有限，不合并为共同机制，也不挑选亚组挽救结论。

### 数值和时间规则

- 时间治理保持为月 0–3 资源确认、月 4–6 G1 与协议冻结、月 7–12 模拟恢复和模型准入、月 13–18/20 开发验证与冻结、月 21–24 未触碰外部检验；月 20 未冻结不开放最终测试，月 24 无未触碰结果则阶段 II 最低交付未完成，阶段 III 只能在 24 月后条件性开展。
- 主网格仍为 12 小时；不受支持时只能在建模前固定为 24 小时或事件时间。发病前任务从 ICU 第 12 小时开始，每 12 小时设置 landmark，使用最多 24 小时且至少 12 小时的 as-of 历史，预测未来 12 小时；发病后主时间点为第 7 日，第 14 日作敏感性分析。
- 疑似感染配对仍为标本先则抗菌药在 72 小时内、抗菌药先则标本在 24 小时内；有记录慢性器官功能障碍时 baseline SOFA 取入 ICU 前 24 小时最低可计算值，SOFA 成分按滚动 24 小时取最差，相对 baseline +2 的窗口为感染前 48 小时至后 24 小时。只分析首次发病，重叠 landmark 的每次住院总权重为 1；恢复须连续 24 小时。
- G1 仍要求每个自由风险/转移参数在开发/外部至少 20/10 个事件或转移，外部测试至少 20 个有支持医院；每个共同维度至少两个测量，每项在两库至少 30% 合格时间格实测，并覆盖至少 70% 合格医院和 80% 患者。K=min(通过模块数,4)，状态机制数≤3，滞后只允许 1 或 2 个冻结时间格。
- 主要任务标准仍为 Brier 相对最强简单基线差值的上侧 95% 界≤+0.01、校准斜率 0.80–1.20、绝对风险误差≤0.02。行动比例<5% 或 >95%，或加权 ESS<20% 名义样本时，不估计相应治疗作用。
- 模拟仍为每个核心情景至少 1,000 次或至关键比例 Monte Carlo 标准误≤0.02；状态 ARI/主要典型相关≥0.80，转移 MAE≤0.05 且 95% coverage 为 0.90–0.98，符号/滞后恢复率≥0.80，边检测敏感度≥0.80 且 FDR≤0.10，零边假结构的 95% 区间排除 0 比例≤0.05，错设触发失配/弃权比例≥80% 且错误结构高置信≤0.05，概率校准斜率为 0.80–1.20、绝对偏差≤0.02。
- 外部医院仍按固定种子 20260717 分为 30% 适配区和 70% 未触碰测试区；跨分区排除超过原合格测试患者或主要事件 10%，或医院、事件/转移、共同测量支持不足时，须启动备份或降级。
- R1 仍要求第一奇异轴解释能量≥50%，P_state/P_obs 相关≥0.70，归一化 MAE≤0.50，|α|≤0.20 SD、β=0.80–1.20、95% coverage 为 0.90–0.98，每项共同测量外部校准斜率 0.80–1.20 且标准化截距绝对值≤0.20；试验中至少 80% 观测值位于冻结合理范围，至少 60% 的访视时存活在院者可由不少于两个实测指标计算 P_obs。缺失敏感性仍含 delta ±0.5/±1 SD 和 best/worst tipping，两个试验的主要访视结局仍构成 Holm FWER 0.05 家族。

### 关键限制和主要可行性结论

第 14 节仍是完整权威位置。资源、人员、G1、模型结果和 RCT 语义尚未具备；临床尺度到模拟参数的映射，以及精确多类别校准估计量、置信界和 threshold registry 仍未解决。观测资料不能识别真实因果网络、治疗效应、反事实策略、机制、中介或控制；状态解释仅限达到恢复、对齐、稳定性和校准标准的量；适配后运输不等于冻结模型外部稳定；RCT 不验证未测潜在状态、动力学、转移边或整个阶段 II 模型；最接近工作检索也不支持全球首次。所有关键限制均保留了对应的失败触发与停止或降级后果，没有被摘要化为无后果的一般性声明。

## Required routing

v036 可继续接受新的叙事与语言评估；无需因内容保真返回科学审查。
