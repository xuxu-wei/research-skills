---
review_id: language-assessment-I01-001-v050-r104
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-academic-language-assessor-r104
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r104
input_artifact_ids:
  - idea-dossier-I01-001-v050
input_versions:
  - v050
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v050
  version: v050
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/idea-dossier-v050.md
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
  - research-skills-openai/skills/academic-language-assessor/references/common-l1-interference-patterns.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/scan_idea_language_candidates.py
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/idea-dossier-v050.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
coverage_receipt:
  reader_entry:
    status: completed
    reviewed_count: 12
    basis: H1、Title、完整 Idea 单句摘要、受众与定位、结构式摘要五项、主要研究问题和核心假设均逐句审读至句末。
  core_scientific_role:
    status: completed
    reviewed_count: 10
    basis: 覆盖研究对象、两项主要任务、模拟与外部检验、模型更新、失败输出、条件性试验延伸及贡献等实际出现的角色；未要求不存在的角色。
  terminology_concordance:
    status: completed
    reviewed_count: 6
    basis: 对普通阅读触发的六个概念群完成全篇中文、英文和缩写一致性核对；未保留完整术语清单。
  local_language:
    status: completed
    reviewed_count: 311
    basis: 审读 frontmatter 后全部非空、非表格分隔线的行级读者单元；契约固定标题与字段仅核对边界，不参与评分。
