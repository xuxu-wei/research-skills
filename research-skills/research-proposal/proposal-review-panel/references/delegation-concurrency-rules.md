# Delegation Concurrency Rules for Panel Review

## 规则

reviewer panel 的所有 reviewer 之间互不依赖——每个 reviewer 仅接收：
- proposal 文件（独立读取）
- reviewer role brief
- 评审范围和目标

reviewer 之间不存在共享状态、不互传评分、不协商。因此**不存在需要分批的理由**。

## 执行方式

一次性将全部 reviewer brief 放入 `delegate_task(tasks=[...])` 的同一 tasks 数组，Agent 框架会自动用满 `max_concurrent_children` 并发执行。

```
delegate_task(tasks=[
    {"role": "broad-field reviewer", ...},
    {"role": "narrow-domain reviewer", ...},
    {"role": "methodology/statistics reviewer", ...},
    {"role": "cross-disciplinary reviewer", ...},
    {"role": "translational/end-user reviewer", ...},
    {"role": "skeptical reviewer", ...},
    ...  # 用户指定额外 reviewer 也一并放入
])
```

## 为何不分批

- 分批 = 人为串行化，总耗时 = N/并发数 × 单 reviewer 耗时
- 一次全发 = 自然并行，总耗时 ≈ 单 reviewer 耗时（最慢的那个）
- 不存在输出洪峰问题——父 agent 不展示全部输出，只收集结果后汇总 panel summary

## 例外

仅当用户**明确要求**分批时（如"先评审 3 个再来"），才分批。默认全部并发。
