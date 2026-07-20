---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-check-I01-001-r042
review_id: idea-narrative-preservation-I01-001-r042
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-r042
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r042
input_artifact_ids:
  - idea-dossier-I01-001-v028
  - idea-dossier-I01-001-v029
  - protected-content-register-I01-001-v004
  - revision-delta-I01-001-v028-to-v029
input_versions:
  - v028
  - v029
  - v004
  - v029
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v028
    version: v028
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/idea-dossier-v028.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v029
    version: v029
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/idea-dossier-v029.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v004
    version: v004
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/protected-content-register-v004.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v028-to-v029
    version: v029
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/revision-delta-v028-to-v029.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/idea-dossier-v028.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/idea-dossier-v029.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/protected-content-register-v004.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/revision-delta-v028-to-v029.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "Research question, objectives, and core hypothesis — complete section"
    revised_locator: "Research question, objectives, and core hypothesis — complete section; Prespecified criteria for completing the 24-month validation stage; Trial-specific mapping to observed visits and independent clinical-state analysis"
    semantic_status: preserved
    evidence: "研究对象、患者—时间状态及转移的推断单位、三部分核心问题、24 个月阶段边界、可恢复性前提、观察性与随机化证据分离以及 RCT 不补足阶段 II 的规则均保持不变；长问句拆为三个子问题未改变研究身份。"
  - protected_id: PCR-002
    prior_locator: "Title, summary, audience, and positioning — complete section"
    revised_locator: "Title, summary, audience, and positioning — complete section; Structured abstract"
    semantic_status: preserved
    evidence: "研究仍定位为候选表征的证据整合、计划性跨数据库验证、基准资源与可证伪设计，而非普通预测工具；两公共数据库、隔离外部测试以及分试验且有条件的 RCT 次要分析范围均保留。"
  - protected_id: PCR-003
    prior_locator: "Data, materials, and existing evidence base > Current resource and evidence status — complete table"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status — complete table"
    semantic_status: preserved
    evidence: "数据库存在和版本已核实但访问、协议、提取、项目计数、人员承诺、试验授权与语义均未核实的状态未变；所有模型与分析仍标为尚未生成，检索置信度仍为单项高、完整组合低至中等。"
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence — complete subsection"
    revised_locator: "Data, materials, and existing evidence base > Local RCT evidence — complete subsection"
    semantic_status: preserved
    evidence: "EXIT-SEP 的 1,817、1,760、395、57 及 SOFA/乳酸计数与时间语义缺口全部保留；XBJ-SCAP 的 710、675、617、671、658、SOFA/WBC/CRP 计数、SCAP 边界、不可用变量及 D-dimer 单位缺口也均未改变。"
  - protected_id: PCR-005
    prior_locator: "Research content and work packages > Twenty-four-month programme and Work packages — complete tables and minimum analysis order"
    revised_locator: "Research content and work packages > Twenty-four-month programme; Work packages; minimum analysis order"
    semantic_status: preserved
    evidence: "月 0–3、4–6、7–12、13–18/20、21–24 的工作和交付顺序未变；简单模型先行、至多一个复杂候选、不更新参数外部测试优先及两种有限更新分报的最低顺序完整保留。"
  - protected_id: PCR-006
    prior_locator: "Data, materials, and existing evidence base > Public ICU database roles and observability audit — complete subsection and audit table"
    revised_locator: "Data, materials, and existing evidence base > Public ICU database roles and observability audit — complete subsection and audit table"
    semantic_status: preserved
    evidence: "开发库、外部库和备份库角色及月 6 审计时点不变；20/10 事件与转移支持、至少 20 家外部医院、每维至少两个锚点、30% 时间格、70% 医院、80% 患者、K≤4、状态模式≤3 和 12 小时主网格等规则逐项一致。"
  - protected_id: PCR-007
    prior_locator: "Data, materials, and existing evidence base > Prespecified variable roles — complete table"
    revised_locator: "Data, materials, and existing evidence base > Prespecified variable roles — complete table"
    semantic_status: preserved
    evidence: "Y_t、A_t、M_t、标签专用变量和 B 的内容与用途未变；治疗不得作生理锚点、标签副本须分离、未检测不等于正常、数据库特异信息仅用于探索性观测模型等边界均保留。"
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol specifications for the two primary clinical tasks — complete table"
    revised_locator: "Research design and methods > Protocol specifications for the two primary clinical tasks — complete table"
    semantic_status: preserved
    evidence: "人群、72/24 小时感染配对、SOFA 基线及 −48/+24 小时窗、不可回填的信息时点、12 小时预测和第 7 日目标、首次发病与延迟进入、竞争事件、同格顺序、估计对象、指标和聚类不确定性均未改变。"
  - protected_id: PCR-009
    prior_locator: "Research design and methods > Protocol specifications for the two primary clinical tasks — post-table sensitivity-label and leakage paragraph"
    revised_locator: "Research design and methods > Protocol specifications for the two primary clinical tasks — paragraph after the table"
    semantic_status: preserved
    evidence: "仍只有对称 ±24 小时配对和感染前 24 小时最低 SOFA/前后各 24 小时器官窗两种敏感性标签，且不得替换主结果；所有未来信息、跨划分、重复住院、重叠权重及结局驱动泄漏检查均保留。"
  - protected_id: PCR-010
    prior_locator: "Research design and methods > Mutually exclusive post-onset state and event system — complete subsection"
    revised_locator: "Research design and methods > Mutually exclusive post-onset state and event system — complete subsection"
    semantic_status: preserved
    evidence: "六类互斥状态的 12 小时赋值与优先级未变；恢复、恶化、存活出 ICU、转院和死亡的定义、可用时点、吸收或竞争角色及无法排序时的处理均一致。"
  - protected_id: PCR-011
    prior_locator: "Research design and methods > Observational target, anchoring and abstention — complete subsection"
    revised_locator: "Research design and methods > Observational target, anchoring and abstention — complete subsection"
    semantic_status: preserved
    evidence: "联合预测/生成目标及 A_t 的非因果解释未变；锚定、K、状态模式、滞后、20 个种子、缺失敏感性参数、行动重叠和有效样本量阈值，以及 90%/80%/80%/0.70 的解释限制均逐项保留。"
  - protected_id: PCR-012
    prior_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery — complete subsection and standards table"
    revised_locator: "Research design and methods > Simulation and semi-synthetic recovery tests — complete subsection and standards table"
    semantic_status: preserved
    evidence: "仅将名称改为模拟恢复检验；月 7–10、至少 1,000 次或 Monte Carlo 标准误≤0.02、全部生成场景以及 0.80、0.05、0.90–0.98、0.10、0.05 等恢复、覆盖、错误发现和校准标准均未改变。"
  - protected_id: PCR-013
    prior_locator: "Research design and methods > Hospital-based cross-database validation — complete subsection"
    revised_locator: "Research design and methods > Hospital-based cross-database validation — complete subsection"
    semantic_status: preserved
    evidence: "种子 20260717、医院分层 30%/70% 划分、跨分区患者排除、首次合格记录、结局前排除报告、测试集优先连通分量敏感性、独立保管和三种外部分析方式分报均保持不变。"
  - protected_id: PCR-014
    prior_locator: "Research design and methods > Trial-specific mapping to observed visits and independent clinical-state analysis — Trial semantics/common-anchor eligibility and Prespecified mapping paragraphs"
    revised_locator: "Research design and methods > Trial-specific mapping to observed visits and independent clinical-state analysis — Trial semantics/common-anchor eligibility and Prespecified mapping paragraphs"
    semantic_status: preserved
    evidence: "新端点的事后次要探索性地位、原终点另报、授权和原始语义核验、共同锚点资格及排除、每试验至少两个锚点、WBC/CRP 候选地位、固定标准化/SVD 公式、符号规则和不得用 RCT 分组或结局拟合均保留。"
  - protected_id: PCR-015
    prior_locator: "Research design and methods > Trial-specific mapping to observed visits and independent clinical-state analysis — Agreement/error standards, mapped estimand, and independent clinical-state paragraphs"
    revised_locator: "Research design and methods > Trial-specific mapping to observed visits and independent clinical-state analysis — Agreement/error standards, mapped estimand, and independent clinical-state paragraphs"
    semantic_status: preserved
    evidence: "eICU D7/D8 评价的能量≥50%、相关≥0.70、误差≤0.50、截距/斜率/覆盖/锚点校准、RCT 80%/60% 条件均不变；死亡—住院—出院排序、概率比较、SOFA 独立替代及语义不足时不建端点的规则也一致。"
  - protected_id: PCR-016
    prior_locator: "Research design and methods > Trial-specific mapping to observed visits and independent clinical-state analysis — trial analysis table and final sparse-visit paragraph"
    revised_locator: "Research design and methods > Trial-specific mapping to observed visits and independent clinical-state analysis — trial analysis table and final sparse-visit paragraph"
    semantic_status: preserved
    evidence: "两试验的目标分析集、完整结局或改良意向治疗边界、617/671/658 敏感性集、D1/D0 基线限制、缺失插补信息、δ 与转折点、界限分析、Holm 0.05、探索性 FDR、交互限定及禁止伪连续插值均未改变。"
  - protected_id: PCR-017
    prior_locator: "Research content and work packages > Conjunctive stage-II success definition — complete subsection"
    revised_locator: "Research content and work packages > Prespecified criteria for completing the 24-month validation stage — complete subsection"
    semantic_status: preserved
    evidence: "五类证据必须同时满足且不得相互或由 RCT 补足的规则不变；双库支持、恢复或降级命名、Brier 上侧 95% 界≤+0.01、校准 0.80–1.20、风险误差≤0.02、无高严重度泄漏、≥20 家医院、状态≥0.70、符号≥0.80 及只收紧标准均保留。"
  - protected_id: PCR-018
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Planned outputs; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence progression"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Planned outputs; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence progression; Current resource and evidence status"
    semantic_status: preserved
    evidence: "所有标签、审计、模型、恢复、外部验证和 RCT 仍为计划产物；阶段 II 所需产物、跨数据库稳定最低端点、RCT 的有限组间差异范围及条件性整合/验证增量均未增强，文献证据状态也未提高。"
  - protected_id: PCR-019
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions — complete subsection"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions — complete subsection"
    semantic_status: preserved
    evidence: "模拟参数范围和多类别校准细节仍明确为待登记；月 7 前或查看外部结果前的时限、三类允许依据、硬标准只收紧以及未登记不得形成恢复或阶段 II 结论的后果均保留在唯一权威位置。"
  - protected_id: PCR-020
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions — items 1–5"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions — items 1–5"
    semantic_status: preserved
    evidence: "访问和人员不确定性、标签与时间泄漏、潜在状态不可直接解释、完整恢复与对齐条件、非随机缺失和治疗支持限制、阴性对照边界，以及不更新参数测试不可由有限更新挽救的限制均未弱化。"
  - protected_id: PCR-021
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions — items 6–9"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions — items 6–9"
    semantic_status: preserved
    evidence: "RCT 仍仅为潜在数据源且授权/原始语义/映射待核实；两试验不得合并、稀疏访视不得伪连续化、不得事后亚组挽救，非系统综述边界、全部非因果与非工具主张及低至中等检索置信度均保留。"
  - protected_id: PCR-022
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions — public-data access through timeline rows"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions — public-data access through timeline rows"
    semantic_status: preserved
    evidence: "月 3、月 6、月 12、月 20、月 24 的触发与停止规则，以及 20 家医院、每参数 10 个外部事件/转移、70%/80% 锚点覆盖、10% 排除、5%/95% 行动和 20% 有效样本等阈值、替代方案及不可挽救结论均未改变。"
  - protected_id: PCR-023
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions — RCT and literature-positioning rows"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions — RCT and literature-positioning rows"
    semantic_status: preserved
    evidence: "RCT 授权、核心语义、每试验至少两个锚点及一致性失败时的停止/独立 SOFA 端点规则保留；结果不一致或区间与无差异相容时仍分报且不合并/不事后选亚组，更强首次或不存在性主张仍需扩展检索。"
  - protected_id: PCR-024
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions — items 7–9; Title and positioning claim-support table — bounded-search row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions — items 7–9; Title and positioning claim-support table — bounded-search row"
    semantic_status: preserved
    evidence: "真实因果网络、治疗因果效应、反事实策略、机制、中介、控制、数字孪生、以 RCT 验证整个系统、伪连续轨迹、有限更新冒充外部验证、已验证工具/平台/推广及系统综述或全球首次等不支持主张均继续被明确排除。"
  - protected_id: PCR-025
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification criteria and result interpretation — complete table"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification criteria and result interpretation — complete table"
    semantic_status: preserved
    evidence: "时间泄漏、双库支持不足、恢复失败、缺失或重叠敏感、无参数更新外测失败、试验映射失败、试验语义不可审计及五类证据全达标的八项结果解释均保留；最终支持范围仍限于候选表征，而非因果机制或临床工具。"
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

