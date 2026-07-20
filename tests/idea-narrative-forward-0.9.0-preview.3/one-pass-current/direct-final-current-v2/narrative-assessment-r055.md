---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-r055
review_id: narrative-review-r055
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-narrative-v035-r055
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r055
input_artifact_ids:
  - idea-dossier-I01-001-v035
  - reader-handoff-forward-001
input_versions:
  - v035
  - v001
input_dossier:
  artifact_id: idea-dossier-I01-001-v035
  version: v035
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v2/idea-dossier-v035.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v2/idea-dossier-v035.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: major_narrative_revision
findings:
  - finding_id: NAR-001
    severity: major
    category: summary_burden_and_progressive_disclosure
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary 与 Positioning and contribution frame 两个条目"
    observed_evidence: "开篇一句同时承载研究对象、全病程范围、知识约束与不确定性、文献和专家先验、双数据库、模拟、隔离外部验证、24 个月期限、两项条件性 RCT 分析及非因果边界；紧接的定位条目又列出形成增量贡献所需的全过程条件。"
    current_reader_effect: "跨学科读者尚未获得问题—缺口—设计关系，就必须同时记住主研究、验证资格、延后扩展和解释边界，读完一遍后难以用简洁语言复述积极的主要目标与贡献。"
    target_function: "开篇先给出问题边界、阶段 I–II 的主要目标和积极贡献，再以一个可独立理解的短句预告阶段 III；端点分支、资格标准和失败解释留到相应设计章节。"
  - finding_id: NAR-002
    severity: major
    category: pervasive_repetition_and_narrative_balance
    dossier_locator:
      section_heading: "Research question, objectives, and core hypothesis"
      subsection_heading: "Primary research question"
      content_anchor: "研究问题第（3）项从“在阶段 II 达到跨数据库判定标准后”开始的条件性 RCT 分支"
    observed_evidence: "投影观测摘要端点与独立 SOFA 临床状态端点的选择逻辑及其限制，先后在结构化摘要、主要问题、目标 4、工作包、研究设计、证据链、必需分析、计划输出、贡献层级、标题与定位主张表、限制及风险中反复展开；不少位置重复端点资格、分开报告和不支持整个模型等同一组信息。"
    current_reader_effect: "延后且条件性的阶段 III 在阅读篇幅和出现频率上接近阶段 I–II 主研究，读者需要反复判断每次表述是否增加新功能，24 个月主线及其阶段性因果顺序因而失焦。"
    target_function: "把完整的 RCT 资格、映射、端点选择和解释边界集中在研究设计；其他必需章节仅保留各自合同功能所需的最小陈述，使阶段 I–II 明确保持为主要路线、阶段 III 明确保持为延后扩展。"
  - finding_id: NAR-003
    severity: minor
    category: distributed_limitations_and_defensive_repetition
    dossier_locator:
      section_heading: "Contribution, innovation, impact, application, and closest-work comparison"
      subsection_heading: "贡献与证据层级"
      content_anchor: "首段末句“不构成新算法或全球首次”及证据层级表末行的否定性边界"
    observed_evidence: "非因果、非机制、非控制、非数字孪生、非临床工具、非全球首次等边界已在多个前置和中段章节反复列举，之后又由“限制与边界条件”完整汇总；其中若干重复并不直接解释相邻设计选择。"
    current_reader_effect: "必要边界的高频重述挤压了研究要回答什么、为何值得做以及能贡献什么的正向论证，并使读者难以辨认唯一完整的限制说明位置。"
    target_function: "以“限制与边界条件”为唯一完整限制权威；其他位置只在省略会扭曲相邻研究问题、方法选择或允许解释时保留一条自包含的最小边界，不保留限制清单或指向该权威位置的交叉引用。"
  - finding_id: NAR-004
    severity: minor
    category: section_function_and_repetition
    dossier_locator:
      section_heading: "Key techniques and implementation"
      subsection_heading: null
      content_anchor: "编号 1–10 的技术与实施列表"
    observed_evidence: "该列表再次概述双时间标签、G1 审计、变量角色、简单模型、锚定、缺失、外部隔离、RCT 映射、不确定性和负向控制，而这些内容已在前一节研究设计中逐项展开；列表主要重复规则，较少说明其独立的实施功能或交付接口。"
    current_reader_effect: "读者在进入证据链之前需要重读一遍方法目录，却难以判断本节相对研究设计新增了什么，产生停滞而非有用的实施层递进。"
    target_function: "保留本节及十类实施内容，但将其压缩为实施层索引：每项只说明将实现或产出的具体对象及其与后续证据链的接口，不再复述前节的完整资格、阈值和解释边界。"
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

