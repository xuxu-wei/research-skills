---
review_id: language-assessment-I01-001-r007
reviewer_skill: academic-language-assessor
reviewer_instance_id: academic-language-assessor-new-v006-r007b
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: language-review-r007
input_artifact_ids:
  - idea-dossier-I01-001-v006
input_versions:
  - v006
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v006
  version: v006
  path: tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
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
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: minor_language_revision
coverage_receipt:
  reader_entry:
    status: completed
    reviewed_count: 27
    basis: >-
      检查了两处标题、单句摘要、受众与定位入口、结构式摘要五个字段、研究问题、四项目标、核心假设，以及贡献与标题主张入口；固定字段名不计入语言评分。
  core_scientific_role:
    status: completed
    reviewed_count: 12
    basis: >-
      按正文实际出现的中心模型、四项预测任务、开发与外部应用、状态表示与观测过程评价、恢复诊断、结论状态及条件性后续研究等角色逐一核对读者可见名称，未添加正文中不存在的角色。
  terminology_concordance:
    status: completed
    reviewed_count: 8
    basis: >-
      对候选扫描及通读触发的八个概念组完成全篇首用、复合短语、双语形式、修饰语指向和跨位置一致性核对；仅保留下列已确认问题。
  local_language:
    status: completed
    reviewed_count: 169
    basis: >-
      逐一检查397行文档中的169个非空读者可见正文、列表或表格单元；固定二级和三级标题、表格分隔行、机器元数据及固定字段名不计入语言评分。
