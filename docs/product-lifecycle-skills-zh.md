# 产品全生命周期 Skills 路线图

## 概述

本文档描述了覆盖产品从发现到落地全流程的 Claude Code Skills 体系。这些 skills 旨在帮助产品经理、开发者和团队在产品开发的每个阶段都能获得专业指导。

---

## 产品生命周期阶段

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           产品开发全流程                                     │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│  发现    │   定义   │   设计   │   开发   │   测试   │   发布   │   运营   │
│ Discovery│Definition│  Design  │ Develop  │   Test   │ Release  │ Operate  │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ product- │ prd-     │ product- │ 语言类   │ compre-  │ devops-  │ observ-  │
│ discovery│ master   │ ux-expert│ skills   │ hensive- │ excellen-│ ability- │
│          │          │          │ api-     │ testing  │ ce       │ sre      │
│          │          │          │ design   │          │          │          │
│          │          │          │ tech-    │          │          │          │
│          │          │          │ spec     │          │          │          │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
                                                                       │
                                                                       ▼
                                                              ┌────────────────┐
                                                              │ product-       │
                                                              │ analytics      │
                                                              │ (增长与优化)    │
                                                              └────────────────┘
```

---

## Skills 详细说明

### 1. product-discovery (产品发现)

**阶段:** 发现
**目标:** 识别市场机会，验证产品想法

| 能力 | 说明 |
|------|------|
| 市场调研 | TAM/SAM/SOM 分析、Porter 五力模型 |
| 用户研究 | 用户访谈、问卷设计、Ethnography |
| 竞品分析 | 功能矩阵、定位图、SWOT 分析 |
| 机会识别 | Jobs-to-be-Done、Kano 模型 |
| MVP 验证 | 精益创业方法、假设验证 |

**输出物:**
- 市场分析报告
- 用户画像 (Persona)
- 竞品分析矩阵
- 价值主张画布

---

### 2. prd-master (PRD 写作大师)

**阶段:** 定义
**目标:** 将产品想法转化为可执行的需求文档

| 能力 | 说明 |
|------|------|
| PRD 写作 | 标准 PRD 结构、模板 |
| 用户故事 | As a... I want... So that... |
| 验收标准 | Given/When/Then 格式 |
| 优先级排序 | RICE、MoSCoW、Kano |
| 需求拆解 | Epic → Story → Task |

**输出物:**
- PRD 文档
- 用户故事地图
- 需求优先级矩阵
- 发布计划

---

### 3. product-ux-expert (产品交互体验师) ✅ 已完成

**阶段:** 设计
**目标:** 设计优秀的用户体验

| 能力 | 说明 |
|------|------|
| 可用性评估 | Nielsen 10 大原则 |
| 无障碍设计 | WCAG 2.2 AA 合规 |
| 认知心理学 | Hick's Law、Fitts's Law |
| 用户旅程 | Journey Mapping |

---

### 4. technical-spec (技术方案设计)

**阶段:** 开发 (前期)
**目标:** 做出正确的技术决策

| 能力 | 说明 |
|------|------|
| 设计文档 | RFC/Design Doc 写作 |
| 技术选型 | 评估矩阵、Trade-off 分析 |
| 架构设计 | C4 模型、架构图 |
| 风险评估 | 识别与缓解策略 |

**输出物:**
- Technical Design Document
- 架构决策记录 (ADR)
- 接口定义文档
- 里程碑计划

---

### 5. devops-excellence (DevOps 卓越实践)

**阶段:** 发布
**目标:** 可靠、高效地发布产品

| 能力 | 说明 |
|------|------|
| CI/CD | GitHub Actions、GitLab CI |
| 容器化 | Docker、Kubernetes |
| IaC | Terraform、Pulumi |
| 发布策略 | 蓝绿、金丝雀、滚动 |
| 安全扫描 | SAST、DAST、SCA |

**输出物:**
- CI/CD 配置模板
- Dockerfile 最佳实践
- Kubernetes manifests
- 发布 checklist

---

### 6. observability-sre (可观测性与 SRE)

**阶段:** 运营
**目标:** 保持系统稳定运行

| 能力 | 说明 |
|------|------|
| 监控 | Prometheus、Grafana、Datadog |
| 日志 | ELK、Loki、结构化日志 |
| 追踪 | Jaeger、Zipkin、OpenTelemetry |
| SRE | SLO/SLI/SLA、事故响应 |
| 混沌工程 | 故障注入、韧性测试 |

**输出物:**
- 监控仪表盘
- 告警规则
- Runbook
- Postmortem 模板

---

### 7. product-analytics (产品数据分析)

**阶段:** 增长
**目标:** 用数据驱动产品决策

| 能力 | 说明 |
|------|------|
| 埋点设计 | 事件、属性、命名规范 |
| 指标体系 | 北极星指标、AARRR |
| 漏斗分析 | 转化率优化 |
| A/B 测试 | 实验设计、统计显著性 |
| 留存分析 | 同期群分析、生命周期 |

**输出物:**
- 埋点规范文档
- 指标看板设计
- A/B 测试计划
- 数据分析报告

---

## 现有 Skills (已完成)

| Skill | 类别 | 状态 |
|-------|------|------|
| typescript-project | 开发 | ✅ |
| golang-web | 开发 | ✅ |
| rust-project | 开发 | ✅ |
| python-project | 开发 | ✅ |
| zig-project | 开发 | ✅ |
| api-design | 开发 | ✅ |
| auth-security | 开发 | ✅ |
| database-patterns | 开发 | ✅ |
| product-ux-expert | 设计 | ✅ |
| comprehensive-testing | 测试 | ✅ |
| mcp-server-development | 开发 | ✅ |

---

## 使用方式

```bash
# 安装 skill
cp -r skills/<skill-name> ~/.claude/skills/

# 或在项目中使用
mkdir -p .claude/skills
cp -r skills/<skill-name> .claude/skills/
```

---

## 路线图

| 阶段 | Skill | 优先级 | 状态 |
|------|-------|--------|------|
| 定义 | prd-master | P0 | 待开发 |
| 发布 | devops-excellence | P0 | 待开发 |
| 运营 | observability-sre | P1 | 待开发 |
| 增长 | product-analytics | P1 | 待开发 |
| 发现 | product-discovery | P2 | 待开发 |
| 开发 | technical-spec | P2 | 待开发 |
