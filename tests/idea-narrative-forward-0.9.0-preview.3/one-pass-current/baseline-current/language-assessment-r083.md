---
review_id: language-assessment-r083
reviewer_skill: academic-language-assessor
reviewer_instance_id: academic-language-assessor-fresh-r083
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r083
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
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/english-academic-language-conventions.md
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
  - finding_id: LANG-R083-001
    severity: major
    finding_kind: terminology
    category: title modifier attachment
    dossier_locator: "Title (line 27) and Title field (line 31)"
    current_problem: >-
      “条件性稀疏 RCT 次要再分析”在普通汉语句法中容易让“稀疏”修饰 RCT
      本身，而正文实际指重复测量或访视数据稀疏；该歧义位于标题中的核心设计说明。
    target_state: >-
      标题应明确把“稀疏”限定为访视或重复测量数据的属性，并保留再分析具有条件性、
      次要性且针对 RCT 的证据地位。
    required_change_or_replacement: >-
      将两处标题统一改为“脓毒症全病程候选动态系统表征：计划开展跨数据库检验及
      基于稀疏访视数据的条件性 RCT 次要再分析”。
    content_to_preserve: >-
      保留“候选”“计划开展”“跨数据库检验”“条件性”“RCT”“次要再分析”以及
      稀疏性只属于访视数据而不属于试验设计的含义。
    acceptance_test: >-
      标题和 Title 字段逐字一致；重新解析标题时，“稀疏”只修饰“访视数据”，
      且没有任何修饰语可被理解为改变 RCT、跨数据库检验或候选表征的证据类别。
    term_or_phrase: 条件性稀疏 RCT 次要再分析
    recommended_form_or_plain_description: 基于稀疏访视数据的条件性 RCT 次要再分析
    evidence_basis: >-
      读者交接文件不允许假定读者熟悉新造标签；正文第 169–171、242–261 行明确表明
      稀疏性属于 D7/D8 等离散访视测量，而不是 RCT 本身。推荐形式为直接描述，
      不依赖未经核验的紧凑术语。
    first_use_definition: >-
      在标题中直接写明“基于稀疏访视数据”，使属性所属对象无需另查定义即可确定。
    competing_forms_and_locators:
      - "条件性稀疏 RCT 次要再分析 — line 27"
      - "条件性稀疏 RCT 次要再分析 — line 31"
      - "严格条件化的稀疏 RCT 次要再分析层 — line 34"
      - "条件性稀疏 RCT 次要再分析 — line 67"
  - finding_id: LANG-R083-002
    severity: major
    finding_kind: terminology
    category: core validation criteria
    dossier_locator:
      - "One-sentence summary (line 32)"
      - "Structured abstract: Objective and hypothesis (line 39)"
      - "Objective 3 (line 66)"
      - "Absolute simulation and semi-synthetic recovery gate (lines 214–226)"
    current_problem: >-
      “绝对模拟恢复门”“绝对恢复/假置信门”“恢复与准入门”“零边假置信”等表达
      把不同的统计判定对象压缩为同一个项目化的“门”隐喻；在给出可恢复量、错误结构
      高置信概率和后续处置之前，跨学科读者无法确定每个标签究竟指评价、阈值还是决策。
    target_state: >-
      首次出现时分别命名两类科学判定：对预设生成情景中状态、转移和结构的模拟恢复
      是否达到标准，以及错误结构被高置信支持的频率是否低于标准；之后只使用与各自
      对象对应的稳定短称。
    required_change_or_replacement: >-
      在第 32 行首次出现处改为“预设的模拟恢复标准和错误结构高置信率标准”，并在
      第 214–226 行将两类标准分别定义为“模拟恢复标准”和“错误高置信控制标准”。
      全文据此替换仅写“恢复门”“假置信门”或“绝对门”的指代；涉及模型能否进入
      下一阶段时另写“达到上述标准后方可进入下一阶段”，不要让“门”同时表示统计量、
      阈值、评价结果和流程动作。
    content_to_preserve: >-
      保留所有预设生成情景、数值阈值、错误结构控制、自动停止或降级后果，以及预测
      表现不能补偿模拟恢复失败这一限制。
    acceptance_test: >-
      首次定义能让读者分别回答“评价什么、依据什么阈值、未达到时发生什么”；全文
      搜索“恢复门”“假置信门”“绝对门”不再发现未定义的独立用法，并逐处确认保留
      第 218–226 行的全部数值和处置规则。
    term_or_phrase: 绝对恢复/假置信门
    recommended_form_or_plain_description: 预设的模拟恢复标准和错误结构高置信率标准
    evidence_basis: >-
      读者交接文件不允许假定项目内部流程词汇；第 218–226 行已经给出可直接命名的
      评价对象、阈值和后果，因此可用透明描述替代未核验的紧凑标签，无需另造术语。
    first_use_definition: >-
      “模拟恢复标准用于判断预设生成情景中的状态、转移和结构能否按规定精度恢复；
      错误结构高置信率标准用于限制模型在零边或错设情景中高置信支持错误结构的频率。”
    competing_forms_and_locators:
      - "绝对模拟恢复门 — line 32"
      - "绝对恢复/假置信门 — lines 39 and 66"
      - "恢复与准入门 — line 85"
      - "绝对 Monte Carlo 门 — line 40"
      - "绝对恢复与假置信门 — line 71"
      - "绝对模拟门 — line 112"
      - "Absolute simulation and semi-synthetic recovery gate — line 214"
      - "零边假结构 / 错设假置信 — lines 224–225"
      - "recovery/FDR/coverage/假置信门 — line 293"
  - finding_id: LANG-R083-003
    severity: major
    finding_kind: terminology
    category: external-validation terminology
    dossier_locator:
      - "One-sentence summary (line 32)"
      - "Structured abstract: Approach and Expected result (lines 40–41)"
      - "Hospital-primary genuine cross-database validation (lines 228–240)"
      - "Evidence chain: planned cross-database validation (lines 306–312)"
    current_problem: >-
      同一外部验证设计交替使用“真正未触碰”“untouched final test”“test”“真正外部门”
      和“zero update”，但首次出现时没有区分数据集的隔离状态与模型不更新的分析方式。
      这些词控制主要贡献和成功判定，混用会让读者把“未用于开发的数据”与“在外部数据
      上不重新校准模型”误认为同一条件。
    target_state: >-
      对数据集统一使用“预先隔离的外部测试集”，并对主要分析统一使用“模型不更新的
      外部验证”；首次定义两者关系，随后分别稳定使用，不以 test、untouched 或
      zero-update 单独承载核心含义。
    required_change_or_replacement: >-
      在摘要首次出现处写明“在预先隔离、未参与模型选择或调参的外部测试集上，先开展
      不重新校准或更新模型的外部验证”。第 228–240 行保留该定义并分别引入短称
      “隔离外部测试集”和“模型不更新验证”；全文将表示同一对象或操作的中英混合形式
      统一为这两个短称。
    content_to_preserve: >-
      保留医院优先分区、适配区与测试区隔离、跨分区患者处理、测试结果揭盲限制、
      适配区仅校准和仅观测层更新、全模型重拟合不属于外部验证，以及有限更新不能替代
      模型不更新结果的全部条件。
    acceptance_test: >-
      首次定义后，读者能分别指出哪个短称描述数据来源隔离、哪个短称描述模型更新状态；
      对全文 relevant locators 做一致性检查，不再出现用 test、untouched、zero update、
      zero-update 或“真正外部”单独替代这两个定义的情况，且所有分区与更新层级不变。
    term_or_phrase: 真正未触碰的跨数据库检验
    recommended_form_or_plain_description: 预先隔离的外部测试集上的模型不更新验证
    evidence_basis: >-
      第 230–240 行直接区分了医院级数据隔离和 zero update、仅校准、仅观测层更新等
      分析层级；推荐表述逐项说出数据集状态与模型操作，适合并非都熟悉机器学习评估
      术语的既定跨学科读者。
    first_use_definition: >-
      “预先隔离的外部测试集是未参与变量、模型、阈值或更新层级选择的数据；模型不更新
      验证是在该测试集上不重新校准或更新任何模型参数的评价。”
    competing_forms_and_locators:
      - "真正未触碰的跨数据库检验 — line 32"
      - "未触碰数据库外测试 — line 39"
      - "最终测试区 / 零更新 — line 40"
      - "未触碰跨库结果 — line 41"
      - "真正外部门 — line 87"
      - "untouched final test — line 230"
      - "zero update / zero-update — lines 240, 309 and 355"
      - "test / final test — lines 230–240"
  - finding_id: LANG-R083-004
    severity: major
    finding_kind: terminology
    category: fallback endpoint definition
    dossier_locator:
      - "One-sentence summary (line 32)"
      - "Structured abstract: Expected result (line 41)"
      - "Automatic independent fallback (line 254)"
      - "Planned outputs (line 347)"
    current_problem: >-
      核心失败分支在首次出现时直接称为“death-ranked SOFA 临床状态再分析”，后文又出现
      “独立 SOFA 分支”“independent fallback”“death-ranked SOFA”和
      “trial-specific independent secondary clinical-state reanalysis”。这些形式没有在
      首次使用处明确死亡、住院存活和活着出院的排序关系，也没有稳定区分端点定义与
      分支动作。
    target_state: >-
      首次出现时用中文直接定义端点的分层顺序，并给出唯一短称“死亡优先分层 SOFA
      次要端点”；将“转入该端点的独立再分析”用于动作，将端点名称用于测量对象。
    required_change_or_replacement: >-
      第 32 行改为“若投影不满足标准，则改用独立于阶段 II 表征的次要端点：死亡置于
      最差层，访视时仍住院的存活者按 SOFA 从高到低排序，访视前活着出院者置于最有利层
      （下称‘死亡优先分层 SOFA 次要端点’）”。第 254 行保留完整操作定义；其余位置
      用该短称指端点，用“改用该独立端点进行再分析”指流程动作。
    content_to_preserve: >-
      保留死亡、访视时存活在院、访视前活着出院三个层级，SOFA 的不利方向，端点与
      阶段 II 表征独立，以及投影失败和试验语义失败触发不同后果的边界。
    acceptance_test: >-
      首次出现即能复述三类结局的完整顺序；全文检查所有 competing forms 后，每处都
      明确指向“端点”或“改用端点的动作”之一，不再保留未定义的 death-ranked、fallback
      或 trial-specific clinical-state 标签，且第 254、258–259 行的分析规则未改变。
    term_or_phrase: death-ranked SOFA 临床状态再分析
    recommended_form_or_plain_description: 死亡优先分层 SOFA 次要端点及其独立再分析
    evidence_basis: >-
      第 252、254 和 258–259 行已给出可直接陈述的排序规则；用该规则作为定义比保留
      未核验的中英混合标签更符合读者交接文件规定的跨学科知识基线。
    first_use_definition: >-
      “死亡优先分层 SOFA 次要端点将死亡置于最差层，将访视时仍住院的存活者按 SOFA
      从高到低排序，并将访视前活着出院者置于最有利层。”
    competing_forms_and_locators:
      - "death-ranked SOFA 临床状态再分析 — line 32"
      - "独立 death-ranked SOFA 次要再分析 — line 41"
      - "独立 SOFA 分支 — lines 125, 246 and 356"
      - "Automatic independent fallback — line 254"
      - "trial-specific independent secondary clinical-state reanalysis — line 254"
      - "death-ranked SOFA — lines 317 and 347"
  - finding_id: LANG-R083-005
    severity: major
    finding_kind: language
    category: readability and flow
    dossier_locator: "One-sentence complete-Idea summary (line 32)"
    current_problem: >-
      单句同时承载时间范围、两类数据来源、四段病程、模型属性、两项阶段 II 判定、
      三个阶段 III 前提、两个分支和五类禁止主张；多层“并”“仅在”“才”“则”使主干
      动词与条件后果相距过远，目标读者需要反复回读才能恢复研究主线。
    target_state: >-
      用三至四个连续句子依次说明阶段 I–II 的研究对象与数据、阶段 II 的验证方式、
      阶段 III 的启动条件与两种分支，以及所有分支共同的解释边界。
    required_change_or_replacement: >-
      将该条拆为三至四句：第一句止于候选动态系统表征；第二句只说明阶段 I–II 的模拟
      判定和外部验证；第三句说明阶段 III 的三个启动条件与投影通过/失败两种分支；
      最后一句集中陈述共同不支持的主张。拆句时采用 LANG-R083-001 至 004 的稳定术语。
    content_to_preserve: >-
      保留 24 个月、文献/专家先验、两个须审计的公共 ICU 数据库、发病前至结局的范围、
      知识约束和不确定性感知属性、阶段 I–II、EXIT-SEP D7、XBJ-SCAP D8、三个前提、
      投影与独立 SOFA 两分支，以及不支持因果网络、连续动力学、控制或数字孪生的限制。
    acceptance_test: >-
      修订后的每句只有一个主要交际任务；按顺序回答“研究什么、阶段 II 如何检验、
      阶段 III 何时及如何分支、不能解释什么”，且逐项核对 content_to_preserve 无遗漏，
      不新增科学条件或结果性措辞。
  - finding_id: LANG-R083-006
    severity: minor
    finding_kind: language
    category: mixed Chinese-English register
    dossier_locator:
      - "Positioning and contribution frame (line 34)"
      - "Current verified-resource versus prospective-gate status (lines 121–129)"
      - "Key techniques and implementation (lines 269–278)"
      - "Contribution and evidence ladder (lines 374–385)"
      - "Risk and automatic alternative matrix (lines 418–431)"
    current_problem: >-
      中文叙述中密集嵌入 benchmark/resource、project-local derivative、not generated、
      pass/fail、fallback、prediction-only、pooled effect、no-go、stress test 等普通英文
      流程词；这些词既非必须保留的数据库/试验专名，也未统一定义，削弱中文学术语体的
      连贯性，并对不同学科读者造成不必要的切换负担。
    target_state: >-
      数据库名、试验名、标准缩写、数学符号和确有必要的方法名可保留英文；普通流程、
      状态和后果使用一致的中文科学表达，首次保留必要英文短称时同时给出中文含义。
    required_change_or_replacement: >-
      在列出的五处逐项改写普通流程词，例如用“基准/资源”“项目内衍生材料”“尚未生成”
      “通过/未通过”“备用分析”“仅用于预测”“合并效应”“停止条件”和“压力测试”；
      对 adaptation、test、zero update、fallback 等核心词优先执行 LANG-R083-003 和 004，
      不改数据库、试验、统计量、变量符号或规范化缩写。
    content_to_preserve: >-
      保留 MIMIC-IV、eICU-CRD、EXIT-SEP、XBJ-SCAP、RCT、SOFA、SVD、FDR、ESS、
      MAR、MNAR 等专名或通行缩写及其技术含义，也保留所有状态类别和停止/降级后果。
    acceptance_test: >-
      对五个定位范围逐行检查：除 content_to_preserve 所列专名、通行缩写、代码变量和
      确需保留的方法名外，普通流程词均已改为中文或在首次出现时有中文释义；同一词在
      表格与正文中的译法一致，且没有改变任何数值、逻辑条件或证据状态。
