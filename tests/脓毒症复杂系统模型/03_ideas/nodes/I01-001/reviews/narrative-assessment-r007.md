---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-r007
review_id: narrative-review-I01-001-r007
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-idea-narrative-assessor-r007
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: r007
input_artifact_ids:
  - idea-dossier-I01-001-v006
input_versions:
  - v006
input_dossier:
  artifact_id: idea-dossier-I01-001-v006
  version: v006
  path: tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
reader_handoff:
  artifact_id: embedded-reader-handoff
  version: embedded
  path: null
files_read:
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: minor_narrative_revision
findings:
  - finding_id: NAR-001
    severity: minor
    category: reader_reasoning_sequence
    dossier_locator:
      section_heading: "Background, current state, gap, significance, and rationale"
      subsection_heading: "Background"
      content_anchor: "因而本研究把患者病程表示为一个开放的动态临床系统"
    observed_evidence: >-
      Background 的末句已经给出本研究选择的开放动态系统表示及其组成，随后才进入
      Current state、Gap 和 Significance；Rationale 又再次承担这一设计选择的说明。
    current_reader_effect: >-
      读者在了解既有研究和未解决问题之前先遇到拟议方案，需要在读到 Gap 后回头重释
      Background 末句，也使 Background 与 Rationale 的功能边界变得模糊。
    target_function: >-
      Background 只建立脓毒症病程随时间变化且受治疗与测量过程影响的问题背景；选择
      开放动态表示的理由在 Gap 和 Significance 之后首次完整出现于 Rationale。
  - finding_id: NAR-002
    severity: minor
    category: progressive_disclosure_and_definition_order
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary 中首次出现“持续恢复”"
    observed_evidence: >-
      “持续恢复”在摘要、Significance、研究问题和目标中承担任务二的核心结局功能，但其
      区别于存活出 ICU 的 24 小时操作性含义直到 Research design and methods 的
      Unified full-course population, time axis, and state space 才出现。
    current_reader_effect: >-
      面向临床、系统科学、人工智能和方法学的混合读者会先按日常含义理解这一中央结局，
      到方法部分才发现它是一个特定复合事件，因而需要回读前面的任务与意义陈述。
    target_function: >-
      在首次读者可见使用处提供足以区分持续恢复、存活出 ICU 和短暂改善的简短释义，
      同时把完整操作定义保留在方法部分。
  - finding_id: NAR-003
    severity: minor
    category: terminology_burden_and_progressive_disclosure
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "“动态状态模型”在本研究中指"
    observed_evidence: >-
      开篇定义段在读者进入 Structured abstract 和问题背景前，同时展开状态停留与转移、
      完整冻结对象、跨数据库诊断所用特征与分布比较，并定义后文不再承担论证功能的
      “人体开放复杂巨系统”标签；跨数据库诊断的完整操作说明在方法部分另有权威位置。
    current_reader_effect: >-
      混合读者必须在尚未形成问题框架时一次吸收多个不同层级的概念，其中部分细节要到
      方法部分才有用途，单次出现的标签还增加了不产生后续回报的术语负担。
    target_function: >-
      开篇只保留理解题目、摘要和核心问题所必需的读者级定义；跨数据库诊断的特征与判定
      细节集中在对应方法小节，开放系统的科学前提用 Background 中已经存在的自然科学
      描述表达，而不额外引入未继续使用的标签。
  - finding_id: NAR-004
    severity: minor
    category: section_function_and_repeated_caveat
    dossier_locator:
      section_heading: "Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Working assumptions"
      content_anchor: "任务三的固定操作化说明"
    observed_evidence: >-
      Working assumptions 先以“用户提出的”准则解释任务三，随后明确说明该内容“不是工作
      假设”；同一操作定义和“不验证潜在生理状态”的边界已经分别由 H3、结果依赖解释和
      Limitations and boundary conditions 承担。
    current_reader_effect: >-
      该段既不履行工作假设小节的功能，又把科学设计写成对产出过程的回应，并让同一防御性
      边界出现多个近似权威位置，打断 WA-01 与 WA-02 的阅读连续性。
    target_function: >-
      Working assumptions 只呈现尚待确认且会影响推进方式的假设；任务三的操作理由集中在
      H3，认识边界由结果解释和限制部分各自保留其必要的局部功能，不再以产出过程表述。
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

