---
review_id: language-assessment-I01-001-r108
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-academic-language-assessor-r108
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r108
input_artifact_ids:
  - idea-dossier-I01-001-v051
input_versions:
  - v051
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v051
  version: v051
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md
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
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
coverage_receipt:
  reader_entry:
    status: completed
    reviewed_count: 10
    basis: >-
      逐一检查标题、完整想法摘要、受众与定位、结构式摘要六个字段、主要研究问题和核心假设；每个句内的研究对象、操作、目标量与解释后果均检查至句末。
  core_scientific_role:
    status: completed
    reviewed_count: 27
    basis: >-
      对全文实际出现的 27 个研究对象、测量、推断目标、分析操作、检验结果和条件性输出角色核对其所有读者可见名称；未把未出现的角色强加给文本。
  terminology_concordance:
    status: completed
    reviewed_count: 14
    basis: >-
      对普通阅读和有界扫描触发的 14 个概念簇完成全文首用、角色区分、复合修饰和跨位置一致性检查；扫描命中仅作注意提示，只有经语义确认的问题写入 findings。
  local_language:
    status: completed
    reviewed_count: 319
    basis: >-
      检查除 15 个固定 H2 标题和 5 个固定推理 H3 标题外的全部 319 个正文、自由标签、表格、列表和参考文献单元，覆盖语法、语体、时态、局部清晰度与重复。
