---
review_id: language-assessment-r097
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh_language_original_r097
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: baseline-current-r097
input_artifact_ids:
  - idea-dossier-I01-001-v003
input_versions:
  - v003
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
reader_handoff:
  artifact_id: embedded-reader-handoff
  version: embedded
  path: null
files_read:
  - AGENTS.md
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/scan_idea_language_candidates.py
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - https://www.bmj.com/content/384/bmj-2023-074819
  - https://pubmed.ncbi.nlm.nih.gov/34463696/
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: ALA-R097-001
    severity: major
    finding_kind: terminology
    category: 核心研究对象的名称与层级
    dossier_locator:
      - "标题与摘要：第 27、31–32、39 行"
      - "主要研究问题与目标：第 60、65、71 行"
      - "方法与解释：第 85、92、95、107、224、272、287、294、300、311、345、364、370、403、416、425 行"
    current_problem: >-
      核心研究对象先后被称为“候选动态系统表征”“候选全病程表示”“候选状态表示”“候选架构”“候选系统表征”，而“复杂候选”“受限复杂候选”“准入模型”又省略了语义中心。跨学科读者无法稳定判断这些名称是同一对象、上下位对象，还是不同模型层级。
    target_state: >-
      在首次出现处用直接描述界定核心研究对象，并明确一般候选表征、简单基线和准入复杂模型之间的层级；其后每一层只保留一个名称。
    required_change_or_replacement: >-
      将核心对象统一为“覆盖脓毒症发病前、首次发病、发病后状态与结局，并联合描述患者状态、治疗行动和测量过程的候选动态系统表征”；把裸用的“复杂候选”改为“通过预设恢复判定标准后准入的复杂动态模型”，并在首次使用时说明它属于该候选表征的一种模型实现。
    content_to_preserve: >-
      保留“候选/计划”限定、全病程范围、状态—行动—测量过程分工、简单基线先行及至多一个复杂模型的设计边界。
    acceptance_test: >-
      全文检索核心对象及模型层级：标题、摘要、研究问题、目标、方法、输出和解释矩阵中的同一角色使用同一名称；任何“候选”均带有可识别的语义中心，且一般表征、基线与复杂模型的关系可由首次定义直接判断。
    term_or_phrase: 候选动态系统表征／候选全病程表示／候选架构／复杂候选
    recommended_form_or_plain_description: >-
      “覆盖脓毒症全病程并联合描述患者状态、治疗行动和测量过程的候选动态系统表征”；下位对象称“通过预设恢复判定标准后准入的复杂动态模型”。
    evidence_basis: >-
      全文内部一致性核对显示同一核心对象和下位模型使用多个没有层级说明的名称；这些是项目特定概念，采用直接描述比另造短标签更适合所声明的跨学科读者。
    first_use_definition: >-
      本研究拟构建一种候选动态系统表征，即对 ICU 患者从脓毒症发病前至结局的时间状态、状态转移、治疗行动和测量过程进行联合描述；复杂动态模型仅是通过预设恢复判定标准后才准入的一种实现。
    competing_forms_and_locators:
      - "“候选动态系统表征”：第 27、31、32、60 行"
      - "“候选全病程表示”：第 39 行"
      - "“候选状态表示”：第 65 行"
      - "“候选架构”：第 50 行"
      - "“候选系统表征/系统表征”：第 83、87、92、311 行"
      - "“复杂候选/受限复杂候选/准入复杂候选”：第 39、40、71、85、95、107、112、224、272、294、345、353、364、416、425 行"
      - "“自动降级模型/准入模型”：第 107、300 行"
  - finding_id: ALA-R097-002
    severity: major
    finding_kind: terminology
    category: 标题复合短语的修饰关系
    dossier_locator:
      - "标题：第 27、31 行"
      - "定位、目标与证据链：第 34、50、54、60、67、123、261、314、397、405 行"
    current_problem: >-
      “条件性稀疏 RCT 次要再分析”按通常句法会把“稀疏”理解为修饰 RCT，并且没有说明“条件性”究竟约束试验、数据还是分析。正文实际表达的是只有预设条件满足后，才使用 RCT 的稀疏访视数据开展次要再分析。
    target_state: >-
      让“稀疏”只修饰访视数据，让条件明确约束分析是否开展，并在标题、摘要、目标与证据链中保持同一直接表述。
    required_change_or_replacement: >-
      标题使用“计划跨数据库检验与有条件开展的 RCT 稀疏访视数据次要再分析”；首次说明写明“仅在阶段 II、试验语义和投影判定标准均满足时，才使用各 RCT 的 D7/D8 稀疏访视数据开展次要再分析”。
    content_to_preserve: >-
      保留 RCT、次要再分析、实际 D7/D8 访视、两个试验分开分析以及预设条件不满足时不进入投影分支的限制。
    acceptance_test: >-
      重新解析标题及所有短式名称时，“稀疏”只能附着于“访视数据”，“有条件开展”只能附着于“次要再分析”；全文不再出现可被理解为“稀疏 RCT”的短语。
    term_or_phrase: 条件性稀疏 RCT 次要再分析
    recommended_form_or_plain_description: 有条件开展的 RCT 稀疏访视数据次要再分析
    evidence_basis: >-
      第 54、123、261 行明确把稀疏性归于重复测量或访视；与标题及第 34、50、67、314、397、405 行的复合短语对照后，可确认现有修饰关系会产生错误读法。
    first_use_definition: >-
      仅在预设条件满足后，分别使用两项 RCT 的 D7 或 D8 稀疏访视数据开展次要再分析。
    competing_forms_and_locators:
      - "“条件性稀疏 RCT 次要再分析”：第 27、31、67、405 行"
      - "“严格条件化的稀疏 RCT 次要再分析层/稀疏 RCT 层”：第 34、50、397 行"
      - "“条件性稀疏 RCT 观测投影或独立临床状态再分析”：第 314、405 行"
      - "直接说明“重复测量稀疏/稀疏访视/稀疏 D1/D4/D7”：第 54、123、261 行"
  - finding_id: ALA-R097-003
    severity: major
    finding_kind: terminology
    category: 读者入口处的判定标准名称
    dossier_locator:
      - "完整 Idea 摘要：第 32 行"
      - "定位、结构式摘要与核心假设：第 34、39–42、66–71 行"
      - "判定标准定义：第 79–100、214–226、242–254 行"
    current_problem: >-
      “绝对模拟恢复门”“绝对恢复/假置信门”“试验语义门”“冻结观测投影门”等项目短标签在标题后最早的摘要与假设中先于实质判据出现；“门”没有指出被判断的对象、指标或失败后果，“假置信”也不能让临床、流行病学和系统辨识读者得到同一含义。
    target_state: >-
      在首次读者入口处直接说出主要判定对象和后果；R0、R1 等短标签只在完整定义之后作为后续简称。
    required_change_or_replacement: >-
      把首次短标签分别展开为“模拟中预设的状态/转移恢复与假结构控制标准”“试验随机化、访视与结局语义的核验条件”以及“冻结映射在外部数据中的测量一致性、校准和投影误差标准”；后文可在完整定义后保留 R0/R1。
    content_to_preserve: >-
      保留所有数值阈值、判定顺序、失败分支、不得用预测表现或组间差异补救失败的限制，以及表格的既定结构。
    acceptance_test: >-
      从第 32 行开始逐个检查判定短语：读者无需跳到后文即可识别被判断的科学对象、至少一个核心判据和失败后果；R0/R1 仅出现在定义之后，且定义不再依赖另一个未解释的“门”标签。
    term_or_phrase: 绝对模拟恢复门／绝对恢复与假置信门／试验语义门／冻结观测投影门
    recommended_form_or_plain_description: >-
      直接列明恢复与假结构控制、试验语义核验、测量一致性与投影误差等判定对象；定义后再使用 R0/R1 简称。
    evidence_basis: >-
      第 79–100、214–226、246–250 行提供了可以直接描述的实质判据，但第 32、34、39–42、66–71 行只给项目短标签，形成可定位的首次使用缺口。
    first_use_definition: >-
      阶段 II 只有在模拟中达到预设的状态/转移恢复和假结构控制标准，并在独立外部数据中达到预设校准与稳定性标准时才成立；RCT 分支还须核验随机化、访视和结局语义，并达到冻结映射的测量一致性与投影误差标准。
    competing_forms_and_locators:
      - "“绝对模拟恢复门/绝对恢复/假置信门”：第 32、34、39、42、66、71、85、95、107、212、265、290、293、345、353、376、381、394、403 行"
      - "“试验语义门/冻结观测投影门/投影门”：第 32、40、54、67、88、110、112、125、246、250、276、317、347、356、368、395、405、406、428 行"
      - "“资源门/审计与协议门/恢复与准入门/真正外部门”：第 83–88 行"
  - finding_id: ALA-R097-004
    severity: major
    finding_kind: terminology
    category: RCT 投影分支的对象与结局名称
    dossier_locator:
      - "摘要、预期结果与研究问题：第 32、40–42、60、67、88、110 行"
      - "映射与估计目标：第 242–252 行"
      - "证据链、输出与解释：第 276、314、317–319、347、368、383、395、405–406 行"
    current_problem: >-
      “冻结观测投影”“状态投影”“可观测代理”“投影可观测状态摘要”“投影可观测摘要”“投影摘要”交替指向潜在状态投影 P_state、由实测锚点计算的代理 P_obs，以及包含死亡/出院排序的分析结局。三个不同角色被相近短语合并，读者无法确定随机化比较的具体对象。
    target_state: >-
      分开命名潜在状态投影、试验中可计算的观测代理和最终排序结局；每个名称与公式符号、数据来源和分析角色一一对应。
    required_change_or_replacement: >-
      统一使用“潜在状态的一维投影（P_state）”“由试验实测共同锚点计算的一维观测代理（P_obs）”和“把死亡、P_obs 及存活出院按预设顺序组成的访视排序结局”；摘要与贡献陈述直接指向第三个对象，不再使用“投影可观测摘要”。
    content_to_preserve: >-
      保留冻结映射、共同锚点、SVD 构造、数值方向、D7/D8 实际访视、试验分别分析以及不验证完整潜在动力学的边界。
    acceptance_test: >-
      全文核对 P_state、P_obs 和最终排序结局：每处只承担一个角色，任何“投影/代理/摘要”均有明确修饰中心；随机化估计目标可由名称直接定位到最终排序结局。
    term_or_phrase: 投影可观测状态摘要／投影可观测摘要／状态投影／可观测代理
    recommended_form_or_plain_description: >-
      “潜在状态的一维投影（P_state）”“由试验实测锚点计算的一维观测代理（P_obs）”和“死亡—P_obs—存活出院访视排序结局”三者分开命名。
    evidence_basis: >-
      第 248、252 行公式与排序规则明确显示三个科学角色；全文一致性核对显示这些角色在摘要、证据链和解释矩阵中被多个相近短语交叉指称。
    first_use_definition: >-
      冻结观测方程先给出潜在状态的一维投影 P_state，再由试验实测共同锚点计算其一维观测代理 P_obs；随机化比较使用把死亡、P_obs 和存活出院按预设顺序组成的访视排序结局。
    competing_forms_and_locators:
      - "“冻结观测投影/观测投影”：第 32、40、60、88、110、314、395、405 行"
      - "“状态投影/可观测代理”：第 248、276 行"
      - "“投影可观测状态摘要/投影可观测摘要”：第 32、42、60、88、252、318、319、347、368、383、406 行"
      - "“投影摘要/投影可观测状态扰动估计/随机化投影摘要扰动”：第 41、67、317、383 行"
  - finding_id: ALA-R097-005
    severity: major
    finding_kind: terminology
    category: SOFA 分支排序结局的首次定义
    dossier_locator:
      - "完整 Idea 摘要与预期结果：第 32、41 行"
      - "目标与分支定义：第 67、88、110、125、252–254、276 行"
      - "证据链、输出与解释：第 317–318、347、356、369、384、395、405–406、428 行"
    current_problem: >-
      “death-ranked SOFA”在摘要首次出现时没有说明死亡、仍住院存活者和存活出院者的排序规则，后文又与“独立 SOFA”“trial-specific independent secondary clinical-state reanalysis”等名称交替。该短语不能让声明的跨学科读者判断它是 SOFA 分数、复合排序结局还是缺失值处理规则。
    target_state: >-
      首次出现即用直接中文描述结局的三个层级，并为该独立分支保留一个一致名称。
    required_change_or_replacement: >-
      使用“死亡置于最差层级、仍住院存活者按 SOFA 由高到低排序、存活出院置于最有利层级的试验特异访视排序结局”；如需简称，只能在这一定义后使用“独立 SOFA 访视排序结局”。
    content_to_preserve: >-
      保留死亡最差、存活出院最有利、仍住院者按 SOFA 排序、与阶段 II 表征独立、两个试验分开以及只作次要再分析的限制。
    acceptance_test: >-
      摘要首次出现时即可还原三个排序层级；正文、图题、摘要和结论统一使用同一已定义名称，不再出现未解释的“death-ranked SOFA”或另一个英语分支标签。
    term_or_phrase: death-ranked SOFA／独立 SOFA／trial-specific independent secondary clinical-state reanalysis
    recommended_form_or_plain_description: >-
      “死亡最差、仍住院存活者按 SOFA 排序、存活出院最有利的试验特异访视排序结局”；定义后简称“独立 SOFA 访视排序结局”。
    evidence_basis: >-
      第 254 行提供了完整排序规则；focused verification 查阅的 SOFARANK 随机试验将同类构造明确称为 ranked outcome 并直接说明死亡在最差端，支持采用显式排序描述，而不是保留未定义的复合短语（PubMed 34463696）。
    first_use_definition: >-
      若投影分支不成立，则使用与阶段 II 表征独立的试验特异访视排序结局：死亡为最差层级，仍住院存活者按 SOFA 从高到低排列，存活出院为最有利层级。
    competing_forms_and_locators:
      - "“death-ranked SOFA”：第 32、41、67、317、347、384、428 行"
      - "“独立 SOFA/独立临床状态再分析”：第 42、88、110、125、276、314、356、369、395、405 行"
      - "“trial-specific independent secondary clinical-state reanalysis/trial-specific clinical-state 再分析”：第 254、318 行"
  - finding_id: ALA-R097-006
    severity: major
    finding_kind: terminology
    category: 外部检验、可迁移性与更新的关系
    dossier_locator:
      - "标题、摘要与核心假设：第 27、31–42、50、66、71 行"
      - "外部数据库设计：第 87、98、109、134、189、228–240 行"
      - "证据链、解释与定位：第 278、306–312、346、355、365–366、370、376、382、393–397、404、427 行"
    current_problem: >-
      “跨数据库检验/验证”“真正外部检验”“未触碰”“运输/运输性”“适配后运输”“zero-update”“transport updating”并列使用，却没有稳定区分冻结模型在独立数据上的外部验证、模型性能跨场景的可迁移性，以及利用适配数据进行校准或更新。中文“运输”还会给医学读者造成日常词义干扰。
    target_state: >-
      对三个操作分别使用直接、稳定的学术名称，并把“未触碰”展开为数据未参与开发、调参或阈值选择的事实条件。
    required_change_or_replacement: >-
      使用“独立外部数据库验证（冻结模型且零更新）”“外部数据库适配后的校准/观测层更新”和“模型性能对新医院或数据库的可迁移性”；把“未触碰测试区”改为“未参与开发、模型选择、调参或阈值设定的最终外部测试区”。
    content_to_preserve: >-
      保留医院优先分区、患者不跨集合、零更新结果优先、有限更新不得替代零更新失败、最终测试数据在冻结前不可访问及失败后限制主张的设计。
    acceptance_test: >-
      全文逐处检查外部数据相关措辞：每处可明确归入冻结模型外部验证、适配后更新或可迁移性判断之一；不再使用裸露的“运输”“未触碰”或未定义的 zero-update/transport updating 来代替科学操作。
    term_or_phrase: 跨数据库检验／未触碰／运输性／zero-update／transport updating
    recommended_form_or_plain_description: >-
      “独立外部数据库验证（冻结模型且零更新）”“适配数据上的校准或观测层更新”“模型性能对新场景的可迁移性”。
    evidence_basis: >-
      全文内部对照显示这些短语分别承担验证、更新和场景适用性三个角色；focused verification 查阅的 BMJ 临床预测模型方法指南将 external validation 定义为在未参与开发的新数据中评价模型，并把 model updating 与 transportability 分开讨论（BMJ 2024;384:e074819）。
    first_use_definition: >-
      阶段 II 先在一个未参与开发、模型选择、调参或阈值设定的外部数据库测试区评价冻结模型；零更新结果用于外部验证，适配区上的校准或观测层更新另行报告，二者共同界定模型在新医院或数据库中的可迁移性。
    competing_forms_and_locators:
      - "“跨数据库检验/验证、跨库检验/验证、外部检验/验证”：第 27、31、32、34、38、42、50、66、87、109、112、240、306、376、404 行"
      - "“未触碰/untouched/真正外部”：第 32、34、39、41、66、71、87、98、109、112、134、189、230、250、306、346、358、370、376、382、404 行"
      - "“运输/运输性/外部运输/适配后运输”：第 34、50、71、238、278、355、365、366、393、394、397、404、427 行"
      - "“zero-update/zero update/transport updating”：第 98、240、250、309、310、355、365、366、382、404、427 行"
  - finding_id: ALA-R097-007
    severity: major
    finding_kind: terminology
    category: 失败后果的动作标签
    dossier_locator:
      - "摘要、定位与阶段计划：第 32、40、42、83–88、95、106–112 行"
      - "数据、模型与 RCT 后果：第 122–125、144–155、212、220–226、238、242–259、278、294、312、317–318 行"
      - "输出、解释与风险矩阵：第 329、333、345、352–358、364–369、384、405、422–430、439 行"
    current_problem: >-
      “降级/自动降级”“fallback”“stop/no-go”“弃权”被用来表示多种不同后果，包括改变时间网格、删除变量或边、改用简单模型、改换分析人群、转入独立 RCT 端点、缩小可支持主张以及完全停止端点。一个动作标签同时承担结果状态、科学操作和主张后果，尤其使候选扫描命中的条件句难以执行。
    target_state: >-
      每个条件句直接写出触发后采取的具体科学操作、保留的分析对象和不得再提出的主张；只在完整动作之后使用可选简称。
    required_change_or_replacement: >-
      按情形分别写为“改用 24 小时时间网格”“删除该边”“仅保留多状态或线性模型”“改用 FAS/mITT 并说明人群变化”“转入与阶段 II 独立的 SOFA 访视排序结局”“停止该新状态端点”或“仅报告数据库层面的结果”，不再用单独的“降级/fallback/stop/no-go”代替这些动作。
    content_to_preserve: >-
      保留每个触发条件、预设顺序、不可补救项、允许继续的最低产物、不可提出的主张，以及所有表格和列表的既定格式。
    acceptance_test: >-
      对 scanner 命中的 127 条后果候选逐条复核：每条都能从句面识别触发条件、具体动作、受影响对象和科学主张后果；全文不再存在没有直接动作说明的“降级/fallback/stop/no-go”。
    term_or_phrase: 降级／自动降级／fallback／stop／no-go／弃权
    recommended_form_or_plain_description: >-
      不设单一替换词；按每个后果分别直接写明改网格、删边、改模型、改分析人群、转独立端点、缩小主张或停止端点。
    evidence_basis: >-
      全文后果候选的功能核对显示同一词族至少承担七类不同操作；这种多义性可由 dossier 内部证据直接确定，无需外部术语来源。
    first_use_definition: >-
      当某项判定标准未满足时，正文必须直接说明是改变时间网格、删除模型成分、改用较简单模型、转入独立端点、限制可支持主张，还是停止该端点。
    competing_forms_and_locators:
      - "“降级/自动降级”：第 32、40、42、84、85、95、106、107、112、144、155、220、226、238、259、278、294、312、329、333、345、358、423、430、439 行"
      - "“fallback”：第 242、246、254、335、384、405、428 行"
      - "“stop/no-go”：第 83、118、121、242、256、310、335、349、412、437 行"
      - "“弃权”：第 41、52、108、212、225、274、294、331、345、353、354、367、381、394 行"
  - finding_id: ALA-R097-008
    severity: minor
    finding_kind: language
    category: 面向读者的内部状态词与混合语言标签
    dossier_locator:
      - "资源状态与日期后果：第 83、120–129 行"
      - "外部输出与主张支持表：第 310、383、403–410 行"
      - "最终边界：第 439 行"
    current_problem: >-
      data-access no-go、not generated、project-local derivative、stable/database-specific/abstained、projection-pass、editorial_repositioning、scientific_discovery、identity_status、preserved 和 new_idea_required 等内部状态词直接进入中文正文或自由表格单元。它们不是必须保留的机器前置元数据，也没有面向跨学科读者的自然语言定义。
    target_state: >-
      普通正文和自由表格单元使用自然中文描述证据状态、支持程度和停止边界；机器前置元数据保持原样且不计入语言修订。
    required_change_or_replacement: >-
      分别改为“数据访问条件未满足”“尚未生成”“项目内衍生材料”“稳定/数据库特异/不予解释”“仅在投影判定通过时”“编辑定位”“科学发现主张”“研究身份保持不变”和“需要另立研究问题”等直接表述。
    content_to_preserve: >-
      保留证据是否核验、是否生成、支持程度、投影分支条件及研究身份边界；不得修改 YAML 前置元数据、固定标题或 Claim-Support 表头。
    acceptance_test: >-
      只扫描普通正文和自由表格单元时，不再出现这些未定义内部状态词；对应中文表述能直接说明证据状态或科学后果，且固定脚手架与机器元数据未被改名。
  - finding_id: ALA-R097-009
    severity: minor
    finding_kind: language
    category: 长句、限定语堆叠与局部可读性
    dossier_locator:
      - "完整 Idea 摘要：第 32 行"
      - "外部支持与 RCT 方法：第 238、246、250 行"
      - "必需分析与剩余执行条件：第 335、435 行"
    current_problem: >-
      这些句子在一个语法单位中同时堆叠数据条件、时间条件、多个操作、数值判据、失败后果和否定性边界；第 32 行还连续嵌入多个未定义短标签。读者需要回读才能把条件与其后果正确配对。
    target_state: >-
      每个句子或表格单元围绕一个主要操作组织，条件与后果就近配对；完整 Idea 摘要仍保持合同要求的一句话。
    required_change_or_replacement: >-
      第 32 行保留一句话格式，但按“研究对象—阶段 II 验证—RCT 条件分支—主张边界”的平行顺序压缩；第 238、246、250、335、435 行拆成较短句或同一表格单元内的编号条件，并删除不增加判定信息的重复限定语。
    content_to_preserve: >-
      保留全部数值阈值、时间点、角色、分支、不可估计内容和主张边界；不得改变摘要的一句话基数或表格结构。
    acceptance_test: >-
      第 32 行仍为一句且四个语义段顺序清楚；其余定位处每个句子只含一个主操作，所有“若/仅当/否则/不得”均能在同一局部单位找到唯一对应的条件或后果，无数值与边界信息丢失。
