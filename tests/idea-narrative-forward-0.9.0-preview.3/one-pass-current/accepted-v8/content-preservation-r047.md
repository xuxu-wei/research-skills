---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r047
review_id: content-preservation-review-I01-001-r047
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-r047
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r047
input_artifact_ids:
  - idea-dossier-I01-001-v030
  - idea-dossier-I01-001-v032
  - protected-content-register-I01-001-v006
  - revision-delta-I01-001-v030-to-v032
input_versions:
  - v030
  - v032
  - v006
  - v032
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v030
    version: v030
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/idea-dossier-v030.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v032
    version: v032
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v8/idea-dossier-v032.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/protected-content-register-v006.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v030-to-v032
    version: v032
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v8/revision-delta-v030-to-v032.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/idea-dossier-v030.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v8/idea-dossier-v032.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/protected-content-register-v006.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v8/revision-delta-v030-to-v032.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter > identity_anchor"
    revised_locator: "YAML frontmatter > identity_anchor"
    semantic_status: preserved
    evidence: >-
      五项身份锚点逐字一致：核心问题、24 个月阶段 II 目标、纵向脓毒症相关 ICU 患者系统、三类条件性证据来源，以及尊重患者与医院聚类的患者—时间状态和转移推断单位均未改变。
  - protected_id: PCR-002
    prior_locator: "## Research question, objectives, and core hypothesis > ### Primary research question and ### Objectives"
    revised_locator: "## Research question, objectives, and core hypothesis > ### Primary research question and ### Objectives"
    semantic_status: preserved
    evidence: >-
      发病前在险期至结局的完整对象范围、四项研究目标、跨医院和跨数据库稳定性问题、阶段 II 与实际访视映射的双重门槛，以及映射失败时独立死亡—SOFA 临床状态分支均保持原义。
  - protected_id: PCR-003
    prior_locator: "## Title, summary, audience, and positioning > One-sentence complete-Idea summary and Positioning and contribution frame"
    revised_locator: "## Title, summary, audience, and positioning > One-sentence complete-Idea summary and Positioning and contribution frame"
    semantic_status: preserved
    evidence: >-
      题名和摘要重排了修饰关系，但仍限定为 24 个月计划、两个先审计的公共数据库、开发与参数调整之外的不更新参数验证、五类证据全部达标后才启动的分试验 RCT 次要分析；证据整合、计划验证、基准资源和可证伪设计的定位及“单项模块不主张新颖”的强度未提高。
  - protected_id: PCR-004
    prior_locator: "## Structured abstract > Expected result"
    revised_locator: "## Structured abstract > Expected result"
    semantic_status: preserved
    evidence: >-
      双时刻标签、双数据库审计、互斥状态、模拟恢复与不可解释项记录、两项主要任务、两项次要诊断及不更新参数的外部验证仍全部表述为计划产物；RCT 映射仍在阶段 II 后且有条件，失败时仍转向独立临床状态，没有把任何计划写成完成结果。
  - protected_id: PCR-005
    prior_locator: "## Data, materials, and existing evidence base > ### Current resource and evidence status"
    revised_locator: "## Data, materials, and existing evidence base > ### Current resource and evidence status"
    semantic_status: preserved
    evidence: >-
      数据库存在和版本仅为已核实；访问、协议、提取、校验和、项目计数、人员承诺、试验授权与原始语义仍未核实；本地试验材料仍只是衍生报告；WBC/CRP 仍只是候选；新模型及各类新结果仍未生成；截至 2026-07-17 的模块先例为高置信、完整组合缺口仅低至中等置信。
  - protected_id: PCR-006
    prior_locator: "## Data, materials, and existing evidence base > ### Public ICU database roles and observability audit"
    revised_locator: "## Data, materials, and existing evidence base > ### Public ICU database roles and observability audit"
    semantic_status: preserved
    evidence: >-
      MIMIC-IV v3.1 的开发角色、eICU-CRD v2.0 按医院划分适配集与最终测试集的外部角色、月 0–3 预设且同等审计的 HiRID/AmsterdamUMCdb 备选规则，以及共同层只接纳可审计概念、数据库特异信息仅作探索性观测模型用途，均未改变。
  - protected_id: PCR-007
    prior_locator: "## Data, materials, and existing evidence base > ### Local RCT evidence"
    revised_locator: "## Data, materials, and existing evidence base > ### Local RCT evidence"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 的 45 个 ICU、1,817/1,760/395/57 及 SOFA、乳酸计数，与 XBJ-SCAP 的 710/675/617/671/658、SOFA/WBC/CRP 和 28 日状态计数均一致；D1/D7、D0/D8 时序待核验、SCAP 不等于确认 Sepsis-3、结构性缺失字段和 D-dimer 单位未核实等状态也未改变。
  - protected_id: PCR-008
    prior_locator: "## Research content and work packages > ### Twenty-four-month programme"
    revised_locator: "## Research content and work packages > ### Twenty-four-month programme"
    semantic_status: preserved
    evidence: >-
      月 0–3、4–6、7–12、13–18/20、21–24 的工作顺序和信息隔离保持不变；简单基线仍先于至多一个复杂候选模型，开发包仍在外部结果前冻结，最终测试仍不更新参数，适配集再校准与仅更新观测模型仍分开报告。
  - protected_id: PCR-009
    prior_locator: "## Research content and work packages > ### Prespecified criteria for completing the 24-month validation stage"
    revised_locator: "## Research content and work packages > ### Prespecified criteria for completing the 24-month validation stage"
    semantic_status: preserved
    evidence: >-
      五类证据必须全部通过且互不补救的规则未变；Brier 差值上侧 95% 界 ≤+0.01、斜率 0.80–1.20、绝对风险误差 ≤0.02、至少 20 个外部医院、状态对齐 ≥0.70、符号一致率 ≥0.80 等阈值及月 6 前、不得使用外部结果、只可收紧的细化规则全部一致。
  - protected_id: PCR-010
    prior_locator: "## Data, materials, and existing evidence base > ### Public ICU database roles and observability audit > audit table and paragraph beginning '主时间方案为 12 小时'"
    revised_locator: "## Data, materials, and existing evidence base > ### Public ICU database roles and observability audit > audit table and paragraph beginning '主时间方案为 12 小时'"
    semantic_status: preserved
    evidence: >-
      首次合格住院/ICU、20/10 事件与转移支持、终止状态分计、12 小时排序及预拟合替代、每维至少两个锚点、30% 时间格实测、70% 医院/80% 患者覆盖、测量时刻记录、禁止无条件前移和有限例外均未变。K 仍为审计模块数与 4 的较小值，“状态模式不超过 3”仍原样承担复杂度上限用途，支持不足仍强制简化。
  - protected_id: PCR-011
    prior_locator: "## Data, materials, and existing evidence base > ### Prespecified variable roles"
    revised_locator: "## Data, materials, and existing evidence base > ### Prespecified variable roles"
    semantic_status: preserved
    evidence: >-
      Y_t、A_t、M_t、仅标签字段和 B 的纳入内容、排除内容、双重用途副本与时间隔离、未测不等于正常、接口缺失不编码成生理状态以及未知基线显式编码规则均一致。
  - protected_id: PCR-012
    prior_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks > Primary pre-onset task column"
    revised_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks > Primary pre-onset task column"
    semantic_status: preserved
    evidence: >-
      成人首个合格 ICU 与至少 12 小时历史、72/24 小时感染配对、SOFA 基线和滚动窗口、信息可用时刻不回填、12 小时动态预测时点与未来 12 小时风险、住院总权重 1、竞争终止、时间格内顺序、累积发生估计对象、Brier/校准及患者和医院聚类区间均未变。
  - protected_id: PCR-013
    prior_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks > Primary post-onset task column"
    revised_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks > Primary post-onset task column"
    semantic_status: preserved
    evidence: >-
      首次发病与可审计延迟进入、左截断且不回溯发病时刻、恢复连续 24 小时后才可用、每 12 小时评价、日 7 主要与日 14 敏感性、终止状态和恢复区分、相同时间格规则、日 7 有利集合占用、Aalen–Johansen、多类别 Brier 和聚类不确定性均一致。
  - protected_id: PCR-014
    prior_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks > paragraph beginning '主标签之外仅设置两种敏感性标签'"
    revised_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks > paragraph beginning '主标签之外仅设置两种敏感性标签'"
    semantic_status: preserved
    evidence: >-
      仍恰有两种且不替代主结果的敏感性标签：培养—抗菌药对称 ±24 小时，以及所有患者使用感染前 24 小时最低可计算 SOFA 并将器官功能窗限于前后各 24 小时；全部泄漏核查类别也保持不变。
  - protected_id: PCR-015
    prior_locator: "## Research design and methods > ### Mutually exclusive post-onset state and event system"
    revised_locator: "## Research design and methods > ### Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      12 小时互斥赋值、死亡→转院/不可观察→存活出 ICU→恶化/新器官衰竭→生理恢复→持续脓毒症的优先级、无法排序时的处理和事件时间敏感性均一致；六类状态的定义、可用时刻和变量分工没有变化。
  - protected_id: PCR-016
    prior_locator: "## Research design and methods > ### Observational target, anchoring and abstention > paragraphs defining p(X_0:T,...) and anchor constraints"
    revised_locator: "## Research design and methods > ### Observational target, anchoring and abstention > paragraphs defining p(X_0:T,...) and anchor constraints"
    semantic_status: preserved
    evidence: >-
      X_t、Y_t、A_t、M_t、B、S 与完整联合分布及非因果解释保持不变；每维至少两个锚点、首载荷 +1、稀疏交叉载荷、K≤4、“状态模式≤3”、仅 1 或 2 个滞后、20 个固定种子及对齐后才解释的规则均一致。“状态模式≤3”仍用于模型结构复杂度约束，没有被改成新的科学对象或类别定义。
  - protected_id: PCR-017
    prior_locator: "## Research design and methods > ### Observational target, anchoring and abstention > paragraph beginning '非随机缺失主分析'"
    revised_locator: "## Research design and methods > ### Observational target, anchoring and abstention > paragraph beginning '非随机缺失主分析'"
    semantic_status: preserved
    evidence: >-
      MAR/选择模型基线、δ=−1/−0.5/0/+0.5/+1 标准差、转折点分析、行动概率和有效样本量分层、5%/95% 与 20% 的不估计门槛，以及 90%/80%/80%/0.70/区间校准的删除、合并或特异性判定均未变；预测表现仍不能补救解释失败。
  - protected_id: PCR-018
    prior_locator: "## Research design and methods > ### Simulation and semi-synthetic recovery tests"
    revised_locator: "## Research design and methods > ### Simulation and semi-synthetic recovery tests"
    semantic_status: preserved
    evidence: >-
      月 7–10、不得读取最终外部结果、至少 1,000 次或 Monte Carlo 标准误 ≤0.02 均一致。正确设定、真值零边/独立状态、状态数过多而过拟合、遗漏状态、错误滞后和错设观测模型只是把原情景展开；交叉因素及 ARI/相关、转移误差、覆盖、符号/滞后、灵敏度、FDR、假边、错设识别、校准斜率和偏差的全部阈值与后果未变。
  - protected_id: PCR-019
    prior_locator: "## Research design and methods > ### Hospital-based cross-database validation > hospital split and numbered patient-handling rules"
    revised_locator: "## Research design and methods > ### Hospital-based cross-database validation > hospital split and numbered patient-handling rules"
    semantic_status: preserved
    evidence: >-
      体量/接口分层、种子 20260717、医院 30%/70% 划分、医院优先、划分表/链接版本/校验和预冻结、跨分区患者全部排除且不重哈希、同分区首个合格记录、结局前排除报告、测试优先连通分量敏感性及独立保管人盲态支持检查均一致。
  - protected_id: PCR-020
    prior_locator: "## Research design and methods > ### Hospital-based cross-database validation > paragraph beginning '确定标签、变量统一方案'"
    revised_locator: "## Research design and methods > ### Hospital-based cross-database validation > paragraph beginning '确定标签、变量统一方案'"
    semantic_status: preserved
    evidence: >-
      外部分析仍依次且分别报告：不更新参数、适配集截距/斜率再校准、仅更新观测模型且固定状态/转移参数；目标数据库完整重拟合仍被界定为更新或再开发，不是外部验证，有限更新仍不能补救不更新参数验证失败。
  - protected_id: PCR-021
    prior_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis > trial semantics, anchor eligibility, and prespecified mapping"
    revised_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis > ordered eligibility and mapping lists"
    semantic_status: preserved
    evidence: >-
      段落改为有序列表，但次要探索性质、原终点分报、阶段 II 后且组间比较前冻结、授权和完整原始语义要求、共同锚点四项资格与排除项、每试验至少两个锚点，以及 Z_C、观测方程、SVD、P_state、P_obs、并列与符号规则、禁止使用分组/结局/跨试验合并均不变。
  - protected_id: PCR-022
    prior_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis > Consistency and error standards"
    revised_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis > Consistency and error standards lists"
    semantic_status: preserved
    evidence: >-
      eICU D7/D8 窗口先行且不得按 RCT 调参、所有标准联合通过的规则未变；Frobenius 能量 ≥50%、相关 ≥0.70、归一化误差 ≤0.50、|α|≤0.20、β 0.80–1.20、覆盖 0.90–0.98、锚点校准、盲态试验 80% 合理范围与 60% 可计算比例等数值和方向全部一致，试验内重估权重仍判失败。
  - protected_id: PCR-023
    prior_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis > mapping-passing estimand and independent clinical-state analysis"
    revised_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis > mapping-passing estimand and independent clinical-state analysis"
    semantic_status: preserved
    evidence: >-
      映射通过时仍按死亡最差、住院存活者 P_obs 从高到低、存活出院最有利排序，并采用兼容中心/分层的概率指数或胜出概率；映射失败但语义充分时仍改用独立死亡—SOFA—出院排序，D7/D8、随机化、中心或生存语义不可核实时仍不构造新端点。
  - protected_id: PCR-024
    prior_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis > trial table and paragraph on sparse visits"
    revised_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis > trial table and paragraph on sparse visits"
    semantic_status: preserved
    evidence: >-
      两试验目标人群、完整结局/全分析/符合方案/类脓毒症/严格重叠子集和 D1/D0 基线警示均一致；死亡出院排序、插补变量和重算、Rubin/聚类合并、±0.5/±1 标准差与转折点/界限、结构性缺失不插补、Holm 0.05、探索性 FDR、只报告交互、稀疏访视不插值及不合并均未变。
  - protected_id: PCR-025
    prior_locator: "## Research design and methods > ### Secondary representation diagnostics"
    revised_locator: "## Research design and methods > ### Secondary representation diagnostics"
    semantic_status: preserved
    evidence: >-
      伪遮蔽 MAE、RMSE、对数评分和覆盖，未来轨迹的连续等级概率评分、负对数似然、占用和结局校准，以及按变量、状态、医院和观察密度分层均一致；伪遮蔽仍仅评价原本实测值并只承担次要表征诊断功能。
  - protected_id: PCR-026
    prior_locator: "## Required analyses and evidence"
    revised_locator: "## Required analyses and evidence"
    semantic_status: preserved
    evidence: >-
      阶段 II 的八组交付仍完整覆盖审计与职责、标签/状态测试、变量隔离与泄漏、基线和恢复情景及不可解释原因、缺失/支持/阴性对照、两项主要和两项次要任务、医院划分/权限/校验和/三种模式及五类证据判定表；RCT 前授权、57 例未知状态、分析集差异、映射、并列、插补、中心、Holm 与交互规范均未变。
  - protected_id: PCR-027
    prior_locator: "## Expected outputs, falsification criteria, and interpretations > ### Falsification criteria and result interpretation"
    revised_locator: "## Expected outputs, falsification criteria, and interpretations > ### Falsification criteria and result interpretation"
    semantic_status: preserved
    evidence: >-
      泄漏、双数据库支持不足、恢复失败、缺失/行动支持不足、不更新参数外部验证失败、试验映射失败和试验语义不可核验的各自解释与降级分支均一致；唯一正面解释仍要求五类阶段 II 证据全部达标，没有增强任何主张。
  - protected_id: PCR-028
    prior_locator: "## Contribution, innovation, impact, application, and closest-work comparison > ### Contribution and evidence progression"
    revised_locator: "## Contribution, innovation, impact, application, and closest-work comparison > ### Contribution and evidence progression"
    semantic_status: preserved
    evidence: >-
      数据可追溯仍为计划；状态恢复和两项主要任务仍是阶段 II 必需；跨数据库不更新参数验证仍是最低端点；随机化访视摘要仍为条件性次要分析；独立死亡—SOFA 状态仍与候选表征独立；贡献仍仅在计划执行后成立，实证贡献仍未建立。
  - protected_id: PCR-029
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Feasibility and resources"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      六类所需角色及缺少具名人员、承诺和工时的状态未变；计算范围仍为两个主数据库、K≤4、“状态模式≤3”、两项主要任务、两项次要诊断和至多一个复杂候选模型。“状态模式≤3”仍是计算与复杂度范围，没有改变其原用途或补写含义。数据库与结果状态、24 个月最低交付、RCT 位于其外且不得补救任何阶段 II 缺口均一致。
  - protected_id: PCR-030
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Working assumptions"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Working assumptions"
    semantic_status: preserved
    evidence: >-
      两项待登记内容仍未解决且后果相同：月 7 前登记临床尺度到模拟参数范围，未完成则不得声称复杂候选通过恢复；查看最终外部结果前登记多类别校准估计量、置信界与细化阈值，未完成则相应结论不得进入阶段 II。允许依据、既定情景、硬标准只可收紧以及筛选下限不能替代有效样本量/稳定性均未变。
  - protected_id: PCR-031
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions > items 1–5"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions > items 1–5"
    semantic_status: preserved
    evidence: >-
      数据/人员/结果不确定性、标签和时间泄漏途径、潜在状态仅在锚定/恢复/对齐/校准后可解释且预测不得补救、非随机缺失和行动支持限制、阴性对照边界，以及不更新参数验证优先于有限更新和跨分区排除可能削弱支持，均在唯一权威限制位置原强度保留。
  - protected_id: PCR-032
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions > items 6–8"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions > items 6–8"
    semantic_status: preserved
    evidence: >-
      两试验仍只是潜在个体级来源，衍生材料不替代授权与原始语义，锚点/单位/映射仍未检验；人群、访视、锚点和估计对象不同仍须分开，稀疏访视不支持伪连续轨迹，冲突或宽区间不得事后亚组补救；非系统文献检索的所有缺口与低至中等置信边界均原样保留。
  - protected_id: PCR-033
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Risks, alternatives, and stop conditions"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      访问/人员、双数据库支持、跨分区与支持阈值、泄漏、恢复与假结构、缺失/行动支持、不更新参数外部验证、进度、RCT 授权/语义/映射、试验冲突和文献定位的十一条“触发→替代→停止或有界结论”均保留；月份、数值阈值、降级路线及所有不得补救规则均未改变。
  - protected_id: PCR-034
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions > item 9, Interpretation boundary"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions > item 9, Interpretation boundary"
    semantic_status: preserved
    evidence: >-
      观察性数据和预测仍不支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生主张；RCT 次要分析仍最多支持实际访视摘要或独立临床状态的随机组间差异，不能验证潜在动力学、转移边或整个模型；当前计划仍不是已验证工具、药物平台或无条件临床推广依据。
  - protected_id: PCR-035
    prior_locator: "## Title and positioning claim-support table > row '有界检索尚未发现完整证据组合的代表性先例'"
    revised_locator: "## Title and positioning claim-support table > row '有界检索尚未发现完整证据组合的代表性先例'"
    semantic_status: preserved
    evidence: >-
      截至 2026-07-17 的检索仍为有界检索，只以低至中等置信支持“未发现代表性完整组合”；仍未增加全球不存在、科学或方法首创、新算法、无专利或临床首次主张，单项模块仍不主张新颖。
