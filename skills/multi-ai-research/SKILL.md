---
name: multi-ai-research
description: Parallel multi-AI cross-validation research workflow (大版本). Dispatch N internal sub-agents + grok + gemini in parallel, automatically cross-validate findings, tier by confidence (strong consensus / partial / conflict / insufficient), generate tiered action items with arbitration. Use when user says "多 AI 调研", "交叉验证", "独立共识", "三脑调研", "multi-ai research", "parallel research", "cross-validate", or needs deep research that benefits from internal data + external 2026 consensus. NOT for quick factual Q&A, pure code reasoning, or tasks needing deep project context.
---

<!-- v1 | 2026-04-09 | 从 2026-04-08 X reply deboost 调研实战沉淀；集成自动置信度分级 + 仲裁 + 改动清单 -->

# Multi-AI Research（并行多 AI 交叉验证）

**核心价值**：能力乘法，不是加法。Claude（主脑）+ grok（X 社区/实时）+ gemini（Google 生态/结构化）+ N 个内部 sub-agent = **N+3 个 agent 并行**处理同一个研究问题。

**关键洞察**（2026-04-08 实战验证）：两个独立外部 AI 的共识信号 **强于** 任何单个 AI 的深度。"更深度" < "更少错"。

**和 ask-opencli 的关系**：
- `ask-opencli` = 单次 grok 或 gemini 调用（日常 second opinion）
- `multi-ai-research` = **完整调研工作流**，并行多 AI + 内部数据 + 交叉验证 + 自动仲裁

如果用户只是想"问 grok 一个问题"，用 `ask-opencli`。如果用户要做"深度调研"或"交叉验证多个维度"，用这个 skill。

---

## 何时触发

### ✅ 适合

- 深度研究任务（手动做 >30 分钟）
- 行业机制问题（算法规则、产品决策、社区共识）
- 需要外部共识加权的内部数据推断
- 时效性问题（grok 有实时 X 数据，gemini 有最新 web 索引）
- 反转既有假设（数据 vs 理论冲突时仲裁）
- 新工具/新做法的可行性调研

### ❌ 不适合

- 纯代码推理（单个 Claude 足够）
- 需要深度项目 context 的任务（外部 AI 不了解你的代码库）
- 快速事实问答（<30 秒能解决，并行开销不值）
- 创意生成（单家强模型即可）

---

## 工作流（7 Phase）

### Phase 1：问题分解（Claude 自动 + 用户可覆盖）

从用户的一个研究问题，自动拆分成：

1. **内部数据查询**（1-5 个 sub-agent 并行）
   - 数据分布/量化分析
   - 内容对比/质性分析
   - 多维度切分
   - 时序/趋势分析
   - （按需增加）

2. **外部理论查询**（2 个 Bash 并行）
   - grok：侧重实时/社区/X 信号
   - gemini：侧重结构化/框架/长推理

**默认分解策略**：
- 3 个内部 agent + 2 个外部 AI = 5 个并行任务
- 如果用户问题偏理论 → 减少内部 agent 到 1-2 个，加大外部 AI 权重
- 如果用户问题偏数据 → 加到 4-5 个内部 agent，只跑 2 个外部 AI 做交叉

**用户可覆盖**：用户明确说"只问 grok 和 gemini"或"只派内部 agent"时按用户指令。

### Phase 2：Prompt 自动生成

对每个并行任务，自动生成具体 prompt：

#### 内部 agent prompt 模板

```
你的任务是**只读数据分析**，不要修改任何文件。

## 背景
{{研究问题的 2-3 句背景描述}}

## 数据源
{{数据库路径或文件列表}}

## 任务
{{具体要查的维度，1-5 个 task}}

## 输出格式
- 结构化 markdown 报告
- 每个结论标注 n（样本数）和 置信度
- 3 屏幕内
- 纯文本返回，不要尝试写文件
```

#### grok / gemini prompt 模板

```
{{研究问题的精简描述，≤300 字}}

具体问：
(1) {{子问题 1}}
(2) {{子问题 2}}
...

请基于 2026 年上半年真实情况/最新数据回答，要具体可引用。
```

**关键要求**：问 grok 和 gemini 的 prompt **必须一致**（独立对比的前提）。

### Phase 3：并行派发（一条消息多个工具调用）