unresolved_issues:
  - ALA-R097-001
  - ALA-R097-002
  - ALA-R097-003
  - ALA-R097-004
  - ALA-R097-005
  - ALA-R097-006
  - ALA-R097-007
  - ALA-R097-008
  - ALA-R097-009
---

# Language Assessment Report

**Assessment ID**: language-assessment-r097  
**Target Language**: Chinese（保留必要英文缩写、符号和正式专名）  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、医学 AI 与转化研究（跨学科）  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文语法和时态基本可靠，但标题、摘要、研究问题、主要贡献及条件后果中存在多组核心名称不一致、首次使用不可理解或修饰关系误导的问题。术语 hard gate 未通过；修订应集中于术语层级、RCT 两个分支的结局名称、外部验证操作和失败后果，不需要把文本交给全面语法重写。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 6 | borderline |
| Terminology Consistency | 3 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 4 | fail |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 未发现可无争议计数的语法错误；中文文本按逐句审阅而非机械分词，明显错误密度低于 3/500 词阈值 |
| Academic register | pass | 没有两个章节以会话语体为主；项目/软件式短标签造成的局部学术表达问题已单列，但未达到系统性非正式语体阈值 |
| Terminology coherence | fail | 核心研究对象、RCT 数据关系、RCT 两个结局对象、外部验证操作及失败后果在读者入口或解释后果中存在不一致、不可及时理解或会产生错误修饰关系的名称 |
| Tense systematic violation | pass | 全文把拟开展工作、尚未生成结果和既有文献证据区分清楚；Idea 文本使用计划性表达符合跨学科研究计划约定 |

