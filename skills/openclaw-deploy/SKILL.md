---
name: openclaw-deploy
description: 在远程服务器上一键部署 OpenClaw。当用户需要安装 OpenClaw、部署 OpenClaw、配置 OpenClaw 到服务器时使用
argument-hint: [SSH连接信息，如 root@host -p port]
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch, WebFetch, Task, Glob, Grep, Edit
---

# OpenClaw 远程一键部署

在远程 Linux 服务器上自动部署 OpenClaw + AI 模型 + 聊天频道。

---

## 第零步：输出傻瓜教程

**skill 启动后，必须先输出以下准备清单**，让用户知道需要什么，然后再用 AskUserQuestion 收集信息：

```markdown
# OpenClaw 一键部署

欢迎！部署前你需要准备以下东西：

| 序号 | 准备什么 | 说明 | 必需？ |
|------|----------|------|--------|
| 1 | 一台 Linux 服务器 | 最低 1GB 内存 + 500MB 磁盘，支持 SSH 登录 | 必需 |
| 2 | SSH 免密登录 | 确保本机能 `ssh user@host` 直接连上 | 必需 |
| 3 | AI 模型 API Key | 智谱GLM / DeepSeek / OpenAI / Claude / Kimi / 通义 任选 | 必需 |
| 4 | 聊天频道 Bot Token | Telegram(@BotFather) 或 Discord 或 飞书，也可以暂不配 | 可选 |
| 5 | 代理地址 | 中国大陆服务器 + 海外频道(Telegram/Discord)时需要 | 视情况 |
| 6 | 浏览器控制 | 让 Bot 能操控浏览器搜索/截图/填表，需额外安装 Playwright | 可选 |
```

---

## 第一步：收集信息

用 AskUserQuestion 收集（$ARGUMENTS 已提供的跳过）。分两轮问：

### 第一轮（必填 3 项）：

用 AskUserQuestion 同时问以下 3 个问题：

1. **SSH 连接信息**（header: "SSH 连接"）
   - 选项根据上下文动态生成（如之前用过的服务器），兜底选项"其他服务器"
2. **AI 模型**（header: "AI 模型"）
   - 智谱 GLM-5（国产，无需代理）
   - DeepSeek（国产，无需代理）
   - OpenAI GPT-4o（需代理或海外服务器）
   - Anthropic Claude（需代理或海外服务器）
3. **聊天频道**（header: "聊天频道"）
   - Telegram（需 Bot Token，中国大陆需代理）
   - Discord（需 Bot Token）
   - 飞书（需 Bot Token）
   - 暂不配置
4. **浏览器控制**（header: "浏览器"）
   - 启用（Bot 可操控浏览器搜索/截图/填表）
   - 暂不配置

### 第二轮（根据第一轮结果追问）：

- 如果用户没提供 API Key → 问 API Key
- 如果选了聊天频道 → 问 Bot Token
  - 如果用户没有 Bot Token → 给出创建教程：
    - Telegram：找 @BotFather，发 `/newbot`
    - Discord：去 discord.com/developers 创建 Application → Bot
    - 飞书：去 open.feishu.cn 创建自建应用
- 如果选了 Telegram/Discord 且服务器在中国大陆 → 问代理地址
  - 自动判断：如果 SSH 到服务器后 `curl -s --connect-timeout 3 https://api.telegram.org` 失败，则判定需要代理

---

## 第二步：环境检查

SSH 连接到服务器，**单条命令**获取全部信息：

```bash
ssh <SSH_ARGS> "echo '=== CPU ===' && nproc && echo '=== 内存 ===' && free -h && echo '=== 磁盘 ===' && df -h / && echo '=== 系统 ===' && uname -a && echo '=== Node.js ===' && node -v 2>/dev/null || echo '未安装' && echo '=== npm ===' && npm -v 2>/dev/null || echo '未安装' && echo '=== 包管理器 ===' && which pacman apt yum dnf 2>/dev/null && echo '=== OpenClaw ===' && openclaw --version 2>/dev/null || echo '未安装'"
```

**最低要求**：1GB RAM + 500MB 磁盘。不满足则告知用户并停止。

---

## 第三步：安装 Node.js（如未安装）

根据检测到的包管理器：

