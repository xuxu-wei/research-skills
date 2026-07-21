# Research Skills OpenAI 路线图

## 文档元数据

| 字段 | 当前值 |
|---|---|
| 文档状态 | Personal Experimental/Preview |
| 规划基线 | 2026-07-21 |
| 当前插件版本 | `0.12.0` |
| 当前范围 | 51 个 Skill、22 个独立 Reviewer、5 个完整工作流 |
| 发现面 | 7 个声明入口、6 个隐式入口、1 个 explicit-only 入口 |
| 当前路线图状态 | Phase 0–9 均已完成；已完成 Phase 只作为历史记录，不自动复验 |

## 产品定位

`research-skills-openai` 是供单一所有者在 ChatGPT Work 和 Codex 中使用的研究工作流插件。当前路线只优化个人使用的可靠性、可复现产物、独立评估、清晰血缘和人工决策，不承诺生产支持、团队分发或自动外部提交。

本文件同时用于记录过去已经完成的工作、说明当前版本状态和规划未来事项。标记为“已完成”的 Phase 是历史记录，不是后续版本的重复执行清单；除非所有者明确重开，否则不得再次运行。后续版本可能使其中原有步骤或验收口径不再适用，当前开发只验证正在进行的事项和本次变更直接影响的合同。

所有完整工作流都必须保持角色分离：Generator 和 Drafter 不自评，Reviewer 针对冻结的只读输入在新实例中运行，Assembler 不静默修复源产物。实质性修订必须生成新版本并接受新的独立评估；Fatal 或未解决的 Blocking finding 会阻止晋级。

## 当前状态

- 当前源码为 `0.12.0`，包含 51 个 Skill、22 个独立 Reviewer 和 76 条工作流边。
- 五个完整工作流为 Idea、Proposal、Article、Perspective 和 Research Polisher。
- 七个声明入口中，六个允许隐式调用；Research Polisher 永久保持 explicit-only。
- 旧版确定性回放和匿名语料结论保留在各自已完成 Phase 中；它们不是 `0.12.0` 的重复执行清单。
- GitHub Marketplace 安装、缓存发现和路由机制已经诊断；所有者接受其作为当前个人使用基线，但不将此表述扩展为严格全量工作流已验证。
- Phase 7 和 Phase 8 已关闭；完整 Search/Deep Research 原生闭环仅在所有者明确要求时复验。
- `0.10.0` 的四条原始测试基线已经先于源码改动冻结；`0.11.0` 只运行本次改造直接需要的静态、单元、fixture 和 fresh-agent forward tests。

## 阶段总览

| Phase | 名称 | 状态 | 当前结论 |
|---:|---|---|---|
| 0 | 引用与 Registry 闭合 | 已完成 | 依赖、入口和 Registry 一致 |
| 1 | Context 精简 | 已完成 | 发现描述和默认上下文受控 |
| 2 | Search 与 Deep Research 路由 | 已完成 | 原生检索路由和停止条件已定义 |
| 3 | 工作流状态机闭合 | 已完成 | 五个工作流具备独立评估闭环 |
| 4 | 场景评估与持续验证 | 已完成 | 5/5 工作流和 63 个负向守卫通过 |
| 5 | GitHub Marketplace 安装与更新 | 已完成 | 安装机制有效，当前版本已获所有者接受 |
| 6 | 维护性与当前版本强化 | 已完成 | Artifact、DOCX、README、Cover Letter 和 Idea v3 完成 |
| 7 | 个人安装与工作流就绪 | 已完成 | 所有者确认安装、发现和当前工作流可顺利运行 |
| 8 | 个人原生研究闭环 | 已完成 | 当前能力已获所有者接受；完整原生闭环转为按需复验 |
| 9 | 跨工作流人类可读性 | 已完成 | 共享叙事评估、语言/术语边界、writer repair、内容保真和 evaluator 隔离完成当前分支验收 |

## Phase 0：引用与 Registry 闭合

- 状态：`已完成`
- 优先级：`历史基线`
- 目标：关闭插件内引用、资源、入口和工作流边的结构性缺口。

### 已完成

- Markdown、Reference、Template、Script 和跨 Skill 引用均可解析。
- Orchestrator 到 Reviewer 的边均要求委派执行。
- Registry、Manifest 和 Skill 库存保持一致。

