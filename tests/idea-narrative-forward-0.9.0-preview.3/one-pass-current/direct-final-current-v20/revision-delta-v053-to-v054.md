---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v053-to-v054
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v053-to-v054
source_artifact:
  artifact_id: idea-dossier-I01-001-v053
  version: v053
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/idea-dossier-v053.md
target_artifact:
  artifact_id: idea-dossier-I01-001-v054
  version: v054
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/idea-dossier-v054.md
writer_brief:
  artifact_id: editorial-repair-writer-brief-I01-001-r120
  version: r120
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/editorial-repair-writer-brief-r120.yaml
change_type: editorial_repair_delta
scientific_change_declared: false
frozen: true
---

# Revision delta: v053 → v054

## Repair actions executed

| Repair item | Revised locator | Operation | Observable result |
|---|---|---|---|
| NRP-001 | Research design and methods > Secondary representation diagnostics; 试验观察映射和独立分析 | move | 两项次要表征诊断完整结束后才出现试验公式、资格分支和试验特异处理；试验方法正文整体移动，EXIT-SEP 与 XBJ-SCAP 仍分开，旧位置无残片或副本。 |
| NRP-002 | Objectives；Work packages；Evidence chains；Required analyses；Expected outputs；Contribution；Claim-support；Feasibility/assumptions/risks/limitations | consolidate | “试验观察映射和独立分析”保留唯一完整技术规范，“Limitations and boundary conditions”保留唯一完整 11 类限制；其他位置仅保留本节所需的目标、依赖、证据、输出、解释或停止后果。 |
| F-01 | Contribution and evidence ladder > 从属的试验访视结局证据 > 必需证据 | replace | 不可见的“第 7 节”已由“Research design and methods 中‘试验观察映射和独立分析’小节”替代；数据、语义、结局构造、缺失、中心和多重性六项要求均保留。 |
| F-02 | Research design and methods > 试验观察映射和独立分析 > 外部忠实度判定 | replace | 明确为“第一奇异轴所解释的 L_C Frobenius 能量比例至少为 50%”；矩阵、奇异轴、阈值和全部条件合取不变。 |

## NRP-002 locator dispositions

| Locator | Executed disposition |
|---|---|
| Objectives | 目标 4 仅保留主体研究达到标准后、按试验分别分析且不计入阶段 II 成功的身份陈述。 |
| Work packages and minimum route | WP5 保留时间、依赖、分试验输出和不属于阶段 II 成功；研究顺序保留试验结果不能绕过前序失败的后果。 |
| Evidence chain: 有前置条件的随机试验次要分析 | 四个必需字段完整保留；方法字段只承担分试验核验、实际访视结局、缺失/敏感性和多重性功能。 |
| Required analyses and evidence | 改为授权、原始语义、试验特异资格和执行固定方法的紧凑要求；字段表、公式、插补和多重性细节不再重复。 |
| Planned outputs | 仅保留分试验结果或不开展新访视分析的原因记录。 |
| Falsification and stop criteria | 映射失败仅阻断代理排序结局，符合条件时仍保留独立 SOFA 分支；核心语义失败停止全部新访视结局，方向不一致或区间过宽不以亚组选择修复。 |
| Interpretation matrix | 分开保留映射结局和独立 SOFA 结局两行及其不同的允许与禁止解释，不重复资格算法。 |
| Contribution and evidence ladder | 保留从属证据层级和主张强度，并以具名方法小节承载完整技术要求。 |
| Verified representative closest-work comparison | 仅保留试验二次分析先例和“主体研究之后、按试验分开”的定位差异。 |
| Title and positioning claim-support table | 从属延伸主张、条件状态和非主要贡献边界均保留；实施列缩为具名技术权威。 |
| Feasibility and resources | 仅陈述访问、人员、工时、范围和结果状态，不复述试验分支。 |
| Working assumptions；Risks, alternatives, and stop conditions | 四项假设的固定内容、负责人、时点和后果完整保留；风险表仅保留对象特异触发、响应和后果。 |
| Limitations and boundary conditions | 11 类限制原样保留为唯一完整限制权威，无跨节指针替代限制。 |

