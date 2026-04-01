# Plan Template (Step-Test-Update Loop)

Use this template when creating `plan/<name>.md`.

```md
# <Task Name> 执行计划

- 计划版本: v1
- 适用仓库: <absolute path>
- 执行模式: 每步改动 -> 立即测试 -> 回写计划 -> 下一步

## 0. 执行约束（DoR）

- 目标: <clear objective>
- 兼容性: <required | not required>
- 提交策略: <per_step | milestone | final_only>
- 测试策略:
  - 步骤级: 每步至少 1 条定向测试 + 1 条健康检查
  - 最终: 运行阶段/全量回归

## 1. 分析结果（先于改动）

- 架构盘点摘要:
  - 模型/配置入口: <paths>
  - 工厂/注册表入口: <paths>
  - 适配层入口: <paths>
  - 基础设施入口(http/cache/storage/logging): <paths>
- 重复/冗余候选列表:

| id | 类别 | 文件与符号 | 证据 | 影响 | 风险 | 建议收敛方向 |
|----|------|------------|------|------|------|--------------|
| F1 | <same-concept multi-def> | <path::symbol> | <call path/test/warn> | <high/med/low> | <high/med/low> | <canonical> |
| F2 | ... | ... | ... | ... | ... | ... |

## 2. 详细步骤（从分析映射而来）

### Step A1 <title>

- 状态: `in_progress`
- 目标: <what this step delivers>
- 预计改动文件:
  - `<file1>`
  - `<file2>`
- 详细改动:
  - <implementation detail 1>
  - <implementation detail 2>
- 步骤级测试命令:
  - `<command 1>`
  - `<command 2>`
- 完成判定:
  - <done criteria>

### Step A2 <title>

- 状态: `pending`
- ...

## 3. 回归测试矩阵

- 阶段完成检查:
  - `<command>`
- 最终检查:
  - `<command>`

## 4. 执行日志（每步完成后追加）

- <YYYY-MM-DD>
  - Step A1: `completed`
    - 修改文件:
      - `<file>`
    - 主要改动:
      - <summary>
    - 执行测试:
      - `<command>` -> pass/fail
      - `<command>` -> pass/fail
```

## Status Transition Rules

- Only one step can be `in_progress`.
- Move to next step only after current step tests pass.
- If blocked, mark `blocked` with reason and evidence.

## Evidence Rules

- Keep exact command strings.
- Record pass/fail explicitly.
- If command cannot run, write the reason and closest fallback validation.