| 包管理器 | 命令 |
|----------|------|
| pacman (Arch) | `pacman -S --noconfirm nodejs npm` |
| apt (Debian/Ubuntu) | `curl -fsSL https://deb.nodesource.com/setup_22.x \| bash - && apt install -y nodejs` |
| dnf (RHEL/Fedora) | `dnf install -y nodejs npm` |
| yum (CentOS) | `curl -fsSL https://rpm.nodesource.com/setup_22.x \| bash - && yum install -y nodejs` |

安装后验证：`node -v && npm -v`，确认 Node.js >= 22。

---

## 第四步：安装 OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

> **重要**：安装脚本会尝试启动交互式 onboarding wizard，在非 TTY 环境会报 `/dev/tty: No such device or address` 错误。**这是正常的**，OpenClaw 本体已安装成功。

验证：`openclaw --version`

---

## 第五步：写入配置文件

**直接写 `~/.openclaw/openclaw.json`**，不用交互式 wizard。

### 模型配置模板

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "<PROVIDER_NAME>": {
        "baseUrl": "<BASE_URL>",
        "apiKey": "<API_KEY>",
        "api": "openai-completions",
        "models": [
          {
            "id": "<MODEL_ID>",
            "name": "<DISPLAY_NAME>",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 128000,
            "maxTokens": 32000
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "<PROVIDER_NAME>/<MODEL_ID>"
      },
      "memorySearch": {
        "enabled": false
      }
    }
  },
  "gateway": {
    "mode": "local"
  }
}
```

### 常见模型参考

| Provider 名 | MODEL_ID | baseUrl |
|-------------|----------|---------|
| zhipu | glm-5 | `https://open.bigmodel.cn/api/paas/v4` |
| openai | gpt-4o | `https://api.openai.com/v1` |
| deepseek | deepseek-chat | `https://api.deepseek.com/v1` |
| kimi | moonshot-v1-128k | `https://api.moonshot.cn/v1` |
| qwen | qwen-max | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| anthropic | claude-sonnet-4-5-20250929 | `https://api.anthropic.com/v1` |

> **注意**：Anthropic 模型的 `api` 字段应为 `"anthropic-messages"` 而非 `"openai-completions"`。

写入后立即修复权限：

```bash
mkdir -p ~/.openclaw/agents/main/sessions ~/.openclaw/credentials
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
```

---

## 第六步：启动网关（systemd）

按顺序执行：

```bash
# 安装 systemd 服务
openclaw gateway install

# 启用 linger（退出 SSH 后服务不会停）
loginctl enable-linger $(whoami)

# 启动
export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemctl --user start openclaw-gateway.service
```

等待 3 秒后验证：

```bash
systemctl --user status openclaw-gateway.service | head -10
```

确认 `Active: active (running)`。

### 轮换 device token

网关首次启动后，轮换 operator token 修复可能的认证问题：

```bash
# 先获取 device ID
DEVICE_ID=$(openclaw devices list 2>&1 | grep -oP '[a-f0-9]{40,}')
# 轮换 token
openclaw devices rotate --role operator --device "$DEVICE_ID"
```

---

## 第七步：配置聊天频道（如需要）

根据用户选择的频道执行对应配置。

### 7a. 设置频道

**Telegram：**
```bash
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.botToken '<BOT_TOKEN>'
openclaw config set channels.telegram.dmPolicy pairing
```

**Discord：**
```bash
openclaw config set channels.discord.enabled true
openclaw config set channels.discord.botToken '<BOT_TOKEN>'
openclaw config set channels.discord.dmPolicy pairing
```

**飞书：**
```bash
openclaw config set channels.feishu.enabled true
openclaw config set channels.feishu.token '<BOT_TOKEN>'
openclaw config set channels.feishu.dmPolicy pairing
```

### 7b. 配置代理（中国大陆服务器 + 海外频道时必须）

> **适用场景**：服务器在中国大陆，且频道是 Telegram 或 Discord（需访问海外 API）。
> 飞书是国内服务，不需要代理。

先测试是否需要代理（自动判断）：

```bash
# Telegram
curl -s --connect-timeout 3 https://api.telegram.org/bot<BOT_TOKEN>/getMe
# Discord
curl -s --connect-timeout 3 https://discord.com/api/v10/users/@me -H "Authorization: Bot <BOT_TOKEN>"
```

如果超时/失败，说明需要代理。用用户提供的代理测试：

```bash
export http_proxy='<PROXY_URL>' && export https_proxy='<PROXY_URL>'
curl -s --connect-timeout 5 https://api.telegram.org/bot<BOT_TOKEN>/getMe
```

确认返回成功后，写入 systemd override。