findings:
  - finding_id: F-LA-001
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: central-study-object
    normalized_locator: reader-entry-and-core-methods
    failure_mode: competing-object-names
    fingerprint: meso|central-study-object|reader-entry-and-core-methods|competing-object-names
    category: 术语一致性与跨学科读者入口
    dossier_locator:
      - H1 与 Title（行 33、37）
      - One-sentence complete-Idea summary 与 Structured abstract（行 38、40、44–48）
      - Primary research question、Objectives 与 Core hypothesis（行 76、80、87）
      - 成功定义、方法、证据链与解释边界（行 99、106、109、121、285、305、320、356–373、403、421、427、437、440）
    current_problem: >-
      同一总体研究对象先后称为“全病程候选动态系统表征”“候选动态复杂系统表征”“全病程候选复杂系统表征”“候选全病程表征”和“跨数据库候选系统表征”，同时又以“复杂候选”“冻结模型”和“复杂表示”指代不同阶段或模型类别；首次出现时没有明确总体对象与阶段特异模型之间的命名边界。
    target_state: >-
      先用直接描述界定总体研究对象，再为其设置一个稳定短称；“复杂候选”和“冻结模型”只用于各自明确的阶段角色。
    required_change_or_replacement: >-
      将标题改为修饰关系明确的直接描述，例如“脓毒症从未发病在险期到结局的知识约束纵向动态表征：24 个月跨数据库构建与检验计划”；在摘要首次定义“全病程动态表征”，并明确“复杂候选”仅指通过基线后接受模拟检验的切换或非线性候选，“冻结模型”指按预设规则选定并用于外部评价的模型。随后按这三种角色统一全篇称谓。
    content_to_preserve: >-
      保留 24 个月阶段 I–II、发病前至结局连续体、知识约束、简单基线后至多一个复杂候选、模型冻结和独立外部评价等边界。
    acceptance_test: >-
      复核 H1、全部入口单元及行 99–440 的相关称谓：总体对象只使用已定义的直接名称或短称；每个“复杂候选”与“冻结模型”均能唯一对应其阶段角色；标题中“知识约束”“纵向动态”和病程范围的修饰对象无歧义。
    term_or_phrase: 全病程候选动态系统表征／候选动态复杂系统表征／候选全病程表征／跨数据库候选系统表征
    recommended_form_or_plain_description: >-
      总体对象写为“覆盖未发病在险期、首次发病、发病后互斥状态与结局的知识约束纵向动态表征”，其后可简称“全病程动态表征”；阶段特异对象分别直称“接受模拟检验的复杂候选模型”和“用于外部评价的冻结模型”。
    evidence_basis: >-
      全篇称谓核对显示入口单元的核心修饰语不一致，且后文的对象、候选类别和评价阶段角色未在首次使用时分开。建议采用 dossier 已说明的组成要素作直接描述，无需外部术语检索。
    first_use_definition: >-
      “本文所称全病程动态表征，是指覆盖可比未发病在险期、首次发病、发病后互斥状态与结局，并区分患者状态、治疗行动和观测过程的知识约束纵向表征。”
    competing_forms_and_locators:
      - “全病程候选动态系统表征”：行 33、37
      - “候选动态复杂系统表征”：行 38、76
      - “全病程候选复杂系统表征／候选复杂系统表征／候选全病程表征”：行 40、44、45、48
      - “全病程状态表征／跨数据库候选系统表征／系统表征端点”：行 80、106、320、437
      - “复杂候选／复杂表示／候选模型／冻结模型”：行 45–46、66、70、87、99、109、112–126、142、166、233、249、285、305、349、356–373、421–442
  - finding_id: F-LA-002
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: simulation-recovery-criterion
    normalized_locator: reader-entry-and-methods
    failure_mode: clinical-methodological-role-collision
    fingerprint: meso|simulation-recovery-criterion|reader-entry-and-methods|clinical-methodological-role-collision
    category: 术语可理解性与角色区分
    dossier_locator:
      - 入口单元与核心假设（行 38、40、44–47、70、87）
      - 工作包、方法与证据链（行 99、121、126、166、223–235、276、301–306、349、357、379、384、421、423、440）
      - 发病后临床状态（行 193、202、207、209）
    current_problem: >-
      “恢复”同时指模拟中重获已知状态、转移概率、符号或滞后的方法学检验，以及患者的“生理恢复”状态；“恢复检验”“模拟可恢复性”“绝对恢复”“状态恢复”和“可恢复不变量”在入口处未给出方法学定义，跨学科读者容易把模型可辨识性问题与临床恢复混为一谈。
    target_state: >-
      方法学角色在首次出现时用对象明确的定义说明，后文始终带“模拟”或具体被恢复量；患者状态始终称为“生理恢复”。
    required_change_or_replacement: >-
      在行 38 首次出现时改为“模拟恢复检验（检验模型能否从已知生成情景中重获预设状态、转移概率、关系符号和滞后）”；后文方法学用语统一为“模拟恢复检验”“状态恢复准确度”或具体量名，不单独使用“恢复”“绝对恢复”或“可恢复不变量”。保留“生理恢复”专指患者状态。
    content_to_preserve: >-
      保留正确指定、零边和错设情景，绝对判据、自动降级、状态与转移参数、符号与滞后，以及生理恢复状态的既定定义。
    acceptance_test: >-
      全篇检索“恢复”：每一方法学出现均明确由模拟产生的已知量或检验对象，每一临床出现均明确为“生理恢复”；行 38–47 的读者入口无需跳至行 223 后即可区分两种角色。
    term_or_phrase: 恢复检验／模拟可恢复性／绝对恢复／状态恢复／生理恢复
    recommended_form_or_plain_description: >-
      方法学角色使用“模拟恢复检验”，并直接说明其检验的是从已知生成情景中重获预设状态、转移概率、关系符号和滞后；临床角色固定为“生理恢复”。
    evidence_basis: >-
      dossier 内部同时存在方法学恢复和患者生理恢复，且前者在标题后首批入口单元中未定义。直接写出检验对象即可消除角色冲突，无需外部术语检索。
    first_use_definition: >-
      “模拟恢复检验是指在生成机制已知的模拟数据中，检验拟合过程能否重获预设状态、转移概率、关系符号和滞后。”
    competing_forms_and_locators:
      - “恢复检验／模拟恢复检验／模拟可恢复性”：行 38、40、44–47、99
      - “绝对模拟恢复／绝对恢复／可恢复量／可恢复不变量”：行 45、70、87、121、126、166、276、301、349、357、379、384
      - “状态恢复／转移恢复／恢复预定不变量”：行 229–235、357、421
      - “生理恢复”：行 193、202、207、209
  - finding_id: F-LA-003
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: external-validation-consequence
    normalized_locator: hypothesis-and-interpretation-matrix
    failure_mode: literal-transport-metaphor
    fingerprint: meso|external-validation-consequence|hypothesis-and-interpretation-matrix|literal-transport-metaphor
    category: 术语自然度与科学后果表达
    dossier_locator:
      - Core hypothesis（行 87）
      - 外部支持、失败与允许解释（行 247、359、368–369、397、404、438、442）
      - 最接近工作比较（行 394）
    current_problem: >-
      “跨数据库运输”“数据库级运输”“运输失败”“适配后可运输”和“运输性”把模型在外部数据库中的适用性、评价结果、失败状态及适配后结果都压缩为“运输”。该词在普通中文中首先表示实体移动，且这些用法对应不同科学后果，跨学科读者不能从词面判断具体含义。
    target_state: >-
      按科学角色直接说明冻结模型在外部数据库中是否维持预设标准、适配后是否达到标准，以及证据仅支持数据库层描述还是外部有效性。
    required_change_or_replacement: >-
      首次使用时定义“跨数据库外部有效性”为冻结模型在未用于开发或调参的外部数据中维持预设评分、校准、状态对齐和结构标准；把失败写成“冻结模型在外部数据库中未达到预设标准”，把适配后结果写成“经适配后达到外部评价标准”，把“数据库级运输”写成“仅能报告数据库层面的外部适用性或描述性结果”。最接近工作表中如需保留英文 transportability，应给出这一中文解释。
    content_to_preserve: >-
      保留冻结模型、仅重估校准、仅重估观测方程和全部重估四种操作的区分，以及失败不得被适配后结果替代的解释边界。
    acceptance_test: >-
      全篇不再用未定义的“运输”单独表示外部有效性；行 87、247、359、368–369、394、397、404、438、442 均明确是冻结模型结果、适配后结果、数据库层描述或文献主题中的哪一种。
    term_or_phrase: 跨数据库运输／数据库级运输／运输失败／适配后可运输／运输性
    recommended_form_or_plain_description: >-
      优先使用“冻结模型在外部数据库中的外部有效性”“冻结模型在外部数据库中未达到预设标准”“经适配后达到外部评价标准”等直接描述；仅在确有必要时于首次定义后使用短称。
    evidence_basis: >-
      dossier 内部角色核对显示同一字根同时承担研究主题、检验动作、失败状态和适配后结论，且普通中文词面不能提供这些区分。直接描述已由 dossier 自身的评价规则支持，无需外部术语检索。
    first_use_definition: >-
      “跨数据库外部有效性是指冻结模型在未用于开发或调参的外部数据库评价数据中，仍达到预设的评分、校准、状态对齐和结构稳定标准。”
    competing_forms_and_locators:
      - “跨数据库运输”：行 87、397
      - “数据库级运输”：行 247、438
      - “跨数据库运输失败／运输失败”：行 368、404、442
      - “适配后可运输／适配后的运输”：行 359、369
      - “运输性／强化学习与运输”：行 394
  - finding_id: F-LA-004
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: secondary-representation-diagnostics
    normalized_locator: abstract-objectives-and-methods
    failure_mode: competing-diagnostic-labels
    fingerprint: meso|secondary-representation-diagnostics|abstract-objectives-and-methods|competing-diagnostic-labels
    category: 术语一致性
    dossier_locator:
      - Expected result、Objective 3 与 Pass/fail（行 47、82、196）
      - 工作包、方法顺序与证据链（行 122、126、166、274–276、308–312、338、350、384）
    current_problem: >-
      同一组诊断先称“两项次要表示诊断”或“次要表示诊断”，后文改称“两项次要诊断”，直到较后位置才看出具体是伪遮蔽重建和未来轨迹诊断；“表示”还与总体对象的“表征”形成无说明的词形竞争。
    target_state: >-
      首次出现即给出统一名称和两项组成，后文用同一短称。
    required_change_or_replacement: >-
      在行 47 改为“两项次要表征诊断（伪遮蔽重建和未来轨迹诊断）”，其后统一称“两项次要表征诊断”；若某处只指其中一项，则直写该项名称。
    content_to_preserve: >-
      保留两项诊断的次要地位、具体指标、不能替代主要任务或恢复检验的边界。
    acceptance_test: >-
      全篇检索“表示诊断”“次要诊断”和“表征诊断”：同一组合只保留首次定义后的统一形式，单项出现均明确具体诊断名称。
    term_or_phrase: 两项次要表示诊断／次要表示诊断／两项次要诊断
    recommended_form_or_plain_description: 两项次要表征诊断（伪遮蔽重建和未来轨迹诊断）
    evidence_basis: >-
      全篇称谓核对显示三种形式指向行 274–276 所述同一组诊断；直接列出两项组成即可完成定义，无需外部术语检索。
    first_use_definition: “两项次要表征诊断是伪遮蔽重建诊断和未来轨迹诊断。”
    competing_forms_and_locators:
      - “两项次要表示诊断／次要表示诊断”：行 47、82、196
      - “两项次要诊断／次要诊断”：行 122、126、166、274、308、312、338、350、384
  - finding_id: F-LA-005
    severity: major
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: complete-idea-summary
    normalized_locator: line-38
    failure_mode: stacked-clause-density
    fingerprint: micro|complete-idea-summary|line-38|stacked-clause-density
    category: 中文学术清晰度、简洁性与可读性
    dossier_locator: One-sentence complete-Idea summary（行 38）
    current_problem: >-
      单句同时承载数据支持前提、知识约束、四段病程范围、两项主要任务、两类验证、论文目标和条件性试验延伸；“利用两个人群、事件与变量支持须先核验的纵向公共 ICU 数据库”等多层前置修饰使主干和修饰对象难以一次识别。
    target_state: >-
      在保持“一句”字段约束下，读者能依次识别研究对象、数据前提、两项主要任务、主要检验和条件性延伸。
    required_change_or_replacement: >-
      保留一个句号，将主句主干提前，按“构建什么—用什么数据—检验什么—产出与条件性延伸”重排为并列分句；把数据库支持前提改为后置定语或独立插入语，并删除不增加边界的修饰词。
    content_to_preserve: >-
      保留 24 个月、双数据库支持须先核验、全病程范围、两项主要任务、模拟检验、冻结模型外部验证、非单一预测工具定位和试验次要分析的条件性。
    acceptance_test: >-
      修订后仍为且仅为一句；主语与“构建/检验”主干在前半句可直接定位；数据库支持条件不会被误读为“利用两个人群”；两项主要任务和两类验证均各有明确宾语。
  - finding_id: F-LA-006
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: external-validation-hypothesis
    normalized_locator: line-45
    failure_mode: ambiguous-modifier-attachment
    fingerprint: micro|external-validation-hypothesis|line-45|ambiguous-modifier-attachment
    category: 并列结构与修饰关系
    dossier_locator: Structured abstract—Objective and hypothesis（行 45）
    current_problem: >-
      “在时间外、医院外和未触碰数据库外数据中”把验证集类型、医院边界和数据库边界压缩为不平行的“外”字结构，“未触碰”也可能修饰“数据库外数据”而非外部数据库中的最终评价数据。
    target_state: >-
      三类评价数据以平行名词短语出现，且“未用于开发或适配”明确修饰外部数据库最终评价数据。
    required_change_or_replacement: >-
      改为“在时间外验证集、医院外验证集，以及外部数据库中未用于开发或适配的最终评价数据上维持……”。
    content_to_preserve: >-
      保留时间外、医院外和外部数据库最终评价三层证据，以及校准、状态对齐和结构稳定性三个标准。
    acceptance_test: >-
      三个并列成分均为可识别的数据集或评价集；“未用于开发或适配”只有一个明确的修饰对象；不改变任何验证层级。
  - finding_id: F-LA-007
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: primary-research-question
    normalized_locator: line-76
    failure_mode: unnatural-clustering-predicate
    fingerprint: micro|primary-research-question|line-76|unnatural-clustering-predicate
    category: 中文搭配与读者入口
    dossier_locator: Primary research question（行 76）
    current_problem: >-
      “在患者与医院聚类得到尊重的前提下显示……”是英语式直译，“聚类得到尊重”不是自然的中文统计表达，且“显示跨数据库状态与结构有效性”的动作主体不清楚。
    target_state: >-
      明确分析如何处理聚类，以及研究检验的外部有效性对象。
    required_change_or_replacement: >-
      改为“在分析中正确处理患者内及医院内聚类后，检验其状态与结构在外部数据库中的有效性……”。
    content_to_preserve: >-
      保留患者和医院两层聚类、跨数据库状态与结构评价，以及不将预测等同于因果的限制。
    acceptance_test: >-
      句中明确出现“处理患者内及医院内聚类”的分析动作，并给出“检验”的明确宾语；研究问题仍保持一个问句。
  - finding_id: F-LA-008
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: time-and-entry-definitions
    normalized_locator: protocol-and-evidence-chain
    failure_mode: competing-language-forms
    fingerprint: meso|time-and-entry-definitions|protocol-and-evidence-chain|competing-language-forms
    category: 中英术语一致性
    dossier_locator:
      - Protocol locks 表（行 187–192）
      - Evidence chains 与 Required analyses（行 297、334）
    current_problem: >-
      正文已经使用“临床事件时刻”“信息可用时刻”“延迟进入”等中文形式，但局部又切换为 availability、event time、next-state 和 delayed entry，且未说明这些英文形式是否与既有中文概念完全同义。
    target_state: >-
      同一时间与进入概念在中文正文中保持单一形式；需要英文对照时只在首次定义处括注一次。
    required_change_or_replacement: >-
      行 188 分别使用“信息可用时刻”和“临床事件时刻”，行 192 使用“下一时点状态”，行 297、334 使用“延迟进入”；如保留英文，只在首次定义后括注 availability time、event time 或 delayed entry。
    content_to_preserve: >-
      保留事件发生与信息可用的双时钟、同一时间格行动、下一边界状态及左截断/延迟进入的技术含义。
    acceptance_test: >-
      全篇核对四组形式：每个概念只有一个中文主称，英文只在首次括注且不单独替代中文；行 187–192 与行 297、334 的指代完全一致。
    term_or_phrase: availability／event time／next-state／delayed entry
    recommended_form_or_plain_description: 信息可用时刻／临床事件时刻／下一时点状态／延迟进入
    evidence_basis: >-
      dossier 在相邻位置已经给出对应中文概念，英文切换未增加技术信息却造成同义关系不明；可直接依照 dossier 内部定义统一，无需外部术语检索。
    first_use_definition: >-
      “临床事件时刻指事件发生的时刻；信息可用时刻指该信息在源系统中可用于分析的最早时刻；延迟进入指患者在发病后首个可审计时点才进入风险集。”
    competing_forms_and_locators:
      - “临床事件时刻／event time”：行 187、188
      - “信息可用时刻／availability”：行 187–189
      - “下一边界实测生理／next-state”：行 192
      - “延迟进入／delayed entry”：行 186、189–195、297、334
  - finding_id: F-LA-009
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: data-access-and-trial-documents
    normalized_locator: resource-and-trial-prerequisites
    failure_mode: undefined-abbreviations
    fingerprint: meso|data-access-and-trial-documents|resource-and-trial-prerequisites|undefined-abbreviations
    category: 缩写首次定义与跨学科可及性
    dossier_locator:
      - 资源与证据状态表（行 97、135、137–138）
      - 数据库和试验前提（行 147、158、255、413、415）
      - 本地材料参考项（行 470–473）
    current_problem: >-
      DUA、CRF、SAP、QC 和 EDC 在决定数据库访问、试验语义核验或材料证据等级的位置直接出现，未在首次读者可见使用处展开；目标读者跨越临床、统计、系统科学和医学 AI，不能假设所有人熟悉试验管理与数据治理缩写。
    target_state: >-
      每个非通用缩写在首次正文使用时给出中文全称，必要时括注英文与缩写，后文再使用缩写。
    required_change_or_replacement: >-
      首次使用时分别写为“数据使用协议（data use agreement, DUA）”“病例报告表（case report form, CRF）”“统计分析计划（statistical analysis plan, SAP）”“质量控制（QC）”和“电子数据采集系统（electronic data capture, EDC）”；参考项可保留缩写，但应与前文定义一致。
    content_to_preserve: >-
      保留各文件或流程在访问确认、试验语义核验和本地衍生材料证据等级中的不同作用。
    acceptance_test: >-
      从行 33 顺序阅读时，DUA、CRF、SAP、QC、EDC 的第一次出现均带可理解的中文全称；后续缩写与首次定义一一对应，且未把不同文件角色合并。
    term_or_phrase: DUA／CRF／SAP／QC／EDC
    recommended_form_or_plain_description: >-
      数据使用协议（DUA）；病例报告表（CRF）；统计分析计划（SAP）；质量控制（QC）；电子数据采集系统（EDC）。
    evidence_basis: >-
      这些缩写位于数据准入和试验分析停止条件中，且 embedded reader handoff 明确不能假设读者掌握其他学科的隐含词汇；问题是缺少首次定义而非术语标准性争议，无需外部检索。
    first_use_definition: >-
      “数据库访问需确认数据使用协议（data use agreement, DUA）；试验语义需由病例报告表（case report form, CRF）和统计分析计划（statistical analysis plan, SAP）等原始文件核验。”
    competing_forms_and_locators:
      - “DUA”：行 97、135、147、413
      - “CRF／SAP”：行 138、158、255、415、470
      - “QC”：行 137、470–473
      - “EDC”：行 472
  - finding_id: F-LA-010
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: conditional-trial-route
    normalized_locator: lines-255-265
    failure_mode: untranslated-reader-labels
    fingerprint: meso|conditional-trial-route|lines-255-265|untranslated-reader-labels
    category: 目标语言一致性
    dossier_locator:
      - 行 255：Shared prerequisites
      - 行 257、261：Mapping-based route 两个标签
      - 行 263：Visit-level hierarchical outcome and randomized comparison
      - 行 265：Independent trial-specific clinical-state route and stopping condition
    current_problem: >-
      五个加粗的自由文本导语完全使用英文，而相邻正文及整份 dossier 的目标语言为中文；它们承担路线导航功能，跨学科中文读者必须先翻译才能判断前提、映射路线、结局与停止条件之间的关系。
    target_state: >-
      路线导航标签使用自然中文，并与正文中的“共同前提”“基于映射的路线”“独立临床状态路线”等称谓一致。
    required_change_or_replacement: >-
      依次改为“共同前提”“基于映射的路线：共同实测锚点与冻结计算”“基于映射的路线：经验一致性标准”“访视层级结局与随机化比较”“试验特异的独立临床状态路线及停止条件”。
    content_to_preserve: >-
      保留五段的顺序、两条互斥路线、访视层级结局、随机化比较和停止条件，不更改任何方法内容。
    acceptance_test: >-
      行 255–265 的五个加粗导语全部为中文且与正文术语一致；每段仍能唯一标识其原有功能和路线边界。
  - finding_id: F-LA-011
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: contribution-claim-types
    normalized_locator: lines-403-407
    failure_mode: mixed-language-internal-labels
    fingerprint: meso|contribution-claim-types|lines-403-407|mixed-language-internal-labels
    category: 自由标签的目标语言与内部记号泄漏
    dossier_locator: Title and positioning claim-support table 的“Contribution frame / claim type”数据单元（行 403–407）
    current_problem: >-
      自由文本单元使用 integration、validation、benchmark、translational、resource、scientific novelty 等英文类别，其中行 406 还出现内部式蛇形记号 editorial_repositioning；这些不是契约固定表头，直接暴露在中文读者界面中。
    target_state: >-
      表内自由类别用自然中文表达，内部记号不进入读者可见文本，同时保留每行原有类别区分。
    required_change_or_replacement: >-
      分别改为“整合／验证”“验证／基准”“验证／转化”“定位调整／整合／资源”“科学新颖性”；不要更改契约固定的 Claim-Support 表头。
    content_to_preserve: >-
      保留五行的类别组合、标题与定位主张、证据链和支持状态；固定表头及其字段数保持不变。
    acceptance_test: >-
      行 403–407 的所有自由类别均为自然中文，普通正文中不再出现 editorial_repositioning；表头、列数与每行类别数量不变。
  - finding_id: F-LA-012
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: governance-signoff
    normalized_locator: line-93
    failure_mode: category-mismatch-predicate
    fingerprint: micro|governance-signoff|line-93|category-mismatch-predicate
    category: 语法与搭配
    dossier_locator: Twenty-four-month minimum and dated gates（行 93）
    current_problem: >-
      “负责人签署是计划所需角色”把签署动作与角色身份作等同判断，主语和宾语类别不匹配；后半句虽然说明没有人员承诺，却不能消除前半句的语义错位。
    target_state: >-
      明确签署要求对应必须落实的职责，而不是把签署本身称为角色。
    required_change_or_replacement: >-
      改为“下表涉及的负责人签署要求，对应计划中必须落实的职责；这不表示当前已有具名人员作出承诺。”
    content_to_preserve: >-
      保留角色尚未具名、当前无人员承诺及外部评价结果由独立保管人保持不可访问的边界。
    acceptance_test: >-
      修订句的主语为“签署要求”，谓语说明其与职责的对应关系；不得写成已有具名负责人或既有承诺。
  - finding_id: F-LA-013
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: external-support-threshold
    normalized_locator: line-247
    failure_mode: compressed-parallel-conditions
    fingerprint: micro|external-support-threshold|line-247|compressed-parallel-conditions
    category: 并列条件与量词对应
    dossier_locator: Hospital-prioritized independent cross-database validation，第 5 条（行 247）
    current_problem: >-
      “任一自由风险或转移参数低于外部 10 个事件或转移”把风险参数、转移参数、事件和转移交叉并列，数量阈值与各参数类型的对应关系需要读者回到前文推断。
    target_state: >-
      风险参数与事件数、转移参数与转移次数形成两个平行且明确的条件。
    required_change_or_replacement: >-
      改为“任一自由风险参数对应的外部事件少于 10 个，或任一自由转移参数对应的外部转移少于 10 次”。
    content_to_preserve: >-
      保留外部每个自由参数至少 10 个事件或转移的阈值，以及触发备份数据库的后果。
    acceptance_test: >-
      两个条件均包含参数类型、对应计数对象和阈值；事件数不再可能修饰转移参数，转移次数也不再可能修饰风险参数。
