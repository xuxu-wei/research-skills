---
review_id: language-assessment-r059
reviewer_skill: academic-language-assessor
reviewer_instance_id: academic-language-assessor-r059
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r059
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - reader-handoff-forward-001
input_versions:
  - v003
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
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
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LNG-R059-001
    severity: major
    finding_kind: language
    category: title_modifier_attachment
    dossier_locator:
      - "主标题与 Title 字段（第27、31行）"
      - "Positioning and contribution frame（第34行）"
      - "Primary research question 与 Objective 4（第60、67行）"
      - "Evidence-chain 标题、贡献段和 claim-support 表（第314、376、397、405行）"
    current_problem: >-
      “条件性稀疏 RCT 次要再分析”按通常句法使“稀疏”修饰 RCT，并使“条件性”可同时附着于 RCT 或次要分析；正文第54、261行表明真正稀疏的是重复随访测量，条件限定的是是否启动次要分析。竞争形式还包括“严格条件化的稀疏 RCT 次要再分析层”“稀疏 RCT 层”“实际稀疏 RCT 访视”和“条件性稀疏 RCT 观测投影或独立临床状态再分析”。
    target_state: >-
      标题和首次概述明确让“稀疏”只修饰随访测量，让预设条件只限制次要分析的启动，并用中文全称说明 RCT。
    required_change_or_replacement: >-
      将标题改为“脓毒症全病程候选动态系统表征：计划开展跨数据库检验，并在满足预设条件时对随机对照试验的稀疏随访测量进行次要分析”；第34、50、60、67、314、376、397、405行同步改用“在满足预设条件时，对随机对照试验的稀疏随访测量进行次要分析”或语法等价的直接表述。
    content_to_preserve: >-
      保留“候选”和“计划”的证据状态、跨数据库检验、随机试验次要分析的条件性、D7/D8 实际访视、重复测量稀疏以及两个失败分支。
    acceptance_test: >-
      全篇检索不再出现“稀疏 RCT”“实际稀疏 RCT 访视”或“条件性稀疏 RCT”；推荐标题复解析时，“全病程”和“候选”修饰“动态系统表征”，“在满足预设条件时”修饰“进行次要分析”，“稀疏”只修饰“随访测量”，“随机对照试验的”也只修饰“随访测量”。
  - finding_id: LNG-R059-002
    severity: major
    finding_kind: terminology
    category: core_object_terminology
    dossier_locator:
      - "标题、摘要和研究问题（第27、31、32、34、39、42、50、54、60、65、67行）"
      - "阶段 II 成功定义与 evidence chains（第92、252、254、287、311、319行）"
      - "解释矩阵和定位表（第368–370、393、403、406行）"
    current_problem: >-
      中央研究对象在读者正文中交替称为“候选动态系统表征”（第27、31、32、60行）、“候选表征”（第34行）、“候选全病程表示”（第39行）、“候选架构”（第50行）、“候选状态表示”（第65行）、“计划跨数据库候选系统表征”（第92、311行）、“候选表示”（第287、393行）、“最小全病程候选表示”（第370行）和“阶段 II 表征/模型、整个系统模型/整个模型”（第32、42、54、67、252、254、319、368、369、406行）。这些形式没有说明哪些是同一研究对象，哪些专指可选的复杂模型实现。
    target_state: >-
      为中央研究对象保留一个稳定的描述性名称，并明确区分研究对象、可选复杂模型实现和阶段 II 冻结产物。
    required_change_or_replacement: >-
      在摘要首次出现时写“脓毒症全病程候选动态系统表征（下称‘候选表征’）”；此后中央对象一律称“候选表征”。只有在指切换或非线性实现时使用“复杂候选模型”，在指阶段 II 的冻结输出时使用“阶段 II 冻结的候选表征”，在边界声明需要同时涵盖二者时使用“候选表征及其模型实现”。
    content_to_preserve: >-
      保留全病程范围、知识约束和不确定性感知属性，保留至多一个复杂模型的独立角色，并保留阶段 II 与阶段 III 的边界。
    term_or_phrase: "候选动态系统表征及其竞争称谓"
    recommended_form_or_plain_description: "候选表征；复杂实现另称复杂候选模型；冻结产物另称阶段 II 冻结的候选表征"
    evidence_basis: "原稿对同一对象使用多个未定义称谓，且没有支持任一压缩标签为领域标准术语的证据；采用按科学角色区分的描述性表达。"
    first_use_definition: "脓毒症全病程候选动态系统表征（下称‘候选表征’）"
    competing_forms_and_locators:
      - "候选动态系统表征、候选全病程表示、候选架构、候选状态表示、候选系统表征、候选表示、整个系统模型 — 第27–67、92、252–370、393–406行"
    acceptance_test: >-
      全篇角色复核后，同一中央对象只使用“候选表征”；“复杂候选模型”和“阶段 II 冻结的候选表征”各自只指其已定义角色；不再以“候选架构”“候选系统表征”“最小全病程候选表示”或无指代范围的“整个系统模型/整个模型”指同一对象。
  - finding_id: LNG-R059-003
    severity: major
    finding_kind: terminology
    category: simulation_and_clinical_recovery_terminology
    dossier_locator:
      - "摘要、Objectives 和核心假设（第32、34、39、41、42、52、66、71行）"
      - "后发病结局与状态定义（第186、195、200、202行）"
      - "Absolute simulation and semi-synthetic recovery gate（第214、220、225行）"
      - "Evidence chains、输出和解释（第265、290、293、329、345、353、364、365、376、381、394、403、425行）"
    current_problem: >-
      “恢复”同时表示患者“生理恢复”（第186、195、200、202行）和模拟中对状态、转移或结构的重建（其余所列位置）；“绝对恢复”“恢复门”和“可恢复不变量”在首次出现时没有说明重建对象，“假置信”则是难以由跨学科读者直接理解的压缩标签。正文另以“错误结构高置信”（第225行）给出了更直接的含义。
    target_state: >-
      临床状态、模拟重建性能和对错误结构的高置信度支持使用三个互不混淆的直接表述。
    required_change_or_replacement: >-
      患者结局统一称“生理恢复状态”；模拟语境首次写“在已知生成机制下重建预设状态、转移和结构的性能（下称‘模拟重建性能’）”；把“假置信”改为“错误结构被高置信度支持的频率”或“对错误结构的高置信度支持”。把“绝对恢复/假置信门”直接改为“模拟重建性能和错误结构高置信度支持率的预设判定标准”。
    content_to_preserve: >-
      保留临床恢复状态的操作定义、所有模拟阈值、零边与错设情景、弃权规则以及对可解释结构的限制。
    term_or_phrase: "恢复、绝对恢复、假置信"
    recommended_form_or_plain_description: "生理恢复状态；模拟重建性能；错误结构被高置信度支持的频率"
    evidence_basis: "原稿用同一词根表示临床结局与模拟评价，并未提供‘绝对恢复’或‘假置信’为标准术语的证据；描述性替换直接对应原稿定义的评价对象。"
    first_use_definition: "在已知生成机制下重建预设状态、转移和结构的性能（下称‘模拟重建性能’）"
    competing_forms_and_locators:
      - "恢复、生理恢复、绝对恢复、恢复门、可恢复不变量、假置信、错误结构高置信 — 第32–71、186–225、265–425行"
    acceptance_test: >-
      全篇检索中，裸用“恢复”不再横跨患者状态和模拟评价；“生理恢复状态”“模拟重建性能”“错误结构被高置信度支持的频率”各自只承担一种角色，首次出现即可识别所指对象。
  - finding_id: LNG-R059-004
    severity: major
    finding_kind: terminology
    category: decision_criteria_and_stage_labels
    dossier_locator:
      - "摘要、定位和 Objectives（第32、34、39、40、50、54、66、67、71行）"
      - "日期表、成功定义和 work packages（第79、83–88、95、98、100、106、110、112行）"
      - "G1 审计与方法章节（第122、125、127、131、138、142–148、161、189、212、214行）"
      - "RCT R0/R1 与后续复述（第244、246、250、254、270、276、284、290、293、303、304、317、326、335、343、347、352–355、368、370、380、383、391–407、422–428、435行）"
    current_problem: >-
      “门”被用作资源确认、数据审计、模型性能、任务评价、外部检验和 RCT 启动等不同科学条件的共同隐喻，形成“绝对模拟恢复门”“绝对恢复/假置信门”“绝对 Monte Carlo 门”“试验语义门”“观测投影门”“真正外部门”“Brier 非劣门”“泄漏门”“合取门”等大量形式。G1 在第84行先以“硬下限”出现，直到后文仍未给出一句可直接识别其科学内容和功能的定义；R0/R1 虽在第246、250行列项，但标题和复述仍主要使用英文内部标签。
    target_state: >-
      每个条件以其科学对象和判定功能命名；G1、R0、R1 仅作为在中文全称之后使用的短标签。
    required_change_or_replacement: >-
      第84行首次写“达到预设的双数据库可观测性审计最低标准（G1）”；第246行标题写“试验语义与共同生理锚点合格性标准（R0）”；第250行标题写“测量一致性、校准与投影重建误差标准（R1）”。其余“门”按实际功能改为“启动条件”“最低标准”“判定标准”“停止条件”或“进入下一分析阶段的条件”；例如第32行改为“模拟重建性能达到预设标准”和“冻结观测投影满足预设一致性与可计算性标准”。
    content_to_preserve: >-
      保留所有日期、阈值、先后顺序、合取关系、停止条件和 RCT 两阶段判定，不改变任何方法选择。
    term_or_phrase: "门、G1、R0、R1 及其派生标签"
    recommended_form_or_plain_description: "按科学对象分别使用最低标准、判定标准、启动条件或停止条件；代码只在中文功能名称之后作短标签"
    evidence_basis: "原稿把一个项目隐喻用于多种不同科学条件，未提供其为领域通用术语的证据；功能性描述来自原稿已有的对象、阈值与后果。"
    first_use_definition: "达到预设的双数据库可观测性审计最低标准（G1）"
    competing_forms_and_locators:
      - "绝对模拟恢复门、试验语义门、观测投影门、真正外部门、Brier 非劣门、泄漏门、合取门以及未先解释的 G1/R0/R1 — 第32–435行所列位置"
    acceptance_test: >-
      全篇不再以裸用“门”承担科学定义；G1、R0、R1 的第一次读者正文出现均紧随中文全称和功能说明，后续短标签只指该一定义，且任何标准的数值和后果均未丢失。
  - finding_id: LNG-R059-005
    severity: major
    finding_kind: terminology
    category: validation_data_roles_and_parameter_updates
    dossier_locator:
      - "摘要、成功定义和 work packages（第32、39–42、71、87、98、109、112行）"
      - "外部数据库角色与医院分区（第134、144、189、228–240行）"
      - "R1、evidence chain 和 required analyses（第250、275、308–312、332行）"
      - "失败解释、定位与风险表（第346、355、365、366、370、382、404、406、416、423、427行）"
    current_problem: >-
      外部验证数据角色交替写成“适配区/最终测试区”“adaptation/test”“untouched final test”“未触碰 test”“第二数据库未触碰测试区”“真正未触碰/未触碰数据库外/未触碰外部/未触碰跨库”；参数更新状态则交替写成“零更新/zero update/zero-update/zero”“仅校准/adaptation-only calibration/calibration”“仅观测层更新/adaptation-only observation-layer update/adaptation-only decoder/decoder adaptation/observation”，以及“全模型重拟合/full refit/transport updating/development/transport update”。至少四个需要严格区分的核心角色被中英文和不同短语交叉命名。
    target_state: >-
      两类数据集和四种参数处理状态各有一个中文名称，并在第一次出现时以直接操作说明定义。
    required_change_or_replacement: >-
      数据角色统一为“适配医院集”和“最终检验医院集”，首次说明后者在模型开发和适配期间不查看结局或模型性能。四种处理状态依次写为：“不更新任何模型参数”“仅用适配医院集重新估计校准截距和斜率”“仅用适配医院集重新估计观测层参数”“用目标数据库重新拟合全模型（属于模型再开发，不作为外部验证）”。第40行先给出这一组定义，随后全篇只用对应中文短称。
    content_to_preserve: >-
      保留医院 30%/70% 分配、跨分区患者规则、最终检验数据不参与开发、执行次序、允许重新估计的参数范围以及全模型重拟合不属于外部验证的边界。
    term_or_phrase: "外部验证数据角色与参数重新估计状态"
    recommended_form_or_plain_description: "适配医院集、最终检验医院集，以及四种明确说明哪些参数被重新估计的中文操作名称"
    evidence_basis: "原稿用中英文竞争形式交叉命名至少六个操作角色；推荐形式直接复述数据使用和参数操作，不主张新的标准术语。"
    first_use_definition: "适配医院集；最终检验医院集在模型开发和适配期间不查看结局或模型性能"
    competing_forms_and_locators:
      - "适配区/adaptation、最终测试区/test/untouched，以及 zero update、calibration、decoder/observation update、full refit/transport update — 第32–427行所列位置"
    acceptance_test: >-
      全篇角色复核后，数据集只称“适配医院集/最终检验医院集”，四种参数状态只使用上述四个操作性名称；不再出现 adaptation/test、untouched、zero-update、decoder adaptation、full refit 或 transport updating 等竞争形式，且每一处读者均能判断哪些参数发生了重新估计。
  - finding_id: LNG-R059-006
    severity: major
    finding_kind: terminology
    category: contingent_trial_branch_terminology
    dossier_locator:
      - "摘要、研究问题和 Objective 4（第32、41、42、54、60、67、88、110、125行）"
      - "Conditional trial-observation projection and independent fallback（第242、246、248、250、252、254、276行）"
      - "RCT evidence chain、输出和解释（第314、317–319、335、347、356、368、369、383–384、395、405–406、428行）"
    current_problem: >-
      投影分支的同一量被称为“投影可观测状态摘要”“投影可观测摘要”“投影摘要”“RCT 可观测代理 P_obs”“death-ranked 投影摘要”，结果又称“状态扰动估计”“访视特异扰动”“有限随机化扰动”或“组间不同”。失败分支则在“独立 death-ranked SOFA 临床状态再分析/端点”“独立 SOFA 分支”“trial-specific independent secondary clinical-state reanalysis”“trial-specific clinical-state 再分析”“独立试验临床状态”和“fallback”之间切换。读者难以确认这些形式是否指同一统计量、同一分析分支和同一可支持结论。
    target_state: >-
      投影量、投影分支的比较、独立临床状态分支各有一个直接中文名称；P_obs 仅在定义后作公式符号使用。
    required_change_or_replacement: >-
      第248行定义为“基于实际 D7/D8 观测值计算的一维投影摘要（P_obs）”；投影分支结果统一写“随机分组在该访视投影摘要上的差异”。第254行定义失败分支为“独立于阶段 II 候选表征、按死亡和 SOFA 排序的试验特异性次要临床状态分析（下称‘独立临床状态分析’）”。摘要、图题候选、evidence chain、解释矩阵和 claim-support 表同步使用这两个中文分支名。
    content_to_preserve: >-
      保留 D7/D8、死亡和出院的排序、P_obs 公式、中心/分层相容的比较、两个试验分开报告、分支触发条件，以及不验证潜在动力学或整个候选表征的限制。
    term_or_phrase: "观测投影分支及独立临床状态分支的竞争称谓"
    recommended_form_or_plain_description: "一维投影摘要（P_obs）、随机分组在该访视投影摘要上的差异、独立临床状态分析"
    evidence_basis: "原稿没有证明‘观测投影’及其派生形式为领域标准术语；推荐形式直接对应公式、比较量和独立分析的科学功能。"
    first_use_definition: "基于实际 D7/D8 观测值计算的一维投影摘要（P_obs）"
    competing_forms_and_locators:
      - "投影可观测状态摘要、投影可观测摘要、投影摘要、可观测代理、death-ranked 投影摘要及多种扰动名称 — 第32–428行所列位置"
      - "独立 death-ranked SOFA、独立 SOFA 分支、trial-specific clinical-state、fallback、独立试验临床状态 — 第242–428行所列位置"
    acceptance_test: >-
      全篇角色复核只保留“一维投影摘要（P_obs）/随机分组在该访视投影摘要上的差异”和“独立临床状态分析”两组名称；不再出现 death-ranked、fallback、projection-pass、trial-specific clinical-state 或用“扰动”单独命名结果的竞争形式。
  - finding_id: LNG-R059-007
    severity: minor
    finding_kind: terminology
    category: evidence_and_analysis_status_language
    dossier_locator:
      - "Current verified-resource versus prospective-gate status 表（第118–129行）"
      - "G1 表和 external-validation output（第138、142–148、310行）"
      - "Title and positioning claim-support table（第401–410行）"
      - "Identity and final stop boundary（第437、439行）"
    current_problem: >-
      三类不同状态在中文正文中使用未定义英文代码：资源证据状态为 verified/unverified/not generated/project-local derivative（第120–129行），运输性分析状态为 stable/database-specific/abstained（第310行），主张支持状态为 supported/qualified/unsupported（第403–410行）；第439行还把机器字段 identity_status、preserved 和 new_idea_required 写入读者正文。虽然这些状态维度不应合并，但当前形式要求读者掌握项目内部标签。
    target_state: >-
      三类状态分别以自然中文定义和呈现，机器状态不进入读者正文。
    required_change_or_replacement: >-
      资源表使用“已有公开资料支持/尚未核验/尚未生成/项目内衍生资料”；运输结果使用“跨数据库稳定/仅适用于特定数据库/证据不足而不作解释”；主张表使用“有支持/有条件支持/无支持”。第439行改为“本版本保留原研究构想的核心问题、目标、研究对象、证据基础和推断单位；若这些要素发生所列变化，应作为新的研究构想另行评估”。
    content_to_preserve: >-
      保留资源证据状态、运输性分析状态和主张支持状态之间的维度差异，并保留第439行的研究构想边界。
    term_or_phrase: "读者正文中的机器状态标签"
    recommended_form_or_plain_description: "按资源状态、跨数据库结果状态和主张支持状态分别使用自然中文说明"
    evidence_basis: "这些英文串和机器字段属于项目状态表示而非已证明的领域标准术语；中文替换逐项保留原状态含义。"
    first_use_definition: "已有公开资料支持／尚未核验／尚未生成／项目内衍生资料"
    competing_forms_and_locators:
      - "verified/unverified/not generated/project-local derivative、stable/database-specific/abstained、supported/qualified/unsupported、identity_status/preserved/new_idea_required — 第118–148、310、401–439行"
    acceptance_test: >-
      每张表有且只有一组已定义的中文状态；三组状态不互换；读者正文不再出现上述英文状态串或 identity_status/new_idea_required。
  - finding_id: LNG-R059-008
    severity: major
    finding_kind: terminology
    category: model_disposition_and_workflow_metaphors
    dossier_locator:
      - "摘要、定位与日期表（第32、40–42、50、52、54、67、71、83–88行）"
      - "工作包、模拟判定和外部验证（第95、106–112、122、125、144、155、212、220、224–226、238、242、246、250、254、259、270–278行）"
      - "Evidence chains、输出、停止条件和风险表（第288、294、296、300、304、309–312、318、329、333、335、344–358、364–370、394–407、422–430、439行）"
    current_problem: >-
      模型和分析的处置结果由项目管理或软件隐喻表达：自动降级/降级、准入/晋级、淘汰、挽救/救回/豁免、封存/封印、防火墙、失败产物/失败图，以及 data-access no-go、fallback、stop、stable/database-specific/abstained 等。相同词根跨越不同操作，例如“降级”有时指改时间网格、有时指改模型、有时指改推断范围；“淘汰”有时指停止复杂模型，有时仅指停止结构解释。第439行的内部状态词进一步把工作流状态暴露给读者。
    target_state: >-
      每处直接说明发生的科学操作、保留的分析和停止的主张，不用处置隐喻代替后果。
    required_change_or_replacement: >-
      按语境逐项替换：“降级”改为“转用 24 小时/事件时间”“转用多状态或线性基线”或“仅作数据库层面的描述”；“淘汰”改为“停止继续评估该复杂候选模型”或“该结构不再解释”；“准入/晋级”改为“进入下一分析阶段”；“挽救/救回/豁免”改为“不能抵消该项失败，也不能支持继续该分析”；“封存”改为“停止继续分析并保存现有结果”；“防火墙”改为“变量角色分离规则”；“失败图/失败产物”改为“显示未满足标准的状态、医院或变量的图/记录”。英文 no-go、fallback、stop 和内部状态改为相应中文操作与后果。
    content_to_preserve: >-
      保留所有预设替代路线、停止条件、可继续报告的基线或描述性结果、不可支持的主张，以及变量角色分离的实质规则。
    term_or_phrase: "模型和分析处置的项目管理或软件隐喻"
    recommended_form_or_plain_description: "逐处直接写明停止的分析、采用的替代分析、仍可报告的结果和不再支持的主张"
    evidence_basis: "原稿未提供这些隐喻为科研领域标准术语的证据，且同一词根对应不同操作；功能性替换来自原稿各处明确后果。"
    first_use_definition: "不建立新的总括短标签；在每个首次处直接陈述相应科学操作与后果"
    competing_forms_and_locators:
      - "降级、准入、晋级、淘汰、挽救、救回、豁免、封存、封印、防火墙、失败产物/图、no-go、fallback、stop — 第32–439行所列位置"
    acceptance_test: >-
      对所列位置逐项检查后，每个处置句都明确回答“停止哪一分析、转用哪一分析、仍可报告什么、不能再主张什么”；不再依赖降级、淘汰、晋级、挽救、封存、封印、防火墙、no-go、fallback 或 stop 等未展开隐喻。
  - finding_id: LNG-R059-009
    severity: minor
    finding_kind: language
    category: readability_and_clause_density
    dossier_locator:
      - "One-sentence complete-Idea summary（第32行）"
      - "Gate R0 与 Gate R1 方法段（第246、250行）"
      - "RCT 启动前条件（第335行）"
      - "closest-work 限制段（第397行）"
    current_problem: >-
      这些位置把研究对象、条件、方法、失败分支和边界压入单个长句或单段清单；第32行还叠加多个前置修饰语。即使术语统一，跨学科读者仍需回读以确认主句和条件的附着关系。
    target_state: >-
      每段先给主句，再用并列结构或项目符号列条件；一句只承担一个主要论证动作。
    required_change_or_replacement: >-
      第32行仍保持“一句话摘要”，但压缩为“研究对象与阶段 I–II 证据；满足条件后才进行两项 RCT 次要分析及失败分支”两个并列主干。第246、250、335行各保留一句定义性主句，把资格条件、数值标准和失败后果改成项目符号；第397行把检索结论、覆盖限制和允许主张分成三句。
    content_to_preserve: >-
      保留所有限定条件、数值阈值、失败分支、检索范围和证据强度，不以删去科学条件换取简短。
    acceptance_test: >-
      第32行仍为一个完整句且只有两个并列主干；第246、250、335行的每个项目只表达一类条件；第397行分别陈述检索所得、未覆盖范围和可允许定位，修订后无需回读即可确定每个修饰语的所指。
