# Python Rules（Python 特定规则）

Python 项目扫描和修复的特定规则。

## 扫描检查项

| ID | 类别 | 检查项 | 严重度 |
|----|------|--------|--------|
| PY-01 | Bug | 可变默认参数（def f(x=[])） | 高 |
| PY-02 | Bug | except 裸捕获（except: 或 except Exception） | 中 |
| PY-03 | Bug | 循环内 await 无 gather/TaskGroup | 中 |
| PY-04 | Design | 上帝类（> 500 行，> 10 个公开方法） | 中 |
| PY-05 | Dedup | 多处相同的 try/except 模式 | 中 |
| PY-06 | Perf | 循环内重复创建正则（应预编译） | 低 |
| PY-07 | Perf | 字符串拼接在循环中（应用 join 或 list） | 低 |

## SKIP 规则（Python 特定）

| 条件 | 判定 | 理由 |
|------|------|------|
| 类型注解不完整但功能正确 | SKIP | 类型注解是渐进式的 |
| 用 dict 而非 dataclass | SKIP | 除非 dict 结构在 > 3 处重复 |
| 缺少 docstring | SKIP | 独立处理，不混入功能修复 |

## 验证命令
```bash
ruff check . && ruff format --check . && pytest
```