findings:
  - finding_id: LANG-R108-001
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: physiological-anchor-variables
    normalized_locator: first-use-and-observation-mapping
    failure_mode: role-collapsing-anchor-label
    fingerprint: "meso|physiological-anchor-variables|first-use-and-observation-mapping|role-collapsing-anchor-label"
    category: 术语可及性与角色一致性
    dossier_locator:
      - "Structured abstract，Objective and hypothesis（第 45 行）"
      - "Current resource and result status 及 support audit（第 100、110、138、141、165–168 行）"
      - "Observational target, anchoring, and evidence-qualified interpretation（第 224–226 行）"
      - "Conditional trial-observation mapping and independent analysis（第 273、275、277 行）"
      - "Key techniques and implementation（第 303、307 行）"
    current_problem: >-
      “锚点预测”在核心假设中首次出现时没有说明锚点是跨数据库可比的生理测量变量；后文又用“锚点”“共同锚点”“观测锚点”和“实测锚点”分别或交替指变量、观测值与预测对象。跨学科读者无法仅凭这些短语稳定判断每处所指的科学角色。
    target_state: >-
      首次出现时定义共同生理锚点，并在全文明确区分锚点变量、锚点观测值和锚点预测值；允许定义后使用简短形式，但同一形式不得跨越这三个角色。
    required_change_or_replacement: >-
      将第 45 行的“锚点预测”改为“对跨数据库共同生理测量变量（共同生理锚点）的预测”。定义后，变量一律称“共同生理锚点变量”或已定义的“共同锚点”，实际测得的数值称“锚点观测值”，模型输出称“锚点预测值”；第 277 行的“观测锚点/实测锚点”须依其实际角色改为“锚点观测值”或“具有实测值的共同生理锚点变量”。
    content_to_preserve: >-
      保留双库审计、每维至少两个锚点、单位与时间语义、覆盖率、载荷与尺度约束、试验映射资格、观测方程及全部数值阈值，不改变变量是否合格或如何进入模型的科学规则。
    acceptance_test: >-
      从第 45 行起全文检索所有含“锚点”的读者可见表述；每一处均能唯一归入变量、观测值或预测值三类之一，首次定义先于任何短形式，且第 277 行不再用同一个名词同时表示变量和数值。
    term_or_phrase: 锚点；共同锚点；锚点预测；观测锚点；实测锚点
    recommended_form_or_plain_description: >-
      共同生理锚点变量；锚点观测值；锚点预测值。
    evidence_basis: >-
      第 45、89、224、226 和 303 行把“锚点预测”列为目标量，第 141、165–168、273 和 307 行把锚点写成变量，第 277 行又把“观测锚点/实测锚点”写成可落入范围或用于计算的值；这一角色切换对给定跨学科读者不透明。建议采用直接描述，不依赖另一个项目短标签。
    first_use_definition: >-
      “共同生理锚点是指在两个重症监护数据库中均通过单位、测量语义、时间戳和可见性审计，可用于锚定潜在状态的实测生理变量。”
    competing_forms_and_locators:
      - "“锚点预测”：第 45、89、224、226、303 行"
      - "未限定角色的“锚点”：第 100、102、138、165–168、177–178、215、217、226、265、290、322、352、378、453、472 行"
      - "“共同锚点/共同生理锚点/候选共同锚点集”：第 110、141、256、271、273、277、307、336、361、382、460 行"
      - "“观测锚点/实测锚点”：第 277 行"
  - finding_id: LANG-R108-002
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: secondary-representation-diagnostics
    normalized_locator: abstract-objectives-and-diagnostics
    failure_mode: unnamed-and-inconsistent-diagnostics
    fingerprint: "meso|secondary-representation-diagnostics|abstract-objectives-and-diagnostics|unnamed-and-inconsistent-diagnostics"
    category: 核心输出命名一致性
    dossier_locator:
      - "Structured abstract，Expected result（第 47 行）"
      - "Objective 3 及 work packages（第 82、124、128 行）"
      - "Protocol locks 及 Secondary representation diagnostics（第 205、292–294 行）"
      - "Evidence chain、required analyses 和 evidence ladder（第 330–331、357、372、407 行）"
    current_problem: >-
      首两次出现只称“两项次要表示诊断”，没有说是哪两项；后文在“表示/表征”“伪遮蔽重建/部分状态重建”“未来轨迹诊断”之间切换。读者可能把“部分状态重建”误读为潜在状态恢复，而非对原已测生理值进行伪遮蔽后的重建诊断。
    target_state: >-
      首次出现即给出两项诊断的直接名称，全文统一使用“表征”，并使伪遮蔽重建与未来轨迹预测始终保持为两个不同的次要诊断。
    required_change_or_replacement: >-
      将第 47 行改为“两项次要表征诊断（对原已测生理值的伪遮蔽重建诊断，以及未来轨迹预测诊断）”；后文统一用“伪遮蔽重建诊断”和“未来轨迹预测诊断”。第 62、76、82 和 205 行凡以“表示”指 representation 者改为“表征”，但不得改动数学符号或普通动词“表示”。
    content_to_preserve: >-
      保留两项诊断的次要地位、伪遮蔽仅作用于原已测值、各自的评分与覆盖指标、分层报告方式，以及它们不能改变主要任务或阶段 II 判定的边界。
    acceptance_test: >-
      全文只能找到一个首次定义和两个稳定的诊断名称；“部分状态重建”和术语意义上的“表示诊断”不再出现，且每一处“两项次要诊断”均可追溯到这两个名称。
    term_or_phrase: 两项次要表示诊断；伪遮蔽重建；部分状态重建；未来轨迹诊断
    recommended_form_or_plain_description: >-
      两项次要表征诊断：对原已测生理值的伪遮蔽重建诊断；未来轨迹预测诊断。
    evidence_basis: >-
      第 47、82 和 205 行未命名两项诊断，第 124、294 和 330 行才显示其内容；同一概念族同时使用“表示”和“表征”，且“部分状态重建”与阶段 II 的状态恢复术语容易混淆。直接描述足以解决问题，无需另造短标签。
    first_use_definition: >-
      “两项次要表征诊断是：遮蔽原本已测的生理值后检验其重建误差与覆盖，以及检验未来生理轨迹预测的评分与校准。”
    competing_forms_and_locators:
      - "“两项次要表示诊断”：第 47、82、205 行"
      - "“两项次要诊断”：第 128、331、357、372、407 行"
      - "“伪遮蔽重建”：第 124、330 行"
      - "“部分状态重建”：第 294 行"
      - "“未来轨迹诊断”：第 124、294、330 行"
      - "representation 的“生成表示/观察性表示”：第 62、76 行"
  - finding_id: LANG-R108-003
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: primary-task-performance-criterion
    normalized_locator: freeze-and-external-criteria
    failure_mode: underdefined-proper-score-term
    fingerprint: "meso|primary-task-performance-criterion|freeze-and-external-criteria|underdefined-proper-score-term"
    category: 统计术语跨学科可及性
    dossier_locator:
      - "24-month milestones（第 102 行）"
      - "WP3、primary-task protocol 和 evidence chain（第 124、203、330–331 行）"
      - "Required analyses、falsification criteria 和 working assumptions（第 357、381、447 行）"
    current_problem: >-
      “适当评分”在中文中可被理解为未具体说明的“合适评分”，没有显式指出统计学上的 proper scoring rule；该词又控制分析冻结、外部检验和阶段 II 判定，首次出现时尚未与 Brier 分数建立关系。
    target_state: >-
      使用能明确指向 proper scoring rule 的中英对照术语，并在首次出现时给出本计划实际采用的 Brier 或多类别 Brier 分数实例。
    required_change_or_replacement: >-
      将首次出现的“适当评分”改为“恰当评分规则（proper scoring rules；本计划主要采用 Brier 分数或多类别 Brier 分数）”；后文统一使用“恰当评分规则”或直接写出相应 Brier 指标，不再单独使用“适当评分”。
    content_to_preserve: >-
      保留全部 Brier 非劣界、校准斜率、校准截距或绝对风险误差、置信界和最终测试授权规则；本 finding 不改变任何评价指标或阈值。
    acceptance_test: >-
      第 102 行之前或当行出现完整定义；全文检索“适当评分”无结果，所有冻结和外部判定位置均明确连接到恰当评分规则及 dossier 已指定的 Brier 指标。
    term_or_phrase: 适当评分
    recommended_form_or_plain_description: >-
      恰当评分规则（proper scoring rules；如 Brier 分数和多类别 Brier 分数）。
    evidence_basis: >-
      dossier 在第 112、114、203、205、330、331 和 447 行实际指定 Brier 类指标，说明所指并非泛称的“合适评分”；补出“规则”和英文术语即可消除跨学科歧义。
    first_use_definition: >-
      “恰当评分规则是对概率预测分布进行评价、并在真实分布下使期望得分最优的一类评分规则；本计划主要使用 Brier 分数或多类别 Brier 分数。”
    competing_forms_and_locators:
      - "“适当评分”：第 102、124、357、381 行"
      - "具体的“Brier/多类别 Brier 分数”：第 112、114、203、205、330、331、447 行"
  - finding_id: LANG-R108-004
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: misspecification-diagnostic
    normalized_locator: objective-recovery-and-stop-rules
    failure_mode: collapsed-false-confidence-roles
    fingerprint: "meso|misspecification-diagnostic|objective-recovery-and-stop-rules|collapsed-false-confidence-roles"
    category: 检验对象命名
    dossier_locator:
      - "Objective 3（第 82 行）"
      - "Recovery admission and absolute criteria（第 101、240–241 行）"
      - "Key techniques、evidence chain 和 required analyses（第 304、323、355 行）"
      - "Falsification criteria（第 379 行）"
    current_problem: >-
      “假置信检查”和“错设与零边假置信检查”没有写明是谁对什么给出错误的高置信结论，并把零边机制中的虚假结构与模型错设下的过度置信两个不同结果压进同一短语；第 240–241 行实际上给出了两个不同的判定对象。
    target_state: >-
      用直接表述区分“零边机制下产生虚假结构”和“模型错设下仍给出错误的高置信结构结论”，首次出现时同时定义，后文不得用一个无对象的“假置信”统称二者。
    required_change_or_replacement: >-
      将第 82 行的“执行绝对恢复与假置信检查”改为“检验已知结构能否按预设绝对标准恢复，并分别检查零边机制下是否产生虚假结构、模型错设时是否仍给出错误的高置信结构结论”。后文使用“零边虚假结构检查”和“错设下错误高置信结论检查”，或继续使用同等清楚的完整描述。
    content_to_preserve: >-
      保留零边虚假边比例、错设识别比例、错误结构高置信比例、复杂候选淘汰和不得事后调整阈值的所有规则，并保持两个判定对象彼此独立。
    acceptance_test: >-
      第 82 行即可辨认两个检查对象；全文不再出现无主客体的“假置信检查”，第 240 和 241 行的两项判定分别只映射到一个稳定名称。
    term_or_phrase: 假置信检查；零边假结构；错设下的假置信识别
    recommended_form_or_plain_description: >-
      零边机制下的虚假结构检查；模型错设下错误高置信结构结论的检查。
    evidence_basis: >-
      第 240 行检验零边生成机制中的虚假边，第 241 行检验错设时是否仍对错误结构给出高置信；第 355 行的压缩短语使两个科学角色的修饰关系不再明确。建议直接描述 dossier 已写出的判定对象。
    first_use_definition: >-
      “零边虚假结构检查判断无真实边时模型是否仍报告边；错设下错误高置信结论检查判断生成机制不符合模型假设时，模型是否仍对错误结构给出高置信结论。”
    competing_forms_and_locators:
      - "“假置信检查”：第 82 行"
      - "“零边假结构”：第 101、240、379 行"
      - "“错设下的假置信识别”：第 241 行"
      - "“错设与零边假置信检查”：第 355 行"
      - "“错设识别”：第 304、323、371、379 行"
  - finding_id: LANG-R108-005
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: contribution-positioning
    normalized_locator: positioning-and-contribution-statements
    failure_mode: shifting-governance-metaphor
    fingerprint: "meso|contribution-positioning|positioning-and-contribution-statements|shifting-governance-metaphor"
    category: 贡献表述的术语自然度
    dossier_locator:
      - "Positioning and contribution frame（第 40 行）"
      - "Contribution and evidence ladder（第 402 行）"
      - "Title and positioning claim-support table（第 431 行）"
    current_problem: >-
      “分析治理”“方法治理价值”和“可审计证据治理”在三个贡献位置交替出现，既不是稳定定义的科学产物，也没有说明治理所指的具体分析操作或记录；读者只能从全文反推其意为预先规定规则、停止决定和审计记录。
    target_state: >-
      直接陈述预先规定分析步骤、判定与停止规则并保留可审计记录的贡献，不再以不同“治理”隐喻代称。
    required_change_or_replacement: >-
      第 40 行用“可证伪、可审计的分析规则与判定记录”替换“可证伪的分析治理”；第 402 和 431 行分别改为“预先规定分析与停止规则并保留可审计决定记录的价值”和“可审计的分析规则、判定与负向结果记录”。
    content_to_preserve: >-
      保留贡献的条件性、整合与验证定位、基准或研究资源价值、可证伪性、负向结果以及不主张新算法的边界。
    acceptance_test: >-
      第 40、402 和 431 行均直接说明具体操作或产物；全文不再用“分析治理/方法治理/证据治理”作为未定义的贡献标签。
    term_or_phrase: 分析治理；方法治理价值；证据治理
    recommended_form_or_plain_description: >-
      预先规定分析步骤、判定标准与停止规则，并保留可审计的决定和负向结果记录。
    evidence_basis: >-
      三处短语词根相同但修饰对象不同，全文的直接内容是分析冻结、预设判定、停止规则和按对象记录结果；以这些科学操作直接表述即可，无需保留治理隐喻。
    first_use_definition: >-
      “此处指预先规定分析步骤、判定标准和停止规则，并保留可审计的决定及负向结果记录。”
    competing_forms_and_locators:
      - "“可证伪的分析治理”：第 40 行"
      - "“方法治理价值”：第 402 行"
      - "“可审计证据治理”：第 431 行"
  - finding_id: LANG-R108-006
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: randomized-trial-data-sources
    normalized_locator: first-trial-name-use-line-139
    failure_mode: undefined-trial-abbreviations
    fingerprint: "meso|randomized-trial-data-sources|first-trial-name-use-line-139|undefined-trial-abbreviations"
    category: 缩写首用定义
    dossier_locator:
      - "Current resource and result status（第 139 行首次出现）"
      - "Local randomized-trial evidence status（第 185、187 行）"
      - "Conditional trial-observation mapping and independent analysis（第 267–290 行）"
    current_problem: >-
      EXIT-SEP 和 XBJ-SCAP 在第 139 行首次出现时只有试验缩写；两项试验的人群和干预直到第 185、187 行及参考文献才可拼合。对不熟悉这些试验的系统辨识、统计或医学人工智能读者，首次出现不能建立缩写与科学对象的对应关系。
    target_state: >-
      首次出现时保留官方试验缩写，并各用一条直接的中文描述说明人群、干预和随机对照试验身份；后文可只用缩写。
    required_change_or_replacement: >-
      将第 139 行首次出现改为“EXIT-SEP（脓毒症患者血必净注射液与 28 日死亡结局的随机对照试验）和 XBJ-SCAP（重症社区获得性肺炎患者血必净注射液与安慰剂的随机对照试验）”。若采用正式中文试验名，应以参考文献 [17] 和 [18] 的原始题名为准，仍须保留上述人群与试验类型信息。
    content_to_preserve: >-
      保留两个官方缩写、两项试验分开分析、样本数、访视时点、授权和语义尚待核验，以及它们仅承担条件性次要分析的证据角色。
    acceptance_test: >-
      第 139 行单独阅读即可分别回答两项缩写对应的人群、干预和研究类型；后续所有缩写拼写一致，且没有暗示两项试验可合并。
    term_or_phrase: EXIT-SEP；XBJ-SCAP
    recommended_form_or_plain_description: >-
      官方缩写加各自的人群、干预和随机对照试验身份说明。
    evidence_basis: >-
      dossier 第 185、187 行及参考文献 [17]、[18] 已提供足以作直接首用说明的信息，不需外部引入新名称。
    first_use_definition: >-
      “EXIT-SEP 是脓毒症患者血必净注射液随机对照试验；XBJ-SCAP 是重症社区获得性肺炎患者血必净注射液与安慰剂随机对照试验。”
    competing_forms_and_locators: []
  - finding_id: LANG-R108-007
    severity: minor
    finding_kind: terminology
    finding_level: micro
    finding_scope: occurrence
    scientific_role: observation-mapping-fidelity-criterion
    normalized_locator: fidelity-criterion-line-277
    failure_mode: undefined-cross-disciplinary-metric
    fingerprint: "micro|observation-mapping-fidelity-criterion|fidelity-criterion-line-277|undefined-cross-disciplinary-metric"
    category: 跨学科技术术语首用
    dossier_locator: "Conditional trial-observation mapping and independent analysis，第 277 行"
    current_problem: >-
      “第一奇异轴解释 L_C Frobenius 能量至少 50%”只给出系统辨识或线性代数短语，没有说明这里的能量占比如何由奇异值计算；临床与转化研究读者无法从该句判断 50% 的分母和比较对象。
    target_state: >-
      保留 Frobenius 术语和 50% 阈值，同时在同一句用普通数学语言说明它是第一奇异值平方占全部奇异值平方和的比例。
    required_change_or_replacement: >-
      改为“第一奇异轴所解释的 \(L_C\) Frobenius 能量占比（即第一奇异值的平方占全部奇异值平方和的比例）至少为 50%”。
    content_to_preserve: >-
      保留矩阵 \(L_C\)、奇异值分解、第一奇异轴和 50% 阈值，不改变映射忠实度的任何计算或后果。
    acceptance_test: >-
      不借助其他学科术语即可从第 277 行写出该比例的分子和分母，且数值阈值仍为 50%。
    term_or_phrase: Frobenius 能量
    recommended_form_or_plain_description: >-
      Frobenius 能量占比，即第一奇异值平方占全部奇异值平方和的比例。
    evidence_basis: >-
      该词只在第 277 行出现，公式上下文给出奇异值分解但没有给出比例的普通语言定义；对嵌入式读者画像中的非数学学科，这是一个跨学科首用缺口。
    first_use_definition: >-
      “此处的第一奇异轴 Frobenius 能量占比，是第一奇异值平方除以全部奇异值平方和。”
    competing_forms_and_locators: []
  - finding_id: LANG-R108-008
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: complete-idea-summary
    normalized_locator: one-sentence-summary-line-38
    failure_mode: stacked-modifiers-and-clauses
    fingerprint: "micro|complete-idea-summary|one-sentence-summary-line-38|stacked-modifiers-and-clauses"
    category: 中文学术清晰度
    dossier_locator: "Title, summary, audience, and positioning，One-sentence complete-Idea summary（第 38 行）"
    current_problem: >-
      一个固定单句同时承载两类证据来源、数据库审计限定、五层表征修饰、两种验证操作、条件性试验延伸和非因果边界；“以文献和专家先验及两个……数据库”与“知识约束、不确定性感知候选动态系统表征”均为重叠修饰，读者需回读才能确定依存关系。
    target_state: >-
      仍保持一个句子和一个字段，但以并列谓语和三个清楚分句依次呈现主体研究、条件性延伸与解释边界，所有修饰词紧邻其语义中心。
    required_change_or_replacement: >-
      用以下单句替换：“本研究计划在 24 个月内，基于文献与专家先验，并使用两个须先完成访问和可观测性审计的公共重症监护数据库，构建覆盖脓毒症发病前在险时段、首次发病、发病后演化和结局且具有知识约束并显式处理不确定性的候选动态系统表征，再以预设机制下的模拟重建和跨数据库检验形成可审计证据；仅当主体研究达到标准后，才对各项试验分别开展次要分析，考察随机分配与实际访视临床状态的关系；所有预测结果和观察性表征均仅作非因果解释。”
    content_to_preserve: >-
      保留 24 个月、文献与专家先验、两个公共重症监护数据库及其审计、全病程范围、知识约束与不确定性、模拟和跨数据库检验、试验延伸的条件性与分试验处理，以及非因果解释边界。
    acceptance_test: >-
      该字段仍严格为一个句子；首次通读即可按“主体研究—条件性延伸—解释边界”复述内容，且上述九类信息全部保留。
  - finding_id: LANG-R108-009
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: structured-abstract-gap
    normalized_locator: background-gap-line-44
    failure_mode: nonparallel-evidence-coordination
    fingerprint: "micro|structured-abstract-gap|background-gap-line-44|nonparallel-evidence-coordination"
    category: 语法与并列关系
    dossier_locator: "Structured abstract，Background and gap（第 44 行）"
    current_problem: >-
      “取得模拟重建、主要临床任务与跨数据库证据”把操作、任务和证据作为“取得”的并列宾语，三者语法层级不一致；“发病前、首次发病、发病后和结局”也省略了不同阶段所需的中心词。
    target_state: >-
      将病程阶段写成平行结构，并使“证据”统领模拟重建、主要任务表现和跨数据库检验三个方面。
    required_change_or_replacement: >-
      将句末改为“却仍不能回答：同一候选表征能否在不混淆预测与因果的前提下，贯通脓毒症发病前在险时段、首次发病、发病后演化和结局，并同时获得模拟重建、主要临床任务表现和跨数据库检验三方面的证据。[26-38]”
    content_to_preserve: >-
      保留预测与因果区分、四个病程部分、三类证据和引文 [26-38]，不改变 gap 的科学范围。
    acceptance_test: >-
      “获得”的直接宾语只有“证据”，三个证据方面语法平行，四个病程部分各有可识别的阶段中心词。
  - finding_id: LANG-R108-010
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: research-gap
    normalized_locator: gap-paragraph-line-62
    failure_mode: mixed-level-evidence-list
    fingerprint: "micro|research-gap|gap-paragraph-line-62|mixed-level-evidence-list"
    category: 语法与局部清晰度
    dossier_locator: "Background, current state, gap, significance, and rationale，Gap（第 62 行）"
    current_problem: >-
      “取得相互一致的数据支持、模拟重建、主要任务表现、状态对齐与结构稳定性证据”把“证据”只附着到最后一项，使前四项看似是与证据并列的结果；同句“生成表示”又与全文 representation 的“表征”用法不一致。
    target_state: >-
      由“相互一致的证据”统领五个方面，并在术语意义上统一使用“表征”。
    required_change_or_replacement: >-
      改为“现有证据尚不能回答：一个以脓毒症为中心、同时覆盖可比未发病在险时段、首次发病、发病后互斥状态和结局的候选动态系统表征，能否在两个异质公共数据库中获得关于数据支持、模拟重建、主要任务表现、状态对齐和结构稳定性的相互一致证据，同时避免把观察政策下的预测或生成表征误作因果系统。”
    content_to_preserve: >-
      保留研究对象、全病程范围、两个异质数据库、五个证据方面和非因果边界。
    acceptance_test: >-
      五个方面都明确受“证据”统领；该句不再出现术语意义上的“生成表示”，且不改变任何科学主张。
  - finding_id: LANG-R108-011
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: stage-three-evidence-boundary
    normalized_locator: repeated-stage-three-boundaries
    failure_mode: near-verbatim-caveat-repetition
    fingerprint: "meso|stage-three-evidence-boundary|repeated-stage-three-boundaries|near-verbatim-caveat-repetition"
    category: 简洁性与重复
    dossier_locator:
      - "Objective 4、timeline 和 work packages（第 83、104、116、126 行）"
      - "Trial mapping 与 evidence chains（第 269、346 行）"
      - "Planned outputs、contribution 和 closest-work comparison（第 373、402、420 行）"
      - "Limitations（第 458、463 行）"
    current_problem: >-
      “阶段 III 仅在主体研究达到标准后开展，且不计入或补足阶段 II 成功”以近似完整句在多个相邻功能位置重复；限定本身重要，但重复措辞增加篇幅并削弱各处局部重点。
    target_state: >-
      在所有由叙事结构要求保留的现有位置，使用一条稳定而简洁的边界句；语言修订不得自行决定删除哪个科学位置的边界。
    required_change_or_replacement: >-
      将各保留位置的核心措辞统一压缩为“阶段 III 仅在阶段 II 达到预设标准后开展，其结果不计入也不能补足阶段 II 成功。”各处只补充本节特有的信息，例如分试验分析或时间边界；在没有叙事修订指令时，不删除任何当前承载完整限制的位置。
    content_to_preserve: >-
      保留阶段 III 的前置条件、从属地位、24 个月边界、分试验处理，以及不得计入或补足阶段 II 的完整限制。
    acceptance_test: >-
      每个列明位置至多出现一次该边界的完整语义，核心用词一致；所有当前科学限制仍可在原位置找到，是否跨节删减由叙事修订另行决定。
  - finding_id: LANG-R108-012
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: limited-adaptation-evidence-boundary
    normalized_locator: repeated-no-update-boundaries
    failure_mode: near-verbatim-caveat-repetition
    fingerprint: "meso|limited-adaptation-evidence-boundary|repeated-no-update-boundaries|near-verbatim-caveat-repetition"
    category: 简洁性与重复
    dossier_locator:
      - "Conjunctive minimum success definition（第 116 行）"
      - "Hospital-primary cross-database validation（第 265 行）"
      - "Falsification criteria 和 interpretation matrix（第 381–392 行）"
      - "Limitations（第 457 行）"
    current_problem: >-
      “有限适配不能补偿或改变不更新外部检验未达到标准的结论”在五处以近似完整形式反复出现；同一边界在局部重复时掩盖了每节原本要说明的操作、结果或解释角色。
    target_state: >-
      在所有由叙事结构要求保留的位置使用一条稳定、短而完整的边界句，并把该位置特有的适配操作或解释紧邻其后。
    required_change_or_replacement: >-
      统一核心句为“仅校准适配和仅观测层适配只描述适配后表现，不能改变不更新外部检验未达到标准的结论。”各列明位置仅增加本节独有的信息；在没有叙事修订指令时，不删除现有科学边界的位置。
    content_to_preserve: >-
      保留不更新外部检验的主要证据地位、两种有限适配的名称与角色、全模型重拟合属于开发，以及适配结果不能挽救主要外部检验的限制。
    acceptance_test: >-
      各列明位置至多出现一次完整限制，核心术语和逻辑关系一致；不更新、两种有限适配与全模型重拟合的证据角色仍彼此分明。
  - finding_id: LANG-R108-013
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: publication-deliverable
    normalized_locator: objectives-delivery-line-85
    failure_mode: vague-prestige-language
    fingerprint: "micro|publication-deliverable|objectives-delivery-line-85|vague-prestige-language"
    category: 学术语体
    dossier_locator: "Research question, objectives, and core hypothesis（第 85 行）"
    current_problem: >-
      “一篇或多篇高水平论文”以未定义的声望形容词描述计划性交付，既不能被语言层面核验，也与全文审慎、可审计的语体不一致。
    target_state: >-
      保留论文交付目标，但用可识别的出版物类型而非声望判断表述。
    required_change_or_replacement: >-
      改为“交付方向包括一篇或多篇同行评议论文和可审计的科学证据，而不是仅产出预测工具。”若论文类型已确定，可用具体类型替换“同行评议论文”，但不得预先声称质量、声望、影响或接收。
    content_to_preserve: >-
      保留一篇或多篇论文、可审计科学证据及不以预测工具为唯一产出的交付方向。
    acceptance_test: >-
      句中不再出现“高水平”等未经定义的声望形容词，且论文与可审计证据两个目标均保留为前瞻性目标。
  - finding_id: LANG-R108-014
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: label-feature-separation
    normalized_locator: variable-role-table-line-180
    failure_mode: missing-feature-set-complement
    fingerprint: "micro|label-feature-separation|variable-role-table-line-180|missing-feature-set-complement"
    category: 语法与对象明确性
    dossier_locator: "Variable roles 表，“仅用于标签”行（第 180 行）"
    current_problem: >-
      “不进入相同或更早标志时点”缺少“进入”的对象，字面上像是变量不能进入一个时间点，而非不能进入该时间点的特征集或模型输入。
    target_state: >-
      补出特征集或模型输入这一语法宾语，保持时间先后限制不变。
    required_change_or_replacement: >-
      将该分句改为“这些标签变量不进入同一或更早标志时点的特征集；抗菌药的双重用途遵循信息可用时钟，并与行动变量分离。”
    content_to_preserve: >-
      保留仅用于标签的变量范围、同一或更早标志时点禁入、抗菌药双重用途、信息可用时钟和行动变量分离。
    acceptance_test: >-
      “进入”的直接宾语明确为特征集或等价的模型输入，且禁止时段仍为同一或更早标志时点。
  - finding_id: LANG-R108-015
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: missing-data-baseline
    normalized_locator: missingness-method-line-228
    failure_mode: ambiguous-modifier-attachment
    fingerprint: "micro|missing-data-baseline|missingness-method-line-228|ambiguous-modifier-attachment"
    category: 修饰关系与方法表述
    dossier_locator: "Observational target, anchoring, and evidence-qualified interpretation（第 228 行首句）"
    current_problem: >-
      “使用显式测量过程的随机缺失或选择模型基线”无法判断“显式测量过程”只修饰随机缺失基线、同时修饰两类基线，还是“随机缺失或选择模型”共同构成一个基线；两种分析角色没有形成平行结构。
    target_state: >-
      将随机缺失基线和选择模型基线写成两个并列、各有明确谓语的选项，并说明显式建模测量过程适用于哪一项。
    required_change_or_replacement: >-
      按当前句中已写出的两类基线，改为“主要拟合采用两类基线：一类在显式建模测量过程后假定随机缺失，另一类采用选择模型。”若实际设计中显式测量过程也属于第二类，须在第二分句重复写明，而不能依赖悬空修饰语。
    content_to_preserve: >-
      保留随机缺失与选择模型两个选项、显式测量过程、后续模式混合偏移、选择模型临界点及全部数值范围。
    acceptance_test: >-
      单读首句即可列出基线的数量、每类基线的缺失假设及“显式测量过程”的修饰范围；不改变后续敏感性分析。
  - finding_id: LANG-R108-016
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: singular-vector-tie-rule
    normalized_locator: observation-equation-line-275
    failure_mode: omitted-tie-break-object
    fingerprint: "micro|singular-vector-tie-rule|observation-equation-line-275|omitted-tie-break-object"
    category: 局部技术清晰度
    dossier_locator: "Conditional trial-observation mapping and independent analysis（第 275 行）"
    current_problem: >-
      “奇异值并列时按预先固定的锚点字典序决定”省略了“决定”的对象；读者无法判断字典序决定的是并列轴的次序、第一奇异轴、载荷方向还是符号。
    target_state: >-
      在不改变规则的前提下，明确写出字典序实际决定的数学对象和作用。
    required_change_or_replacement: >-
      将该分句写成“奇异值并列时，按预先固定的锚点字典序确定【实际被排序或定号的对象】”，并用 dossier 实际规则中的名词替换括号内容；若决定第一奇异轴，可直接写“确定第一奇异轴”，若决定并列轴次序或符号，则须分别直述。
    content_to_preserve: >-
      保留奇异值并列这一触发条件、预先固定的锚点字典序、后续符号与 SOFA 的方向约束，以及映射不使用治疗分组或试验结局的限制。
    acceptance_test: >-
      修改后句中“确定/决定”具有一个明确的数学宾语；两名具备不同学科背景的目标读者能给出同一答案，且没有新增或改变并列处理规则。
  - finding_id: LANG-R108-017
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: trial-evidence-reference
    normalized_locator: evidence-ladder-line-409
    failure_mode: unresolvable-section-reference
    fingerprint: "micro|trial-evidence-reference|evidence-ladder-line-409|unresolvable-section-reference"
    category: 文内指称
    dossier_locator: "Contribution and evidence ladder 表，“从属的试验访视结局证据”行（第 409 行）"
    current_problem: >-
      “第 7 节规定的数据……”引用了正文中未显示的节号；dossier 使用未编号的固定标题，读者无法可靠定位“第 7 节”。
    target_state: >-
      用固定节标题而非不可见编号指向相应方法内容。
    required_change_or_replacement: >-
      将“第 7 节规定的数据、语义、结局构造、缺失、中心和多重性条件”改为“‘Conditional trial-observation mapping and independent analysis’一节规定的数据、语义、结局构造、缺失、中心和多重性条件”。
    content_to_preserve: >-
      保留所指方法节及数据、语义、结局构造、缺失、中心和多重性六类条件，不改动固定标题。
    acceptance_test: >-
      点击或文本检索所给标题可唯一定位对应 H3；全文不存在指向未显示编号的“第 7 节”。
  - finding_id: LANG-R108-018
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: conditional-method-statements
    normalized_locator: dense-method-and-limit-units
    failure_mode: excessive-condition-stacking
    fingerprint: "meso|conditional-method-statements|dense-method-and-limit-units|excessive-condition-stacking"
    category: 可读性与句法负荷
    dossier_locator:
      - "Protocol locks 表（第 196–205 行）及信息泄漏段（第 207 行）"
      - "Observational target 和 recovery criteria（第 228、244 行）"
      - "Hospital-primary validation 与 trial mapping（第 256、277、287–288 行）"
      - "Required analyses、contribution 和 limitations（第 361、402、463 行）"
    current_problem: >-
      多个单元把人群条件、时间窗、测量规则、数值阈值、例外和失败后果压在一个超长句中；虽然各条件可逐项找出，但主语和后果需跨越多个分号回溯，跨学科读者难以首次阅读即确认哪个后果由哪个条件触发。
    target_state: >-
      在保留现有表格、列表和字段格式的前提下，每个完整短句只承担一个主要操作或一组同类标准，并让每个例外或停止后果紧邻其触发条件。
    required_change_or_replacement: >-
      在每个列明的原表格单元格、列表项或段落内，将长句拆成 2–4 个完整短句或清楚编号的同类条件组：先写对象与主要规则，再写阈值，最后写未达到标准的后果；不得把内容移出原表格/列表，也不得合并不同科学条件。第 277 行尤其应把外部忠实度标准、试验资料检查和失败后果分为三个句群；第 463 行应把禁止主张、试验解释边界和不一致结果边界分开。
    content_to_preserve: >-
      保留所有人群、时序、变量、模型、数值阈值、例外、敏感性分析、停止规则、表格与列表结构，以及每项条件现有的科学作用域。
    acceptance_test: >-
      每个列明单元均可在不回读前一分号组的情况下把触发条件配对到其后果；所有数值、否定词和条件词与原文逐项一致，表格行数、列表项数和字段基数不变。
