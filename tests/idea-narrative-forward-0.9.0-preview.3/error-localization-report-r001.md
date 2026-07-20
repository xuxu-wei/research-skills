# Idea editorial repair 错误定位报告

- 报告版本：`r001`
- 开发目标版本：`0.10.0`
- 适用范围：旧版脓毒症 dossier v003 至 v057 的开发期回归，以及 `tests/脓毒症复杂系统模型` 新提示词 forward run
- 证据边界：解释两条 fixture 的实际运行轨迹；案例词语、具体疾病、数据源和阶段安排不作为跨领域规则

## 结论

反复出现“本轮修好、下一轮又发现新问题”的直接系统原因，是语言评估覆盖面和问题粒度在开发过程中持续变化，形成了移动的验收标准。原稿信息密度和模型偏好压缩命名是放大因素，但现有证据不能把主要失败归因于上下文过长。

Writer 并非普遍拒绝执行：绝大多数有明确动作、位置和验收测试的修订均被完成。不过，本例确认了两类 writer 失败：一次修订中产生新短标签，以及一次明确动作漏改；v051 又确认了一次确定性命令被自写窄检查替代并错误记录结果。后两类都属于执行与自证问题，不能仅凭长上下文解释。

后续 v055→v057 与新提示词 v005→v006 提供了更强的反证：canonical YAML brief 足够明确时，fresh writer 能在完整 dossier 上忠实执行全部纳入的 major action，pre-freeze checker 可在冻结前逐项确认；后续新发现的 major 主要来自上一位 assessor 的覆盖遗漏，而不是 writer 拒绝执行。旧例 writer 的允许输入约 185 KB，新例约 134 KB，两者都完成了纳入动作，因此“上下文过长”仍只是待配对实验检验的候选因素，不能作为本次主因。

因此，本轮保留 narrative assessor 与 language assessor 两个独立角色，只合并它们给 writer 的交接接口。Narrative 负责宏观论证和章节功能；language 负责科学角色称名、术语、修饰关系与局部可读性。两者合并会扩大单次审阅范围，并掩盖已经观察到的正交结果：同一 v050 可以通过 narrative 和内容保真，同时仍未通过 language。

## 修改轨迹

| 顺序 | 产物 | 观察 |
|---:|---|---|
| 1 | v003 上的多次旧语言评估 | 同一冻结文本曾得到 10、9、4 项问题，均要求 major revision；问题数量不等于严重度，但覆盖范围不稳定。 |
| 2 | `baseline-current/narrative-assessment-r079.md` | 稳定识别五段链、渐进披露、条件性后续分析挤占主线、限制重复和实现节功能问题。 |
| 3 | `baseline-current/language-assessment-r101.md` | 识别 4 项语言问题，并声称完成全文扫描。 |
| 4 | `baseline-current/editorial-repair-writer-brief-r102.yaml` | 将 5 项 narrative action 与 4 项 language action 规范化为一个可执行 brief；三源 coverage validator 通过。 |
| 5 | `direct-final-current-v16/idea-dossier-v050.md` | 宏观叙事得到显著改善；writer 初次产生 4 个新短标签，随后由同一 writer 修复。仍有一个 r101/r102 已明确要求替换的 reader-facing internal token 被遗漏。 |
| 6 | `direct-final-current-v16/content-preservation-r103.md` | 12 项保护内容全部通过；该结果只证明科学内容保真，不证明语言就绪。 |
| 7 | `baseline-current/language-assessment-r105.md` | 在四遍覆盖合同下重新审阅同一 v003，报告 9 项问题，显示 r101 有明显覆盖遗漏和 reviewer variance。 |
| 8 | `direct-final-current-v16/narrative-assessment-r104.md` | Fresh reviewer 判定 `narrative_ready`，证明宏观结构修复已闭合。 |
| 9 | `direct-final-current-v16/language-assessment-r104.md` | Fresh reviewer 对 v050 判定 `major_language_revision`，其中既包括旧动作漏执行，也包括先前评估未覆盖的科学角色命名和局部语言问题。 |
| 10 | `baseline-current/editorial-repair-writer-brief-r106.yaml` | 将 5 项 narrative 与 r105 的 9 项 language action 合并为一个 YAML brief，并要求同一 writer 在完整 dossier 上依次完成四个 bounded section passes。 |
| 11 | `direct-final-current-v17/idea-dossier-v051.md` | 确定性 dossier linter 返回 OK，无结构告警；正文未保留 fixture 中已知的 reader-facing internal tokens。 |
| 12 | `direct-final-current-v17/revision-delta-v003-to-v051.md` | Writer 起初未运行规定 diff，而以窄 regex 代替并错误记录“无候选”；独立复跑发现 10 个 advisory candidates。Writer 随后只修正 delta，逐项给出 4 个 `descriptive_not_label`、5 个 `standard_and_defined` 和 1 个 `fixed_scaffolding` 处置。 |
| 13 | `direct-final-current-v17/content-preservation-r107.md` | Fresh checker 判定 `scientific_content_preserved`；PCR-001 至 PCR-012 及五个 identity anchors 均通过。 |

