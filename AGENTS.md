# AGENTS.md

## 顶层操作原则

- 修改文件前读取距离目标文件最近的 `AGENTS.md`；子目录规则在其范围内覆盖本文件。
- 同时维护两种配置：`research-skills/` 下的 Hermes 源与 `research-skills-openai/` 下的 OpenAI 插件。不得在两者之间复制平台专属元数据或运行时语法。
- 新建或大幅改写 Skill 前使用 `skill-creator`；涉及插件结构、Marketplace 或安装流程时使用 `plugin-creator`。
- 限定变更范围，保留无关用户工作；除非请求明确包含，否则不得修改外部或第三方 Skill。
- 维持单一职责、渐进披露、独立评估、产物血缘、可见异议和明确停止条件。
- 生成器、评估器、Reviewer 与汇编器必须保持角色分离。实质性产物发生变化后，必须由新的独立实例重新评估，才能晋级或最终交付。
- 源文件、生成的 Registry、Manifest、文档和验证预期必须同步更新。
- 交付前运行适用的仓库与插件审计；修复所有错误，并报告仍然存在的警告。
- 涉及 OpenAI 插件的本地开发、安装、测试或发布时，遵循 `research-skills-openai/docs/development-test-release-workflow.md`；插件子树内更具体的 `AGENTS.md` 规则仍然优先。
