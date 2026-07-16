# Research Skills OpenAI 路线图

## 文档元数据

| 字段 | 当前值 |
|---|---|
| 文档状态 | Personal Experimental/Preview |
| 规划基线 | 2026-07-16 |
| 当前插件版本 | `0.9.0-preview.1` |
| 当前范围 | 49 个 Skill、20 个独立 Reviewer、5 个完整工作流 |
| 发现面 | 7 个声明入口、6 个隐式入口、1 个 explicit-only 入口 |
| 当前验收状态 | `in_progress_owner_observation`，`0/13` 个 owner-observed 槽位完成 |

## 产品定位

`research-skills-openai` 是供单一所有者在 ChatGPT Work 和 Codex 中使用的研究工作流插件。当前路线只优化个人使用的可靠性、可复现产物、独立评估、清晰血缘和人工决策，不承诺生产支持、团队分发或自动外部提交。

所有完整工作流都必须保持角色分离：Generator 和 Drafter 不自评，Reviewer 针对冻结的只读输入在新实例中运行，Assembler 不静默修复源产物。实质性修订必须生成新版本并接受新的独立评估；Fatal 或未解决的 Blocking finding 会阻止晋级。

## 当前状态

- 当前源码为 `0.9.0-preview.1`，包含 49 个 Skill 和 68 条工作流边。
- 五个完整工作流为 Idea、Proposal、Article、Perspective 和 Research Polisher。
- 七个声明入口中，六个允许隐式调用；Research Polisher 永久保持 explicit-only。
- 17 个 entry mode 已通过确定性回放；Phase 4 的五个工作流和 63 个负向守卫通过。
- Phase 8 的 20-case 匿名语料全部通过，false-ready 为 0，Fatal/Blocking 检出、血缘、Reviewer 隔离、写入边界和异议保留均为 100%。
- GitHub Marketplace 安装机制已经实现；所有者环境已在 Codex App 和新的 Codex CLI 任务中诊断确认 `0.9.0-preview.1` 安装缓存与当前版本发现。正式 `personal-distribution-current` owner receipt 尚未记录，因此该槽位仍未完成。
- 确定性验证不等于真实运行验收。当前 13 个 owner-observed 槽位全部待完成，因此状态保持 `in_progress_owner_observation`。

## 阶段总览

| Phase | 名称 | 状态 | 当前结论 |
|---:|---|---|---|
| 0 | 引用与 Registry 闭合 | 已完成 | 依赖、入口和 Registry 一致 |
| 1 | Context 精简 | 已完成 | 发现描述和默认上下文受控 |
| 2 | Search 与 Deep Research 路由 | 已完成 | 原生检索路由和停止条件已定义 |
| 3 | 工作流状态机闭合 | 已完成 | 五个工作流具备独立评估闭环 |
| 4 | 场景评估与持续验证 | 已完成 | 5/5 工作流和 63 个负向守卫通过 |
| 5 | GitHub Marketplace 安装与更新 | 已完成 | 安装机制有效，当前版本运行验证待 Phase 7 完成 |
| 6 | 维护性与当前版本强化 | 已完成 | Artifact、DOCX、README、Cover Letter 和 Idea v3 完成 |
| 7 | 个人安装与工作流就绪 | 进行中 | 当前版本安装发现已诊断确认；正式分发 receipt、五个 happy path 和两个控制待完成 |
| 8 | 个人原生研究闭环 | 进行中 | 三个 Search 和两个 Deep Research 槽位待完成 |

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

- 无源码工作；真实 Search 和 Deep Research 运行观察属于 Phase 8。

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

- 无源码工作；真实运行结果由 Phase 7 验证。

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
- GitHub `main`、Marketplace `git-subdir`、更新/重装命令和本地 cachebuster 流程已经实现。
- 历史安装已证明 Marketplace 注册、升级和新任务发现机制可工作。

### 待完成

- `0.9.0-preview.1` 的安装缓存与新任务发现已完成诊断确认；正式 owner-observed 记录属于 Phase 7，不重复记为本阶段开发工作。

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
- 当前版本保持 49 个 Skill、20 个 Reviewer、7 个声明入口、6 个隐式入口和 17 个 entry mode。

