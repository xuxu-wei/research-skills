---
review_id: language-assessment-I01-001-r088
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-academic-language-assessor-r088
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r088
input_artifact_ids:
  - idea-dossier-I01-001-v047
input_versions:
  - v047
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v047
  version: v047
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v13/idea-dossier-v047.md
reader_handoff:
  artifact_id: embedded-reader-handoff
  version: embedded
  path: null
  target_language: zh-CN
  disciplines: 重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学人工智能、转化研究
  reader_prior_knowledge: 读者各自在本领域受过研究训练，但不假定理解项目内部状态词、未定义缩写、跨学科自造词或非标准复合术语；应能先由标题、摘要和研究问题把握主线，再进入技术细节。
files_read:
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v13/idea-dossier-v047.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: R088-T01
    severity: major
    finding_kind: terminology
    category: 术语的标准含义与跨学科可理解性
    dossier_locator: "第 45 行 Objective and hypothesis；第 93 行 Twenty-four-month minimum and dated decisions 首段；相关简称见第 98、107、135、166、293、344、438、458 行"
    current_problem: “双库可观测性审计”把系统辨识中已有明确技术含义的“可观测性”用于数据库访问、事件与转移数量、医院覆盖、时间戳、共同指标、接口和缺失情况的综合审计；系统辨识读者可能误以为这里检验的是能否由输出推断全部系统状态，而摘要没有及时排除这一读法。“G1 审计”随后又以内部简称替代其科学内容。
    target_state: 首次进入摘要时直接说明这是两个数据库的数据可用性和分析支持度审计；只有在确实检验动态系统的正式可观测性条件时才使用“可观测性”。
    required_change_or_replacement: 在第 45 行改用“两个数据库的数据可用性与分析支持度审计”；首次引入 G1 时写明审计所含的事件与转移、医院、时间戳、共同生理指标、接口和缺失支持，之后统一使用“G1 数据支持审计”。逐处检查相关简称，不得仅替换示例行。
    content_to_preserve: 保留该审计在月 6 前决定共同变量、时间网格、候选复杂度以及是否继续跨数据库分析的全部功能和停止后果；不得改动任何阈值。
    acceptance_test: 全篇检索“可观测性”“双库观测”“G1 审计”“数据支持审计”；所有指向数据库可用性和支持度检查的实例统一为自解释形式或已定义的“G1 数据支持审计”，且“可观测性”只在明确给出状态—输出可推断含义时出现。由系统辨识与临床流行病学读者各自阅读第 45 行即可说出审计对象而不会把它解释为系统可观测性检验。
    term_or_phrase: 双库可观测性审计
    recommended_form_or_plain_description: 两个数据库的数据可用性与分析支持度审计；定义后可简称 G1 数据支持审计
    evidence_basis: "系统辨识的权威方法说明把 observability 定义为能够由系统输出获知全部状态，并以状态空间模型的可观测性矩阵刻画（MathWorks Control System Toolbox: https://uk.mathworks.com/help/control/ref/statespacemodel.obsv.html）。dossier 第 93、153–166 行列出的实际审计对象主要是数据访问、事件支持、医院覆盖、时间戳、共同生理指标、接口和缺失，并非该正式性质，因此直接描述更准确。"
    first_use_definition: “先在两个数据库中审计数据访问、事件与转移数量、医院覆盖、时间戳、共同生理指标、接口和缺失情况，以决定可执行队列、时间网格和模型复杂度（下称 G1 数据支持审计）。”
    competing_forms_and_locators:
      - “双库可观测性审计”（第 45 行）
      - “双库可观测性与数据支持审计（G1 审计）”（第 93 行）
      - “双库观测和变量用途审计”（第 47 行）
      - “G1 审计”（第 98、107、135、166、263、293、296、307、344、347、359、394、419、433、438、458 行）
  - finding_id: R088-T02
    severity: major
    finding_kind: terminology
    category: 核心检验名称与临床语义区分
    dossier_locator: "第 38 行 One-sentence complete-Idea summary 首次出现“绝对模拟恢复”；第 40、45、47、70、82、87、99、108、120、225、227–239、315、347、361、368、390、394–396、419、432、440 行相关实例"
    current_problem: “绝对恢复/绝对模拟恢复”不是跨学科读者可立即识别的标准检验名；在脓毒症 dossier 中又与第 213 行“生理恢复”并存，临床读者在摘要入口可能误把它理解为患者绝对恢复，而不是用模拟数据评价潜在状态、转移与结构能否按预设阈值恢复。
    target_state: 用标准的“模拟恢复检验”作总称，并在首次出现处写明被恢复的科学对象和“绝对”所指的是预设判定阈值，而不是患者结局或相对性能比较。
    required_change_or_replacement: 在第 38 行以一个自足短语定义“用模拟数据按预设绝对阈值检验潜在状态、转移概率和预设结构能否被正确恢复（下称模拟恢复检验）”；后文总称统一为“模拟恢复检验”，具体结果分别写“状态恢复”“转移概率误差”“边检测错误率”“区间覆盖”等。删除裸用的“绝对恢复”，并保留“生理恢复”专指临床状态。
    content_to_preserve: 保留正确指定、零边、过拟合、遗漏状态、错误滞后、错误观测模型、至少 1,000 次重复或 MCSE 标准，以及第 233–239 行所有数值阈值和失败处置。
    acceptance_test: 全篇检索“绝对恢复”“绝对模拟恢复”“模拟恢复”“生理恢复”和裸用“恢复”；总检验只保留已定义的“模拟恢复检验”，每个分项恢复均有明确对象，“生理恢复”只指患者状态。第 38、45、47 行在不查阅第 227–239 行时也能让读者识别检验对象、数据来源和绝对阈值的含义。
    term_or_phrase: 绝对恢复／绝对模拟恢复
    recommended_form_or_plain_description: 模拟恢复检验，即用预设生成机制的数据按预设绝对阈值评价潜在状态、转移概率和预设结构的恢复误差、错误率与区间覆盖
    evidence_basis: "模拟研究的方法学指南要求明确数据生成机制、估计目标、方法和性能量，并使用偏差、覆盖率等可解释指标及其 Monte Carlo 不确定性（Morris, White, Crowther, 2019: https://pmc.ncbi.nlm.nih.gov/articles/PMC6492164/）；计算模型方法指南使用 parameter recovery 指称从模拟数据恢复生成参数的检查（Wilson & Collins, 2019: https://pmc.ncbi.nlm.nih.gov/articles/PMC6879303/）。这些来源支持“模拟恢复检验+具体性能量”的表达，但不支持让“绝对恢复”在临床语境中独立充当检验名。"
    first_use_definition: “用预设生成机制的模拟数据，按事先规定的误差、覆盖率和错误结构阈值检验潜在状态、转移概率及预设结构能否被正确恢复（下称模拟恢复检验）。”
    competing_forms_and_locators:
      - “绝对模拟恢复”（第 38 行）
      - “绝对恢复检验”（第 40、45、70、82、99 行）
      - “绝对恢复”（第 47、87、108、120、225、347、361、368、390、419、440 行）
      - “模拟恢复”（第 227–239、298、315、432 行）
  - finding_id: R088-T03
    severity: major
    finding_kind: terminology
    category: 失败指标的可解释命名
    dossier_locator: "第 47 行 Expected result 首次出现“错误高置信检查”；第 99、120、225、237–238、298、347、361、368、390、419、440 行相关实例"
    current_problem: “错误高置信”把错误对象、判定依据和统计量压缩在一个非标准复合标签中。第 237 行实际测量零边场景下假边置信区间排除 0 的重复比例，第 238 行又测量错设场景下错误结构被高置信支持的比例；二者条件和指标不同，摘要中的同一标签不能让读者知道所指哪一项。
    target_state: 每次都写明生成场景、错误对象、判定规则和重复比例；若需要总称，使用自解释的“错误结构支持率检查”，并立即列明所含两类指标。
    required_change_or_replacement: 第 47 行改为直接描述“检查在零边或错设场景中错误结构仍被置信区间或预设判定规则支持的重复比例”；第 99、120、225、237–238、298、347、361、368、390、419、440 行分别按零边假边和错设错误结构两类指标展开，不再裸用“错误高置信”。
    content_to_preserve: 保留假边的 95% 区间排除 0 的重复比例不超过 0.05、错设下错误结构高置信比例不超过 0.05、至少 80% 重复触发失配或停止解释，以及所有相应停止处置。
    acceptance_test: 全篇检索“错误高置信”“错误结构”“零边”和“错设”；不得再出现未说明对象与统计规则的“错误高置信”。每一处均能回答“在哪种生成场景、什么错误、由何规则判定、统计哪个比例”，且第 237 与 238 行的两类性能量不被合并。
    term_or_phrase: 错误高置信
    recommended_form_or_plain_description: 在零边或错设生成场景中，错误结构仍被置信区间或预设判定规则支持的重复比例
    evidence_basis: "Morris 等的模拟研究指南主张按研究目的明确性能量，并分别报告偏差、覆盖率、错误率及 Monte Carlo 误差（https://pmc.ncbi.nlm.nih.gov/articles/PMC6492164/）。dossier 第 237–238 行已经给出两个不同且可直接命名的指标，因此无需保留不能指出场景和统计规则的复合标签。"
    first_use_definition: 不建议保留新的短标签；首次出现即写成“在零边或错设生成场景中，错误结构仍被置信区间或预设规则支持的重复比例”。
    competing_forms_and_locators:
      - “错误高置信检查”（第 47 行）
      - “零边错误高置信”（第 99、347、368 行）
      - “错设下错误高置信”（第 238 行）
      - “错误结构高置信比例”（第 238 行）
      - “错误高置信基准”（第 361 行）
  - finding_id: R088-T04
    severity: major
    finding_kind: terminology
    category: 后果术语的角色分离
    dossier_locator: "第 47 行 Expected result 首次出现“弃权记录”；第 120、225、238、298、316、330、347、361、368、381、390、397、440 行相关诊断、处置与记录"
    current_problem: 机器学习中的“弃权”通常指模型在个体样本上拒绝输出预测；本 dossier 却让它交替指模型失配信号、分析者删除或合并状态、停止解释某条边、把结构标为数据库特异以及保存处置记录。该词因而同时承担诊断、决定、对象状态和记录四种角色，跨学科读者无法从“弃权记录”判断谁因何停止对什么作何结论。
    target_state: 分别使用“触发失配判定”“停止解释相应状态或边”“不保留该复杂候选”“标记为数据库或照护政策特异”和“记录不再解释的项目及原因”等带有主体、对象和后果的直接表达。
    required_change_or_replacement: 逐处根据实际角色替换“弃权”：第 238 行写清诊断触发比例与随后停止解释的对象；第 225、298、316、330、347、361、368、381、390、397、440 行写清删除、合并、停止解释、限制外推或记录原因中的具体一项。除非 dossier 真正引入模型对个体病例拒绝预测的机制，否则不再使用“弃权”。
    content_to_preserve: 保留所有失配阈值、状态或边的删除/合并规则、简单表征后备方案、数据库或照护政策特异标记，以及失败仍形成可复用记录的原则。
    acceptance_test: 全篇检索“弃权”“失配”“删除”“合并”“停止解释”“不再保留”“特异”和“记录”；每一项失败后果都明确触发者、受影响的状态/边/候选表征及允许报告的范围。若仍保留“弃权”，它只能指模型对个体预测拒绝输出且须在首次出现处定义；否则该词出现次数应为 0。
    term_or_phrase: 弃权／弃权记录
    recommended_form_or_plain_description: 按实际角色分别写明触发失配判定、停止解释相应状态或边、不保留候选表征、限制跨数据库解释或记录停止解释的项目及原因
    evidence_basis: "机器学习综述把 reject option/abstention 定义为模型在认为可能出错时拒绝对测试样本作出预测，并讨论预测质量与拒绝比例的权衡（Hendrickx et al., 2021: https://arxiv.org/abs/2107.11277）。dossier 并未在上述各处描述这一单一机制，而是描述多种分析处置，因此直接写明角色和后果是更可靠的跨学科表达。"
    first_use_definition: 不建议把“弃权”作为总称；第 47 行应直接写“记录因失配、不稳定或外部不一致而不再保留或解释的状态、边及候选表征，并注明触发标准和允许报告的范围”。
    competing_forms_and_locators:
      - “弃权记录”（第 47、120、298、330、361 行）
      - “失配或弃权”（第 238 行）
      - “删除、合并或标明为数据库或照护政策特异”（第 225 行）
      - “停止结构解释”（第 234 行）
      - “不再保留复杂候选／只解释已经恢复的不变量”（第 237–238 行）
      - “状态或边被弃权”（第 381 行）
  - finding_id: R088-T05
    severity: minor
    finding_kind: terminology
    category: 外部评价数据与操作的术语一致性
    dossier_locator: "第 38 行 One-sentence complete-Idea summary；第 40、45–48、62、70、82、87、97–101、111、113、122、135、141、147、202、229、241–251、267、299、328–331、347、350–351、362、371、379–380、384、390、396、406–409、417–419、426、432–446、459–460 行"
    current_problem: dossier 交替使用“未触碰外部测试数据”“未接触外部结果”“未触碰数据库外测试”“未触碰跨数据库结果”“最终测试数据只访问一次”和“零更新外部检验”。“未触碰”若按字面理解会与第 251 行的一次性访问冲突；数据在模型开发期间的隔离状态、使用固定模型进行的评价操作及评价后产生的结果没有稳定分名。
    target_state: 将三个角色分开：模型开发与选择期间保持隔离的外部测试集；在该数据上使用原固定模型进行的外部性能评价；评价完成后得到的外部结果。把“零更新”只用于说明评价时不重新拟合或更新参数。
    required_change_or_replacement: 第 38 行首次写为“在模型开发与选择期间保持隔离的外部测试集上评价固定模型”；第 46 行定义“使用原固定模型、不重新拟合或更新参数的外部性能评价（下称零更新外部评价）”。后文统一以“隔离外部测试集”指数据，以“零更新外部评价”指操作，以“外部评价结果”指输出；适配区则在首次出现时说明只用于预先限定的再校准或观测层更新。
    content_to_preserve: 保留医院优先分区、适配区与最终测试区比例、患者不跨集合、规范固定、一次性访问顺序、仅重新校准、仅更新观测层和完整重拟合的层级区别，以及所有失败后果。
    acceptance_test: 全篇检索“未触碰”“未接触”“最终测试”“零更新”“外部检验”“外部评价”“适配区”；每个实例都能唯一归入数据、操作或结果之一。不得再用“未触碰/未接触”描述已经执行评价后的数据或结果；“零更新外部评价”每次都指原固定模型且不含重新校准或观测层更新。
    term_or_phrase: 未触碰／未接触外部测试数据（结果）；零更新外部检验
    recommended_form_or_plain_description: 模型开发与选择期间保持隔离的外部测试集；使用原固定模型且不重新拟合或更新参数的外部性能评价（零更新外部评价）
    evidence_basis: "临床预测模型方法指南将外部验证说明为在未用于模型开发的不同但相关数据中评价原模型的预测性能，并明确它不等于重新拟合模型（Riley et al., 2024: https://pmc.ncbi.nlm.nih.gov/articles/PMC10788734/）；TRIPOD+AI 还建议用 evaluation data 避免 validation data 在调参与性能评价之间的歧义（https://www.bmj.com/content/385/bmj-2023-078378）。这些定义支持按“隔离数据—固定模型评价—评价结果”分名。"
    first_use_definition: “外部数据库按医院分为仅供预定有限调适的适配区，以及在模型开发、选择和阈值固定期间保持隔离的最终测试区；在后者上使用原固定模型且不更新任何参数的评价称为零更新外部评价。”
    competing_forms_and_locators:
      - “未触碰外部测试数据”（第 38、46 行）
      - “未接触外部结果”（第 40、113 行）
      - “未触碰数据库外测试”（第 45 行）
      - “未触碰跨数据库结果”（第 47、122、362 行）
      - “零更新外部检验”（第 46、48、70、101、111、202、251、329、350、371、379–380、396、418、442 行）
      - “最终测试数据只访问一次”（第 251 行）
  - finding_id: R088-T06
    severity: minor
    finding_kind: terminology
    category: 核心对象名称完整性
    dossier_locator: "第 45 行 Objective and hypothesis 首次出现“受限复杂候选”；第 82、99、108、120、125、141、166、225、227–239、251、296–298、316、347、361、368、378–381、390、426、432、440、460 行相关实例"
    current_problem: “复杂候选”“受限复杂候选”“复杂切换或非线性候选”省略了中心名词，读者需猜测所指是候选模型、候选结构还是候选动态系统表征；后文三者承担的处置并不完全相同。
    target_state: 在首次出现处写出完整科学对象；只有在同一局部语境中指代明确时才使用统一短称，并把模型拟合实体、结构解释和总体候选表征分开。
    required_change_or_replacement: 第 45 行写为“受限的复杂候选动态系统表征”；第 99 行若指切换或非线性模型则写“复杂候选模型”；涉及边、符号或滞后时写“候选结构”。先确定每处实际对象，再统一同一对象的名称，不得用一个省略中心词的“候选”覆盖三种角色。
    content_to_preserve: 保留至多保留一个复杂候选、复杂度受 G1 审计约束、失败时退回简单表征以及模型、结构和总体表征各自的处置。
    acceptance_test: 全篇检索“复杂候选”“受限复杂候选”“非线性候选”“切换候选”“候选模型”“候选结构”和“候选表征”；每一处都有明确中心名词，且同一科学对象只有一个首选名称。修订后第 45、99、120、225、237–238 行不得让读者在模型、结构和总体表征之间猜测指代。
    term_or_phrase: 复杂候选／受限复杂候选
    recommended_form_or_plain_description: 按对象分别使用“复杂候选动态系统表征”“复杂候选模型”或“候选结构”，不得省略中心名词
    evidence_basis: 该问题可由 dossier 内部角色对照直接确认：第 45 行指总体表征，第 99 行指切换或非线性模型，第 237–238 行处置结构解释，而裸用“复杂候选”不能区分这些对象；直接补出中心名词比另造总称更清楚。
    first_use_definition: “受限的复杂候选动态系统表征，即仅在数据支持审计和模拟恢复检验均达到预设标准后才保留的切换或非线性表征。”
    competing_forms_and_locators:
      - “受限复杂候选”（第 45 行）
      - “复杂切换或非线性候选”（第 99 行）
      - “复杂候选”（第 108、120、125、225、237、361、368、378、426、432、460 行）
      - “复杂结构”（第 99、108、225、368、440 行）
  - finding_id: R088-L01
    severity: minor
    finding_kind: language
    category: 中文学术清晰度与读者入口
    dossier_locator: 第 38 行 One-sentence complete-Idea summary
    current_problem: 单句连续承载研究对象、24 个月时限、知识来源、候选表征、两个主要任务、模拟恢复、外部测试隔离、证据贡献和条件性试验分析，主干被“并通过……形成……”及多层并列成分掩埋；跨学科读者需在首次入口回读才能区分主体研究和后续条件性分析。
    target_state: 保持合同要求的一个完整句子，但用清楚的主干和不超过五个按顺序组织的信息块呈现研究对象、主体研究、两个主要任务、隔离外部评价和条件性后续分析。
    required_change_or_replacement: 在不增加第二句的前提下，先给“本研究计划构建并检验什么”，再给两个主要任务和隔离外部评价，最后用一个分号引出条件满足后的分试验次要分析；删除可由 structured abstract 承担的“形成可审计的证据整合、验证、基准与可复用资源贡献”等定位枚举，并用 R088-T02、T05 的自解释术语替换压缩标签。
    content_to_preserve: 保留计划而非既有结果的证据状态、24 个月主体研究、发病前与发病后两个主要结局、固定模型的隔离外部评价，以及主体研究达标且试验数据和语义可用后才开展分试验次要分析。
    acceptance_test: 该字段仍为一个列表项中的一个完整句子；依次只含“对象与计划—两个主要任务—隔离外部评价—条件性试验分析”四个主信息块，主体研究与后续分析之间有明确边界，不再出现连续两层以上的“以……构建并检验……评价……并通过……形成……”套叠。读者只读此句即可复述研究对象、两项主要任务、外部证据状态和后续分析条件。
  - finding_id: R088-L02
    severity: minor
    finding_kind: language
    category: 可读性与局部信息组织
    dossier_locator: "第 225 行 Observational target, anchoring, missingness, and abstention 第二段；第 267 行 观测映射成立时的分析第二段；第 444 行 Limitations and boundary conditions 第 8 项"
    current_problem: 三处各自在一个段落或编号项内并列多个科学层次：第 225 行混合缺失模型、敏感性参数、行动重叠阈值和结构处置；第 267 行混合外部映射检验、五组数值标准、试验数据可计算性和失败判定；第 444 行混合授权、语义、人群边界、稀疏访视、试验合并和推广边界。数值虽明确，但局部主题焦点不稳定。
    target_state: 每处按科学功能拆成短句或同一节内的项目表，使每个句子只承担一种操作：方法、判定阈值、失败后果或解释边界。
    required_change_or_replacement: 第 225 行依次拆为“缺失机制与敏感性”“行动重叠与 ESS”“状态或边的保留条件”三个段落或列表项；第 267 行拆为“外部映射性能”“各锚点校准”“试验数据可计算性”“失败条件”四组；第 444 行在同一编号 8 内拆成授权与语义、人群边界、访视与合并限制、推广边界四句。只重组语言，不增删任何科学条件。
    content_to_preserve: 保留所有模型名称、delta 水平、重叠与 ESS 阈值、对齐/保留/校准阈值、试验访视和语义条件、人群限制以及监管边界；保持 limitations 仍为一个权威编号位置。
    acceptance_test: 第 225、267、444 行对应内容均已拆分；每个新句或列表项只回答“采用什么方法”“达到什么标准”“失败后如何处置”或“结论限于何处”中的一项。逐项核对原有数字、方向符号、访视日和停止后果，数量与数值均不变。
