---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-r056
review_id: narrative-review-I01-001-r056
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh_baseline_narrative_r056
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r056
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - reader-handoff-forward-001
input_versions:
  - v003
  - v001
input_dossier:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: major_narrative_revision
findings:
  - finding_id: NAR-001
    severity: major
    category: reader_reasoning_chain
    dossier_locator:
      section_heading: "Background, current state, gap, significance, and rationale"
      subsection_heading: null
      content_anchor: "最近近邻使“单个模块新颖”不可成立。"
    observed_evidence: "本节清楚说明了脓毒症时间演化、EHR 标签歧义、数据库异质性和已有方法，但所谓缺口主要表述为尚未找到把若干模块合在一起的代表性架构；随后直接转入观察性偏倚边界和阶段 III 投影门，没有单独说明仍无法回答的科学或证据问题、解决它对目标读者的价值，以及为何主体设计正好回应这一问题。"
    current_reader_effect: "读者能够复述已有模块和项目边界，却难以在不借助后续方法章节的情况下回答“尚缺什么证据、为什么值得补、主体设计为何合适”这三个连续问题。"
    target_function: "用彼此区分且前后相接的段落完成背景、当前状态、未解决证据缺口、意义和设计理由五段链，并把 novelty positioning 与技术门槛留给各自承担该功能的章节。"
  - finding_id: NAR-002
    severity: major
    category: progressive_disclosure_and_reader_baseline
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary"
    observed_evidence: "一句式摘要在完成正向研究目的之前同时装入双库审计、绝对模拟恢复、未触碰检验、冻结观测投影、RCT 失败分支和多类禁止解释；Structured abstract 又继续使用 proper score、zero update、观测层更新等跨学科读者未必共享且尚未解释的术语。G1、as-of、投影可观测摘要等关键概念也在首次承担推理作用后才由后文细化。"
    current_reader_effect: "声明的跨学科读者需要先解析项目特定标签和多层例外，才能找出主体问题与主要贡献，并须回到后文才能解释前面的中心陈述。"
    target_function: "先用目标读者可直接理解的语言交代主体问题、24 个月阶段 II 目标和贡献，再以最少必要边界预告条件性阶段 III；核心跨学科术语在首次承担推理作用时得到简明定义。"
  - finding_id: NAR-003
    severity: major
    category: conditional_component_weight
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "仅在阶段 II、试验语义和冻结观测投影门均通过后"
    observed_evidence: "24 个月最低交付之外的阶段 III RCT 分支进入标题、长摘要、结构化摘要、背景、主问题、目标、工作包、技术清单、证据链、计划产物、贡献阶梯、Claim-Support 表和风险矩阵；其中资格、投影失败、SOFA 替代和禁止解释的完整逻辑在多个位置反复展开，而不是只在技术权威位置完整说明。"
    current_reader_effect: "一个条件性下游组件获得与主体阶段 I–II 相当的叙述权重，使读者难以判断研究的最低成功对象，并显著增加理解主问题之前的概念负担。"
    target_function: "在“Conditional trial-observation projection and independent fallback”保留阶段 III 的完整资格、操作、替代和解释逻辑；问题、目标、证据链、产物与 Claim-Support 仅保留各自合同功能所需的最小陈述。"
  - finding_id: NAR-004
    severity: major
    category: caveat_saturation_and_limitations_authority
    dossier_locator:
      section_heading: "Evidence chains"
      subsection_heading: "Evidence chain: 可用性时钟、风险集与互斥病程"
      content_anchor: "Limits and failure conditions"
    observed_evidence: "五条证据链都在 Input、Method、Output、Supports 之后增加独立的 Limits and failure conditions；同类边界又出现在摘要、背景、非假设、方法、技术、必需分析、解释矩阵、贡献、Claim-Support 和风险矩阵。第 14 个 H2 已具有完整限制、风险、替代和停止条件功能，但当前不是唯一完整权威位置。"
    current_reader_effect: "正向论证被反复的失败与禁止性陈述打断，读者难以判断哪个表述是完整权威版本，也难以区分必要的局部科学边界与重复防御。"
    target_function: "使“Feasibility, resources, risks, alternatives, and stop conditions”成为唯一完整限制与假设权威位置；删除五条证据链的独立限制字段，保留每链的 Input、Method / analysis / processing、Output、Supports，并仅在紧邻设计选择且省略会造成误解时保留自足的最小局部边界。"
  - finding_id: NAR-005
    severity: major
    category: section_function_failure
    dossier_locator:
      section_heading: "Key techniques and implementation"
      subsection_heading: null
      content_anchor: "As-of 标签引擎"
    observed_evidence: "本节的十项内容主要再次概括前一方法章节的标签、审计、基线、锚定、缺失、外部分割、RCT 投影、不确定性和负向控制；除少数“引擎”“审计器”称谓外，没有系统说明将实现哪些对象、记录、接口、输入输出和可复现边界。"
    current_reader_effect: "标题承诺的 implementation 功能无法由本节独立获得，读者只能回到方法章节推断实际实现结构，同时再次阅读已经出现的科学规范。"
    target_function: "把本节改为可执行实现图谱，逐项命名实现对象、输入、输出、持久记录、接口和版本/冻结边界；完整方法规范仍由 Research design and methods 承担。"
  - finding_id: NAR-006
    severity: major
    category: repetition_and_navigation
    dossier_locator:
      section_heading: "Research content and work packages"
      subsection_heading: "Work packages and minimum route"
      content_anchor: "最低顺序固定为"
    observed_evidence: "恢复阈值、外部医院分区与更新层级、RCT 两级分支以及失败后果在日期门、工作包、最低顺序、详细方法、技术清单、五条证据链、必需分析、计划产物、伪证标准、解释矩阵和风险矩阵中多次重述，常带有足以再次成为完整规范的细节，而不仅是该章节所需的角色性摘要。"
    current_reader_effect: "读者难以分辨时间表、方法规范、实现、证据追踪、验收、产物、解释和风险各自的权威功能，并需反复比较近似版本以确认是否存在差异。"
    target_function: "为各 H2 保留唯一章节功能：时间表只说明顺序与交付，方法只说明完整科学规范，实现只说明对象与接口，证据链只说明四项可审计链，必需分析只说明验收证据，产物只说明交付与解释，贡献与 Claim-Support 只说明主张，限制章节只说明风险、替代与停止条件。"
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