> **重要**：proxy.conf 必须**一次性写完所有环境变量**（代理 + no_proxy + DISPLAY），
> 不要分多次追加，后续浏览器步骤也不需要再改这个文件。

```bash
mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
cat > ~/.config/systemd/user/openclaw-gateway.service.d/proxy.conf << EOF
[Service]
Environment="http_proxy=<PROXY_URL>"
Environment="https_proxy=<PROXY_URL>"
Environment="no_proxy=127.0.0.1,localhost,::1"
Environment="NO_PROXY=127.0.0.1,localhost,::1"
Environment="DISPLAY=:99"
EOF
```

> **为什么要 `no_proxy`**：没有它，OpenClaw 连本地 Chrome CDP 端口也会走代理，
> 导致浏览器启动成功但 OpenClaw 检测不到，报 `Failed to start Chrome CDP`。
> 即使当前不配浏览器，也要加上 `no_proxy`，防止后续开启浏览器时踩坑。

> **为什么要 `DISPLAY=:99`**：浏览器需要显示服务器，即使 headless 模式也需要。
> 如果不配浏览器，这个变量无害。

### 7c. 重启网关（必须通过 systemd！）

> **关键坑点**：`openclaw config set` 会触发内部热重启，但热重启**不会**加载 systemd 的环境变量（代理）。
> 所有涉及频道/代理的配置改完后，必须用 `systemctl --user restart` 来重启。

```bash
export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
```

### 7d. 验证频道连接

等待 5 秒后：

```bash
openclaw channels status
```

确认输出包含 `enabled, configured, running`。

**如果看到 `fetch failed` 或 `Network request failed`**：代理没生效，检查 proxy.conf 并确认是通过 systemctl 重启的。

### 7e. 配对用户

让用户在对应频道给 Bot 发一条消息。Bot 会回复配对码。

> **关键坑点**：配对命令是 `openclaw pairing approve <channel> <CODE>`，
> **不是** `openclaw devices approve <CODE>`（那个会报 `unknown requestId`）。

```bash
# 查看待配对列表（必须指定频道名）
openclaw pairing list <channel>
# 例如：openclaw pairing list telegram

# 批准配对
openclaw pairing approve <channel> <PAIRING_CODE>
# 例如：openclaw pairing approve telegram BAEWET79
```

配对码有效期约 1 小时。如果过期，让用户重新发消息即可生成新码。

---

## 第八步：配置浏览器控制（可选）

> 让 Bot 能操控浏览器，执行搜索、截图、填表等操作。
> 如果第一步用户选了「暂不配置」，跳过此步。

### 8a. 安装 Playwright Chromium + Xvfb

> **不要用系统自带的 Chromium**。滚动发行版（Arch 等）会出现 ICU/libFLAC 等库版本不匹配，
> 稳定发行版也可能版本过旧。**统一用 Playwright 自带的 Chromium**，一条命令解决。

```bash
# 安装 Playwright Chromium（自带所有依赖，不依赖系统库）
npx playwright install chromium

# 安装 Xvfb 虚拟显示（无头服务器必须）
# Arch:
pacman -S --noconfirm xorg-server-xvfb
# Debian/Ubuntu:
apt install -y xvfb
```

验证 Playwright Chromium 可运行：

```bash
PLAYWRIGHT_CHROME=$(find ~/.cache/ms-playwright/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)
$PLAYWRIGHT_CHROME --version
```

### 8b. 创建 Chromium Wrapper + 代理中继（需要代理时）

> **为什么需要 wrapper**：
> 1. OpenClaw 自动检测 `/usr/bin/chromium` 来启动浏览器，wrapper 让它用 Playwright 版本
> 2. Chromium 不支持 `http_proxy` URL 中嵌入的认证（`user:pass@host`），会报 `ERR_INVALID_AUTH_CREDENTIALS`
> 3. wrapper 自动 unset 代理环境变量，改用 `--proxy-server` 指向本地无认证代理中继

**如果需要代理**（中国大陆访问海外站点），先搭建本地代理中继：

