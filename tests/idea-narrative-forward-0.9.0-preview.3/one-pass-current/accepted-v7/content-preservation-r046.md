---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-check-I01-001-r046
review_id: content-preservation-r046
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-r046
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r046
input_artifact_ids:
  - idea-dossier-I01-001-v030
  - idea-dossier-I01-001-v031
  - protected-content-register-I01-001-v006
  - revision-delta-I01-001-v030-to-v031
input_versions:
  - v030
  - v031
  - v006
  - v031
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v030
    version: v030
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/idea-dossier-v030.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v031
    version: v031
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v7/idea-dossier-v031.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/protected-content-register-v006.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v030-to-v031
    version: v031
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v7/revision-delta-v030-to-v031.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/idea-dossier-v030.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v7/idea-dossier-v031.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/protected-content-register-v006.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v7/revision-delta-v030-to-v031.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter > identity_anchor"
    revised_locator: "YAML frontmatter > identity_anchor"
    semantic_status: preserved
    evidence: |-
      五个身份锚点的英文值保持相同：主要问题、24 个月阶段 II 目标、纵向脓毒症相关 ICU 对象、三类证据基础，以及患者—时间状态与转移并尊重患者和医院聚类的推断单位均未变。
  - protected_id: PCR-002
    prior_locator: "Research question, objectives, and core hypothesis > Primary research question and Objectives"
    revised_locator: "Research question, objectives, and core hypothesis > Primary research question and Objectives"
    semantic_status: preserved
    evidence: |-
      未发病在险时段与发病后轨迹、四段病程、未参与开发医院和数据库中的稳定性、阶段 II 与实际访视映射双重条件，以及四项目标的设计范围和独立临床状态备选均保留。
  - protected_id: PCR-003
    prior_locator: "Title, summary, audience, and positioning > summary and positioning"
    revised_locator: "Title, summary, audience, and positioning > summary and positioning"
    semantic_status: preserved
    evidence: |-
      24 个月计划、两个先审计公共库、不更新参数的主要外部检验、五类阶段 II 证据、分试验且有授权/语义/访视条件的 RCT 次要分析，以及整合、验证、基准资源、可证伪设计和单模块非新颖的定位均保持原强度。
  - protected_id: PCR-004
    prior_locator: "Structured abstract > Expected result"
    revised_locator: "Structured abstract > Expected result"
    semantic_status: preserved
    evidence: |-
      双时刻标签、双库审计、互斥状态、恢复检验及不具解释资格项目、两主任务、两次诊断、无参数更新外验和条件性试验映射均仍是计划产物；映射不足时的独立临床状态分支及“非现有模型或已完成结果”边界未变。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Current resource and evidence status"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status"
    semantic_status: preserved
    evidence: |-
      两库存在与版本已核实但访问/可执行性未核实、凭证和提取事项未核实、项目计数未生成、RCT 材料仅为衍生报告、原始语义未核实、WBC/CRP 仅候选、人员承诺未核实、无新结果，以及截至 2026-07-17 的高置信模块先例和低至中等置信组合缺口均保留。
  - protected_id: PCR-006
    prior_locator: "Data, materials, and existing evidence base > Public ICU database roles and observability audit"
    revised_locator: "Data, materials, and existing evidence base > Public ICU database roles and observability audit"
    semantic_status: preserved
    evidence: |-
      MIMIC-IV v3.1 的有条件开发库角色、eICU-CRD v2.0 的按医院适配/最终测试角色、月 0–3 预设并同等审计的备份库，以及共同层和库特异信息的准入边界未变。
  - protected_id: PCR-007
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence"
    revised_locator: "Data, materials, and existing evidence base > Local RCT evidence"
    semantic_status: preserved
    evidence: |-
      EXIT-SEP 的 45 个 ICU、1,817/1,760/395/57、SOFA 1,750/1,542/1,296、乳酸 855 至 223 及 D1/D7 待核验状态均在；XBJ-SCAP 的 710/675/617/671/658、SOFA 703/628/610、WBC 704/634/614、CRP 579/503/467、28 日 675、D0/D8 待核验、SCAP 边界、五类缺失字段和 D-dimer 单位状态均在。
  - protected_id: PCR-008
    prior_locator: "Research content and work packages > Twenty-four-month programme"
    revised_locator: "Research content and work packages > Twenty-four-month programme"
    semantic_status: preserved
    evidence: |-
      月 0–3、4–6、7–12、13–18/20、21–24 的工作顺序、六类职责和独立保管、三类简单基线先行、至多一个复杂候选、冻结分析包、无参数更新外验与两类有限更新分报，以及结果可见前的信息屏障均保留。
  - protected_id: PCR-009
    prior_locator: "Research content and work packages > Prespecified criteria for completing the 24-month validation stage"
    revised_locator: "Research content and work packages > Prespecified criteria for completing the 24-month validation stage"
    semantic_status: preserved
    evidence: |-
      五类证据全通过且不能互相补足的规则未变；双库支持、正确/零边/核心错设恢复、Brier 上侧 95% 界不超过 +0.01、斜率 0.80–1.20、绝对风险误差不超过 0.02、无高严重度泄漏、至少 20 家外部医院、状态不低于 0.70、符号不低于 0.80、适配结果分报和硬标准只可收紧均保留。
  - protected_id: PCR-010
    prior_locator: "Data, materials, and existing evidence base > Public ICU database roles and observability audit > audit table and 12-hour paragraph"
    revised_locator: "Public ICU database roles and observability audit > audit table; Working assumptions > item 3"
    semantic_status: changed
    evidence: |-
      首次合格记录、至少 20 家外部医院、自由参数的 20/10 支持、终止状态、12/24 小时规则、锚点的 2、30%、70% 和 80% 门槛、观测过程保留、K=min(4,审计模块数)及前移例外均保留；但 v030 和冻结 register 明确规定“状态模式不超过 3”，v031 从审计规则删除该对象并改称“不超过 3”的计数对象未定、未明确前不得用于复杂候选模型选择。数值尚在，方法对象和适用状态已改变。
  - protected_id: PCR-011
    prior_locator: "Data, materials, and existing evidence base > Prespecified variable roles"
    revised_locator: "Data, materials, and existing evidence base > Prespecified variable roles"
    semantic_status: preserved
    evidence: |-
      Y_t、A_t、M_t、仅标签字段和 B 的内容、禁止用途、带时戳副本、信息可用顺序及显式未知值处理均保留相同含义。
  - protected_id: PCR-012
    prior_locator: "Research design and methods > Protocol specifications > Primary pre-onset task"
    revised_locator: "Research design and methods > Protocol specifications > Primary pre-onset task"
    semantic_status: preserved
    evidence: |-
      成人与首个合格 ICU、至少 12 小时历史、72/24 小时感染配对、基线和滚动 SOFA、感染前 48 至后 24 小时窗口、标签可用时刻、12 小时预测时点与未来 12 小时、住院权重 1、终止/删失、格内顺序、离散多项风险、指标和双层 bootstrap 全部保留。
  - protected_id: PCR-013
    prior_locator: "Research design and methods > Protocol specifications > Primary post-onset task"
    revised_locator: "Research design and methods > Protocol specifications > Primary post-onset task"
    semantic_status: preserved
    evidence: |-
      首次发病和延迟进入、发病零点与 24 小时恢复可用时刻、每 12 小时评价、第 7 日主分析和第 14 日敏感性、三类终止、器官支持行动分离、有利集合及分项报告、多状态/Aalen–Johansen、指标、分层和有效转移数均未变。
  - protected_id: PCR-014
    prior_locator: "Research design and methods > Protocol specifications > two sensitivity-label paragraph"
    revised_locator: "Research design and methods > Protocol specifications > two sensitivity-label paragraph"
    semantic_status: preserved
    evidence: |-
      仍恰有两种不替换主结果的敏感性标签：培养—抗菌药对称 ±24 小时，以及感染前 24 小时最低 SOFA 配合前后各 24 小时器官功能窗；十类时间与划分泄漏核查对象均保留。
  - protected_id: PCR-015
    prior_locator: "Research design and methods > Mutually exclusive post-onset state and event system"
    revised_locator: "Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: |-
      12 小时互斥赋值、死亡至持续脓毒症的优先级、同戳处理和事件时间敏感性，以及六种状态/事件的 SOFA 阈值、24 小时恢复、双时刻、复发、行动分离、竞争终止、吸收性和界限分析均保留。
  - protected_id: PCR-016
    prior_locator: "Research design and methods > Observational target, anchoring and abstention"
    revised_locator: "Observational target, anchoring and abstention; Working assumptions > item 3"
    semantic_status: changed
    evidence: |-
      X_t/Y_t/A_t/M_t/B/S、联合分布、非因果解释、每维至少两个锚点、首载荷 +1、尺度、交叉载荷、K≤4、1/2 格滞后、瞬时环、多种子对齐和可解释量均保留；但 v030 和 register 的“状态模式≤3”从锚定与可识别约束中删除，v031 改为对象未定且暂不得使用，改变了原先已生效的复杂度限制。
  - protected_id: PCR-017
    prior_locator: "Research design and methods > Observational target, anchoring and abstention > nonrandom-missingness paragraph"
    revised_locator: "Research design and methods > Observational target, anchoring and abstention > nonrandom-missingness paragraph"
    semantic_status: preserved
    evidence: |-
      MAR/选择模型基线、δ=−1/−0.5/0/+0.5/+1、转折点、按状态/医院/时间层的行动概率和有效样本量、5%/95% 与 20% 禁止估计规则，以及 90%/80%/80%/0.70/区间标准和预测不能补救均保留。
  - protected_id: PCR-018
    prior_locator: "Research design and methods > Simulation and semi-synthetic recovery tests"
    revised_locator: "Research design and methods > Simulation and semi-synthetic recovery tests"
    semantic_status: preserved
    evidence: |-
      月 7–10、每情景至少 1,000 次或 Monte Carlo 标准误不超过 0.02、六类生成情景、全部交叉因素，以及状态 0.80/90%、转移 0.05 与 0.90–0.98、符号滞后 0.80、边 0.80/0.10、假边 0.05、错设 80%/0.05、校准 0.80–1.20/0.02 和解释后果均保留；场景措辞的展开未改变测试集合。
  - protected_id: PCR-019
    prior_locator: "Research design and methods > Hospital-based cross-database validation > split and patient-handling rules"
    revised_locator: "Research design and methods > Hospital-based cross-database validation > split and patient-handling rules"
    semantic_status: preserved
    evidence: |-
      体量四分位/接口分层、种子 20260717、医院 30%/70%、医院先于患者、固定划分和链接版本、跨分区患者全排除、同区首次合格记录、结局前排除审计、测试优先连通分量和独立保管人检查均未变。
  - protected_id: PCR-020
    prior_locator: "Research design and methods > Hospital-based cross-database validation > three external-analysis modes"
    revised_locator: "Research design and methods > Hospital-based cross-database validation > three external-analysis modes"
    semantic_status: preserved
    evidence: |-
      固定分析要素后按无参数更新、适配集截距/斜率再校准、仅更新观测模型且冻结状态/转移的顺序分报仍在；目标库完整重拟合/再开发仍不属于外部验证，有限更新不能补救无更新失败的限制仍保留。
  - protected_id: PCR-021
    prior_locator: "Research design and methods > Trial-specific mapping > semantics, anchor eligibility, and mapping"
    revised_locator: "Research design and methods > Trial-specific mapping > numbered eligibility and mapping lists"
    semantic_status: preserved
    evidence: |-
      次要探索性、原终点另报、分试验、阶段 II 后冻结、授权和原始语义、共同锚点四项资格与至少两个锚点、WBC/CRP/D-dimer 边界，以及 MIMIC 标准化、Z_C、SVD、P_state、P_obs、并列/方向和禁止使用 RCT 分组/结局/跨试验数据均保留；列表化仅改变呈现。
  - protected_id: PCR-022
    prior_locator: "Research design and methods > Trial-specific mapping > Consistency and error standards"
    revised_locator: "Research design and methods > Trial-specific mapping > Consistency and error standards"
    semantic_status: preserved
    evidence: |-
      eICU D7/D8 先验评价及不按 RCT 调整、Frobenius 50%、相关 0.70、归一化误差 0.50、截距 0.20、斜率 0.80–1.20、覆盖 0.90–0.98、锚点校准、试验合理范围 80%、至少两个锚点的可计算比例 60%、全项通过和禁按试验重估权重均未变。
  - protected_id: PCR-023
    prior_locator: "Research design and methods > Trial-specific mapping > mapping-passing and independent-state estimands"
    revised_locator: "Research design and methods > Trial-specific mapping > mapping-passing and independent-state estimands"
    semantic_status: preserved
    evidence: |-
      映射通过时死亡最差、P_obs 高差低好、存活出院最优及中心/分层相容概率指数或胜出概率不变；映射不足但必要语义可核时的独立死亡—SOFA—出院端点，以及核心语义不足时不构造新端点的分支均保留。
  - protected_id: PCR-024
    prior_locator: "Research design and methods > Trial-specific mapping > trial table and sparse-visits paragraph"
    revised_locator: "Research design and methods > Trial-specific mapping > trial table and sparse-visits paragraph"
    semantic_status: preserved
    evidence: |-
      EXIT-SEP 1,817/1,760 与 D7/D1 边界、XBJ-SCAP 710/675/617/671/658 与 D8/D0 边界、死亡/出院排序、多重插补与重算、Rubin/聚类 bootstrap、δ±0.5/±1、转折和界限、结构缺失不插补、Holm 0.05、其他 FDR、亚组交互、稀疏访视不插值和不合并均保留。
  - protected_id: PCR-025
    prior_locator: "Research design and methods > Secondary representation diagnostics"
    revised_locator: "Research design and methods > Secondary representation diagnostics"
    semantic_status: preserved
    evidence: |-
      伪遮蔽 MAE/RMSE/对数评分/覆盖，未来轨迹的连续等级概率评分/负对数似然/占用/结局校准和四类分层均未变；v031 明示其不支持更广恢复、验证或因果主张，是对 v030“只承担表征诊断功能”的同强度展开。
  - protected_id: PCR-026
    prior_locator: "Required analyses and evidence"
    revised_locator: "Required analyses and evidence"
    semantic_status: preserved
    evidence: |-
      阶段 II 的八类交付及 RCT 启动前的授权、57 例未知状态、随机集与全分析集差异、锚点/单位/访视/映射、并列、插补、中心、Holm 和交互规范均保留；恢复情景改为展开后的同一组对象。
  - protected_id: PCR-027
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification criteria and result interpretation"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification criteria and result interpretation"
    semantic_status: preserved
    evidence: |-
      时间泄漏、双库支持不足、恢复失败、缺失/重叠不足、无参数更新外验失败、试验映射失败、核心试验语义失败的解释边界，以及仅五类阶段 II 证据全通过时的正面解释均保留原强度。
  - protected_id: PCR-028
    prior_locator: "Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence progression"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence progression"
    semantic_status: preserved
    evidence: |-
      数据可追溯、恢复与两主任务、跨数据库稳定、随机访视摘要、独立临床状态五级证据阶梯及各自必要证据和条件强度未变；实证贡献继续以“若计划得到执行”为条件。
  - protected_id: PCR-029
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    revised_locator: "Feasibility and resources; Working assumptions > item 3"
    semantic_status: changed
    evidence: |-
      六个最低职责、人员/工时未核实、两主库、K≤4、两主任务、两次诊断、至多一复杂候选、资源状态、24 个月最低交付和 RCT 位于最低交付之外均保留；但 v030 和 register 把“状态模式≤3”列为计算范围，v031 从计算范围删除并改成计数对象未定、方法学批准不存在且暂不得用于选择。该约束不再具有相同处置，故并非 retained_once_at_authority_location。
  - protected_id: PCR-030
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > items 1-2"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > items 1-2"
    semantic_status: preserved
    evidence: |-
      模拟参数登记的情景集合、三方负责人、月 7 前登记、允许证据来源和未登记后果，以及多类别校准估计量/置信界/细化阈值的未决状态、固定指标、仅收紧、外测前登记、允许证据来源与未登记后果均保留。
  - protected_id: PCR-031
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations > items 1-5"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations > items 1-5"
    semantic_status: preserved
    evidence: |-
      数据/人员/结果状态、标签与七类时间泄漏、潜在状态可识别性及预测不能补救、测量过程/重叠/有效样本量/阴性对照边界，以及无参数更新主证据和有限更新不能补救、跨区排除可能削弱支持的五项限制均保留。
  - protected_id: PCR-032
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations > items 6-8"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations > items 6-8"
    semantic_status: preserved
    evidence: |-
      两试验仅为潜在个体源且衍生材料不能替代授权/原始语义、试验差异要求分报且稀疏访视不支持伪连续轨迹、结果方向/区间不能事后亚组补救，以及非系统检索的完整缺口清单和低至中等置信边界均未变。
  - protected_id: PCR-033
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: |-
      11 个触发—替代—停止/有界结论分支均保留，包括月 3/6/12/20/24、20 家医院、10 个外部事件或转移、70%/80%/10%、5%/95%/20%、无参数更新失败、RCT 授权/语义/至少两个锚点、试验不一致和文献定位边界。
  - protected_id: PCR-034
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations > item 9"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations > item 9"
    semantic_status: preserved
    evidence: |-
      真实因果网络、治疗因果效应、反事实策略、机制、中介、控制和数字孪生均仍不受支持；条件性 RCT 只支持实际访视摘要或独立临床状态的随机组差异，且不能验证未测动力学、转移边或整体模型；非已验证模型/临床工具/药物平台和非无条件推广边界未变。
  - protected_id: PCR-035
    prior_locator: "Title and positioning claim-support table > bounded-search row"
    revised_locator: "Title and positioning claim-support table > bounded-search row"
    semantic_status: preserved
    evidence: |-
      截至 2026-07-17 仅以低至中等置信未发现完整组合先例的边界保持不变；扩大检索和完成研究前不主张科学或方法首创，且单模块不主张新颖，全球不存在、新算法、无专利和临床首次仍不受支持。