结论为 `major_narrative_revision`。当前 dossier 已包含完整研究对象、相互兼容的标题—问题—目标—输出—主张元素，也提供了可执行的阶段设计；问题不在科学内容缺失，而在读者路线。开篇先承担大量限定、术语和条件分支，背景段落把缺口主要写成组合式定位，尚未明确闭合“当前证据不能回答什么—为什么这对目标读者重要—为何主体设计是合适回应”。其后，阶段 III、失败条件和同一方法规范在多个必需章节中重复展开，使主体 24 个月阶段 I–II 路线失去应有的叙述重心。

修订需要重新分配章节功能、恢复渐进披露并建立唯一技术和限制权威位置，因此不是局部润色即可解决。核心科学身份、证据基础、推断单位和方法边界均可在不改变的前提下完成这项编辑修复。

## Findings

### NAR-001 — 五段推理链在缺口、意义和理由处未闭合

背景和当前状态有充分材料：读者能理解脓毒症标签的时间问题、数据库差异、已有纵向模型及观察性偏倚。不过，本节把“缺口”主要写成未发现一个恰好贯通五层的代表性架构，并立即说明项目的可辩护组合空间。这是定位论证，不足以独立回答仍缺少哪一种可检验的科学或证据能力。意义也没有作为“若补上该证据，重症研究、临床流行病学与系统辨识读者能作出什么更可靠判断”的正向功能出现；设计理由则分散在状态—行动—观察边界、绝对恢复、跨库检验和 RCT 投影规则中。修订应把这五个功能写成顺序清楚的主干，而不是让方法和防御性限定替代意义。