```bash
# 创建代理中继脚本（Node.js，去掉认证层，Chrome 直连）
cat > ~/.openclaw/proxy-relay.js << 'RELAYEOF'
const http = require("http");
const net = require("net");
const UPSTREAM_HOST = process.env.PROXY_HOST || "127.0.0.1";
const UPSTREAM_PORT = parseInt(process.env.PROXY_PORT || "7890", 10);
const UPSTREAM_USER = process.env.PROXY_USER || "";
const UPSTREAM_PASS = process.env.PROXY_PASS || "";
const LOCAL_PORT = parseInt(process.env.RELAY_PORT || "7891", 10);
const authHeader = UPSTREAM_USER
  ? "Basic " + Buffer.from(UPSTREAM_USER + ":" + UPSTREAM_PASS).toString("base64")
  : null;
const server = http.createServer((req, res) => {
  const opts = { host: UPSTREAM_HOST, port: UPSTREAM_PORT, path: req.url,
    method: req.method, headers: { ...req.headers } };
  if (authHeader) opts.headers["Proxy-Authorization"] = authHeader;
  const proxy = http.request(opts, (pRes) => { res.writeHead(pRes.statusCode, pRes.headers); pRes.pipe(res); });
  proxy.on("error", (e) => { res.writeHead(502); res.end(String(e)); });
  req.pipe(proxy);
});
server.on("connect", (req, clientSocket, head) => {
  const connectReq = "CONNECT " + req.url + " HTTP/1.1\r\nHost: " + req.url + "\r\n"
    + (authHeader ? "Proxy-Authorization: " + authHeader + "\r\n" : "") + "\r\n";
  const proxySocket = net.connect(UPSTREAM_PORT, UPSTREAM_HOST, () => { proxySocket.write(connectReq); });
  let buf = Buffer.alloc(0);
  const onData = (chunk) => {
    buf = Buffer.concat([buf, chunk]);
    const idx = buf.indexOf("\r\n\r\n");
    if (idx === -1) return;
    proxySocket.removeListener("data", onData);
    const resp = buf.slice(0, idx).toString();
    const rest = buf.slice(idx + 4);
    if (resp.includes(" 200 ")) {
      clientSocket.write("HTTP/1.1 200 Connection Established\r\n\r\n");
      if (rest.length) clientSocket.write(rest);
      if (head.length) proxySocket.write(head);
      proxySocket.pipe(clientSocket); clientSocket.pipe(proxySocket);
    } else { clientSocket.end("HTTP/1.1 502 Bad Gateway\r\n\r\n"); proxySocket.end(); }
  };
  proxySocket.on("data", onData);
  proxySocket.on("error", () => clientSocket.destroy());
  clientSocket.on("error", () => proxySocket.destroy());
});
server.listen(LOCAL_PORT, "127.0.0.1", () => {
  console.log("proxy-relay listening on 127.0.0.1:" + LOCAL_PORT + " -> " + UPSTREAM_HOST + ":" + UPSTREAM_PORT);
});
RELAYEOF

# 创建 systemd 服务（用实际的代理信息替换变量）
cat > ~/.config/systemd/user/proxy-relay.service << EOF
[Unit]
Description=Local Proxy Relay (auth-stripping for Chrome)
Before=openclaw-gateway.service

[Service]
ExecStart=/usr/bin/node /root/.openclaw/proxy-relay.js
Environment="PROXY_HOST=<UPSTREAM_PROXY_HOST>"
Environment="PROXY_PORT=<UPSTREAM_PROXY_PORT>"
Environment="PROXY_USER=<UPSTREAM_PROXY_USER>"
Environment="PROXY_PASS=<UPSTREAM_PROXY_PASS>"
Environment="RELAY_PORT=7891"
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOF

export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemctl --user daemon-reload
systemctl --user enable --now proxy-relay.service

# 验证中继工作
curl -s --connect-timeout 5 -x http://127.0.0.1:7891 https://api.telegram.org | head -1
```

> **架构说明**：
> ```
> Chrome --proxy-server=127.0.0.1:7891 → proxy-relay（无认证）→ 上游代理（带认证）→ 海外网站
> ```

**创建 wrapper**（根据是否需要代理，选择对应版本）：

```bash
# 备份系统 chromium（如果有）
mv /usr/bin/chromium /usr/bin/chromium.system 2>/dev/null

# 获取 Playwright Chrome 路径
PLAYWRIGHT_CHROME=$(find ~/.cache/ms-playwright/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)

# === 需要代理的版本 ===
cat > /usr/bin/chromium << EOF
#!/bin/bash
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
exec $PLAYWRIGHT_CHROME --proxy-server=http://127.0.0.1:7891 "\$@"
EOF

# === 不需要代理的版本 ===
# cat > /usr/bin/chromium << EOF
# #!/bin/bash
# unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
# exec $PLAYWRIGHT_CHROME "\$@"
# EOF

chmod +x /usr/bin/chromium

# 验证
/usr/bin/chromium --version
```

