---
review_id: language-assessment-I01-001-r129
reviewer_skill: academic-language-assessor
reviewer_instance_id: academic-language-assessor-r129c
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r129
input_artifact_ids:
  - idea-dossier-I01-001-v056
input_versions:
  - v056
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v056
  version: v056
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/idea-dossier-v056.md
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
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/english-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/common-l1-interference-patterns.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/idea-dossier-v056.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
coverage_receipt:
  reader_entry:
    status: completed
    reviewed_count: 12
    basis: "逐一复核扫描器界定的标题、摘要、受众、定位、研究问题、核心假设和贡献入口单元，未在发现首个问题后停止。"
  core_scientific_role:
    status: completed
    reviewed_count: 16
    basis: "复核全文实际出现的 16 类科学角色在标题、正文、表格和解释语句中的读者可见名称；未添加文中不存在的角色。"
  terminology_concordance:
    status: completed
    reviewed_count: 8
    basis: "对 8 个经上下文触发的概念簇追踪全部相关形式与位置；仅保留下列已确认问题。"
  local_language:
    status: completed
    reviewed_count: 15
    basis: "完整复核 15 个二级章节及其 36 个三级单元中的正文、列表、表格、公式说明和参考文献，覆盖语法、语域、时态、局部清晰度与局部重复。"