unresolved_issues:
  - LNG-R059-001
  - LNG-R059-002
  - LNG-R059-003
  - LNG-R059-004
  - LNG-R059-005
  - LNG-R059-006
  - LNG-R059-007
  - LNG-R059-008
  - LNG-R059-009
---

# Language Assessment Report

**Assessment ID**: language-assessment-r059  
**Target Language**: Chinese (zh-CN)  
**Discipline**: multidisciplinary critical-care medicine, clinical epidemiology, longitudinal statistics, system identification, systems science, and medical AI  
**Target Journal**: not specified  
**Scope**: complete Idea dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

语法和时态总体稳定，但标题修饰关系、中央研究对象、判定条件、外部验证数据角色、参数更新状态和 RCT 两个分支的名称尚未形成跨学科读者可直接识别的一致体系。术语硬门失败，因此目前不能判为语言就绪；这些问题均可通过有边界的术语统一和句法重组修复，无需专业编辑全面重写。

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 5 | borderline |
| Terminology Consistency | 3 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 4 | borderline |
| Readability & Flow | 4 | borderline |

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 约 0–1 个明确语法错误/500 词级单位（按中文词级近似）；未超过阈值 |
| Academic register | pass | 多节存在内部工作流隐喻和中英文切换，但并非以会话体为主；按术语问题处理 |
| Terminology coherence | fail | 至少 8 个核心角色族存在竞争形式、未定义内部标签或误导性修饰关系 |
| Tense systematic violation | pass | 作为前瞻性 Idea dossier，计划性语气在方法和预期结果中保持一致 |

