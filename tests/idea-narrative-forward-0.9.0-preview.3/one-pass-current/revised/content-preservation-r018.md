---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r018
review_id: content-preservation-review-I01-001-r018
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-reviewer-r018
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r018
input_artifact_ids:
  - idea-dossier-I01-001-v006
  - idea-dossier-I01-001-v007
  - protected-content-register-I01-001-v006
  - revision-delta-I01-001-v006-to-v007
input_versions: [v006, v007, v006, v007]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v006.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v007
    version: v007
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v007.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/protected-content-register-v006.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v006-to-v007
    version: v007
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v006-to-v007.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v006.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v007.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/protected-content-register-v006.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v006-to-v007.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML identity_anchor; Research question, objectives, and core hypothesis > 主要研究问题"
    revised_locator: "YAML identity_anchor; Research question, objectives, and core hypothesis > 主要研究问题"
    semantic_status: preserved
    evidence: "v007 保留以脓毒症全病程为中心的知识约束、不确定性感知候选动态系统表征，仍覆盖发病前、首次发病、发病后状态与结局，未改成普通预后或泛 ICU 风险模型。"
  - protected_id: PCR-002
    prior_locator: "YAML identity_anchor.primary_objective; Research content and work packages; Contribution, innovation, impact, application, and closest-work comparison"
    revised_locator: "YAML identity_anchor.primary_objective; Research content and work packages; Contribution, innovation, impact, application, and closest-work comparison"
    semantic_status: preserved
    evidence: "v007 仍要求 24 个月内完成阶段 I–II，并保留证据整合、外部验证、基准与研究资源的交付定位，而非仅产出预测工具。"
  - protected_id: PCR-003
    prior_locator: "Research question, objectives, and core hypothesis > 主要研究问题 and 研究目标 4"
    revised_locator: "Research question, objectives, and core hypothesis > 主要研究问题 and 研究目标 4"
    semantic_status: preserved
    evidence: "v007 仍以阶段 II 成功、试验资料语义合格和观测桥接合格为前提，分试验比较第 7 日或第 8 日摘要；桥接不合格时仍转入独立 SOFA 端点。"
  - protected_id: PCR-004
    prior_locator: "YAML identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    semantic_status: preserved
    evidence: "研究对象仍是纵向脓毒症中心 ICU 患者系统，推断单位仍为患者—时间状态与状态转移，并保留患者和医院聚类。"
  - protected_id: PCR-005
    prior_locator: "Research content and work packages > 最低顺序; Feasibility > final paragraph"
    revised_locator: "Research content and work packages > 研究顺序; Feasibility > final paragraph"
    semantic_status: preserved
    evidence: "v007 仍把全病程连续体、公共 ICU 与条件性随机试验证据以及患者—时间推断单位列为身份边界，并明确改变这些要素即构成新研究构想。"
  - protected_id: PCR-006
    prior_locator: "Data, materials, and existing evidence base > resource table and database-role paragraphs"
    revised_locator: "Data, materials, and existing evidence base > resource table and database-role paragraphs"
    semantic_status: preserved
    evidence: "MIMIC-IV v3.1、eICU-CRD v2.0 的开发与外部角色及 HiRID/AmsterdamUMCdb 的预先指定备份条件均未改变。"
  - protected_id: PCR-007
    prior_locator: "Data, materials, and existing evidence base > resource table rows 1-3; Feasibility > 可行性与资源"
    revised_locator: "Data, materials, and existing evidence base > resource table rows 1-3; Feasibility > 可行性与资源"
    semantic_status: preserved
    evidence: "v007 继续区分已核验的数据库存在与版本和未核验的访问、协议、提取及项目支持，未把官方规模写成项目可用性证据。"
  - protected_id: PCR-008
    prior_locator: "Data, materials, and existing evidence base > EXIT-SEP and XBJ-SCAP rows and paragraphs"
    revised_locator: "Data, materials, and existing evidence base > EXIT-SEP and XBJ-SCAP rows and paragraphs"
    semantic_status: preserved
    evidence: "两项试验仍仅是条件性阶段 III 数据来源；本地衍生材料仍只支持稀疏性和字段缺口，不能替代授权、原始资料与核心语义核验。"
  - protected_id: PCR-009
    prior_locator: "Data, materials, and existing evidence base > roles rows; Feasibility > 可行性与资源"
    revised_locator: "Data, materials, and existing evidence base > roles rows; Feasibility > 可行性与资源"
    semantic_status: preserved
    evidence: "最低团队角色保持不变，v007 仍明确只有角色规范而没有具名人员、工时或承诺。"
  - protected_id: PCR-010
    prior_locator: "Data, materials, and existing evidence base > results and closest-work rows"
    revised_locator: "Data, materials, and existing evidence base > results and closest-work rows"
    semantic_status: preserved
    evidence: "v007 仍声明模型、模拟、外部测试和新试验结果尚未生成，并保持模块先例高置信、完整组合缺口低至中等置信的证据状态。"
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > timeline table and 最低顺序"
    revised_locator: "Research content and work packages > timeline table and 研究顺序"
    semantic_status: preserved
    evidence: "全部分析阶段及其先后关系未变；v007 仅把‘锁定/冻结’改写为对应的预先确定、定稿和结果访问限制。"
  - protected_id: PCR-012
    prior_locator: "Research design and methods > 两项主要临床任务的预定协议"
    revised_locator: "Research design and methods > 两项主要临床任务的预定协议"
    semantic_status: preserved
    evidence: "发病前任务的 12 小时地标、12–24 小时既往信息和未来 12 小时风险，以及发病后第 7 日主要终点和第 14 日敏感性分析均保留。"
  - protected_id: PCR-013
    prior_locator: "Research design and methods > task protocol and 主标签以外 paragraph"
    revised_locator: "Research design and methods > task protocol and 主标签以外 paragraph"
    semantic_status: preserved
    evidence: "主标签、双时钟、首次发病、延迟进入、竞争事件与泄漏防护均未变，两项标签敏感性分析及其不替代主结果的限制也完整保留。"
  - protected_id: PCR-014
    prior_locator: "Research design and methods > 发病后互斥状态"
    revised_locator: "Research design and methods > 发病后互斥状态"
    semantic_status: preserved
    evidence: "六类互斥状态的优先次序、连续 24 小时恢复条件、出院不替代恢复及行动派生标签隔离均逐项保留。"
  - protected_id: PCR-015
    prior_locator: "Data, materials, and existing evidence base > 主要角色 table; Research design and methods > 观察性目标、锚定和弃权"
    revised_locator: "Data, materials, and existing evidence base > 主要角色 table; Research design and methods > 观察性目标、锚定和弃权"
    semantic_status: preserved
    evidence: "Y_t、A_t、M_t、标签和 B 的角色隔离及共同层的语义、单位、时间和可见性要求均未改变。"
  - protected_id: PCR-016
    prior_locator: "Research design and methods > 观察性目标、锚定和弃权"
    revised_locator: "Research design and methods > 观察性目标、锚定和弃权"
    semantic_status: preserved
    evidence: "联合预测与生成目标、可解释不变量、每维至少两个锚点、首载荷 +1、K≤4、体制≤3 及 1 或 2 格滞后均保留。"
  - protected_id: PCR-017
    prior_locator: "Research design and methods > 基于预设绝对阈值的模拟恢复检验"
    revised_locator: "Research design and methods > 基于预设绝对阈值的模拟恢复检验"
    semantic_status: preserved
    evidence: "生成场景、至少 1,000 次重复或标准误≤0.02、全部恢复阈值与失败后的删除、合并、弃权或简单模型路线均未改变；仅明确了高置信误判率的名称。"
  - protected_id: PCR-018
    prior_locator: "Research design and methods > 观察性目标、锚定和弃权 paragraph 3"
    revised_locator: "Research design and methods > 观察性目标、锚定和弃权 paragraph 3"
    semantic_status: preserved
    evidence: "模式混合 δ 偏移、选择模型临界点、5%/95% 行动比例和 20% 有效样本量阈值及不得估计治疗作用的边界均保留。"
  - protected_id: PCR-019
    prior_locator: "Research design and methods > 医院优先的跨数据库外部验证"
    revised_locator: "Research design and methods > 医院优先的跨数据库外部验证"
    semantic_status: preserved
    evidence: "固定种子 20260717、30%/70% 医院分配、医院优先、跨分区患者全排除和测试集禁用事项均未改变。"
  - protected_id: PCR-020
    prior_locator: "Research design and methods > 医院优先的跨数据库外部验证 final paragraph"
    revised_locator: "Research design and methods > 医院优先的跨数据库外部验证 final paragraph"
    semantic_status: preserved
    evidence: "零参数更新、仅校准更新、仅观测模型更新的顺序与分开报告要求，以及全模型重拟合不属于外部验证的边界均保留。"
  - protected_id: PCR-021
    prior_locator: "Research content and work packages > 阶段 II 成功必须同时满足"
    revised_locator: "Research content and work packages > 阶段 II 成功必须同时满足"
    semantic_status: preserved
    evidence: "v007 将‘合取’改为‘全部必要标准’，但五组同时满足条件、所有数值阈值及适配改进和阶段 III 不得补足失败的规则不变。"
  - protected_id: PCR-022
    prior_locator: "Research design and methods > 条件性试验观测桥接与独立替代端点"
    revised_locator: "Research design and methods > 条件性试验观测桥接与独立替代端点"
    semantic_status: preserved
    evidence: "每项试验分开核验、至少两个同义同单位实测锚点、阶段 II 标准化与奇异值分解、禁用分组/结局/跨试验数据及不得重估权重均保留。"
  - protected_id: PCR-023
    prior_locator: "Research design and methods > 观测桥接合格阈值 paragraphs"
    revised_locator: "Research design and methods > 观测桥接合格阈值 paragraphs"
    semantic_status: preserved
    evidence: "能量、相关、归一化误差、截距、斜率、覆盖、锚点校准、合理范围与可计算比例的全部阈值及任一失败即停用摘要分支的规则均未变。"
  - protected_id: PCR-024
    prior_locator: "Research design and methods > trial table and following paragraph"
    revised_locator: "Research design and methods > trial table and following paragraph"
    semantic_status: preserved
    evidence: "两试验分开、分析集、中心、死亡/出院层级、插补、δ、临界点、界限分析、Holm、亚组交互及不插值、不合并效应均保留。"
  - protected_id: PCR-025
    prior_locator: "Structured abstract > Expected result; Data, materials, and existing evidence base > results row"
    revised_locator: "Structured abstract > Expected result; Data, materials, and existing evidence base > results row"
    semantic_status: preserved
    evidence: "v007 继续将模型、恢复、外部验证和试验分析表述为计划产物，并明确并非现有模型或验证结果。"
  - protected_id: PCR-026
    prior_locator: "Title, summary, audience, and positioning; Contribution, innovation, impact, application, and closest-work comparison"
    revised_locator: "Title, summary, audience, and positioning; Contribution, innovation, impact, application, and closest-work comparison"
    semantic_status: preserved
    evidence: "贡献仍限于条件性证据整合、计划外部验证、基准、研究资源和未达标记录；模块已有先例且不主张新算法或全球首次。"
  - protected_id: PCR-027
    prior_locator: "Expected outputs, falsification criteria, and interpretations > observation-pattern table"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > observation-pattern table"
    semantic_status: preserved
    evidence: "各失败或部分成功模式的允许解释和禁止解释均未增强；阶段 II 成功仍最多支持审计、恢复、任务表现与独立外部证据。"
  - protected_id: PCR-028
    prior_locator: "Title and positioning claim-support table"
    revised_locator: "Title and positioning claim-support table"
    semantic_status: preserved
    evidence: "标题三部分仍受计划、候选、条件性、次要和分试验范围约束，科学首创、方法首创、应用与转化主张仍明确不受支持。"
  - protected_id: PCR-029
    prior_locator: "Feasibility > 工作假设与尚待冻结的规范 row 1"
    revised_locator: "Feasibility > 工作假设与尚待确定的规范 row 1"
    semantic_status: preserved
    evidence: "未解决的数据支持项目、月 6 时点、允许信息、硬下限和降维/改时制/备份/停止后果均保留；G1 仅被自然语言化为月 6 审计。"
  - protected_id: PCR-030
    prior_locator: "Feasibility > 工作假设与尚待冻结的规范 row 2"
    revised_locator: "Feasibility > 工作假设与尚待确定的规范 row 2"
    semantic_status: preserved
    evidence: "模拟参数映射仍待确定，生成场景、绝对恢复量、月 6 前允许证据及未解决则不启动复杂候选模型均未改变。"
  - protected_id: PCR-031
    prior_locator: "Feasibility > 工作假设与尚待冻结的规范 row 3"
    revised_locator: "Feasibility > 工作假设与尚待确定的规范 row 3"
    semantic_status: preserved
    evidence: "校准估计与阈值表仍待完成，+0.01、0.80–1.20、≤0.02、只能收紧及未解决不得访问最终测试结果均保留。"
  - protected_id: PCR-032
    prior_locator: "Feasibility > 工作假设与尚待冻结的规范 row 4"
    revised_locator: "Feasibility > 工作假设与尚待确定的规范 row 4"
    semantic_status: preserved
    evidence: "12 小时主方案、24 小时和事件时间替代顺序、月 6 前且拟合和测试访问前的决定条件，以及不足时停止端点均保留。"
  - protected_id: PCR-033
    prior_locator: "Feasibility > 工作假设与尚待冻结的规范 row 5"
    revised_locator: "Feasibility > 工作假设与尚待确定的规范 row 5"
    semantic_status: preserved
    evidence: "K≤4、体制≤3、1 或 2 格滞后、每维至少两个锚点及月 6 前的决定依据与降维替代均未改变。"
  - protected_id: PCR-034
    prior_locator: "Feasibility > 工作假设与尚待冻结的规范 row 6"
    revised_locator: "Feasibility > 工作假设与尚待确定的规范 row 6"
    semantic_status: preserved
    evidence: "所有结果仍明确尚未生成，只能按预先规定顺序、阈值和分支产生，逾期仍表示相应端点未完成。"
  - protected_id: PCR-035
    prior_locator: "Feasibility > 工作假设与尚待冻结的规范 row 7"
    revised_locator: "Feasibility > 工作假设与尚待确定的规范 row 7"
    semantic_status: preserved
    evidence: "试验授权和核心语义仍未核验；分试验、目标访视、层级、分析集规则、24 个月后核验及语义不合格停止条件均保留。"
  - protected_id: PCR-036
    prior_locator: "Feasibility > 工作假设与尚待冻结的规范 row 8"
    revised_locator: "Feasibility > 工作假设与尚待确定的规范 row 8"
    semantic_status: preserved
    evidence: "每项试验至少两个实测锚点、预先确定映射、全部忠实度阈值、允许证据以及不合格或需重估权重时采用独立 SOFA 的规则未变。"
  - protected_id: PCR-037
    prior_locator: "Feasibility > 工作假设与尚待冻结的规范 row 9"
    revised_locator: "Feasibility > 工作假设与尚待确定的规范 row 9"
    semantic_status: preserved
    evidence: "模块非新颖高置信、完整组合缺口低至中等置信、禁止全球首次及更强主张所需扩展检索均完整保留。"
  - protected_id: PCR-038
    prior_locator: "Feasibility > 限制与边界条件 paragraph 1"
    revised_locator: "Feasibility > 限制与边界条件 paragraph 1"
    semantic_status: preserved
    evidence: "数据库权限、协议、提取和人员承诺均未被提升为已具备；待审计支持、接口缺失与不得用向前填充替代实测密度的限制均保留在权威限制段。"
  - protected_id: PCR-039
    prior_locator: "Feasibility > 限制与边界条件 paragraph 1"
    revised_locator: "Feasibility > 限制与边界条件 paragraph 1"
    semantic_status: preserved
    evidence: "发病时刻非唯一、标签构造敏感性及后录入、同格未来行动、未来测量频率和跨拆分处理的泄漏风险均保留。"
  - protected_id: PCR-040
    prior_locator: "Feasibility > 限制与边界条件 paragraph 2"
    revised_locator: "Feasibility > 限制与边界条件 paragraph 2"
    semantic_status: preserved
    evidence: "模拟恢复不证明真实机制、非随机缺失与反馈限制、不能识别未测真值或治疗作用，以及预测诊断不能替代结构与主要任务证据均保留。"
  - protected_id: PCR-041
    prior_locator: "Feasibility > 限制与边界条件 paragraph 2"
    revised_locator: "Feasibility > 限制与边界条件 paragraph 2"
    semantic_status: preserved
    evidence: "跨数据库差异风险、适配后更新不能替代零更新验证及全模型重拟合仅属更新或开发的限制均未改变。"
  - protected_id: PCR-042
    prior_locator: "Feasibility > 限制与边界条件 paragraph 3"
    revised_locator: "Feasibility > 限制与边界条件 paragraph 3"
    semantic_status: preserved
    evidence: "两试验不合并、稀疏访视不插值、XBJ-SCAP 人群不等于确认 Sepsis-3 及结构性缺失不得填补均保留。"
  - protected_id: PCR-043
    prior_locator: "Feasibility > 风险、替代方案与停止条件 row 1"
    revised_locator: "Feasibility > 风险、替代方案与停止条件 row 1"
    semantic_status: preserved
    evidence: "月 3/月 6 触发条件、备份/时间方案/删模块替代及无两个数据库支持时停止跨数据库端点均未变。"
  - protected_id: PCR-044
    prior_locator: "Feasibility > 风险、替代方案与停止条件 row 2"
    revised_locator: "Feasibility > 风险、替代方案与停止条件 row 2"
    semantic_status: preserved
    evidence: "跨分区患者全排除、20 家医院、10 个事件或转移、70%/80% 覆盖和 10% 排除阈值，以及备份失败后仅描述数据库层面均保留。"
  - protected_id: PCR-045
    prior_locator: "Feasibility > 风险、替代方案与停止条件 row 3"
    revised_locator: "Feasibility > 风险、替代方案与停止条件 row 3"
    semantic_status: preserved
    evidence: "v007 将 as-of 查询改为按当时可用信息执行的查询，仍要求修正查询、删除变量、保留可执行标签，并以未清除高严重度泄漏阻止测试访问。"
  - protected_id: PCR-046
    prior_locator: "Feasibility > 风险、替代方案与停止条件 row 4"
    revised_locator: "Feasibility > 风险、替代方案与停止条件 row 4"
    semantic_status: preserved
    evidence: "任一恢复或结构检验不合格即采用简单模型并淘汰复杂候选，且不得以预测表现重新纳入的规则未改变。"
  - protected_id: PCR-047
    prior_locator: "Feasibility > 风险、替代方案与停止条件 row 5"
    revised_locator: "Feasibility > 风险、替代方案与停止条件 row 5"
    semantic_status: preserved
    evidence: "非随机缺失敏感性或行动重叠不足时的敏感区间、合并/删除、政策限定及禁止解释未测值或治疗关系均保留。"
  - protected_id: PCR-048
    prior_locator: "Feasibility > 风险、替代方案与停止条件 row 6"
    revised_locator: "Feasibility > 风险、替代方案与停止条件 row 6"
    semantic_status: preserved
    evidence: "适当评分规则、校准、对齐或符号失败后的三类更新仍须分开报告，更新成功仍不能称零更新候选跨数据库成功。"
  - protected_id: PCR-049
    prior_locator: "Feasibility > 风险、替代方案与停止条件 row 7"
    revised_locator: "Feasibility > 风险、替代方案与停止条件 row 7"
    semantic_status: preserved
    evidence: "少于两个锚点、单位或时序不一致或忠实度阈值失败时仍只能采用独立死亡优先 SOFA，且不得称为阶段 II 表征扰动或验证。"
  - protected_id: PCR-050
    prior_locator: "Feasibility > 风险、替代方案与停止条件 row 8"
    revised_locator: "Feasibility > 风险、替代方案与停止条件 row 8"
    semantic_status: preserved
    evidence: "核心试验语义不能核验时仍只允许原终点复现或数据审计，并停止新状态端点和禁止制造轨迹或字段。"
  - protected_id: PCR-051
    prior_locator: "Feasibility > 风险、替代方案与停止条件 row 9 and final paragraph"
    revised_locator: "Feasibility > 风险、替代方案与停止条件 row 9 and final paragraph"
    semantic_status: preserved
    evidence: "月 12、月 20、月 24 三项未完成判定、24 个月内完成并保存阶段 II 定稿结果，以及阶段 III 不得补救或绕过阶段 II 的规则均保留。"
  - protected_id: PCR-052
    prior_locator: "Feasibility > 风险、替代方案与停止条件 row 10"
    revised_locator: "Feasibility > 风险、替代方案与停止条件 row 10"
    semantic_status: preserved
    evidence: "提出首次、专利或全球不存在主张前仍须补做系统、引文、专利和非英语检索，当前定位仍保持有界和条件性。"
  - protected_id: PCR-053
    prior_locator: "Research question > 核心假设; Feasibility > 限制与边界条件 paragraph 4"
    revised_locator: "Research question > 核心假设; Feasibility > 限制与边界条件 paragraph 4"
    semantic_status: preserved
    evidence: "观察性数据、预测与联合建模不支持因果网络、治疗因果效应、反事实策略、机制、中介、控制或未测真值的边界完整保留。"
  - protected_id: PCR-054
    prior_locator: "Structured abstract > Contribution and impact; interpretation table; Feasibility > limitations paragraphs 3-4"
    revised_locator: "Structured abstract > Contribution and impact; interpretation table; Feasibility > limitations paragraphs 3-4"
    semantic_status: preserved
    evidence: "试验次要分析仍最多支持实际访视有限差异，不支持潜在动力学、转移边、中介、控制、额外结构或整个候选表征得到验证。"
  - protected_id: PCR-055
    prior_locator: "Title and positioning claim-support table; Feasibility > limitations paragraph 4"
    revised_locator: "Title and positioning claim-support table; Feasibility > limitations paragraph 4"
    semantic_status: preserved
    evidence: "已验证模型、临床工具、因果网络、可控系统、数字孪生、药物平台、无条件推广和全球首创均继续明确不受支持。"
  - protected_id: PCR-056
    prior_locator: "Feasibility > 限制与边界条件 paragraph 4"
    revised_locator: "Feasibility > 限制与边界条件 paragraph 4"
    semantic_status: preserved
    evidence: "有界检索不能支持全球首次或不存在相近工作，以及 SSC 2026 对未获当地监管批准辖区使用 XueBiJing 的谨慎建议均原义保留。"
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