### 待完成

- 无。

### 完成条件

- 插件审计不报告悬空引用、缺失资源或未声明入口。

## Phase 1：Context 精简

- 状态：`已完成`
- 优先级：`历史基线`
- 目标：降低发现和默认加载成本，同时保留工作流门禁。

### 已完成

- 超长流程被压缩或移入条件引用。
- 入口描述和 Orchestrator Context 保持在维护预算内。
- Reviewer 隔离、状态转换和 Artifact Schema 未因精简而削弱。

### 待完成

- 无；已有超限文件作为维护性技术债，在后续触及时继续缩减。

### 完成条件

- Context 测量不超过当前回归阈值，且插件审计无新增超限错误。

## Phase 2：Search 与 Deep Research 路由

- 状态：`已完成`
- 优先级：`历史基线`
- 目标：建立内置 Search、Deep Research 和学术精读之间的明确分工。

### 已完成

- 快速、近期、精确和窄范围检索默认使用内置 Search。
- 多阶段、多方向或多来源综合使用 Deep Research。
- Deep Research 不可用时返回自包含 handoff，并停在 `deep_research_handoff_required`。
- `academic-deep-search` 仅处理适合精读 2–5 篇论文的具体问题；广泛问题交给 `research-opportunity-mapper`。

### 待完成

- 无源码工作；真实 Search 和 Deep Research 运行观察仅在所有者要求时按 Phase 8 可选复验清单执行。

### 完成条件

- 路由、停止状态、Artifact 绑定和单边恢复契约通过确定性测试。

## Phase 3：工作流状态机闭合

- 状态：`已完成`
- 优先级：`历史基线`
- 目标：使完整工作流从输入规范化闭合到人工审阅包。

### 已完成

- Idea、Proposal、Article、Perspective 和 Research Polisher 均具备生成、独立评估、修订、复评和人工交付路径。
- Assembler 保留未解决 Finding 和异议，不静默修复源内容。
- Reviewer 不可用时停在 `independent_review_pending`，不退化为内联自评。

### 待完成

- 无；当前工作流运行能力已经由所有者接受，严格运行档案保留为可选复验。

### 完成条件

- 每个工作流都具备正常人工交付状态、Fatal 停止状态和 Reviewer 不可用停止状态。

## Phase 4：场景评估与持续验证

- 状态：`已完成`
- 优先级：`历史基线`
- 目标：用确定性场景覆盖正常路径和关键失败路径。

### 已完成

- 五个工作流的端到端确定性场景全部通过。
- 63 个负向守卫覆盖绕过门禁、陈旧输入、无效血缘、缺失 Reviewer、Assembler 越权和 false-ready。
- 每个实质性新版本都必须绑定新的 Reviewer 实例后才能晋级。

### 待完成

- 无；场景与 Skill 契约变更时同步更新。

### 完成条件

- Phase 4 报告保持 5/5 工作流通过、63 个负向守卫通过。

## Phase 5：GitHub Marketplace 安装与更新

- 状态：`已完成`
- 优先级：`历史基线`
- 目标：建立个人 Preview 的 Marketplace 安装、更新和本地开发流程。

### 已完成

- Manifest 与 Registry 使用同步 SemVer。
- GitHub `main`、Marketplace `git-subdir`、更新/重装命令和 Local/Git 互斥调试流程已经实现；cachebuster 仅写入本地安装副本。
- 历史安装已证明 Marketplace 注册、升级和新任务发现机制可工作。

### 待完成

- 无；安装缓存与新任务发现已经诊断并由所有者接受。正式 owner-observed 绑定仅在按需严格复验时记录。

### 完成条件

- 安装机制、SemVer 规则和插件包验证持续通过。

## Phase 6：维护性与当前版本强化

- 状态：`已完成`
- 优先级：`P0 已关闭`
- 目标：提高 Artifact 完整性、交付可用性、验证器可移植性和 Idea 工作流质量。

### 已完成