unresolved_issues:
  - R088-T01
  - R088-T02
  - R088-T03
  - R088-T04
  - R088-T05
  - R088-T06
  - R088-L01
  - R088-L02
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r088  
**Target Language**: Chinese (zh-CN)  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学人工智能与转化研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier（完整 dossier）  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

正文的语法、学术语域和计划性时态总体成熟；当前阻断点集中在读者入口和关键失败后果中的术语。若干标签在系统辨识、模拟研究或机器学习中已有不同的标准含义，或把多个科学角色压成一个内部短称，因此跨学科读者尚不能仅凭标题、摘要和研究问题稳定进入技术主线。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 9 | pass |
| Academic Register & Tone | 9 | pass |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 6 | borderline |
| Readability & Flow | 6 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 完整阅读未发现明确语法错误，远低于每 500 词 3 个错误的门槛；中文未作伪精确分词换算。 |
| Academic register | pass | 各节保持正式、客观的学术语域；未见两个以上章节的系统性口语化。 |
| Terminology coherence | fail | 失败依据不是合同固定英文标签，而是至少四组控制核心设计或失败后果的读者用语：“可观测性审计”“绝对恢复”“错误高置信”“弃权”。前两组已进入摘要，后两组控制候选结构的保留或停止解释，却没有及时给出跨学科可识别的含义。 |
| Tense systematic violation | pass | dossier 是计划性研究，全文以“计划、须、若……则”等前瞻表达描述拟开展工作，没有把拟议方法或结果系统写成已经完成。 |