## 后续轨迹与最终定位

| 顺序 | 产物 | 观察与归因 |
|---:|---|---|
| 14 | `direct-final-current-v21/idea-dossier-v055.md` 与 r126 readiness | Narrative 报告两项 major 与一项 minor；language 报告只给出 minor。r127 brief 只纳入两项 major，符合“minor 仅记录”的后续政策。 |
| 15 | `direct-final-current-v22/idea-dossier-v056.md` | Fresh writer 忠实完成 r127 两项 major；pre-freeze、64 项内容保护和五个 identity anchors 均通过。 |
| 16 | `direct-final-current-v22/narrative-assessment-r129.md` 与 `language-assessment-r129.md` | Narrative 已 `narrative_ready`，language 新发现两个 major：中央研究对象命名漂移、验证分层与模型更新标签混淆。它们不在 r126 报告内，故直接归因为 `assessor_coverage_failure / assessor_variance`，不是 v056 writer 漏执行 r127。 |
| 17 | `direct-final-current-v22/editorial-repair-writer-brief-r130.yaml` | 只纳入 ALA-001/002，明确排除 ALA-003–007 minor；覆盖 validator 通过，动作包含角色映射、全出现位置和实际文本验收。 |
| 18 | `direct-final-current-v23/idea-dossier-v057.md` 与 delta | 同一 fresh writer 在约 185 KB 允许输入上完成两项 major；独立 pre-freeze 核对 64/64、5/5、11/11，正文数值 token 和 38 个数学表达式序列不变。 |
| 19 | `direct-final-current-v23/content-preservation-r131.md` | Fresh preservation 判定 `scientific_content_preserved`；64 项保护内容、五个身份锚点和 11 个限制族全部通过。 |
| 20 | `direct-final-current-v23/narrative-assessment-r132.md` 与 `language-assessment-r132.md` | Fresh narrative 为 `narrative_ready`；fresh language 仅有两项 minor，四遍覆盖与四项 hard gate 通过。按当前政策不再修订。 |
| 21 | 新提示词 v004→v005 | Readiness 发现的是科学身份/任务定义冲突，正确返回 fresh methodology preflight；r005 随后 `pass`，说明叙事检查没有接管方法学。 |
| 22 | 新提示词 v005→v006 | r002 brief 只纳入两项 reader-blocking language major；fresh writer、pre-freeze 与 58 项内容保真均通过。v006 fresh narrative/language 只剩 minor，未再触发修订。 |
| 23 | 新提示词 v006 evaluator / journal route | Evaluator 的唯一项目输入为 v006，先冻结 4/3/4/4/4/4 与 `revise_then_promote`，再以官方 scope/article-type 匹配 Communications Medicine Article；独立 medical reviewer 未见 evaluator 报告或分数并确认候选。 |
| 24 | 新提示词 portfolio/state | 初版索引只登记 39/56，属于完整性阻断而非 minor；修正后 index、workflow state 和 round manifest 均登记 56/56，所有逻辑引用、路径和 `based_on` 可解析，仍保持 `revision_required`。 |
| 25 | 旧例 v057 一次性 blind evaluator | 唯一项目输入为 v057；冻结评分为 4/3/4/4/4/4，Clarity 从原稿的 2 提升到 4，Novelty、Feasibility、Impact 均未变化。决定为 `revise_then_promote` 而非 `promote`；纯编辑修订没有消除资源、容量或证据方面的实质问题，也不改变生产工作流的非晋级状态。期刊检索仅在科学评价冻结后进行。 |

