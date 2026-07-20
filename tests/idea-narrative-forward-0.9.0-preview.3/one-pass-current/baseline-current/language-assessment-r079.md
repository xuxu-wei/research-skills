---
review_id: language-assessment-r079
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-independent-academic-language-assessor-r079
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r079
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
  - finding_id: LANG-R079-T01
    severity: major
    finding_kind: terminology
    category: 术语可理解性、首次定义与跨语境歧义
    dossier_locator:
      - "Title, summary, audience, and positioning / One-sentence complete-Idea summary（第 32 行）"
      - "Structured abstract / Objective and hypothesis（第 39 行）"
      - "Research design and methods / Absolute simulation and semi-synthetic recovery gate（第 214–226 行）"
    current_problem: >-
      “绝对模拟恢复门/绝对恢复”在摘要和核心假设中先于操作说明出现；“恢复”同时用于模拟中对状态、转移或结构的重建，以及第 193–204 行的患者“生理恢复”状态。跨学科读者在首次出现处无法判断它指模型可恢复性、临床恢复，还是一般性能阈值。
    target_state: >-
      用一个直接说明模拟目的和绝对判据的名称指代模型可恢复性检验，并始终与患者的“生理恢复”分开。
    required_change_or_replacement: >-
      在首次读者可见位置改为“基于预设绝对阈值的模拟可恢复性检验”，其后可简称“模拟可恢复性检验”；把仅写作“恢复门”“绝对门”或“绝对 recovery”的同一概念统一到该表达。不得把患者状态“生理恢复”改成同一短语。
    content_to_preserve: >-
      保留正确指定、零边、过拟合和错设生成情景，以及状态、转移概率、结构、校准、覆盖率和弃权的全部预设数值判据；保留“预测表现不能补偿可恢复性失败”的边界。
    acceptance_test: >-
      全篇核对后，模拟语境只使用“模拟可恢复性检验/模拟可恢复性”，患者状态只使用“生理恢复”；摘要首次出现即说明它在预设生成情景中按绝对阈值检验能否正确重建状态、转移和结构；不再残留无定语的“恢复门”或中英混写的“绝对 recovery”。
    term_or_phrase: 绝对模拟恢复门／绝对恢复
    recommended_form_or_plain_description: 基于预设绝对阈值的模拟可恢复性检验
    evidence_basis: >-
      第 214–226 行已经给出该概念的实际内容：在预设数据生成情景中，以 ARI/相关、转移 MAE、覆盖率、符号/滞后恢复率、FDR、错误结构和校准等绝对阈值判断模型能否重建目标量。建议表达直接取自这组操作说明，不把 dossier 的压缩标签假定为领域标准术语。
    first_use_definition: >-
      “基于预设数据生成情景和绝对阈值，检验候选模型能否正确重建状态、转移概率、预设结构及概率校准的模拟可恢复性检验。”
    competing_forms_and_locators:
      - "绝对模拟恢复门（第 32 行）"
      - "绝对恢复（第 34、42、66、71、107、265、290、345、353、376、381、394、403 行）"
      - "绝对 Monte Carlo 门（第 40 行）"
      - "恢复门（第 71 行）"
      - "Monte Carlo 与半合成绝对门（第 85 行）"
      - "绝对模拟门（第 112 行）"
      - "Absolute simulation and semi-synthetic recovery gate（第 214 行）"
      - "绝对 recovery（第 293 行）"
  - finding_id: LANG-R079-T02
    severity: major
    finding_kind: terminology
    category: 非标准压缩术语与方法角色区分
    dossier_locator:
      - "Structured abstract / Objective and hypothesis（第 39 行）"
      - "Research content and work packages / dated gates（第 85 行）"
      - "Absolute simulation and semi-synthetic recovery gate（第 224–225 行）"
    current_problem: >-
      “假置信”被用作核心准入条件，却没有在首次出现处说明它究竟是零边情景中的假边检出、错设情景中的高置信错误结构，还是模型未能弃权；后文又以“零边假结构”“错设假置信”“错误结构高置信”等不同形式承载不同量。该压缩词对目标读者并非自明，并把两个应分开的评估对象合并成一个标签。
    target_state: >-
      分别、直接命名零边情景下的假结构频率，以及错设情景下的高置信错误结论与失配/弃权表现。
    required_change_or_replacement: >-
      删除单独使用的“假置信”。在总述中写作“零边情景下的假结构率，以及错设情景下的高置信错误结构率和失配/弃权检验”；在具体表格中分别使用“假边高置信检出率”和“错设模型的高置信错误结构率与弃权率”，并保持二者数值判据分开。
    content_to_preserve: >-
      保留零边情景中任一假边区间排除 0 的比例不超过 0.05、错设情景中至少 80% 重复触发失配/弃权，以及高置信错误结构不超过 0.05 的三项约束。
    acceptance_test: >-
      全篇不再出现未定义的“假置信”；每处均能从文字判断是在报告假边、错设后的高置信错误结构，还是弃权表现；第 224 行和第 225 行的不同评估量没有被重新合并。
    term_or_phrase: 假置信／零边假置信／错设假置信
    recommended_form_or_plain_description: 零边情景下的假结构率；错设情景下的高置信错误结构率与失配/弃权表现
    evidence_basis: >-
      第 224 行把零边情景操作化为“假边 95% 区间排除 0 的重复比例”，第 225 行把错设情景操作化为“触发失配/弃权的重复比例”和“错误结构高置信比例”。建议采用这三个可观察量的直接描述，不另造总括短词。
    first_use_definition: >-
      “在零边生成情景中评估假结构被高置信检出的频率，并在模型错设情景中评估高置信错误结构的频率以及模型能否识别失配并弃权。”
    competing_forms_and_locators:
      - "假置信门（第 39、66、71、293 行）"
      - "恢复/假置信/弃权（第 41、345、376 行）"
      - "结构不稳定和假置信（第 52 行）"
      - "零边假置信（第 85、329、353 行）"
      - "零边假结构（第 224 行）"
      - "错设假置信/弃权、错误结构高置信（第 225 行）"
  - finding_id: LANG-R079-T03
    severity: major
    finding_kind: terminology
    category: 核心复合术语、修饰关系与科学角色区分
    dossier_locator:
      - "One-sentence complete-Idea summary（第 32 行）"
      - "Background, current state, gap, significance, and rationale（第 54 行）"
      - "Conditional trial-observation projection and independent fallback（第 242–254 行）"
    current_problem: >-
      “冻结观测投影门”“投影可观测状态摘要”“投影可观测摘要”“可观测代理”“投影 fidelity”等形式交替出现，并以同一“投影”词根指代映射、由映射得到的变量、适用性检验、通过后的分析分支和分析结局。“投影可观测状态摘要”的修饰关系也不清楚：普通语序不能确定“可观测”修饰状态、投影还是摘要。核心 RCT 连接逻辑因此在首次出现处不可直接理解。
    target_state: >-
      分开命名四个科学角色：冻结的确定性映射、由实测共同锚点计算的一维观测代理、映射/代理的适用性检验，以及通过检验后在实际访视比较的一维观测代理结局。
    required_change_or_replacement: >-
      用“冻结的确定性映射”指映射；用“一维观测代理（P_obs）”指由共同生理锚点计算的变量；用“观测代理适用性检验（测量不变性、校准和映射忠实度）”指 R1 评估；用“访视时点的一维观测代理结局”指随机化比较对象。摘要首次出现时直接说明这四者的先后关系，避免继续使用“投影可观测……”这一修饰不明的复合形式。
    content_to_preserve: >-
      保留 C_r、冻结观测方程、SVD、P_state、P_obs、R0/R1 的全部定义与阈值，保留投影失败后转入独立 death-ranked SOFA 分支的条件，以及任何分支均不验证完整潜在动力学或整个系统模型的边界。
    acceptance_test: >-
      全篇逐处核对后，映射、代理变量、适用性检验、通过分支和结局分别使用上述唯一名称；摘要首次出现即给出一维观测代理如何由实测共同锚点和冻结观测方程得到；不存在“投影可观测状态摘要”这类修饰指向不明的表达，且 P_state 与 P_obs 未被混称。
    term_or_phrase: 冻结观测投影门／投影可观测状态摘要
    recommended_form_or_plain_description: 冻结的确定性映射；一维观测代理（P_obs）；观测代理适用性检验；访视时点的一维观测代理结局
    evidence_basis: >-
      第 246–250 行实际区分了共同锚点资格、确定性 SVD 映射、潜在状态投影 P_state、RCT 可计算的观测代理 P_obs 和 R1 的测量不变性/校准/忠实度检查；第 252 行才定义随机化比较对象。建议名称直接对应这些已写明的功能，不主张任何新的标准短词。
    first_use_definition: >-
      “仅当阶段 II 冻结观测方程能够把试验实际测得的共同生理锚点确定性地映射为一维观测代理，并且该代理在治疗组比较前通过测量不变性、校准和映射忠实度检验时，才比较实际访视时点的一维观测代理结局。”
    competing_forms_and_locators:
      - "冻结观测投影门、投影可观测状态摘要（第 32 行）"
      - "投影可观测摘要（第 42、60、252、318、319、368、383、406 行）"
      - "确定性低维投影、绝对投影忠实度门（第 54 行）"
      - "确定性投影、投影摘要（第 67 行）"
      - "观测投影门（第 88、110 行）"
      - "投影 fidelity 门（第 110、276 行）"
      - "阶段 II 状态投影 P_state、RCT 可观测代理 P_obs（第 248 行）"
      - "RCT 冻结投影器（第 276 行）"
      - "RCT 观测投影（第 314 行）"
      - "projection-pass（第 383、406 行）"
  - finding_id: LANG-R079-T04
    severity: major
    finding_kind: terminology
    category: 核心验证集角色与中英形式一致性
    dossier_locator:
      - "One-sentence complete-Idea summary（第 32 行）"
      - "Hospital-primary genuine cross-database validation（第 228–240 行）"
      - "Evidence chain: 医院优先、未触碰的计划跨数据库检验（第 306–312 行）"
    current_problem: >-
      第二数据库中的适配数据和最终外部测试数据是阶段 II 核心证据角色，但正文交替使用“真正未触碰”“未触碰 test”“untouched final test”“test”“final test”“zero update/zero-update/零更新”等形式。“未触碰”是直译式隐喻，单独出现时不能说明禁止访问的时间边界；“test”又同时指数据集、医院和操作。读者必须跨段推断数据角色与更新层级。
    target_state: >-
      用稳定的中文名称区分数据角色，并用直接动词说明各更新层级。
    required_change_or_replacement: >-
      数据角色统一为“适配集”和“预先隔离的独立外部测试集（模型、变量、阈值和更新策略冻结前不可访问）”；分析层级统一为“完全不更新的外部验证”“仅重新校准”“仅更新观测模型”和“全模型重新拟合”。首次出现时给出不可访问边界，此后不再以“未触碰/test/untouched”代替角色名称。
    content_to_preserve: >-
      保留按医院 30%/70% 预分配、患者跨分区排除、测试医院不得进入适配集、测试结果不得用于选择变量或阈值、有限更新不能替代完全不更新结果，以及全模型重拟合不属于外部验证的全部限制。
    acceptance_test: >-
      全篇核对后，eICU 的两个数据角色只称“适配集”和“独立外部测试集”，且首次出现包含开发阶段不可访问的定义；四种分析层级各有唯一中文名称；普通中文正文不再出现裸用的“test”“untouched final test”或“zero-update”，代码标识和表内既有符号除外。
    term_or_phrase: 真正未触碰的跨数据库检验／未触碰 test／untouched final test／zero update
    recommended_form_or_plain_description: 预先隔离的独立外部测试集；完全不更新的外部验证；仅重新校准；仅更新观测模型
    evidence_basis: >-
      第 230–240 行已明确该角色的实际边界：医院先行分配、测试医院不进入适配集、模型和阈值冻结后才单次运行，并依次区分不更新、仅校准、仅观测层更新和全模型重拟合。建议用这些操作事实直接命名，避免把英文标签或“未触碰”隐喻当作标准术语。
    first_use_definition: >-
      “第二数据库预先按医院划分为适配集和独立外部测试集；后者在模型、变量、阈值和更新策略冻结前不可访问，并首先用于完全不更新的外部验证。”
    competing_forms_and_locators:
      - "真正未触碰的跨数据库检验（第 32 行）"
      - "未触碰数据库外测试、未触碰跨库结果（第 39、41 行）"
      - "零更新外部检验（第 42 行）"
      - "未触碰最终测试（第 66 行）"
      - "真正外部门、未触碰测试区（第 87 行）"
      - "未触碰 test、zero-update（第 98、189、250、382 行）"
      - "adaptation/test、zero/calibration/observation 更新（第 109 行）"
      - "untouched final test、test、adaptation（第 230–240 行）"
      - "未触碰外部检验（第 306–312、346、358、370、376 行）"
      - "zero update/zero-update/零更新（第 40、98、240、309、355、365、366、404、427 行）"
  - finding_id: LANG-R079-T05
    severity: minor
    finding_kind: terminology
    category: 项目隐喻与描述性科学表达
    dossier_locator:
      - "Candidate variable-role firewall（第 157–165 行）"
      - "Key techniques and implementation（第 271 行）"
      - "Contribution and evidence ladder（第 376 行）"
    current_problem: >-
      “变量角色防火墙/状态—行动—观察防火墙”是软件式隐喻；其实际功能已在表格中写成字段角色划分、标签副本隔离和时间滞后。跨学科读者不需要该隐喻，且后文又以“变量角色表”“三过程分工”“角色防火墙”等形式切换。
    target_state: >-
      用描述性名称稳定表示字段角色的唯一分配与隔离规则。
    required_change_or_replacement: >-
      统一改为“变量角色划分与隔离规则”；首次出现时说明每个字段只承担一个主要角色，标签派生副本与预测特征隔离，并按可用时间实施滞后。
    content_to_preserve: >-
      保留 Y_t、A_t、M_t、label-only 和 B 的全部角色边界，以及器官支持不得充当生理锚点、标签派生副本不得泄漏的限制。
    acceptance_test: >-
      全篇只用“变量角色划分与隔离规则”指这一机制；“状态、行动和观察过程”仅作为被划分的科学角色，不再与“防火墙”组合；所有原有角色约束仍可逐项定位。
    term_or_phrase: 变量角色防火墙／状态—行动—观察防火墙
    recommended_form_or_plain_description: 变量角色划分与隔离规则
    evidence_basis: >-
      第 161–165 行的角色表已经直接列出每类变量的允许用途与禁止用途，足以构成定义；建议名称来自该表所陈述的实际操作，不依赖软件隐喻或项目内部词汇。
    first_use_definition: >-
      “变量角色划分与隔离规则：每个字段只承担一个主要分析角色；标签派生副本与预测特征分开存放，并按信息实际可用时间实施滞后。”
    competing_forms_and_locators:
      - "变量角色防火墙（第 271、344 行）"
      - "变量角色表（第 328 行）"
      - "状态—行动—观察防火墙（第 376 行）"
      - "三过程分工（第 403 行）"
      - "角色防火墙（第 407 行）"
  - finding_id: LANG-R079-L06
    severity: major
    finding_kind: language
    category: 可读性、句法负载与信息层级
    dossier_locator:
      - "One-sentence complete-Idea summary（第 32 行）"
      - "Primary research question（第 60 行）"
    current_problem: >-
      一句话摘要约 345 个字符，在一个句子中连续嵌入研究对象、两阶段证据、三项先决条件、两个试验访视、投影分支、替代分支和禁止主张；主研究问题约 192 个字符，又在总问句内嵌三个层级不同的子任务和条件分支。两处均承担首次定向功能，却要求读者在核心术语尚未定义时同时保持过多条件关系。
    target_state: >-
      摘要仍满足单句字段要求，主问题仍保持一个明确问句，但各自采用并列、同构的主干，只保留辨认研究对象、阶段关系和边界所需的信息。
    required_change_or_replacement: >-
      压缩一句话摘要中的实现细节，把“构建并检验候选表征—在先决条件满足后进行 RCT 次要分析—不作因果或数字孪生主张”写成清楚的三段并列主干；主研究问题的三个编号分句使用平行谓语和一致的宾语层级。不得删除 24 个月范围、跨数据库检验、RCT 条件分支或非因果边界。
    content_to_preserve: >-
      保留全病程研究对象、知识约束和不确定性、阶段 I–II、第二数据库独立检验、阶段 III 的条件性与替代分析、EXIT-SEP D7/XBJ-SCAP D8，以及不支持因果网络、连续动力学、控制或数字孪生的边界。
    acceptance_test: >-
      一句话摘要仍为一个句子且只有一个清楚的条件分支；主研究问题的三个编号分句均以平行动词开头并共享同一研究对象。不了解项目内部标签的目标读者可仅凭这两处指出研究对象、阶段 II 的验证动作、阶段 III 的启动条件与失败后的分析去向。
  - finding_id: LANG-R079-L07
    severity: major
    finding_kind: language
    category: 方法段可读性与条件组织
    dossier_locator:
      - "Gate R0 — trial semantics and common-anchor eligibility（第 246 行）"
      - "Gate R1 — measurement invariance, calibration and absolute projection fidelity（第 250 行）"
    current_problem: >-
      R0 和 R1 各自被写成约 470–480 个字符的单一段落。资格条件、变量排除、数值阈值、数据来源、盲态检查和失败后果连续串接；尤其 R1 在同一句群中混合奇异轴能量、相关、NMAE、回归校准、覆盖率、锚点校准、试验范围支持和失败规则。内容可定位，但语言结构没有显出判定层级。
    target_state: >-
      每个方法段按“前提—所需数据—判定指标—失败后果”分层，使每个数值阈值只附着于一个明确对象。
    required_change_or_replacement: >-
      将 R0 拆成试验语义前提、共同锚点纳入条件、最低锚点数和失败去向；将 R1 拆成低维性、P_state/P_obs 一致性、校准与覆盖、试验盲态可计算性和失败去向。可用短句或项目符号，但不得把不同阈值合并或改变其逻辑关系。
    content_to_preserve: >-
      保留全部 R0/R1 数据语义、变量排除条件、至少两个锚点、所有数值阈值、试验标签遮蔽、不得根据 RCT 结果调参，以及任一条件失败即进入独立 SOFA 分支的规则。
    acceptance_test: >-
      R0 和 R1 中每个句子或项目符号只承担一个判定功能；每个数值阈值紧邻其被判定对象；读者无需回读即可分别列出资格、映射、校准、范围支持和失败后果，且与原文逐项核对时没有阈值或限制缺失。
  - finding_id: LANG-R079-L08
    severity: major
    finding_kind: language
    category: 中文学术语域与中英混排
    dossier_locator:
      - "Observational target, anchoring and abstention（第 208–212 行）"
      - "Hospital-primary genuine cross-database validation（第 230–240 行）"
      - "Required analyses and evidence（第 335 行）"
      - "Contribution and evidence ladder（第 376 行）"
      - "Remaining execution gates（第 435 行）"
    current_problem: >-
      中文正文系统性保留普通英文名词、动作词和项目标签，例如 loading、cross-loading、bin、stay、test、adaptation、fallback、stop、benchmark/resource、center handling、threshold registry、simulation stability；同一段中还把中文、缩写、代码式斜线和英文复合词连续堆叠。标准符号与通用缩写可以保留，但这些普通英语形式未定义且并非都承担不可替代的专业含义，削弱中文学术语域和跨学科可读性。
    target_state: >-
      保留必要的标准缩写、数学符号、数据库名和方法名；普通叙述概念使用自然中文，确需保留的英文术语在首次出现处给出中文名称和英文原词。
    required_change_or_replacement: >-
      对全文做一次限定范围的中英混排校订：将普通词替换为“载荷/交叉载荷、时间区间、住院记录、测试集、适配集、替代分析、停止、基准或资源、中心处理、阈值登记表、模拟稳定性”等直接中文；仅在首次定义或精确代码/符号语境保留英文。不得翻译 ICU、SOFA、RCT、SVD、MAR、MNAR、FDR、ESS 等已成为标准缩写的形式，但应确保首次出现对目标读者足够清楚。
    content_to_preserve: >-
      保留公式、变量符号、数据库和试验专名、统计量缩写、既有数值阈值，以及真正需要逐字对应分析代码或数据字段的标识符。
    acceptance_test: >-
      全文检索普通英文词后，每个保留项要么是标准缩写/专名/数学符号，要么在首次出现处有中文名称和用途说明；上述五个定位段不再依赖未定义的英文普通名词来表达数据角色、判定动作或失败后果。
  - finding_id: LANG-R079-L09
    severity: minor
    finding_kind: language
    category: 简洁性、限定语叠加与近义重复
    dossier_locator:
      - "Structured abstract / Expected result and Contribution and impact（第 41–42 行）"
      - "Core hypothesis and non-hypotheses（第 71–73 行）"
      - "Projection-pass estimand and Automatic independent fallback（第 252–254 行）"
      - "Evidence chain: 条件性稀疏 RCT…（第 318–320 行）"
      - "Interpretation matrix and closest-work boundary（第 368–370、397–410 行）"
    current_problem: >-
      “不支持/不验证潜在动力学、转移边、中介、控制或整个模型”等边界语句和“条件性、次要、访视特异、分试验”等限定在多个相邻或近邻位置近义复现。多数限定具有科学作用，但局部重复增加篇幅并遮蔽每段的新信息。
    target_state: >-
      每个 cited 段落只陈述一次与该段功能直接相关的边界，限定语采用固定顺序和固定形式；跨章节是否保留同一边界由叙事审阅决定，语言校订不替代该决定。
    required_change_or_replacement: >-
      仅压缩上述定位内的近义复述和重复限定，把同一段内的禁止主张合并为一次平行列举；不要自行删除跨章节的科学边界，也不要决定应由哪个章节独占该边界。
    content_to_preserve: >-
      保留预测与因果的区分、投影分支与独立 SOFA 分支的不同解释范围、试验不合并、阶段 III 不补足阶段 II 失败，以及对数字孪生、控制、机制和临床推广的限制。
    acceptance_test: >-
      每个列出的段落中，同一限制不再以近义句重复两次；所有原有限定仍可在原章节范围内找到；任何跨章节删留都附有单独的叙事审阅决定，而不是由本语言 finding 自动决定。