```
Tool 1: Agent (general-purpose)  run_in_background=true  [内部数据 agent A]
Tool 2: Agent (general-purpose)  run_in_background=true  [内部数据 agent B]
Tool 3: Agent (general-purpose)  run_in_background=true  [内部数据 agent C]
Tool 4: Bash run_in_background=true  [OPENCLI_BROWSER_COMMAND_TIMEOUT=300 opencli grok ask "..." --timeout 300 -f json]
Tool 5: Bash run_in_background=true  [opencli gemini ask "..." --format plain]
```

**必须在 Claude 的同一条 assistant 消息里**一次性调用多个工具，才能真正并行。

### Phase 4：等待（不要 poll）

Background agent / Bash 任务完成会**自动通知**。在等的时候，Claude 可以：

- 读现有 docs / memory 获取更多 context
- 准备输出结构
- 做初步的 Phase 5/6 分析框架

**明确禁止**：
- 不要 sleep + 轮询任务状态
- 不要主动 Read output 文件（除非收到完成通知）
- 不要抢跑做结论

### Phase 5：交叉验证 + 自动置信度分级（大版本核心）

所有结果回来后，**按 4 层分类规则**自动仲裁每个发现：

#### 分类规则矩阵

| Tier | 判定条件 | 置信度 | 处理 |
|---|---|---|---|
| 🟢 **Strong consensus** | 内部数据(n≥20) + grok + gemini **全部支持** | 高 | 可直接写进最终结论，作为硬依据 |
| 🟡 **Partial consensus** | 内部数据 + **1 家外部 AI** 支持 | 中 | 小幅建议，保留怀疑 |
| 🔴 **Conflict** | 内部数据 vs 外部 AI **矛盾** | 需仲裁 | 按仲裁原则决定 |
| ⚪ **Insufficient data** | 内部数据 n<10 且没有强外部支持 | 低 | 标为假设，需 A/B 测试 |

#### 仲裁原则（自动执行）

**原则 1：样本量门槛**
- n ≥ 20：可作为高置信度依据
- 10 ≤ n < 20：中置信度，小幅改动
- n < 10：仅观察，不作为结论
- n < 5：完全忽略

**原则 2：数据 vs 理论冲突时**
- 内部数据 n ≥ 20 → **优先内部数据**（除非外部 AI 双方都独立反对）
- 内部数据 n < 10 → **优先外部 AI 共识**（双方一致时）
- 内部数据 n < 5 → 结论待定，标为 open question

**原则 3：外部 AI 可疑概念识别**
- gemini 有时会给出疑似幻觉的概念（如"Phoenix 架构"等具体命名）
- 规则：概念名**只在 gemini 单家出现且无 grok 交叉** → 标为 "potential hallucination"，不采纳
- grok 引用的社区数据（"用户反馈说..."）→ 中等可信度

**原则 4：反直觉发现的特别处理**
- 如果 n ≥ 20 数据和常识/理论相反（如"小帖 > 大爆款"）
- 且外部 AI 共识支持
- 标注 "⚠️ 反直觉但强共识"，需要在后续跟进验证

### Phase 5.5：外部 AI 案例二次验证（大版本新增）

外部 AI 有时会给出具体的"案例"（如 `@morsyxbt 100→1600/月`），这类"单家独有案例"需要二次验证：

**验证方式**（按优先级）：

1. **用户工具直接验证**：如果是 X 账号 → 用 `twitter -c user <handle>` 查是否真实存在
2. **反向问另一家 AI**：问 gemini "你听说过 @morsyxbt 吗？" 看是否有交叉记忆
3. **Web search 验证**：让用户手动搜或用额外 web 工具

**2026-04-09 实战案例**：
- Grok 独家提到 `@morsyxbt` 100→1600/月
- Gemini 没提
- 用 `twitter -c user morsyxbt` 验证：**真实账号，10.2k followers, verified**
- 结论：账号真实，但"100→1600/月"的具体数字仍需 morsyxbt 本人 tweet 确认
- Tier：从 "单家可疑" 升级到 "单家可信案例"

**潜在幻觉的识别**：
- 如果验证失败（账号不存在/数字对不上）→ 标记为 `hallucination`，从 report 删除
- 如果部分验证（账号存在但数字未证）→ 标记为 `partial verified`，保留但降低权重

### Phase 6：自动生成改动清单（tiered action items）

输出结构：