判定为 `minor_narrative_revision`。主阅读路线已经成立：Background 说明脓毒症病程的时间依赖性及治疗、测量与结局之间的相互关系；Current state 概括可用纵向数据库和相邻建模路线；Gap 提出统一病程表示、观测过程区分、四任务外部评价与状态表示诊断尚未被共同回答；Significance 说明获得支持和未获支持结果各自能提供的病程与数据边界；Rationale 则把资格验收、开发期恢复诊断、冻结模型和外部评价连接成回应上述缺口的顺序。无需重构这条主路线。

题目、完整构想摘要、结构化摘要、主要研究问题、目标、核心假设和贡献框架均指向同一研究对象、同一低维受约束全病程模型、一个开发数据库、一个异质外部数据库、四项任务以及跨数据库状态表示诊断。积极主张与限制总体保持平衡，完整限制也有明确的集中位置。现有问题主要来自一处方案先于缺口出现、一项核心结局定义偏晚、开篇概念负担略重，以及任务三说明在不合适的小节重复；这些均可通过局部移动、定义和合并解决。

## Findings

### NAR-001 — Background 提前承担了 Rationale 的方案选择功能

Background 的前两句有效建立了临床问题，但末句由“因而本研究把……”转入拟议状态表示。由于 Current state 与 Gap 尚未出现，读者还没有判断该表示为何是合适回应的依据。将这项设计选择留到 Rationale，并让 Background 以动态病程及观测、治疗依赖这一问题前提收束，即可恢复 Background → Current state → Gap → Significance → Rationale 的单向推进。

### NAR-002 — “持续恢复”的技术含义晚于多次核心使用

“持续恢复”不是普通叙述性结果，而是任务二中的特定复合事件，并且不等同于存活出 ICU。当前完整定义虽存在，却在多个摘要性和论证性使用之后。首次使用处需要一个不取代方法定义的简短读者级释义，使前面的摘要、意义与研究问题可以在各自层级独立理解。

### NAR-003 — 开篇定义段混合了读者入口与方法细节

对“动态状态模型”“全病程”“受约束”和“外部验证”的早期解释有助于跨学科读者，但同一段继续展开跨数据库诊断的具体特征与分布比较，并引入后文不再使用的“人体开放复杂巨系统”标签。这些内容没有在开篇承担新的读者功能。保留入口定义、把诊断细节留在其方法小节，并用 Background 已有的治疗—测量—环境交互描述承载开放系统前提，可降低概念负担而不损失科学内容。

### NAR-004 — Working assumptions 中的任务三段落既重复又不符合小节功能

该段自身声明任务三的固定操作化不是工作假设，因此无法回答该小节承诺的“尚待确认条件”。“用户提出的”也把科学选择系于产出过程，而不是直接说明无潜在状态金标准这一科学理由。H3 已经是操作定义的自然权威位置，结果模式表和限制部分又分别承担成功解释与认识边界；在这些位置保留各自必要内容并移除 Working assumptions 中的重复说明，可恢复小节功能和权威位置。

## Preserved strengths

- 五段式论证功能均存在，Gap 到 Rationale 的对应关系清楚，Significance 同时说明正向结果与不支持结果的读者意义。
- 题目、摘要、研究问题、目标、假设、预期产出和贡献使用兼容的核心要素，没有把任务三误写为潜在生理状态验证。
- Research design and methods、Key techniques and implementation、Evidence chains、Required analyses and evidence、Expected outputs 以及 Claim-Support 表分别履行方法规范、实现对象、证据血缘、验收分析、交付物和主张审计功能；这些必需功能不应在修订中被合并删除。
- Limitations and boundary conditions 是完整限制的集中位置；修订应保留这一权威位置，并仅在其他部分保留直接支持相邻推理的最小边界。
- 条件性随机试验和动物研究被明确置于核心研究之外，未改变题目、主要问题或 12–18 个月核心交付的身份。

## Handoff

See the paired `narrative-repair-plan-r007.yaml` for executable actions.