unresolved_issues:
  - LANG-R079-T01
  - LANG-R079-T02
  - LANG-R079-T03
  - LANG-R079-T04
  - LANG-R079-T05
  - LANG-R079-L06
  - LANG-R079-L07
  - LANG-R079-L08
  - LANG-R079-L09
---

# Language Assessment Report

**Assessment ID**: language-assessment-r079  
**Target Language**: Chinese（zh-CN）  
**Discipline**: 重症医学与临床流行病学，结合纵向统计、系统辨识、系统科学和医疗 AI  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

文本的基本语法、学术审慎程度和计划性时态总体可靠，但核心方法术语在首次出现处对既定跨学科读者不可直接理解，且同一科学角色在多种中英形式间切换；这是非补偿性的术语问题。摘要、主研究问题和 RCT 方法段还存在显著句法超载。因此，在术语与可读性完成系统修订前，不宜视为语言就绪。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 6 | borderline |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 全篇未见超过阈值的明确语法错误；约 0–1 个/500 个中文词语单位，主要问题是句法负载而非语法失范 |
| Academic register | pass | 多个章节有中英混排和项目式术语，但语气并非口语或会话体，未达到非正式语域硬门槛 |
| Terminology coherence | fail | 至少四组核心概念在摘要、核心假设或主要设计中仍不可直接理解或跨形式切换：模拟可恢复性、错误高置信结构、RCT 观测代理链和独立外部测试角色 |
| Tense systematic violation | pass | 计划、尚未生成、条件性启动和已核验事实的证据状态区分一致；没有把计划工作系统性写成已完成结果 |