unresolved_issues:
  - LANG-R108-001
  - LANG-R108-002
  - LANG-R108-003
  - LANG-R108-004
  - LANG-R108-005
  - LANG-R108-006
  - LANG-R108-007
  - LANG-R108-008
  - LANG-R108-009
  - LANG-R108-010
  - LANG-R108-011
  - LANG-R108-012
  - LANG-R108-013
  - LANG-R108-014
  - LANG-R108-015
  - LANG-R108-016
  - LANG-R108-017
  - LANG-R108-018
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r108  
**Target Language**: Chinese（固定英文脚手架、公式、正式名称与参考文献标识符除外）  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学人工智能与转化研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文的语法、语体与前瞻性时态总体稳定，但四个核心概念簇尚未达到给定跨学科读者的首用可及性和一致命名要求，因而术语 hard gate 未通过。修订可保持定向，不需要全篇专业重写。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
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
| Grammar error density | pass | 清楚语法错误保守估计低于 1 个/500 中文词语当量；问题为少量可定位的并列或宾语缺失，不构成系统密度失误 |
| Academic register | pass | 无两个以上章节的系统口语化；仅第 85 行有一处声望性形容词 |
| Terminology coherence | fail | 4 个核心概念簇存在首用不可及、角色折叠或不一致命名：共同生理锚点、两项次要表征诊断、恰当评分规则、零边与错设检查 |
| Tense systematic violation | pass | 本文是前瞻性 Idea dossier，计划、条件与尚未生成状态的时态一致；没有把计划工作系统写成已完成结果 |