findings:
  - finding_id: LANG-001
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: external-state-representation
    normalized_locator: summary-line-36-and-cross-database-state-sections-lines-40-315
    failure_mode: ambiguous-development-state-modifier-and-occupancy-label
    fingerprint: "meso|external-state-representation|summary-line-36-and-cross-database-state-sections-lines-40-315|ambiguous-development-state-modifier-and-occupancy-label"
    category: 术语一致性与修饰语指向
    dossier_locator: >-
      单句摘要第36行；术语释义第40行；Gap、Rationale、研究问题、目标与核心假设第64、72、76、84、87行；外部应用与状态表示诊断第165、167、169行；证据链及标题主张表第222–227、315行。
    current_problem: >-
      “开发状态”在普通汉语中可被读作研究或产品的开发进度状态，而本稿实际指在开发数据库中估计并于外部应用前冻结的模型状态；“在外部数据库中的占用”又没有直接说明所指的是外部患者落入各状态的比例。上下文最终能恢复所指，但跨学科读者在摘要和研究问题处需要回读。
    target_state: >-
      首次出现即明确性质属于模型状态、这些状态来自开发数据库并已冻结，同时用直接表述说明“占用”是外部患者在各状态中的比例；后文对同一角色使用稳定短称。
    required_change_or_replacement: >-
      在第36行首次出现时改为“在开发数据库中估计并冻结的模型状态在外部患者中的出现比例（状态占据率）和可分离性”。此后凡指同一角色，使用“这些冻结模型状态”或完整表述；凡指频率，统一使用“状态占据率”，并保留“开发阶段”表示研究阶段的正常用法。对下列位置作全篇一致性替换，不改动外部数据库不得重新估计或重新命名状态的限定。
    content_to_preserve: >-
      状态在开发数据库中估计并冻结、标签在外部数据库中继承、外部患者的状态比例与基于预定临床特征的可分离性分别评价，以及外部数据不用于重新估计或重命名状态。
    acceptance_test: >-
      从摘要到结论边界逐项检索后，不再有可独立理解为“开发进度”的“开发状态”；首次出现给出完整定义，后续短称均唯一回指冻结模型状态；所有表示频率的“占用”均明确为状态占据率，且未把分布距离、可分离性或患者病程转移合并为同一概念。
    term_or_phrase: 开发状态在外部数据库中的占用和可分离性
    recommended_form_or_plain_description: >-
      在开发数据库中估计并冻结的模型状态在外部患者中的状态占据率和基于预定临床特征的可分离性
    evidence_basis: >-
      本稿第165行明确状态数、参数与标签在开发完成后冻结，第167行明确外部比较对象是继承同一标签的患者在预定临床特征上的分布；这两处足以确定修饰对象。问题来自普通汉语中的修饰语指向，不需要另造术语或以外部文献替代直接描述。
    first_use_definition: >-
      “在开发数据库中估计并冻结的模型状态”指模型在开发数据中确定、并在外部应用前固定其参数和标签的潜在状态；“状态占据率”指外部患者在相应状态中的比例。
    competing_forms_and_locators:
      - “开发状态在外部数据库中的占用和可分离性”：第36、40、72、84、102、227、268、315、349行
      - “开发状态在预定临床特征上的可分离性”：第64、76、87、122行
      - “开发状态标签／冻结开发状态／开发必需状态／必需开发状态”：第165、167、175–176、212、222、225、276、283、285、301行
      - “状态占用／最小占用／冻结占用”：第40、118、146、165、167、169、193、211、226、248行
  - finding_id: LANG-002
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: task-three-prediction-target
    normalized_locator: summary-question-hypothesis-and-task-three-sections
    failure_mode: stacked-qualifiers-and-role-form-variation
    fingerprint: "meso|task-three-prediction-target|summary-question-hypothesis-and-task-three-sections|stacked-qualifiers-and-role-form-variation"
    category: 术语、限定语叠加与修饰语指向
    dossier_locator: >-
      单句摘要第36行；结构式摘要第47行；Significance第68行；主要研究问题第76行；核心假设第87行；H3任务行第158行；第三条证据链第217–219行；外部验证分析与预期输出第256、267行；结果解释与固定操作化说明第286、333行。
    current_problem: >-
      “从部分已观测历史预测被有意遮蔽但实际测得的临床变量”反复把输入历史、遮蔽操作、变量的实测属性和预测动作压入同一长串修饰语；“部分”可附着于历史范围或观测程度。后文又交替使用“遮蔽实测值”“被有意遮蔽的实测临床变量”和“测量补全用途”，使读者需要自行区分任务名称、评分目标与结果解释。
    target_state: >-
      用主谓宾结构分别命名输入、预测目标和解释范围；首次说明变量原本已在数据库中测得、仅为评价而暂时遮蔽，随后按科学角色使用一致的直接表述。
    required_change_or_replacement: >-
      在第36行将任务三写为“任务三基于遮蔽前及其他未遮蔽的观测历史，预测按预定规则暂时遮蔽、但数据库中实际测得的临床变量”。在任务名称与研究问题中使用该直接结构；在评分语境统一使用“按预定规则暂时遮蔽的实测值”；在解释语境使用“实测临床变量的预测（测量补全）”。不得另造没有定义的紧凑标签，也不得削弱“潜在生理状态不是真值或验证端点”的限定。
    content_to_preserve: >-
      输入只包括遮蔽前和其他未遮蔽观测，评分目标必须是数据库中实际测得而后被暂时遮蔽的变量，潜在生理状态不是任务三的真值、标签或验证端点，任务通过仅支持测量补全用途。
    acceptance_test: >-
      每个读者入口都能分别回答“基于什么信息、预测什么对象、对象为何可评分、任务通过允许怎样解释”；全篇检索不再出现原长串修饰语，评分目标统一为“按预定规则暂时遮蔽的实测值”，解释统一为“实测临床变量的预测（测量补全）”，且没有新增未定义短标签。
    term_or_phrase: 从部分已观测历史预测被有意遮蔽但实际测得的临床变量
    recommended_form_or_plain_description: >-
      基于遮蔽前及其他未遮蔽的观测历史，预测按预定规则暂时遮蔽、但数据库中实际测得的临床变量
    evidence_basis: >-
      第158行明确输入、遮蔽块和实测目标，第333行明确任务只支持测量补全而不验证潜在状态；因此可用本稿已经固定的角色关系作直接描述，无需验证或创造新术语。
    first_use_definition: >-
      任务三使用遮蔽前及其他未遮蔽的观测历史，预测数据库中原本已经测得、但为评价模型而按预定规则暂时遮蔽的临床变量。
    competing_forms_and_locators:
      - “从部分已观测历史预测被有意遮蔽但实际测得的临床变量”：第36、47、68、76、286、333行
      - “被有意遮蔽但实际测得的临床变量”：第87、256、267行
      - “被有意遮蔽的实测临床变量”：第158行
      - “遮蔽实测值／遮蔽实测临床变量”：第158、217、219行
      - “测量补全用途”：第286、333行
  - finding_id: LANG-003
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: simulation-recovery-diagnostic
    normalized_locator: objectives-methods-evidence-and-stop-sections-lines-48-363
    failure_mode: ambiguous-coordination-and-modifier-attachment
    fingerprint: "meso|simulation-recovery-diagnostic|objectives-methods-evidence-and-stop-sections-lines-48-363|ambiguous-coordination-and-modifier-attachment"
    category: 术语一致性与并列结构
    dossier_locator: >-
      Approach与Rationale第48、72行；目标与研究单元第83、94行；资格、模型复杂度、技术、证据链、必需分析、预期输出、证伪标准、贡献和停止条件中的第122、134、148、193、204–205、210、244、251、266、274、294、349、363行。
    current_problem: >-
      “参数与潜在状态恢复诊断”可解析为“参数”与“潜在状态恢复诊断”两个并列对象，也可解析为同时评价参数恢复和潜在状态恢复的诊断；“参数与潜在状态恢复报告”进一步放大该附着歧义。第48和72行的动词句虽能帮助恢复含义，名词短语在后文仍反复要求回读。
    target_state: >-
      首次出现以完整动词句说明诊断同时检验参数和潜在状态能否恢复，后文使用具有明确共同修饰范围的单一名词形式。
    required_change_or_replacement: >-
      保留第48行“检验参数和潜在状态能否被可靠恢复”的直接说明，并在该处或第83行引入“参数和潜在状态的恢复诊断”；后文把同一诊断统一为该形式，把报告相应写成“参数和潜在状态的恢复诊断报告”。仅指潜在状态时保留“潜在状态恢复诊断”，不得把两类诊断结果合并为一个未分项的科学量。
    content_to_preserve: >-
      诊断同时涉及参数估计和潜在状态恢复，开发阶段以模拟检验，两类结果各自保留，失败时按预定复杂度顺序处理。
    acceptance_test: >-
      全篇每处名词短语都能唯一解析为“对参数恢复与潜在状态恢复进行诊断”；涉及报告时明确是诊断报告；只评价潜在状态的第349行仍保持其较窄范围，未被错误扩展到参数。
    term_or_phrase: 参数与潜在状态恢复诊断
    recommended_form_or_plain_description: 参数和潜在状态的恢复诊断
    evidence_basis: >-
      第48和72行已经直接陈述“检验参数和潜在状态能否被可靠恢复”，第146行又分别列出参数偏倚、区间覆盖与标签交换等检查，因此所需修订只是让名词短语与本稿已经清楚表达的并列角色一致。
    first_use_definition: >-
      开发阶段将通过模拟检验参数估计值和潜在状态能否从模拟数据中可靠恢复；下文将这一组检查称为“参数和潜在状态的恢复诊断”。
    competing_forms_and_locators:
      - “检验参数和潜在状态能否被可靠恢复”：第48、72行
      - “参数与潜在状态恢复诊断”：第83、94、122、134、148、193、204–205、210、244、251、266、274、294、363行
      - “参数与潜在状态恢复报告”：第94行
      - “潜在状态恢复诊断”：第349行
  - finding_id: LANG-004
    severity: minor
    finding_kind: terminology
    finding_level: micro
    finding_scope: occurrence
    scientific_role: open-dynamic-clinical-system-perspective
    normalized_locator: terminology-definition-paragraph-line-40
    failure_mode: opaque-and-decorative-megasystem-label
    fingerprint: "micro|open-dynamic-clinical-system-perspective|terminology-definition-paragraph-line-40|opaque-and-decorative-megasystem-label"
    category: 术语与隐喻
    dossier_locator: 第40行术语释义段末句。
    current_problem: >-
      “人体开放复杂巨系统”是一个紧凑且带修辞色彩的标签，“巨系统”没有在稿内承担可辨认的测量或模型角色；同一句随后给出的直接描述已经完整表达所指。该标签对重症医学、统计学和期刊编辑等受众增加了无必要的术语负担。
    target_state: >-
      只保留可直接识别研究视角的描述，不要求读者接受或记忆一个未在后文使用的标签。
    required_change_or_replacement: >-
      删除引号内的“人体开放复杂巨系统”标签，将整句改为“本研究将患者病程视为一个与治疗、测量和外部环境持续交换信息的开放动态临床系统”。后文不另设短称。
    content_to_preserve: >-
      患者病程具有动态性，并持续与治疗、测量和外部环境交换信息。
    acceptance_test: >-
      第40行不再出现“巨系统”或新的同义隐喻；保留的句子明确说出研究对象、动态属性以及与治疗、测量和环境的关系，且不依赖项目词汇表。
    term_or_phrase: 人体开放复杂巨系统
    recommended_form_or_plain_description: >-
      与治疗、测量和外部环境持续交换信息的开放动态临床系统
    evidence_basis: >-
      同一句已经用直接描述给出全部科学所指，且该紧凑标签在正文其他位置不承担名称功能；因此直接描述优于保留或另造短标签。
    first_use_definition: >-
      不保留短标签；首次且唯一一次表述直接写为“本研究将患者病程视为一个与治疗、测量和外部环境持续交换信息的开放动态临床系统”。
    competing_forms_and_locators: []
  - finding_id: LANG-005
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: complete-idea-summary
    normalized_locator: one-sentence-complete-idea-summary-line-36
    failure_mode: overloaded-clause-chain
    fingerprint: "micro|complete-idea-summary|one-sentence-complete-idea-summary-line-36|overloaded-clause-chain"
    category: 简洁性与局部可读性
    dossier_locator: 第36行“One-sentence complete-Idea summary”字段。
    current_problem: >-
      单句依次嵌入病程范围、两类建模输入、模型属性、外部数据库、四项任务、任务三限定和三类证据输出，并以“并……其中……从而……”连续连接；读者需要回读才能确定任务三限定和末尾证据分别附着于哪个动作。
    target_state: >-
      在保持一个句子的前提下，使研究对象、模型构建与外部评价、输出范围形成三个清楚的并列层次，每个限定语紧邻其修饰对象。
    required_change_or_replacement: >-
      将该字段重组为最多三个以分号连接的主干：第一段交代研究对象，第二段交代约束、开发数据库、模型构建和外部应用，第三段交代四项任务及对应输出；任务三说明须紧跟“第三项任务”，末段须补出明确谓语和主语。保持单句字段，不拆成列表或多句，并落实LANG-001与LANG-002的直接表述。
    content_to_preserve: >-
      成人重症监护全病程范围、文献与专家约束、一个开发数据库和一个异质外部数据库、统一低维动态状态模型、四项预定任务、任务三的实测目标限定，以及状态表示、预测用途和失效边界证据。
    acceptance_test: >-
      字段仍为一个句号结束的一句话；至多三个顶层并列主干；“其中第三项”的先行项唯一，“从而”等结果连接词不再悬空，每项证据输出都有明确的产生动作。
  - finding_id: LANG-006
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: task-three-operational-definition
    normalized_locator: working-assumptions-line-333
    failure_mode: user-conversation-provenance-leakage
    fingerprint: "micro|task-three-operational-definition|working-assumptions-line-333|user-conversation-provenance-leakage"
    category: 学术语域与内部工作语境
    dossier_locator: 第333行“任务三的固定操作化说明”。
    current_problem: >-
      “本研究把用户提出的……准则操作化为”把对话来源带入学术正文，使固定设计要素看似依赖一次用户指令，而不是由研究对象和可观测数据边界直接陈述。
    target_state: >-
      只陈述公开数据库缺少潜在状态金标准这一前提，以及任务三由此采用的预先操作化，不提用户、请求或编辑过程。
    required_change_or_replacement: >-
      删除“用户提出的‘给定部分状态或序列，补全未观测的其他状态’准则”及其对话性引导，把段首改为“公开观察性重症监护数据库不提供潜在生理状态金标准，因此任务三预先操作化为：给定遮蔽前及其他未遮蔽的观测历史，预测按预定规则暂时遮蔽、但数据库中实际测得的临床变量。”
    content_to_preserve: >-
      数据库没有潜在生理状态金标准、任务三是固定设计要素、成功仅支持测量补全且不支持潜在状态恢复。
    acceptance_test: >-
      第333行及其他读者可见正文不再出现“用户提出”“用户要求”“根据请求”等对话来源；操作化仍由可观测数据边界直接引出，并完整保留潜在状态不是验证端点的限制。
  - finding_id: LANG-007
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: conditional-follow-up-independence
    normalized_locator: conditional-follow-up-line-185
    failure_mode: double-negation-and-branch-metaphor
    fingerprint: "micro|conditional-follow-up-independence|conditional-follow-up-line-185|double-negation-and-branch-metaphor"
    category: 中文清晰度与隐喻
    dossier_locator: 第185行末句。
    current_problem: >-
      “任一分支不可用不抹去另一满足资格的分支”同时使用“分支”“不可用”“抹去”三个项目或软件隐喻，并形成连续否定；虽然含义可由上下文推知，但读者需要重构为两项后续研究彼此独立的条件判断。
    target_state: >-
      直接说明随机试验分析与动物研究分别依据自身条件决定是否开展，一项不具备条件不影响另一项。
    required_change_or_replacement: >-
      将末句改为“随机试验分析与动物研究分别依据各自条件决定是否开展；其中一项不具备开展条件，不影响另一项在满足自身条件时开展。”
    content_to_preserve: >-
      两项后续研究各有独立资格与后果，一项不能开展时，不自动排除另一项。
    acceptance_test: >-
      句中不再使用“分支”“不可用”或“抹去”表达研究资格；两个研究对象、各自条件和互不影响的关系均有明确主语与谓语，且没有连续否定。
  - finding_id: LANG-008
    severity: minor
    finding_kind: terminology
    finding_level: micro
    finding_scope: occurrence
    scientific_role: animal-study-quality-and-reporting-standards
    normalized_locator: conditional-follow-up-line-185
    failure_mode: undefined-bilingual-short-forms
    fingerprint: "micro|animal-study-quality-and-reporting-standards|conditional-follow-up-line-185|undefined-bilingual-short-forms"
    category: 双语术语首用
    dossier_locator: 第185行“MQTiPSS 与 ARRIVE 2.0”首次出现处；对应参考文献第393–394行。
    current_problem: >-
      “MQTiPSS”仅以缩写出现，“ARRIVE 2.0”也未说明是动物研究报告指南；跨学科目标受众中的临床、系统科学或统计学读者不能仅凭缩写判断两者在句中的语言角色。
    target_state: >-
      首次出现用直接中文说明两项文件分别是临床前脓毒症研究质量标准和动物研究报告指南，并在括号内保留正式短称。
    required_change_or_replacement: >-
      将“符合 MQTiPSS 与 ARRIVE 2.0 的动物研究”改为“符合临床前脓毒症研究最低质量阈值（MQTiPSS）和 ARRIVE 2.0 动物研究报告指南的动物研究”。不翻译或改写正式短称，后文如再出现只使用已定义短称。
    content_to_preserve: >-
      动物研究须同时满足临床前脓毒症研究质量要求和动物研究报告要求，两项正式短称及其版本保持不变。
    acceptance_test: >-
      第185行首次出现时，非动物实验专业读者无需查参考文献即可识别两项标准各自的用途；短称拼写和“2.0”版本在正文与参考文献中一致，且没有引入另一未定义缩写。
    term_or_phrase: MQTiPSS 与 ARRIVE 2.0
    recommended_form_or_plain_description: >-
      临床前脓毒症研究最低质量阈值（MQTiPSS）和 ARRIVE 2.0 动物研究报告指南
    evidence_basis: >-
      本稿参考文献第393行给出Minimum Quality Threshold in Pre-Clinical Sepsis Studies，第394行给出The ARRIVE guidelines 2.0；直接说明两项文件的用途即可满足跨学科读者首用要求，无需改动正式名称。
    first_use_definition: >-
      MQTiPSS是临床前脓毒症研究最低质量阈值，ARRIVE 2.0是动物研究报告指南；两者在本稿中分别承担质量要求与报告要求的角色。
    competing_forms_and_locators: []