unresolved_issues:
  - LANG-R083-001
  - LANG-R083-002
  - LANG-R083-003
  - LANG-R083-004
  - LANG-R083-005
  - LANG-R083-006
---

# Language Assessment Report

**Assessment ID**: language-assessment-r083  
**Target Language**: Chinese (zh-CN; technical English retained only where justified)  
**Discipline**: critical-care and clinical-epidemiology research with longitudinal statistics, system identification, and medical AI  
**Target Journal**: not specified  
**Scope**: complete Idea dossier, including all reader-facing prose, tables, and references; contract-fixed headings and field labels were treated as scaffolding  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

The dossier is grammatically controlled and scientifically cautious, but its central design is not yet consistently accessible to the stated multidisciplinary reader. Four core concepts are introduced through ambiguous modifier attachment or project-specific mixed-language shorthand, and the opening summary is too syntactically dense to serve its orientation function. These problems are repairable by targeted language revision rather than wholesale rewriting or professional editing.

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 7 | pass |
| Terminology Consistency | 3 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | No recurring clear grammatical error pattern; estimated below 1 clear error per 500 Chinese word-equivalents. |
| Academic register | pass | No section is dominantly conversational and no systematic informal register occurs in two or more sections. |
| Terminology coherence | fail | Four core reader-facing concepts are misleading at first use, inaccessible without project-internal vocabulary, or represented by multiple undeclared forms: the sparse-visit RCT descriptor, simulation decision criteria, isolated external validation, and the ranked SOFA fallback endpoint. |
| Tense systematic violation | pass | Prospective actions remain consistently prospective or modal; established evidence and current resource status are distinguished from planned work. |