`scientific_content_preserved`。v029 保留了 v028 的研究身份、研究对象与推断单位、数据和试验来源、全部设计与分析承诺、数值和时间规则、验证逻辑、证据状态、主张强度、工作假设、局限、替代方案、停止条件及明确不支持的主张。修订主要包括标题与句法消歧、首次出现时定义“阶段 II 达标”和“模拟恢复检验”、将长问题拆为三个子问题，以及用自然语言说明未达标时不作相应结构解释。这些变化没有改变受保护科学含义或强度，也没有新增数据、方法、结果或证据。

revision delta 将 `scientific_change` 明确记为 `false`，并将变更限定为 editorial repair；对两版 dossier 的直接比较与这一声明一致。未发现身份漂移、未声明的科学变化、把计划写成结果、主张增强、局限弱化或可行性问题被隐藏。

## Protected-content trace

25 个受保护条目均恰好核验一次并可在 v029 中定位。主要位置变化如下：

- PCR-001 的核心研究问题由一个长句改为三个子问题；独立临床状态替代方案仍保留在目标 4 和试验方法中。
- PCR-005、PCR-012、PCR-017 的标题和术语分别改为更直接的 24 个月验证阶段、模拟恢复检验及阶段 II 达标标准；全部时序、阈值和合取判定不变。
- PCR-014 至 PCR-016 将 RCT 映射对象明确为阶段 II 达标后冻结的模型；这使原有前置条件更清楚，未改变映射公式、资格、阈值、估计对象或替代分析。
- PCR-019 至 PCR-023 仍集中在 `Feasibility, resources, risks, alternatives, and stop conditions`，未被删除、分散或弱化。
- PCR-024 的不支持主张仍同时受局限段和定位表约束；PCR-018 与 PCR-025 的计划状态、证据强度和失败解释保持原界限。

## Required routing

v029 可进入全新的 narrative assessment 和 academic language assessment。后续评审仍须使用新的独立实例；本报告不判断叙事质量、语言质量或科学设计本身是否正确。