unresolved_issues:
  - F-LA-001
  - F-LA-002
  - F-LA-003
  - F-LA-004
  - F-LA-005
  - F-LA-006
  - F-LA-007
  - F-LA-008
  - F-LA-009
  - F-LA-010
  - F-LA-011
  - F-LA-012
  - F-LA-013
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-v050-r104  
**Target Language**: Chinese  
**Discipline**: 跨学科生物医学系统研究（重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学 AI 与转化研究）  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

主要语法、正式语体和计划性时态稳定，但三个核心概念群在跨学科读者入口处仍有命名竞争或误导性直译，触发术语一致性硬门槛；单句摘要的高密度结构进一步妨碍首次阅读。应完成定向语言修订后再进行独立复评。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 7 | pass |
| Academic Register & Tone | 8 | pass |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 6 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 未见超过 3/500 词的模式；清晰问题集中于 3 处局部搭配或并列结构，按全文平均低于 1/500 词。 |
| Academic register | pass | 无章节呈现系统性口语语体；局部英文标签属于目标语言与术语问题。 |
| Terminology coherence | fail | 总体研究对象、模拟恢复角色和跨数据库外部有效性 3 个核心概念群在入口或关键后果处存在竞争称谓、角色混同或误导性直译。 |
| Tense systematic violation | pass | 计划性动作、既有证据和未生成结果的时间状态区分稳定；无方法或结果章节的系统时态违例。 |

