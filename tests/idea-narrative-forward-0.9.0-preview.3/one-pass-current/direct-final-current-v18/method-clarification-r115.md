---
review_id: method-clarification-I01-001-r115
reviewer_skill: methodology-statistics-preflight
reviewer_instance_id: methodology-statistics-preflight-r115-fresh-01
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r115
input_artifact_ids:
  - idea-dossier-I01-001-v052
input_versions:
  - v052
files_read:
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/methodology-statistics-preflight/SKILL.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/working-assumption-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/endpoint-metric-checks.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/idea-dossier-v052.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: revise_endpoint_or_metric
idea_handoff_decision: proceed_with_assumptions
findings:
  - finding_id: MCF-CCR-001
    classification: working_assumption
    severity: blocking_if_unresolved_before_simulation
  - finding_id: MCF-STATE-ROLE-001
    classification: working_assumption
    severity: blocking_if_unresolved_before_simulation
unresolved_issues:
  - 系统辨识负责人尚须在首次模拟拟合前确认连续潜在状态恢复的唯一统计定义及状态角色绑定。
---

# 连续潜在状态恢复标准的科学澄清

## 结论

“连续主要典型相关至少 0.80”按现有表述**不是唯一可计算的判定量**。典型相关分析对两个多维变量给出一列按大小排序的典型相关，而不是天然唯一的一个数；现有文本也未规定取第一项、最小项或平均值，未规定维度或秩不一致的处理，也未规定如何把至少 1,000 次模拟重复汇总为情景级达标结论。不同选择能够让同一候选模型得到不同的准入结果，因此这不是纯措辞问题，也不得由编辑写作者静默决定。

本问题无需触发整体澄清停止。研究问题、生成机制、连续潜在状态对象和降级路线已经存在；即使保守标准未达到，仍可合并或删除维度，或改用线性状态空间、多状态或仅预测表征。因此可在下面这个明确、有界、可验证的工作假设下条件性推进。

## 有界工作假设

```yaml
assumption_id: WA-CCR-001
unconfirmed_detail: >-
  连续潜在状态恢复的典型相关如何从多维相关序列和多次模拟重复归约为唯一准入统计量，以及“状态恢复”中各类状态对象的对应关系。
working_assumption: >-
  连续分支只评价生成的连续潜在生理状态 X 与其估计后验均值；每次模拟重复先计算覆盖全部真实潜在维度的最小典型相关，再以该最小典型相关在重复间均值的双侧 95% 正态近似区间下限作为情景级统计量。只有该下限至少为 0.80 才达标。维度不等、任一侧秩不足或协方差奇异时，该次重复记为 0。离散调整兰德指数只评价生成的离散潜在机制或状态区段，不评价临床规则直接生成的发病后互斥结局状态。
basis_for_planning: >-
  该定义对所有真实连续维度提出恢复要求，避免仅用最大的第一典型相关掩盖其余维度未恢复；以置信区间下限判定也把蒙特卡洛不确定性纳入准入。它不改变研究问题、临床主要任务或推断对象，并保留 dossier 已规定的简单模型降级路线。
impact_if_false: >-
  若负责人不接受这一定义、拟采用第一典型相关或其他汇总方式，当前连续状态恢复门槛不得用于复杂候选准入；须在查看任何模拟恢复结果前重新完成方法学澄清并冻结替代定义。若结果已经被查看，相关连续状态恢复结论失效，复杂候选不得凭该结果晋级，只能保留已预设的线性、多状态或仅预测路线，直至新的独立评估完成。
verification_needed: >-
  确认连续潜在状态矩阵、估计后验均值、评价格点、维度、秩处理、重复级计算代码、情景级汇总代码，以及调整兰德指数所对应的离散潜在机制标签；用一个完全恢复、一个仅恢复首维和一个维度不匹配的确定性测试例验证预期分别为达标、未达标和未达标。
verification_point: >-
  首次模拟拟合和任何模拟结果查看之前，最迟在月 7 的模拟方案与代码冻结时。
affected_design_component: >-
  WP2 的绝对模拟与半合成恢复、复杂候选准入，以及所有基于连续潜在状态恢复作出的结构解释。
owner: 系统辨识负责人；纵向统计负责人独立复核计算与判定代码
deadline: 月 7 模拟方案与代码冻结前，且必须早于首次模拟拟合或结果查看
```

