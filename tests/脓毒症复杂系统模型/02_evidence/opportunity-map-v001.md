# 脓毒症复杂系统模型：研究机会地图

## 元数据

- Schema version: `research-idea.v3`
- Artifact ID: `opportunity-map-v001`
- Evidence source: `evidence-map-v001`
- Freshness checked: `2026-07-20`

## Summary

- Number of opportunities: 7
- Overall evidence status: `partial`
- Main limitations: 主要临床任务、时间零点、状态定义和成功阈值未固定；数据库变量与时间戳适配尚未做数据级审计；EXIT-SEP/XBJ-SCAP 个体数据访问和逐时变量未核实；现有动态表型、状态空间和 RCT 表型分析使宽泛的新颖性主张风险较高。

## Scientific Gap

- Unanswered problem: 尚不清楚能否在成人脓毒症中，预先规定一个维度受限、临床可解释且可在异质 ICU 数据间复现的状态—转移表示，使其在明确区分生理过程、观测过程和临床处置过程的前提下，分别完成当前状态估计、状态转移时间和未来轨迹预测，并在外部数据库保持校准与临床可用性。
- Missing knowledge or evidence:
  - 尚无项目级证据证明候选公开数据库共享足够一致的变量、采样时点、治疗记录和结局定义，可辨识同一个动态表示。
  - 尚未确定哪些潜在状态可由现有观测辨识、哪些只可预测而不能作因果解释，以及缺失模式和临床测量决策如何进入模型。
  - 尚未建立将“是否发生脓毒症”“何时发生”“何时转向死亡或恢复”“部分观测下状态估计”和“未来轨迹”分开的参照标准、时间范围、删失/竞争风险规则和评价指标。
  - 尚无证据表明一个在开发数据库中得到的关系网络可跨中心、跨地域维持稳定；也尚无证据表明 RCT 的可用时点足以检验该网络的机制含义。