---

## Strengths

- 全文持续把拟开展工作、既有材料和尚未生成的结果区分开，计划性语气稳定。
- 正式学术语体占主导，没有口语化、直接称呼读者或感叹式表述。
- 数字阈值、时间窗和条件后果大多以平行表格或列表呈现，便于定位。
- “预测不等同于因果”、条件性试验分析及失败结果边界使用了明确而克制的语言。
- 中英文数据库名、方法名和数学符号总体保持原有技术含义，没有把契约固定字段误作正文语言问题。

---

## Specific Issues

### Chinese Academic Clarity

| Finding | Locator | Concise evidence and reader effect | Severity |
|---|---|---|---|
| F-LA-005 | 行 38 | 单句摘要中多层前置修饰和七类信息争夺主干，首次阅读难以确定数据库条件修饰什么。 | major |
| F-LA-006 | 行 45 | 三种“外”字结构不平行，“未触碰”的修饰对象不唯一。 | minor |
| F-LA-007 | 行 76 | “聚类得到尊重”是非自然中文搭配，检验动作的宾语不清。 | minor |
| F-LA-010 | 行 255–265 | 五个路线导航标签完全为英文，增加中文读者的跨段切换成本。 | minor |
| F-LA-011 | 行 403–407 | 中文表格自由标签混用英文，并泄漏 editorial_repositioning 形式的内部记号。 | minor |
| F-LA-012 | 行 93 | 把“签署”与“角色”等同，主宾语类别不匹配。 | minor |
| F-LA-013 | 行 247 | 两类参数与两类计数对象交叉并列，阈值对应关系需回读。 | minor |