### 唯一可执行的计算定义

对预先指定为需要连续状态恢复的每个模拟情景和每次重复 \(b=1,\ldots,B\)：

1. 在预先固定的患者—时间评价格点上，组成真实连续潜在状态矩阵 \(X_b\in\mathbb{R}^{n_b\times d_b}\) 与同一点的估计后验均值矩阵 \(\widehat X_b\)。不得依据恢复结果删选患者、时点或维度。
2. 对两矩阵按列中心化，使用同一组患者—时间行计算典型相关 \(\rho_{b1}\ge\cdots\ge\rho_{bd_b}\)。典型相关取非负相关系数本身，不取平方值。
3. 若估计维度不等于 \(d_b\)、任一矩阵列秩小于 \(d_b\)，或典型相关所需协方差为奇异且预先固定的算法不能得到全部 \(d_b\) 个相关，则令 \(r_b=0\)；否则令 \(r_b=\min_j\rho_{bj}\)。不得只报告最大的第一典型相关。
4. 情景级统计量固定为
   \[
   L=\max\left\{0,\ \bar r-1.96\,s_r/\sqrt{B}\right\},
   \]
   其中 \(\bar r\) 和 \(s_r\) 分别是 \(r_b\) 在独立模拟重复间的均值与样本标准差。仅当 \(L\ge0.80\) 时，该情景的连续状态恢复达标。
5. 情景适用性必须在模拟结果查看前列明。正确生成且要求恢复连续状态的情景必须适用；错设情景是否要求恢复须由其预设科学目的决定，但不能在看到结果后移除适用性。错设情景另有“识别失配并停止解释”的既定判定，不能以连续相关较高代替。

这个定义特意比“第一典型相关至少 0.80”更保守：只恢复一个强方向而遗漏其余真实维度时不会通过。若某个维度使标准未达到，应执行 dossier 已规定的合并、删除或降级动作，而不能事后改成第一典型相关。

## 直接相关的状态角色澄清

当前 dossier 同时使用了三类“状态”：规则直接定义的发病后互斥临床状态、连续潜在生理状态 \(X(t)\)，以及复杂候选可能包含的离散潜在机制或区段。恢复表中的“离散调整兰德指数或连续……典型相关”没有在该表内把统计量逐一绑定到这三类对象，存在把临床结局标签与潜在机制标签混用的风险。

在上述工作假设下，角色必须固定为：

- 典型相关只评价已知模拟真值的连续 \(X(t)\) 与其估计后验均值；
- 调整兰德指数只评价生成的离散潜在机制或区段与估计离散标签，并在计算前完成标签置换对齐；
- 发病后互斥临床状态是按 SOFA、器官支持、死亡、出院和转院规则生成的临床端点，不以这两个潜在状态恢复统计量评价；其性能按多状态占用、转移概率、校准和既定临床任务指标评价。

若复杂候选没有离散潜在机制，调整兰德指数不适用，不得把规则生成的临床端点临时改作其替代对象。这个角色绑定与连续统计量定义应由科学负责人写入模拟规范和判定代码；编辑写作者只能逐字转述经确认的规范，不能在“第一典型相关”“最小典型相关”、维度处理或状态对象之间自行选择。

## 方法学判定

- 端点/指标状态：现有短语未充分操作化，需按上述假设固定后方可执行。
- 数据—方法关系：对预设模拟真值与估计后验均值可计算；真实临床资料中没有潜在状态真值，因此该绝对恢复统计量只适用于模拟或半合成恢复，不得被表述为真实数据中的状态识别证明。
- 最小分析路线：存在。采用上述保守统计量进行复杂候选准入；未达到标准时执行预设的合并、删除或简单表征降级路线。
- 停止条件：若月 7 前未由指定负责人确认并冻结唯一计算定义，或定义是在查看模拟结果后才选择，则停止复杂候选的连续状态恢复判定与结构晋级；不停止已经独立成立的线性、多状态或仅预测路线。
