# Evidence Grading: Two-Dimensional System

## Dimension A: Evidence Strength

证据本身的可靠性——不依赖于其与当前 claim 的关系。

| Level | Label | Definition |
|-------|-------|------------|
| S | strong | Multiple independent studies with consistent findings, no major methodological flaws |
| M | moderate | Some research support but with limitations (single study, small sample, moderate risk of bias) |
| W | weak | Only preliminary evidence or indirect inference; exploratory analyses |
| C | conceptual | Based on theoretical reasoning or logical argument; no direct empirical evidence |
| I | illustrative | Used for illustrative purposes only; not evidentiary support |

## Dimension B: Evidence Directness

证据与当前主张之间的逻辑距离——证据是否直接测量/证明了该主张。

| Level | Label | Definition | Example |
|-------|-------|------------|---------|
| D | direct | Evidence directly supports the claim | A prespecified measure directly tests the bounded proposition |
| A | adjacent | Evidence supports a closely related claim; reasonable extrapolation | Evidence from one defined population is extended to a related population |
| ID | indirect | Evidence supports a premise or component, not the full claim | A component-level finding is used to support a system-level effect |
| AN | analogical | Evidence from an analogous domain or context | Evidence from context A is used to support a strategy in context B |
| IO | illustrative_only | Purely illustrative; carries no evidentiary weight | One example is used to imply a general pattern |

## Combined Matrix

Evidence strength × directness → Allowed claim strength:

| Strength ↓ / Directness → | Direct | Adjacent | Indirect | Analogical | Illustrative |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **Strong** | strong | strong | moderate | weak | — |
| **Moderate** | moderate | moderate | weak | weak | — |
| **Weak** | weak | weak | weak | speculative | — |
| **Conceptual** | weak | speculative | speculative | speculative | — |
| **Illustrative** | — | — | — | — | — |

"—" = evidence provides no support for this claim in this configuration.

## Overclaim Risk Assessment

| Condition | Risk | Action |
|-----------|------|--------|
| High strength + Direct | Low | Claim can be stated confidently |
| High strength + Indirect | High | Must downgrade claim strength or add boundary condition |
| Moderate + Adjacent | Medium | Claim needs hedging, boundary conditions |
| Low strength + Direct | Medium | Claim is promising but preliminary — must use cautious language |
| Any + Illustrative | Critical | Cannot use as evidence; illustrative only |

## Example

```
C3: "方案 X 改善预先指定的主要结果"
  Evidence E2: 一项直接检验该结果、但尚未由独立研究复现的研究
  Strength: Moderate (直接研究, 尚未独立复现)
  Directness: Direct (直接测量了预先指定的主要结局)
  → Allowed claim strength: moderate
  → Overclaim risk: Low

C7: "该证据架构适用于所有研究场景"
  Evidence E5: 仅在少数已定义场景中应用
  Strength: Moderate
  Directness: Indirect (少数场景 → 全领域推广)
  → Allowed claim strength: weak
  → Overclaim risk: High → 弱化措辞或增加边界条件
```