findings:
  - finding_id: ALA-001
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: central-study-object
    normalized_locator: title-summary-question-and-model-path
    failure_mode: opaque-and-shifting-core-name
    fingerprint: meso|central-study-object|title-summary-question-and-model-path|opaque-and-shifting-core-name
    category: "术语一致性；核心科学角色命名；复合修饰语附着"
    dossier_locator: >-
      H1 与 Title（第 33、37 行）；One-sentence complete-Idea summary（第 38 行）；
      Structured abstract 的 Objective and hypothesis（第 45 行）与 Approach（第 46 行）；
      Primary research question（第 76 行）；Objectives 2–3（第 81–82 行）；
      模型准则、证据输出与解释语句（第 107、117、129、246、250、255–256、326–327、347、392、400、411、417、461、467、469、496 行）。
    current_problem: >-
      核心研究对象在“脓毒症全病程候选动态系统表征”“知识约束、不确定性感知候选动态系统表征”
      “候选表征”“候选状态表征”“候选结构”“复杂候选”和“最小全病程候选表征”之间切换。
      标题和摘要中的长串前置修饰语没有说明“候选”究竟修饰模型、潜在状态表征还是整套分析，
      “不确定性感知”又以拟人化短语代替具体动作；跨学科读者可能把中央研究对象误读为一个既定模型类别、
      一组输出或整个研究方案。
    target_state: >-
      标题和首次摘要用直接措辞说明研究对象、时间与临床范围、先验约束及不确定性处理；
      后文分别用有明确中心词的名称指代总体表征、实际拟合的复杂模型和待检验结构，不让一个简称承担多个角色。
    required_change_or_replacement: >-
      将标题和首次摘要的中心名改为直接描述，例如“用于描述重症监护期间脓毒症发病前风险、
      首次发病、发病后状态及其转移的候选动态表征”；把“知识约束、不确定性感知”改为
      “受文献和专家先验约束，并报告估计与预测不确定性”。后文在指实际拟合对象时使用
      “候选复杂模型”，在指其输出时使用“潜在状态表征”，在指边或依赖时明确写“待检验结构关系”；
      不再使用无中心词的“复杂候选”或让“候选结构”兼指模型与结构关系。
    content_to_preserve: >-
      保留计划研究状态、24 个月阶段 I–II、重症监护范围内从未发病在险时段至发病后结局的覆盖、
      文献与专家先验、对不确定性的报告、简单模型备选路线，以及预测或生成表征的非因果解释边界。
    acceptance_test: >-
      标题仍为一个标题，摘要仍为一个句子，研究问题仍为一个问句；三处均能在不阅读后续方法的情况下
      识别研究对象及范围。全文检索每一种“候选”用法后，模型、表征输出和结构关系各有唯一且带中心词的名称，
      不再出现“复杂候选”，且所有替换后的修饰语均只附着于预期对象。
    term_or_phrase: "脓毒症全病程候选动态系统表征；知识约束、不确定性感知候选动态系统表征；复杂候选"
    recommended_form_or_plain_description: >-
      用“用于描述重症监护期间脓毒症发病前风险、首次发病、发病后状态及其转移的候选动态表征”直接说明总体对象；
      按具体角色分别使用“候选复杂模型”“潜在状态表征”和“待检验结构关系”。
    evidence_basis: >-
      文内第 230–232 行把对象具体写为患者—时间状态、状态转移及其联合预测或生成分布，
      而第 107、117、246、250、255–256 行把“复杂候选”用于实际模型选择。
      这些内部定义足以支持直接角色描述；不需要另造或外部验证新的简称。
    first_use_definition: >-
      “本研究拟构建一种候选动态表征，用于描述重症监护期间脓毒症发病前风险、首次发病、发病后状态及其转移；
      该表征受文献和专家先验约束，并报告估计与预测不确定性。”
    competing_forms_and_locators:
      - "“脓毒症全病程候选动态系统表征”——H1、Title 与 Primary research question（第 33、37、76 行）"
      - "“知识约束、不确定性感知候选动态系统表征”——One-sentence complete-Idea summary（第 38 行）"
      - "“全病程候选表征”与“候选表征”——Structured abstract、Background/Gap/Significance 与 Evidence chains（第 40、44–45、62、66、341 行）"
      - "“候选状态表征”与“候选结构”——Primary research question 和 Objectives 2–3（第 76、81–82 行）"
      - "“复杂候选”“复杂切换或非线性候选”与“受限复杂候选”——Approach、时间节点、方法、输出和停止条件（第 46、89、107、117、129、134、150、246、250、255–256、326–327、347、392、400、411、461、467、469、496 行）"
      - "“最小全病程候选表征”——Interpretation matrix（第 417 行）"
  - finding_id: ALA-002
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: validation-strata-and-frozen-model-test
    normalized_locator: abstract-objective-through-cross-database-methods
    failure_mode: validation-labels-support-wrong-setting-reading
    fingerprint: meso|validation-strata-and-frozen-model-test|abstract-objective-through-cross-database-methods|validation-labels-support-wrong-setting-reading
    category: "术语一致性；验证场景命名；修饰语附着"
    dossier_locator: >-
      Structured abstract 的 Objective and hypothesis 与 Approach（第 45–46 行）；Expected result 与 Contribution（第 47–48 行）；
      Objective 3（第 82 行）；时间节点与工作包（第 109、122、130–131、134 行）；
      Hospital-primary cross-database validation（第 261–280 行）；试验映射判定（第 296 行）；
      Evidence chains、Planned outputs、Interpretation matrix、Contribution 和 Limitations（第 352–360、393、402、412–413、423、429、450、480、494 行）。
    current_problem: >-
      “时间外”“医院外”“未触碰数据库检验”“未触碰跨数据库检验”“未触碰测试区”和“不更新外部检验”
      被用来命名三个不同验证层次。“医院外”在临床中文中可被读成院前或院外场景；“不更新”没有在首次出现时说明
      不更新的是模型参数；“未触碰”是口语化隐喻。读者因此可能把按医院留出、第二数据库隔离测试和冻结模型外部验证
      误认为同一操作，或误判验证人群所在场景。
    target_state: >-
      对按时间留出、按医院留出和第二数据库隔离测试三个层次使用互不重叠的直接名称，
      并在首次提到主要外部验证时明确测试数据未参与开发且模型不进行重新校准或参数更新。
    required_change_or_replacement: >-
      将“时间外”统一改为“按时间留出的验证”，将“医院外”统一改为“按医院留出的验证”；
      首次出现主要外部检验时写成“在第二数据库中未参与开发的隔离测试集上，对冻结模型进行不含重新校准或参数更新的外部验证”，
      后文统一简称“冻结模型外部验证”。保留并分别命名“仅校准适配”“仅观测层适配”和“全模型重拟合”。
    content_to_preserve: >-
      保留时间、医院和数据库三个层次，医院优先分区，测试资料隔离，冻结模型不更新作为主要外部证据，
      以及三种后续适配或重拟合操作与主要证据分开报告的关系。
    acceptance_test: >-
      结构化摘要首次列出三种验证时即能区分其数据划分与模型更新状态；全文不再以“医院外”表示留出医院，
      不再使用“未触碰”修饰数据或结果，也不再出现未说明更新对象的“不更新外部检验”。
      全文核对确认三种验证层次与三种后续操作没有被合并或互换。
    term_or_phrase: "时间外；医院外；未触碰数据库检验；未触碰跨数据库检验；不更新外部检验"
    recommended_form_or_plain_description: >-
      “按时间留出的验证”“按医院留出的验证”，以及“在第二数据库的隔离测试集上对冻结模型进行不含重新校准或参数更新的外部验证”；
      后者可在定义后简称“冻结模型外部验证”。
    evidence_basis: >-
      第 261–280 行明确说明医院分区、测试资料隔离、冻结模型和四种更新操作，
      因而可用文内已固定的对象和动作替代容易误读的简称，无须外部术语来源。
    first_use_definition: >-
      “验证包括按时间留出的验证、按医院留出的验证，以及在第二数据库中未参与开发的隔离测试集上对冻结模型进行不含重新校准或参数更新的外部验证。”
    competing_forms_and_locators:
      - "“时间外”——Structured abstract、WP3、Evidence chain 与 Planned outputs（第 45–46、130、352–353、393 行）"
      - "“医院外”——Structured abstract、WP3、Evidence chain 与 Planned outputs（第 45–46、130、352、393 行）"
      - "“未触碰数据库检验”与“未触碰外部数据库”——Structured abstract 与 Core hypothesis（第 45、89 行）"
      - "“未触碰跨数据库结果/检验/资料”——Structured abstract、WP4、minimum route、outputs 与 contribution（第 47–48、131、134、393、423 行）"
      - "“未触碰最终测试区/未触碰测试区”——Objective 3、时间节点、数据库角色、任务标准、医院分区与 implementation（第 82、109、156、211、263、329 行）"
      - "“不更新外部检验”——时间节点、成功定义、方法、证据链、解释、贡献与限制（第 109、122、275、280、296、329、360、402、412–413、429、450、480、494 行）"
      - "“冻结模型的跨数据库检验/冻结后的可恢复不变量在未触碰测试资料中稳定”——Structured abstract 与 contribution ladder（第 46、429 行）"
  - finding_id: ALA-003
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: simulation-recovery-and-reconstruction-outputs
    normalized_locator: reader-entry-through-recovery-and-diagnostic-sections
    failure_mode: shared-recovery-root-collapses-distinct-operations
    fingerprint: meso|simulation-recovery-and-reconstruction-outputs|reader-entry-through-recovery-and-diagnostic-sections|shared-recovery-root-collapses-distinct-operations
    category: "术语一致性；科学对象与评估操作区分"
    dossier_locator: >-
      One-sentence summary 与 Structured abstract（第 38、44–48 行）；Objectives 2–3 与 Core hypothesis（第 81–82、89 行）；
      时间节点和 WP2–WP3（第 107、129–130 行）；Observational target 与 simulation recovery（第 232、236–259 行）；
      Secondary representation diagnostics（第 282–284 行）；Evidence chains、outputs、stop criteria、contribution 与 limitations（第 343–348、350–354、392、400、423、428–429、478 行）。
    current_problem: >-
      “模拟重建”“绝对恢复”“绝对模拟恢复”“可恢复性检查”“可恢复不变量”和“伪遮蔽重建诊断”共享“恢复/重建”词根，
      但分别指模拟中对潜在状态或结构的恢复评估、按预设绝对阈值作判定、可跨重参数化解释的目标量，
      以及对原已测生理值的遮蔽重建。后文虽能消除歧义，摘要和目标中的首次使用仍增加不必要的回读。
    target_state: >-
      每一术语直接写出被评估或被重建的对象，并把判定标准、目标量和次要诊断分开命名。
    required_change_or_replacement: >-
      对模拟部分统一写“模拟中的潜在状态与结构恢复评估（按预设绝对阈值判定）”；
      将“可恢复不变量”首次改为“在允许重参数化下保持一致且经模拟可恢复的目标量”，定义后如保留简称须保持单一角色；
      将“伪遮蔽重建诊断”写为“遮蔽原已测生理值后的重建误差诊断”。
    content_to_preserve: >-
      保留模拟机制、绝对阈值、允许的重参数化、状态占用率与转移概率等目标量，
      以及次要诊断只遮蔽原已测值且不改变主要判定的边界。
    acceptance_test: >-
      从摘要到方法逐一检索“恢复”和“重建”，每次出现都能从同一句识别具体对象与操作；
      模拟恢复评估、可解释目标量和遮蔽值重建诊断使用三个互不混用的名称，且全文一致。
    term_or_phrase: "模拟重建；绝对恢复；绝对模拟恢复；可恢复不变量；伪遮蔽重建诊断"
    recommended_form_or_plain_description: >-
      “模拟中的潜在状态与结构恢复评估（按预设绝对阈值判定）”；
      “在允许重参数化下保持一致且经模拟可恢复的目标量”；
      “遮蔽原已测生理值后的重建误差诊断”。
    evidence_basis: >-
      第 232、236–259 行明确模拟恢复对象与标准，第 284 行明确遮蔽重建只作用于原已测生理值；
      文内信息足以直接区分三种科学角色。
    first_use_definition: >-
      “模拟中的潜在状态与结构恢复评估，是指在预设生成机制下检验指定状态量和结构关系能否达到预先固定的绝对阈值。”
    competing_forms_and_locators:
      - "“模拟重建”——summary、Structured abstract、resource status 与 limitations（第 38、44、47、150、459、481 行）"
      - "“绝对恢复”与“绝对模拟恢复”——Approach、Objective 3、时间节点、WP2、evidence chains、outputs、stop criteria、contribution 和 assumptions（第 46、82、89、107、129、134、346、392、400、423、428、440、467、469 行）"
      - "“可恢复性检查”与“可恢复不变量”——Structured abstract、Rationale、Objectives、Core hypothesis、methods、evidence chains、contribution 与 limitations（第 45、48、70、81、89、232、256、348、423、429、478 行）"
      - "“伪遮蔽重建诊断”——Expected result、Objective 3、WP3、Secondary diagnostics 与 Evidence chain（第 47、82、130、284、353–354 行）"
  - finding_id: ALA-004
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: conditional-trial-visit-outcomes
    normalized_locator: research-question-objective-and-trial-analysis
    failure_mode: umbrella-label-blurs-two-distinct-outcome-roles
    fingerprint: meso|conditional-trial-visit-outcomes|research-question-objective-and-trial-analysis|umbrella-label-blurs-two-distinct-outcome-roles
    category: "术语一致性；次要结局角色命名；中英文简称衔接"
    dossier_locator: >-
      Primary research question 与 Objective 4（第 76、83 行）；试验观测映射和独立分析（第 286–317 行）；
      Evidence chain、Planned outputs、Interpretation matrix、Contribution ladder 与 Limitations（第 364–369、394、403–404、415–416、430、441、483 行）。
    current_problem: >-
      首次出现的“实际访视临床状态”把两个互斥分支统称为临床状态：一个是由死亡、一维可观测代理和存活出院排序的访视有序结局，
      另一个才是与阶段 II 表征独立的 SOFA 有序临床状态结局。后文的“新访视结局”“主要状态端点”和“次要访视结局”
      继续作为宽泛简称，可能使读者把可观测代理构成的结局误作直接临床状态，或把两个分支误作并列分析。
    target_state: >-
      使用一个明确的上位名称，并为两个互斥分支保留各自唯一名称；只把 SOFA 分支称为“临床状态结局”。
    required_change_or_replacement: >-
      首次改写为“按试验分别比较预先指定的访视有序结局”；紧接着说明该结局按资格条件采用两个互斥定义：
      “死亡—可观测代理—存活出院有序结局”或“独立 SOFA 有序临床状态结局”。
      全文以“访视有序结局”作上位名称，删除“实际访视临床状态”和未指明分支的“主要状态端点”。
    content_to_preserve: >-
      保留阶段 II 达标这一前置条件、两项试验分开分析、两个分支互斥、各自的排序规则、
      分层标准化概率指数及并列各计半分，以及这些结果不验证阶段 II 潜在动力学的边界。
    acceptance_test: >-
      研究问题仍为一个问句；读者在 Objective 4 结束前能识别上位结局及两种互斥定义。
      全文检索确认代理构成的结局从未被简称为“临床状态”，SOFA 分支始终带“SOFA”，
      且“主要状态端点”均被替换为具体分支名或明确上位名。
    term_or_phrase: "实际访视临床状态；新访视结局；主要状态端点；次要访视结局"
    recommended_form_or_plain_description: >-
      上位名称用“访视有序结局”；两个分支分别用“死亡—可观测代理—存活出院有序结局”
      和“独立 SOFA 有序临床状态结局”。
    evidence_basis: >-
      第 298 行定义代理构成的有序结局，第 308 行定义独立 SOFA 结局，第 403、415–416、483 行说明两者解释边界；
      这些文内定义支持功能性分名，无须选择新的估计目标。
    first_use_definition: >-
      “随机试验阶段按试验分别比较访视有序结局；该结局根据预设资格条件采用死亡—可观测代理—存活出院有序结局，
      或采用与阶段 II 表征独立的 SOFA 有序临床状态结局。”
    competing_forms_and_locators:
      - "“实际访视临床状态”——Primary research question 与 Objective 4（第 76、83 行）"
      - "“新访视结局”与“新的访视结局分析”——trial analysis 与 stop statements（第 288、290、306、310、314–315、394、497 行）"
      - "“由死亡、一维可观测代理和存活出院共同排序的访视结局”——trial analysis、table、stop criterion、interpretation 与 limitation（第 298、314、403、415、483 行）"
      - "“独立的 SOFA 有序临床状态端点”——trial analysis、table、stop criterion、interpretation 与 limitation（第 298、308、314、403、416、483 行）"
      - "“主要状态端点”——trial table（第 314 行）"
      - "“次要访视结局/实际访视有序结局”——Evidence chain、Planned outputs、Contribution ladder 与 trial formula（第 300、368、394、430 行）"
  - finding_id: ALA-005
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: event-time-and-information-availability
    normalized_locator: abstract-objective-protocol-and-evidence-chain
    failure_mode: clock-metaphor-precedes-direct-definition
    fingerprint: meso|event-time-and-information-availability|abstract-objective-protocol-and-evidence-chain|clock-metaphor-precedes-direct-definition
    category: "术语首次定义；隐喻；跨学科可读性"
    dossier_locator: >-
      Expected result（第 47 行）；Rationale（第 70 行）；Objective 1（第 80 行）；WP1（第 128 行）；
      variable roles 与 primary-task protocol（第 186、202–203 行）；Evidence chain、required analyses、planned outputs 与 closest-work comparison（第 339、376、390、437 行）。
    current_problem: >-
      “双时钟协议”在摘要入口先于直接定义出现，后文又有“两条时钟”“可追溯时钟”“标签可用性时钟”和“信息可用时钟”。
      “时钟”是项目内隐喻，不能在首次使用时让临床、统计和工程读者确定它指两个时间变量、两个时间轴还是两个计算过程；
      第 70 与 202–203 行才给出实际含义。
    target_state: >-
      首次使用即写出“临床事件时刻”和“信息可用时刻”两个对象；如需简称，只使用一个不会改变对象类型的短语。
    required_change_or_replacement: >-
      将首次“标签与双时钟协议”改为“标签、临床事件时刻与信息可用时刻协议”；
      后文统一使用“两类时间记录”或直接重复两个标准名称，删除“双时钟”“可追溯时钟”和“标签可用性时钟”。
    content_to_preserve: >-
      保留临床事件发生时刻与信息在源系统中可用时刻的区别、标签形成规则，以及防止未来信息回填的功能。
    acceptance_test: >-
      摘要首次出现时即给出两个完整名称；全文检索不再出现“时钟”隐喻，
      且每一处时间规则都能明确指向临床事件时刻、信息可用时刻或二者。
    term_or_phrase: "双时钟；两条时钟；可追溯时钟；标签可用性时钟；信息可用时钟"
    recommended_form_or_plain_description: >-
      “临床事件时刻和信息可用时刻”；需要上位短语时使用“两类时间记录”。
    evidence_basis: >-
      第 70 行直接给出两个时间对象，第 202–203 行分别规定其计算与使用；
      文内定义足以替代隐喻性短语。
    first_use_definition: >-
      “方案分别记录临床事件发生时刻和相关信息在源系统中可用的时刻，并只使用标志时点前已经可用的信息。”
    competing_forms_and_locators:
      - "“双时钟协议/双时钟/信息可用双时钟标签”——第 47、128、339、390、437 行"
      - "“两条时钟”——Rationale（第 70 行）"
      - "“可追溯时钟”与“标签可用性时钟”——Objective 1（第 80 行）"
      - "“信息可用时钟”——variable roles、primary-task protocol 与 required analyses（第 186、203、376 行）"
  - finding_id: ALA-006
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: model-selection-and-stop-consequences
    normalized_locator: milestones-recovery-output-and-risk-sections
    failure_mode: project-workflow-metaphors-replace-scientific-actions
    fingerprint: meso|model-selection-and-stop-consequences|milestones-recovery-output-and-risk-sections|project-workflow-metaphors-replace-scientific-actions
    category: "学术语域；项目流程式措辞；隐喻与局部重复"
    dossier_locator: >-
      Positioning and contribution frame（第 40 行）；Objectives 后的交付表述（第 85 行）；
      时间节点与 success definition（第 105、107、114、117 行）；simulation criteria（第 246、250、255–256 行）；
      implementation、evidence outputs 与 stop criteria（第 327、332、347、392、400、405 行）；
      contribution 与 risk table（第 423、467、493、496 行）。
    current_problem: >-
      “模型准入”“晋级/不晋级”“淘汰复杂候选”“终止复杂扩张”“封存简单表征”“进入完成状态”
      把科学判定写成项目流程或竞赛隐喻；“可证伪的分析治理”“方法治理价值”和“高水平论文”
      则是含义宽泛或带评价色彩的标签。相同的“未达到标准、停止解释或不晋级决定及原因”还在多个输出位置近似重复。
    target_state: >-
      每个触发条件后直接说明继续分析、停止分析、改用何种模型、限制何种解释或记录何种未完成结果；
      贡献和交付使用可观察、可核查的科学产物名称。
    required_change_or_replacement: >-
      分别改为“满足标准后才进入后续复杂模型分析”“停止复杂模型分析并改用预设简单模型”
      “保留并报告简单模型结果”“将相应阶段记为未完成”；将“分析/方法治理”改为
      “预设且可核查的分析、判定与停止规则”，将“高水平论文”改为“同行评议研究论文”。
      对重复的后果短语保留各处必要的触发条件，但用该处具体科学后果替代整串模板化表述。
    content_to_preserve: >-
      保留所有预设阈值、停止条件、模型简化路径、负向结果记录、责任人确认、论文交付方向，
      以及不同章节中确有必要的局部后果陈述。
    acceptance_test: >-
      全文检索不再出现“晋级”“不晋级”“淘汰”“复杂扩张”“封存”或“进入完成状态”；
      每个原位置均明确写出科学动作或解释后果。贡献和交付语句不再以“治理”或“高水平”作为未定义的价值判断，
      且重复后果短语不再逐字复现。
  - finding_id: ALA-007
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: recovery-and-trial-criteria
    normalized_locator: simulation-definition-and-trial-mapping-criteria
    failure_mode: nested-conditions-and-enumerations-obscure-local-relations
    fingerprint: meso|recovery-and-trial-criteria|simulation-definition-and-trial-mapping-criteria|nested-conditions-and-enumerations-obscure-local-relations
    category: "局部可读性；限定语堆叠；并列关系"
    dossier_locator: >-
      Absolute simulation and semi-synthetic recovery criteria（第 240、246、250 行）；
      试验观测映射和独立分析的忠实度判定、概率指数解释与确认要求（第 296、304、306 行）；
      trial-specific table 的 EXIT-SEP 与 XBJ-SCAP 两行（第 314–315 行）。
    current_problem: >-
      多个句子或表格单元同时承载对象定义、五项以上阈值、例外、时间条件和失败后果，
      并连续使用分号与嵌套修饰语。目标读者能够恢复含义，但必须反复确认哪个阈值属于哪个对象、
      哪个条件触发哪个后果；第 296 行尤其把外部忠实度与试验资料内检查置于同一长段。
    target_state: >-
      每个局部单元先给出被判定对象，再以平行结构列出标准，最后单独说明失败后果；
      数学符号、阈值、方向和表格行列关系保持不变。
    required_change_or_replacement: >-
      将第 240、246、296、304、306 行按“对象—计算—标准—后果”拆成短句或项目列表；
      第 296 行把第二数据库忠实度标准与试验资料内可计算性检查分为两个段落。
      第 314–315 行保留原表格结构，但在单元格内用编号或显式平行分句分别呈现人群、缺失处理、敏感性分析和停止规则。
    content_to_preserve: >-
      保留所有公式、数值阈值、符号方向、随机化层、缺失处理、分支条件和停止后果，
      不改变表格行数、列数或任何估计目标。
    acceptance_test: >-
      每个修改后的句子或表格分句只承担一个主要判定关系；读者无需跨越另一个阈值或例外即可找到对应对象和后果。
      逐项核对原公式、阈值、方向、分支条件及表格结构全部保留。
