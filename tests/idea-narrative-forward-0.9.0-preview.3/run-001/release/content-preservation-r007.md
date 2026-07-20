---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r007
review_id: content-preservation-review-I01-001-r007
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-r007
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r007
input_artifact_ids:
  - idea-dossier-I01-001-v009
  - idea-dossier-I01-001-v010
  - protected-content-register-I01-001-v009
  - revision-delta-I01-001-v009-to-v010
input_versions:
  - v009
  - v010
  - v009
  - v009-to-v010
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v009
    version: v009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v010
    version: v010
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v010.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v009
    version: v009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v009.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v009-to-v010
    version: v009-to-v010
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v009-to-v010.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v010.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v009.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v009-to-v010.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "v009 frontmatter > identity_anchor; Research question, objectives, and core hypothesis"
    revised_locator: "v010 L26-L33; L87-L106"
    semantic_status: preserved
    evidence: >-
      主要问题、24 个月目标、纵向脓毒症 ICU 对象、文献与公共 ICU 数据及条件性试验输入、患者—时间状态与转移推断单位均未改变；v010 L490 继续给出同一身份边界。
  - protected_id: PCR-002
    prior_locator: "v009 L83-L85, Primary research question"
    revised_locator: "v010 L89-L95, Primary research question"
    semantic_status: preserved
    evidence: >-
      原来的三个相继问题仅改排为三个编号项；全病程模型、跨数据库状态与结构检验以及阶段 II 成功后的稀疏访视随机分组比较保持原顺序、条件性与含义。
  - protected_id: PCR-003
    prior_locator: "v009 L87-L96, Objectives and Core hypothesis"
    revised_locator: "v010 L97-L106, Objectives and Core hypothesis"
    semantic_status: preserved
    evidence: >-
      四项目标及“至多一个受限复杂候选”的核心假设未改；共同指标、事件支持、尺度、状态数、滞后、锚定、两项主要任务、状态对齐与结构稳定性条件均保留。
  - protected_id: PCR-004
    prior_locator: "v009 frontmatter > identity_anchor; L173-L203, protocol locks and post-onset states"
    revised_locator: "v010 L26-L33; L183-L213"
    semantic_status: preserved
    evidence: >-
      成人纵向 ICU 系统、发病前动态风险集、观察起点已发病者排除、首次新发与延迟进入分层及左截断处理、患者—时间状态和转移推断单位均保持不变。
  - protected_id: PCR-005
    prior_locator: "v009 L38-L47, Three-stage map; L100-L127, milestones and work packages"
    revised_locator: "v010 L49-L53, 三阶段导航; L110-L137, milestones and work packages"
    semantic_status: preserved
    evidence: >-
      三阶段导航被移动并压缩，但月 0–6、月 3–24、月 3–6 交叠、阶段 I–II 最低交付、阶段 III 的阶段 II 成功与资格前提以及不能改变阶段 II 成败均在权威进度与工作包中完整保留。
  - protected_id: PCR-006
    prior_locator: "v009 L445-L447, Resources and governance"
    revised_locator: "v010 L460-L462, Resources and governance"
    semantic_status: preserved
    evidence: >-
      两个主要数据库、最多 4 个状态维度、最多 3 个切换机制、至多一个复杂候选、两项主要任务和两项次要诊断的上限逐字保留；排除的动物、随机试验、因果机制与控制策略范围不变。
  - protected_id: PCR-007
    prior_locator: "v009 L244-L285, Conditional trial observation mapping and secondary analyses"
    revised_locator: "v010 L254-L295, Conditional trial observation mapping and secondary analyses"
    semantic_status: preserved
    evidence: >-
      两项试验继续分开、采用实际第 7 日和第 8 日访视、只作次要或探索性分析、稀疏访视不插值为连续轨迹，并将独立 SOFA 分析与阶段 II 映射分离。
  - protected_id: PCR-008
    prior_locator: "v009 L131-L163, Public ICU databases and planned roles"
    revised_locator: "v010 L141-L173, Public ICU databases and planned roles"
    semantic_status: preserved
    evidence: >-
      MIMIC-IV v3.1、eICU-CRD v2.0、启动期预先指定的 HiRID 或 AmsterdamUMCdb 备份角色及共同概念层限制未改变；数据库特异变量仍只用于探索性观测模型。
  - protected_id: PCR-009
    prior_locator: "v009 L165-L169, Trial data considered for conditional stage III analyses"
    revised_locator: "v010 L175-L179, Trial data considered for conditional stage III analyses"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 的随机分配数、分析集数、28 日状态数及各访视非缺失数均相同；671 人标签只改为中文并在同处保留“全分析集且基线 SOFA 至少 2 分”的原操作定义，未生成新结果。
  - protected_id: PCR-010
    prior_locator: "v009 L421-L433, Current feasibility and evidence status"
    revised_locator: "v010 L436-L448, Current feasibility and evidence status"
    semantic_status: preserved
    evidence: >-
      数据库存在与版本核验、访问与项目审计未核验、人员未具名、模型与全部新结果尚未生成，以及尺度映射、校准估计量、区间构造和阈值尚未冻结的状态均保留。
  - protected_id: PCR-011
    prior_locator: "v009 L421-L447, Current feasibility and evidence status; Resources and governance"
    revised_locator: "v010 L436-L462, Current feasibility and evidence status; Resources and governance"
    semantic_status: preserved
    evidence: >-
      本地衍生材料不能替代个体数据授权、原始试验文件与语义核验的边界，以及六类具名专业与独立数据保管人员的最低配置均未改变。
  - protected_id: PCR-012
    prior_locator: "v009 L173-L190, Protocol locks; sensitivity definitions"
    revised_locator: "v010 L183-L200, Protocol locks; sensitivity definitions"
    semantic_status: preserved
    evidence: >-
      感染配对 72/24 小时规则、SOFA 基线、滚动窗、发病窗、首次满足时点、信息可用时间和两种敏感性定义均逐项保留。
  - protected_id: PCR-013
    prior_locator: "v009 L173-L190, primary pre-onset task column"
    revised_locator: "v010 L183-L200, primary pre-onset task column"
    semantic_status: preserved
    evidence: >-
      ICU 第 12 小时起每 12 小时预测、此前 12–24 小时信息、未来 12 小时 CIF、竞争终止与 IPCW、原因别风险模型、Brier 与校准指标、总权重为 1 及患者和医院聚类均未改变。
  - protected_id: PCR-014
    prior_locator: "v009 L173-L203, primary post-onset task and mutually exclusive states"
    revised_locator: "v010 L183-L213, primary post-onset task and mutually exclusive states"
    semantic_status: preserved
    evidence: >-
      每 12 小时更新、第 7 日主要终点、第 14 日敏感性、有利集合与分开报告、离散多状态和 Aalen–Johansen、状态优先级及恢复和恶化定义均保持原义。
  - protected_id: PCR-015
    prior_locator: "v009 L155-L163, Variable-role separation; L190, leakage audit"
    revised_locator: "v010 L165-L173, Variable-role separation; L200, leakage audit"
    semantic_status: preserved
    evidence: >-
      生理测量、治疗行动、测量过程、标签变量和基线协变量继续分离；治疗和测量频率不作锚点、未检测与接口缺失不作生理状态、标签副本隔离及全部泄漏审计项目均保留。
  - protected_id: PCR-016
    prior_locator: "v009 L205-L223, Observational model target, anchoring, and reporting"
    revised_locator: "v010 L215-L231, Observational model target, anchoring, and reporting"
    semantic_status: preserved
    evidence: >-
      联合分布目标、导出对象、每维至少两个共同锚点、首锚点载荷 +1、交叉载荷约束、无同窗瞬时循环、1 或 2 个冻结滞后窗及 20 个种子对齐报告均未改变。
  - protected_id: PCR-017
    prior_locator: "v009 L223, missingness and treatment paragraph"
    revised_locator: "v010 L233, missingness and treatment paragraph"
    semantic_status: preserved
    evidence: >-
      缺失随机与选择模型两类并列基线、测量过程显式表示、五个模式混合偏移、选择模型临界点，以及状态、医院、时间层治疗概率与有效样本量报告均保留。
  - protected_id: PCR-018
    prior_locator: "v009 L225-L229, Simulation and semi-synthetic recovery study"
    revised_locator: "v010 L235-L239, Simulation and semi-synthetic recovery study"
    semantic_status: preserved
    evidence: >-
      月 7–10、最终外部结果隔离、全部预设数据生成机制、交叉变化因素和状态恢复、转移、结构、错设与校准评价量均保持不变。
  - protected_id: PCR-019
    prior_locator: "v009 L449-L462, operational threshold rows"
    revised_locator: "v010 L464-L476, operational threshold rows"
    semantic_status: preserved
    evidence: >-
      事件与转移支持、锚点覆盖、1,000 次或 MCSE 0.02、ARI/典型相关、种子匹配、转移误差与覆盖、结构恢复、错误发现率、错设识别、校准及跨数据库对齐的全部数值门槛未改变。
  - protected_id: PCR-020
    prior_locator: "v009 L462-L463, nonrandom missingness/treatment overlap and two-primary-task rows"
    revised_locator: "v010 L434; L477-L478"
    semantic_status: changed
    evidence: >-
      缺失与治疗重叠部分、+0.01 数值、校准门槛和禁止替代均保留；但 v009 的“上侧 95% 界”被 v010 确定为“双侧 95% 置信区间上限”，且新增若原预设为单侧界则改变区间构造的分支。双侧或单侧置信界是统计推断规范，不是仅有措辞差异；delta 将其记为工作假设和有限措辞校正，未声明科学变更。
  - protected_id: PCR-021
    prior_locator: "v009 L231-L242, Hospital-based cross-database validation"
    revised_locator: "v010 L241-L250; L433"
    semantic_status: changed
    evidence: >-
      30%/70% 医院比例、固定种子、按医院标识符可复现分组、结局前冻结、跨分区患者排除及敏感性分析均保留；但 v009 的“合格体量四分位”被 v010 确定为“每院合格患者数四分位”，并新增若原指标不同则更换分层变量和重做分组的分支。选择医院分层变量会改变分层随机分配，属于验证设计规范；delta 将其记为工作假设和措辞校正，未声明科学变更。
  - protected_id: PCR-022
    prior_locator: "v009 L242, three external analyses"
    revised_locator: "v010 L252, three external analyses"
    semantic_status: preserved
    evidence: >-
      冻结对象及不更新模型、仅用适配数据再校准、仅更新观测层的固定顺序未改变；全模型重新拟合仍另列为跨数据库模型更新研究。
  - protected_id: PCR-023
    prior_locator: "v009 L464-L466, external support, results, and timing rows"
    revised_locator: "v010 L479-L481, external support, results, and timing rows"
    semantic_status: preserved
    evidence: >-
      20 家医院、每参数 10 个事件或转移、70% 医院与 80% 患者锚点覆盖、10% 跨分区排除、Brier 非劣、0.70 对齐、0.80 符号一致及月 12/20/24 后果均未改变。
  - protected_id: PCR-024
    prior_locator: "v009 L248-L252, Trial semantics and common-observation eligibility"
    revised_locator: "v010 L258-L262, Trial semantics and common-observation eligibility"
    semantic_status: preserved
    evidence: >-
      阶段 II 完成冻结、授权与原始文件、随机与访视语义核验、直接实测共同生理锚点、构念/标本/单位/时间一致、禁止变量、每试验至少两个锚点和不得重估试验权重均保留。
  - protected_id: PCR-025
    prior_locator: "v009 L254-L268, Pre-specified deterministic observation mapping"
    revised_locator: "v010 L264-L278, Pre-specified deterministic observation mapping"
    semantic_status: preserved
    evidence: >-
      开发库冻结标准化与截断、奇异值分解、P_state 与 P_obs 定义、并列奇异值选轴、与同日 SOFA 非负相关定向、不使用治疗或结局及不合并试验均未改变。
  - protected_id: PCR-026
    prior_locator: "v009 L467, Observation-mapping external fidelity row"
    revised_locator: "v010 L484, Observation-mapping external fidelity row"
    semantic_status: preserved
    evidence: >-
      50%、0.70、0.50、0.20、0.80–1.20、0.90–0.98、80% 生理范围和 60% 可计算访视等全部映射忠实度门槛及任一失败即停止摘要分支的后果均未改变。
  - protected_id: PCR-027
    prior_locator: "v009 L274-L285, Analysis targets and trial table"
    revised_locator: "v010 L284-L295, Analysis targets and trial table"
    semantic_status: preserved
    evidence: >-
      死亡/住院/出院层级、P_obs 与 SOFA 排序、概率指数、1,817 与 710 人目标总体、675 人降级、多重插补与敏感性、Holm 0.05 家族和亚组交互限制均保留。
  - protected_id: PCR-028
    prior_locator: "v009 L113-L115, Minimum success definition; L368-L370, Scientific falsification criteria"
    revised_locator: "v010 L123-L125; L378-L380"
    semantic_status: preserved
    evidence: >-
      阶段 II 五类必要证据仍须全部满足，任一失败即不成功；正确指定恢复、无边/错设、两项主要任务、外部任务/对齐/结构稳定性和结果后重选的证伪条件均未改变。
  - protected_id: PCR-029
    prior_locator: "v009 L37-L47, positioning; L378-L388, Contribution and evidence ladder"
    revised_locator: "v010 L38-L53; L388-L398"
    semantic_status: preserved
    evidence: >-
      贡献仍限于组织可审计的证据路线、验证、基准与资源；组成方法已有先例，增量仍是有界整合与验证而非方法首次出现。
  - protected_id: PCR-030
    prior_locator: "v009 L49-L55, Structured abstract; L358-L366, Planned outputs"
    revised_locator: "v010 L55-L61; L368-L376"
    semantic_status: preserved
    evidence: >-
      模型、模拟、任务、外部验证、映射与试验组间差异继续全部表述为计划或拟生成结果；没有把计划工作改写成已完成证据。
  - protected_id: PCR-031
    prior_locator: "v009 L390-L413, closest-work comparison and claim-support table"
    revised_locator: "v010 L400-L423, closest-work comparison and claim-support table"
    semantic_status: preserved
    evidence: >-
      有界检索日期、模块先例的高置信、完整组合缺口的低至中等置信、获得支持与限定表述的区分，以及执行和更广检索前不得主张实际组合增量均未改变。
  - protected_id: PCR-032
    prior_locator: "v009 L372-L374, Interpretation; L435-L443, Scientific and interpretive boundaries"
    revised_locator: "v010 L382-L384; L450-L458"
    semantic_status: preserved
    evidence: >-
      任务预测、模拟恢复、跨数据库稳定性和试验差异继续分开；有限更新不能替代冻结模型失败；一维摘要和独立 SOFA 结论范围均保持原强度。
  - protected_id: PCR-033
    prior_locator: "v009 L94-L96, Core hypothesis; L421-L433, Current feasibility"
    revised_locator: "v010 L104-L106; L436-L448; L470"
    semantic_status: preserved
    evidence: >-
      共同指标和事件支持、尺度/状态数/滞后/锚定预固定、双数据库审计约束复杂度、月 6 前不接触外部结果的登记、既有阈值只可收紧及阶段 III 资格依赖均保留。PCR-020 和 PCR-021 的新增方法假设另行标为 changed，不据此把本项门槛登记原则重复计为改变。
  - protected_id: PCR-034
    prior_locator: "v009 L435-L443, Scientific and interpretive boundaries"
    revised_locator: "v010 L450-L458, Scientific and interpretive boundaries"
    semantic_status: preserved
    evidence: >-
      权威限制七项完整保留：因果与机制限制、主要外部依据、试验结论范围、无条件推广限制、禁用创新与应用主张、XBJ-SCAP 人群和字段边界、阶段 III 不补足阶段 II 失败。
  - protected_id: PCR-035
    prior_locator: "v009 L449-L466, stage II alternatives and stop-condition rows"
    revised_locator: "v010 L464-L481, stage II alternatives and stop-condition rows"
    semantic_status: preserved
    evidence: >-
      数据与人员、备份库、12/24 小时或事件时间、支持不足降级、泄漏停止、恢复/错设/任务失败后果、外部支持降级和月 24 封存逻辑均未改变。
  - protected_id: PCR-036
    prior_locator: "v009 L468-L471, trial alternatives and stop-condition rows"
    revised_locator: "v010 L482-L485, trial alternatives and stop-condition rows"
    semantic_status: preserved
    evidence: >-
      试验语义失败停止、XBJ-SCAP 675 人降级、共同变量和 SOFA 备选、映射失败禁止恢复、如实报告不一致或敏感结果、不得选择亚组或合并共同效应的逻辑均保留。
  - protected_id: PCR-037
    prior_locator: "v009 L435-L438, Scientific and interpretive boundaries items 1-4"
    revised_locator: "v010 L450-L455, Scientific and interpretive boundaries items 1-4"
    semantic_status: preserved
    evidence: >-
      观察性关联、预测、状态表示和测量过程不支持治疗因果、真实反馈、反事实、中介或个体控制结论，阴性对照与时间反转也不证明模型正确；边界未减弱。
  - protected_id: PCR-038
    prior_locator: "v009 L439, boundary item 5; L471, closest-work row"
    revised_locator: "v010 L456, boundary item 5; L486, closest-work row"
    semantic_status: preserved
    evidence: >-
      全球首次、全球不存在、专利空白、新算法、数字孪生、控制、临床决策、药物平台或临床应用主张的额外证据前提与当前条件性整合验证定位均未改变。
  - protected_id: PCR-039
    prior_locator: "v009 L437-L443, boundary items 3, 4, 6, and 7"
    revised_locator: "v010 L454-L458, boundary items 3, 4, 6, and 7; L482-L485"
    semantic_status: preserved
    evidence: >-
      试验不支持未测潜在动力学、状态转移边、完整系统、机制、共同治疗效应或无条件推广；XBJ-SCAP 不等同确认 Sepsis-3、字段不得构造、阶段 III 不补足阶段 II 失败的边界均保留。
