---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r008
review_id: content-preservation-review-I01-001-r008
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-scientific-content-preservation-reviewer-r008
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r008
input_artifact_ids:
  - idea-dossier-I01-001-v009
  - idea-dossier-I01-001-v011
  - protected-content-register-I01-001-v009
  - revision-delta-I01-001-v009-to-v011
input_versions:
  - v009
  - v011
  - v009
  - v009-to-v011
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v009
    version: v009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v011
    version: v011
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v011.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v009
    version: v009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v009.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v009-to-v011
    version: v009-to-v011
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v009-to-v011.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v011.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v009.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v009-to-v011.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "Frontmatter > identity_anchor"
    revised_locator: "Frontmatter > identity_anchor"
    semantic_status: preserved
    evidence: "五项身份锚点逐项相同；仅 artifact/version/path、血缘和轮次元数据更新。"
  - protected_id: PCR-002
    prior_locator: "Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "Research question, objectives, and core hypothesis > Primary research question > numbered questions 1–3"
    semantic_status: preserved
    evidence: "原连续三问拆成依赖顺序明确的三项；构建对象、跨数据库检验对象、聚类处理及阶段 II 成功后才开展试验摘要比较均未改变。"
  - protected_id: PCR-003
    prior_locator: "Research question, objectives, and core hypothesis > Objectives and Core hypothesis"
    revised_locator: "Research question, objectives, and core hypothesis > Objectives and Core hypothesis"
    semantic_status: preserved
    evidence: "四项目标、预设数据生成机制、两项主要任务、两项次要诊断、跨数据库稳定性及至多一个受限复杂候选的条件性假设均原样保留。"
  - protected_id: PCR-004
    prior_locator: "Frontmatter > identity_anchor; Research design and methods > Protocol locks"
    revised_locator: "Frontmatter > identity_anchor; Research design and methods > Protocol locks for the two primary clinical tasks"
    semantic_status: preserved
    evidence: "成人 ICU 纵向脓毒症中心对象、发病前动态风险集、发病后新发与左截断延迟进入分层，以及患者—时间状态和转移推断单位均未变。"
  - protected_id: PCR-005
    prior_locator: "Title, summary, audience, and positioning > Three-stage map; Research content and work packages"
    revised_locator: "Title, summary, audience, and positioning > 三阶段导航; Research content and work packages"
    semantic_status: preserved
    evidence: "三阶段说明被重排并拆成导航条目；阶段 I/II 月份、月 3–6 交叠、24 个月最低交付、阶段 III 条件及不得补足阶段 II 失败均保留。"
  - protected_id: PCR-006
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance"
    semantic_status: preserved
    evidence: "两个主要数据库、最多 4 个状态维度、最多 3 个切换机制、至多一个复杂候选、两项主要任务和两项次要诊断的范围，以及排除项目均相同。"
  - protected_id: PCR-007
    prior_locator: "Research design and methods > Conditional trial observation mapping and secondary analyses"
    revised_locator: "Research design and methods > Conditional trial observation mapping and secondary analyses > opening paragraph, Analysis targets, and trial table"
    semantic_status: preserved
    evidence: "次要或探索性性质、两试验分开报告、实际第 7/8 日访视、不得把稀疏访视插值为连续轨迹，以及独立 SOFA 分支均未改变。"
  - protected_id: PCR-008
    prior_locator: "Data, materials, and existing evidence base > Public ICU databases and planned roles"
    revised_locator: "Data, materials, and existing evidence base > Public ICU databases and planned roles"
    semantic_status: preserved
    evidence: "MIMIC-IV、eICU-CRD、备份库和共同概念层的角色与限定均逐项相同。"
  - protected_id: PCR-009
    prior_locator: "Data, materials, and existing evidence base > Trial data considered for conditional stage III analyses"
    revised_locator: "Data, materials, and existing evidence base > Trial data considered for conditional stage III analyses"
    semantic_status: preserved
    evidence: "两项试验的随机人数、衍生样本数、死亡/状态及各访视非缺失计数均相同；XBJ-SCAP 671 人群仅将英文标签改为中文并显式保留原操作定义。"
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > 尚待冻结的方法规范 and Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "已核验、未核验和尚未生成项目全部保留；区间构造仍明确尚未冻结，且被收窄表述为主要任务 95% 上置信限构造，未被写成已选定方法。"
  - protected_id: PCR-011
    prior_locator: "Current feasibility and evidence status; Resources and governance"
    revised_locator: "Current feasibility and evidence status; Resources and governance"
    semantic_status: preserved
    evidence: "本地衍生试验材料的证据边界、所需原始文件与持有人核验、最低具名角色和独立数据保管职责均未变。"
  - protected_id: PCR-012
    prior_locator: "Research design and methods > Protocol locks > Event time, information availability time, prediction times, and sensitivity definitions"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > event/information rows and sensitivity paragraph"
    semantic_status: preserved
    evidence: "感染配对窗口、基线 SOFA、器官功能窗、发病时刻、信息可用时间及两种敏感性定义逐项一致。"
  - protected_id: PCR-013
    prior_locator: "Research design and methods > Protocol locks > Primary pre-onset task column"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > Primary pre-onset task column"
    semantic_status: preserved
    evidence: "12 小时动态预测、历史窗、首次发病 CIF、竞争终止/IPCW、模型、主要评价、重叠窗权重与聚类处理均未变。"
  - protected_id: PCR-014
    prior_locator: "Research design and methods > Protocol locks > Primary post-onset task; Mutually exclusive post-onset state and event system"
    revised_locator: "Research design and methods > Protocol locks; Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: "第 7 日主要终点、第 14 日敏感性、互斥多状态、Aalen–Johansen、状态优先级以及恢复和恶化定义均相同。"
  - protected_id: PCR-015
    prior_locator: "Data, materials, and existing evidence base > Variable-role separation; Protocol locks > leakage audit"
    revised_locator: "Data, materials, and existing evidence base > Variable-role separation; Protocol locks > leakage audit paragraph"
    semantic_status: preserved
    evidence: "生理、治疗、测量过程、标签和基线变量分离，以及全部泄漏审计对象均完整保留。"
  - protected_id: PCR-016
    prior_locator: "Research design and methods > Observational model target, anchoring, and reporting"
    revised_locator: "Research design and methods > Observational model target, anchoring, and reporting"
    semantic_status: preserved
    evidence: "联合分布目标、导出对象、锚定和尺度约束、交叉载荷、禁止同窗循环、冻结滞后及 20 个种子状态对齐均未变。"
  - protected_id: PCR-017
    prior_locator: "Research design and methods > Observational model target, anchoring, and reporting > missingness and treatment paragraph"
    revised_locator: "Research design and methods > Observational model target, anchoring, and reporting > missingness and treatment paragraph"
    semantic_status: preserved
    evidence: "缺失随机与选择模型并列基线、五个模式混合偏移、临界点分析及分层行动概率和有效样本量报告均相同。"
  - protected_id: PCR-018
    prior_locator: "Research design and methods > Simulation and semi-synthetic recovery study"
    revised_locator: "Research design and methods > Simulation and semi-synthetic recovery study"
    semantic_status: preserved
    evidence: "月 7–10、外部结果隔离、全部数据生成机制与交叉因素、全部恢复和错设评价量均未变。"
  - protected_id: PCR-019
    prior_locator: "Feasibility > Operational thresholds table > support, simulation, recovery, structure, calibration rows"
    revised_locator: "Feasibility > Operational thresholds, alternatives, and stop conditions > corresponding rows"
    semantic_status: preserved
    evidence: "事件/转移支持、锚点覆盖、模拟次数/MCSE、恢复、覆盖、结构错误率、校准、种子稳定性和跨库对齐的所有数值门槛均一致。"
  - protected_id: PCR-020
    prior_locator: "Feasibility > Operational thresholds table > Nonrandom missingness/treatment overlap and two primary tasks rows"
    revised_locator: "Feasibility > 尚待冻结的方法规范; Operational thresholds table > Nonrandom missingness/treatment overlap and two primary tasks rows"
    semantic_status: preserved
    evidence: "缺失和重叠门槛、+0.01 上侧 95% 界方向、校准标准及禁止替代规则均不变；v011 只明确具体上置信限构造仍待月 6 前、拟合和外部结果访问前冻结，没有选定区间算法或新增切换分支。"
  - protected_id: PCR-021
    prior_locator: "Research design and methods > Hospital-based cross-database validation > hospital split and cross-hospital patient rules"
    revised_locator: "Research design and methods > Hospital-based cross-database validation; Feasibility > 尚待冻结的方法规范"
    semantic_status: preserved
    evidence: "合格医院规模四分位和接口完整性分层、医院标识符、种子 20260717、30/70 分组、结果隔离、跨分区患者排除与敏感性分析均保留；v011 仅明确规模指标的具体计算定义尚待审计后和结果隔离下冻结，未自行指定新指标。"
  - protected_id: PCR-022
    prior_locator: "Research design and methods > Hospital-based cross-database validation > three external analyses"
    revised_locator: "Research design and methods > Hospital-based cross-database validation > closing paragraph"
    semantic_status: preserved
    evidence: "冻结内容、三种外部分析顺序、有限更新边界及全模型重拟合的另行研究标记均未改变。"
  - protected_id: PCR-023
    prior_locator: "Feasibility > Operational thresholds table > external support, external results, and freeze/time rows"
    revised_locator: "Feasibility > Operational thresholds, alternatives, and stop conditions > external support, external results, and freeze/time rows"
    semantic_status: preserved
    evidence: "外部医院/事件/锚点支持、10% 排除上限、备份库和降级、外部任务/对齐/符号标准及月 12/20/24 停止条件全部相同。"
  - protected_id: PCR-024
    prior_locator: "Research design and methods > Conditional trial observation mapping > Trial semantics and common-observation eligibility"
    revised_locator: "Research design and methods > Conditional trial observation mapping > Trial semantics and common-observation eligibility"
    semantic_status: preserved
    evidence: "阶段 II 冻结、授权和语义核验、共同变量资格、禁止变量、至少两个锚点及不得重估试验特异权重均未变。"
  - protected_id: PCR-025
    prior_locator: "Research design and methods > Conditional trial observation mapping > Pre-specified deterministic observation mapping"
    revised_locator: "Research design and methods > Conditional trial observation mapping > Pre-specified deterministic observation mapping"
    semantic_status: preserved
    evidence: "分试验变量集、MIMIC 标准化和截断、SVD 映射、并列轴选择、SOFA 定向、禁止使用组别/结局及禁止合并试验均相同。"
  - protected_id: PCR-026
    prior_locator: "Feasibility > Operational thresholds table > Observation-mapping external fidelity"
    revised_locator: "Feasibility > Operational thresholds, alternatives, and stop conditions > Observation-mapping external fidelity"
    semantic_status: preserved
    evidence: "第一奇异轴、相关、误差、回归、覆盖、锚点校准、生理范围和可计算比例的全部阈值及失败即终止规则均未变。"
  - protected_id: PCR-027
    prior_locator: "Research design and methods > Conditional trial observation mapping > Analysis targets and trial table"
    revised_locator: "Research design and methods > Conditional trial observation mapping > Analysis targets and trial table"
    semantic_status: preserved
    evidence: "结局层级和排序、概率指数、独立 SOFA、1817/710 目标人群、675 降级条件、缺失敏感性、Holm 家族和亚组边界均相同。"
  - protected_id: PCR-028
    prior_locator: "Research content and work packages > Minimum success definition; Expected outputs > Scientific falsification criteria"
    revised_locator: "Research content and work packages > Minimum success definition; Expected outputs > Scientific falsification criteria"
    semantic_status: preserved
    evidence: "阶段 II 五类必要证据和任一失败即不成功，以及五类直接挑战核心假设的结果均未改变。"
  - protected_id: PCR-029
    prior_locator: "Title, summary, audience, and positioning; Contribution and evidence ladder"
    revised_locator: "Title, summary, audience, and positioning; Contribution and evidence ladder"
    semantic_status: preserved
    evidence: "贡献仍限于有界证据整合、验证、研究基准与资源建设，并继续承认组成方法已有先例。"
  - protected_id: PCR-030
    prior_locator: "Structured abstract > Expected result; Expected outputs > Planned outputs"
    revised_locator: "Structured abstract > Expected result; Expected outputs > Planned outputs; Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "所有标签、审计、模型、模拟、任务、外部验证和试验新分析仍明确为计划生成或尚未生成，没有改写成已完成结果。"
  - protected_id: PCR-031
    prior_locator: "Representative closest-work comparison; Title and positioning claim-support table"
    revised_locator: "Representative closest-work comparison; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: "组成模块已有先例的高置信、完整组合缺口的低至中等置信、限定支持与执行前无实际增量的强度均相同。"
  - protected_id: PCR-032
    prior_locator: "Interpretation of the planned evidence; Scientific and interpretive boundaries"
    revised_locator: "Interpretation of the planned evidence; Scientific and interpretive boundaries"
    semantic_status: preserved
    evidence: "四类证据分别报告、有限更新不得替代外部失败、试验摘要与独立 SOFA 的支持范围均未变。"
  - protected_id: PCR-033
    prior_locator: "Core hypothesis; Current feasibility and evidence status; threshold registration row"
    revised_locator: "Core hypothesis; 尚待冻结的方法规范; Current feasibility and evidence status; threshold registration row"
    semantic_status: preserved
    evidence: "共同指标/事件支持与尺度、状态、滞后、锚定前置条件，月 6 登记、不得依据外部结果修改和既有阈值只能收紧，以及阶段 III 依赖均保留；新增小节只明示两个有界待冻结规范。"
  - protected_id: PCR-034
    prior_locator: "Feasibility > Authoritative limitations > Scientific and interpretive boundaries"
    revised_locator: "Feasibility > Authoritative limitations > Scientific and interpretive boundaries"
    semantic_status: preserved
    evidence: "因果、真实网络、外部验证、试验解释、未测动力学、国际推广、算法/首次/工具主张、有界检索、XBJ-SCAP 人群和阶段 III 边界均完整保留在权威位置。"
  - protected_id: PCR-035
    prior_locator: "Feasibility > Operational thresholds, alternatives, and stop conditions > resource and stage II rows"
    revised_locator: "Feasibility > Operational thresholds, alternatives, and stop conditions > resource and stage II rows"
    semantic_status: preserved
    evidence: "数据库/人员、时间方案、支持不足、泄漏、恢复与任务失败、外部不足和月 24 封存的全部备选与停止逻辑均未变。"
  - protected_id: PCR-036
    prior_locator: "Feasibility > Operational thresholds, alternatives, and stop conditions > trial rows"
    revised_locator: "Feasibility > Operational thresholds, alternatives, and stop conditions > trial rows"
    semantic_status: preserved
    evidence: "试验语义失败、675 人降级、共同变量/映射失败、SOFA 备选、多重性与不一致结果报告的全部后果均相同。"
  - protected_id: PCR-037
    prior_locator: "Feasibility > Scientific and interpretive boundaries > items 1–4"
    revised_locator: "Feasibility > Scientific and interpretive boundaries > items 1–4"
    semantic_status: preserved
    evidence: "观察性关联、预测、状态表示和测量过程不支持因果、真实网络、反事实、中介或控制，阴性对照也不证明正确的边界均保留。"
  - protected_id: PCR-038
    prior_locator: "Feasibility > Scientific and interpretive boundaries > item 5; closest-work/application threshold row"
    revised_locator: "Feasibility > Scientific and interpretive boundaries > item 5; closest-work/application threshold row"
    semantic_status: preserved
    evidence: "全球首次/不存在、专利空白、新算法、数字孪生、控制、临床工具、药物平台和临床应用的证据前提及当前条件性定位均未减弱。"
  - protected_id: PCR-039
    prior_locator: "Feasibility > Scientific and interpretive boundaries > items 3, 4, 6, and 7"
    revised_locator: "Feasibility > Scientific and interpretive boundaries > items 3, 4, 6, and 7"
    semantic_status: preserved
    evidence: "试验分析不支持未测动力学、转移边、完整系统、机制、共同治疗效应或无条件推广；XBJ-SCAP 与缺失字段边界及阶段 III 不得补足阶段 II 失败均保留。"
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

