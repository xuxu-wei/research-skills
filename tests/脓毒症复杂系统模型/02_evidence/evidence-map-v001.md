# 脓毒症复杂系统模型：证据地图

## 元数据

- Schema version: `research-idea.v3`
- Artifact ID: `evidence-map-v001`
- Source skill: `research-opportunity-mapper`
- Freshness checked: `2026-07-20`

## Scope

- Research domain: 成人脓毒症、重症医学、纵向临床数据、系统辨识与预测模型
- Topic / raw idea: 以文献和专家知识描述反馈关系，利用公开 ICU 纵向数据辨识状态演化及网络关系；若公开数据阶段成立，再以 EXIT-SEP、XBJ-SCAP 等随机试验作条件性二次分析，并可选择开展动物机制验证。
- Intended output: 为后续研究方向选择、方法学预审和完整研究构想撰写提供可追溯证据边界；本文件不评价或选择最终研究构想。
- Downstream task: `idea_generation`
- Evidence status: `partial`

## Evidence Acquisition Note

- 检索模式：`standard`。课题边界已有雏形，但主要终点、数据库、时间窗、模型对象和验证阈值尚未固定，因此采用“先覆盖、再聚焦、最后补缺”的有界检索。
- 经批准读取的项目输入仅有：`00_input/user-idea-v001.md` 和 `01_context/research-context-brief-v001.md`；未读取该测试目录中的任何其他项目文件。
- 检索日期与范围：截至 2026-07-20，覆盖奠基性研究至当日可核验资料；优先 PubMed/PMC 原始论文、期刊原文、PhysioNet/数据库官方文档、SCCM/ESICM 指南和正式报告规范。
- 检索主题簇：脓毒症定义与筛查；公开 ICU 数据及访问条件；标签和时间零点；系统辨识、状态空间、动态贝叶斯网络与数字孪生；缺失信息与状态重建；动态表型和轨迹；跨医院/跨数据库验证；EXIT-SEP 与 XBJ-SCAP 及其二次分析；随机试验中的效应异质性和中介分析；可选动物验证。
- 排除边界：不扩展为系统综述；儿童脓毒症、纯组学研究和与 ICU 纵向建模无直接关系的动物研究不作全面检索；预印本不作为关键结论的唯一支持。
- 停止理由：每个预定领域均已取得至少一项可核验的代表性原始来源或官方来源；继续检索的新增结果开始重复已识别的工作类型。剩余关键不确定性主要依赖个体数据访问、数据字典、采样时点、预注册分析方案和更全面的引文数据库检索，而不是继续扩大一般文献搜索。

## Source Summary

| Source class | Sources available | Role | Limitations |
|---|---|---|---|
| User-provided materials | 原始研究设想；研究背景简报 | 确认三阶段设想、公开数据库优先、RCT 与动物研究均为条件性后续步骤，以及 12–18 个月资源边界 | 属于用户陈述，不等同于已核实事实；未提供数据字典、方案、统计分析计划或数据访问证明 |
| Retrieval routes executed | PubMed/PMC；JAMA、BMJ、Nature、PLOS、Springer 等期刊页面；PhysioNet 和数据库官方仓库；SCCM/ESICM 指南页面 | 核验临床定义、可用数据、最近邻研究、报告规范、随机试验和动物研究规范 | 属于有界证据地图，不具备系统综述的穷尽性；部分来源只核验到摘要或官方元数据 |
| Retrieved / available sources | Sepsis-3；2026 Surviving Sepsis Campaign；MIMIC-IV、eICU-CRD、HiRID、AmsterdamUMCdb、SICdb、中国感染 ICU 数据；动态表型、状态空间、外部验证、RCT 和动物规范的原始来源 | 支持科学缺口、方法约束、可行方向及新颖性风险判断 | 数据库字段可比性、可导出时间序列和队列重叠尚未做数据级审计 |
| Missing / inaccessible sources | EXIT-SEP/XBJ-SCAP 个体数据、代码本和精确采样时点；专家问卷材料；拟用公共数据库的实际访问凭证；预注册方案；完整引文网络 | 决定后续机制分析、时间序列重建、效应异质性分析和“首次”表述能否成立 | 资源状态均须视为未核实，不能用论文已发表替代个体数据已可用 |

## Key Claims