```markdown
## Action Items (auto-generated, tiered)

### 🔴 极高置信度必做（Strong consensus，可直接落地）
1. [action] — 依据：{数据来源 + AI 共识} — 预期效果：{具体可衡量}
   - Rollback：{怎么撤销}
   - Verify：{24-48h 后如何验证}
2. ...

### 🟡 高置信度建议做（Partial consensus）
1. [action] — 依据：{单侧支持} — 前提假设：{什么条件下才成立}
2. ...

### ⚪ 待验证假设（Insufficient data）
1. [hypothesis] — 需要：{什么数据才能确认} — 建议：{A/B 测试设计}
2. ...

### 🚫 不做（Conflict / 反对证据强）
1. [originally planned action] — 反对依据：{为什么不做}
```

### Phase 7：Artifact 保存

保存到 `.omx/artifacts/multi-ai-research-<slug>-<YYYYMMDD-HHMMSS>.md`

必须包含：
1. **原始研究问题**（用户的一句话）
2. **Phase 1 问题分解**（每个任务的具体 prompt）
3. **Phase 3 并行任务列表**（task id + 命令）
4. **每个 agent 的 raw response**（N 个内部 + 2 个外部）
5. **Phase 5 交叉验证矩阵**（每个发现的置信度判定）
6. **Phase 6 改动清单**（tiered action items）
7. **用时 + 任务数**（metadata）

---

## ⚠️ 命令速查（防呆，最先看这个）

**grok 和 gemini 的有效子命令只有这些，其他都是错的：**

```bash
# ✅ Grok —— 只有一个子命令 ask
OPENCLI_BROWSER_COMMAND_TIMEOUT=300 opencli grok ask "问题" --timeout 300 -f json

# ✅ Gemini —— 5 个子命令，最常用是 ask
opencli gemini ask "问题" --format plain         # 最常用（单次问答）
opencli gemini new                               # 开新对话
opencli gemini deep-research "问题"              # Deep Research
opencli gemini deep-research-result              # 取 Deep Research 结果
opencli gemini image "画一个..."                 # 生图
```

**❌ 常见错误命令（运行会直接报 `unknown command`）**：

| ❌ 错误 | ✅ 正确 | 备注 |
|---|---|---|
| `opencli gemini chat "..."` | `opencli gemini ask "..."` | **没有 chat 子命令**（常见错误，别习惯性用） |
| `opencli gemini query "..."` | `opencli gemini ask "..."` | 没有 query |
| `opencli grok chat "..."` | `opencli grok ask "..."` | grok 只有 ask |
| `opencli grok new` | `opencli grok ask "..." --new true` | grok 的"新对话"是 ask 的参数 |

**记忆锚点**：**`ask` 是两家唯一的"问一次"命令**。不是 `chat`，不是 `query`，不是 `prompt`。

如果不确定，跑 `opencli grok --help` 或 `opencli gemini --help` 看完整子命令列表。

---

## 首次使用：安装 opencli（5 分钟一次性）