> **注意**：写 wrapper 文件时避免通过 SSH 传递 `#!/bin/bash`，
> 某些 shell（zsh）会把 `!` 转义为 `\!`。建议用 `scp` 或在远程服务器上直接编辑。

### 8c. 启动 Xvfb 服务

```bash
cat > ~/.config/systemd/user/xvfb.service << 'EOF'
[Unit]
Description=Xvfb Virtual Framebuffer
Before=openclaw-gateway.service

[Service]
ExecStart=/usr/bin/Xvfb :99 -screen 0 1280x720x24 -nolisten tcp
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOF

export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemctl --user daemon-reload
systemctl --user enable --now xvfb.service
```

### 8d. 配置 OpenClaw 浏览器（三个必设项 + profile）

> **三个配置缺一不可**，否则 Chrome 无法在无头服务器上以 root 运行：

```bash
openclaw config set browser.enabled true
openclaw config set browser.headless true    # 无头模式，不开会尝试打开 GUI
openclaw config set browser.noSandbox true   # root 运行必须，否则 Chrome 静默崩溃
```

创建 headless profile（使用 openclaw 驱动，不用 Chrome 扩展）：

```bash
openclaw browser create-profile --name headless --driver openclaw --color '#0066CC'
openclaw config set browser.defaultProfile headless
```

> **不要用默认的 extension driver**。extension driver 需要在 Chrome 里安装 OpenClaw 扩展，
> 无头服务器上不可能操作。`--driver openclaw` 使用 Playwright 直接驱动。

### 8e. 确保 systemd 环境变量完整

> 如果第 7 步已经写了 proxy.conf（含 `no_proxy` 和 `DISPLAY=:99`），这里**不需要再改**。
> 如果第 7 步没配代理（不需要代理的场景），这里只需加 `DISPLAY`：

```bash
# 仅当第 7 步没写过 proxy.conf 时才需要
mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
cat > ~/.config/systemd/user/openclaw-gateway.service.d/proxy.conf << 'EOF'
[Service]
Environment="DISPLAY=:99"
EOF
```

### 8f. 清理 + 验证配置 + 重启

> **重要**：先运行 `openclaw doctor --fix` 清理可能的无效配置 key，
> 避免网关因配置校验失败反复崩溃重启。

```bash
# 清理无效配置
openclaw doctor --fix

# 杀掉可能残留的 Chrome 进程
killall -9 chrome chrome_crashpad 2>/dev/null
rm -f ~/.openclaw/browser/headless/user-data/SingletonLock 2>/dev/null

# 重启网关
export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
sleep 5

# 测试导航（用简单站点，首次连接较慢属正常）
openclaw browser navigate https://example.com --timeout 60000

# 测试快照
openclaw browser snapshot | head -20

# 确认状态（应显示 running: true）
openclaw browser status
```

### 8g. 低功耗设备性能调优（ARM/树莓派等）

> **适用场景**：树莓派、ARM 开发板等低功耗设备。x86 服务器通常不需要。
> **核心问题**：Chrome 使用 `swiftshader-webgl`（CPU 软件渲染），ARM CPU 处理复杂页面极慢。
> 内存不是瓶颈（8GB 足够），CPU 才是。

**问题 1：浏览器操作超时 20 秒不够**

OpenClaw 硬编码了 20 秒超时（`timeoutMs: 2e4`），低功耗设备上需要 60 秒。

```bash
# 修改所有浏览器操作超时：20s → 60s
for f in pi-embedded-*.js reply-*.js; do
  FILE="/usr/lib/node_modules/openclaw/dist/$f"
  [ -f "$FILE" ] && sed -i 's/timeoutMs: 2e4/timeoutMs: 6e4/g' "$FILE"
done

# 修改浏览器 CLI 命令超时
for f in browser-cli-*.js; do
  FILE="/usr/lib/node_modules/openclaw/dist/$f"
  [ -f "$FILE" ] && sed -i 's/timeoutMs: 2e4/timeoutMs: 6e4/g; s/?? 2e4/?? 6e4/g' "$FILE"
done

# 修改默认代理超时常量
sed -i 's/DEFAULT_BROWSER_PROXY_TIMEOUT_MS = 2e4/DEFAULT_BROWSER_PROXY_TIMEOUT_MS = 6e4/g' \
  /usr/lib/node_modules/openclaw/dist/pi-embedded-*.js \
  /usr/lib/node_modules/openclaw/dist/reply-*.js
```