---

## Strengths

- 对“计划”“尚未生成”“条件满足时”“当前未核验”的使用稳定，能够持续区分拟议研究、既有证据和未来结果。
- 学术语气总体审慎，没有以宣传性词语替代证据；对预测、因果、机制、控制和数字孪生的边界表达明确。
- X_t、Y_t、A_t、M_t、B、S、P_state 和 P_obs 等数学对象在方法部分有明确局部定义，数值阈值通常紧邻对应表格。
- 章节、表格和证据链结构清楚，有助于定位数据角色、分析步骤、产物和限制。
- 中文标点、数值和标准缩写总体一致，未发现系统性主谓失配、残句或时态错误。

---

## Specific Issues

### Chinese Academic Clarity

- **LANG-R079-L06（major）**：一句话摘要和主研究问题在首次定向位置承载过多嵌套条件；需要在不改变字段结构和科学边界的前提下压缩主干。
- **LANG-R079-L07（major）**：R0/R1 方法段把资格、指标、阈值与失败后果写入两个超长段落；需要按判定功能分层。
- **LANG-R079-L08（major）**：普通英文叙述词在中文正文中系统性混用，影响跨学科读者的连续阅读。
- **LANG-R079-L09（minor）**：相邻或近邻位置重复相同的禁止主张和限定语；语言修订只处理局部复述，不决定跨章节科学边界的放置。