| Claim ID | Human-readable label and claim | Type | Support status | Supporting source and locator | Opposing evidence | Confidence | Novelty verification | Guideline alignment | Limitations |
|---|---|---|---|---|---|---|---|---|---|
| C1 | **[来源事实] 成人脓毒症的临床定义与筛查边界。** Sepsis-3 将脓毒症定义为感染所致宿主反应失调引起的危及生命的器官功能障碍；2026 成人指南强调其为临床诊断，并反对仅以 qSOFA 作为唯一筛查工具。 | guideline | supported | [Singer et al., JAMA 2016, 定义与临床操作化](https://pmc.ncbi.nlm.nih.gov/articles/PMC4968574/)；[Prescott et al., Surviving Sepsis Campaign 2026, 成人筛查建议](https://doi.org/10.1007/s00134-026-08361-1) | 无直接反证 | high | not_applicable | aligned | 数据库中的回顾性标签仍需将感染、器官功能和时间零点具体操作化 |
| C2 | **[来源事实] 存在互补的公开成人 ICU 纵向数据。** MIMIC-IV、eICU-CRD、HiRID、AmsterdamUMCdb 和 SICdb 分别提供不同地域、中心数量、采样密度与病例结构；多数需要培训、数据使用协议或身份认证。 | data | supported | [MIMIC-IV v3.1 官方页](https://physionet.org/content/mimiciv/3.1/)；[eICU-CRD v2.0 官方页](https://physionet.org/content/eicu-crd/2.0/)；[HiRID v1.1.1 官方页](https://www.physionet.org/content/hirid/1.1.1/)；[AmsterdamUMCdb 官方仓库](https://github.com/AmsterdamUMC/AmsterdamUMCdb)；[SICdb v1.0.8 官方页](https://www.physionet.org/content/sicdb/1.0.8/) | 无直接反证 | high | not_applicable | aligned | “公开”不等于即时可取；各库变量语义、频率和照护流程不同 |
| C3 | **[来源事实与证据推断] 单库内部随机划分不能代替外部验证。** 公共 ICU 数据在患者构成、治疗实践、记录方式和结局上存在系统差异；跨中心、跨数据库及最好跨地域验证是评估可迁移性的必要组成。 | data | supported | [Sauer et al., 公共 ICU 数据库系统比较，Critical Care 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9150442/)；[ICU 人工智能外部验证系统综述与荟萃分析，BMC Med Inform Decis Mak 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11702098/)；[Wong et al., 外部验证专有脓毒症模型，JAMA Intern Med 2021](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307) | 个别模型可在特定外部队列维持较好区分度，但不能消除总体迁移风险 | high | not_applicable | aligned | 数据库间的标签差异可能与模型迁移误差混合，须分别报告 |
| C4 | **[来源事实] 中国感染 ICU 数据可作为地域外部样本，但当前公开数据规模和记录完整性有限。** 自贡第四人民医院数据约含 2,790 例感染相关 ICU 患者，为单中心、2019–2020 年数据，且官方说明存在较多缺失和设备数据粒度限制。 | data | supported | [PhysioNet 中国感染 ICU 数据 v1.1 官方页](https://physionet.org/content/icu-infection-zigong-fourth/1.1/)；[数据描述论文，Frontiers in Public Health 2022](https://pubmed.ncbi.nlm.nih.gov/35372245/) | 无直接反证 | moderate | not_applicable | aligned | 入组以感染诊断关键词为基础；未核实是否覆盖拟定状态变量和干预时点 |
| C5 | **[来源事实] 脓毒症起点与标签细节会改变模型性能。** Sepsis-3 的电子病历实现即使仅有细微差异，也可显著改变病例识别和预测性能，因此必须预先固定感染窗口、SOFA 基线、起点和预测提前量。 | metric | single-source | [Subtle variation in Sepsis-III definitions markedly influences predictive performance, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10803347/)；可复核操作化代码见 [MIT-LCP MIMIC-IV sepsis3.sql](https://github.com/MIT-LCP/mimic-code/blob/main/mimic-iv/concepts/sepsis/sepsis3.sql) | 无直接反证 | moderate | not_applicable | aligned | 主要实证结论来自一项研究；代码实现不是临床金标准 |
| C6 | **[来源事实与证据推断] ICU 缺失模式本身携带照护信息，填补值不能当作真实生理状态。** 检查是否被开立、距上次测量的时间以及测量频率可预测病情；因此“未观测状态推断”必须区分缺失值填补与潜在状态估计，并输出不确定性。 | method | supported | [ICU 患者资料缺失信息观察研究，JMIR 2019](https://pubmed.ncbi.nlm.nih.gov/30622091/)；[多机构住院患者实验室缺失模式研究，J Biomed Inform 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10849195/)；[Che et al., GRU-D，Scientific Reports 2018](https://pubmed.ncbi.nlm.nih.gov/29666385/) | 无直接反证 | high | partially_verified | aligned | 这些来源支持缺失信息的重要性，不证明任何具体状态重建方法足够准确；第二项研究为多机构住院新冠患者，并非纯 ICU 队列 |
| C7 | **[来源事实] 脓毒症静态亚型、生命体征/体温轨迹、SOFA 轨迹和多状态病程均已有研究。** 因而“动态表型”或“轨迹预测”本身不是未被研究的主题。 | background | supported | [Seymour et al., SENECA 表型，JAMA 2019](https://jamanetwork.com/journals/jama/fullarticle/2733996)；[Bhavani et al., 体温轨迹，AJRCCM 2019](https://pubmed.ncbi.nlm.nih.gov/30789749/)；[Klouwenberg et al., 多状态 Markov 病程，Critical Care 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6909511/)；[Xu et al., SOFA 轨迹及三队列验证，Critical Care 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9250715/)；[脓毒症恶化轨迹及外部验证，npj Digital Medicine 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13187286/) | 不同研究的队列、起点、状态定义和目的不一致，尚未形成统一可迁移表示 | high | verified | aligned | 不能由代表性文献推断所有动态方法均已覆盖 |
| C8 | **[来源事实] ICU 和脓毒症领域已有状态空间、动态贝叶斯网络、强化学习和数字孪生原型。** 最近邻工作已覆盖潜在状态、状态转移、器官关系、干预预测或个体化模拟的部分组件。 | method | supported | [Raghu et al., 连续状态空间与脓毒症强化学习，PMLR 2017](https://proceedings.mlr.press/v68/raghu17a.html)；[Ghassemi et al., ICU 切换状态空间模型，KDD 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5543372/)；[De Blasi et al., 器官衰竭动态贝叶斯网络，PLOS ONE 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8081190/)；[Lal et al., 脓毒症数字孪生试点，Critical Care Explorations 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7671877/) | 数字孪生试点样本很小；不同工作并未同时完成可观测性检验、跨库验证和因果干预识别 | moderate | verified | not_applicable | 最近邻覆盖的是不同局部目标，不能据此声称已有“完整系统”或其完全不可行 |
| C9 | **[证据推断] 电子病历中的时间关联或网络权重不能自动解释为干预的因果作用。** 反馈式临床决策、适应症混杂和随时间变化的混杂会使治疗、指标与结局相互关联；因果解释需要额外设计和假设。 | method | supported | [Daniel et al., 随时间变化暴露与混杂教程，BMJ 2017](https://www.bmj.com/content/359/bmj.j4587)；[Gottesman et al., 观察性医疗强化学习评估原则](https://arxiv.org/abs/1805.12298)；[De Blasi et al., 动态贝叶斯网络研究将边解释为时间关联](https://pmc.ncbi.nlm.nih.gov/articles/PMC8081190/) | 无直接反证；随机分配可识别被分配治疗的总体效应，但不自动识别全部中介路径 | high | not_applicable | aligned | 该结论约束解释范围，不否定预测模型或探索性网络的价值 |
| C10 | **[证据推断] 原设想中的四类成功标准是不同估计任务。** 脓毒症发生、发生时间、死亡/恢复转移时间、部分观测下状态估计和未来轨迹预测应分别规定人群、时间零点、预测范围、参照标准、校准与临床用途，不能用一个总体准确率概括。 | metric | supported | [TRIPOD+AI 报告规范，BMJ 2024](https://www.bmj.com/content/385/bmj-2023-078378)；[PROBAST+AI 风险与适用性工具，BMJ 2025](https://www.bmj.com/content/388/bmj-2024-082505) | 无直接反证 | high | not_applicable | aligned | 具体主终点和可接受阈值仍需临床负责人、统计负责人和数据审计共同确定 |
| C11 | **[来源事实] ICU 预测模型在外部环境常出现性能和校准下降。** 现有外部验证综述与具体脓毒症模型验证均表明，开发集性能不能直接外推到其他医院或地区。 | implementation | supported | [ICU 人工智能外部验证综述，2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11702098/)；[Wong et al., Epic 脓毒症模型外部验证，2021](https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307) | 下降幅度随模型和队列而异，部分模型可保持可接受性能 | high | not_applicable | aligned | 外部验证失败可能同时来自病例组合、标签、测量和临床流程差异 |
| C12 | **[来源事实] EXIT-SEP 是中国多中心安慰剂对照随机试验。** 该试验在 45 家 ICU 随机分配 1,817 名脓毒症患者，比较血必净与安慰剂，主要结局为 28 天死亡率并报告组间差异。 | data | single-source | [Liu et al., EXIT-SEP, JAMA Internal Medicine 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10152378/) | 无直接反证 | high | not_applicable | partially_aligned | 论文存在不等于个体数据、代码本和逐时测量可供本项目使用；数据访问另见 C19 |
| C13 | **[来源事实] XBJ-SCAP 的疾病范围不同于一般脓毒症队列。** 该试验纳入 710 名重症社区获得性肺炎患者，主要结局为 8 天肺炎严重指数等级改善，因此只能在适当疾病与时间边界内用于补充分析。 | data | single-source | [Song et al., XBJ-SCAP, Critical Care Medicine 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6727951/) | 重症肺炎可与脓毒症重叠，但两者不能直接等同 | high | not_applicable | partially_aligned | 尚未核实其个体数据、器官指标时点与 EXIT-SEP 是否可共同建模 |
| C14 | **[来源事实与新颖性核验] EXIT-SEP 已发表基于 SENECA 四表型的事后异质性分析。** 该研究在 1,760 名患者中重现 α、β、γ、δ 表型并分析血必净效应；死亡结局的治疗×表型交互未达统计学显著。因此，泛化的“表型—血必净疗效”二次分析与既有工作明显重叠。 | background | single-source | [Post hoc analysis of EXIT-SEP by clinical phenotype, 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12257024/) | 个别亚组内结果提示差异，但不能替代正式交互检验；作者也要求进一步验证 | high | verified | aligned | 只核验到一项直接最近邻论文；更细的动态表型或时间依赖效应是否重复仍取决于变量和方案 |
| C15 | **[来源事实与证据推断] 随机分配只直接支持被分配治疗的因果比较，不自动识别中介网络；亚组差异需正式交互检验。** 中介分析仍依赖中介—结局混杂等假设，效应异质性也不能由“一个亚组显著、另一个不显著”推出。 | method | supported | [AGReMA 中介分析报告指南，JAMA 2021](https://jamanetwork.com/journals/jama/fullarticle/2784353)；[CONSORT 2025 解释与阐释：亚组分析](https://pmc.ncbi.nlm.nih.gov/articles/PMC11995452/) | 无直接反证 | high | not_applicable | aligned | 正确方法仍需结合可用时间点、缺失机制、治疗依从性和预先规定的因果问题 |
| C16 | **[来源事实] 2026 成人脓毒症指南对血必净持审慎立场。** 指南建议在未获监管批准的辖区之外不使用血必净，证据确定性极低，并指出偏倚和中国以外适用性问题。 | guideline | single-source | [Surviving Sepsis Campaign 2026, 血必净建议及证据说明](https://doi.org/10.1007/s00134-026-08361-1) | EXIT-SEP 在中国队列报告死亡率获益，但不能消除跨辖区适用性和偏倚顾虑 | high | not_applicable | partially_aligned | 指南建议针对临床使用，不等于否定合规的机制或二次研究；需核对所在辖区审批状态 |
| C17 | **[来源事实] 若开展动物验证，应遵循脓毒症模型和动物报告规范；人鼠炎症反应的可转化性证据存在冲突。** 动物实验更适合检验一个预先规定的机制或干预假设，而不是作为电子病历模型的笼统“外部验证”。 | guideline | conflicting | [MQTiPSS 脓毒症临床前研究共识，Shock 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6093828/)；[ARRIVE 2.0, PLOS Biology 2020](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000410)；[Seok et al., PNAS 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3587220/)；[Takao & Miyakawa, PNAS 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4313832/) | 两项转录组比较对人鼠相似性得出相反结论 | moderate | not_applicable | aligned | 结论依赖模型类型、感染源、支持治疗、终点和分析尺度；不能泛化为“动物均不可转化” |
| C18 | **[未核实的新颖性主张] “建立首个完整的人体脓毒症开放复杂巨系统模型”目前没有可辩护的证据基础。** 有界检索发现多个近邻组件，但既不能证明已有完全相同系统，也不能证明不存在。 | gap | unverified | 参照 C7、C8、C14 的最近邻来源；本次检索未取得可证明“首个”或“完整”的穷尽性证据 | 无法以有限检索证明不存在同类工作 | not_verified | unverified | unverified | 必须在模型对象、输入输出、状态、反馈、辨识条件和验证任务固定后再做定向引文检索；不得使用“首个”表述 |
| C19 | **[用户陈述与资源状态未核实] EXIT-SEP、XBJ-SCAP 原始数据“可能可获取”，但实际使用权、变量字典、逐时测量和跨试验可比性未被证明。** 同样，公开数据库的账户准入与所需字段覆盖尚未完成项目级核验。 | implementation | unverified | 用户输入文件中的资源陈述；公开数据库的通用访问条件见 C2 | 无数据使用协议、获批通知、数据字典或样例提取可供核验 | not_verified | not_applicable | unverified | 在资源确认前，RCT 分析和特定动态状态变量只能是条件性后续步骤 |

## Contradictions

| Issue | Sources in conflict | Current handling |
|---|---|---|
| 血必净试验结果与当前国际指南的外推态度 | EXIT-SEP 报告中国 ICU 队列的 28 天死亡率差异；2026 Surviving Sepsis Campaign 对批准辖区以外使用给出条件性反对建议，并强调极低证据确定性和适用性顾虑 | 将试验结果限定为特定中国队列的来源事实；临床外推、机制推断和其他辖区使用分别评估，不以单个 RCT 结果覆盖指南限制 |
| EXIT-SEP 表型亚组内信号与总体交互检验 | 2025 事后分析报告部分表型内差异，但治疗×表型交互未达显著；CONSORT 2025 要求以交互而非亚组内显著性比较推断异质性 | 不把亚组内显著性当作疗效异质性的证明；后续若分析须预先规定交互、连续效应修饰和多重性处理 |
| 动物炎症模型的人体可转化性 | Seok et al. 认为小鼠反应较差地模拟人类炎症；Takao & Miyakawa 以不同分析得出较高相似性 | 记录为冲突证据；只允许以明确机制、临床相似支持治疗和 MQTiPSS/ARRIVE 设计来论证具体动物实验 |
| 高密度临床数据与因果网络解释 | 公共 ICU 数据和动态模型可提供丰富时间关系；因果方法文献指出适应症混杂和时间变化混杂会破坏直接因果解释 | 将数据驱动边和权重默认解释为预测性或关联性；只有满足明确识别假设和设计时才升级为因果主张 |
| 动态模型的当前进展与“完整系统”表述 | 现有轨迹、状态空间、动态贝叶斯网络和数字孪生已覆盖多个组件，但在对象、任务与验证上不统一 | 科学缺口表述为“尚缺何种跨库、预先规定且可检验的表示与验证证据”，不表述为文献完全空白 |

## Evidence Limitations

- 本地图是面向研究设计的有界证据检索，不是按 PRISMA 注册和双人筛选完成的系统综述；不能支持穷尽性的“首次”或“无人研究”主张。
- 未取得任何候选数据库或 RCT 的个体数据，未运行队列计数、变量覆盖、时间戳一致性、缺失模式、事件率或样本量分析。
- 未核验 EXIT-SEP 与 XBJ-SCAP 的数据使用权、代码本、给药依从性、逐时实验室/生命体征及共同变量；任何联合分析均为待定。
- 当前未固定主要临床任务、时间零点、预测范围、状态定义、恢复定义、删失规则、竞争风险、外部验证层级和最低可接受性能。
- 新颖性核验以代表性近邻工作为主，未完成 Scopus/Web of Science 全引文网络、注册平台、会议论文和非英文文献的穷尽检索。
- 2026 年来源距离检索日较近；正式发表版本、勘误和后续独立验证仍需在定稿前复核。
- 专家知识尚未通过透明的遴选、结构化征询、一致性和异议记录转化为可审计的先验约束。