**Decision: `scientific_content_preserved`.** 冻结 register 中 39 个受保护项目均可在 v011 中追踪到相同含义、相同主张强度、相同条件性以及相同方法、阈值、验证、备选和停止承诺。研究身份的五项锚点保持一致；计划工作没有被写成已经完成，当前可行性不足也没有被隐藏。

v011 对主要临床任务的 95% 上置信限构造和医院规模四分位分层指标所作的说明，属于范围明确但仍待冻结的规范，而不是自行选定的新方法。前者在 v009 已由“置信区间构造尚未冻结”明确留下待定空间；v011 保留 +0.01 阈值和判定方向，只限定其须在月 6 前、模型拟合和外部结果访问前冻结。后者保留 v009 的合格体量四分位、接口完整性、医院标识符、固定种子、30%/70% 分组和跨分区处理，只将规模指标的具体计算定义置于月 4–6 审计完成后且验证结果继续隔离的冻结点。两处都没有指定具体估计量、区间算法、医院指标或结果驱动切换分支。

revision delta 明确声明本轮没有科学变化，并把上述两处界定为撤销未经授权具体化后的有界待定规范。独立逐项比较未发现与该声明相矛盾的未声明科学变化。

## Protected-content trace

- PCR-001–PCR-004：身份、问题、目标、研究对象和推断单位保持；主要问题只从连续段落拆成依赖顺序明确的三问。
- PCR-005–PCR-011：阶段、资源角色、试验输入和可行性状态保持；三阶段图被移到概念桥后，XBJ-SCAP 671 人群的英文标签被替换为含原操作定义的中文表述。
- PCR-012–PCR-028：标签、风险集、多状态、联合模型、缺失机制、模拟、外部验证、试验映射、全部数值门槛和成功/证伪规则保持；PCR-020 和 PCR-021 的待定规范仅增加冻结边界说明。
- PCR-029–PCR-039：贡献和缺口主张强度、计划结果状态、权威限制、可行性发现、备选/停止条件及不支持的主张类别均保持。

`undeclared_scientific_changes` 为空；`findings` 为空；`unresolved_issues` 为空。

## Files read and validation

按 preservation 合同计入 `files_read` 的项目输入恰为 frontmatter 所列四个文件，没有读取 narrative、language、evaluation、preflight 或任何先前 content-preservation 报告。为执行本检查，另行读取的评审规则资源为仓库根 `AGENTS.md`、`research-skills-openai/AGENTS.md`、`idea-narrative-assessor/SKILL.md`、`references/content-preservation-contract.md`、`templates/content-preservation-check.md` 和 `scripts/validate_narrative_outputs.py`；这些不是项目证据输入，故不写入合同限定的 `files_read` 数组。

Validator command:

```powershell
python research-skills-openai/skills/idea-narrative-assessor/scripts/validate_narrative_outputs.py --preservation tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/content-preservation-r008.md --register tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v009.yaml
```

Validator result: `PASS: content-preservation output is valid and covers the frozen register`.

## Required routing

v011 可进入新的独立 narrative assessment 和 academic language assessment；本报告不评价其叙事质量、语言质量或科学设计正确性。