---

## Strengths

1. “计划”“尚未核验”“尚未生成”等证据状态用语在摘要、资源表、方法和限制中保持一致，没有把预期结果写成既成结果。
2. 预测、观察性表征与因果解释之间的语言边界明确，并在研究问题、核心假设、解释矩阵和限制中保持相同方向。
3. SOFA、mITT、潜在状态投影和一维可观测代理等多数缩写或技术对象在首次实质使用处有全称、公式或直接说明。
4. 不更新外部检验、仅校准适配、仅观测层适配和全模型重拟合在定义后保持为四个可区分的操作名称。
5. 正文整体采用正式、克制的科学语体，没有系统口语、感叹、直接称呼读者或不适合方法文本的修辞问句。

---

## Specific Issues

以下正文只给出证据、读者影响与优先级；完整替换、保留内容和验收条件见 frontmatter 中对应 finding。

### Chinese Academic Clarity (if applicable)

- LANG-R108-008、009、010：摘要与 gap 的修饰堆叠或并列层级要求回读；均可在保持字段和主张不变的前提下作局部改写。
- LANG-R108-011、012：两个重要证据边界以近似完整句多次重复。语言修订只压缩和统一措辞，不决定哪些跨节位置保留限制。
- LANG-R108-018：若干方法表格单元和限制段把条件、阈值与后果堆在一个长句中；应在原结构内分句。