undeclared_scientific_changes:
  - change_id: USC-001
    protected_ids: [PCR-020]
    prior_locator: "v009 L463"
    revised_locator: "v010 L434 and L478"
    change: >-
      将未定的“上侧 95% 界”具体化为“双侧 95% 置信区间上限”，并允许核验后改用单侧 95% 置信上界。该选择改变非劣性判据的区间构造和统计推断规范。
    delta_disclosure: >-
      delta 披露其为“明确工作假设”及可能的有限措辞校正，但同时明确否认方法或科学内容变化，未将其声明为科学变更。
  - change_id: USC-002
    protected_ids: [PCR-021]
    prior_locator: "v009 L233"
    revised_locator: "v010 L243 and L433"
    change: >-
      将未定的“合格体量四分位”具体化为“每院合格患者数四分位”，并允许核验后更换分层变量和重新生成医院分组。该选择改变医院分层随机分配的设计输入。
    delta_disclosure: >-
      delta 披露其为“明确工作假设”及可能的有限措辞校正，但同时明确否认设计或科学内容变化，未将其声明为科学变更。
findings:
  - finding_id: CPR-007-F001
    protected_ids: [PCR-020]
    severity: blocking
    finding: >-
      置信界类型从未定表述变为双侧区间上限，并附带可改为单侧界的后续分支；这超出 register 允许的定义或术语替换，触及受保护的分析承诺。
  - finding_id: CPR-007-F002
    protected_ids: [PCR-021]
    severity: blocking
    finding: >-
      医院体量分层指标从未定表述变为每院合格患者数，并附带可更换分层变量和重分组的后续分支；这超出纯编辑范围，触及受保护的外部验证设计。
