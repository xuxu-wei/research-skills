# AGENTS.md

本文件适用于 `research-skills-openai/` 插件子树，并覆盖仓库根目录中冲突的通用规则。

## 输出内容

所有面向研究者和用户的文本使用自然语言和标准科学术语；模型内部工作术语/状态机术语不允许出现在任何面向用户的内容中。

## 产品边界

- 将插件视为所有者个人维护的 Experimental/Preview 研究工具，服务于 ChatGPT Work 和 Codex。
- 优先保证个人使用可靠、产物可复现、评估独立和人工决策明确。不得暗示生产支持、公共就绪、Provider 验证、自动更新或自动外部提交。
- 默认采用 `personal-owner` 验收边界；不维护共享或公共认证路线。
- 插件保持 skills-only；只有在真实 MCP Server、App mapping 或 Hook 已实现并通过测试时才能扩展。

## 工作流不变量

每个完整工作流必须依次完成生成、全新独立评估、定向修订、全新复评或 Panel，以及最终人工审阅包。

- Orchestrator 负责路由、状态和停止条件，不负责评分。
- Generator 和 Drafter 不得自评。Reviewer 必须在新的委派实例中针对冻结的只读输入运行，并且只能写 Review 或核验报告。
- Assembler 必须保留来源、冲突、少数意见和异议，不得静默修复源产物。
- 每次实质性变更都必须创建新版本，并由新的 Evaluator 评估后才能晋级或进入 ready 状态。
- 无法执行独立评审时，返回 `independent_review_pending` 和自包含 continuation brief，然后停止；不得以内联自评替代。

## 产物与人工边界

- 源产物保持不可变；修订、Review 报告和 Delta 分开保存，并包含完整血缘。所有工作流的 LLM-facing 合同使用 `{artifact_id, version, exact_path}`、冻结状态、完整索引与唯一当前指针，不写入 SHA/Digest；旧字段可读取但忽略。确定性开发工具可在内存中比较内容，但不得把哈希保存进工作流接口。
- Fatal 或未解决的 Blocking finding 会阻止晋级和 ready 状态。
- 工作流止于供人类审阅和签字的材料，不向期刊、基金方、仓库或其他外部平台提交。
- 确定性 Fixture 只能建立 `deterministic_validated`，不能证明真实运行完成。
- 只有当前版本任务绑定了源码身份、产物逻辑身份、Reviewer 身份（如适用）、时间戳、结果和所有者确认后，才能记录为 `owner_observed`。索引完整性与当前指针必须核验；不要求把 Digest 写入人类或 LLM 审阅的记录。

## Skill 与发现纪律

- 修改 Skill 前，读取目标 `SKILL.md`、其必需引用、`workflow-registry.yaml` 及调用它的所有 Orchestrator；新建或大幅改写时使用 `skill-creator`。
- 核心流程保留在 `SKILL.md`；Schema、Rubric、示例、变体和长篇操作细节放入直接链接且带加载条件的引用。
- 除非所有者作出明确产品决策，否则保持发现面稳定。Research Polisher 永久为 explicit-only。
- 描述和默认加载上下文保持精简；已有超限 Skill 或引用属于 Roadmap 技术债，修改时不得继续增大。
- Source、Registry、生成元数据、文档、Fixture 和验证预期必须同步更新。

## 版本化开发与交付

- `.codex-plugin/plugin.json` 与 `workflow-registry.yaml` 必须使用相同 SemVer。
- 版本变化时同步所有当前版本声明，同时保留明确标记为历史记录的版本信息。
- 交付前运行适用的仓库和插件审计，修复全部错误并报告剩余警告。
- 完成插件版本升级任务后，必须创建包含完整升级内容的 Commit 并推送到 GitHub；不得只留在本地工作树。
- 保留无关用户工作，不得发布本地 cachebuster 版本。

## 渐进披露

仅在任务需要时加载对应细节：

- `workflow-registry.yaml`：库存、角色、边、模式和调用策略。
- `README.md`：安装、更新、Quickstart、产物默认值、个人验收操作和验证命令。
- `ROADMAP.md`：过去与现在的记录及未来规划。已完成 Phase 是历史快照，即使后续版本使其不再适用也不得自动重跑；只有所有者明确重新开启时才能复验。
- 目标 `SKILL.md` 及其显式链接的引用：工作流局部流程、Schema、Rubric、Template 和资源加载条件。
- 根目录 `AGENTS.md`：仓库级配置隔离、Authoring 工具、审计要求以及 Hermes/OpenAI 边界。

## 必需验证

```powershell
python scripts/audit_openai_research_plugin.py
python scripts/audit_openai_research_proposal.py
python scripts/audit_openai_research_perspective.py
python scripts/test_openai_roadmap_contract.py
python scripts/test_openai_release_contract.py
python scripts/test_openai_cross_workflow_narrative_contract.py
python scripts/test_openai_article_docx_contract.py
python scripts/test_openai_plugin_dev.py
python scripts/codex_plugin_converter.py --mode codex --fail-on-invalid
python "$env:USERPROFILE\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" research-skills-openai
```

此外，对每个新增或修改的 Skill 运行 `skill-creator/scripts/quick_validate.py`。上述清单只覆盖当前改动；ROADMAP 中已完成的历史 Phase 验证不得因版本升级而重复执行。

修改共享 Hermes 工作流契约或源文件时，还必须运行 `python scripts/audit_research_workflows.py`。