---

## Strengths

- The dossier consistently distinguishes planned analyses from completed results, especially in the structured abstract, resource-status table, and remaining execution requirements.
- Causal, predictive, descriptive, and interventional claims are separated with disciplined modal language; the text does not drift into unsupported efficacy or mechanism claims.
- Numerical thresholds, time windows, dataset versions, and analysis branches are expressed precisely and remain stable across methods, evidence chains, and stop criteria.
- Abbreviations and proper names such as ICU, RCT, SOFA, MIMIC-IV, and eICU-CRD are used consistently; mathematical symbols are defined locally before detailed use.
- Lists and tables generally provide strong local parallelism, making technically dense sections easier to scan than the opening prose.

---

## Specific Issues

### Chinese Academic Clarity

- **LANG-R083-001 (major):** The title's modifier attachment makes the trial appear “sparse,” although the dossier means that trial visits or repeated measurements are sparse. The exact replacement and title-wide consistency test are in frontmatter.
- **LANG-R083-005 (major):** The complete-Idea summary contains the entire staged design, both branches, and all claim limits in one sentence. Its scientific content should be preserved while its communicative tasks are separated.
- **LANG-R083-006 (minor):** Several tables and prose sections switch repeatedly between Chinese and ordinary English workflow words. Proper names and standard abbreviations can remain, but ordinary process and status labels need a coherent Chinese register.