- 验证器自动推导版本和库存，并拒绝无效版本转换。
- Proposal、SAP 和 Article 的新评估只读取当前冻结产物；旧版本、Delta、分数和决策保持隔离。
- Article 以完整 Markdown 为审计源，DOCX 为优先交付格式，并支持原生表格、Figure、Parity 和 Render QA。
- 五个完整工作流维护项目根 README；Article 和 Perspective 支持版本化 Cover Letter。
- Idea 使用 `research-idea.v3` 完整 Dossier、可读 Reference Ledger、闭合 evidence chain 和自适应方向路由。
- 当前版本保持 50 个 Skill、21 个 Reviewer、7 个声明入口、6 个隐式入口和 17 个 entry mode。
- Idea 在科学/方法修订后运行独立 narrative 与完整 dossier language readiness；orchestrator 将两路 included actions 消解为单一 writer brief，writer 不读取两份报告或 assessor plan。必要的 editorial repair 经过该 brief、protected-content register、内容保真核验和 fresh reassessment 后，才允许 dossier-only evaluator 读取当前稿。
- Idea evaluator 在冻结评分与决定后依据官方 scope 匹配具体期刊；最终生物医学/临床 Idea 随后由独立 `medical-journal-review` 复核候选，且该 reviewer 不接收 evaluator 分数或 findings。
- Editorial repair 失败归因区分 assessor coverage、brief normalization、writer execution/regression 与经配对实验确认的 context attention；普通成功路径不强制生成额外诊断产物。

### 待完成

- 无；这些能力的当前版本已经纳入所有者接受的个人使用基线。

### 完成条件

- Artifact completeness、Article DOCX、Context、Phase 4、Phase 7 和 Phase 8 确定性测试全部通过。

## Phase 7：个人安装与工作流就绪

- 状态：`已完成`
- 优先级：`P0 已关闭`
- 目标：证明当前版本在所有者 Codex 环境中能够安装、发现并完成五个工作流的受控人工交付。

### 已完成

- 17 个 entry mode 的确定性回放全部通过，入口绕过和陈旧输入守卫有效。
- 五个工作流的状态、角色隔离、版本血缘和停止条件已经实现。
- Research Polisher 已实现为第五个工作流和第七个声明入口，并永久保持 explicit-only。
- Research Polisher 冻结研究 Dossier，由科学意义、实际价值和传播定位三个互盲角色分别提出 `reposition_only`、`small_extension` 和 `moderate_extension` 策略，再由独立方法学/可发表性 Reviewer 评估，最终停在人工策略选择。
- 所有者确认当前安装、发现和路由机制满足个人使用基线；这不声称五个工作流均已完成严格 owner-observed 全量验证。

### 可选复验

- 无活动任务。仅在所有者明确要求严格复验时，重新执行 distribution、五个 happy path 和两个控制槽位并写入私人 receipt。
- 严格复验仍须覆盖 `personal-research-polisher-happy` 的显式正向调用，并确认其不接管语言润色、普通写作、新 Idea 或一般文献检索。

### 完成条件

- 当前版本保持确定性验证通过，且所有者确认安装、发现和工作流可满足个人研究使用。
- 若所有者重新要求严格复验，Accepted run 仍必须绑定任务、源码身份、Artifact、版本、Digest、Reviewer 实例、时间戳、结果和所有者确认，false-ready 必须为 0。

## Phase 8：个人原生研究闭环

- 状态：`已完成`
- 优先级：`按需复验`
- 目标：证明当前版本能够正确使用内置 Search，并完成 Deep Research 的停止与返回闭环。

### 已完成

- 20-case 匿名语料覆盖五个工作流的 happy、fixable、fatal/pending 和 no-gain 结果。
- Fatal/Blocking 检出、Major finding 检出、血缘、Reviewer 隔离、写入边界和异议保留均为 100%，false-ready 为 0。
- 三个风险分层的合成 repeat case 保持独立 Reviewer 和一致结果。
- 所有者接受当前 Search/Deep Research 路由能力作为个人使用默认基线；严格原生闭环仍明确标记为未全量验证、仅按需复验。

### 可选复验

- 无活动任务。不得自动恢复既有 Phase 8 task 或 pending edge。
- 仅在所有者明确要求时，可选复验 `personal-search-current`、`personal-search-exact`、`personal-search-narrow-academic`、`personal-deep-research-inactive` 和 `personal-deep-research-complete`。

### 完成条件

