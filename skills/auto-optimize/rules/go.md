# Go Rules（Go 特定规则）

Go 项目扫描和修复的特定规则。

## 扫描检查项

| ID | 类别 | 检查项 | 严重度 |
|----|------|--------|--------|
| GO-01 | Bug | 未检查 error 返回值 | 高 |
| GO-02 | Bug | goroutine 泄漏（无 context 取消或 done channel） | 高 |
| GO-03 | Bug | data race（共享变量无 mutex 或 channel） | 高 |
| GO-04 | Design | 接口定义在实现侧而非消费侧 | 中 |
| GO-05 | Dedup | 多处相同的 error wrapping 模式 | 中 |
| GO-06 | Perf | 循环内 append 未预分配 cap | 低 |
| GO-07 | Perf | 字符串拼接用 + 而非 strings.Builder | 低 |

## SKIP 规则（Go 特定）

| 条件 | 判定 | 理由 |
|------|------|------|
| 用 init() 做初始化 | SKIP | Go 惯用法，除非有副作用问题 |
| 导出但未使用的函数 | 检查 | 可能是公开 API，标记为 DEFER |
| 缺少 godoc 注释 | SKIP | 独立处理 |

## 验证命令
```bash
go vet ./... && golangci-lint run && go test ./...
```