### Grammar & Syntax

No actionable grammatical error pattern was identified. The main sentence-level problem is structural overload rather than ungrammatical construction; it is recorded as LANG-R083-005.

### Academic Register & Tone

No colloquial or promotional hard-gate pattern was identified. LANG-R083-006 addresses the narrower issue of dense mixed-language operational wording in otherwise formal prose.

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LANG-R083-001 | 条件性稀疏 RCT 次要再分析 | title, lines 27 and 31 | “稀疏” appears to modify the trial rather than its visit data | yes |
| LANG-R083-002 | 绝对恢复/假置信门 | lines 32, 39, 66, 214–226 | multiple statistical objects and decisions are collapsed into a project metaphor | yes |
| LANG-R083-003 | 真正未触碰的跨数据库检验 | lines 32, 40–41, 228–240, 306–312 | dataset isolation and lack of model updating are not distinguished at first use | yes |
| LANG-R083-004 | death-ranked SOFA 临床状态再分析 | lines 32, 41, 254, 347 | the endpoint ordering and the action taken after projection failure are conflated | yes |

### Tense & Voice Conventions

No actionable tense or voice issue was identified. Prospective study actions use planned, conditional, or future-oriented wording, while prior evidence and current evidence status are expressed separately.

### Conciseness & Redundancy

