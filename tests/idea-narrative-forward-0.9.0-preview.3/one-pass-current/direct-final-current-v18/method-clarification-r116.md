# 条件性随机试验分析的方法学澄清

```yaml
review_id: method-clarification-r116
reviewer_skill: methodology-statistics-preflight
reviewer_instance_id: methodology-statistics-preflight-r116-20260720
workflow_id: idea-narrative-forward-0.9.0-preview.3
round_id: r116
input_artifact_ids:
  - idea-dossier-v052
input_versions:
  - v052
files_read:
  - AGENTS.md
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
  - R116-F1
unresolved_issues:
  - 试验统计负责人尚须在治疗组比较前书面确认唯一主要估计目标、并列处理和分层权重。
```

## 审查范围与条件性结论

本澄清只审查 dossier 第 281 行与第 363 行所述有前置条件的随机试验次要分析，不判断该分析是否必然开展，也不评价主体研究的价值或总体可行性。

该分析可以在下述明确且有界的工作假设下继续准备。继续始终以 dossier 已列前提为条件，包括阶段 II 达到合取标准、相应试验个体资料获准使用，以及随机化、分析集、中心或分层因素、实际访视时序和生存或住院语义得到核验。两项试验必须分别分析，不合并估计。

## R116-F1：当前两个术语不能视为已定义的同义表达

第 281 行的“概率指数或胜率”没有给出“胜率”的数学定义；第 363 行则明确要求预先固定“概率指数并列规则”。在本结局中，访视前死亡者同处最差层，访视前存活出院者同处最有利层，因此并列不是可忽略的边缘情形，而是结局构造产生的结构性组成部分。

令同一随机化层内独立抽取的一名试验组参与者和一名对照组参与者的有序访视结局分别为 \(Y_1\) 和 \(Y_0\)，且数值或次序越高表示越有利。记

\[
W=P(Y_1>Y_0),\qquad L=P(Y_1<Y_0),\qquad T=P(Y_1=Y_0).
\]

- 半权重并列的概率指数是 \(W+\tfrac12T\)。
- 若“胜率”指严格胜概率，则它是 \(W\)，在 \(T>0\) 时不等于概率指数。
- 若“胜率”实际意指胜负比，则它是 \(W/L\)，与概率指数具有不同尺度和解释；即使没有并列，两者也只是可相互转换，而不是同一个数值估计目标。

因此，当前表述构成主要对比量歧义，不能由后续写作者把“概率指数”与“胜率”自行当作同义词。第 363 行对概率指数并列规则的明确要求，为选择概率指数作为保守的唯一主要估计目标提供了 dossier 内部依据。

## 唯一主要估计目标

**名称：分层标准化概率指数（并列各计半分）。**

对每项试验单独定义随机化层 \(S=s\)。这些层必须使用原随机化资料中经核验的中心或分层因素，不得依据治疗结果事后创建、合并或选择。该试验的主要估计目标为

\[
\theta_{PI}
=\sum_s \omega_s
\left\{
P(Y_1>Y_0\mid S=s)
+\tfrac12P(Y_1=Y_0\mid S=s)
\right\},
\]

其中，\(Y_1\) 与 \(Y_0\) 是从同一随机化层、该试验预先指定的目标分析集中分别独立抽取的试验组和对照组参与者的实际第 7 日或第 8 日有序访视结局。\(\omega_s\) 为该目标分析集中各随机化层的合并组样本比例；权重只使用合并治疗组的层成员数，在查看任何组间结局比较前固定。若原随机化资料不能核验所需的中心或分层因素，则不得改用事后层或忽略设计因素，而应停止新的访视结局主要比较。

有序访视结局按 dossier 已定义的临床层级构造：

1. 访视前死亡为最差层；死亡与死亡比较记为并列。
2. 访视时存活住院者按一维可观测代理比较；代理值越低越有利。两人的代理值相同则记为并列。
3. 访视前存活出院为最有利层；存活出院与存活出院比较记为并列。

试验组结局更有利记为胜，对照组结局更有利记为负，并列对两组各计半分。\(\theta_{PI}=0.5\) 表示没有随机优越性；\(\theta_{PI}>0.5\) 表示随机分配至试验组更有利；\(\theta_{PI}<0.5\) 表示对照组更有利。估计、区间和检验须保留原随机化的中心或分层结构。该定义分别应用于 EXIT-SEP 和 XBJ-SCAP，不产生跨试验合并效应。

第 281 行主要对比中的“或胜率”应删除。若以后将严格胜概率 \(W\) 或胜负比 \(W/L\) 明确定义并保留，只能作为预先规定的次要或敏感性分析，不能替换上述主要估计目标，也不能在查看治疗组结果后决定是否报告。

## 有界工作假设与核验责任

```yaml
assumption_id: WA-R116-PI
unconfirmed_detail: 第 281 行“胜率”是否原本意指概率指数、严格胜概率或胜负比。
working_assumption: 每项符合启动条件的试验均以“分层标准化概率指数（并列各计半分）”作为新访视有序结局的唯一主要估计目标；主要方法中删除“或胜率”。
basis_for_planning: 有序结局、方向和结构性并列已经给出；第 363 行明确要求概率指数并列规则；该选择不改变结局层级、主体研究问题或条件性从属地位。
impact_if_false: 不开展或不晋级相应试验的新访视主要比较；在治疗组结果保持不可见时修订估计目标并接受新的独立方法学审查。不得事后切换为严格胜概率或胜负比。主体阶段 I–II 路线和原试验终点复现不受影响。
verification_needed: 书面确认公式、方向、并列各计半分、目标分析集、原随机化中心或分层因素及合并组层权重，并与原始病例报告表、统计分析计划、随机化资料和数据字典核对。
verification_point: 每项试验完成核心语义核验之后、分析计划和代码冻结之前，且必须早于任何治疗组比较。
affected_design_component: 有前置条件的随机试验次要分析中的新访视有序结局主要对比。
owner: 每项试验的具名统计负责人；项目负责人负责记录确认，独立方法学审查者负责复核。
deadline: 每项试验分析计划和比较代码冻结前，且早于治疗标签用于任何组间结局计算。
```

若到该期限仍未确认，后果不是任选一种“胜率”定义继续，而是停止相应的新访视结局主要分析，仅保留 dossier 已允许的原终点复现或数据审计记录。