unresolved_issues:
  - ALA-001
  - ALA-002
  - ALA-003
  - ALA-004
  - ALA-005
  - ALA-006
  - ALA-007
---

# Language Assessment Report

Use logical artifact identity (`artifact_id`, `version`, and `path`) and
`files_read` for provenance. Do not add SHA, content-hash, or digest fields.
For `complete_idea_dossier`, the dossier reference and reader handoff are
required. A file-backed handoff must occur in `files_read`; an embedded handoff
uses `path: null` and is not added as a fictitious file or input artifact.
Validate this file with `scripts/validate_language_assessment.py` before handoff.
For a completed `complete_idea_dossier` assessment, all four coverage receipts
use `status: completed`; this records coverage rather than language quality. Use
bounded counts and a concise basis; do not list every term or create a
persistent terminology inventory.
Omit `coverage_receipt` from a clarification or independence stop report.

**Assessment ID**: language-assessment-I01-001-r129
**Target Language**: Chinese（含英文数据库名、方法名、缩写与数学符号）
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识与医学人工智能
**Target Journal**: 未指定
**Scope**: complete_idea_dossier
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 7 | pass |
| Terminology Consistency | 5 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 未发现明确语法错误，观察值为 0/500 个等量词项，低于阈值 |
| Academic register | pass | 无章节以会话体为主；项目流程式隐喻虽反复出现，但未达到两个章节系统性口语化的阈值 |
| Terminology coherence | fail | 2 个核心概念簇在读者入口支持错误或不确定解读：中央研究对象与三层验证场景；适用 Idea 首次定义和读者可及性条款 |
| Tense systematic violation | pass | 0 个章节存在系统性时态冲突；计划、定义和既有证据的时间状态保持区分 |

