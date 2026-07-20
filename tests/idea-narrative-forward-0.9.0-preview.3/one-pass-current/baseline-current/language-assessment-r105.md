---
review_id: lang-r105
reviewer_skill: academic-language-assessor
reviewer_instance_id: baseline-language-r105
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: baseline-current-r105
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
  - research-skills-openai/skills/academic-language-assessor/references/common-l1-interference-patterns.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/scan_idea_language_candidates.py
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
coverage_receipt:
  reader_entry:
    status: completed
    reviewed_count: 13
    basis: 已完整检查标题、摘要各字段、主要研究问题、核心假设与非假设等全部有界读者入口单元。
  core_scientific_role:
    status: completed
    reviewed_count: 11
    basis: 已核对实际存在的研究对象、主要任务与目标量、检验和更新操作、失败分支及贡献等核心角色的全部读者称名。
  terminology_concordance:
    status: completed
    reviewed_count: 12
    basis: 已对候选扫描触发的 12 个概念簇完成首用、复合修饰关系与全篇一致性核对；仅报告有读者证据的问题簇。
  local_language:
    status: completed
    reviewed_count: 277
    basis: 已逐一检查除固定 H2/H3 标题和 Markdown 分隔线外的全部正文、列表、表格与参考文献单元。
findings:
  - finding_id: LAR-105-01
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: conditional-rct-secondary-analysis
    normalized_locator: title-positioning-objective
    failure_mode: modifier-attachment-obscures-data-property
    fingerprint: meso|conditional-rct-secondary-analysis|title-positioning-objective|modifier-attachment-obscures-data-property
    category: 中文学术清晰度；术语；标题复合修饰关系
    dossier_locator:
      - 第 27、31 行标题
      - 第 34、50、67 行定位与目标
      - 第 376、397、405 行贡献与定位正文
    current_problem: >-
      “条件性稀疏 RCT 次要再分析”“严格条件化的稀疏 RCT 次要再分析层”和“稀疏 RCT 层”使“稀疏”在普通句法下更像修饰 RCT 本身，而文中实际指试验的重复测量或访视资料稀疏；“条件性/严格条件化”也未在标题中说明是哪一分析受哪些前置条件约束。
    target_state: >-
      标题和首次定位应明确：稀疏性属于访视资料，次要再分析仅在预设的阶段 II、试验语义和投影条件满足后开展；后文使用一个稳定简称。
    required_change_or_replacement: >-
      将标题后半部改成修饰关系明确的直接表述，例如“计划跨数据库检验；仅在预设条件满足后利用 RCT 稀疏访视资料开展次要再分析”。首次正文说明三类前置条件后，可统一简称为“有前置条件的 RCT 次要再分析”；删除“严格条件化的稀疏 RCT 层”等易误附着形式。标题改写后须再次检查“稀疏访视资料”“预设条件”和“次要再分析”各自的修饰对象。
    content_to_preserve: >-
      保留计划性、次要分析属性、两项试验分开分析、访视稀疏、阶段 II 之外开展以及三类前置条件；不得把条件性弱化为一般可能性。
    acceptance_test: >-
      标题与首次正文均不能把“稀疏”读成 RCT 样本量或设计属性；全篇只保留一个在首次使用后可回指的简称，且固定脚手架标题不被改名。
    term_or_phrase: 条件性稀疏 RCT 次要再分析
    recommended_form_or_plain_description: >-
      仅在预设条件满足后利用 RCT 稀疏访视资料开展的次要再分析
    evidence_basis: >-
      本文第 54、169、171、244–261 行把稀疏性具体归于重复测量和实际访视，并把条件具体归于阶段 II、试验语义与投影判定；因此可直接描述，无需外部术语核验。当前复合修饰关系会支持“RCT 本身稀疏”的错误读法。
    first_use_definition: >-
      在标题或紧随标题的首个自由文本单元中说明：“该次要再分析仅在阶段 II、试验语义和观测投影均达到预设标准后开展，所用 RCT 资料仅含稀疏的实际访视测量。”
    competing_forms_and_locators:
      - “严格条件化的稀疏 RCT 次要再分析层”——第 34 行
      - “稀疏 RCT 层”——第 50、376、397 行
      - “条件性稀疏 RCT 次要再分析”——第 27、31、67、405 行
  - finding_id: LAR-105-02
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: randomized-projection-endpoint
    normalized_locator: summary-methods-evidence-chain
    failure_mode: competing-forms-obscure-referent
    fingerprint: meso|randomized-projection-endpoint|summary-methods-evidence-chain|competing-forms-obscure-referent
    category: 术语一致性；主要目标量
    dossier_locator:
      - 第 32、42、60、67、88 行读者入口与目标
      - 第 248、250、252、276 行投影定义与估计目标
      - 第 317–319、347、368、383、406 行输出与解释
    current_problem: >-
      “投影可观测状态摘要”“投影可观测摘要”“投影摘要”“一维可观测代理 P_obs”及“状态投影 P_state”在核心入口和后文交替出现。第 248、252 行实际上区分了潜在状态的一维投影、由实测锚点计算的代理以及加入死亡/出院排序后的试验结局，但入口称名把三者压成同一个标签。
    target_state: >-
      分别命名潜在状态投影、实测锚点代理和最终有序访视结局，并在第一次出现时说明它们的关系；后文不得用“投影摘要”同时指代多个对象。
    required_change_or_replacement: >-
      首次出现时直接写成“由试验实际访视的共同生理测量计算的一维可观测代理 P_obs”；方法部分保留“潜在状态投影 P_state”与“可观测代理 P_obs”的明确区分；进入治疗组比较时另称“由死亡、P_obs 和存活出院共同排序的访视结局”。全篇逐项替换模糊的“投影可观测状态摘要/投影摘要”，并按这三个科学角色完成一致性检查。
    content_to_preserve: >-
      保留冻结映射、每项试验独立的共同锚点、D7/D8 实际访视、P_state 与 P_obs 的数学定义、死亡和出院排序以及有限随机化解释边界。
    acceptance_test: >-
      全篇检索后，P_state 只指潜在状态投影，P_obs 只指实测锚点代理，治疗组比较的目标只用一个明确的有序访视结局名称；标题、摘要、目标、方法、输出和解释表中的回指一致。
    term_or_phrase: 投影可观测状态摘要／投影可观测摘要／投影摘要／可观测代理 P_obs
    recommended_form_or_plain_description: >-
      由冻结观测方程和试验实际访视共同锚点计算的一维可观测代理 P_obs；用于组间比较时，明确称为由死亡、P_obs 和存活出院共同排序的访视结局
    evidence_basis: >-
      第 248 行给出 P_state 与 P_obs 两个不同对象，第 252 行又增加死亡和存活出院的排序；当前跨位置称名没有稳定保留这一区别。该判断来自 dossier 内部定义与给定跨学科读者基线，不需要外部来源。
    first_use_definition: >-
      在第 32 行首次提及时写明“由试验实际访视共同生理测量计算的一维可观测代理；治疗组比较时再与死亡和存活出院共同组成有序访视结局”，完整公式可继续留在第 248 行。
    competing_forms_and_locators:
      - “投影可观测状态摘要”——第 32、252 行
      - “投影可观测摘要”——第 42、60、88、318、319、368、383、406 行
      - “投影摘要”——第 67、317、347、383 行
      - “RCT 可观测代理 P_obs”——第 248 行
      - “一维可观测代理”——第 276 行
      - “阶段 II 状态投影 P_state”——第 248、250 行
  - finding_id: LAR-105-03
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: independent-sofa-fallback-endpoint
    normalized_locator: summary-objective-methods-outputs
    failure_mode: undefined-and-inconsistent-endpoint-name
    fingerprint: meso|independent-sofa-fallback-endpoint|summary-objective-methods-outputs|undefined-and-inconsistent-endpoint-name
    category: 术语一致性；失败分支结局
    dossier_locator:
      - 第 32、41、42、54、67、88、110、125 行读者入口与计划
      - 第 254、276、317、318 行方法与输出
      - 第 347、356、369、384、395、405、428 行结果解释与备选路径
    current_problem: >-
      同一失败分支被称为“death-ranked SOFA 临床状态再分析”“独立 SOFA 分支/端点”“trial-specific independent secondary clinical-state reanalysis”“trial-specific clinical-state 再分析”和“独立临床状态再分析”。核心入口在给出死亡、住院 SOFA 和存活出院的排序定义之前就使用英文复合短语，跨学科读者无法判断这是 SOFA 连续结局、序数复合结局还是一个阶段 II 状态端点。
    target_state: >-
      首次使用即以中文直接说明三层排序和该端点与阶段 II 表征的独立性，随后只使用一个稳定的中文简称。
    required_change_or_replacement: >-
      在第 32 行首次使用时写成“与阶段 II 表征独立的有序次要临床状态端点：D7/D8 前死亡最差，访视时仍住院者按 SOFA 从高到低排序，访视前存活出院最有利”。其后统一简称为“独立的 SOFA 有序临床状态端点”；仅在确有必要时于首次定义后括注一个英文名称，不再交替使用 death-ranked、trial-specific、fallback 和多种中文短称。
    content_to_preserve: >-
      保留投影失败才启用、每项试验独立、SOFA/死亡/住院/出院语义必须可核验、与阶段 II 表征无关以及核心语义失败时停止新端点的条件。
    acceptance_test: >-
      第一次出现即可辨认三层排序与独立性；全篇只保留一个中文简称，且所有失败分支、输出、解释表和风险表均回指同一端点。
    term_or_phrase: death-ranked SOFA／独立 SOFA／trial-specific independent secondary clinical-state reanalysis
    recommended_form_or_plain_description: >-
      与阶段 II 表征独立的 SOFA 有序临床状态端点：死亡最差，访视时住院者按 SOFA 从高到低排序，访视前存活出院最有利
    evidence_basis: >-
      第 254 行已直接规定三层排序和独立性，但第 32 行起的多套简称未传递该定义。推荐形式完全展开 dossier 已固定的对象和操作，不依赖外部术语或新造短语。
    first_use_definition: >-
      在第 32 行首次出现处给出三层排序、D7/D8 访视和“与阶段 II 表征独立”三个要素，后文再使用统一简称。
    competing_forms_and_locators:
      - “death-ranked SOFA 临床状态再分析/端点”——第 32、41、67、317、347、384、428 行
      - “独立 SOFA 分支/端点”——第 42、88、110、125、276、356、369、395、405 行
      - “trial-specific SOFA 层级端点”——第 54 行
      - “trial-specific independent secondary clinical-state reanalysis”——第 254 行
      - “trial-specific clinical-state 再分析”——第 318 行
      - “与阶段 II 独立的临床状态再分析”——第 54 行
  - finding_id: LAR-105-04
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: recoverable-invariant-targets
    normalized_locator: abstract-hypothesis-observational-target
    failure_mode: core-target-defined-after-first-use
    fingerprint: meso|recoverable-invariant-targets|abstract-hypothesis-observational-target|core-target-defined-after-first-use
    category: 术语可理解性；核心假设目标量
    dossier_locator:
      - 第 39、71 行摘要与核心假设
      - 第 208–212、225、273 行目标、锚定与判定
      - 第 293–295、376、381–382 行证据链与贡献
    current_problem: >-
      “恢复不变量”“可恢复不变量”“锚定不变量”和“冻结不变量”在摘要与核心假设中承担主要目标量，但首次出现时没有说明不变量具体指哪些量、在哪类允许重参数化下保持不变，容易被不同领域读者分别理解为因果不变量、物理守恒量或跨数据库稳定参数。
    target_state: >-
      第一次出现时直接列明本项目允许解释的不变量及其限定关系，之后使用一个稳定短称；“恢复”应明确为在预设模拟生成机制中重建，而非从观察数据识别真实系统。
    required_change_or_replacement: >-
      将首次用语改为“在预先允许的重参数化下仍保持一致、并能在预设模拟生成机制中重建的状态占用率、转移概率、锚点预测以及预设依赖的符号或滞后”，随后统一简称为“可恢复不变量”。把“锚定不变量”“冻结不变量”分别改为“受锚定约束的这些量”和“冻结后接受外部检验的这些量”，避免暗示新的不变量类别。
    content_to_preserve: >-
      保留允许的重参数化、状态占用、转移概率、锚点预测、符号/滞后、模拟恢复、外部稳定性及不解释任意潜变量坐标的边界。
    acceptance_test: >-
      摘要首次使用即可回答“不变量是什么、在哪种等价关系下不变、恢复发生在何种证据环境”；全篇不再用三个未定义的修饰变体指同一组量。
    term_or_phrase: 恢复不变量／可恢复不变量／锚定不变量／冻结不变量
    recommended_form_or_plain_description: >-
      在允许的重参数化下保持一致、并能在预设模拟生成机制中重建的状态占用率、转移概率、锚点预测以及预设依赖的符号或滞后
    evidence_basis: >-
      第 71、208–212 行已限定具体量、重参数化和解释边界，说明该概念可由 dossier 自身直接展开；第 39 行的首次用语未携带这些限定，给定读者横跨临床、流行病学、系统辨识和系统科学，存在多种合理但互不相同的专业读法。
    first_use_definition: >-
      在第 39 行“恢复不变量”首次出现处同句给出量的类型、允许重参数化和模拟恢复语境；完整阈值可保留在后文。
    competing_forms_and_locators:
      - “恢复不变量”——第 39 行
      - “可恢复不变量”——第 71、295 行
      - “锚定不变量”——第 376 行
      - “冻结不变量”——第 382 行
  - finding_id: LAR-105-05
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: cross-database-validation-updates
    normalized_locator: abstract-external-validation-methods
    failure_mode: mixed-language-competing-operation-names
    fingerprint: meso|cross-database-validation-updates|abstract-external-validation-methods|mixed-language-competing-operation-names
    category: 术语一致性；中英混用；外部检验操作
    dossier_locator:
      - 第 40、87、98、109 行摘要与工作包
      - 第 230–240、250 行外部检验方法
      - 第 308–312、355、365–366、382 行证据链与解释
      - 第 404、427 行定位与风险表
    current_problem: >-
      同一组外部检验操作在“零更新/zero update/zero-update”“适配/adaptation”“仅校准/仅观测层更新”“有限更新”“transport updating/update”和“运输/运输性”之间切换；裸用“运输”还会产生普通汉语中的物流含义。读者需要反复回到第 240 行才能辨认哪些参数保持冻结、哪些允许更新以及哪一种不属于外部验证。
    target_state: >-
      为四个操作分别使用一个中文名称，并在首次出现时说明更新对象与证据身份；跨数据库表现统一使用“跨数据库适用性”或定义后的“可运输性”，不以裸词“运输”指代统计概念。
    required_change_or_replacement: >-
      全篇统一为：（1）“冻结模型不作任何更新的外部检验”；（2）“仅更新校准参数的适配分析”；（3）“仅更新观测层参数的适配分析”；（4）“全模型重新拟合，仅作为模型开发而非外部验证”。首次列举后可分别简称为“不更新外部检验”“仅校准适配”“仅观测层适配”和“全模型重拟合”。把“外部运输/适配后运输/transport update”改为直接说明“跨数据库适用性”或“适配后的跨数据库表现”。
    content_to_preserve: >-
      保留医院优先分区、最终测试区不可用于开发、四种更新层级、零更新为主要外部检验、有限适配不能补偿主要外部检验失败以及全模型重拟合不属于外部验证。
    acceptance_test: >-
      全篇检索后，每个更新名称唯一对应一组可更新参数和一种证据身份；不再混用 zero-update/zero update/零更新，也不再以裸词“运输”表示跨数据库适用性。
    term_or_phrase: 零更新／zero update／adaptation／有限更新／transport updating／运输
    recommended_form_or_plain_description: >-
      冻结模型不作任何更新的外部检验；仅更新校准参数的适配分析；仅更新观测层参数的适配分析；全模型重新拟合（仅作模型开发）
    evidence_basis: >-
      第 240 行已经给出四种操作的参数边界和证据身份，足以直接描述；其他位置的中英混用和短称省略了这一差别。该问题由内部一致性和给定读者基线触发，无需外部核验。
    first_use_definition: >-
      在第 40 行首次列举外部分析时，以四个中文名称说明各自更新对象，并明确第一种为主要外部检验、第四种不属于外部验证。
    competing_forms_and_locators:
      - “零更新/zero update/zero-update”——第 40、42、87、98、240、250、309、310、312、355、365、366、382、404、427 行
      - “适配/adaptation/adaptation-only”——第 40、66、87、109、134、230、234、237、240、308、309、312、404、423、427 行
      - “仅校准/仅观测层更新/有限更新”——第 40、87、98、240、310、312、355、366、382、404 行
      - “transport updating/transport update/外部运输/适配后运输”——第 240、278、310、355、366、427 行
  - finding_id: LAR-105-06
    severity: major
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: eligibility-and-failure-consequences
    normalized_locator: positioning-gates-methods-risks
    failure_mode: internal-metaphors-replace-scientific-actions
    fingerprint: meso|eligibility-and-failure-consequences|positioning-gates-methods-risks|internal-metaphors-replace-scientific-actions
    category: 学术语域；中文清晰度
    dossier_locator:
      - 第 34、41–42、50 行定位与摘要
      - 第 79–112 行日期判定与工作包
      - 第 230–240、250 行外部检验与投影判定
      - 第 271、275、294、329、345、353–358 行技术与停止条件
      - 第 376、407、424–430 行贡献与风险表
    current_problem: >-
      “门/硬门/按门”“变量角色防火墙”“外部封印”“泄漏清零”“打开 test”“救回/挽救”和不带对象的“自动降级”把不同的科学判定、数据访问控制和替代分析压成项目管理或软件隐喻。文本整体仍属正式语域，但这些内部化短语遍布多个章节，削弱跨学科可读性并掩盖具体的判定对象与后果。
    target_state: >-
      每处使用标准科学或方法学语言，直接写明判定标准、受影响对象、允许的替代分析和对可支持主张的后果。
    required_change_or_replacement: >-
      将“X 门/硬门”改为“预先规定的 X 判定标准/准入条件”；“变量角色防火墙”改为“变量角色分离规则”；“外部封印”改为“外部测试集预分配、权限隔离和分析冻结”；“泄漏清零”改为“无未解决的高严重度信息泄漏问题”；“打开 test”改为“授权访问并分析最终外部测试集”；“救回/挽救”改为“不能补偿或改变未通过判定”。每个“降级”须写出实际替代项及其可支持的主张，例如“改用多状态模型，并停止复杂结构解释”。R0/R1 等必要短标签可在直接定义后保留。
    content_to_preserve: >-
      保留所有预设判定标准、日期、访问隔离、变量角色边界、自动替代分析、停止规则和不可支持的结论；不得通过语言简化删除任何科学条件。
    acceptance_test: >-
      所列位置不再依靠项目管理或软件隐喻才能理解；每个判定句均能直接回答“什么对象按什么标准被判定，未达到时改做什么，允许支持什么结论”。
  - finding_id: LAR-105-07
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: negative-result-and-abstention-outputs
    normalized_locator: abstract-simulation-validation-outputs
    failure_mode: same-label-covers-distinct-results-and-actions
    fingerprint: meso|negative-result-and-abstention-outputs|abstract-simulation-validation-outputs|same-label-covers-distinct-results-and-actions
    category: 术语；失败结果表达
    dossier_locator:
      - 第 41、52、87、108–109 行摘要与工作包
      - 第 225、274、294、309、331 行模拟、技术与证据链
      - 第 345–346、353–354、367、381–382、394、404 行输出与解释
    current_problem: >-
      “失败图”没有说明图中失败的是医院、状态、结构、校准还是判定标准；“弃权”则交替表示检测到错设、停止结构解释、不估计治疗作用、模型不晋级和一项记录。相同短词覆盖不同科学角色，读者无法从摘要中的“弃权记录、失败图”辨认交付物。
    target_state: >-
      失败输出的名称应说明汇总对象、未达到的标准和科学后果；每种“弃权”应按实际动作分别表述。
    required_change_or_replacement: >-
      将“失败图”改为“按医院、状态、变量或结构汇总未达到预设判定标准及其后果的图表”，并在首次使用处说明实际分层；将“弃权”按语境分别改为“停止结构解释”“不估计治疗作用”“不让复杂模型晋级”或“记录未达到标准及后续处置”。全篇核对每一处，不以一个通用替换词覆盖不同动作。
    content_to_preserve: >-
      保留负向结果发布、错设检测、低支持关系、停止解释、模型不晋级以及按医院/状态/变量分层展示的计划。
    acceptance_test: >-
      摘要首次提及即可辨认负向交付物；全篇没有不带对象与后果的“失败图”或“弃权”，每个位置的名称与其实际科学动作一致。
    term_or_phrase: 失败图／弃权
    recommended_form_or_plain_description: >-
      未达到预设判定标准及其后果的分层汇总图；按具体语境分别写明停止结构解释、不估计治疗作用或模型不晋级
    evidence_basis: >-
      dossier 在第 212、225、294、309、353–354 行给出了这些词对应的不同对象和后果，证明它们不是一个单一科学操作；可直接展开，不需要外部术语核验。
    first_use_definition: >-
      在第 41 行把交付物写成“按预设对象汇总未达到标准、停止解释或不晋级决定及其原因的记录与图表”，后文再使用与具体对象对应的名称。
    competing_forms_and_locators:
      - “失败图”——第 41、87、109、309、346、382、404 行
      - “弃权/强制弃权/弃权记录/弃权清单”——第 41、52、108、225、274、294、331、345、353、354、367、381、394 行
  - finding_id: LAR-105-08
    severity: major
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: reader-entry-summary
    normalized_locator: one-sentence-summary-line-32
    failure_mode: overloaded-single-sentence
    fingerprint: micro|reader-entry-summary|one-sentence-summary-line-32|overloaded-single-sentence
    category: 可读性与衔接；中文学术清晰度
    dossier_locator: 第 32 行 One-sentence complete-Idea summary
    current_problem: >-
      该单句同时承载数据条件、四段病程、两类表征修饰语、阶段 I–II 两种检验、阶段 III 三项前置条件、两试验访视、投影成功与失败分支以及四类不支持主张；多个未定义短语又嵌入条件从句，读者无法在一次阅读中稳定分出研究对象、主要操作、分支条件和解释边界。
    target_state: >-
      在保持“一句话”字段约束的前提下，以清楚的三段并列结构依次表达阶段 I–II 主体、阶段 III 条件分支和共同解释边界，并使用本报告其他术语项规定的直接称名。
    required_change_or_replacement: >-
      仍保留一个完整句子，但只设三个可辨认的分句：（1）24 个月内构建并检验什么；（2）哪些前置条件满足时做哪一种 RCT 次要分析，失败时改做哪一种独立端点；（3）两种分支共同不能支持什么。删除不增加区分度的叠加修饰词，避免在同一名词短语内同时放置数据来源、审计状态、模型属性和证据阶段。
    content_to_preserve: >-
      保留 24 个月、两个公共 ICU 数据库及访问/可观测性前提、四段病程、阶段 I–II 检验、EXIT-SEP D7 与 XBJ-SCAP D8、投影与独立 SOFA 分支以及因果/连续动力学/控制/数字孪生边界；字段必须仍为一句话。
    acceptance_test: >-
      修订后仍恰为一个句子；目标读者无需回读即可分别指出研究对象、阶段 I–II 证据操作、阶段 III 的 if/then 分支和共同解释边界，且句中不含未定义的项目短标签。
  - finding_id: LAR-105-09
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: scope-limit-statements
    normalized_locator: summary-methods-evidence-interpretation
    failure_mode: near-verbatim-caveat-repetition
    fingerprint: meso|scope-limit-statements|summary-methods-evidence-interpretation|near-verbatim-caveat-repetition
    category: 简洁性与冗余
    dossier_locator:
      - 第 32、42、54、71–73 行入口与背景
      - 第 252–261 行 RCT 方法
      - 第 296、304、312、320 行五条证据链的限制句
      - 第 368–370、385、397、406、410、428 行解释、定位与风险表
    current_problem: >-
      “RCT 不验证潜在动力学、转移边、中介、控制或整个模型”“次要诊断或 RCT 不能补偿阶段 II 失败”以及“当前不构成数字孪生/因果网络”等边界以近乎相同的词序反复出现。必要限制本身清楚，但逐字式重复增加篇幅，并放大第 32 行等入口单元的负担。
    target_state: >-
      每个局部单元保留与其科学对象直接相关的边界，用稳定、简洁的称名避免近乎逐字重复；不同限制不得被误合并或删除。
    required_change_or_replacement: >-
      对所列位置做逐句去重：同一局部单元只保留一次完整边界，其余位置用针对当前对象的短句表达，不重复整串“潜在动力学—转移边—中介—控制—整个模型”。限制应按“投影分支”“独立 SOFA 分支”“观察性阶段 II”分别表述。由叙事评估或获批写作简报决定跨章节的最终保留位置；本项只要求消除近乎逐字的语言重复。
    content_to_preserve: >-
      保留预测不等于因果、RCT 分支不验证阶段 II 潜在结构、失败分支与阶段 II 独立、有限更新不能补偿不更新外部检验失败，以及当前不构成数字孪生、控制或临床工具的全部不同边界。
    acceptance_test: >-
      所列位置中没有一整串限制在未增加新对象、新条件或新后果时近乎逐字重复；每个科学上不同的限制仍可定位，固定章节、字段句数和表格格式均保持不变。