unresolved_issues:
  - LANG-001
  - LANG-002
  - LANG-003
  - LANG-004
  - LANG-005
  - LANG-006
  - LANG-007
  - LANG-008
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r007  
**Target Language**: Chinese（含英文数据库名、方法名与缩写）  
**Discipline**: 脓毒症与重症医学、临床人工智能、系统辨识及纵向统计学的交叉研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: minor_language_revision

**Recommendation**: polish

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 7 | pass |
| Terminology Consistency | 6 | borderline |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 6 | borderline |
| Readability & Flow | 6 | borderline |

---

## Hard Gate Status

**Overall**: pass

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 未发现符合硬门定义的明确语法错误模式，约为0个/500个中文词元；局部拗口结构计入可读性问题 |
| Academic register | pass | 仅第333行有一处对话来源泄漏；未在两个或更多章节形成系统性非正式语域 |
| Terminology coherence | pass | 两个核心概念组存在可恢复的形式或修饰语问题，少于三个核心概念不一致阈值；其余问题为局部或次要角色 |
| Tense systematic violation | pass | 作为计划阶段的Idea，方法与预期结果一致使用现在时、将来指向或计划性表达，没有把拟开展研究系统写成已完成结果 |

---

## Strengths

- 标题中的研究对象、开发数据库与异质外部数据库关系直接，复合标题的主要修饰语没有附着到错误对象。
- 第40行及时定义“动态状态模型”“全病程”“受约束”和“外部验证”，并明确区分跨数据库状态表示评价与患者病程中的状态转移。
- 全稿稳定区分计划、预期结果和已存在证据，没有用完成时态暗示研究已经产生结果。
- 数学符号、任务编号、Holm、Brier、Markov和Bernoulli等方法名的中英文形式总体一致，标点与数字格式稳定。
- 任务三多次保留“实测变量”与“潜在生理状态不是验证端点”的语言边界，所需修订是降低表达负担，而不是重新选择科学含义。