### Grammar & Syntax

- LANG-R108-009（第 44 行）和 LANG-R108-010（第 62 行）：证据列表的中心词附着不平行。
- LANG-R108-014（第 180 行）：“进入”缺少“特征集/模型输入”这一宾语。
- LANG-R108-015（第 228 行）：缺失数据基线的修饰范围不明确。

### Academic Register & Tone

- LANG-R108-013（第 85 行）：“高水平论文”是不可核验的声望性修饰；应保留论文目标而改用出版物类型。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LANG-R108-001 | 锚点及其变量、观测值、预测值形式 | 第 45、100–307 行所列位置 | 无法稳定判断同一短语所指的科学角色 | yes |
| LANG-R108-002 | 两项次要表示/表征诊断 | 第 47、82、124、205、292–294 行等 | 首用未命名，且“部分状态重建”可能被读成状态恢复 | yes |
| LANG-R108-003 | 适当评分 | 第 102、124、357、381 行 | 可能被读成泛称的“合适评分”，而非 proper scoring rule | yes |
| LANG-R108-004 | 假置信、零边假结构、错设识别 | 第 82、240–241、355 行等 | 两个不同检查对象被压成一个无主客体标签 | yes |
| LANG-R108-005 | 分析/方法/证据治理 | 第 40、402、431 行 | 贡献产物需由读者反推，且三处命名漂移 | yes |
| LANG-R108-006 | EXIT-SEP；XBJ-SCAP | 第 139 行首次出现 | 非试验本领域读者不能在首次出现时识别人群与研究类型 | yes |
| LANG-R108-007 | Frobenius 能量 | 第 277 行 | 非数学读者不能确定 50% 的分子与分母 | yes |