- Consequence of the gap: 在这些证据补齐前，项目可以研究预测性状态表示和跨库可迁移性，但不能把电子病历中的网络权重称为已识别的因果调控关系，也不能声称建立了“完整”或“首个”人体脓毒症系统。若严格设计，阴性结果同样可以界定哪些状态、时间尺度和关系无法从常规 ICU 数据可靠辨识。
- Supporting sources and locators: [公开 ICU 数据库系统比较，Critical Care 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9150442/)；[脓毒症标签实现差异研究，2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10803347/)；[ICU 人工智能外部验证综述，2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11702098/)；[动态多状态脓毒症病程，Critical Care 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6909511/)；[ICU 动态贝叶斯网络，PLOS ONE 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8081190/)；[TRIPOD+AI，BMJ 2024](https://www.bmj.com/content/385/bmj-2023-078378)。

## Novelty Positioning

- Closest work:
  - Klouwenberg et al. 已用多状态 Markov 模型描述感染、脓毒症和后续病程并作独立验证：[Critical Care 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6909511/)。
  - Xu et al. 已识别并跨三个独立 ICU 队列验证 SOFA 轨迹亚型：[Critical Care 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9250715/)。
  - 2026 年研究已在 MIMIC/eICU 上建立并外部验证脓毒症恶化轨迹预测模型：[npj Digital Medicine 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13187286/)。
  - Raghu et al. 和 Ghassemi et al. 已分别把连续/切换状态空间用于脓毒症决策或 ICU 干预状态建模：[PMLR 2017](https://proceedings.mlr.press/v68/raghu17a.html)、[KDD 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5543372/)。
  - Lal et al. 已发表小样本脓毒症数字孪生原型：[Critical Care Explorations 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7671877/)。
  - EXIT-SEP 已完成 SENECA 表型与血必净效应的事后分析：[2025 年事后分析](https://pmc.ncbi.nlm.nih.gov/articles/PMC12257024/)。
- Overlap with closest work: 原设想中的潜在状态、状态转移、轨迹预测、器官网络、干预响应和动态表型均已有局部近邻；单独使用动态聚类、状态空间、数字孪生或 RCT 表型分层不足以构成清晰差异化。
- Evidence-supported differentiation: 目前仅能支持一个**待验证的窄化差异**：在建模前固定临床问题与状态集合，把专家/文献约束与数据估计分开，显式建模缺失和照护过程，对每项预测任务使用独立参照标准，并在至少一个异质外部数据库检验状态定义、转移和校准是否可迁移。其贡献应定位为“可检验的跨库动态表示及其失效边界”，而不是“首个开放复杂巨系统”。这一差异化只得到部分核验，须待数据审计和针对性最近邻检索后确认。
- Novelty risk: `high`

## Reader Reasoning Handoff (Idea workflows only)

| Function | Evidence-grounded handoff |
|---|---|
| Background | 脓毒症是感染相关、随时间变化且高度异质的器官功能障碍。多种公开 ICU 数据提供纵向生命体征、实验室、治疗和结局，但其人群、实践与记录方式明显不同（C1–C4）。 |
| Current state | 已有静态表型、生命体征/体温/SOFA 轨迹、多状态 Markov 模型、状态空间、动态贝叶斯网络、数字孪生原型和外部预测验证；模型迁移后性能常下降，EXIT-SEP 也已有表型疗效事后分析（C7、C8、C11、C14）。 |
| Gap | 尚缺一个在分析前定义、能区分生理—观测—处置过程、对多项任务分别验证且能跨异质数据库复现的状态—转移表示；其可观测性、可辨识性和因果解释边界没有项目级证据（C5、C6、C9、C10、C18、C19）。 |
| Significance | 若该表示可跨库复现，可为动态风险评估、有限观测下状态估计和后续试验分析提供共同坐标；若不能复现，也能给出常规 ICU 数据可辨识边界，减少不可迁移或过度因果化的模型进入临床研究。 |
| Rationale | 因此先以公开数据完成预先规定、任务分离和外部验证的第二阶段最有证据基础；只有达到数据完整性、校准、迁移与可解释性门槛后，才冻结模型并核验 RCT 时点是否允许预先规定的效应修饰或中介问题，动物研究仅用于一个明确机制假设（C12–C17、C19）。 |

## Opportunities

| ID | Type | Title | Description | Supporting claim labels | Supporting source and locator | Evidence confidence | Novelty risk | Why it matters | Feasibility concerns | Recommended generation paths |
|---|---|---|---|---|---|---|---|---|---|---|
| O1 | benchmark | **把四类目标拆成可复核的纵向任务基准** | 以一个共同队列和时间轴，分别定义脓毒症发生/发生时间、死亡或恢复的状态转移、部分观测下状态估计及未来轨迹；为每项任务预先指定预测范围、参照标准、删失/竞争风险、区分度、校准、时间误差和临床效用指标。 | C5 脓毒症标签敏感；C10 多任务须分开；C11 外部性能下降 | [标签实现差异](https://pmc.ncbi.nlm.nih.gov/articles/PMC10803347/)；[TRIPOD+AI](https://www.bmj.com/content/385/bmj-2023-078378)；[PROBAST+AI](https://www.bmj.com/content/388/bmj-2024-082505) | high | medium | 先把“成功”转化为可证伪标准，可阻止单一总体准确率掩盖时间偏差、校准失效或数据泄漏。 | 恢复状态和时间零点需临床共识；事件率、随访、标签泄漏及竞争风险尚未审计。 | 第二阶段主线；所有模型方向的共同基准 |
| O2 | method | **构建受约束且可辨识性明确的动态状态表示** | 由临床/文献给出有限状态、允许关系和时间尺度，数据只估计预先允许的转移及不确定性；明确哪些边是预测关联、哪些具备因果解释所需的设计与假设，并以简单多状态模型作为最低对照。 | C7 已有动态轨迹；C8 已有状态空间近邻；C9 关联不等于因果；C18 完整系统主张未核实 | [多状态 Markov 模型](https://pmc.ncbi.nlm.nih.gov/articles/PMC6909511/)；[状态空间模型](https://proceedings.mlr.press/v68/raghu17a.html)；[动态贝叶斯网络](https://pmc.ncbi.nlm.nih.gov/articles/PMC8081190/)；[时间变化混杂教程](https://www.bmj.com/content/359/bmj.j4587) | moderate | high | 这是最接近原始“反馈系统”设想、同时能限制过度解释的研究对象；可把失败定位到状态定义、时间尺度或辨识条件。 | 状态过多会不可辨识；专家约束需要透明征询；非规则采样、治疗反馈和数据量会限制估计。 | 第二阶段方法主线候选；与 O1、O3 绑定 |
| O3 | data | **把跨数据库可迁移性设为主要贡献之一** | 在 MIMIC-IV 建立或训练，在 eICU-CRD 作多中心美国验证，并在变量允许时选择 HiRID/AmsterdamUMCdb/SICdb 之一及中国感染 ICU 数据作地域压力测试；事先规定统一变量表、单位、采样窗、标签版本和允许的本地再校准。 | C2 公开 ICU 数据互补；C3 单库划分不足；C4 中国数据有限；C11 外部性能下降 | [MIMIC-IV v3.1](https://physionet.org/content/mimiciv/3.1/)；[eICU-CRD v2.0](https://physionet.org/content/eicu-crd/2.0/)；[公开 ICU 数据比较](https://pmc.ncbi.nlm.nih.gov/articles/PMC9150442/)；[中国感染 ICU 数据](https://physionet.org/content/icu-infection-zigong-fourth/1.1/)；[外部验证综述](https://pmc.ncbi.nlm.nih.gov/articles/PMC11702098/) | high | medium | 直接检验系统表示是否超越单中心实践和记录方式，并可产生有价值的失效边界。 | 变量交集可能迫使状态表示过度简化；中国数据较小且选择机制不同；访问审批与计算资源未核验。 | 第二阶段验证主线；可成为 O2 的主要差异化 |
| O4 | metric | **把缺失值填补与潜在状态估计分开评价** | 建立两层验证：对真实保留测量采用接近临床过程的遮蔽评估填补；对潜在状态则用未来观测、事件转移和外部校准间接检验，并报告不确定性与对测量策略的敏感性。 | C6 缺失模式有信息；C10 任务须分开 | [ICU 患者资料缺失信息观察研究](https://pubmed.ncbi.nlm.nih.gov/30622091/)；[多机构住院患者实验室缺失模式研究](https://pmc.ncbi.nlm.nih.gov/articles/PMC10849195/)；[GRU-D](https://pubmed.ncbi.nlm.nih.gov/29666385/) | high | high | 防止把算法填补值当作不可观测的“真实状态”，也能检验模型是否只学习了某医院的开单习惯。 | 潜在状态无直接金标准；随机遮蔽会高估真实世界表现；需要按医院和变量检查测量政策。 | O1 的必要评价模块；O2 的伴随分析 |
| O5 | benchmark | **把既有动态表型作为比较基准和稳定性压力测试** | 不把聚类本身作为主新颖性；重现 SENECA、SOFA 或生命体征轨迹中的可行基准，比较患者随时间换类、边界不确定性、状态与结局校准以及跨库一致性。 | C7 现有表型和轨迹丰富；C14 RCT 表型分析已发表 | [SENECA](https://jamanetwork.com/journals/jama/fullarticle/2733996)；[SOFA 轨迹](https://pmc.ncbi.nlm.nih.gov/articles/PMC9250715/)；[生命体征轨迹](https://pmc.ncbi.nlm.nih.gov/articles/PMC9510534/)；[EXIT-SEP 表型事后分析](https://pmc.ncbi.nlm.nih.gov/articles/PMC12257024/) | high | high | 让新表示与临床已知异质性建立可解释联系，并暴露静态分型对时间变化和边界患者的不足。 | 不同研究变量和入组窗不一致；复现失败可能来自标签/采样差异；不宜进行无约束的多重亚组探索。 | 第二阶段对照与敏感性分析，不建议作为唯一主线 |
| O6 | implementation | **冻结公开数据模型后再开展条件性 RCT 二次分析** | 只有在第二阶段的状态定义、代码和分析问题冻结，且试验数据证实具备必要时点后，才在 EXIT-SEP 检验预先规定的动态状态是否修饰随机治疗效应；若研究中介，只估计可识别的有限路径并报告假设。XBJ-SCAP 仅作疾病范围合适的补充或独立验证。 | C12 EXIT-SEP；C13 XBJ-SCAP 范围；C14 已有表型分析；C15 交互与中介要求；C16 指南审慎；C19 数据未核实 | [EXIT-SEP](https://pmc.ncbi.nlm.nih.gov/articles/PMC10152378/)；[XBJ-SCAP](https://pmc.ncbi.nlm.nih.gov/articles/PMC6727951/)；[EXIT-SEP 表型分析](https://pmc.ncbi.nlm.nih.gov/articles/PMC12257024/)；[AGReMA](https://jamanetwork.com/journals/jama/fullarticle/2784353)；[CONSORT 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11995452/)；[SSC 2026](https://doi.org/10.1007/s00134-026-08361-1) | moderate | high | 随机试验可把后续问题从纯观察性相关推进到治疗效应及其有限机制解释，同时避免用试验反向调节开发模型。 | 实际数据权属和时间粒度未核实；既有表型分析造成直接重叠；交互功效、多重性、中介假设及 XBJ-SCAP 疾病差异均可能阻止分析。 | 第三阶段条件性方向；不是第二阶段成功的必要条件 |
| O7 | implementation | **只为一个预先规定的机制假设设计可选动物桥接研究** | 若第二阶段和 RCT 分析共同提出具体、可干预且在人类数据中可测的机制，再选择能模拟感染源、器官功能障碍、复苏和抗菌治疗的模型，遵循 MQTiPSS 与 ARRIVE 2.0；不把动物结果称作临床预测模型的外部验证。 | C17 动物规范与转化冲突；C19 资源未核实 | [MQTiPSS](https://pmc.ncbi.nlm.nih.gov/articles/PMC6093828/)；[ARRIVE 2.0](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000410)；[人鼠炎症相似性冲突：Seok et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3587220/)、[Takao & Miyakawa](https://pmc.ncbi.nlm.nih.gov/articles/PMC4313832/) | moderate | unverified | 可在严格窄化后验证一个机制链条，但应避免用宽泛模型造成低可转化性和资源分散。 | 无具体机制、模型、样本量、终点、实验平台或伦理路径；人鼠可转化性依赖模型和分析尺度。 | 第三阶段可选支线；未满足机制触发条件时停止 |

## Idea Direction Evidence (Idea workflows only)

- Current direction value: `uncertain`
- Evidence confidence: `moderate`
- Distinct supported directions:
  - Title: 受约束的跨库脓毒症动态状态模型
  - Rationale: 最贴近原始第二阶段设想，并可通过 O1 的任务基准、O2 的受约束表示和 O3 的外部验证形成可证伪主线；现有近邻要求把贡献窄化到预先规定、跨库复现和失效边界。
  - Supporting claims: C2、C3、C5–C11、C18
  - Evidence confidence: `moderate`
  - Feasibility note: 必须先完成变量交集、时间戳、事件率、状态维度和辨识性审计；12–18 个月内宜限制状态数和主要任务数。
  - Closest to current direction: `true`
  - Title: 以可迁移性和标签稳健性为主贡献的公开 ICU 基准
  - Rationale: 公共数据库异质性和外部性能下降证据较强；即使复杂动态模型不胜出，规范化队列、任务和跨库失效分析仍可形成独立科学价值。
  - Supporting claims: C2–C6、C10、C11
  - Evidence confidence: `high`
  - Feasibility note: 变量协调工作量大，但科学目标比“完整系统”更清楚；需预先限定数据库组合。
  - Closest to current direction: `false`
  - Title: 冻结动态状态后的随机试验效应修饰分析
  - Rationale: 随机分配可支持明确的治疗效应问题，但只能在个体数据、时间变量和分析功效满足要求时开展；现有 EXIT-SEP 表型分析使其不适合作为未经窄化的首要新颖性来源。
  - Supporting claims: C12–C16、C19
  - Evidence confidence: `moderate`
  - Feasibility note: 当前资源状态未核实，应保留为触发式第三阶段而非承诺性主线。
  - Closest to current direction: `false`
- Conflicts or ties: “动态系统方法贡献”与“跨库验证/基准贡献”都可构成第二阶段中心，但前者新颖性风险更高、后者与原始理论雄心距离更远；何者为主要论文问题会实质改变状态维度、数据选择和成功标准。RCT 方向受数据权限和既有分析双重约束。
- Negative searches:
  - 有界检索未核验到与固定对象完全相同的“完整人体脓毒症开放复杂巨系统”，但有限检索不能证明其不存在，不能据此作首次主张。
  - 未发现 EXIT-SEP 或 XBJ-SCAP 个体数据公开下载、完整代码本或逐时变量清单的可核验证据。
  - 未取得证明候选公共数据库共同覆盖全部预想状态、干预和事件的项目级数据审计。
- Recommended route: `direction_route_confirmation_required`
- Recommendation rationale: 需要负责人先确认第二阶段的首要科学贡献是“动态状态表示”还是“跨库可迁移性基准”，并把 RCT 分析明确为条件性后续；在该选择完成前，多个终点和贡献类型仍然并列，直接写成一个构想会造成不可检验的范围扩张。

## Downstream Notes

### For multi-path-idea-generator

- 最多形成三条实质不同路径：受约束动态状态主线、跨库可迁移性/基准主线、冻结模型后的条件性 RCT 主线；不要把不同算法包装成不同方向。
- 每条路径必须继承 C5、C9、C10、C18、C19 的限定：固定标签和时间零点、关联不等于因果、多任务分开、不得作“首个/完整”主张、资源未核实。
- 动物研究只能附属于一个已明确的人类机制假设，不应独立补足第二阶段证据。

### For methodology-statistics-preflight

- 先做数据库访问、变量交集、单位、时间戳、事件率、缺失机制和标签版本审计，再判断状态维度和样本量。
- 分别检查时间到事件、竞争风险、纵向状态估计、动态预测、校准、决策效用和跨库再校准方案；防止时间泄漏与同一患者跨分割。
- 对状态空间或网络模型审查可观测性、结构/参数可辨识性、非规则采样、治疗反馈、适应症混杂、模型复杂度和不确定性。
- RCT 预审必须核验数据权属、测量时点、交互功效、多重性、中介—结局混杂假设及与既有事后分析的重叠。

### For complete dossier writer

- 将相关事实、限定语和标准引文写入自足文本；不得向独立评价者暴露本地图。
- 用标准术语说明状态空间、动态预测、外部验证、效应修饰和中介分析；“开放复杂巨系统”若保留，必须作为用户工作设想解释，不能作为已被文献认可的模型类别。
- 清楚区分来源事实、用户拥有资源的陈述、证据推断和未核实状态；不将预测性网络边改写为调控靶点。

### For idea-portfolio-assembler

- 链接本证据地图与机会地图，并保留 RCT 访问、公共数据变量适配、主要方向选择及新颖性定向检索四项未决事项。
- 组合时不得把 O1–O7 全部堆入单一 12–18 个月方案；主线应限于 O1–O3，其他作为比较模块或触发式后续。

### For proposal-context-brief-builder / proposal-orchestrator

- 将阶段门槛写成可核验条件：数据审计通过；任务与成功阈值预先规定；至少一个异质外部数据库完成；模型冻结；RCT 变量/权限/功效核验；最后才考虑动物机制验证。
- 预算和时间安排应把数据协调、代码复现和外部验证列为实质工作，而不是默认数据库可直接合并。

### For proposal-evaluator

- 独立评价者只应收到已经整合证据和限定语的完整构想，不接收本地图本身。
- 评价时重点核查：主要问题是否唯一、四类任务是否拆分、外部验证是否真实、因果措辞是否受限、RCT 与既有表型分析是否重叠、条件性阶段是否有明确停止条件。