undeclared_scientific_changes:
  - change_id: PRES-R046-001
    prior_meaning: "状态模式的计数对象已经确定，且上限为 3；该上限属于审计、锚定/可识别约束和计算范围。"
    revised_meaning: "上限 3 的计数对象尚未确定，也没有方法学批准；明确前不得用于复杂候选模型选择。"
    affected_protected_ids: [PCR-010, PCR-016, PCR-029]
    declaration_status: "revision delta 明确声称科学内容未改变，因此没有把此变化声明为科学变更。"
findings:
  - finding_id: PRES-R046-001
    affected_protected_ids: [PCR-010, PCR-016, PCR-029]
    evidence: |-
      冻结 v030 在审计表、锚定与可识别约束、实施要点和可行性计算范围四处将“≤3”明确绑定到“状态模式”；冻结 register 也三次要求保留同一对象与上限。v031 删除这些有效方法约束并新增“计数对象未定、方法学批准不存在、明确前禁用”的工作假设。只依据本次获准读取的四个项目输入，无法把该新增不确定性视为原材料的忠实呈现；它改变了复杂度控制的对象和生效状态。
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

决定为 `editorial_scope_violation`。35 个保护项均已检查且各出现一次；其中 32 项保持原含义、数值、证据状态和主张强度，PCR-010、PCR-016、PCR-029 因同一项复杂度约束变化而标记为 `changed`。研究中心问题、对象、目的和总体范围未漂移，因此不属于 `identity_drift_detected`；差异报告又明确声称没有科学变化，因此也不属于 `scientific_change_declared`。