unresolved_issues:
  - LAR-105-01
  - LAR-105-02
  - LAR-105-03
  - LAR-105-04
  - LAR-105-05
  - LAR-105-06
  - LAR-105-07
  - LAR-105-08
  - LAR-105-09
---

# Language Assessment Report

**Assessment ID**: lang-r105
**Target Language**: Chinese
**Discipline**: 跨学科生物医学系统研究（重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学 AI 与转化研究）
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
| Academic Register & Tone | 5 | borderline |
| Terminology Consistency | 3 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 未发现可稳定复现的明确语法错误密集模式；约低于 1 个/500 词等值文本 |
| Academic register | pass | 多章节存在项目管理/软件隐喻，但正文主导语域仍是正式学术语体，未达到两个章节由会话式表达主导的阈值 |
| Terminology coherence | fail | 5 个核心概念簇存在竞争称名、首用不可解码或复合修饰误附着：条件性 RCT 分析、投影结局、独立 SOFA 端点、可恢复不变量及外部检验更新 |
| Tense systematic violation | pass | 研究计划、尚未生成的结果与条件性后续分析均持续使用前瞻或条件表达，无方法/结果时态系统性错置 |

---

## Strengths

- 研究状态始终以“计划”“尚未生成”“条件满足时”等方式表达，未把拟开展工作误写为既成结果。
- 因果、预测、结构恢复和随机化比较的动词大体保持区分，关键否定范围通常能明确落到相应对象。
- 表格中的数值、时间点、阈值和分支后果多采用平行结构，便于核对。
- P_state、P_obs、Y_t、A_t、M_t 等符号在正式定义后使用较稳定；主要问题集中在公式之前的读者称名，而非符号本身。