---

## Strengths

1. 计划状态与证据状态区分清楚：摘要第 47 行和资源表第 141 行明确说明模型、模拟、预测和外部测试结果尚未生成。
2. 因果措辞受到持续约束：第 76、87、221、269、273、381–384、450 行稳定区分预测、观察性关系、随机化扰动与治疗因果效应。
3. 缩写多数在首次实质性使用时定义，且数据库、临床结局、统计指标和时间单位的中英文形式总体稳定。
4. 方法与停止后果大量使用可检查的数值阈值，避免了“显著提升”“重大突破”等宣传性或含混措辞。
5. 各节的计划性时态和客观语态与 Idea dossier 的预研究性质一致。

---

## Specific Issues

### Chinese Academic Clarity

- **R088-L01（minor）**：第 38 行的一句式完整摘要信息块过多，主体研究与条件性后续分析的边界在首次阅读时不够突出。完整的单句约束、保留内容和验收方法见 frontmatter。
- **R088-L02（minor）**：第 225、267、444 行把方法、阈值、失败处置和解释边界集中在同一局部段落。应只做局部拆分，不改变条件、数字或 limitations 的权威位置。

### Grammar & Syntax

未发现需要单独修订的明确语法错误。公式、表格短语和合同固定字段没有被误计为句法错误。