## Strengths

- 前瞻计划、尚未生成的结果和已完成证据之间大体使用不同语气，未系统性地把计划写成既成结果。
- 预测、关联、随机化比较与因果机制之间的边界多次以明确否定句表达。
- 多数数值标准、时间点和失败后果均可定位，便于实施语言修订时保留原意。
- 主要和次要任务、两个随机试验以及投影分支与独立临床状态分支在结构上可辨认。

## Specific Issues

### Chinese Academic Clarity

- **LNG-R059-001（major）**：标题把“稀疏”句法上附着到 RCT，而正文显示稀疏的是随访测量。使用 frontmatter 中给出的完整替换标题，并同步改写第34、50、60、67、314、376、397、405行。
- **LNG-R059-008（major）**：多节使用“门、降级、淘汰、晋级、挽救、封存、封印、防火墙”等内部工作隐喻。逐处改为科学条件、实际操作和可支持结论。
- **LNG-R059-009（minor）**：第32、246、250、335、397行的条件密度过高；保留所有条件但重组主句、并列项和项目符号。

推荐标题已经重新解析：  
“脓毒症全病程候选动态系统表征：计划开展跨数据库检验，并在满足预设条件时对随机对照试验的稀疏随访测量进行次要分析”。其中，“全病程”和“候选”修饰“动态系统表征”；“在满足预设条件时”限制“进行次要分析”；“随机对照试验的”和“稀疏”均修饰“随访测量”。未发现修订标题把条件、证据状态或数据属性移接到错误中心词。