> **官方仓库**：https://github.com/jackwener/opencli
> **npm 包**：`@jackwener/opencli` ([npmjs](https://www.npmjs.com/package/@jackwener/opencli))
> **作者**：jackwener
> **License**：Apache-2.0

### 环境要求

- Node.js ≥ 20.0.0
- Chrome 或 Chromium 浏览器
- macOS / Linux / Windows 均支持

### 一、安装 opencli CLI

```bash
npm install -g @jackwener/opencli
```

验证：

```bash
opencli --version
```

### 二、安装 Browser Bridge 扩展

opencli 通过一个**轻量的 Chrome 扩展 + 本地 daemon** 复用你浏览器已登录的 session。首次运行会自动引导安装：

```bash
opencli doctor
```

按提示把扩展加载到 Chrome（通常是 `chrome://extensions` → 开发者模式 → 加载已解压的扩展，路径 doctor 会告诉你）。

### 三、登录目标 AI 网站

用装了扩展的那个 Chrome profile 打开并登录：

- https://grok.com（Premium/Premium+ 订阅）
- https://gemini.google.com（Advanced 订阅）

登录一次就行，session 会被 opencli 长期复用。

### 四、设置环境变量（必须）

```bash
# 加到 ~/.zshrc 或 ~/.bashrc
export OPENCLI_BROWSER_COMMAND_TIMEOUT=300
```

**为什么必须**：opencli 的默认 browser command timeout 是 60 秒（`runtime.js:25`），对 grok 复杂问题不够。不设这个 grok 会报 `timed out after 60s`。这是血泪教训。

### 五、可选：安装 opencli 的 AI skills

opencli 自己提供了几个 AI skill，也可以装：

```bash
npx skills add jackwener/opencli
```

（这些 skill 和 `multi-ai-research` 不冲突，是互补的。）

### 六、验证全链路

```bash
OPENCLI_BROWSER_COMMAND_TIMEOUT=300 opencli grok ask "请只回复：OK" --timeout 300 -f json
opencli gemini ask "请只回复：OK" --format plain
```

两个都返回 OK 就代表全链路通了。

---

## Phase 0: Pre-flight Prerequisites（强制检查）

运行前**必须**按顺序检查，任一失败停止流程并向用户报告：

### 0.1 CLI 可用性

```bash
# opencli 存在
which opencli || echo "🔴 opencli 未安装"
opencli --version 2>&1 | head -1

# twitter-cli 存在（如果任务涉及 X 数据）
which twitter 2>&1
```

### 0.2 环境变量（grok 必需）

```bash
echo "OPENCLI_BROWSER_COMMAND_TIMEOUT=${OPENCLI_BROWSER_COMMAND_TIMEOUT:-未设置}"
```

如果**未设置**：
- **不要静默跳过**，否则 grok 会 60s 硬截断
- 在每次 Bash 调用时**强制前置**：`OPENCLI_BROWSER_COMMAND_TIMEOUT=300 opencli grok ask ...`
- 或提示用户在 shell rc 加 `export OPENCLI_BROWSER_COMMAND_TIMEOUT=300`

### 0.3 登录状态（手动）

首次运行时提醒用户确认：
- grok.com 在 Chrome 已登录（Premium/Premium+）
- gemini.google.com 在 Chrome 已登录（Advanced）

### 0.4 Claude Code Agent 工具可用

- 当前 session 能调 `general-purpose` subagent（用于内部数据任务）
- 能用 `run_in_background=true` 参数

### 0.5 数据源健康检查（针对 domain 特定场景）

如果研究问题涉及**内部数据分析**，先跑数据健康检查：

**示例：X reply 场景**
```python
# 检查 reply_tracking 数据完整度
import sqlite3
conn = sqlite3.connect('/path/to/tracker.db')

# Pending 堆积（collector bug 指示）
stale = conn.execute("""
    SELECT COUNT(*) FROM reply_tracking
    WHERE check_stage='pending'
      AND posted_at < datetime('now', '-24 hour')
""").fetchone()[0]

# 关键字段覆盖率
by_type = conn.execute("""
    SELECT type, COUNT(*) as total,
           SUM(CASE WHEN check_stage='pending' THEN 1 ELSE 0 END) as pending
    FROM reply_tracking
    GROUP BY type
""").fetchall()

# 硬阈值判断
if stale > 50:
    print("🔴 >50 条 reply 永久 pending，疑似 collector bug，先修再 research")
for t in by_type:
    if t[1] > 10 and t[2] / t[1] > 0.5:
        print(f"🔴 type={t[0]} 的 pending 率 >50%，可能 collector 只覆盖部分 type")
```

**教训**（2026-04-09 实测发现）：@mylifcc 的 collector 只追踪 `reply/quote` 不追 `post`，导致 27 条 post 全部 pending 被当成"0 views"。**Phase 0 的 data health check 能提前暴露这种 bug**，避免"拿污染数据做调研"。

### 判定规则

| Pre-check 状态 | 行动 |
|---|---|
| 全绿 | 继续 Phase 1 |
| CLI 缺失 | 停止，告知用户安装 |
| 环境变量缺失 | 自动 Bash 前置，**不要**跳过 |
| 登录状态不明 | 告知用户浏览器确认 |
| 数据源有 bug | **先修再研究**，不要对着污染数据做结论 |

---

## 命令参考

### 并行 Bash 调用（grok + gemini）

**在 Claude Code 里通过 Bash 工具启动**，`run_in_background=true`，一条消息里多个 tool call：

```bash
# Bash call 1 (background)
OPENCLI_BROWSER_COMMAND_TIMEOUT=300 opencli grok ask "{{PROMPT}}" --timeout 300 -f json

# Bash call 2 (background)
opencli gemini ask "{{PROMPT}}" --format plain
```

两个 Bash 调用 **必须在同一条 assistant 消息里**调用，否则会串行。

### 并行 Agent 派发（内部数据）

**使用 Agent 工具**，`run_in_background=true`，一条消息里多个 tool call：

```
Agent 1: subagent_type=general-purpose, description=...
Agent 2: subagent_type=general-purpose, description=...
Agent 3: subagent_type=general-purpose, description=...
```

每个 agent 的 prompt 独立且完整（Phase 2 生成）。

### 可选：更多 AI 并行（未来扩展）

opencli 还支持其他 AI 服务（perplexity 等，持续扩展），未来可加入：

```bash
opencli perplexity ask "{{PROMPT}}" --format plain
```

---

## Error handling

### grok 超时（60s 截断）
- **根因**：`OPENCLI_BROWSER_COMMAND_TIMEOUT` 没设
- **修复**：`export OPENCLI_BROWSER_COMMAND_TIMEOUT=300`
- **不要**靠缩短 prompt 绕开（用户 2026-04-08 反馈：不要改问题改超时）

### grok 返回 "Not logged in"
- 停止，让用户在浏览器手动打开 grok.com 登录
- 不要自动重试

### gemini 返回可疑概念（Phoenix 架构等）
- Phase 5 自动标为 "potential hallucination"
- 不采纳，需要 grok 交叉验证后才能采用

### 内部 agent timeout
- 缩小 agent 任务范围（分解成 2 个小 agent）
- 或者改用直接 Bash SQL 替代

### 部分任务失败
- 如果 grok 失败但 gemini 成功 → 降级到单外部 AI
- 如果 2 个外部都失败 → 降级到"仅内部数据"调研，标注报告为 "internal only"
- 不要掩盖失败

---

## 2026-04-08 实战案例（此 skill 的设计来源）

**研究问题**：X reply deboost 机制是什么？为什么有的 reply 有流量有的没有？

**Phase 1 分解**：
- Agent A：reply views 分布分层（n=1079）
- Agent B：高/低流量 reply 内容对比（A组 10 条 vs B组 10 条）
- Agent C：时序 × 作者 × 骨架 × 热度 多维切分
- Grok：2026 Reply Guy 模式机制
- Gemini：同上（独立对比）

**Phase 3 并行派发**：5 个任务同时启动，Claude 在等的时候继续读 docs

**Phase 4 等待**：5 个任务在 5-10 分钟内陆续完成（Agent B 最慢）

**Phase 5 自动交叉验证**：

| 发现 | 内部证据 | grok | gemini | Tier |
|---|---|---|---|---|
| 不是账号级 deboost | Agent A 长尾分布 | ✅ | ✅ | 🟢 强共识 |
| 原帖热度 U 型 | Agent A+C U 型 | ✅ | ✅ | 🟢 强共识 |
| 中文 reply >> 英文 reply（1000×） | Agent B 独家 | 部分 | 部分 | 🟡 部分共识 |
| 踩坑预警 > 补充实测 | Agent A 927V vs 308V | 无意见 | 无意见 | 🟡 数据独支 |
| Reply Guy 模式 | 行为匹配 | ✅ | ✅ | 🟢 外部强共识 |
| long 回复更好 | n=0 | ✅ | ✅ | ⚪ 数据不足 |
| Phoenix 架构 | — | 无提及 | ✅ | 🚫 潜在幻觉 |

**Phase 6 自动改动清单**：
- 🔴 必做：CN:EN 10:1 / 踩坑预警首选 / 禁顶满 / 作者白黑名单 / 时段加权
- 🟡 建议：原帖热度甜区软约束 / HVC 机制
- ⚪ 待验证：long 回复效果（需 A/B 测试）
- 🚫 不做：基于 Phoenix 架构的假设（不采纳单侧幻觉）

**结果**：30 分钟从"有困惑"到"SKILL.md v8.2 → v8.3 完整改动清单"。

---

## 和其他 skill 的关系

- **ask-opencli**：单次 grok/gemini 调用，日常 second opinion。本 skill 包含 ask-opencli 的能力但扩展为多 AI 编排。
- **x-learn-reply v2**：domain-specific 版本，专门做 X reply 策略优化。内部 Phase 4/5（交叉验证 + 改动清单）复用了本 skill 的方法论。
- **cognitive-portrait**：参考了本 skill 的"主 agent 派发 sub-agent 并行"模式，但场景是单人认知画像分析。

如果你的场景是 **domain-specific 优化**（如 X reply / X post），优先用 domain 版本。如果是**通用深度调研**，用本 skill。

---

## 禁止事项

- ❌ 不跳过 Phase 0 prerequisites 检查
- ❌ 不串行调 grok 和 gemini（必须同一消息并行）
- ❌ 不 poll 等待 background task（等通知）
- ❌ 不跳过 Phase 5 置信度分级（直接把 AI 回答当结论）
- ❌ 不把单家 AI 的独有概念当事实（可能是幻觉）
- ❌ 不采纳样本 n<10 的内部数据作为高置信度依据
- ❌ 不跳过 Phase 7 artifact 保存

---

Task: {{ARGUMENTS}}