undeclared_scientific_changes: []
findings: []
unresolved_issues:
  - issue_id: LANG-R045-004
    status: unresolved_confirmation_required
    revised_locators:
      - "### Public ICU database roles and observability audit > audit table"
      - "### Observational target, anchoring and abstention"
      - "## Key techniques and implementation > item 2"
      - "### Feasibility and resources"
    evidence: >-
      v030 与 v032 在四个用途位置分别保持“状态模式不超过 3”“状态模式≤3”、审计输出中的“状态模式”和可行性范围中的“状态模式≤3”。上限仍为 3，仍服务于审计后的模型复杂度控制，支持不足仍要求简化；修订没有猜测其计数对象、重命名状态或引入新限制。
    required_action: >-
      继续保留为未解决的作者或方法学负责人确认事项；在获得批准定义前不得把该术语改写成具体状态类别或新的方法学承诺。
---

# Content-preservation check

## Decision rationale

`scientific_content_preserved`。v032 的变更限于题名修饰关系、摘要句法、术语首次解释、模拟情景的显式展开，以及 RCT 映射与判定标准的列表化。研究身份、对象和范围、数据与证据状态、方法与分析承诺、全部数值和时间阈值、验证逻辑、主张强度、假设、限制、条件分支、停止规则及不支持的主张类别均与 v030 一致；修订差异也没有声明科学变化。

## Protected-content trace

冻结登记中的 PCR-001 至 PCR-035 共 35 项均恰好核验一次，35 项均为 `preserved`，缺失 0 项、重复 0 项、未知 0 项。非平凡移动仅见于 RCT 映射段落从连续文字改为有序列表；公式、顺序、联合通过规则及阈值不变。模拟情景由“正确、零边、过拟合和错设”改为逐项明示，但对应的生成情景、交叉因素、判定标准和失败后果不变。

“状态模式≤3”在 v032 中保留 v030 的四个用途：审计所得复杂度上限、锚定模型的结构约束、审计交付项，以及可行性/计算范围。该词仍未获得授权定义，因此 `LANG-R045-004` 正确保留为 `unresolved_confirmation_required`，不构成已解决的语言事项，也未被转换成新的科学决定。

## Required routing

内容保真核验不阻止进入新的叙事与学术语言评估。`LANG-R045-004` 必须继续转交作者或方法学负责人确认；确认前不得推断“状态模式”的计数对象或改变上限用途。

## Validator

- Frozen register: `PASS: protected-content register is valid`.
- Preservation report and exact protected-ID coverage: `PASS: content-preservation output is valid and covers the frozen register`.
