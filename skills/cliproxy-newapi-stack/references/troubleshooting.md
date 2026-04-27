# Stack Troubleshooting (踩过的坑)

| 症状 | 根因 | 修复 |
|---|---|---|
| NewAPI 渠道测试失败：`upstream connection refused` | 容器里的 `127.0.0.1` 是容器自己 | base_url 改成 `http://172.17.0.1:<CLIPROXY_PORT>` |
| 写价格用 `/api/option/` PUT 返回 success 但实际不生效 | 这版接口幂等行为不一致 | 直接 `sqlite3 UPDATE options ...` + `docker restart new-api` |
| 调用经 NewAPI 后 `quota=0` 入 logs | 模型名没在 ModelRatio 里登记，走 default 0 | 必须显式写 ratio 给 CLIProxyAPI 暴露的虚拟模型名（如 `gpt-5.4`） |
| 30 并发 5KB payload 时混合 200/503 (~50%) | CLIProxyAPI conductor 把 408 当 5xx 触发 1 分钟冷却，selector 在窗口期同步拒所有请求 | `config.yaml` 加 `disable-cooling: true`，改 `internal/config/config.go` 触达的开关 |
| 直连 :8317 返回 408 但经 NewAPI 变 503 | NewAPI 把 auth_unavailable 包装成 503 | 看 `/root/CLIProxyAPI/cli-proxy-api.log` 里的真实上游码 |
| `Empty reply from server` 公网调用 | UFW 默认 `deny incoming`，端口未放行 | `ufw allow <PORT>/tcp` |
| 加新 OAuth 账号后日志显示老号还在被路由 | 多账号轮询正常 | 老号 429/quota 用尽时 selector 才把它 mark unavailable，新号自动顶上 |
| NewAPI `/api/option/` 401 | 未登录或漏 `New-Api-User: 1` 头 | 先 `POST /api/user/login` 拿 cookie，再调 `GET /api/option/ -H 'New-Api-User: 1'` |
| 用户看到 `quota=-N` 但前端没反应 | 持续消费导致负余额 | 直接 `UPDATE users SET quota=N WHERE id=?` + 重启容器 |
| 老 PID 还监听端口，新启动不生效 | 旧 `go run` 进程没退 | `lsof -i:<PORT>` → 精确 `kill <pid>`；不要 `pkill -9 go` |
| OAuth 卡 `Authentication timed out` | 5 分钟窗口 + 隧道未就位 | 改走本地 OAuth + scp |
| Codex login 通过但实际请求 401 | 账号无 ChatGPT Plus/Pro 订阅 | 换有效订阅账号；不要假设 login 成功 = 可用 |

## 容器网络速记
```
container 127.0.0.1 ≠ host
container -> host =  http://172.17.0.1:<port>     (default bridge)
host -> container = http://127.0.0.1:<port>       (port-published)
external -> host =  http://<HOST>:<port>          (UFW must allow)
```

## CLIProxyAPI cooldown 原理
- 文件：`sdk/cliproxy/auth/conductor.go`
- 触发：`case 408, 500, 502, 503, 504` → `state.NextRetryAfter = now+1min`
- 后果：单次 408 把整账号冻 60s；30 并发期间 99% 请求落在窗口内
- 解药：`config.yaml: disable-cooling: true`（`internal/config/config.go` 的开关，运行时读）

## NewAPI 计费日志
```sql
SELECT id, datetime(created_at,'unixepoch','localtime') AS t,
       model_name, prompt_tokens, completion_tokens,
       quota, channel_id, request_id
FROM logs ORDER BY id DESC LIMIT 20;
```
- `quota=0` 通常意味着模型名漏了 ratio 配置或走了 default 0。
- `request_id` 与响应头 `X-Oneapi-Request-Id` 对应，可跨层追踪。