- 路线图完成以确定性基线和所有者对个人运行能力的接受为准；不声称三个 Search 和两个 Deep Research 槽位已经完成严格 owner-observed 全量验证。
- 若按需重开严格复验，Search 的 Material claim 必须绑定已打开的权威来源，Deep Research return 与恢复必须绑定同一 Evidence Artifact 和 Digest。

## Phase 9：跨工作流人类可读性

- 状态：`已完成`
- 优先级：`P0 已关闭`
- 目标：在不削弱科学审计、内容保真和独立评估的前提下，让 Idea、Proposal、Perspective 和 Article 的最终交付对象先形成读者可理解的论证，再进入最终评价。

### 已完成

- 四条 `0.10.0` 原始测试基线在源码修改前冻结；公共叙事角色、语言/术语边界、三条写作工作流适配、内容保真和 evaluator 隔离合同均进入 `0.11.0`。
- Idea 与 Proposal 的 current fixtures 在证据边界生成 reader-aware continuation 并真实停止；Article 完整发现给定材料、应用所有者指定的单一语义权威，并在独立方法审核处停止，均未越权生成下游文稿或评价。
- Perspective 当前测试先关闭 input-builder 和 argument-architect 的无产物缺陷，再由一个 writer 完成科学版本链。renewed panel 在科学问题尚未关闭时真实停止；另一个 fresh writer 在无 follow-up、无 replacement 条件下用早期双文件检查点和逐 section 写入完成稿件，并通过 8/8 conformance。
- 当前静态验证为 51 个 Skill、22 个独立 Reviewer、72 条工作流边、Registry schema v6，全部 32 个新增或修改 Skill 通过 `quick_validate.py`；插件级审计为 0 error、0 warning。
- Local 开发通道通过安装、版本核验和 fresh-task 发现；原始 `tests/test-*` fixtures 保持 74/74 文件且内容变更为 0。生成运行目录不作为 release 资产。

### 当前设计

- 新增一个公共 `research-narrative-assessor`，负责宏观论证链、章节功能、渐进披露、重复、正向主张与必要限定的平衡，以及标题—摘要—问题—贡献的一致性。原 `idea-narrative-assessor` 仅保留兼容，不再是生产 Idea 路由。
- `academic-language-assessor` 保持独立角色，负责句段语言、读者可理解的术语选择、中英文漂移、不自然隐喻和内部工作语言泄漏。只有核心术语不确定、误导或目标读者难以理解时才做聚焦核验；不新增术语 Skill、状态或常规术语表。
- 两个 Reviewer 对同一冻结稿并行运行。Orchestrator 将两路 finding 去重、消解冲突并规范化为一个 YAML writer brief；writer 不读取原始报告。
- 每份文稿只设一个完整 limitation 权威位置，其他位置不提及，也不使用“见限制部分”式指针；仅当 limitation 本身推进当前推理且省略会造成歪曲时才例外出现。
- Editorial repair 前冻结 protected-content register；修订后由 fresh preservation reviewer 核验。只有 `scientific_content_preserved` 可进入 fresh narrative/language reassessment 和 final evaluator。
- Final evaluator 只读取最终当前稿或合同定义的读者 bundle、稳定 rubric 与最小必要事实/期刊约束；不读取旧稿、计划、科学审计、readiness 报告、repair brief、protected register、delta 或 prior evaluation。
- 新产物使用可读的 artifact ID、版本、准确路径、冻结状态、完整索引和唯一当前指针；不把 SHA/Digest 写入 LLM-facing 合同。旧 Digest 字段可读取但忽略。
- Proposal 在 prose 前由 fresh planner 产出完整 section-content plan，再交给不同 writer 实例。Perspective 复用已有 argument architect 和 paragraph map。Article 先发现全部给定材料，明确一个语义权威并保留与其兼容的支持材料，再形成完整 section-content blueprint。
- 无法立即确认但可在一个具体、有界且可证伪假设下通过的方法学意见，writer 按该已通过假设继续，并仅在合同指定的 Assumptions 权威位置记录一次研究推进风险。不能被有界化或可能改变主要结论的问题不得条件通过。
- Writer 可由同一实例按章节做有界 pass，但始终保有完整源文档并交付一个完整新版本；不得拆给多个片段 writer。只有排除输入、assessor 和 brief 问题后，同一 writer 出现“完整上下文漏执行而有界视图成功”的配对结果，才归因为 context attention。