---

## Strengths

- 全文持续使用计划性表达，并反复区分待生成结果与现成结果；没有通过时态把研究设想写成已完成研究。
- “共同生理锚点—锚点观测值—锚点预测值”在结构化摘要首次出现时给出功能性定义，后文的数学符号与中文角色基本一致。
- SOFA、恰当评分规则、Brier 分数和 mITT 均在首次相关使用处给出中文说明或明确对应关系；英文数据库名、单位、公式符号与文献题名总体稳定。
- 预测、生成表征、观察性关系和因果作用的措辞边界清楚，语气总体正式且没有系统性口语表达。

---

## Specific Issues

### Chinese Academic Clarity (if applicable)

- **ALA-001、ALA-002（major）**：标题、摘要和研究问题中的复合中心词与验证修饰语会支持错误的对象或场景解读；完整替换和保留项见 frontmatter。
- **ALA-005、ALA-006（minor）**：“时钟”“未触碰”“晋级”“淘汰”“封存”和“治理”等隐喻增加跨学科读者的转换负担。
- **ALA-007（minor）**：模拟与试验判定段落的限定语和阈值堆叠削弱局部可读性，但具体对象仍可由邻近文本恢复。

### Grammar & Syntax

未发现达到可执行 finding 程度的明确语法错误。ALA-007 属于句法负荷与局部组织问题，而不是主谓、成分残缺或修饰语悬垂等明确语法错误。