---

## Strengths

- 计划性语气一致，摘要、资源表和预期输出反复区分“拟开展”与“已完成”，未把待验证对象写成既有结果。
- 因果、控制、数字孪生和临床推广边界表述明确，否定性限定通常有可定位的科学对象。
- 时态与语态符合 Idea dossier：既有知识用现在时或完成性表述，拟执行分析使用计划性表达。
- 表格广泛用于承载阈值、数据角色和分支条件，修订后可继续作为局部清晰度的主要支撑。
- Sepsis-3、SOFA、RCT、ICU 等面向声明读者的标准术语总体保持一致；公式符号在定义后的使用也较稳定。

---

## Specific Issues

### Chinese Academic Clarity (if applicable)

- **ALA-R097-002（major）**：第 27、31 行的“条件性稀疏 RCT”存在错误修饰读法；正文自己已表明稀疏性属于访视数据。
- **ALA-R097-007（major）**：第 83–88、220–226、242–259、422–430 行等把多种科学后果压缩为“降级/fallback/stop”，读者无法从标签本身执行分支。
- **ALA-R097-008（minor）**：第 120–129、403–410、439 行把内部状态词带入普通中文正文或自由表格单元。
- **ALA-R097-009（minor）**：第 32、238、246、250、335、435 行限定语和条件后果过度堆叠；具体操作见 frontmatter。

