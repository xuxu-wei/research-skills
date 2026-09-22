# Research Skills

面向 OpenAI 生态的科研流程 Skill 仓库。唯一维护的插件是 `research-skills-openai`，用于 Codex 中的选题、标书、论文、Perspective、已有研究改进和科学评审。

Skill 提供研究流程和判断依据。搜索、数据库访问、文档处理等通用能力使用当前环境可用的工具与插件，不在本仓库重复构建。主任务负责整理、规划、撰写、修订和汇编，独立评审检查科学内容。

## Skill 入口

| 任务 | 主流程 | 独立评审 | 主要用途 |
| --- | --- | --- | --- |
| 研究选题 | `research-idea-orchestrator` | `idea-evaluator` | 从问题、证据或数据形成可比较的研究方向 |
| 研究标书 | `proposal-orchestrator` | `proposal-evaluator` | 将研究问题、论证、方法和资源组织成可行方案 |
| 研究论文 | `article-orchestrator` | `article-evaluator` | 根据实际研究材料撰写和修订论文 |
| Perspective | `perspective-orchestrator` | `perspective-evaluator` | 构建有证据、反论证和明确贡献的学术观点 |
| 已有研究改进 | `research-improvement-planner` | `research-improvement-evaluator` | 比较重新定位、补充分析和研究扩展的科学价值与代价 |

另有四个按需使用的专业 Skill：

| Skill | 用途 |
| --- | --- |
| `methodology-statistics-preflight` | 检查研究问题、设计、数据和分析是否匹配 |
| `medical-journal-review` | 从医学方法学、临床意义和期刊读者角度评审论文 |
| `sap-writer` | 编写或修订统计分析计划，并安排独立评审 |
| `sap-evaluator` | 独立检查统计分析计划的合理性和可实施性 |

前四个主流程允许 Codex 按任务自动匹配。研究改进入口及其余专业和评审 Skill 保持显式调用，可由用户或主流程按需使用。

例如：

```text
用 $research-idea-orchestrator 根据这些文献和可用数据，比较值得开展的研究方向。
用 $proposal-orchestrator 将这份研究构想发展为符合所附指南的标书。
用 $article-orchestrator 根据研究方法、结果表和草稿修订论文。
用 $perspective-orchestrator 围绕这个观点形成一篇有证据和反论证的 Perspective。
用 $research-improvement-planner 评估这项已完成研究还值得补做哪些工作，并比较收益和成本。
```

评审也可直接调用，例如 `用 $article-evaluator 独立评审这份论文和所附研究结果。`

## 工作方式

先理解已有材料和研究目标，再按需要补充证据、检查设计、起草和修订。独立评审由未参与该版本撰写的评审者完成，保留有依据的异议。方法、结果或实质性结论发生变化时，保存新版本并重新评审；纯措辞和排版修改不需要重跑完整流程。

方向选择、额外资源投入和对外提交由研究者决定。缺少关键证据或独立评审时，可交付注明限制的草稿。默认提供可编辑的 Markdown，也可按要求使用可用工具制作其他格式。

## 安装和更新

在支持插件命令的 Codex CLI 中，从 GitHub 注册 Marketplace 并安装：

```powershell
codex plugin marketplace add xuxu-wei/research-skills --ref main
codex plugin add research-skills-openai@xuxu-research-preview
```

更新已安装的 GitHub 版本：

```powershell
codex plugin marketplace upgrade xuxu-research-preview
codex plugin add research-skills-openai@xuxu-research-preview
```

安装后开启新的 Codex 任务。若 `codex` 不在 PATH 中，使用当前环境实际的 CLI 可执行文件路径。Marketplace 保持原有名称、GitHub 地址和插件子目录，跟踪 `main`；尚未合入 `main` 的重构分支不会通过这些命令安装。

本插件仍是个人维护的实验性项目。源码版本以 [插件 Manifest](research-skills-openai/.codex-plugin/plugin.json) 为准；人工验证状态见 [ROADMAP.md](ROADMAP.md)。ChatGPT 网页端的安装与行为尚未验证。

## 辅助脚本：生成兼容技能包

不再维护 Hermes 版 `research-skills/` 或预生成的 `skills-flatten/` 副本。需要普通 Skill 目录时，从唯一技能源按需导出：

```powershell
python scripts/auxiliary/generate_flatten_skills.py
```

默认生成到仓库的 `dist/skills-flatten/`，不论从哪个工作目录调用。指定其他输出目录：

```powershell
python scripts/auxiliary/generate_flatten_skills.py --output .local/exports/research-skills
```

`--output` 的相对路径以调用时的工作目录为准。脚本要求 Python 3.11 或更新版本，仅使用标准库；输出目录必须不存在或为空。已有非空目录不会被覆盖，重新导出时请指定新的目录。

脚本复制各 Skill 的 `SKILL.md` 和引用、资源等文件，排除 `agents/` 平台元数据、测试和缓存。它不安装插件，也不改写 Skill 语义或模拟目标平台的工具能力；目标环境的调用与独立评审能力需要另行确认。分发导出包时应附上仓库的 [LICENSE](LICENSE)。

原根目录脚本入口已移至 `scripts/auxiliary/`。生成包不提交到 Git；`dist/` 和 `.local/` 已忽略。

## 仓库结构

```text
research-skills-openai/
  .codex-plugin/plugin.json       插件信息与唯一版本号
  skills/                        14 个 Skill 及其按需参考资料
  README.md                      插件导航
.agents/plugins/marketplace.json GitHub Marketplace
scripts/auxiliary/               辅助自动化脚本
tests/scripts/                   仅测试辅助脚本
docs/development.md              开发和人工验证方法
ROADMAP.md                       唯一规划文档
```

## 开发与测试

Skill 的触发、科研质量和实际流程全部由所有者人工测试。自动测试仅覆盖辅助脚本，使用合成文件，不读取研究案例或断言 Skill 文案：

```powershell
python -m unittest discover -s tests/scripts -v
```

CI 保留原检查名称 `OpenAI Plugin Preview / validate`，内容仅为上述脚本测试。完整说明见 [开发指南](docs/development.md)。

## 从旧版迁移

此次重构将 51 个 Skill 收敛为 14 个：写作、组织、修订和汇编职责合并到主流程；通用检索交给可用工具和其他插件；独立科学评审保留。移除工作流 Registry、状态协议、固定评分与报告模板，以及旧审计、安装包装脚本和自动 Skill 测试。

| 原名称 | 新名称 | 定位 |
| --- | --- | --- |
| `research-polisher-orchestrator` | `research-improvement-planner` | 为已有研究规划科学改进 |
| `research-polisher-methodology-publishability-reviewer` | `research-improvement-evaluator` | 独立评估改进方案的科学价值与可行性 |

旧名称不保留别名，请更新个人提示词。历史实现和记录可从 Git 历史查看。个人研究输入与运行产物放在已忽略的 `.local/research-runs/`，不放入 `tests/`。

## 许可

[MIT License](LICENSE)。