---

## Specific Issues

### Chinese Academic Clarity

- **LANG-002（minor）**：第36、47、68、76、87、158、217–219、256、267、286、333行的任务三表述叠加多层限定语，并在任务名、评分目标和结果解释间切换形式；读者能恢复含义，但入口句需要回读。
- **LANG-004（minor）**：第40行“人体开放复杂巨系统”增加装饰性标签，直接的动态临床系统描述已经足够。
- **LANG-005（minor）**：第36行单句摘要主干过多，“其中”和末尾结果连接词的附着范围不够迅速。
- **LANG-007（minor）**：第185行末句以连续否定和“分支／抹去”隐喻表达两项后续研究的独立条件，局部可读性较低。

### Grammar & Syntax

未发现达到硬门或需要单列修复的明确语法错误。局部连续否定和主干拥挤分别记录在LANG-007与LANG-005。

### Academic Register & Tone

- **LANG-006（minor）**：第333行“用户提出的”暴露对话来源，不符合研究方案正文应有的自足语域。
- 其余正文保持正式、克制的计划性语调；机器元数据和固定格式字段未作为语域问题计分。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LANG-001 | 开发状态在外部数据库中的占用和可分离性 | 第36、40、64、72、76、84、87、102、165–169、222–227、315、349行 | “开发状态”可能先被理解为开发进度，“占用”没有立即显出患者比例 | yes |
| LANG-002 | 从部分已观测历史预测被有意遮蔽但实际测得的临床变量 | 第36、47、68、76、87、158、217–219、256、267、286、333行 | 输入、目标、遮蔽操作和解释范围压在一个短语内 | yes |
| LANG-003 | 参数与潜在状态恢复诊断 | 第48、72、83、94、122、134、148、193、204–205、210、244、251、266、274、294、349、363行 | 并列范围不明确，可能误读为“参数”与“潜在状态恢复诊断” | yes |
| LANG-004 | 人体开放复杂巨系统 | 第40行 | 非必要紧凑标签扩大跨学科读者的术语负担 | yes |
| LANG-008 | MQTiPSS 与 ARRIVE 2.0 | 第185行 | 非相邻专业读者不能从短称判断两项标准的用途 | yes |