### Grammar & Syntax

没有达到 finding 阈值的独立语法错误。表格中的省略结构在对应列标题下可恢复，不按句子残缺计数。

### Academic Register & Tone

- **ALA-R097-008（minor）**：未定义的英语状态词和内部类别名削弱了面向研究者的自然学术表达。
- “未触碰”“封印”“清零”“挽救/救回”等项目化隐喻的主要读者影响已并入 **ALA-R097-003、006、007**；它们没有使全文转为会话语体，因此 register hard gate 仍通过。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| ALA-R097-001 | 候选动态系统表征等 | 第 27–32、39、50、60、65、71、85–112、224、272、287、294、300、311、345、364、370、403、416、425 行 | 无法判断核心对象及模型层级 | yes |
| ALA-R097-002 | 条件性稀疏 RCT 次要再分析 | 第 27、31、34、50、54、60、67、123、261、314、397、405 行 | “稀疏”可能错误修饰 RCT | yes |
| ALA-R097-003 | 绝对恢复/假置信门等 | 第 32、34、39–42、66–71、79–100、214–226、242–254 行 | 首次使用时看不到判定对象与后果 | yes |
| ALA-R097-004 | 投影可观测摘要等 | 第 32、40–42、60、67、88、110、242–252、276、314、317–319、347、368、383、395、405–406 行 | 混淆 P_state、P_obs 与最终排序结局 | yes |
| ALA-R097-005 | death-ranked SOFA 等 | 第 32、41、67、88、110、125、252–254、276、317–318、347、356、369、384、395、405–406、428 行 | 无法从首次名称还原结局结构 | yes |
| ALA-R097-006 | 外部检验/运输/zero-update 等 | 第 27–42、50、66、71、87、98、109、134、189、228–240、278、306–312、346、355、365–366、370、376、382、393–397、404、427 行 | 混淆外部验证、模型更新与可迁移性 | yes |
| ALA-R097-007 | 降级/fallback/stop/no-go/弃权 | 条件与后果候选，代表性定位为第 83–88、220–226、242–259、352–358、422–430 行 | 无法从动作标签判断具体科学操作 | yes |

