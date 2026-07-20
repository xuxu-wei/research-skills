---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-r044
review_id: preservation-review-r044
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-r044
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r044
input_artifact_ids:
  - idea-dossier-I01-001-v029
  - idea-dossier-I01-001-v030
  - protected-content-register-I01-001-v005
  - revision-delta-I01-001-v029-to-v030
input_versions:
  - v029
  - v030
  - v005
  - v030
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v029
    version: v029
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/idea-dossier-v029.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v030
    version: v030
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/idea-dossier-v030.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v005
    version: v005
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/protected-content-register-v005.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v029-to-v030
    version: v030
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/revision-delta-v029-to-v030.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/idea-dossier-v029.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/idea-dossier-v030.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/protected-content-register-v005.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/revision-delta-v029-to-v030.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter > identity_anchor; # title; ## Research question, objectives, and core hypothesis > ### Primary research question"
    revised_locator: "YAML frontmatter > identity_anchor; # title; ## Research question, objectives, and core hypothesis > ### Primary research question"
    semantic_status: preserved
    evidence: >-
      五项 identity_anchor 值逐字保持；研究对象、患者—时间状态及转移推断单位、三个核心问题、24 个月阶段 II 目标和有条件的两项 RCT 数据来源均未改变。标题只展开 ICU 与 RCT。
  - protected_id: PCR-002
    prior_locator: "## Research question, objectives, and core hypothesis > ### Objectives and ### Core hypothesis"
    revised_locator: "## Research question, objectives, and core hypothesis > ### Objectives and ### Core hypothesis"
    semantic_status: preserved
    evidence: >-
      四项目标、复杂候选的双库支持与预先确定条件、至多一个受限复杂候选，以及主要任务、恢复检验、外部验证和 RCT 输出分别判定的边界全部保留；错误结构措辞仅明确了判断对象。
  - protected_id: PCR-003
    prior_locator: "## Research content and work packages > ### Twenty-four-month programme"
    revised_locator: "## Research content and work packages > ### Twenty-four-month programme"
    semantic_status: preserved
    evidence: >-
      月 0–3、4–6、7–12、13–18/20、21–24 的资源核实、双库审计、基线与恢复实验、冻结分析包和不更新参数外部验证均保留；时间外/医院外仅改为时间留出/医院留出。
  - protected_id: PCR-004
    prior_locator: "## Research content and work packages > ### Prespecified criteria for completing the 24-month validation stage"
    revised_locator: "## Research content and work packages > ### Prespecified criteria for completing the 24-month validation stage"
    semantic_status: preserved
    evidence: >-
      五类证据及不得相互补足的规则未变；+0.01、0.80–1.20、0.02、20 家医院、0.70、0.80 等阈值均相同，月 6 前登记且硬标准只可收紧的限制也相同。
  - protected_id: PCR-005
    prior_locator: "## Research content and work packages > ### Work packages; paragraph beginning ‘最低分析顺序为’"
    revised_locator: "## Research content and work packages > ### Work packages; paragraph beginning ‘最低分析顺序为’"
    semantic_status: preserved
    evidence: >-
      WP1–WP4 的月份、职责与输出均保留，最低分析顺序逐项相同；WP3 仅把不解释的对象改写为明确的不具备解释资格清单。
  - protected_id: PCR-006
    prior_locator: "## Data, materials, and existing evidence base > ### Current resource and evidence status"
    revised_locator: "## Data, materials, and existing evidence base > ### Current resource and evidence status"
    semantic_status: preserved
    evidence: >-
      数据库存在与版本已核实、访问和项目支持未核实、试验材料仅为衍生报告、人员承诺未核实、所有新结果尚未生成，以及有界检索的高置信/低至中等置信分级均未改变；缩写展开未提升证据状态。
  - protected_id: PCR-007
    prior_locator: "## Data, materials, and existing evidence base > ### Public ICU database roles and observability audit"
    revised_locator: "## Data, materials, and existing evidence base > ### Public ICU database roles and observability audit"
    semantic_status: preserved
    evidence: >-
      MIMIC 开发、eICU 外部及备份库角色保持；20/10 事件或转移、12/24 小时方案、每维至少两个锚点、30% 时间格、70% 医院、80% 患者、K≤4 和模式≤3 等支持规则全部相同。
  - protected_id: PCR-008
    prior_locator: "## Data, materials, and existing evidence base > ### Prespecified variable roles"
    revised_locator: "## Data, materials, and existing evidence base > ### Prespecified variable roles"
    semantic_status: preserved
    evidence: >-
      Y_t、A_t、M_t、标签与 B 的用途和隔离规则逐项相同；CRRT 只作全称定义，治疗、标签和生理锚点之间的边界未变。
  - protected_id: PCR-009
    prior_locator: "## Data, materials, and existing evidence base > ### Local RCT evidence; paragraph beginning ‘EXIT-SEP’"
    revised_locator: "## Data, materials, and existing evidence base > ### Local RCT evidence; paragraph beginning ‘EXIT-SEP’"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 的 45 个 ICU、1,817 例随机化、1,760 例状态明确、395 例死亡、57 例未知、SOFA 1,750/1,542/1,296、乳酸 855 至 223 及 D1/D7 时序待核验均相同。
  - protected_id: PCR-010
    prior_locator: "## Data, materials, and existing evidence base > ### Local RCT evidence; paragraph beginning ‘XBJ-SCAP’"
    revised_locator: "## Data, materials, and existing evidence base > ### Local RCT evidence; paragraph beginning ‘XBJ-SCAP’"
    semantic_status: preserved
    evidence: >-
      XBJ-SCAP 的 710、675、617、671、658 例人群及 SOFA、WBC、CRP 非缺失数均相同；时序待核验、SCAP 不等于 Sepsis-3、结构性缺失字段和 D-dimer 单位边界未变。
  - protected_id: PCR-011
    prior_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks; Primary pre-onset task column"
    revised_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks; Primary pre-onset task column"
    semantic_status: preserved
    evidence: >-
      发病前人群、72/24 小时感染配对、SOFA 基线与 −48/+24 小时窗、信息可用时刻、12 小时时点和结局处理、估计对象、指标及聚类区间均逐项保持；AUPRC 只补充全称。
  - protected_id: PCR-012
    prior_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks; Primary post-onset task column"
    revised_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks; Primary post-onset task column"
    semantic_status: preserved
    evidence: >-
      首次发病与延迟进入、24 小时恢复窗口、每 12 小时评价、第 7 日主要和第 14 日敏感性、终止状态、Aalen–Johansen、多类别 Brier 和聚类报告规则均未改变。
  - protected_id: PCR-013
    prior_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks; paragraph beginning ‘主标签之外’; ## Key techniques and implementation > item 10"
    revised_locator: "## Research design and methods > ### Protocol specifications for the two primary clinical tasks; paragraph beginning ‘主标签之外’; ## Key techniques and implementation > item 10"
    semantic_status: preserved
    evidence: >-
      两种且仅两种标签敏感性、不得替换主结果、完整泄漏核查项目、预先裁定的时间反转与阴性对照及未达标结果报告均保留；阴性结果不能证明模型正确仍在限制部分明确保留。
  - protected_id: PCR-014
    prior_locator: "## Research design and methods > ### Mutually exclusive post-onset state and event system"
    revised_locator: "## Research design and methods > ### Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      六级互斥优先顺序、SOFA 下降或增加阈值、连续 24 小时恢复、新启或升级三类器官支持、事件与信息时刻、吸收状态、转院处理、加权与界限分析均相同。
  - protected_id: PCR-015
    prior_locator: "## Research design and methods > ### Observational target, anchoring and abstention"
    revised_locator: "## Research design and methods > ### Observational target, anchoring and abstention"
    semantic_status: preserved
    evidence: >-
      联合分布目标及 A_t 非因果解释保持；每维至少两个锚点、首载荷 +1、K≤4、模式≤3、滞后 1 或 2 格、20 个种子和只解释对齐量等约束未变。
  - protected_id: PCR-016
    prior_locator: "## Research design and methods > ### Observational target, anchoring and abstention; paragraph beginning ‘非随机缺失主分析’"
    revised_locator: "## Research design and methods > ### Observational target, anchoring and abstention; paragraph beginning ‘非随机缺失主分析’"
    semantic_status: preserved
    evidence: >-
      MAR/选择模型、δ=−1/−0.5/0/+0.5/+1、转折点、行动比例 5%/95%、加权有效样本量 20%，以及 90%/80%/80%/0.70 的删除、合并或限制解释规则均未改变。
  - protected_id: PCR-017
    prior_locator: "## Research design and methods > ### Simulation and semi-synthetic recovery tests"
    revised_locator: "## Research design and methods > ### Simulation and semi-synthetic recovery tests"
    semantic_status: preserved
    evidence: >-
      月 7–10、至少 1,000 次或标准误≤0.02、全部生成器与交叉情景，以及 0.80、90%、0.05、0.90–0.98、FDR≤0.10、假边≤0.05、错设≥80% 和校准阈值均保持；新措辞明确错误对象且仍要求不解释未达标结构。
  - protected_id: PCR-018
    prior_locator: "## Research design and methods > ### Hospital-based cross-database validation; paragraphs covering the hospital split and cross-partition patients"
    revised_locator: "## Research design and methods > ### Hospital-based cross-database validation; hospital split paragraph and numbered items 1–5"
    semantic_status: preserved
    evidence: >-
      固定种子 20260717、30%/70% 医院划分、医院优先、跨分区患者全部排除、不按患者重分、结局前特征报告、最终测试优先连通分量敏感性和保管人权限均未变。
  - protected_id: PCR-019
    prior_locator: "## Research design and methods > ### Hospital-based cross-database validation; paragraph beginning ‘确定标签’"
    revised_locator: "## Research design and methods > ### Hospital-based cross-database validation; paragraph beginning ‘确定标签’"
    semantic_status: preserved
    evidence: >-
      冻结标签至评价代码后，仍依次分报不更新参数、适配集重新校准和仅更新观测模型三种方式；完整重拟合或再开发仍明确不属于外部验证。
  - protected_id: PCR-020
    prior_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis; ‘试验语义与共同锚点资格’"
    revised_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis; opening and ‘试验语义与共同锚点资格’"
    semantic_status: preserved
    evidence: >-
      两项端点仍是试验后提出的次要探索性分析，原终点分开复现且不合并；阶段 II 后冻结、授权与原始语义核验、至少两个合格锚点及排除治疗、频率、标签和事后状态的规则均保持。
  - protected_id: PCR-021
    prior_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis; ‘预先确定的映射、映射输出和一致程度’ and ‘一致性与误差标准’"
    revised_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis; ‘预先确定的映射、映射输出和一致程度’ and ‘一致性与误差标准’"
    semantic_status: preserved
    evidence: >-
      C_r、开发集标准化、SVD、P_state/P_obs 公式、符号规则及禁用 RCT 分组/结局均相同；50%、0.70、0.50、0.20、0.80–1.20、0.90–0.98、80% 和 60% 的映射门槛全部保留。
  - protected_id: PCR-022
    prior_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis; ‘映射达到标准时的估计对象’ and ‘独立临床状态分析’"
    revised_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis; ‘映射达到标准时的估计对象’ and ‘独立临床状态分析’"
    semantic_status: preserved
    evidence: >-
      映射达标时的死亡最差、P_obs 排序、出院最有利及概率指数/胜出概率均保持；映射不足时的独立死亡/SOFA 端点和核心语义不可核实时不构造新端点的边界不变。
  - protected_id: PCR-023
    prior_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis; trial-specific table and following paragraph; ## Required analyses and evidence > RCT pre-start paragraph"
    revised_locator: "## Research design and methods > ### Trial-specific mapping to observed visits and independent clinical-state analysis; trial table and following paragraph; ## Required analyses and evidence > RCT pre-start paragraph"
    semantic_status: preserved
    evidence: >-
      两试验目标分析集、访视、基线限制、死亡/出院等级、多重插补、δ、转折点、界限分析、结构性缺失字段、Holm 0.05、探索性错误发现率和仅交互亚组规则均逐项相同。
  - protected_id: PCR-024
    prior_locator: "## Research design and methods > ### Secondary representation diagnostics; ## Evidence chains > ### Evidence chain: 两项主要任务与两项次要诊断; ## Required analyses and evidence > items 5–6"
    revised_locator: "## Research design and methods > ### Secondary representation diagnostics; ## Evidence chains > ### Evidence chain: 两项主要任务与两项次要诊断; ## Required analyses and evidence > items 5–6"
    semantic_status: preserved
    evidence: >-
      伪遮蔽和未来轨迹的全部评分、覆盖与分层仍在，伪遮蔽仍仅评价原实测值且只作诊断；标签/缺失敏感性、消融、接口、标签误差、阴性对照和聚类区间均保留。
  - protected_id: PCR-025
    prior_locator: "## Title, summary, audience, and positioning; ## Structured abstract; ## Title and positioning claim-support table"
    revised_locator: "## Title, summary, audience, and positioning; ## Structured abstract; ## Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      计划性证据整合、跨库验证、基准资源与可证伪设计的定位未变，所有结果仍明确尚未生成且贡献仍取决于未来结果。‘高水平论文’改为‘同行评议学术论文并以高影响力期刊投稿为目标’，没有降低论文交付目标，也没有把目标写成已完成成果。
  - protected_id: PCR-026
    prior_locator: "## Expected outputs, falsification criteria, and interpretations > ### Falsification criteria and result interpretation"
    revised_locator: "## Expected outputs, falsification criteria, and interpretations > ### Falsification criteria and result interpretation"
    semantic_status: preserved
    evidence: >-
      时间泄漏、双库支持、恢复失败、缺失/重叠敏感、不更新参数外部失败、映射失败、试验语义失败及五类证据全部达标的八种解释保持原强度；局部对象只被写得更明确。
  - protected_id: PCR-027
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Feasibility and resources"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      六类具名职责、人员和工时未核实、两个数据库及 K≤4/模式≤3/两任务/两诊断/至多一候选的范围均相同；24 个月最低交付与 RCT 不得补足核心缺口的边界不变。
  - protected_id: PCR-028
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Working assumptions"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Working assumptions"
    semantic_status: preserved
    evidence: >-
      两项待定假设的必含因素、月 7 与外部结果前登记时点、允许证据、未登记后果、硬标准只可收紧及事件/参数下限不得替代经验支持均保留；仅统一外部最终测试集名称。
  - protected_id: PCR-029
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions; items 1–5"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions; items 1–5"
    semantic_status: preserved
    evidence: >-
      数据与人员未落实、标签时序与泄漏、状态可识别条件、缺失机制与治疗支持、阴性对照边界，以及不更新参数验证与有限更新/再开发的区别均完整保留一次。
  - protected_id: PCR-030
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions; items 6–9"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions; items 6–9"
    semantic_status: preserved
    evidence: >-
      试验授权与语义未核实、两试验不合并、稀疏访视不形成连续轨迹、文献检索非系统综述及全部因果/机制/控制/数字孪生和临床推广边界均未删减或弱化。
  - protected_id: PCR-031
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Risks, alternatives, and stop conditions; rows ‘公共数据库访问或人员不足’ through ‘标签或数据泄漏’"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Risks, alternatives, and stop conditions; rows ‘公共数据库访问或人员不足’ through ‘标签或数据泄漏’"
    semantic_status: preserved
    evidence: >-
      月 3、月 6 和月 20 停止条件、备份库和 24 小时/事件时间替代、跨分区患者排除后的 20/10/70%/80%/10% 门槛及只作数据库描述的有界结论均相同。
  - protected_id: PCR-032
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Risks, alternatives, and stop conditions; rows ‘复杂状态不可恢复’ through ‘时间进度不足’"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Risks, alternatives, and stop conditions; rows ‘复杂状态不可恢复或错误结构被高置信判定为存在’ through ‘时间进度不足’"
    semantic_status: preserved
    evidence: >-
      恢复失败后的合并/删除和月 12 结束、δ/行动重叠/有效样本量失败后的不估计与不解释、外部验证失败后有限更新不得救援，以及月 20/月 24 停止条件均保持；语言替换没有放宽任何后果。
  - protected_id: PCR-033
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Risks, alternatives, and stop conditions; rows ‘RCT 授权、语义或映射不足’ through ‘文献定位证据不足’"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Risks, alternatives, and stop conditions; rows ‘RCT 授权、语义或映射不足’ through ‘文献定位证据不足’"
    semantic_status: preserved
    evidence: >-
      RCT 授权/语义/锚点/映射不足时的独立临床端点或停止规则、试验不一致时不合并且不以事后亚组救援、强创新主张需扩展检索的要求全部保留。
  - protected_id: PCR-034
    prior_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions; items 8–9; ## Title and positioning claim-support table"
    revised_locator: "## Feasibility, resources, risks, alternatives, and stop conditions > ### Limitations and boundary conditions; items 8–9; ## Title and positioning claim-support table; related falsification and risk rows"
    semantic_status: preserved
    evidence: >-
      未主张真实系统、因果网络或效应、反事实策略、机制、控制或数字孪生；RCT 不验证潜在动力学或完整模型；未主张现成工具、完成结果、无条件推广、单模块新颖或全球首次。两处重复文献边界虽删除，权威限制、主张表和风险行仍完整承载同一边界。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