### Grammar & Syntax

未发现达到可单列级别的系统性语法错误。主要句法风险来自修饰语堆叠和长句，而不是主谓、时态或成分残缺；见 LNG-R059-001 和 LNG-R059-009。

### Academic Register & Tone

正文整体不是会话体，但内部项目管理词和软件式状态词削弱学术语体。具体替换见 LNG-R059-004、LNG-R059-007 和 LNG-R059-008。

### Terminology Consistency

以下只列触发问题的核心角色，是一次性全篇角色一致性复核的结果；未建立或保存完整术语清单。

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| LNG-R059-001 | 条件性稀疏 RCT 次要再分析 | 第27、31、34、50、60、67、314、376、397、405行；第54、261行显示预期数据属性 | 熟悉重症和研究设计，但不熟悉新标签 | “稀疏”修饰对象错误，“条件性”附着不清 | 在满足预设条件时对随机对照试验的稀疏随访测量进行次要分析 | 标题直接展开，不另造短标签 | 句法修饰关系与 dossier 自身第54、261行 | 全篇无“稀疏 RCT”，标题修饰关系通过复解析 |
| LNG-R059-002 | 中央候选表征 | 第27、31、32、34、39、42、50、54、60、65、67、92、252、254、287、311、319、368–370、393、403、406行 | 不熟悉项目内部对象层级 | 表征、表示、架构、系统表征和模型的角色未区分 | 候选表征；复杂候选模型；阶段 II 冻结的候选表征 | “脓毒症全病程候选动态系统表征（下称‘候选表征’）” | 直接描述研究对象及实现层级，无需外部核验 | 全篇每个形式只承担一个已定义角色 |
| LNG-R059-003 | 恢复/绝对恢复/假置信 | 第32、34、39、41、42、52、66、71、85、107、186、195、200、202、214、220、225、265、290、293、329、345、353、364、365、376、381、394、403、425行 | 临床、统计和系统辨识混合读者 | 同一词根跨临床状态和模拟评价；“假置信”不透明 | 生理恢复状态；模拟重建性能；错误结构被高置信度支持的频率 | 首次明确“在已知生成机制下重建预设状态、转移和结构的性能” | dossier 已给出三个不同功能和对应阈值 | 全篇三种角色不再共用裸词“恢复/假置信” |
| LNG-R059-004 | 门、G1、R0、R1 | 第32、34、39、40、50、54、66、67、71、79、83–88、95、98、100、106、110、112、122、125、127、131、138、142–148、161、189、212、214、244、246、250、254、270、276、284、290、293、303、304、317、326、335、343、347、352–355、368、370、380、383、391–407、422–428、435行 | 不熟悉项目内部阶段或状态词 | 同一隐喻承载多类科学条件；G1 首次出现未定义 | 启动条件、最低标准、判定标准、停止条件；中文全称后再用 G1/R0/R1 | G1、R0、R1 的完整首次定义见 frontmatter required change | 直接描述各条件功能，无需外部核验 | 无裸用“门”；三个短标签首次出现均有中文全称和功能 |
| LNG-R059-005 | 外部验证数据角色与参数更新状态 | 第32、39–42、71、87、98、109、112、134、144、189、228–240、250、275、308–312、332、346、355、365、366、370、382、404、406、416、423、427行 | 熟悉验证概念，但不熟悉本项目的英文短称 | 两类数据和四种更新状态在多组中英文形式间切换 | 适配医院集、最终检验医院集；不更新参数、仅重新估计校准参数、仅重新估计观测层参数、重新拟合全模型 | 第40行直接说明每个数据集和每种参数操作 | dossier 已明确各状态允许改变的参数 | 全篇只保留两类数据名和四种操作名，读者可判断哪些参数改变 |
| LNG-R059-006 | RCT 投影分支与独立临床状态分支 | 第32、41、42、54、60、67、88、110、125、242、246、248、250、252、254、276、314、317–319、335、347、356、368、369、383–384、395、405–406、428行 | 不熟悉新投影标签或内部英语分支名 | 同一统计量、比较和失败分支存在多种名称 | 一维投影摘要（P_obs）；随机分组在该访视投影摘要上的差异；独立临床状态分析 | 第248、254行按 frontmatter 直接定义 | dossier 自身公式、排序规则和分支边界 | 两个分支各只有一个中文名称，P_obs 仅作定义后的符号 |
| LNG-R059-007 | 证据、运输和主张支持状态 | 第118–129、138、142–148、310、401–410、437、439行 | 不熟悉内部英文状态枚举 | 三个不同状态维度均使用未定义英文标签，机器状态进入正文 | 分别使用三组中文状态；机器状态改为自然句 | 各表标题下定义该表状态维度 | 角色分离来自 dossier 表格自身功能 | 每表一组中文状态，三组不混用，正文无机器状态词 |
| LNG-R059-008 | 模型处置和分析流程结果 | 第32、40–42、50、52、54、67、71、83–88、95、106–112、122、125、144、155、212、220、224–226、238、242、246、250、254、259、270–278、288、294、296、300、304、309–312、318、329、333、335、344–358、364–370、394–407、422–430、439行 | 不熟悉内部工作流或软件隐喻 | 相同隐喻对应不同科学操作和结论范围 | 直接写停止、转用、保留和不再支持的对象 | 每个处置句展开为“停止什么/转用什么/仍可报告什么/不能主张什么” | 功能性描述即可，不需验证紧凑标签是否标准 | 所列位置均可直接识别操作和后果，不再依赖处置隐喻 |