### Tense & Voice Conventions

没有 finding。计划、条件和未来执行使用前瞻表达；既有数据库、论文和已知试验结果使用现在时或过去事实表述，未系统性混淆完成状态。

### Conciseness & Redundancy

- **ALA-R097-009（minor）**：少数高密度句把本可由表格或短句承载的判据再次压入长句，造成局部重复和限定语堆叠。
- 多处科学边界在不同功能章节重复出现，但本评估不决定应保留在哪一论证位置；仅要求在同一局部单位内删除近义堆叠，不改变完整限制的叙事归属。

### Readability & Flow

- **ALA-R097-001、003–007** 共同造成读者入口与后果句的主要回读负担：问题并非章节顺序，而是同一局部句中对象、判据和后果缺少稳定名称。
- **ALA-R097-009** 定位的长句需要局部重组；不建议改变 dossier 的章节功能或证据链顺序。

---

## Language Revision Priorities

1. **Terminology consistency**: 7 issues — 先冻结核心对象、两类 RCT 结局、外部验证操作和失败动作的名称及层级，再进行全文一致性核对。
2. **Reader-entry clarity**: 5 issues — 优先修订标题、第 32 行摘要、第 39–42 行结构式摘要、第 60–71 行问题与假设，使每个对象、目标量、判据和后果首次出现即可理解。
3. **Consequence clarity**: 2 issues — 把“降级/fallback/stop/no-go”逐处改成具体科学动作，并保留原触发条件和不可主张内容。
4. **Local readability**: 2 issues — 在不改变一句话摘要基数、表格格式和数值判据的前提下处理长句与限定语堆叠。