## Protected-content preservation receipt

| Protected ID | Revised locator(s) | Text-grounded preservation evidence |
|---|---|---|
| PCR-001 | frontmatter > identity_anchor | 五个 identity-anchor 值逐字保留。 |
| PCR-002 | Primary research question；Objectives | 全病程对象、两库检验、主体成功后分试验延伸及预测/观察与因果区分均保留。 |
| PCR-003 | Core hypothesis and evidence boundary | 共同支持、预先固定、模拟恢复、外部稳定性及非因果估计边界均保留。 |
| PCR-004 | Observational target, anchoring, and evidence-qualified interpretation | 纵向脓毒症中心对象、发病前在险时段、发病后轨迹及患者—时间状态/转移单位均保留。 |
| PCR-005 | Protocol locks for the two primary clinical tasks | 两项任务的人群、时钟、标志时点、竞争事件、估计目标、指标和聚类不确定性完整保留。 |
| PCR-006 | Mutually exclusive post-onset state and event system | 12 小时赋值、六状态固定优先级、可复发/吸收属性和无法排序规则均保留。 |
| PCR-007 | Variable roles | Y、A、M、标签专用变量和 B 的分离及双重用途隔离保留。 |
| PCR-008 | Public intensive-care database roles and support audit | MIMIC-IV、eICU 与预指定备份数据库的角色和替代条件保留。 |
| PCR-009 | Public intensive-care database roles and support audit > audit table | 访问、队列、事件、医院、锚点、接口、缺失、链接和支持审计字段及判定保留。 |
| PCR-010 | Current resource and result status | 已核验数据库存在/版本与未核验访问、样本支持、人员及未生成结果的状态区分保留。 |
| PCR-011 | Local randomized-trial evidence status | 两份衍生报告的样本/访视事实、证据层级和原始语义缺口保留。 |
| PCR-012 | Current resource and result status > trial rows | 授权、原始表单/SAP、随机化、中心、访视和生存/住院语义未核验状态保留。 |
| PCR-013 | Feasibility and resources | 六类最低团队职责、尚无具名承诺/工时和模型范围限制保留。 |
| PCR-014 | Work packages and minimum route | 审计至试验延伸的固定先后顺序、简单路线和试验不能绕过前序失败的后果保留。 |
| PCR-015 | Conjunctive minimum success definition | 双库支持、模拟、两项主要任务、泄漏、外部医院/状态/结构五项合取标准及阈值保留。 |
| PCR-016 | Protocol locks > primary pre-onset task | 未来 12 小时首次发病累积发生风险、标志时点、历史窗、竞争终止、指标和达标条件保留。 |
| PCR-017 | Protocol locks > primary post-onset task | 第 7 日有利状态占用、组成分报、多状态/Aalen–Johansen、指标和不确定性保留。 |
| PCR-018 | Protocol locks > event and availability clocks | 培养—抗菌药配对、SOFA 基线/窗口、事件时刻及信息可用时刻规则保留。 |
| PCR-019 | Mutually exclusive state system > definitions | 恢复、恶化/新器官衰竭、离开 ICU、转院/失访和死亡的定义与优先级保留。 |
| PCR-020 | Observational target and anchoring | 每维至少两个共同锚点、载荷/尺度、维数/机制/滞后上限、20 种子和可恢复不变量保留。 |
| PCR-021 | Observational target > missingness and action support | 显式测量过程、五个偏移值、临界点、5%/95% 与 20% 支持阈值和非治疗作用解释保留。 |
| PCR-022 | Absolute simulation > regimen | 月 7–10、至少 1,000 次或 Monte Carlo 误差阈值及全部生成/错设轴保留。 |
| PCR-023 | Absolute simulation > continuous branch | X_b/估计矩阵、全部典型相关、秩/维度失败记 0、L 公式与 0.80 标准及负责人时点保留。 |
| PCR-024 | Absolute simulation > recovery table | 离散状态、转移、边、零边、错设、校准、种子/自助/外部对齐标准和失败动作保留。 |
| PCR-025 | Hospital-primary validation > partition and cross-hospital rules | 体量/接口分层、种子 20260717、30%/70%、跨区患者规则、敏感性和支持触发保留。 |
| PCR-026 | Hospital-primary validation > four update operations | 不更新、仅校准、仅观测层和全模型重拟合的固定顺序及证据角色保留。 |
| PCR-027 | 试验观察映射和独立分析 > 共享前提 | 阶段 II 合取成功、资料授权、核心试验语义三项共享前提及映射资格非共享性质保留。 |
| PCR-028 | 试验观察映射和独立分析 > 观测映射资格与忠实度 | 候选锚点资格、SVD 映射、外部忠实度全部阈值、遮蔽资料覆盖和失败判定保留；Frobenius 句仅澄清比例关系。 |
| PCR-029 | 试验观察映射和独立分析 > 分层标准化概率指数 | 死亡/代理/出院排序、唯一主要估计目标、公式、并列半分、层权重、方向和分试验估计保留。 |
| PCR-030 | 试验观察映射和独立分析 > 分支与停止 | 映射失败后的独立 SOFA 分支、核心语义不足时停止和负责人确认失败后果保留。 |
| PCR-031 | 试验观察映射和独立分析 > trial table | EXIT-SEP 与 XBJ-SCAP 样本集、访视、缺失/插补/界限、中心、Holm 和停止规则完整保留。 |
| PCR-032 | Secondary representation diagnostics | 伪遮蔽和未来轨迹两项诊断、各自指标、分层及不改变主要判定的角色完整保留。 |
| PCR-033 | Required analyses and evidence；试验观察映射和独立分析 | 阶段 II 八组必需分析原样保留；试验启动要求压缩为授权、语义、资格和固定方法，完整细节保留在方法权威。 |
| PCR-034 | Falsification and stop criteria > 时钟与信息泄漏；数据支持 | 泄漏修正/删除、严重问题阻止测试，以及支持不足时简化/备份/停止的后果保留。 |
| PCR-035 | Falsification and stop criteria > 绝对恢复；非随机缺失；外部结果 | 恢复失败不晋级、预测不能逆转、缺失/支持限定和未更新外部失败后果保留。 |
| PCR-036 | 试验观察映射和独立分析 > 忠实度与分支；Falsification > 试验观测映射/核心语义 | 全部资格与忠实度判定在方法中保留；停止小节保留代理结局阻断、独立 SOFA 备选和核心语义停止。 |
| PCR-037 | Falsification and stop criteria > 时间 | 月 12、月 20、月 24 的触发与相应后果保留。 |
| PCR-038 | Risks, alternatives, and stop conditions | 数据库/团队/隔离/跨院支持/时间/试验资料/定位风险的触发、响应和后果保留。 |
| PCR-039 | Title, summary, audience, and positioning；Structured abstract | 候选表征、计划跨库检验、待生成产物和从属试验延伸的证据状态保留。 |
| PCR-040 | Contribution and evidence ladder | 数据、重建/任务、跨库和从属试验四层证据及主张强度保留。 |
| PCR-041 | Verified representative closest-work comparison | 五条近邻研究线、已有先例、条件性差异和低至中等组合缺口置信度保留。 |
| PCR-042 | Interpretation matrix | 七种结果模式各自允许与禁止解释完整保留。 |
| PCR-043 | 试验观察映射和独立分析；trial evidence chain；Planned outputs | 分试验次要结果或不分析原因、不得计入/补足阶段 II 及不合并试验的边界保留。 |
| PCR-044 | Working assumptions > 连续潜在状态恢复 | WA-R117-01 的计算定义、系统辨识/纵向统计负责人、月 7 前时点及未确认/事后改变后果保留。 |
| PCR-045 | Working assumptions > 试验概率指数 | WA-R117-02 的唯一概率指数、并列半分、目标集/分层/权重、统计负责人时点及停止后果保留。 |
| PCR-046 | Working assumptions > clinical-scale-to-simulation mapping | 月 7 前的信息来源、已固定内容和未解决时不启动恢复/不晋级后果保留。 |
| PCR-047 | Working assumptions > multicategory calibration | 月 6 前可用信息、固定指标/阈值及未解决时不判成功/不访问最终测试后果保留。 |
| PCR-048 | Limitations > 1 | 资源、访问、团队和实际支持未核验的完整限制保留。 |
| PCR-049 | Limitations > 2 | 标签、时钟和信息泄漏的完整限制保留。 |
| PCR-050 | Limitations > 3 | 可恢复性仅限预设条件、模拟非真实识别及预测不能替代结构证据的限制保留。 |
| PCR-051 | Limitations > 4 | 非随机缺失敏感性范围及低行动支持不支持治疗作用的限制保留。 |
| PCR-052 | Limitations > 5 | 数据库差异、未更新外部证据优先和有限适配不能补偿失败的限制保留。 |
| PCR-053 | Limitations > 6；milestones；Risks > time | 24 个月阶段 I–II、月 12/20/24 后果和阶段 III 不能补足阶段 II 的限制保留。 |
| PCR-054 | Limitations > 7 | 试验资料条件性、原始语义未核验、稀疏/异质及不支持伪连续或合并效应的限制保留。 |
| PCR-055 | Limitations > 8 | 候选锚点/单位未核验、忠实度无结果及映射与独立 SOFA 的不同解释范围保留。 |
| PCR-056 | Limitations > 9 | 代表性检索非系统综述、未覆盖来源和组合缺口低至中等置信的限制保留。 |
| PCR-057 | Limitations > 10 | XueBiJing 监管适用范围和不支持无条件国际推广的限制保留。 |
| PCR-058 | Limitations > 11 | 观察性/预测及试验次要分析的全部禁止主张和不可表述为已验证工具/平台的边界保留。 |
| PCR-059 | 24 个月最低交付与时间节点 | 签署只代表计划职责、测试资料隔离至月 18–20 及全部节点决策保留。 |
| PCR-060 | Working assumptions > closing qualification | 事件/参数阈值仅为筛选、待定规范须按时解决且不事后补写数值的边界保留。 |
| PCR-061 | Limitations > 11 | 真实因果网络、治疗因果效应、反事实策略、机制、中介、控制和数字孪生均明确不受支持。 |
| PCR-062 | Limitations > 11；Contribution and evidence ladder | 已验证模型、临床决策工具、药物平台、临床有效性和无条件推广均未获支持；额外证据要求保留。 |
| PCR-063 | Verified representative closest-work comparison；closing paragraph | 新算法、全球首次/不存在和专利不存在主张均未引入；更强定位所需扩展检索保留。 |
| PCR-064 | 试验观察映射和独立分析；Interpretation matrix；Limitations > 11 | 试验访视差异不能验证潜在动力学/边/整个系统，试验不合并且亚组不能改变主要解释。 |