**问题 2：Playwright CDP 连接超时太短**

Playwright 连接 Chrome 有 3 次重试（5s/7s/9s），ARM 设备上不够。改为 15s/20s/25s：

```bash
# 增加 Playwright CDP 连接超时
sed -i 's/const timeout = 5e3 + attempt \* 2e3/const timeout = 15e3 + attempt * 5e3/g' \
  /usr/lib/node_modules/openclaw/dist/pw-ai-*.js
```

**问题 3：Chrome 重启后恢复旧标签**

Chrome 从 user-data 恢复上次会话的所有标签页，在低功耗设备上多标签会耗尽 CPU。
每次重启网关前需要清理：

```bash
# 关闭所有 Chrome 标签（保留一个空白页）
curl -s http://127.0.0.1:18801/json/list 2>/dev/null | \
  python3 -c "
import sys,json,urllib.request
try:
  tabs=json.load(sys.stdin)
  for t in tabs[1:]:
    urllib.request.urlopen(f'http://127.0.0.1:18801/json/close/{t[\"id\"]}')
  print(f'Closed {len(tabs)-1} tabs')
except: pass
" 2>/dev/null
```

> **注意**：以上源码修改会在 OpenClaw 更新后被覆盖，需要重新执行。

**低功耗设备浏览器使用建议**：
- 避免重型 SPA（Google News、Twitter 等），超过 60 秒仍会超时
- 优先用轻量级/文本版网站（CNN Lite、RSS feeds、API 接口）
- 简单页面（example.com、百度）通常 3-5 秒内完成
- 首次浏览器操作较慢（Playwright 需建立 CDP 连接），后续操作快很多

### 8h. X/Twitter 登录（可选）

> **适用场景**：让 Bot 能以已登录身份浏览 X/Twitter（查看时间线、搜索等）。
> 需要先完成 8a-8f 的浏览器配置。

**前置条件**：用户需提供 X/Twitter 的 `auth_token`（40 位十六进制）。
这个 token 可从已登录浏览器的 Cookies 中提取（开发者工具 → Application → Cookies → x.com → auth_token）。

> **核心经验**：**不要尝试自动化登录流程！** 直接注入 auth_token 是唯一可靠方案。
> 我们尝试过 7+ 种登录方案全部失败（见踩坑总结 22-28），原因包括：
> - X 的登录页在 ARM + swiftshader 上无法渲染
> - API 登录流程会触发 IP 限频（error 399）
> - Python HTTP 客户端被 Cloudflare TLS 指纹识别拦截
> - Chrome 跨域请求（CORS）限制无法绕过

**注入 auth_token 到 Chrome：**

```python
# /tmp/x-inject-token.py — 通过 CDP 注入 auth_token
import json, socket, struct, hashlib, base64, time, os, urllib.request

CDP_URL = "http://127.0.0.1:18801"
AUTH_TOKEN = "<用户提供的auth_token>"

# ... CDP 类（见下方完整代码）...

# 1. 清除旧的 x.com/twitter.com cookies
all_ck = c.cmd("Network.getAllCookies")
for ck in all_ck.get("cookies", []):
    dom = ck.get("domain", "")
    if "x.com" in dom or "twitter.com" in dom:
        c.cmd("Network.deleteCookies", {"name": ck["name"], "domain": dom})

# 2. 注入 auth_token
for dom in [".x.com", ".twitter.com"]:
    c.cmd("Network.setCookie", {
        "name": "auth_token", "value": AUTH_TOKEN,
        "domain": dom, "path": "/", "secure": True, "httpOnly": True
    })

# 3. 导航到 x.com/home 触发会话建立
c.cmd("Page.navigate", {"url": "https://x.com/home"})
time.sleep(20)  # ARM 设备需要更长等待

# 4. 验证：页面标题应为 "(N) Home / X"，且 cookies 包含 ct0 和 twid
all_ck = c.cmd("Network.getAllCookies")
# 从 Network 层读取 cookies（ct0 是 httpOnly，JS 读不到）
```

**验证成功的标志：**
- 页面标题包含 `Home / X`（不是 `Login` 或空白页）
- Cookies 中出现 `ct0`（CSRF token）和 `twid`（用户 ID）
- URL 保持在 `x.com/home`（没被重定向到登录页）

**保存 cookies 供其他工具使用：**

