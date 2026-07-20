---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-r006
review_id: narrative-review-I01-001-r006
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: idea-narrative-assessor-r006-fresh-20260720
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: r006
input_artifact_ids:
  - idea-dossier-I01-001-v005
input_versions:
  - v005
input_dossier:
  artifact_id: idea-dossier-I01-001-v005
  version: v005
  path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v005.md
reader_handoff:
  artifact_id: embedded-reader-handoff
  version: embedded
  path: null
files_read:
  - 03_ideas/nodes/I01-001/dossiers/idea-dossier-v005.md
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: minor_narrative_revision
findings:
  - finding_id: NAR-001
    severity: minor
    category: progressive_disclosure_and_repetition
    dossier_locator:
      section_heading: Research question, objectives, and core hypothesis
      subsection_heading: null
      content_anchor: "**Confirmatory family.** 数据资格和最小模型可辨识性是进入外部确认性评价前必须实证满足的条件。"
    observed_evidence: >-
      主问题之后立即出现 D_kc、Delta_k、max-t 重采样、单侧上置信界和 Holm 判定规则的完整技术说明，目标与核心假设要到这段之后才出现；同一套推断程序又在“Research design and methods”下的“Multiplicity and overall interpretation”中完整说明。
    current_reader_effect: >-
      读者在尚未完成“问题—目标—正向假设”的第一遍理解前就必须处理推断细节，并需要在后文判断两处说明哪一处是完整的方法说明。
    target_function: >-
      先连续呈现主问题、目标和核心假设，再在方法部分保留唯一完整的任务级推断与多重性说明；本节只保留识别四项确认性任务所必需的简要关系。
  - finding_id: NAR-002
    severity: minor
    category: definition_order_and_concept_burden
    dossier_locator:
      section_heading: Title, summary, audience, and positioning
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary 末尾的“状态表示的跨库可重复性”"
    observed_evidence: >-
      开篇摘要以及随后结构化摘要、研究问题和设计理由先后使用“状态表示的跨库可重复性”“临床锚定状态的跨库可分离性”和“状态迁移”，但这些表达的具体含义直到“External application and state-transfer diagnostics”才说明；全文同时使用“状态转移”表示患者病程内的变化。
    current_reader_effect: >-
      尚未读到方法部分的临床读者或跨学科读者可能把跨数据库的状态迁移与患者病程内的状态转移混为一谈，也无法在第一遍阅读时准确理解这一核心外部验证目标。
    target_function: >-
      在首次出现处以面向声明读者的概念层次界定跨数据库状态迁移或可重复性，并明确它不同于患者病程内的状态转移；后文继续承担指标、阈值和处置规则的完整方法说明。
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

该 dossier 的主叙事已经完整：背景说明动态且受处置和测量影响的脓毒症病程，现状概括已有局部模型和跨库性能问题，缺口聚焦于一个预先限定且覆盖全病程的统一表示，意义说明共享表示对四项任务及失效边界的价值，设计理由则把数据资格、可辨识性、冻结开发和外部应用连成可理解的顺序。标题、摘要、研究问题、目标、预期产物和贡献框架指向同一个研究对象与四项任务。

当前不需要重构主要论证。两处局部编辑仍会妨碍第一遍阅读：正式推断细节过早插入研究问题与目标之间，并在方法部分再次完整出现；跨数据库的状态迁移或可重复性作为核心目标在开篇出现，却晚于首次使用才获得概念界定。因此决定为 `minor_narrative_revision`。

本评估仅判断读者能否沿 dossier 的表达顺序理解研究问题和设计关系，不判断科学正确性、新颖性、影响、可行性、证据强度或主张强度。

## Findings

### NAR-001 — 推断细节打断正向研究主线

“Research question, objectives, and core hypothesis”先给出主问题，随后用一整段公式和检验程序说明确认性家族，之后才列目标和核心假设。该程序在“Multiplicity and overall interpretation”中还有一处更完整的技术说明。两处内容并非缺失，而是披露顺序和完整说明位置不够集中。修订应保留全部四项假设、比较方向、患者级汇总、多重性控制和通过规则，但让读者先连续完成主问题、目标与核心假设的理解。

### NAR-002 — 跨库状态迁移晚于首次使用才被界定

开篇把状态表示的跨库可重复性列为主要产出，后续又用临床锚定状态的跨库可分离性和状态迁移表述这一目标；与此同时，状态转移用于描述同一患者的病程变化。完整操作规则放在方法部分是合适的，但首次出现处还缺少一个简短的概念区分。修订只需补足读者理解所需的定义顺序，不应提前搬入距离、占用、合并或拆分等全部技术规则。

## Preserved strengths

- 背景、现状、缺口、意义和设计理由均非空且相互区分，缺口到设计的连接明确。
- 标题、完整构想摘要、研究问题、目标、核心假设、预期产物和贡献主张保持同一全病程模型及四项任务，没有核心对象漂移。
- 开篇已解释动态状态模型、全病程、受约束和外部验证，方法部分再逐步展开人群、状态空间、比较模型、四项任务和外部应用。
- 工作包、实施要点、证据链、必需分析、预期产物和主张支持表各自承担计划、实现、追踪、验收、交付和审计功能，不应因表面相似而合并为一个替代部分。
- “Limitations and boundary conditions”是完整限制与边界的集中位置；其他位置的局部边界直接服务于相邻的任务定义或解释，应在修订时保持这种克制。
- 随机试验和动物研究被清楚置于核心研究之外，并由一个专门小节说明条件，不应在此次局部修订中扩大其篇幅或地位。

## Handoff

具体操作见配套的 `narrative-repair-plan-r006.yaml`。