### Academic Register & Tone

未发现系统性口语、修辞性提问、夸张评价或宣传性措辞。个别直接表达不构成语域问题。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| R088-T01 | 双库可观测性审计 | 第 45、93 行及 G1 相关实例 | 系统辨识读者会优先按状态—输出可观测性理解，而实际审计对象主要是数据可用性与支持度 | yes |
| R088-T02 | 绝对恢复／绝对模拟恢复 | 第 38 行首次出现；第 40、45、47 行及全文相关实例 | 临床读者可能与“生理恢复”混淆，也不能从名称识别模拟对象和绝对阈值 | yes |
| R088-T03 | 错误高置信 | 第 47、99、237–238 行及相关实例 | 不同生成场景和不同错误指标被压成同一标签 | yes |
| R088-T04 | 弃权／弃权记录 | 第 47、120、225、238 行及相关后果 | 在预测拒绝、失配诊断、结构处置和记录之间角色漂移 | yes |
| R088-T05 | 未触碰／未接触外部数据（结果）；零更新外部检验 | 第 38、40、45–48、241–251 行及相关实例 | 数据隔离状态、固定模型评价操作和评价后结果没有稳定分名 | yes |
| R088-T06 | 复杂候选／受限复杂候选 | 第 45、99、120、225、237–238 行及相关实例 | 省略中心名词，无法稳定区分模型、结构和总体表征 | yes |