### 验收标准

#### 共用

- 51 个 Skill、22 个独立 Reviewer、Manifest/Registry `0.11.0` 和 Registry schema v6 一致；每个新增或修改 Skill 均通过 `quick_validate.py`。
- Forward-test 验收按实际可达分支判断：若原始 fixture 在证据、readiness、方法学或独立评审边界正确暂停，完整 continuation/state/index、准确的停止理由以及没有越权生成下游产物即为该 fixture 的通过条件；不得为覆盖 writer、evaluator 或 DOCX 分支而虚构证据或放宽科学门槛。未到达分支的合同由当前静态/unit/fixture tests 与既有已完成证据覆盖，不因此重跑已关闭 Phase。
- 简单单方法研究可用简短内容完成各自论证功能；没有问题时直接 ready；没有核心术语疑问时不做术语核验，也不强制长术语表或复杂 repair plan。
- 每个 major narrative/language finding 均映射到 YAML writer brief 中一个可定位、可执行、有验收测试的 action；fresh writer 无需猜测位置、目标功能、替换术语、保留内容或完成标准。
- Writer action conformance、内容保真、fresh readiness 和 final evaluator `files_read` 隔离均通过；只改善表达不得单独升级 novelty、feasibility、impact 或 scientific strength。
- 轻微、局部、未影响科学内容、readiness、决定或广泛输出的问题只写入 `tests/readability-workflow-test-report.md`，不另起修复或复现循环。

#### Idea

- 既有问题稿能识别缺失的意义链、由防御性限定取代科学 gap、术语前置、内部工作语言泄漏和跨章节 limitation 重复，并生成可独立执行的 YAML repair plan。
- 一轮集中修订关闭全部 major finding，protected content 不漂移，最终 fresh evaluator 只读取当前完整 dossier。

#### Proposal

- Context 明确目标评审者知识基线、source intent、binding constraints、gap type 和读者推理 handoff；新写 proposal 在 prose 前存在完整且冻结的 section-content plan，并由另一 writer 实例执行。
- Significance、现状、未解决问题、项目 rationale、aims 和 approach 连续；评审防御不得抢占立项主线。Assumptions、feasibility 和 risks 使用合同指定的权威位置。
- Editorial repair 经单一 YAML brief、action conformance、内容保真和 fresh reassessment；最终 evaluator 只读最终 proposal 与最小 call/factual inputs。

#### Perspective

- Argument architecture 和 paragraph map 明确目标读者、主张推进、反方观点落点、每段功能和 handoff；证据保留与叙述结构不互相替代。
- 每一类 distinct counterargument/boundary 只有一个推进论证的权威位置；不得把 caveat 清单或审计语言当作文章主线。
- 进入 editorial 分支时，readiness、内容保真和 evaluator 隔离必须通过；可选目标读者/期刊模拟只输出 observations，不与 narrative/language reviewer 重复评分。当前 fixture 在 renewed scientific panel 停止，因此验收的是完整停止血缘、保留异议以及不存在 editorial/final/journal 产物。

#### Article

- 入口对所有给定文件建立完整 material inventory；文件名或版本白名单不能隐藏用户已提供的可追溯技术报告、结果或显示材料。一个来源被指定为语义权威时，与其兼容的其他材料仍参与写作和核验。
- 只有 readiness 和方法学审核允许科学撰写时，Introduction 才完成 background→current state→gap→significance→rationale/objective；Methods 依设计逻辑组织；Results 先报告 primary answer；Discussion 先回答研究问题再解释意义。
- 进入撰写分支时，标题、摘要、key points 与完整 manuscript 在 final readiness 前共同冻结并检查；最终 evaluator 只读取该 reader bundle，不读取 blueprint、audit、repair 或 prior evaluation。
- 进入交付分支时，DOCX 与 canonical Markdown 语义一致，表格为原生 Word 表格、图像可用且全文逐页 render QA 通过。若方法审核要求澄清、重分析或停止，则验收没有 manuscript、evaluator、journal 或 DOCX 产物，并提供可执行的恢复路径；不得用示例正文伪造 DOCX 验收。
- 当前保密 Article fixture 以所有者指定的单一 SAP 文件为语义权威；其他位置的 SAP 版本标记均不参与语义裁决。准确文件名只保留在不发布的测试输入和运行记录中，该规则不得写入通用 Skill 合同。