### Tense & Voice Conventions

未发现问题。拟开展的建模、验证和后续研究使用计划性表达，定义与方法描述使用现在时，二者没有系统混淆。

### Conciseness & Redundancy

- **LANG-002（minor）**：任务三的同一长限定语在多个入口近乎逐字重复；角色化直接表述可同时减少重复和附着歧义。
- **LANG-005（minor）**：单句摘要信息密度高于其入口功能所需，宜在保持一句话的合同限制下重组主干。

### Readability & Flow

- **LANG-001、LANG-003（minor）**：两个跨位置名词短语的修饰语范围不够清楚，影响局部首次阅读速度。
- **LANG-007（minor）**：连续否定和隐喻使一个本可直接陈述的条件关系需要回读。
- 段落间的论证次序和章节功能不在本次语言评估范围内，未据此评分或提出修改。

---

## Language Revision Priorities

1. **Terminology and modifier attachment**: 5 issues — 先处理LANG-001至LANG-004及LANG-008的首次定义、直接描述和全篇一致性，再复核每个替换短语的修饰对象。
2. **Concision and local readability**: 2 issues — 按LANG-005重组单句摘要，按LANG-007消除连续否定和分支隐喻。
3. **Academic register**: 1 issue — 按LANG-006删除对用户或请求来源的引用，使操作化说明自足。

---

## Assessment Notes

- 目标读者基线取自第37行嵌入式受众说明：脓毒症与重症医学、系统科学与系统辨识、临床人工智能、临床方法学与统计学研究者，以及医学期刊编辑和同行评审者。因此，对跨学科读者不透明的简称需要首次说明，但没有要求解释该受众通常掌握的全部统计方法。
- 评估覆盖完整dossier的读者可见正文与自由标签。研究构想合同固定的15个二级标题、5个推理三级标题、第1节与结构式摘要字段名、证据链字段名、Claim-Support表头及机器元数据没有被翻译、重命名或作为语言问题计分。
- 候选扫描只用于提示复核；报告没有保留完整术语清单，也没有把专名、引文或固定格式字段本身当作问题。
- 本次只评价语法、语域、术语、时态、简洁性和局部可读性；未评价科学有效性、创新性、影响、可行性、论证结构或章节编排，也未改动源dossier。