### Tense & Voice Conventions

未发现系统性时态或语态问题。前瞻性计划使用现在时、计划性表达和条件句符合 Idea dossier 体裁；已核验、尚待核验和待生成状态区分清楚。

### Conciseness & Redundancy

- LANG-R108-011：阶段 III 的前置与不补足边界存在近似逐句重复。
- LANG-R108-012：有限适配不能改变不更新外部检验结论的边界存在近似逐句重复。

### Readability & Flow

- LANG-R108-008：完整想法摘要可在固定单句内重排为主体研究、条件性延伸和解释边界三个分句。
- LANG-R108-016：奇异值并列规则缺少所决定对象。
- LANG-R108-017：未编号正文中的“第 7 节”无法定位。
- LANG-R108-018：列明的方法与限制单元需在原表格或列表内拆分条件组。

---

## Language Revision Priorities

1. **Terminology**: 4 个 major、3 个 minor findings — 先完成核心角色的首用定义和全文一致命名，再处理两个试验缩写及单个跨学科指标。
2. **Readability and grammar**: 7 个 minor findings — 修正摘要、证据并列、缺失宾语、修饰附着、文内指称和高负荷条件句。
3. **Concision and register**: 4 个 minor findings — 在不改变科学边界位置的前提下统一两类重复限制，并删除一处声望性形容词。

---

## Re-Assessment Status (if applicable)

本次为完整 Idea dossier 的全新独立评估，不接收匿名问题清单，也不比较旧版本、旧分数或既有决定。

| Check | Current assessment |
|--------|--------------------|
| Listed issues no longer present | 不适用 |
| Listed issues still present | 不适用 |
| New current-text issues | LANG-R108-001 至 LANG-R108-018 |

---

## Assessment Notes

- 读者基线按嵌入式 handoff 执行：可假定每位读者具备自身学科基础，但不假定其理解项目标签或其他学科未解释的隐含术语。
- 15 个 H2、5 个固定推理 H3、结构式摘要和证据链字段标签、Claim-Support 表头及机器 frontmatter 仅作为固定脚手架，不评分、不翻译、不建议改名；正文与自由标签仍在范围内。
- 有界 scanner 的 reader-entry、compact-label 和 mixed-language/internal-token prompts 均完成语义判断。标准且已定义的术语、数学符号、数据库版本、文献标识符、引用路径与固定脚手架没有因扫描命中而被报告。
- 未评价科学有效性、论证质量、新颖性、影响、可行性或期刊适配，也未编辑 dossier。