### 开发环境与测试顺序

1. 暂时禁用 Git 安装通道，只启用 Local 插件。
2. 每次 Skill 修改后运行 `python scripts/openai_plugin_dev.py install-local` 和 `verify --channel local --expected-version 0.11.0`，然后新建 Codex task；已有 task 不热加载 Skill。
3. 原始 fixtures 始终只读。基线输出位于 `tests/0.10.0-{workflow}/`，当前测试输出位于 `tests/0.11.0-{workflow}/`。
4. 先运行本次改动的静态/单元测试，再用 fresh agents 从原始 fixtures 运行四条 forward tests。测试者不接收预期缺陷或答案；验收者可在完成后对照 owner oracle。
5. 通过后只提交插件源码、当前验证脚本、报告和版本元数据；保密 fixtures、生成稿和测试输出不得提交或推送。
6. 提交并推送 GitHub 后，禁用 Local、升级并启用 Git 插件，运行 Git channel verify，再用新 task 做安装版本 smoke test。

### 待完成

- 无。已完成 Phase 不因后续版本变化自动重跑；只有所有者明确重开时才重新验收。

### 完成条件

- 上述共用与四条工作流验收标准全部有当前版本证据；无 Critical/Major 未解决项。
- Git commit、`v0.11.0` tag、GitHub push 和 Git 通道 fresh-task 发现均成功；机密测试例和测试产物不在提交中。

## 当前完成判定

`0.10.0` 基线已冻结；`0.11.0` 已用当前四条原始 fixture 的可达分支、fresh-agent 产物、隔离合同、索引完整性、Local 安装发现和无下游越权证据完成验收。Phase 0–9 均为已关闭历史，只有所有者明确重开时才能复验；后续版本不得把历史完成条件当作自动重复执行清单。

### 后续优先事项

- `P1`：规范 Deep Research 接续包（已在 `0.12.0` 实现）。每次需要转交 Deep Research 时，在同一接续目录生成且只生成以下两个配套文件：

  1. `deep-research-request-vNNN.md`：可直接发送给 Deep Research 的自包含研究任务。内容必须包括研究问题与用途、范围与排除项、已知背景与不确定性、待回答子问题、检索与来源要求、要求的报告结构以及验收标准。报告结构至少覆盖结论摘要、逐问题发现、主张与来源对应关系、冲突证据、不确定性与研究空白、对当前研究的启示、未完成事项和带链接的参考资料。文档不得依赖本地文件、内部编号或模型工作术语才能理解。
  2. `deep-research-follow-up-guide-vNNN.md`：面向研究者的验收和后续行动说明。内容必须包括配套请求文件与预期报告的相对路径、报告验收标准，以及收到报告后保存原件、核验关键来源与链接、检查主张可追溯性和适用范围、处理冲突与缺失、决定接受/补充检索/退回修订，并将通过核验的发现纳入原研究工作的具体步骤。

  实施时应在相关编排流程和接续模板中统一这两个文件的命名、版本关系与生成条件，不增加第三份内容重复的说明文件。两份文档均使用自然科研语言；内部状态、调度和审计用语不得进入可发送请求或研究者指引。

  验收标准：两个文件必须版本一致且相互链接；请求文件可脱离插件和本地目录直接使用；输出结构与逐项验收要求明确；指引能够让未参与前序工作的研究者独立判断报告是否合格并完成下一步；缺少来源、链接、关键问题答案、冲突说明或适用范围时不得视为通过；收到报告后必须保留原文，任何影响研究主张、方法或结论的整合都须进入相应工作流的独立复核环节。
- `P2`：仅在 OpenAI 插件的职责边界、合同和验收负担稳定后，将改造后的插件同步到 Hermes 源；不得直接复制 OpenAI 平台元数据或运行时语法。

## 非目标

- 团队或公共分发加固、稳定生产渠道和插件目录提交；
- 固定期刊、Outlet 或 Funder 目录及专用 Adapter；
- 新增第八个声明入口或恢复独立 PubMed Skill；
- 自动外部提交或自动替代人类签字；
- 没有明确个人认证数据需求时引入 Apps SDK 或 MCP。