**观察到的竞争形式与位置（按触发角色汇总）**：

- 标题数据属性：`条件性稀疏 RCT 次要再分析`（第27、31、67、405行）；`严格条件化的稀疏 RCT 次要再分析层`（第34行）；`稀疏 RCT 层/次要分析`（第50、376、397行）；`实际稀疏 RCT 访视`（第60行）；`条件性稀疏 RCT 观测投影或独立临床状态再分析`（第314、405行）。第54、261行的“重复测量稀疏/稀疏 D1…访视”确认“稀疏”应附着于测量或访视数据。
- 中央对象：`候选动态系统表征`（第27、31、32、60行）；`候选表征`（第34行）；`候选全病程表示`（第39行）；`候选架构`（第50行）；`候选状态表示`（第65行）；`计划跨数据库候选系统表征`（第92、311行）；`候选表示`（第287、393行）；`最小全病程候选表示`（第370行）；`阶段 II 表征/模型、整个系统模型/整个模型`（第32、42、54、67、252、254、319、368、369、406行）。
- 临床与模拟“恢复”：`生理恢复`（第186、195、200、202行）；`绝对模拟恢复/绝对恢复/恢复门/恢复与准入门/状态恢复/recovery/恢复失败/恢复通过`（第32、34、39、42、66、71、85、107、214、220、265、290、293、345、353、364、365、376、381、394、403、425行）；`假置信/错误结构高置信`（第39、41、52、66、71、85、225、293、329、345、353、376行）。
- 外部数据角色：`适配区/最终测试区`（第40行）；`adaptation/test` 或单独 adaptation/test（第109、134、144、189、230、234、236–240、250、275、308–312、332、382、404、416、423行）；`untouched final test`（第230行）；`未触碰 test`（第98、134、189、382行）；`第二数据库未触碰测试区`（第87行）；`真正未触碰、未触碰数据库外、未触碰外部、未触碰跨库`（第32、39、41、71、87、109、112、346、370、376、404行）。
- 参数处理状态：`零更新`（第40、42、87、98、310行）、`zero update`（第240、309行）、`zero-update`（第98、250、355、365、366、382、404、427行）；`仅校准`（第40、87行）、`adaptation-only calibration`（第240、309行）、`calibration`（第109、427行）；`仅观测层更新`（第40、87行）、`adaptation-only observation-layer update`（第240行）、`adaptation-only decoder`（第309行）、`decoder adaptation/observation`（第109、427行）；`全模型重拟合/transport updating/development`（第240行）、`transport updating`（第310行）、`full refit`（第312行）、`transport update`（第427行）。
- RCT 投影分支：`投影可观测状态摘要`（第32、252行）；`投影可观测摘要`（第42、60、88、318、319、368、383、406行）；`投影摘要`（第67、317、347行）；`RCT 可观测代理 P_obs/一维可观测代理`（第248、250、252、276行）；`投影可观测状态扰动/访视特异扰动/有限随机化扰动/有限访视扰动/随机化投影摘要扰动/组间不同`（第41、42、60、67、88、252、318、319、368、383行）。
- RCT 独立分支：`独立 death-ranked SOFA 临床状态再分析/次要再分析/端点`（第32、41、67行）；`独立 SOFA 端点/分支`（第88、110、125、276、356行）；`independent fallback/fallback`（第242、246、254、335、384、405、428行）；`trial-specific independent secondary clinical-state reanalysis/trial-specific clinical-state 再分析`（第254、318行）；`独立临床状态再分析/独立次要临床状态差异/独立试验临床状态`（第54、60、314、369、384行）；`death-ranked 投影摘要/SOFA`（第317、347、384、406、428行）。
- 状态语言：资源状态 `verified/unverified/not generated/project-local derivative`（第120–129行）；分析状态 `stable/database-specific/abstained`（第310行）；主张状态 `supported/qualified/unsupported`（第403–410行）；机器状态 `identity_status/preserved/new_idea_required`（第439行）。
- 模型处置：`降级/自动降级`（第32、40、42、84、85、95、106、107、112、122、125、144、155、220、226、238、259、278、294、312、329、333、345、358、423、430、439行）；`淘汰`（第224、225、353、425行）；`准入/晋级`（第40、85、272、300、304、345、358行）；`挽救/救回/豁免`（第71、189、212、250、265、296、353、356、357、425行）；`封存/封印`（第87、275、358、430、439行）；`防火墙`（第157、271、344、376、407行）；`no-go/fallback/stop`（第83、118、121、242、246、254、256、258、259、310、335行）；`失败产物/失败图`（第41、50、87、109、278、309、310、346、404、407行）。