### NAR-002 — 开篇概念负担超过 reader handoff 的共同基线

一句式摘要准确但不可渐进读取：在读者尚未获得问题与缺口时，就要求同时处理“候选动态系统表征”“绝对恢复”“真正未触碰”“冻结观测投影”“death-ranked SOFA”等概念和多个失败分支。部分术语对某一专业熟悉，但 reader handoff 明确不允许假设每位读者掌握所有参与学科的隐含词汇。需要先给出可复述的正向目标，再逐步引入只有在后续设计选择中才必要的概念，并在首次承担推理作用时给出简明定义。

### NAR-003 — 条件性阶段 III 挤占主体研究

阶段 III 被明确排除在 24 个月最低交付之外，却在几乎所有核心叙述位置重复完整分支逻辑。重复提及本身并非问题：主问题、目标、证据链、产物和 Claim-Support 都确实需要记录它们与阶段 III 的关系。问题是这些位置反复解释资格、投影、失败替代和禁止解释，使条件性组件看起来像与阶段 II 同等的研究核心。应保留一个完整技术权威位置，并让每个必需章节只完成自己的最小功能。

### NAR-004 — 限制性内容没有单一完整权威位置

五条证据链各自多出一个独立限制字段，和全篇其他失败、降级及禁止解释陈述形成密集重复。证据链仍应保留边界明确的 Supports，但不需要第五个限制字段。第 14 个 H2 已经具备汇总限制、假设、风险、替代和停止条件的结构，应成为唯一完整权威位置。其他章节只有在某个边界直接使相邻设计选择可理解、且删除会扭曲该选择时，才保留自足的最小限定；不应留下指向第 14 节的替代性提示。

### NAR-005 — 实现章节没有履行实现功能

“Key techniques and implementation” 当前是方法摘要的另一种排列。它需要让读者看到实现对象及其连接关系，例如标签/时钟产物、审计记录、字段角色注册、模型准入记录、分区与冻结清单、投影包和失败发布包各自接收什么、产生什么、如何留痕。这样的改写可以保留现有十项技术内容，同时消除与详细方法章节的重复。

### NAR-006 — 必需章节之间的重复超过各自合同功能

日期门、工作包、方法、实现、证据链、验收清单、产物、解释和风险都属于必需功能，不能因为它们追踪同一研究就合并删除。但当前若干完整规范在这些功能之间重复出现，尤其是恢复门、医院级外部检验和 RCT 分支。修订应为每类细节指定权威章节，再在其他必需章节留下可独立完成其功能的最小信息。这样既保留 15 个 H2、五个证据链 H3、证据链四项结构和 Claim-Support 审计，也能消除反复比对和回读。

## Preserved strengths

- 15 个必需 H2 均存在，标题、主要问题、四项目标、计划产物、贡献定位和 Claim-Support 表指向同一脓毒症全病程候选表征，核心元素没有实质冲突。
- “Background, current state, gap, significance, and rationale” 已具备构造完整五段链的大部分事实材料；需要重排和补足功能，而不是更换研究对象。
- 五个证据链 H3 覆盖数据边界、可恢复不变量、任务效度、跨库检验和条件性 RCT 输出；每条链的 Input、Method / analysis / processing、Output、Supports 都应完整保留。
- Research design and methods 已包含双时钟、状态系统、恢复门、医院优先外部检验和 RCT 投影的详细科学规范，可作为方法权威内容继续保留。
- 阶段 II 与阶段 III 的时间边界、观察性与因果解释边界、投影失败后的独立临床端点边界均已明确；修订应改变其叙述位置和权重，不改变边界本身。
- Claim-Support 表区分了 supported、qualified 和 unsupported 主张，是最终读者审计的重要功能，不应被删除或并入其他章节。

## Handoff

See the paired `narrative-repair-plan-r056.yaml` for executable actions.