候选扫描中的标准数据库名、常见统计缩写、数学符号以及 research-idea.v3 合同固定标题和字段均已排除，不形成术语清单或语言问题。

### Tense & Voice Conventions

未发现系统性时态或语态问题。前瞻性计划使用将来或规范性表达，既有证据使用现在时或完成状态，二者区分稳定。

### Conciseness & Redundancy

- R088-L01 涉及读者入口的一句式过载，应在保持一个完整句子的前提下删去可由后续结构化摘要承担的定位枚举。
- 未把 limitations 中科学上不同的边界条件判作冗余，也未指定应从哪个推理位置删除限制。

### Readability & Flow

- R088-L02 的三个局部段落适合按“方法—阈值—失败后果—解释边界”拆分；这属于局部信息组织，不涉及章节顺序或论证结构判断。
- 标题本身保留了“候选”和“计划”两个证据状态限定；主要可读性障碍来自紧随其后的摘要术语和句内负荷，而非标题格式。

---

## Language Revision Priorities

1. **术语标准性与首次定义**：先处理 R088-T01 至 T04，使摘要和失败后果不再依赖跨学科读者无法共享的内部短称。
2. **外部评价与核心对象分名**：处理 R088-T05、T06，稳定区分数据、操作、结果以及模型、结构、总体表征。
3. **中文读者入口与局部可读性**：最后处理 R088-L01、L02；保持合同字段数量、单句摘要和所有科学阈值不变。