### Grammar & Syntax

未发现达到 actionable finding 程度的明确语法错误。长句问题记录在 LANG-R079-L06 和 LANG-R079-L07，属于句法负载与信息组织，而不是主谓、成分残缺或指代失范。

### Academic Register & Tone

LANG-R079-L08 记录了普通英文词、代码式斜线和项目标签对中文学术语域的系统性干扰。文本语气本身正式、克制，因此学术语域硬门仍通过。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LANG-R079-T01 | 绝对模拟恢复门／绝对恢复 | 第 32、39、214–226 行 | 与患者“生理恢复”冲突，首次出现无法辨认模拟评估对象 | yes |
| LANG-R079-T02 | 假置信／零边假置信／错设假置信 | 第 39、85、224–225 行 | 把假边、高置信错误结构和弃权三个量压成一个不透明词 | yes |
| LANG-R079-T03 | 冻结观测投影门／投影可观测状态摘要 | 第 32、54、242–254 行 | 映射、代理、检验、分支和结局角色混称，复合修饰关系不明 | yes |
| LANG-R079-T04 | 未触碰 test／untouched final test／zero update | 第 32、228–240、306–312 行 | 数据角色和更新层级依赖中英混合标签，访问边界不自明 | yes |
| LANG-R079-T05 | 变量角色防火墙 | 第 157–165、271、376 行 | 软件隐喻替代已可直接描述的变量角色隔离规则 | yes |

