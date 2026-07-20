# Anti-Pattern Checklist

Perspective 文章最常见的 12 种退化模式。Evaluator 和 Final Compositor 共用此清单。

Apply stage-specific input boundaries. A scientific evaluator or compositor may use
the paragraph map and ledger when its own whitelist permits them. A final evaluator
must use only the final Perspective and clean minimal evidence/outlet facts: it
detects paragraph function from the page and checks evidence strength against the
clean facts, never by opening or reconstructing a hidden map or ledger.

## Full Checklist

### AP1: Caveat Creep
连续或嵌套的限定使目标读者难以识别核心判断、适用范围或实际贡献。
Detection: 提取核心主张，判断限定是否各自必要、是否位于权威位置，以及移除重复限定后能否保持科学含义。按读者功能与语义影响判定，不使用统一层数阈值。
Impact: Thesis Clarity, Stance Calibration.

### AP2: Review-Response Language in Body
正文中出现审稿回应语言（"有审稿人指出..."、"未来研究应..."用于回避论证责任）。
Detection: 扫描 "future research" 类表述是否用于填补当前论证缺口。
Impact: Argument Integrity, Stance Calibration.

### AP3: Pedagogical Rhetorical Questions
教学式修辞问句（"你是否想过...？""试问..."），将论证责任转嫁给读者。
Detection: 扫描问号结尾的句子是否承担论证功能。
Impact: Narrative Coherence, Audience Fit.

### AP4: Mini-Review Drift
文章按主题组织而非按论证组织——读者感觉在读综述而非 Perspective。
Detection: 检查段落是否按主题聚类（"关于 X 的研究..."）而非按论证步骤推动。
Impact: Narrative Coherence, Contribution Sufficiency.

### AP5: Framework-Before-Evidence
对仗工整的框架先行，然后向其中填入证据——审美驱动逻辑而非证据驱动。
Detection: 是否存在非从证据自然涌现的结构（"三层输入/三层输出"等）。
Impact: Argument Integrity, Evidence-Claim Match.

### AP6: Narrative Clinical Vignette Opening
以虚构或叙事化临床场景开场而不标明其为 illustrative。
Detection: 第一段是否为"某患者..."式叙事且未标注 illustrative。
Impact: Audience Fit, Stance Calibration（某些 outlet 允许，需匹配 narrative strategy）。

### AP7: Weak Evidence Supporting Strong Claim
弱证据（exploratory / preliminary / small-n）支撑强主张（"fundamentally transforms" / "revolutionizes"）。
Detection: scientific/compositor stages may cross-reference the claim ledger; final
evaluation compares the on-page claim with the verified proposition, strength,
directness, allowed use, and contrary/boundary facts in the clean facts bundle.
Impact: Evidence-Claim Match, Contribution Sufficiency.

### AP8: Orphan Paragraph
某段落不推进任何论证步骤——无法映射到 argument step 或 claim ID。
Detection: scientific/compositor stages may cross-reference the paragraph map; final
evaluation asks whether the paragraph visibly advances a necessary on-page reasoning
function and does not infer a hidden planned step.
Impact: Narrative Coherence, Argument Integrity.

### AP9: Strawman Counterargument
反方观点被弱化为易驳斥的版本，而非最强反对意见。
Detection: 反方部分是否可被合理反对者认可为"他们真实会说的"。
Impact: Argument Integrity, Stance Calibration.

### AP10: Overclaiming / Absolute Language
过度宣称或绝对化语言（"毫无疑问..."、"唯一方向..."、"彻底改变..."、"所有研究都忽略..."）。
Detection: 扫描绝对化表述。
Impact: Stance Calibration, Evidence-Claim Match.

### AP11: Counterargument / Boundary Authority Duplication
同一个科学上明确的反方或边界家族在多个位置被完整重复，造成防御性堆叠并打断论证推进。
Detection: when a family map is allowed, check its authority location; in final
evaluation, identify repeated complete expositions directly in the text. Outside one
authoritative exposition, allow only a short self-contained boundary required by the
adjacent reasoning.
Impact: Narrative Coherence, Argument Integrity, Stance Calibration.

### AP12: Limitation Pointer Substitution
正文用“见限制部分”“如后文所述”等指针替代当前推理所需的边界，使读者必须跳转才能判断相邻主张。
Detection: 检查所有 limitation/counterargument cross-reference；若局部边界对当前推理必要，必须在本地自包含表达；若不必要，应直接省略而不是保留指针。
Impact: Argument Integrity, Narrative Coherence.

## Scoring for Each AP

- absent: 未检测到
- minor: 存在但影响有限，不改变论证核心
- moderate: 影响读者对部分论证的信任
- critical: 使核心主张不可信或不可发表

## Usage in Evaluation

Evaluator 逐条扫描，对每条标注：
- Status: absent / minor / moderate / critical
- Location: 具体段落或 claim ID
- Impact: 受影响的评价维度

Final compositor 使用同一清单做终稿扫描。