---

## Re-Assessment Status (if applicable)

本次为完整 Idea dossier 的全新独立评估，不读取也不比较任何既往问题清单、分数、决定、版本差异或修订报告，因此本节不作 resolved/remaining/new 分类。

---

## Assessment Notes

- **独立性与范围**：本次只评价冻结 v047 的学术语言，不判断科学有效性、创新性、可行性、论证质量或期刊适配性；未修改 dossier。
- **项目输入边界**：唯一文件型项目输入为 `idea-dossier-v047.md`；reader handoff 为本任务内嵌信息，`path: null`，未虚构为输入文件或 artifact。未读取原稿、差异文件、register、既往语言或叙事报告、repair plan、writer brief、preflight、evaluation、测试脚本或预期结论。
- **完整阅读与分段**：dossier 共 503 行、79,556 字节，按第 1–125、126–250、251–375、376–503 行四段连续读取，四段均无输出截断。正文 15 个 H2、五段推理 H3、结构化摘要、全部表格、limitations 和 references 均已覆盖。
- **规范文件读取**：首次并行回读六个规范文件时工具输出发生截断且编码失真；该次输出未作为评估依据。随后以 UTF-8 将 rubric、hard gates、中文约定、跨学科约定、术语规范和模板逐文件完整重读，均无截断。`SKILL.md` 也已完整读取。frontmatter 的 `files_read` 是实际完整读取的文件清单。
- **候选扫描**：已运行规定的 bounded candidate scanner，并逐一处置 reader-entry 与 consequence 组中的紧凑标签；扫描结果未持久化，也未转成术语清单。只对触发歧义、非标准性、跨学科不可达或角色漂移的术语作 focused verification。
- **外部核验边界**：外部来源只用于核验触发术语的既有含义，不是项目输入，也不列入 `files_read`。核验优先采用权威方法说明、报告指南和方法学综述；没有以“搜不到完整复合短语”作为非标准性的证据。
- **评分假定**：未指定目标期刊，按中文生物医学/临床研究、纵向统计、系统辨识和医学人工智能的交叉学术写作约定评分。对计划性 Idea dossier 不套用已完成 Methods/Results 的过去时要求。

