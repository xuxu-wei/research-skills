# Design Pattern: Strategy + Path Routing with Shorthand Inputs

This document captures the UX pattern designed for `research-opportunity-mapper` v2.0+.
Other skills that need to offer users a choice of execution mode can reuse this pattern.

## When to Use

Use when a skill needs users to choose from two independent, orthogonal dimensions:

- **Strategy dimension**: how the task is executed (e.g., exploration breadth, confidence threshold)
- **Path dimension**: who executes it (e.g., agent directly vs. delegated to external tool)

## Pattern

### 1. Present both dimensions in a single interaction

Do NOT ask two sequential questions. Present both together with a shorthand input system.

```
## 探索策略与检索路径

### 探索策略
Standard (S) — 标准    Divergent (D) — 发散    Focused (F) — 聚焦

### 检索路径
Path A — 我直接执行    Path B — 委托外部

简写: SA  SB  DA  DB  FA  FB
```

### 2. Shorthand input convention

| Action | Shorthand |
|--------|-----------|
| Strategy + Path combo | Two capital letters (SA, DB, FA) |
| Strategy only | Single capital letter (S, D, F) — then ask Path |
| Ambiguous "自主决定" | Default to Standard + Path A |

### 3. Default behavior

When user says "自主决定" / "你来定" / "默认" → auto-select Standard mode.
Never assume Divergent or Focused without explicit user confirmation.

### 4. Standard mode is the regression baseline

All modifications must preserve Standard mode behavior exactly as before the change.
New parameters should only affect Divergent and Focused paths. This ensures:
- Users who say "默认" get the same behavior they're used to.
- New features don't break existing workflows.

### 5. Strategy → reference files, not inline tables

Instead of inlining parameter tables in SKILL.md (which bloats it and makes it harder to read),
route to separate reference files based on strategy:

```
references/search-routing-rules.md        ← Standard
references/divergent-search-routing.md    ← Divergent
references/focused-search-routing.md      ← Focused
```

SKILL.md references these files conditionally ("按当前 Level 加载对应文件") rather than
duplicating their content. This keeps SKILL.md lean and makes per-strategy adjustments
self-contained in dedicated files.

### 6. Mode transition without full restart

Allow switching modes mid-session without re-running the full pipeline:

- "太窄了" → switch to Divergent, expand opportunity extraction from existing Evidence Map
- "太多了" → switch to Focused, filter to core types from existing Opportunity Map
- "重新检索" → full restart with new mode

## Design Rationale

1. **User stays in control of fuzziness**. The mapper could auto-detect input specificity and
   choose a strategy, but fuzzy inputs are exactly when user intent matters most. Asking
   the user prevents the mapper from over-narrowing early exploration.

2. **Shorthand reduces friction**. Two-letter input (SA, DB) vs. full sentences makes the
   choice feel lightweight — users are more willing to experiment with different strategies.

3. **Reference-driven keeps SKILL.md focused**. A single SKILL.md with if-else blocks for
   three strategies would be confusing. Separate reference files make each strategy's logic
   self-contained and independently testable.

4. **Mode switching enables iterative refinement**. Users can start with Divergent to
   discover possibilities, then switch to Focused to validate the most promising ones.
   Without this, they'd need to restart the entire session.
