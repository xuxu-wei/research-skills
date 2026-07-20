---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-v003-to-v044-r072
review_id: content-preservation-review-I01-001-r072
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: preservation-reviewer-r072
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r072
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v044
  - protected-content-register-I01-001-v003-r003
  - revision-delta-I01-001-v003-to-v044
input_versions:
  - v003
  - v044
  - r003
  - v044
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v044
    version: v044
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/idea-dossier-v044.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v044
    version: v044
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/revision-delta-v003-to-v044.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/idea-dossier-v044.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/revision-delta-v003-to-v044.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: >-
      YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question
    revised_locator: >-
      YAML frontmatter identity_anchor; Background, current state, gap, significance, and rationale > Background; Research question, objectives, and core hypothesis > Primary research question
    semantic_status: preserved
    evidence: >-
      修订稿继续以脓毒症为中心，覆盖尚未发病的在险时段、首次发病、发病后的生理恢复、持续恶化或器官衰竭以及离开 ICU 或死亡等结局；核心对象仍是全病程患者—时间状态及转移，而不是一般 ICU 风险分层或单一预测任务。
  - protected_id: PCR-002
    prior_locator: >-
      YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; frozen source-context value copied into the register
    revised_locator: >-
      Background, current state, gap, significance, and rationale > Significance; Research question, objectives, and core hypothesis > Objectives
    semantic_status: preserved
    evidence: >-
      修订稿同时保留了三项承诺：24 个月内以文献和专家知识约束候选结构并用公共 ICU 数据完成系统辨识与跨数据库主体检验；以一篇或多篇高水平论文、可审计科学证据和基准资源为交付方向；交付不收缩为单一预测工具。
  - protected_id: PCR-003
    prior_locator: >-
      YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods
    revised_locator: >-
      YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Research design and methods > 两项主要临床任务的预先锁定规范
    semantic_status: preserved
    evidence: >-
      研究对象仍包括可比较的未发病在险时段和发病后轨迹；主要推断单位仍是患者—时间状态及状态转移，主要任务的不确定性分析继续同时尊重患者与医院聚类。
  - protected_id: PCR-004
    prior_locator: >-
      Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit
    revised_locator: >-
      Data, materials, and existing evidence base > 现有证据与可用性状态; 公共 ICU 数据来源及计划用途; Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源
    semantic_status: preserved
    evidence: >-
      文献和专家知识、MIMIC-IV 与 eICU-CRD 仍是核心输入，HiRID 或 AmsterdamUMCdb 仍只作为须预先指定和同等审计的备份。数据库公开存在和版本与团队访问、数据使用协议、可运行提取、项目队列、具名人员及尚未生成的模型结果仍被明确区分，没有把未核验状态改写为已具备。
  - protected_id: PCR-005
    prior_locator: >-
      Data, materials, and existing evidence base > Local RCT evidence and present limits
    revised_locator: >-
      Data, materials, and existing evidence base > 条件性随机对照试验资料的当前状态; Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 仍仅是 24 个月后条件性次要分析的潜在个体级数据来源；本地材料仍被限定为项目内衍生资料，不能替代个体数据授权、原始病例报告表、统计分析计划以及随机化、中心、访视时序和生存或住院语义核验。
  - protected_id: PCR-006
    prior_locator: >-
      Research content and work packages; Research design and methods, including Observational target, anchoring, missingness and abstention
    revised_locator: >-
      Research content and work packages > 24 个月主体研究与日期要求; 工作包及依赖关系; Research design and methods > 双数据库可观测性审计与变量角色; 观察性估计目标、临床锚定与证据不足时的处理; 已知生成机制下的模拟重建性能与错误结构判定
    semantic_status: preserved
    evidence: >-
      资源与可观测性审计、标签和状态及医院分组锁定、简单基线、模拟重建、至多一个复杂候选模型、两项主要任务与两项次要诊断、开发锁定、最终跨数据库检验及其后的条件性试验分析顺序仍在。患者生理状态、治疗行动和检测记录过程继续分离；模拟标准、20 个种子对齐率 90%、自助法保留率 80%、跨数据库方向一致率 80%、状态对齐 0.70 和区间校准要求及其删除、合并或限定解释的后果均保留，预测表现不能豁免失败。
  - protected_id: PCR-007
    prior_locator: >-
      Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation
    revised_locator: >-
      Research content and work packages > 主体研究的合取成功定义; Research design and methods > 以医院为主要分组单位的跨数据库检验
    semantic_status: preserved
    evidence: >-
      数据支持、模拟重建、两项主要任务的概率评分与校准、泄漏清零、最终检验医院集中不更新参数的表现、状态对齐和结构稳定性仍须合取成立。适配医院集中的有限参数调整继续与不更新参数的结果分开报告，不能替代其失败；24 个月后的试验分析不能补足主体失败。
  - protected_id: PCR-008
    prior_locator: >-
      Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system
    revised_locator: >-
      Research design and methods > 两项主要临床任务的预先锁定规范; 发病后互斥状态与事件
    semantic_status: preserved
    evidence: >-
      两项任务、临床事件与信息可用双时间、首次发病风险集、延迟进入、互斥发病后状态、竞争终止、当时可用特征、概率评分与校准、患者和医院聚类不确定性均保持不变。标本与抗菌药 72 小时或 24 小时配对、基线 SOFA、滚动 24 小时成分、首次可排序发病时刻、每次住院总权重为 1、A_t 与下一状态的时间顺序、同时间戳无法排序时不建立相应转移，以及未来治疗、测量频率、重复住院、跨分组处理和结局驱动网格或阈值的泄漏检查均可定位。
  - protected_id: PCR-009
    prior_locator: >-
      Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder
    revised_locator: >-
      Structured abstract > Expected result; Contribution, innovation, impact, application, and closest-work comparison > 正向计划贡献及其证据范围; 代表性相近工作比较
    semantic_status: preserved
    evidence: >-
      修订稿仍明确模型、模拟重建、跨数据库检验和试验新分析均尚未生成；可支持的贡献仍限于条件性的整合、验证和基准资源。各单项模块已有先例，完整组合缺口仍只有低至中等置信度，且不主张新算法或全球首次。
  - protected_id: PCR-010
    prior_locator: >-
      Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria
    revised_locator: >-
      Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源; Working assumptions（待确认规格）; 限制与边界条件; 运行风险、替代与后果
    semantic_status: changed
    evidence: >-
      多数限制仍可在修订稿不同位置追踪，但没有按冻结要求在第 14 节这一全局权威位置完整保留。该节的运行风险表只有公共数据库访问或团队承诺、最终检验数据保管、进度延迟和定位主张四类；标签或泄漏、状态与结构重建、非随机缺失或低重叠、不更新参数的跨数据库失败、试验共同锚点或观测映射失败、试验核心语义失败及月 12、20、24 的具体触发—替代或停止后果仍主要散落在方法和可证伪标准中。共同锚点与观测映射限制未进入第 14 节完整限制清单；两项试验方向不一致或区间过宽时只能报告无支持或跨场景适用性有限且不得以亚组挽救的规则只位于结果解释矩阵。因而未满足 retained_once_at_authority_location 的冻结处置。
  - protected_id: PCR-011
    prior_locator: >-
      Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary
    revised_locator: >-
      Research content and work packages > 24 个月主体研究与日期要求; 工作包及依赖关系; Research design and methods > 满足预设条件后的随机对照试验访视次要分析
    semantic_status: preserved
    evidence: >-
      主体研究仍须在 24 个月内独立完成，试验次要分析仍位于最低交付之外，并以前述主体成功、个体数据授权和核心试验语义核验为共享前提。方法权威小节先列共享前提，再分别规定观测映射分析及其 R0 和 R1 条件与映射失败但临床语义成立时仍可实施的独立临床状态分析；核心语义失败时停止新访视结局，任何试验结果均不能补足主体失败。标题、摘要、问题、目标、工作包、资料、实现、证据链、所需分析、计划产物、贡献和主张表均只保留各自所需的高层功能，没有在这些位置复制完整分支逻辑。
  - protected_id: PCR-012
    prior_locator: >-
      Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions
    revised_locator: >-
      Feasibility, resources, risks, alternatives, and stop conditions > 限制与边界条件
    semantic_status: preserved
    evidence: >-
      第 14 节完整保留观察性数据不能支持治疗因果效应、真实反馈网络、反事实策略、机制、中介或控制，试验分析不能验证未测潜在动力学、转移关系或整个候选表征，以及当前计划不能写成已验证模型、临床决策工具、药物平台、数字孪生、可控系统或无条件推广依据等禁止主张。其他章节只在相邻估计目标、结果解释或主张审计需要时保留局部边界。
