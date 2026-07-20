# Research Skills OpenAI 路线图

## 文档元数据

| 字段 | 当前值 |
|---|---|
| 文档状态 | Personal Experimental/Preview |
| 规划基线 | 2026-07-18 |
| 当前插件版本 | `0.10.0` |
| 当前范围 | 50 个 Skill、21 个独立 Reviewer、5 个完整工作流 |
| 发现面 | 7 个声明入口、6 个隐式入口、1 个 explicit-only 入口 |
| 当前路线图状态 | 个人使用基线已接受，Phase 7–8 已完成 |
| 严格复验状态 | `in_progress_owner_observation`，`0/13` 个 owner-observed 槽位完成（可选） |

## 产品定位

`research-skills-openai` 是供单一所有者在 ChatGPT Work 和 Codex 中使用的研究工作流插件。当前路线只优化个人使用的可靠性、可复现产物、独立评估、清晰血缘和人工决策，不承诺生产支持、团队分发或自动外部提交。

本文件同时用于记录过去已经完成的工作、说明当前版本状态和规划未来事项。标记为“已完成”的 Phase 是历史记录，不是后续版本的重复执行清单；除非所有者明确重开，否则不得再次运行。后续版本可能使其中原有步骤或验收口径不再适用，当前开发只验证正在进行的事项和本次变更直接影响的合同。

所有完整工作流都必须保持角色分离：Generator 和 Drafter 不自评，Reviewer 针对冻结的只读输入在新实例中运行，Assembler 不静默修复源产物。实质性修订必须生成新版本并接受新的独立评估；Fatal 或未解决的 Blocking finding 会阻止晋级。

## 当前状态

- 当前源码为 `0.10.0`，包含 50 个 Skill 和 70 条工作流边。
- 五个完整工作流为 Idea、Proposal、Article、Perspective 和 Research Polisher。
- 七个声明入口中，六个允许隐式调用；Research Polisher 永久保持 explicit-only。
- 17 个 entry mode 已通过确定性回放；Phase 4 的五个工作流和 63 个负向守卫通过。
- Phase 8 的 20-case 匿名语料全部通过，false-ready 为 0，Fatal/Blocking 检出、血缘、Reviewer 隔离、写入边界和异议保留均为 100%。
- GitHub Marketplace 安装、缓存发现和路由机制已经诊断；所有者接受其作为当前个人使用基线，但不将此表述扩展为严格全量工作流已验证。
- Phase 7 已关闭。Phase 8 按所有者决定默认视为已完成，完整 Search/Deep Research 原生闭环仅在所有者明确要求时复验。
- 严格 13 槽位档案仍真实保持 `in_progress_owner_observation` 和 `0/13`；它是可选复验工具，不再是路线图门槛，也不代表已完成严格全量验证。

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

## 当前完成判定

插件当前保持 `deterministic_validated`，个人使用基线已由所有者接受，Phase 7–8 在路线图中均已关闭。严格 receipt 验证器仍真实报告 `in_progress_owner_observation` 和 `0/13`；该状态不再阻塞后续个人开发。

以下 13 个槽位保留为可选的严格全量复验档案，而不是活动路线图门槛：

- 1 个当前版本安装与新任务发现槽位；
- 5 个工作流 happy path；
- 2 个跨工作流控制；
- 3 个 Search 槽位；
- 1 个 Deep Research inactive 控制；
- 1 个完整 Deep Research handoff-return-resume 循环。

除非所有者明确要求，不得自动启动、恢复或调度上述槽位。若重新要求 `owner_observed_ready`，Fixture、状态文本、文件名或仓库内手写记录仍不能替代 owner-observed 证据。

### 后续优先事项

- `P0`：把已在 Idea 中验证的 narrative readiness 抽象为Proposal、 Article、Perspective 等工作流可复用的公共模块。当前版本不改动这些工作流。
- `P2`：仅在 OpenAI 插件的职责边界、合同和验收负担稳定后，将改造后的插件同步到 Hermes 源；不得直接复制 OpenAI 平台元数据或运行时语法。

## 非目标

- 团队或公共分发加固、稳定生产渠道和插件目录提交；
- 固定期刊、Outlet 或 Funder 目录及专用 Adapter；
- 新增第八个声明入口或恢复独立 PubMed Skill；
- 自动外部提交或自动替代人类签字；
- 没有明确个人认证数据需求时引入 Apps SDK 或 MCP。