LANG-R083-005 is the main concision priority: the summary stacks conditions and caveats instead of allocating them to successive sentences. Repeated scientific limitations were not treated as deletable merely because they recur in different reasoning locations.

### Readability & Flow

LANG-R083-005 is the blocking readability issue. The detailed methods are dense but locally navigable through tables and numbered structures; the opening summary is not, because its clause hierarchy is substantially harder to recover than the later design itself.

---

## Language Revision Priorities

1. **Terminology**: 4 issues — repair the title modifier and replace core project shorthand with first-use, function-specific scientific descriptions.
2. **Readability and flow**: 1 issue — split the complete-Idea summary into a short staged sequence while preserving every scientific condition.
3. **Mixed-language register**: 1 issue — translate ordinary workflow and status words consistently while retaining proper names, standard abbreviations, and notation.

---

## Re-Assessment Status (if applicable)

Not applicable. This is a fresh full-dossier Idea assessment; no prior issue list, score, decision, dossier version, or reviewer output was read.

---

## Assessment Notes

- The assessment covered the complete 480-line dossier and every field of the file-backed reader handoff.
- The language target was inferred as Chinese from `language: zh-CN`; English was assessed only where it appears inside the Chinese artifact. The multidisciplinary convention used biomedical/clinical defaults for evidence status and abbreviations, with computer-science/system-identification allowances for equations, symbols, and established method names.
- No target journal was supplied, so no journal-specific style was enforced.
- Contract-fixed research-idea.v3 headings, structured-abstract labels, evidence-chain labels, and schema fields were not scored, translated, renamed, or cited as findings.
- Focused terminology review was triggered only for core terms that were ambiguous, project-specific, mixed across forms, or inaccessible at the stated reader baseline. No full terminology inventory was created.
- This report makes no judgment about scientific validity, novelty, feasibility, impact, or argument quality and performs no source-text edits.