### Academic Register & Tone

ALA-006 记录项目流程式和评价式词语。其余正文保持正式科学语域；没有缩略口语、感叹、读者直呼或结果段修辞问句。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| ALA-001 | 脓毒症全病程候选动态系统表征；复杂候选 | 标题、摘要、研究问题及模型路径 | 无法稳定判断简称指模型、表征输出还是分析整体 | yes |
| ALA-002 | 时间外；医院外；未触碰；不更新外部检验 | 摘要至跨数据库方法与解释 | 可能误判验证场景、数据隔离或模型更新状态 | yes |
| ALA-003 | 模拟重建；绝对恢复；可恢复不变量；伪遮蔽重建 | 摘要至恢复准则与次要诊断 | 多种不同对象共享同一词根，需回读方法才能分辨 | yes |
| ALA-004 | 实际访视临床状态；主要状态端点 | 研究问题、Objective 4 与试验分析 | 可能把代理构成结局误作直接临床状态或合并两个互斥分支 | yes |
| ALA-005 | 双时钟及其变体 | 摘要、Objective 1 与时间协议 | 首次出现时无法确认隐喻对应的两个时间对象 | yes |

### Tense & Voice Conventions

无可执行问题。作为研究设想，未来或计划性动作、当前定义和既有文献事实之间的时态关系一致；中文主动与无主句也未造成行动者混淆。