## 失败归因

| 观察 | 归因 | 依据 |
|---|---|---|
| r101 与 r105 对同一 v003 的覆盖显著不同 | `assessor_coverage_failure` 与 `assessor_variance` | 后一轮拆出了前一轮未检查到的科学角色、入口负担和跨章节重复；文本没有变化。 |
| r102 对已有 findings 的动作是否足够明确 | 排除 `brief_normalization_failure` | 每项均有具体位置、操作、目标功能、保留内容和 acceptance test，且 validator 通过。 |
| v050 初次新增四个短标签 | `writer_regression` | 新表达不是源文本要求；同一 writer 在确定性比较指出后可修复。 |
| v050 仍保留 r101/r102 已明确点名的 internal token | `writer_execution_failure` | 明确动作存在，但正文仍有残留，delta 同时错误声称已清除。 |
| v051 delta 把规定 diff 替换成自写 regex | `writer_execution_failure` | Writer 明确认因是未运行指定命令，而不是读取结果错误；独立运行立即得到 10 个候选。 |
| v050 内容保真和 narrative 通过，但 language 未通过 | 不是 `workflow_contract_conflict` | 三个检查职责不同，结果可以同时成立。 |
| 长上下文是否导致漏改 | 尚不支持 `context_attention_failure` | 没有同一 writer、同一信息、仅改变 active context 的配对实验；单次漏改或事后指出问题后的成功修复不足以证明因果。 |

## 三层根因模型

### 宏观：工作流完成条件

旧流程把技术完整、证据边界和失败条件当作主要完成条件，没有在 evaluator 前要求完整 dossier 的叙事和语言就绪。开发期又不断增强评估合同，使每轮 writer 实际面对不同的验收标准。`0.10.0` 的修正是先稳定 readiness contract，再让 evaluator 只读最终冻结稿。

### 中观：评估与交接覆盖

旧语言报告容易按词项或宽泛主题合并问题，不能保证每个实际科学角色、首次定义、竞争称名和局部句法都被覆盖。Canonical YAML brief 对已经报告的问题通常足够清楚；主要信息损失发生在 assessor 报告形成之前。当前合同因此采用四遍覆盖、可读 fingerprint、action-level 字段和单一 writer brief。

### 微观：模型生成与自检习惯

Writer 倾向把复杂关系重新压缩为短标签、内部式命名或中英混合形式；assessor 也可能对 scanner candidate 作出抽样式判断。Writer 自己在 delta 中声明“已通过”不是验证证据。确定性命令必须按原命令运行，随后仍需 fresh assessor 作语义判断。

## Language report 与 writer brief 的充分性

现行 language finding 对 actionable problem 必须给出：精确 locator、`meso`/`micro` 层级、科学角色、问题机制、目标状态、具体替换或定义、保留内容、证据依据和 acceptance test。非标准、误导或未核实术语必须给出可理解的标准表达或直接描述，不能只写“优化术语”。

Orchestrator 不把两份 reviewer 报告直接交给 writer，而是生成一个 YAML brief，逐项保留来源 finding、处理位置、操作、内容保全和完成测试，并消解 narrative 与 language 的重叠。Brief validator 只能证明接口完整；writer 是否执行仍由 action-level delta、确定性检查和 fresh reassessment 共同判断。