以上仅为触发问题的集中术语核查，不是术语清单。建议表达均依据 dossier 自己给出的操作定义形成直接描述；本评估不把未核验的压缩词宣布为领域标准，也未另建术语产物。

### Tense & Voice Conventions

没有发现系统性问题。作为研究构想，文本恰当地使用“计划、须、若、条件满足时、尚未生成”等前瞻表达；对文献和已有试验使用陈述式，对未完成的访问、审计、模型和结果保持未完成状态。主动与无主句式均符合中文跨学科研究计划的常见表达。

### Conciseness & Redundancy

LANG-R079-L06 和 LANG-R079-L07 反映中心句与方法段的信息压缩过度；LANG-R079-L09 反映限制语的局部近义重复。修订时必须保留科学条件，只调整局部重复、限定顺序和句内层级。

### Readability & Flow

整体章节流向清楚，但核心定向句和 RCT 方法段的局部阅读负荷显著高于其余部分。LANG-R079-T01 至 T04 的首次定义修复应先于 LANG-R079-L06/L07 的句法压缩，否则压缩后的句子仍会依赖不透明术语。

---

## Language Revision Priorities

1. **Terminology Consistency**: 5 issues — 先区分模拟评估、错误高置信结构、RCT 映射/代理/检验/结局和外部数据角色，并完成全篇一致性核对。
2. **Readability & Flow**: 2 issues — 在术语确定后压缩一句话摘要、主研究问题，并分层重组 R0/R1 方法段。
3. **Academic Register & Tone**: 1 issue — 将普通英文叙述词改为自然中文，只保留必要缩写、专名、符号和首次定义的英文原词。
4. **Conciseness & Redundancy**: 1 issue — 在不决定跨章节科学边界的前提下，清理每个定位段内部的近义复述和限定语叠加。