## Identity-anchor byte comparison

| Field | Source register and revised dossier value | Result |
|---|---|---|
| primary_research_question | `can a knowledge-constrained, uncertainty-aware dynamic system representation of ICU patients cover the sepsis-centered pre-onset, onset, post-onset, and outcome continuum, demonstrate cross-database state/structure validity, and then test limited randomized intervention perturbations without conflating prediction with causality?` | identical |
| primary_objective | `construct and validate the sepsis complex-system model, with stage II completed within 24 months.` | identical |
| study_object | `the longitudinal sepsis-centered ICU patient system, including comparable at-risk non-onset intervals and post-onset trajectories.` | identical |
| core_data_or_evidence_base | `literature/expert priors; longitudinal public ICU data; conditionally available EXIT-SEP and XBJ-SCAP individual-level RCT data.` | identical |
| primary_unit_of_inference | `patient-time state and state transition, with patient and hospital clustering respected.` | identical |

## Limitations, assumptions, branches, and milestones

The sole complete limitations authority contains exactly these 11 numbered families once: resources/access/team; labels/clocks/leakage; recoverability/structural scope; nonrandom missingness/action support; cross-database evidence; time/delivery; trial data/semantics; common anchors/mapping; closest-work uncertainty; regulatory applicability; prohibited claims. No family was replaced by a cross-section pointer.