---

## Specific Issues

### Chinese Academic Clarity (if applicable)

- **LAR-105-01、LAR-105-02、LAR-105-03、LAR-105-04、LAR-105-05（major）**：标题、摘要和核心目标中的复合标签没有在首用处稳定指出数据属性、目标量或分析操作，跨学科读者会形成不同但合理的专业解释。
- **LAR-105-06（major）**：多章节以“门、防火墙、封印、清零、救回、降级”等内部化隐喻代替具体科学动作。
- **LAR-105-08（major）**：一句式摘要将主要研究、条件分支和解释边界压入单个高负荷句子。

### Grammar & Syntax

未发现达到单独列项阈值的明确语法错误；主要句法问题是信息过载而非句法不成立，见 LAR-105-08。

### Academic Register & Tone

- **LAR-105-06（major）**：正式语体中系统混入项目管理与软件隐喻。它们并非会话式口语，但会让判定标准和科学后果显得像内部流程指令。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LAR-105-01 | 条件性稀疏 RCT 次要再分析 | 第 27、31、34、50、67、376、397、405 行 | “稀疏”可能误修饰 RCT 本身，前置条件的作用对象不明 | yes |
| LAR-105-02 | 投影可观测状态摘要／P_obs | 第 32、42、60、67、248–252、317–319、347、368、383、406 行 | 潜在投影、实测代理和有序访视结局被读成同一对象 | yes |
| LAR-105-03 | death-ranked SOFA／独立 SOFA | 第 32、41、42、54、67、254、317、347、369、384、428 行 | 无法从首用判断端点的三层排序与阶段 II 独立性 | yes |
| LAR-105-04 | 可恢复不变量 | 第 39、71、208–212、225、273、293–295、376、381–382 行 | 临床、系统科学和系统辨识读者可能分别理解为不同种类的不变量 | yes |
| LAR-105-05 | 零更新／adaptation／transport updating | 第 40、87、98、230–240、308–312、355、365–366、404、427 行 | 不清楚哪些参数更新、哪项属于主要外部检验 | yes |
| LAR-105-07 | 失败图／弃权 | 第 41、52、87、225、274、294、309、345–346、353–354、381–382、404 行 | 失败对象、判定标准和停止动作无法从名称辨认 | yes |

