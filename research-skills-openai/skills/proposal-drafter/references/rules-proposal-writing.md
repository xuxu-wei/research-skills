# rules-proposal-writing

## Purpose

为 `proposal-drafter` 提供 proposal 写作规则。本文只定义写作边界和结构选择原则，不替代用户指定格式。

## Structure Selection

1. 若用户显式指定 proposal 结构、funding call 模板、机构模板、期刊要求或基金申请格式，应优先按照用户结构撰写。
2. 若用户未指定结构，使用 sibling template `template-proposal.md` in `../templates/` 的推荐结构。
3. 若用户结构与默认模板冲突，遵循用户结构。
4. 若用户结构要求的信息缺失，应保留对应栏目并标记缺口，不得补造。

## Default Proposal Scope

默认 proposal 应覆盖以下功能；具体章节数量和顺序由用户模板、binding constraints 与内容计划决定：

- 立项依据；
- 研究内容、研究目标和关键科学问题；
- 研究方案；
- 一个且仅一个 `Assumptions, feasibility, and risks` 权威位置；
- 特色与创新；
- 研究时间计划和预期成果；
- 参考文献，如 evidence summary 或用户材料支持。

## Writing Standards

- 初稿写作应围绕冻结的 content plan、proposal context brief、用户目标和已知证据展开。
- 按 `target_reader_profile` 和 `reader_prior_knowledge` 安排渐进披露；只解释读者在下一步推理前确实需要的术语。
- 每个章节应完成 content plan 中声明的 rhetorical function，并把读者交接到下一节所需的理解状态。
- 研究问题、目标、方法和预期成果必须相互一致。
- 信息缺失、证据不足或需要人工确认的事项记录在工作流交接产物中，不在 proposal 正文添加内部问题清单。
- 语言应正式、准确、可供后续 evaluator 审查。
- 不应使用夸张、营销式或无法证实的表述。

## Do Not Invent

不得补造：

- 数据来源；
- 样本量；
- endpoint / outcome；
- 实验结果；
- 文献结论；
- 合作者承诺；
- 资金、设备或平台可用性；
- feasibility 条件。

## Revision Rules

修订时应针对 evaluator 的具体意见进行 targeted revision。

每轮修订应保留：

- 原 proposal 文件路径；
- 新 proposal 文件路径或版本号；
- 主要修改点；
- 已解决问题；
- 未解决问题。

不得以无计划的全文重写替代可追踪修订。结构性缺陷确实需要整体重构时，先更新内容计划并说明为什么局部修复不能保持论证链。

Editorial repair 时，writer 只能读取统一的 editorial repair brief、当前完整 proposal 和 protected-content register；不得读取原始 narrative/language reports。一个 writer 可以顺序处理若干有边界的 section pass，但必须交付一个完整目标版本。