---

## Re-Assessment Status (if applicable)

不适用。本次是 Idea dossier 的全新独立基线评估，未接收、读取或比较任何既往问题清单、语言报告、分数、决定、修订稿或差异记录。

---

## Assessment Notes

- **评估边界**：只评语言、术语和局部可读性；未评价科学有效性、论证质量、新颖性、影响、可行性、期刊适配或限制应放置在哪一章节。
- **读者基线**：采用 dossier 第 33 行内嵌读者画像，即重症医学、临床流行病学、纵向统计、系统辨识、医学 AI 与转化研究共同体；未假定所有读者熟悉任一单一子领域的项目短标签。
- **候选覆盖**：只读 scanner 完整产生 356 个候选，其中读者入口 13 个、混合语言/版本/内部 token 216 个、条件后果 127 个。先完成 13/13 读者入口候选：逐句识别科学主体、操作、对象或目标量、判据与后果，并逐个把紧凑短语判为标准、已定义、直接描述或需 focused verification；之后完成 216/216 token 与 127/127 后果候选的全文核对。未抽样、未提前停止，也未把固定 research-idea.v3 脚手架、公式符号、参考文献原题或机器前置元数据当作 finding。
- **术语复核**：仅对已触发的外部验证/可迁移性关系和 death-ranked SOFA 命名做 focused verification；使用 BMJ 临床预测模型外部验证方法文章与 PubMed 34463696 的 SOFARANK 随机试验记录。没有建立或持久化术语表、扫描结果或证据包。
- **截断与补读**：首次读取两份中文 AGENTS.md 时控制台发生乱码，随后以 UTF-8 完整重读；术语、模板、scanner 与 validator 的合并读取发生一次工具层截断，定位在 scanner 中段，随后按第 1–160 行和第 161 行至文件末尾完整补读，并单独完整重读 validator。dossier 按第 1–60、61–120、121–180、181–240、241–300、301–360、361–420、421–480 行读取，八段均无截断；完整 scanner 运行输出也无截断。
- **输入隔离**：除 frontmatter 列出的开发说明、指定 dossier 和两项 focused verification 来源外，未读取任何 narrative/language report、repair plan、writer brief、protected register、修订稿、delta、preflight、evaluation、workflow state、portfolio、测试脚本或预期答案。
- **源文件状态**：未修改 dossier 或 Skill 源码；本次只新增本 Language Assessment Report。
