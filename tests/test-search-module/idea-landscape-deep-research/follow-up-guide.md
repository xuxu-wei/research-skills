# Idea Landscape Deep Research 测试

请在当前 `research-skills` 项目中启动完整 `$research-idea-orchestrator`，完成以下
测试。

- 只读输入：`tests/test-idea/idea-initial.md`
- Mapper 输出配置：`idea_landscape`
- 证据检索模式：`deep_research`
- 唯一输出目录：`tests/test-search-module/idea-landscape-deep-research/runs/run-001/`
- 会话显示名：`codex-test-idea-landscape-deep-research`

开始前确认当前启用的是 Local `research-skills-openai` 插件，基础版本为
`0.13.0`，安装版本带有 `+codex.local-*`。如果版本或通道不符，不要继续研究，
只在输出目录写明实际版本和停止原因。

输入完整性只用只读路径和 `unchanged_at_pause: true` 之类的简单确认；不要计算、
记录或报告 SHA、content hash、checksum 或 digest。

使用给定输入启动完整 Idea 工作流，并要求证据阶段调用
`research-landscape-mapper` 的 `idea_landscape` 配置。不得修改输入文件、插件
源码或其他测试目录。证据阶段强制使用 Deep Research，不得以普通 Web Search、
普通对话总结或多次 focused synthesis 代替实际 Deep Research 返回报告。

当工作流需要 Deep Research 时：

1. 在本次运行的 `02_evidence/deep-research/round-NNN/` 下生成且只生成配套的
   `deep-research-request-vNNN.md` 和
   `deep-research-follow-up-guide-vNNN.md`。
2. 运行 mapper 提供的确定性 continuation-package 校验器。
3. 在输出根目录写入 `run-status.yaml`，记录 case、实际插件版本、工作流、输入、
   输出、检索模式、Mapper 输出配置、当前阶段、两份接续文件路径和下一步；然后
   暂停，等待真实 Deep Research 报告，不得自行模拟报告。
4. 在对话中明确返回接续文件和 `run-status.yaml` 的准确路径。

收到并保存真实 `deep-research-report-vNNN.md` 后，在同一工作流会话中继续：
核验核心问题及子问题覆盖、主张—来源可追溯性、完整链接、最相近工作、相反
证据、适用范围和未解决问题；保留原始报告；生成 `idea_landscape` 所要求的
Evidence Map、Opportunity Map、读者推理 handoff 和 Idea direction signals。
原始请求、guide、报告和搜索历史不得进入 `idea-evaluator` 输入。

最终在输出根目录生成 `result-summary.md`，列出实际完成分支、所有产物路径、
引用与链接检查、输入未修改确认、未解决问题和最终停止/完成原因。不要根据此
测试提示猜测预期 Idea 判断、创新性结论或修复答案。