### Tense & Voice Conventions

前瞻性计划使用“计划、将、须、若……则……”等形式，与 Idea dossier 的研究状态一致；未见把计划性方法系统写成已完成方法的时态问题。

### Conciseness & Redundancy

关于“预测表现不能抵消恢复、外部或投影标准失败”的边界在第71、85、95、112、189、212、224–226、250、265、296、304、353、356、357、365–369、425、427行多次以“不能挽救/豁免/救回”等近义句出现。语言修订应先统一为直接后果，再由后续叙事评估决定各推理位置是否都需保留；本报告不指定删除哪一个科学推理位置。

### Readability & Flow

LNG-R059-009 所列长句和密集条件段是主要障碍。术语统一后，再把 R0、R1 和 RCT 启动条件改成“定义句 + 条件清单 + 失败后果”，可在不删科学条件的前提下显著降低回读负担。

## Language Revision Priorities

1. **Terminology and title attachment**: 6 个 major findings — 先固定标题、中央对象、模拟/临床恢复、判定标准、外部更新状态和 RCT 两分支的单一名称。
2. **Reader-facing scientific operations**: 1 个 major finding — 把模型处置与工作流隐喻展开为停止、转用、保留和不支持的具体对象。
3. **Evidence-status labels**: 1 个 minor finding — 为三种不同状态维度分别使用中文标签，并移除机器状态词。
4. **Readability**: 1 个 minor finding — 重组摘要和高密度方法段，不删除阈值或失败条件。

## Re-Assessment Status (if applicable)

不适用。本次为全新独立的 Idea dossier 基线评估，未读取既有问题清单、评分、决定、修订稿或版本差异。

## Assessment Notes

- 评估仅涵盖中文学术语言、术语可及性、语体、简洁性和可读性；未评价科学有效性、统计方法优劣、新颖性、影响或期刊适配。
- 已在内存中完成中央研究对象、主要任务/结局、次要诊断、条件性 RCT 分支、证据状态、外部验证数据角色、参数更新状态、模型处置和分析状态的全篇角色一致性复核；仅报告触发问题的角色，未生成或保存术语登记、证据包或其他产物。
- **Focused verification**: 未执行。所有触发项都可用 dossier 已陈述的科学对象、操作、关系或错误类型作直接描述性替换；无需为保留或新造紧凑标签检索外部来源。
- 文件读取范围严格限于 frontmatter 的 `files_read`；dossier 和 reader handoff 均为只读，未修改任何源文件。