undeclared_scientific_changes:
  - protected_id: PCR-010
    change: >-
      冻结登记要求一次性置于第 14 节的完整限制与失败触发—替代或停止后果被压缩并分散，导致共同锚点与观测映射限制以及多类自动后果不再由该全局权威位置完整控制；修订增量未声明这一范围变化。
findings:
  - finding_id: CPF-001
    protected_id: PCR-010
    category: protected_authority_location
    evidence: >-
      第 14 节的四项运行风险不足以覆盖 PCR-010 冻结的全部限制和失败后果，且关键内容仍由方法或结果解释章节单独承载。
    required_disposition: >-
      恢复 PCR-010 在第 14 节的一次性完整权威表述，同时只在其他章节保留推进局部科学推理所必需的最小边界；若确实拟改变这些限制或后果，应明确声明科学变更并重新进入科学审查。
unresolved_issues:
  - >-
    PCR-010：第 14 节没有一次性完整保留所有冻结的关键限制及每个失败触发条件、对应替代或停止后果；共同锚点与观测映射限制和试验方向不一致或区间过宽时的解释规则也位于非权威章节。
---

# Content-preservation check

## Decision rationale

PCR-001 至 PCR-009、PCR-011 和 PCR-012 的研究身份、对象、输入状态、设计承诺、阈值、证据强度、条件性分支及禁止主张均可在 v044 中以相同含义和强度追踪。PCR-010 未满足冻结登记规定的权威位置处置：修订稿虽然保留了多数相关科学边界，却没有在第 14 节一次性保留完整的限制和失败触发—替代或停止逻辑，且修订增量只声明叙事与术语修复，没有声明这一范围变化。因此决定为 `editorial_scope_violation`，不涉及研究身份改变，也不评价任何设计是否科学正确。

## Protected-content trace

主要技术内容被重新分配至主体研究时序、临床任务、模拟重建、跨数据库检验和条件性试验方法等权威小节；这些移动没有改变 PCR-001 至 PCR-009、PCR-011 和 PCR-012 的含义。唯一未解决的保护项是 PCR-010：标签与泄漏、状态重建、缺失与重叠、零更新外部检验、试验共同锚点或观测映射、试验语义及时间节点的失败后果没有在第 14 节形成冻结登记所要求的完整权威表述；试验结果不一致或区间过宽时的解释限制也仍由结果解释矩阵单独承载。

## Required routing

v044 不能直接进入新的叙事或学术语言评估。应先在不改变其他保护项的前提下恢复 PCR-010 的权威位置处置，再由新的独立审查者重新执行内容保护核对；如果作者有意改变相应限制、替代或停止后果，则应明确声明科学变更并返回科学审查。
