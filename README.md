# Research Skills

面向 OpenAI 生态的科研流程 Skill 仓库。唯一维护的插件是 `research-skills-openai`，包含 10 个 Skill，用于 Codex 中的通用学术写作与编辑，以及选题、标书、论文、Perspective、已有研究改进、统计分析计划和统一科研评估。

Skill 提供研究流程和判断依据。搜索、数据库访问、文档处理等通用能力使用当前环境可用的工具与插件，不在本仓库重复构建。主任务负责整理、规划、撰写、修订和汇编，独立评审检查科学内容。

## Skill 入口

两个可独立使用的通用技能覆盖不同学科的论文、标书、报告、分析计划、教材和其他学术材料：

| Skill | 用途 |
| --- | --- |
| [academic-writer](research-skills-openai/skills/academic-writer/SKILL.md) | 根据材料、笔记或提纲组织和撰写清楚、连贯的学术论述 |
| [academic-humanizer](research-skills-openai/skills/academic-humanizer/SKILL.md) | 检查和修改已有材料的结构、衔接与表达，保留科学含义、证据和作者立场 |

两份技能正文与参考说明使用中文，便于审阅修改；成稿语言遵循任务要求，支持中英文材料。它们可在其他学术任务中单独使用，也已接入下面全部研究流程、专业建议和评审报告的写作与编辑。

六个撰写流程均调用未参与当前版本撰写的 `research-evaluator` 实例完成独立评估：

| 任务 | 主流程 | 主要用途 |
| --- | --- | --- |
| 研究选题 | `research-idea-orchestrator` | 从问题、证据或数据形成可比较的研究方向 |
| 研究标书 | `proposal-orchestrator` | 将研究问题、论证、方法和资源组织成可行方案 |
| 研究论文 | `article-orchestrator` | 根据实际研究材料撰写和修订论文，在一次评估中按需结合医学和编辑判断 |
| Perspective | `perspective-orchestrator` | 构建有证据、反论证和明确贡献的学术观点 |
| 已有研究改进 | `research-improvement-planner` | 比较重新定位、补充分析和研究扩展的科学价值与代价 |
| 统计分析计划 | `sap-writer` | 编写或修订目标明确、方法连贯、能够实施的分析计划 |

另有两个按需使用的专业 Skill：

| Skill | 用途 |
| --- | --- |
| [research-evaluator](research-skills-openai/skills/research-evaluator/SKILL.md) | 统一独立评估科学价值、证据和任务准备程度，按需处理投稿咨询、初筛、修回及评论核查 |
| `methodology-statistics-preflight` | 在起草或继续工作前检查研究问题、设计、数据和分析是否匹配 |

前四个主流程和两个通用写作、编辑技能允许 Codex 按任务自动匹配。研究改进入口及其余专业和评审 Skill 保持显式调用，可由用户或主流程按需使用。

例如：

```text
用 $academic-writer 将这些笔记写成一段面向研究生的学术说明。
用 $academic-humanizer 修改这份英文报告的组织和表达，保留语言、数据、引文和结论强度。
用 $research-idea-orchestrator 根据这些文献和可用数据，比较值得开展的研究方向。
用 $proposal-orchestrator 将这份研究构想发展为符合所附指南的标书。
用 $article-orchestrator 根据研究方法、结果表和草稿修订论文。
用 $perspective-orchestrator 围绕这个观点形成一篇有证据和反论证的 Perspective。
用 $research-improvement-planner 评估这项已完成研究还值得补做哪些工作，并比较收益和成本。
```

评估也可直接调用：

```text
用 $research-evaluator 独立评估这份论文和研究结果，解释适用评分及下一步。
用 $research-evaluator 评阅这份标书，分别说明研究价值、科学依据和申请准备情况。
用 $research-evaluator 检查这份统计分析计划，说明哪些分析可以实施、哪些决定仍待确认。
```

统一评估的正文与参考资料使用中文，发现描述保持英文，继续显式调用。它按任务加载共同价值、科学依据、文章类型，以及标书、分析计划或编辑决策标准；评论来信和更正线索采用专门核查。

综合研究价值、科学依据和任务准备程度分别解释。关键材料不足时暂不评分；尚无结果的方案按拟定研究评价，常规方法也可得到很高的分析计划评价。标书与 SAP 的新增五级标准属于本项目拟议标准，仍待人工试评，具体来源和取舍见[说明](research-skills-openai/skills/research-evaluator/references/guidance/sources.md)。

## 工作方式

先理解已有材料和研究目标，再按需要补充证据、检查设计、起草和修订。撰写读者材料时使用 `academic-writer`，完整草稿形成后，在科学评审或交付前使用 `academic-humanizer` 编辑。写作和编辑由产出材料的任务完成。

独立科学评审由未参与该版本撰写的评审者完成，保留有依据的异议。评审者同样编辑自己撰写的报告，保持发现、批评程度和证据；主任务保留独立评审结论。方法、结果或实质性结论发生变化时，保存新版本并重新评审；纯措辞和排版修改不需要重跑完整流程。

所有报告、表格、图注、摘要和附录直接解释研究对象、判断、证据、评分含义及下一步，使用完整名称，不暴露工作流内部代号或要求读者查阅图例。科学公式与必要术语按含义保留。

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

安装后开启新的 Codex 任务。若 `codex` 不在 PATH 中，使用当前环境实际的 CLI 可执行文件路径。Marketplace 保持原有名称、GitHub 地址和插件子目录，跟踪 `main`；仓库默认直接在 `main` 维护。

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
  skills/                        10 个 Skill 及其按需参考资料
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

此前结构重构将 51 个 Skill 收敛为 14 个：写作、组织、修订和汇编职责合并到主流程；通用检索交给可用工具和其他插件；独立科学评审保留。当时移除了工作流 Registry、状态协议、固定评分与报告模板，以及旧审计、安装包装脚本和自动 Skill 测试。

随后加入通用的 `academic-writer` 和 `academic-humanizer`，形成 16 个 Skill。本次将六个 evaluator 与医学期刊评审合并为 `research-evaluator`，当前为 10 个 Skill。按所有者指定的编辑部流程恢复并扩展有领域依据的评分，定义与适用条件集中在参考标准中；不恢复脱离证据的通用晋级规则、评分脚本或固定报告模板。

| 删除的入口 | 当前入口与用途 |
| --- | --- |
| `idea-evaluator` | `research-evaluator`：选题评价 |
| `proposal-evaluator` | `research-evaluator`：标书评价与准备程度 |
| `article-evaluator` | `research-evaluator`：论文科学评估 |
| `perspective-evaluator` | `research-evaluator`：观点和论证评估 |
| `research-improvement-evaluator` | `research-evaluator`：已有研究改进比较 |
| `sap-evaluator` | `research-evaluator`：分析计划的科学依据与可执行性 |
| `medical-journal-review` | `research-evaluator`：医学解释、投稿咨询及编辑处理 |

更早的 `research-polisher-orchestrator` 已改名为 `research-improvement-planner`；`research-polisher-methodology-publishability-reviewer` 曾改名为 `research-improvement-evaluator`，现在同样迁入统一评估。七个旧入口均已删除，不保留转发技能。

旧名称不保留别名，请更新个人提示词。历史实现和记录可从 Git 历史查看。个人研究输入与运行产物放在已忽略的 `.local/research-runs/`，不放入 `tests/`。

## 许可

[MIT License](LICENSE)。