### Conciseness & Redundancy

ALA-006 覆盖多个章节近似复现的后果模板，ALA-007 覆盖单句内过多条件和阈值的堆叠。此判断只涉及词语与局部句法重复，不决定哪个章节保留完整限制或停止条件。

### Readability & Flow

ALA-007 是主要局部可读性问题；ALA-001 与 ALA-002 还使标题、摘要和研究问题的首次阅读需要回查方法定义。未评价章节顺序、五段推理关系或跨章节论证安排。

---

## Language Revision Priorities

1. **核心科学角色与验证术语**：2 个 major findings — 先直接命名中央对象和三层验证场景，再统一全文简称。
2. **相邻科学角色的术语分离**：3 个 minor findings — 分开模拟恢复、遮蔽值重建、两类试验访视结局和两个时间对象。
3. **学术语域与局部可读性**：2 个 minor findings — 以具体科学动作替换项目流程式隐喻，并把密集判定语句改成平行短句或单元格内编号。

---

## Re-Assessment Status (if applicable)

不适用。本次为完整 Idea dossier 的全新独立评估，未接收既往问题清单、分数、决定、版本文本或修订差异。

---

## Assessment Notes

本报告只判断语言。未评价论证质量、方法正确性、新颖性、影响、可行性或期刊适配，也未编辑源 dossier。
读者基线采用 dossier 内嵌的重症医学、临床流行病学、纵向统计、系统辨识、医学人工智能与转化研究共同体；未假定所有读者熟悉项目自定义简称。
研究构想契约固定的 15 个二级标题、5 个推理标题、section-1 与结构化摘要字段、Evidence chain 字段和 Claim-Support 表头均未评分、翻译或列为问题。
英文专名、数据库名、数学符号和参考文献题名按其科学功能检查；固定元数据中的英文不作为中英文不一致证据。