## 是否应合并两个 assessor

不合并。合并的工作负担和指令冲突风险高于收益，且 v050 已提供职责正交的运行证据。保留以下边界：

- narrative assessor：五段逻辑、章节功能、顺序、渐进披露、限制权威位置、重复和读者回读负担；
- academic language assessor：科学角色称名、标准或直接术语、首次定义、中英文一致性、修饰关系、局部语法和可读性；
- writer：只执行一个已经消解重叠的 YAML brief；
- evaluator：只读 fresh readiness 通过后的当前 dossier，不读取上述报告或 delta。

## Context attention 的确认实验

只有以下配对实验全部满足时，才记录 `context_attention_failure`：

1. 冻结同一 source dossier、canonical brief、protected register、模型设置和输出预算。
2. 预先登记 action-level compliance matrix，不能在看到失败后改变问题定义。
3. Full-context 条件一次呈现完整允许材料。
4. Bounded 条件仅改变材料呈现：同一 writer 依次获得当前章节、对应 actions 和必要 PCR slice；不得增加答案或改写 acceptance test。
5. 两个条件都由同一 writer 写同一个完整 dossier，不用多 writer 拼接章节。
6. 由不知道实验条件的 fresh checker 核对动作、内容保真和新回归。
7. 只有 full-context 稳定漏掉明确动作、bounded 条件在没有新增信息时完成，且已排除输入遗漏、评估覆盖、brief 歧义、合同冲突、输出截断和一般 writer regression，才支持该归因。
8. 单次 rescue 仅为支持性证据；因果结论需要多个 fresh writers 的随机分配复现。

## 已落实的防复发措施

- 在 evaluator 前加入 dossier narrative 与完整 language readiness。
- Language assessment 固定四遍覆盖，并要求读者可见的 mixed-language/internal-token scanner candidates 接受语义判断。
- Scanner 使用结构信号，不把本例词表写入通用规则。
- Narrative 和 language findings 合并为一个 YAML writer brief；writer 不读取 reviewer 历史。
- 同一 writer 在同一个完整 dossier 上按章节进行 bounded passes；不持久化章节碎片。
- 指定的确定性命令不得用自写近似检查替代。
- Short-form diff 在生产流程中是 advisory；候选必须处置，但存在候选不等于失败。
- 科学内容由 protected-content register 和 fresh preservation 独立核对。
- Fresh narrative/language reassessment 只读新 dossier；evaluator 仅在 readiness 通过后只读该 dossier。
- 失败归因仅在 fresh reassessment 仍阻塞或显式诊断时记录；不为普通成功路径增加额外产物。

## 验收闭合状态

- v057 的 fresh narrative reassessment 为 `narrative_ready`，fresh language reassessment 无 critical/major，内容保真为 `scientific_content_preserved`。
- 一次性双版本盲评的 `files_read` 分别只含 v003 或 v057 并绑定准确逻辑引用；v057 的期刊检索发生在评价冻结之后。Clarity 从 2 提升到 4，Novelty、Feasibility、Impact 保持不变，且没有直接 `promote`。
- 新提示词案例的 biomedical journal candidate brief 不含分数或 findings，并由 fresh `medical-journal-review` 在看不到 evaluator 报告的条件下独立复核。
- 新提示词输入从 context、evidence、dossier 到 readiness、evaluation、journal review 和 portfolio 完成了不泄漏旧 fixture 答案的 forward run；index、state 和 manifest 均覆盖 56/56 文件。
- `scripts/test_openai_idea_narrative_forward.py` 已对上述直接验收条件完成确定性复核；低影响 minor 的数量或具体措辞不作为门禁。

## 低影响观察登记

本节是 Idea 工作流开发期唯一的低影响问题登记位置。下列事项均未造成科学内容漂移、readiness 或 evaluator 决定改变，也没有形成大范围污染；因此只记录，不为其启动新的修订、复现或专项测试。修复优先级由插件所有者统一决定。