### 待完成

- 无源码工作；这些能力的当前版本真实使用纳入 Phase 7。

### 完成条件

- Artifact completeness、Article DOCX、Context、Phase 4、Phase 7 和 Phase 8 确定性测试全部通过。

## Phase 7：个人安装与工作流就绪

- 状态：`进行中`
- 优先级：`P0`
- 目标：证明当前版本在所有者 Codex 环境中能够安装、发现并完成五个工作流的受控人工交付。

### 已完成

- 17 个 entry mode 的确定性回放全部通过，入口绕过和陈旧输入守卫有效。
- 五个工作流的状态、角色隔离、版本血缘和停止条件已经实现。
- Research Polisher 已实现为第五个工作流和第七个声明入口，并永久保持 explicit-only。
- Research Polisher 冻结研究 Dossier，由科学意义、实际价值和传播定位三个互盲角色分别提出 `reposition_only`、`small_extension` 和 `moderate_extension` 策略，再由独立方法学/可发表性 Reviewer 评估，最终停在人工策略选择。

### 待完成

- 完成 `personal-distribution-current`：把已诊断确认的 `0.9.0-preview.1` 安装、App/CLI 发现、49 个 Skill、7 个声明入口和6 个隐式入口绑定到正式 owner receipt。
- 完成五个 happy path：Idea、Proposal、Article、Perspective 和 `personal-research-polisher-happy`。
- 完成两个控制：Reviewer 不可用时停在 `independent_review_pending`；Fatal 或未解决 Blocking finding 不得产生 ready 状态。
- Research Polisher 必须验证显式正向调用，同时不接管语言润色、普通写作、新 Idea 或一般文献检索。

### 完成条件

- 安装发现槽位、五个工作流槽位和两个控制槽位均记录为当前版本 `owner_observed`。
- Accepted run 必须绑定任务、源码身份、Artifact、版本、Digest、Reviewer 实例、时间戳、结果和所有者确认。
- 五个 happy path 分别到达 `human_signoff_required` 或 `human_strategy_selection_required`，false-ready 为 0。

## Phase 8：个人原生研究闭环

- 状态：`进行中`
- 优先级：`P0`
- 目标：证明当前版本能够正确使用内置 Search，并完成 Deep Research 的停止与返回闭环。

### 已完成

- 20-case 匿名语料覆盖五个工作流的 happy、fixable、fatal/pending 和 no-gain 结果。
- Fatal/Blocking 检出、Major finding 检出、血缘、Reviewer 隔离、写入边界和异议保留均为 100%，false-ready 为 0。
- 三个风险分层的合成 repeat case 保持独立 Reviewer 和一致结果。

### 待完成

- 完成 `personal-search-current`、`personal-search-exact` 和 `personal-search-narrow-academic`。
- 完成 `personal-deep-research-inactive`，确认不在当前任务中模拟 Deep Research，并生成自包含 handoff。
- 完成 `personal-deep-research-complete`，绑定 handoff、用户启动、完成、Mapper return 和原工作流单边恢复。

### 完成条件

- 三个 Search 和两个 Deep Research 槽位均记录为当前版本 `owner_observed`。
- Search 的 Material claim 绑定已打开的权威来源；Deep Research return 与恢复绑定同一 Evidence Artifact 和 Digest。

## 当前完成判定

插件当前为 `deterministic_validated` 和 `in_progress_owner_observation`。只有以下 13 个槽位全部完成后，才能进入 `owner_observed_ready`：

- 1 个当前版本安装与新任务发现槽位；
- 5 个工作流 happy path；
- 2 个跨工作流控制；
- 3 个 Search 槽位；
- 1 个 Deep Research inactive 控制；
- 1 个完整 Deep Research handoff-return-resume 循环。

Fixture、状态文本、文件名或仓库内手写记录不能替代 owner-observed 证据。

## 非目标

- 团队或公共分发加固、稳定生产渠道和插件目录提交；
- 固定期刊、Outlet 或 Funder 目录及专用 Adapter；
- 新增第八个声明入口或恢复独立 PubMed Skill；
- 自动外部提交或自动替代人类签字；
- 没有明确个人认证数据需求时引入 Apps SDK 或 MCP。