关键变化不是把未决原材料更清楚地说出来。v030 的可审计正文把“不超过 3”明确写为“状态模式不超过 3/状态模式≤3”，并使其同时承担数据审计、锚定/可识别约束和可行性计算范围三种方法功能；冻结 register 亦按这一含义保护。v031 则删除这些规定，新增“计数对象未确定”“方法学批准不存在”和“明确前不得用于复杂候选模型选择”。数值 3 虽被保留，计数对象与规则的生效状态已经改变。四个允许输入中没有证据支持把 v030/register 的明确状态降为未决状态，故这不是纯编辑性澄清，而是未声明的方法变更。

除该问题外，标题和摘要重述、复杂候选模型的命名统一、模拟情景的平行展开、试验映射列表化，以及次要诊断边界的明示，均保持相同科学含义和强度；所有其他已登记数值、时间规则、分支、失败解释、无补救条件、资源状态和不支持主张类别均可在 v031 追踪。

## Protected-content trace

- 32 项在原章节或等价的分层列表中保持同义；试验映射只由连续段落改为“资格—映射—判定”列表，公式和阈值未变。
- PCR-010 的审计表仍保留 K=min(4,审计模块数) 等支持规则，但删除了“状态模式不超过 3”，并把数值 3 移到 Working assumptions 第 3 项作为对象未决且暂不可用的上限。
- PCR-016 的锚定与可识别约束保留 K≤4、锚点、载荷、滞后和对齐规则，却删除了“状态模式≤3”；Working assumptions 第 3 项没有保留其原方法功能。
- PCR-029 的可行性计算范围保留两库、K≤4、两主任务、两次诊断和至多一个复杂候选模型，却删除“状态模式≤3”；新工作假设明确暂停该上限的模型选择用途。

## Required routing

v031 不得直接进入新的叙事与学术语言评估。应返回科学审查，先明确“≤3”的计数对象和方法学依据，并形成经批准的科学变更，或恢复 v030 与冻结 register 中“状态模式≤3”的原约束；随后需要由新的独立实例重新执行内容保持核验。