unresolved_issues:
  - >-
    在科学审查或既有权威方案确认前，无法从四个获准输入确定医院体量的预设定义究竟为何，也无法确定主要任务应使用双侧 95% 置信区间上限还是单侧 95% 置信上界。
---

# Content-preservation check

## Decision rationale

`editorial_scope_violation`。v010 保留了研究的主要问题、对象、范围、目的、推断单位、数据角色、主要任务、试验条件性和解释边界，因此没有研究身份漂移。revision delta 明确把本轮称为纯编辑修复并否认科学或方法变化，所以不满足 `scientific_change_declared` 的条件。

但是，v010 新增的两项“工作假设”不是已经确定含义的术语释义。医院分层量的选择会改变外部验证医院的分层随机分配；单侧或双侧 95% 置信界的选择会改变主要任务非劣性判据的统计推断规范。两者都承认需要以后核验，并在假设错误时更改方法，而 delta 把这种更改称为有限措辞校正。它们分别违反 frozen register 中“不改变设计、分析或验证承诺”的边界。除 PCR-020 与 PCR-021 外，其余 37 项均可在 v010 中按同一含义、强度、条件性和权威位置追溯。

## Protected-content trace

- 研究身份与主要科学路线：v009 的 frontmatter 与研究问题在 v010 L26–L33、L87–L106 保持同一身份；三阶段导航移至 v010 L49–L53，完整进度与最低成功标准仍在 L110–L137。
- 术语和组织层编辑：背景缺口在 v010 L57 拆分并定义“预设结构稳定性”；主要问题在 L91–L95 改为三个平行编号项；XBJ-SCAP 的 671 人人群在 L179 和 L293 以中文复述同一操作定义。这些变化没有改变受保护含义。
- 未声明的分析规范变化：v010 L434、L478 新增并实施双侧 95% 置信区间上限，同时允许以后改成单侧界，影响 PCR-020。
- 未声明的验证设计变化：v010 L243、L433 新增并实施“每院合格患者数”分层量，同时允许以后更换分层变量并重分组，影响 PCR-021。

## Required routing

v010 当前不得进入新的 narrative 与 language assessment。按 preservation contract，应返回编辑修复：要么恢复为不新增方法含义的 v009 表述并删除两个方法性工作假设，要么由权威科学方案明确选择医院分层量和置信界构造，在 revision delta 中声明科学变更，再返回适用的科学审查。完成实质性修改后必须由新的独立 preservation reviewer 重新核验。