结论为 `major_narrative_revision`。本稿的五段读者推理链是完整的：背景说明脓毒症发病时刻和数据库标签并不唯一；当前状态归纳多状态、动态表型、状态空间、跨数据库验证和 RCT 次要分析的既有能力；缺口明确提出同一候选模型在全病程、结构恢复、跨数据库稳定性和稀疏试验观测联系上的未解问题；重要性解释这些不足如何妨碍可解释性与可迁移性判断；设计理由再把双时间、过程角色分离、预设模拟、隔离外部测试和条件性试验分析逐一连回缺口。标题、摘要、问题、目标、核心假设、五条证据链与贡献定位也指向同一个研究对象，没有发现核心元素漂移。

主要叙述障碍发生在这条链之外。开篇摘要把主研究、技术限定、失败分支和解释边界压入同一层级；其后，条件性 RCT 分支和否定性边界在多个必需章节反复完整出现。单个段落大多准确，但全稿的披露顺序和篇幅分配使阶段 III 看起来几乎与 24 个月阶段 I–II 同等中心。修复需要跨章节归位和系统去重，不能只靠局部增补，因此判为重大叙述修订。

## Findings

### NAR-001：开篇摘要承载过多条件

“One-sentence complete-Idea summary”在读者尚未看到问题与缺口时，要求其同时处理多个技术属性、三个阶段、两类数据和两种解释边界；后续定位条目又继续罗列贡献成立的全部条件。这不是术语是否标准的问题，而是信息出现顺序和单次记忆负担的问题。开篇应先让读者说清“要解决什么、24 个月内做什么、可能贡献什么”，随后再预告条件性扩展。

### NAR-002：阶段 III 分支在全稿中反复展开

条件性 RCT 分析是核心身份的一部分，不能删除；证据链、必需分析、计划输出和主张审计也各有独立合同功能，不能合并为一个替代表格。问题在于这些章节多次重复端点选择的操作定义、资格条件和失败解释，而不是只完成各自功能。完整逻辑应由研究设计权威承载；其他章节分别保留问题、目标、时序、输入—处理—输出—支持、验收证据、计划产物或主张范围所需的最小内容。

### NAR-003：限制权威之外仍有多组防御性清单

观察性关系不等于因果、试验端点不验证整个模型、项目不构成数字孪生或临床工具等边界具有科学必要性。若它们直接限定相邻目标量或结果解释，应在当地保留一条自包含的边界；但把同一组否定性边界反复列在定位、核心假设、贡献、主张表和风险之前，会让防御超过动机。完整限制应只在“限制与边界条件”出现一次，其他位置不应留下限制清单或交叉指针。

### NAR-004：“Key techniques and implementation”未形成新的实施层

本节的十项内容与前一节研究设计高度对应，当前主要发挥回顾作用。必需标题与十类内容应保留，但每项应转为可执行对象或可审计产物的简洁索引，例如标签生成、审计矩阵、角色字典、模型比较顺序、外部数据隔离记录或端点映射实现，而不再复述完整阈值与不支持的解释。

## Preserved strengths

- “Background—Current state—Gap—Significance—Rationale”五个小节各自完成承诺的功能，且设计理由逐项回应缺口。
- 标题、摘要、主要问题、四项目标、核心假设和五条证据链保持同一研究身份：脓毒症发病前—首次发病—发病后—结局连续体、公共重症监护数据库、条件性 RCT 证据以及患者—时间状态与状态转移。
- 五条证据链均保留 Input、Method / analysis / processing、Output 和 Supports，且承担可审计血缘功能，不应因去重而删除或合并。
- 阶段 I–II 与阶段 III 的时间先后、外部测试隔离和失败分支在研究设计中表达清楚；修订应保留这些实质内容。
- “Expected outputs, falsification criteria, and interpretations”中的输出、证伪与解释矩阵功能彼此不同，适合保留为结果解释的集中位置。

## Handoff

See the paired `narrative-repair-plan-r055.yaml` for executable actions.