---

## Re-Assessment Status (if applicable)

本次为 Idea dossier 的全新、完整独立评估，不适用既往问题清单比对。

| Check | Current assessment |
|--------|--------------------|
| Listed issues no longer present | 不适用；未读取既往问题清单 |
| Listed issues still present | 不适用；未读取既往问题清单 |
| New current-text issues | 9 个：LANG-R079-T01 至 T05、LANG-R079-L06 至 L09 |

---

## Assessment Notes

- 评估范围为完整 `idea-dossier-I01-001-v003`；research-idea.v3 固定的 15 个 H2、5 个推理 H3、字段标签、证据链字段及 Claim-Support 表头均视为脚手架，未评分、未要求翻译或改名。
- 学科约定按中文的重症医学/临床研究为主体，同时考虑纵向统计、系统辨识、系统科学和医疗 AI 的跨学科读者；未指定目标期刊，故未套用期刊特有格式。
- 仅读取结构化绑定的 frozen dossier、file-backed reader handoff、适用规则和 academic-language-assessor 的必需说明；未读取任何既往叙事、语言、预检、评估、修订稿、差异记录或对话预期。
- 术语建议采用 dossier 已给出的科学对象、操作和判定量的直接描述；没有进行外部术语标准性宣称，也没有创建术语表或独立术语文件。
- 本报告只判断语言；没有判断设计可行性、统计有效性、科学新颖性、证据充分性、影响力或期刊适配性，也未改动源 dossier。