### Tense & Voice Conventions

未发现可操作的时态或语态问题。文本将计划、条件分支、当前证据状态和未来交付区分得较稳定。

### Conciseness & Redundancy

- **LAR-105-09（minor）**：RCT 解释边界、阶段 II 失败不可由后续分析补偿以及非因果/非数字孪生声明在多处近乎逐字重复；应在保留所有科学差别的前提下压缩重复措辞。

### Readability & Flow

- **LAR-105-08（major）**：第 32 行是一句式摘要的主要阅读阻塞点。问题来自并列角色和嵌套条件过多，而不是固定字段必须保持一句话这一约束本身。
- **LAR-105-01 至 LAR-105-07** 的首用定义与称名统一完成后，摘要、目标、方法和解释表之间的局部回指会明显更清楚。

---

## Language Revision Priorities

1. **核心端点和分支称名**：3 个 major 问题——先区分 P_state、P_obs、有序投影结局和独立 SOFA 有序端点，并把定义前移到首次读者入口。
2. **标题、核心假设与外部检验操作**：3 个 major 问题——修复“稀疏”的修饰关系，直接定义可恢复不变量，并统一四种外部更新操作。
3. **学术语域和入口可读性**：2 个 major 问题——用判定标准、访问控制和替代分析的直接表述替代内部隐喻，再重整一句式摘要。
4. **失败输出与重复限制**：2 个 minor 问题——给负向输出可辨认名称，并压缩近乎逐字的边界重复。

---

## Re-Assessment Status (if applicable)

不适用。本次为冻结 Idea dossier 的全新独立评估，未接收匿名问题清单，也未比较任何先前版本、分数、决定或修订差异。

---

## Assessment Notes

- 评估仅覆盖绑定的 `idea-dossier-I01-001-v003` 全文（标题至参考文献）和嵌入式读者交接；未读取其他 dossier 版本、修订记录、叙事/语言/预检/评估报告或其他项目产物。
- 目标读者按交接设定为跨重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学 AI 与转化研究的 PI/研究者；只假设其掌握本专业常识，不假设其理解其他专业或本项目的内部简称。
- research-idea.v3 的固定 H2/H3 标题、字段标签、证据链标签及 Claim-Support 表头只作为定位脚手架，未被评分、翻译、改名或列为发现。
- 候选扫描器的全部有界候选均已按实际语境处置；报告只保留有读者证据的触发概念簇，没有形成完整术语清单。
- 所有建议形式均直接展开 dossier 已声明的对象、操作或后果；没有触发需要当前外部权威来源判定的标准术语争议，因此未浏览互联网，也没有外部 URL。
- 本报告只评估语言，不判断方法有效性、统计设计、创新性、可行性、影响或期刊适配性；未编辑源 dossier。