`idea-dossier-v007` 保留了受保护登记表中全部 56 项科学内容的含义、证据状态、主张强度、条件性和停止边界。修订把若干工作术语替换为面向研究者的自然语言，定义了首次出现的专业术语，明确了每项试验的指标集合和预先确定时点，并拆分或合并部分句子；这些变化没有改变研究身份、数据来源、推断单位、任务、估计对象、阈值、验证顺序、试验分支、可行性判断或不支持的主张类别。修订说明未声明科学变化，逐项比较也未发现未声明的科学变化。

## Protected-content trace

主要位置保持稳定。研究身份与核心问题仍见 YAML 身份字段和研究问题部分；设计、分析与验证承诺仍见研究内容和研究设计部分；未解决规范、限制、风险、替代方案与停止条件仍集中在第 14 节的权威位置。非实质性改写包括把 `landmark`、`proper scoring rule`、`bootstrap`、`pattern-mixture delta` 和 `selection tipping-point` 在首次出现处定义为标准科学术语，把 `G1` 和其他内部工作用语改为相应的月 6 审计或预先确定动作，并把“共同生理指标”明确为每项试验在目标访视实际测得且与阶段 II 生理锚点同义同单位的指标。所有数值、条件和失败后果均可在修订稿中追踪。

## Required routing

判定为 `scientific_content_preserved`。该 dossier 可进入全新的叙事与学术语言评估，无须返回科学审查。