### Grammar & Syntax

明确且可独立修复的构式问题为 F-LA-007、F-LA-012 和 F-LA-013。其余长句主要属于信息密度、修饰关系或术语问题，而非高密度语法错误。

### Academic Register & Tone

未发现系统性口语语体。对论文产出的表述保持为前瞻目标，没有把计划写成已取得的学术影响；本轮不将其判为宣传性结果主张。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| F-LA-001 | 总体研究对象及阶段特异模型称谓 | 行 33–48、76–121、285–440 | 读者难以判断“表征”“复杂候选”和“冻结模型”何时同指、何时分指。 | yes |
| F-LA-002 | 模拟恢复与生理恢复 | 行 38–47、87–235、193–209、276–440 | 方法学可恢复性与患者状态共享同一词根，入口处角色混同。 | yes |
| F-LA-003 | 跨数据库运输等 | 行 87、247、359、368–369、394、397、404、438、442 | 物理移动式词义遮蔽外部评价、适配后结果和失败后果的差别。 | yes |
| F-LA-004 | 次要表示诊断／次要诊断 | 行 47、82、122、126、166、196、274–384 | 同一组诊断的名称与组成未在首次出现处绑定。 | yes |
| F-LA-008 | availability、event time、next-state、delayed entry | 行 187–192、297、334 | 同一时间概念在中英文形式之间无说明切换。 | yes |
| F-LA-009 | DUA、CRF、SAP、QC、EDC | 行 97、135–158、255、413–415、470–473 | 非试验管理专业的读者在准入与停止条件处需要猜测缩写。 | yes |