```bash
# cookies 保存位置
~/.openclaw/x-cookies.json
```

> **重要**：`ct0` cookie 是 httpOnly 的，**只能通过 CDP `Network.getAllCookies` 读取**，
> 不能用 `document.cookie` 读（会返回空）。这是一个常见误判——看到 `ct0: none` 就以为登录失败，
> 实际上页面标题 `Home / X` 已经证明登录成功了。

**安装 x-tweet-fetcher skill（可选）：**

让 Bot 能通过命令获取 X/Twitter 推文内容：

```bash
# 手动下载安装（clawhub install 经常限频）
SKILL_DIR="/usr/lib/node_modules/openclaw/skills/x-tweet-fetcher"
mkdir -p "$SKILL_DIR/scripts"

# 下载 SKILL.md 和 fetch_tweet.py
curl -sL "https://raw.githubusercontent.com/ythx-101/x-tweet-fetcher/main/SKILL.md" \
  -o "$SKILL_DIR/SKILL.md"
curl -sL "https://raw.githubusercontent.com/ythx-101/x-tweet-fetcher/main/scripts/fetch_tweet.py" \
  -o "$SKILL_DIR/scripts/fetch_tweet.py"
chmod +x "$SKILL_DIR/scripts/fetch_tweet.py"

# 验证
openclaw skills list 2>&1 | grep tweet
```

> **坑**：`fetch_tweet.py` 使用 `urllib.request.urlopen()`，这个函数**不会自动使用 `https_proxy` 环境变量**。
> 如果服务器需要代理才能访问外网，必须手动添加 ProxyHandler：

```python
# 在 fetch_tweet.py 的 import 部分加 import os
# 在 urlopen 之前加：
proxy_url = os.environ.get("https_proxy") or os.environ.get("http_proxy") or ""
if proxy_url:
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"https": proxy_url, "http": proxy_url})
    )
else:
    opener = urllib.request.build_opener()
# 然后用 opener.open(url) 替换 urllib.request.urlopen(url)
```

---

## 第九步：最终验证

```bash
# 1. 健康检查
openclaw health

# 2. 频道状态
openclaw channels status

# 3. 测试模型连通（命令行）
openclaw agent --local --agent main -m '你好，简短确认你是什么模型'

# 4. systemd 服务状态
export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemctl --user status openclaw-gateway.service | head -5

# 5. 浏览器状态（如已配置）
openclaw browser status
```

全部通过后，输出总结表格：

| 项目 | 状态 |
|------|------|
| OpenClaw | 版本号 |
| 模型 | provider/model-id |
| 网关 | systemd active (running) |
| Linger | 已启用 |
| 频道 | 频道名 + running |
| Bot 链接 | t.me/xxx_bot |
| 代理 | 有/无 |
| 浏览器 | running / 未配置 |

---

## 保存凭证

在用户本地工作目录保存一份凭证备忘录：

```
文件名：openclaw-credentials.txt
内容：服务器地址、Bot 名称、Bot Token、模型 provider
```

---

## 踩坑总结（按流程顺序）