| 插件版本 | 问题现象 | 推测诊断 | 拟议的解决方案 | 处置 |
|---|---|---|---|---|
| `0.10.0-dev`（旧例产物标记为 `0.9.0-preview.3`） | v055 的 `narrative-assessment-r126.md` 留有 1 项 minor 摘要负担，`language-assessment-r126.md` 留有 6 项 minor；这些项目未进入 r127 writer brief。 | 这些是局部可读性与命名精炼问题，不影响两项 major 修复、科学含义或进入下一次 fresh readiness 的资格。 | 若所有者以后统一处理 minor，可按原 locator 做一次集中微编辑；当前不修改、不复现、不增加测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev`（旧例产物标记为 `0.9.0-preview.3`） | v056 的 `language-assessment-r129.md` 报告 ALA-003 至 ALA-007 共 5 项 minor；r130 brief 明确排除。 | Fresh assessor 在已完成的核心对象与验证命名之外发现局部概念簇和句法负担；不影响 ALA-001/002 两项 major 的必要性与执行边界。 | 保留报告中的 locator 与建议，当前只执行 ALA-001/002；不得把 minor 偷渡进 major 修订。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev` | 旧例最终 v057 的 `language-assessment-r132.md` 仅报告 LANG-001/002 两项 minor：模型排除后果仍混用“晋级/准入”等管理隐喻，Primary research question 的动作与限定仍较密；blind evaluator 独立报告的唯一 minor 也落在后一问题。Narrative 已为 `narrative_ready`，四项 language hard gate 均通过。 | 两项均为非阻断的术语语域和单句负担问题；不改变中央研究对象、验证分层、科学含义、readiness 资格或 evaluator 输入。 | 由所有者以后决定是否集中微编辑；当前保留 v057、不生成新 brief、不修、不复现、不加测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev` | 新测试例 v005 的 `narrative-assessment-r006.md` 有 2 项 minor，`language-assessment-r006.md` 有 8 项 minor；r002 writer brief 只纳入 2 项 major。 | Minor 与当轮两个 reader-blocking 核心命名问题可分离，纳入同一轮会扩大编辑面并增加内容漂移风险。 | 保持原报告可见；当前不修、不复现、不增加专项测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev` | 新测试例 v006 的 `narrative-assessment-r007.md` 有 4 项 minor，`language-assessment-r007.md` 有 8 项 minor，但无 critical/major。 | 主叙事链和核心术语已达到 evaluator 输入资格；剩余问题是局部定义顺序、限定语堆叠和符号首用等非阻断编辑事项。 | 将 v006 作为当前 evaluator 输入；所有者若以后决定统一精修，再从两份报告生成单一 bounded brief。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev` | 内容保真 validator 从仓库根目录调用时不能解析以 workflow root 为基准的相对路径；从该测试 workflow 根目录调用可以通过。 | CLI 的路径基准与产物逻辑路径基准未在调用层显式区分；未影响 validator 结果或产物。 | 未来如需提升易用性，可在命令用法中明确工作目录或增加显式 `--workflow-root`；当前不修改、不复现、不加测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev` | 新例 evaluator 在污染防护合同生效后仍有一次误点到 copyright/licensing 页面并主动作废实例；没有写出最终评价产物。 | 外部页面导航存在偶发重定向或错误链接选择，现有隔离与来源污染防护已正确阻止结果被使用。 | 可在以后考虑先校验页面类型或优先使用稳定的官方直达链接；当前只换用 fresh evaluator 完成既定流程，不修插件、不复现、不加测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev` | 新例最终 `evaluation-r008.md` 的 `instructions_read` 未列出后置读取的 `journal-matching-contract.md`，但其期刊载荷字段、官方来源类型和冻结顺序均符合该合同。 | Reviewer 在冻结科学评价后补读合同并完成匹配，却没有同步补全非项目输入的指令回执；不影响 `files_read` 隔离、评分、候选语义或结果。 | 如所有者以后统一强化回执，可要求写报告前重新生成 `instructions_read`；当前不修改报告、不复现、不加测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev` | 物化后的 `candidate-journal-match-r008.yaml` 未包含模板示例中的 `source_skill` 与 `unresolved_issues`；它已包含语义相同且更具体的 `matching_source_skill`、`materialized_by_skill`，并保留完整无评分候选载荷。 | Nested payload 的精确物化规则只允许添加六项元数据，而模板示例与 payload 字段集存在轻微回执差异；未影响来源、隔离、候选内容、medical review 或索引归属。 | 由所有者以后决定统一 schema 字段还是澄清模板；当前不修改已冻结 brief、不复现、不加测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev` | 新例 portfolio assembler 已写齐八个标准产物，但在耗时的最终自检返回前被主流程中断；没有留下独立自检回执。 | 生成任务把索引枚举与重复语义核对放在同一长回合，返回延迟；所有文件已落盘，后续仍由既定 forward/plugin 验证覆盖。 | 若所有者以后优化执行体验，可将生成与确定性索引校验拆成两个有时限的内部步骤；当前不重跑该 assembler、不为此增加测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev` | 开发测试中两次 fresh preservation 子线程创建请求因 agent thread limit 被拒；释放已完成协调线程后，主 agent 能正常创建 fresh reviewer。 | 这是测试编排并发槽位与已累积子线程生命周期的交互，不是 Skill 科学或编辑合同失败，也未造成隔离降级。 | 后续开发可按阶段主动结束已完成协调线程，再启动下一组 fresh reviewers；当前不改插件、不复现、不加测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0+codex.local-20260720-095426-751580` | Local 安装时，当前 Conda 环境中的 `requests` 报告 `urllib3` 与 `chardet`/`charset_normalizer` 版本兼容性警告；安装和随后 Local 内容一致性验证均以退出码 0 完成。 | 警告来自用于运行安装脚本的全局 Python 依赖组合，不是插件包内容、Skill 加载或 Local/Git 通道隔离失败。 | 所有者若以后整理开发环境，可在独立 `.venv` 中按 `requirements-dev.txt` 安装兼容依赖；当前不调整全局环境、不复现、不增加专项测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0+codex.local-20260720-095426-751580` | Fresh、只读 Codex 发现烟测成功识别 `idea-narrative-assessor` 和两个规定产物，但启动日志提示含 `..` 的图标路径被忽略、PowerShell 暂不支持 shell snapshot，退出后遥测事件发送失败；实例第一次手工读取中文 `AGENTS.md` 时未指定 UTF-8，终端回显为乱码，后续显式 UTF-8 读取正常。 | 当前插件源码及 Local 副本未检出 icon 字段；前三项更可能来自共同加载的其他插件元数据或 Codex 运行时能力/网络。乱码来自 Windows PowerShell 默认解码而非文件损坏。它们未影响版本识别、Skill 发现、只读执行或退出码。 | 所有者以后可在需要时单独审计全局插件图标元数据、Codex 的 PowerShell snapshot 支持和遥测网络；Windows 诊断命令显式使用 UTF-8。当前不修改本插件、不复现、不增加专项测试。 | `record_only_owner_prioritization_pending` |
| `0.10.0-dev` | 暂存后的 whitespace 检查在若干开发期测试报告中识别出 Markdown 双空格硬换行和少量文件尾空行；插件源码、脚本和机器合同的直接检查未因此失败。 | 这些空格主要来自 Markdown 人工换行和 fresh-agent 报告格式，未改变 YAML/Markdown 解析、科学内容、索引或验收结论；批量清理反而会扩大历史证据差异。 | 所有者以后若决定统一测试语料格式，可在独立维护批次中机械规范化；当前保留原始测试证据，不修、不复现、不增加专项测试。 | `record_only_owner_prioritization_pending` |