本轮未把 ICU、AI、Sepsis-3、数据库版本、数学符号、DOI 片段或参考文献中的文件名仅因扫描出现而列为问题；它们在当前语境下属于标准、已说明、描述性或必要的精确标识。

### Tense & Voice Conventions

未发现系统性问题。未来或条件式用于拟开展研究，过去或现在时用于既有文献、当前资源状态和定义，符合研究计划文本的时间状态。

### Conciseness & Redundancy

F-LA-005 是最直接的简洁性问题。其他跨章节条件重复可能承担不同论证功能，本评估不决定其保留位置；只要求在局部句内删除不增加范围、条件或证据状态的堆叠修饰。

### Readability & Flow

主要障碍来自 F-LA-005 至 F-LA-007 的入口句结构，以及 F-LA-010、F-LA-011 的语言切换。章节顺序、论证位置和跨节披露序列不属于本语言评估。

---

## Language Revision Priorities

1. **核心术语**：先处理 F-LA-001 至 F-LA-003，使总体研究对象、模拟检验和外部数据库证据在入口处即可区分。
2. **读者入口句**：处理 F-LA-005 至 F-LA-007，在不改变单句或问句字段约束的前提下恢复清晰主干与修饰关系。
3. **全篇一致性**：处理 F-LA-004、F-LA-008 和 F-LA-009，完成诊断名称、时间词及准入文件缩写的首次定义与全篇核对。
4. **局部中文化与构式**：处理 F-LA-010 至 F-LA-013，消除自由标签中的英文和内部记号，并明确局部并列关系。

---

## Re-Assessment Status

不适用。本轮是对冻结 v050 dossier 的全新完整评估，未接收匿名问题清单，也未读取任何先前版本、差异、修订说明或既往评估。

---

## Assessment Notes

- 读者基线采用任务内嵌 handoff：受众可了解脓毒症基础及各自学科的研究设计或建模概念，但不预设掌握项目特定标签或其他学科的隐含词汇。
- 指令文件、量表、硬门槛、中文与学科惯例、术语政策、模板及两个适用脚本均全文读取；项目内容只读取已绑定 dossier 的 frontmatter 与行 33–486。
- research-idea.v3 的固定 H2/H3 标题、section-1 与结构式摘要字段、证据链字段和 Claim-Support 表头均按固定边界处理；F-LA-010 与 F-LA-011 只涉及自由文本导语或数据单元。
- 有界短语核对未触发必须依赖权威外部资料的标准性争议，因此未浏览网页，也没有外部 URL。
- 本评估不判断研究有效性、可行性、新颖性、影响力、论证结构或期刊适配度；源 dossier 未被编辑。