| 编号 | 坑 | 原因 | 正确做法 |
|------|-----|------|----------|
| 1 | 安装脚本报 `/dev/tty` 错误 | 非交互式 SSH 无 TTY | 忽略，OpenClaw 已装好，手动写配置 |
| 2 | `openclaw channels add --channel telegram` 报 `Unknown channel` | Telegram 不是通过 `channels add` 配置的 | 用 `openclaw config set channels.telegram.*` |
| 3 | Telegram API 连不上（`fetch failed`） | 中国大陆无法直连 api.telegram.org | 必须配代理，写入 systemd 环境变量 |
| 4 | 代理配了但重启后还是 `fetch failed` | `openclaw config set` 触发热重启不加载 systemd 环境变量 | 必须用 `systemctl --user restart` |
| 5 | `openclaw devices approve <CODE>` 报 `unknown requestId` | 用错命令了 | 正确命令：`openclaw pairing approve telegram <CODE>` |
| 6 | `openclaw pairing list` 报 `Channel required` | 必须指定频道参数 | `openclaw pairing list telegram` |
| 7 | 配置验证报错 `dmPolicy="open" requires allowFrom to include "*"` | open 模式需要显式设置 allowFrom | 用 `pairing` 模式，不要改成 `open` |
| 8 | gateway 需要 `gateway.mode` 才能启动 | 手动写配置时漏了 | 配置文件里加 `"gateway": {"mode": "local"}` |
| 9 | `State integrity` 报目录缺失 | 首次安装未创建必要目录 | `mkdir -p ~/.openclaw/agents/main/sessions ~/.openclaw/credentials` |
| 10 | 退出 SSH 后网关停止 | systemd user session 无 linger | `loginctl enable-linger` |
| 11 | 系统 Chromium 启动报库版本不匹配 | Arch 等滚动发行版 ICU/libFLAC 版本不兼容 | 用 Playwright 自带 Chromium，创建 wrapper 替换 `/usr/bin/chromium` |
| 12 | `Chrome extension relay not reachable at 127.0.0.1:18792` | 默认 profile 用 extension driver，需要 Chrome 扩展 | 创建 headless profile：`--driver openclaw`（用 Playwright 直接驱动） |
| 13 | `Failed to start Chrome CDP on port 18801`（Chrome 已启动但检测不到） | `http_proxy` 导致 OpenClaw 连 localhost CDP 也走代理 | systemd 环境变量加 `no_proxy=127.0.0.1,localhost,::1` |
| 14 | 浏览器导航报 `net::ERR_INVALID_AUTH_CREDENTIALS` | Chromium 不支持 `http_proxy` URL 中的 `user:pass@` 认证格式 | wrapper 脚本中 `unset http_proxy https_proxy` |
| 15 | `browser.headless` 和 `browser.noSandbox` 未设置 | 默认都是 false，root 无头运行必须开启 | `openclaw config set browser.headless true` + `browser.noSandbox true` |
| 16 | 浏览器操作超时 `timed out after 20000ms` | OpenClaw 硬编码 20 秒超时，ARM 设备 CPU 软件渲染太慢 | 修改源码 `timeoutMs: 2e4` → `6e4`（见 8g 节） |
| 17 | Playwright CDP 连接超时 `Timeout 9000ms exceeded` | 首次连接重试 5s/7s/9s 不够，ARM 上 Chrome 初始化慢 | 修改源码 `5e3 + attempt * 2e3` → `15e3 + attempt * 5e3`（见 8g 节） |
| 18 | 重启后浏览器操作卡死（14 个标签恢复） | Chrome 从 user-data 恢复旧会话标签，多标签耗尽 CPU | 重启前用 CDP API 关闭多余标签，或清理 user-data |
| 19 | Google News 等重型 SPA 始终超时 | ARM + swiftshader 软件渲染，复杂 JS/CSS 渲染超过 60 秒 | 用轻量级网站或 RSS/API 替代，无法通过增加超时解决 |
| 20 | Chrome 能访问国内站但无法访问海外站 | wrapper 中 unset 了代理变量，Chrome 无法直连海外 | 搭建本地代理中继 + `--proxy-server=127.0.0.1:7891`（见 8b 节） |
| 21 | SSH 传输 wrapper 脚本 shebang 变成 `#\!` | zsh 的历史扩展把 `!` 转义成 `\!` | 用 scp 传输文件，或在远程服务器上直接编辑 |
| 22 | X 登录页显示 "Something went wrong" | ARM + swiftshader 软件渲染无法运行 X 的 React SPA | 不要用浏览器自动化登录，直接注入 auth_token |
| 23 | Twitter API 登录返回 error 399 "Could not log you in now" | 多次失败尝试触发 IP 级别限频 | 不要反复重试登录 API，一旦被限频需等待数小时 |
| 24 | Python twikit/httpx 被 Cloudflare 403 拦截 | Python HTTP 客户端的 TLS 指纹与浏览器不同 | 只能通过真实浏览器（Chrome CDP）发起请求 |
| 25 | Chrome fetch + `credentials: 'include'` 报 CORS 错误 | x.com 向 api.twitter.com 带凭据的跨域请求触发 preflight 失败 | 用 CDP `Fetch.enable` 在协议层注入 Cookie 头绕过 CORS |
| 26 | `document.cookie` 读不到 `ct0` | ct0 是 httpOnly cookie，JS 无权访问 | 用 CDP `Network.getAllCookies` 从协议层读取 |
| 27 | `urllib.request.urlopen()` 不走代理 | urllib 的 urlopen 默认**不使用** `https_proxy` 环境变量 | 显式创建 `ProxyHandler` + `build_opener` |
| 28 | env 文件 source 报 `command not found` | 密码/token 中含 `\|` 等特殊字符未加引号，bash 把 `\|` 后面当命令执行 | env 文件中所有值用单引号包裹 |