WA-R117-01 retains the complete continuous-state recovery definition, system-identification owner, independent longitudinal-statistics review, pre-result/month-7 deadline, and no-promotion/re-review consequences. WA-R117-02 retains the unique stratified standardized probability index, tie handling, analysis set, original strata, pooled-arm stratum weights, named-statistician confirmation before treatment comparison, and stop consequence. The clinical-scale and multicategory-calibration assumptions retain their owners-by-function, deadlines, permitted information and consequences. Mapping eligibility remains branch-specific; mapping failure leaves the independent SOFA branch available when eligible; failure of core trial semantics stops all new visit outcomes. Month 3, 6, 7, 12, 20 and 24 decisions and their original consequences remain explicit. No trial result can bypass, count toward or repair stage-II success.

No causal, mechanism, control, digital-twin, already-validated-tool, clinical-effectiveness, pooled-effect, common-mechanism or unconditional-promotion claim was introduced. No scientific choice was required or made.

## Reader-facing role concordance

| Scientific role | One reader-facing name | First-use locator | Competing forms removed or reclassified | All-occurrence scan |
|---|---|---|---|---|
| Central study object | 脓毒症全病程候选动态系统表征 | Title | No new competing form | consistent |
| Primary research question | 构建并计划验证全病程候选动态系统表征 | Primary research question | No competing question | consistent |
| Primary clinical task 1 | 未来 12 小时首次发病风险 | Structured abstract > Approach | Descriptive variants remain task descriptions | consistent |
| Primary clinical task 2 | 发病后第 7 日有利状态占用 | Structured abstract > Approach | Descriptive variants remain task descriptions | consistent |
| Primary outcomes | 12 小时首次发病累积发生风险；第 7 日有利状态占用 | Protocol locks | No competing primary outcome | consistent |
| Candidate representation | 候选动态系统表征 | Title | “复杂候选” retained only for the method-specific model branch | consistent |
| Conditional trial extension | 有前置条件的随机试验次要分析 | 试验观察映射和独立分析 > opening | Stage III retained only as a phase label where chronology requires it | consistent |
| Mapping-ordered visit outcome | 由死亡、一维可观测代理和存活出院共同排序的访视结局 | 试验观察映射和独立分析 | No competing primary estimand | consistent |
| Independent SOFA endpoint | 独立的 SOFA 有序临床状态端点 | 试验观察映射和独立分析 | Kept distinct from mapping outcome | consistent |
| Evidence status | 计划中、尚未生成或尚未核验 | Current resource and result status | No planned work presented as completed | consistent |
| Contribution | 条件性的证据整合、验证、基准或研究资源 | Structured abstract > Contribution and impact | Trial extension remains subordinate, not co-primary | consistent |

## Deterministic check receipts

- **Exact structural and plugin-version lint:** `python -B research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/idea-dossier-v054.md --expected-plugin-version 0.9.0-preview.3` exited successfully with `OK`. The 15 H2 sections, five Background-to-Rationale H3 sections, five four-field evidence chains, Key techniques table and Claim-Support table are present. The frontmatter binds `idea-dossier-I01-001-v054`, `v054`, the v20 path, plugin version `0.9.0-preview.3`, and `editorial_repair`.
- **Advisory short-form diff:** emitted `quoted-label: 试验观察映射和独立分析` at lines 282, 380, 428 and 449. Each occurrence is `descriptive_not_label`: line 282 is the plain-language subsection title; lines 380, 428 and 449 are direct locatable references to that same subsection. No candidate is used as a coined scientific construct, and no unresolved terminology issue was confirmed.
- **Protected-content scan:** PCR-001 through PCR-064 were checked against both their source locators and the revised locators shown above; each has exactly one preservation row and remains textually present.