`scientific_content_preserved`。冻结登记表的 34 个保护项均可在 v030 中定位，科学含义、证据状态、数值与时间规则、失败解释、停止条件和主张强度均与 v029 相同。修订只涉及缩写定义、术语标准化、句法拆分、局部指称明确、外部测试集命名统一，以及删除两处在权威限制和风险位置已有完整表达的重复文献边界。

特别核对了交付目标与解释边界：`高水平论文和可审查的科学证据` 改为 `同行评议学术论文并以高影响力期刊投稿为目标，同时形成可审查的科学证据`，投稿目标没有弱化，也没有被表述为已完成成果；`不作相应结构解释` 的替换均明确列出不具备解释资格的状态、转移、边或依赖关系及原因，未把停止解释降格为仅作提示。

## Protected-content trace

- 身份、研究问题和 24 个月阶段 II 目标保留在 frontmatter、标题和研究问题部分。
- 五类阶段 II 证据、两项主要任务、全部模拟恢复和跨库验证阈值均保留在原功能位置；时间外/医院外/最终测试集只作更明确的名称替换。
- 试验样本、访视、映射公式、门槛、缺失处理、多重性和独立临床状态后备分支均保持。
- 两处删除的文献定位段落是重复说明；低至中等置信、非系统综述边界、扩展检索触发和禁止全球首次等主张仍完整保留在 gap、主张支持表、限制项目 8 和文献风险行。

## Required routing

该 dossier 可进入新的 narrative assessment 与 academic language assessment；无需返回科学审查。
