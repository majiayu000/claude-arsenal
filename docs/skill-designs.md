# Skill 设计文档

本文档包含 4 个新 skill 的详细设计方案。

---

## 1. api-design

### 概述

```yaml
name: api-design
description: REST/GraphQL/gRPC API 设计最佳实践。用于设计 API 接口、定义数据契约、处理版本控制。涵盖 OpenAPI 3.2、GraphQL Federation、gRPC 流式处理。
```

### 目录结构

```
skills/api-design/
├── SKILL.md                    # 核心技能文档
├── reference/
│   ├── rest.md                 # REST API 设计详解
│   ├── graphql.md              # GraphQL 设计详解
│   ├── grpc.md                 # gRPC 设计详解
│   └── comparison.md           # 三者对比与选型
└── templates/
    ├── openapi/                # OpenAPI 模板
    │   └── openapi.yaml
    ├── graphql/                # GraphQL Schema 模板
    │   └── schema.graphql
    └── grpc/                   # Protobuf 模板
        └── service.proto
```

### SKILL.md 核心内容

```markdown
# API Design

## Core Principles

- **Contract-First** — 先定义 API 规范，再实现代码
- **OpenAPI 3.2** — REST API 使用 OpenAPI 规范
- **版本控制** — URL 路径版本 `/v1/`，配合 Sunset Header
- **幂等性** — PUT/DELETE 必须幂等，POST 使用 Idempotency-Key
- **分页** — 使用 cursor-based 分页，避免 offset
- **错误响应** — RFC 7807 Problem Details 格式

---

## REST API 设计

### 资源命名

| 规则 | 示例 |
|------|------|
| 复数名词 | `/users`, `/orders` |
| 层级关系 | `/users/{id}/orders` |
| 动作用动词 | `/users/{id}/activate` (POST) |
| 查询用参数 | `/users?status=active&limit=20` |

### HTTP 方法语义

| 方法 | 用途 | 幂等 | 安全 |
|------|------|------|------|
| GET | 读取资源 | ✓ | ✓ |
| POST | 创建资源 | ✗ | ✗ |
| PUT | 完整替换 | ✓ | ✗ |
| PATCH | 部分更新 | ✗ | ✗ |
| DELETE | 删除资源 | ✓ | ✗ |

### 状态码使用

| 状态码 | 场景 |
|--------|------|
| 200 OK | 成功返回数据 |
| 201 Created | 资源创建成功 |
| 204 No Content | 删除成功 |
| 400 Bad Request | 请求格式错误 |
| 401 Unauthorized | 未认证 |
| 403 Forbidden | 无权限 |
| 404 Not Found | 资源不存在 |
| 409 Conflict | 冲突（如重复创建） |
| 422 Unprocessable Entity | 验证失败 |
| 429 Too Many Requests | 限流 |

### 错误响应格式 (RFC 7807)

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "Email format is invalid",
  "instance": "/users/123",
  "errors": [
    { "field": "email", "message": "Invalid email format" }
  ]
}
```

### 分页 (Cursor-Based)

```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTAwfQ==",
    "has_next": true,
    "limit": 20
  }
}
```

### 版本控制策略

```
# URL 版本 (推荐)
GET /v1/users
GET /v2/users

# 废弃通知
Sunset: Sat, 31 Dec 2025 23:59:59 GMT
Deprecation: true
Link: </v2/users>; rel="successor-version"
```

---

## GraphQL 设计

### Schema 设计原则

- **领域驱动** — Schema 反映业务领域，非数据库结构
- **避免过度嵌套** — 深度嵌套影响性能和追踪
- **使用 @key 明确实体** — Federation 中必须标识主键
- **描述性命名** — 便于监控和调试

### 类型定义示例

```graphql
type User @key(fields: "id") {
  id: ID!
  email: String!
  profile: UserProfile
  orders(first: Int, after: String): OrderConnection!
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

### 错误处理

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

union CreateUserPayload = User | ValidationError | ConflictError

type ValidationError {
  message: String!
  field: String
}
```

### N+1 问题解决

- 使用 DataLoader 批量加载
- 字段级 @requires/@provides 优化
- 限制查询深度和复杂度

---

## gRPC 设计

### Proto 定义规范

```protobuf
syntax = "proto3";

package api.v1;

service UserService {
  // 一元调用
  rpc GetUser(GetUserRequest) returns (User);

  // 服务端流
  rpc ListUsers(ListUsersRequest) returns (stream User);

  // 客户端流
  rpc UploadUsers(stream User) returns (UploadResponse);

  // 双向流
  rpc Chat(stream Message) returns (stream Message);
}

message User {
  string id = 1;
  string email = 2;
  google.protobuf.Timestamp created_at = 3;
}
```

### 错误处理 (Richer Error Model)

```protobuf
import "google/rpc/status.proto";
import "google/rpc/error_details.proto";

// 使用 google.rpc.Status 携带详细错误
// 通过 trailing metadata 返回
```

### 流式错误处理

```protobuf
message StreamResponse {
  oneof result {
    User user = 1;
    StreamError error = 2;
  }
}

message StreamError {
  string code = 1;
  string message = 2;
}
```

---

## 选型指南

| 场景 | 推荐 | 理由 |
|------|------|------|
| 公开 API / MVP | REST | 简单、通用、易于调试 |
| 前端驱动 / 移动端 | GraphQL | 按需获取、减少请求 |
| 微服务内部通信 | gRPC | 高性能、强类型、流式支持 |
| 实时数据 | gRPC / GraphQL Subscriptions | 双向流支持 |

---

## Checklist

- [ ] API 规范文档先于代码
- [ ] 使用标准错误格式 (RFC 7807 / GraphQL errors)
- [ ] 实现分页、限流、版本控制
- [ ] 提供 SDK / 客户端生成
- [ ] 监控 API 延迟和错误率
```

---

## 2. auth-security

### 概述

```yaml
name: auth-security
description: OAuth 2.1 + JWT 认证安全最佳实践。用于实现用户认证、API 授权、Token 管理。遵循 RFC 9700 安全标准。
```

### 目录结构

```
skills/auth-security/
├── SKILL.md                    # 核心技能文档
├── reference/
│   ├── oauth2.1.md             # OAuth 2.1 详解
│   ├── jwt.md                  # JWT 最佳实践
│   ├── session.md              # 会话管理
│   └── attacks.md              # 攻击防御
└── templates/
    ├── typescript/             # TypeScript 实现
    │   ├── auth.service.ts
    │   └── jwt.util.ts
    └── python/                 # Python 实现
        └── auth.py
```

### SKILL.md 核心内容

```markdown
# Auth Security

## Core Principles

- **OAuth 2.1** — 遵循 RFC 9700 (2025年1月发布)
- **PKCE 必须** — 所有客户端必须使用 PKCE
- **短期 Token** — Access Token 5-15 分钟过期
- **Token 轮换** — Refresh Token 单次使用后失效
- **HttpOnly 存储** — 浏览器中使用 HttpOnly Cookie
- **算法显式** — 验证时显式指定算法，不信任 Header

---

## OAuth 2.1 核心变更

### 废弃的流程

| 流程 | 状态 | 替代方案 |
|------|------|---------|
| Implicit Grant | ❌ 禁止 | Authorization Code + PKCE |
| Password Grant | ❌ 禁止 | Authorization Code + PKCE |
| 无 PKCE 的 Auth Code | ❌ 禁止 | 必须使用 PKCE |

### PKCE 实现

```typescript
import crypto from 'crypto';

function generateCodeVerifier(): string {
  return crypto.randomBytes(32).toString('base64url');
}

function generateCodeChallenge(verifier: string): string {
  return crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');
}

// 授权请求
const authUrl = new URL('https://auth.example.com/authorize');
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('client_id', CLIENT_ID);
authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
authUrl.searchParams.set('code_challenge', codeChallenge);
authUrl.searchParams.set('code_challenge_method', 'S256');
authUrl.searchParams.set('scope', 'openid profile');
```

---

## JWT 最佳实践

### 算法选择 (2025)

| 优先级 | 算法 | 说明 |
|--------|------|------|
| 1 | EdDSA | 最新最安全，量子抗性 |
| 2 | ES256 | ECDSA P-256，广泛支持 |
| 3 | PS256 | RSA-PSS，比 RS256 更安全 |
| 4 | RS256 | RSA，兼容性最好 |

### Token 结构

```typescript
interface AccessToken {
  // Header
  alg: 'ES256';
  typ: 'JWT';
  kid: string;  // Key ID for rotation

  // Payload
  iss: string;  // Issuer
  sub: string;  // Subject (user ID)
  aud: string;  // Audience
  exp: number;  // Expiration (5-15 min)
  iat: number;  // Issued at
  jti: string;  // JWT ID (unique)
  scope: string;
}
```

### 验证检查清单

```typescript
function validateJWT(token: string): Claims {
  // 1. 显式指定算法 - 防止算法混淆攻击
  const decoded = jwt.verify(token, publicKey, {
    algorithms: ['ES256'],  // 不信任 header.alg
    issuer: 'https://auth.example.com',
    audience: 'api.example.com',
  });

  // 2. 检查 Token 类型
  if (decoded.typ !== 'access') {
    throw new Error('Invalid token type');
  }

  // 3. 检查 scope
  if (!decoded.scope.includes('read:users')) {
    throw new Error('Insufficient scope');
  }

  return decoded;
}
```

### 存储策略

| 环境 | 存储位置 | 安全等级 |
|------|---------|---------|
| Web App | HttpOnly + Secure + SameSite Cookie | ✅ 高 |
| SPA | Memory + Refresh Token Rotation | ⚠️ 中 |
| Mobile | Secure Enclave / Keychain | ✅ 高 |
| Server | 环境变量 / Secret Manager | ✅ 高 |

```typescript
// Web App: HttpOnly Cookie
res.cookie('access_token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 15 * 60 * 1000,  // 15 minutes
  path: '/api',
});

// ❌ 避免: localStorage / sessionStorage
// 容易被 XSS 攻击窃取
```

---

## Refresh Token 轮换

### 流程

```
1. Client 发送 refresh_token
2. Server 验证 refresh_token
3. Server 生成新的 access_token + 新的 refresh_token
4. Server 使旧 refresh_token 失效
5. Server 返回新 tokens
6. Client 存储新 tokens
```

### 重用检测

```typescript
async function refreshTokens(refreshToken: string) {
  const stored = await db.refreshToken.findUnique({
    where: { token: refreshToken }
  });

  if (!stored) {
    throw new Error('Invalid refresh token');
  }

  if (stored.used) {
    // 检测到重用 - 可能被盗
    // 撤销该用户所有 tokens
    await db.refreshToken.deleteMany({
      where: { userId: stored.userId }
    });
    throw new Error('Refresh token reuse detected');
  }

  // 标记为已使用
  await db.refreshToken.update({
    where: { id: stored.id },
    data: { used: true }
  });

  // 生成新 tokens
  const newAccessToken = generateAccessToken(stored.userId);
  const newRefreshToken = generateRefreshToken(stored.userId);

  return { accessToken: newAccessToken, refreshToken: newRefreshToken };
}
```

---

## 攻击防御

### CSRF 防护

```typescript
// 使用 SameSite Cookie
res.cookie('session', token, {
  sameSite: 'strict',  // 或 'lax'
});

// 或使用 CSRF Token
const csrfToken = crypto.randomBytes(32).toString('hex');
```

### XSS 防护

- 使用 HttpOnly Cookie 存储 Token
- 实施 Content Security Policy
- 对用户输入进行转义

### 算法混淆攻击

```typescript
// ❌ 危险: 信任 header 中的算法
jwt.verify(token, key);  // 使用 header.alg

// ✅ 安全: 显式指定允许的算法
jwt.verify(token, key, { algorithms: ['ES256'] });
```

### Token 侧信道攻击

```typescript
// 使用 Token Binding 或 DPoP
// DPoP (Demonstration of Proof of Possession)
const dpopProof = generateDPoPProof(privateKey, {
  htm: 'POST',
  htu: 'https://api.example.com/resource',
  ath: accessTokenHash,
});
```

---

## Checklist

- [ ] 使用 OAuth 2.1 + PKCE
- [ ] Access Token 过期时间 ≤ 15 分钟
- [ ] 实现 Refresh Token 轮换
- [ ] 浏览器使用 HttpOnly Cookie
- [ ] 验证时显式指定算法
- [ ] 实现 Token 撤销机制
- [ ] 监控异常登录行为
```

---

## 3. database-patterns

### 概述

```yaml
name: database-patterns
description: PostgreSQL + Redis 数据库设计模式。用于数据建模、索引优化、缓存策略。涵盖 JSONB、分层存储、缓存一致性。
```

### 目录结构

```
skills/database-patterns/
├── SKILL.md                    # 核心技能文档
├── reference/
│   ├── postgresql.md           # PostgreSQL 详解
│   ├── redis.md                # Redis 详解
│   ├── caching.md              # 缓存模式
│   └── migrations.md           # 迁移策略
└── templates/
    ├── schema.sql              # PostgreSQL Schema 模板
    └── redis-patterns.ts       # Redis 模式示例
```

### SKILL.md 核心内容

```markdown
# Database Patterns

## Core Principles

- **PostgreSQL 为主** — 关系数据、事务、复杂查询
- **Redis 为辅** — 缓存、会话、实时数据
- **索引优先** — 先设计查询模式，再设计索引
- **JSONB 谨慎** — 结构化数据优先使用列
- **Cache-Aside** — 默认缓存模式
- **分层存储** — Hot/Warm/Cold 数据分离

---

## PostgreSQL 设计

### 数据类型选择

| 场景 | 推荐类型 | 避免 |
|------|---------|------|
| 主键 | UUID / BIGSERIAL | INT (范围有限) |
| 时间 | TIMESTAMPTZ | TIMESTAMP (无时区) |
| 金额 | NUMERIC(19,4) | FLOAT (精度问题) |
| 状态 | ENUM / TEXT CHECK | INT (可读性差) |
| 半结构化 | JSONB | JSON (无索引) |
| 全文搜索 | TSVECTOR | LIKE '%..%' |

### 索引策略

```sql
-- B-Tree: 等值、范围查询 (默认)
CREATE INDEX idx_users_email ON users(email);

-- B-Tree 复合索引: 注意列顺序
-- 最左前缀原则
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- 部分索引: 减少索引大小
CREATE INDEX idx_active_users ON users(email)
  WHERE status = 'active';

-- JSONB GIN 索引: 包含查询
CREATE INDEX idx_metadata ON products USING GIN (metadata jsonb_path_ops);

-- JSONB 表达式索引: 特定字段
CREATE INDEX idx_product_category ON products ((metadata->>'category'));
```

### JSONB 使用原则

```sql
-- ✅ 适合 JSONB
-- - 动态属性 (用户配置、元数据)
-- - 不需要 JOIN 的嵌套数据
-- - 第三方 API 原始响应

-- ❌ 避免 JSONB
-- - 需要频繁查询的字段 → 提取为列
-- - 需要 JOIN 的关系 → 使用外键
-- - 需要约束的数据 → 使用列 + CHECK

-- 混合模式 (推荐)
CREATE TABLE products (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  price NUMERIC(19,4) NOT NULL,
  category TEXT NOT NULL,           -- 提取常用字段
  metadata JSONB DEFAULT '{}'       -- 动态属性
);

-- 查询优化
SELECT * FROM products
WHERE category = 'electronics'      -- B-Tree
  AND metadata @> '{"brand": "Apple"}';  -- GIN
```

### 查询优化

```sql
-- 使用 EXPLAIN ANALYZE 验证
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE user_id = 123
  AND created_at > '2025-01-01'
ORDER BY created_at DESC
LIMIT 20;

-- 关注:
-- - Seq Scan → 需要索引
-- - Sort → 可用索引避免排序
-- - Nested Loop → 考虑 JOIN 优化
```

### 连接池配置

```typescript
// 推荐: PgBouncer 或内置连接池
const pool = new Pool({
  max: 20,                    // 最大连接数
  idleTimeoutMillis: 30000,   // 空闲超时
  connectionTimeoutMillis: 2000,
});

// 连接数公式
// max_connections = (core_count * 2) + effective_spindle_count
// 通常 20-100 足够
```

---

## Redis 设计

### 数据结构选择

| 场景 | 数据结构 | 示例 |
|------|---------|------|
| 缓存对象 | String | `user:123` → JSON |
| 计数器 | String + INCR | `views:article:456` |
| 用户会话 | Hash | `session:abc` → {userId, ...} |
| 排行榜 | Sorted Set | `leaderboard` → {userId: score} |
| 队列 | List / Stream | `tasks` → LPUSH/RPOP |
| 唯一集合 | Set | `online_users` → {userId...} |
| 实时消息 | Pub/Sub / Stream | 通知、事件 |

### Key 命名规范

```
# 格式: <entity>:<id>:<attribute>
user:123:profile
user:123:settings
order:456:items
session:abc123

# 使用冒号分隔，便于 SCAN 和管理
SCAN 0 MATCH "user:*:profile"
```

### TTL 策略

```typescript
// 根据数据类型设置 TTL
const TTL = {
  SESSION: 24 * 60 * 60,      // 24 hours
  CACHE: 15 * 60,             // 15 minutes
  RATE_LIMIT: 60,             // 1 minute
  TEMPORARY: 5 * 60,          // 5 minutes
};

await redis.set(`cache:user:${id}`, JSON.stringify(user), 'EX', TTL.CACHE);
```

---

## 缓存模式

### Cache-Aside (Lazy Loading)

```typescript
async function getUser(id: string): Promise<User> {
  // 1. 查缓存
  const cached = await redis.get(`user:${id}`);
  if (cached) {
    return JSON.parse(cached);
  }

  // 2. 缓存未命中，查数据库
  const user = await db.user.findUnique({ where: { id } });
  if (!user) {
    throw new NotFoundError('User not found');
  }

  // 3. 写入缓存
  await redis.set(`user:${id}`, JSON.stringify(user), 'EX', 900);

  return user;
}
```

### Write-Through

```typescript
async function updateUser(id: string, data: UpdateUserInput): Promise<User> {
  // 1. 更新数据库
  const user = await db.user.update({
    where: { id },
    data,
  });

  // 2. 同步更新缓存
  await redis.set(`user:${id}`, JSON.stringify(user), 'EX', 900);

  return user;
}
```

### Cache Invalidation

```typescript
async function deleteUser(id: string): Promise<void> {
  // 1. 删除数据库记录
  await db.user.delete({ where: { id } });

  // 2. 删除缓存
  await redis.del(`user:${id}`);

  // 3. 删除相关缓存
  await redis.del(`user:${id}:orders`);
  await redis.del(`user:${id}:profile`);
}
```

### 缓存穿透防护

```typescript
async function getUserSafe(id: string): Promise<User | null> {
  const cacheKey = `user:${id}`;

  const cached = await redis.get(cacheKey);

  // 空值也缓存 - 防止穿透
  if (cached === 'NULL') {
    return null;
  }

  if (cached) {
    return JSON.parse(cached);
  }

  const user = await db.user.findUnique({ where: { id } });

  if (!user) {
    // 缓存空值，短 TTL
    await redis.set(cacheKey, 'NULL', 'EX', 60);
    return null;
  }

  await redis.set(cacheKey, JSON.stringify(user), 'EX', 900);
  return user;
}
```

---

## 分层存储架构

```
┌─────────────────────────────────────────────────┐
│                   Application                    │
└─────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │  Redis  │    │ Postgres │    │ Archive │
   │  (Hot)  │    │  (Warm)  │    │  (Cold) │
   └─────────┘    └─────────┘    └─────────┘

   - 毫秒延迟      - 10ms 延迟     - 秒级延迟
   - 活跃数据      - 近期数据      - 历史数据
   - 内存存储      - SSD 存储      - 对象存储
   - TTL 自动      - 分区表        - 按需查询
     过期          - 定期归档
```

### 数据生命周期

```sql
-- 1. 热数据: Redis (实时访问)
-- 2. 温数据: PostgreSQL 主表 (近30天)
-- 3. 冷数据: PostgreSQL 分区/归档 (历史)

-- 分区表示例
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2025_q1 PARTITION OF orders
  FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');

-- 定期归档
INSERT INTO orders_archive
SELECT * FROM orders WHERE created_at < NOW() - INTERVAL '1 year';

DELETE FROM orders WHERE created_at < NOW() - INTERVAL '1 year';
```

---

## Checklist

- [ ] 主键使用 UUID 或 BIGSERIAL
- [ ] 时间字段使用 TIMESTAMPTZ
- [ ] 为常用查询创建索引
- [ ] JSONB 字段有 GIN 索引
- [ ] 使用 EXPLAIN ANALYZE 验证查询
- [ ] 配置连接池
- [ ] Redis 有明确的 TTL 策略
- [ ] 实现缓存穿透防护
- [ ] 定期归档冷数据
```

---

## 4. mcp-server-development

### 概述

```yaml
name: mcp-server-development
description: MCP (Model Context Protocol) Server 开发指南。用于构建 Claude Code 扩展工具。涵盖 Tools、Resources、Prompts 三种能力。
```

### 目录结构

```
skills/mcp-server-development/
├── SKILL.md                    # 核心技能文档
├── reference/
│   ├── protocol.md             # 协议详解
│   ├── security.md             # 安全最佳实践
│   └── testing.md              # 测试方法
└── templates/
    ├── typescript/             # TypeScript MCP Server
    │   ├── package.json
    │   ├── tsconfig.json
    │   └── src/
    │       └── index.ts
    └── python/                 # Python MCP Server
        ├── pyproject.toml
        └── server.py
```

### SKILL.md 核心内容

```markdown
# MCP Server Development

## Core Principles

- **单一职责** — 每个 Server 专注一个领域
- **最小权限** — 只请求必要的访问权限
- **输入验证** — 严格验证所有用户输入
- **错误处理** — 返回有意义的错误信息
- **幂等设计** — Tools 尽可能幂等
- **文档完善** — 每个 Tool/Resource 有清晰描述

---

## MCP 架构

```
┌─────────────────────────────────────────────────┐
│                   MCP Host                       │
│            (Claude Desktop / IDE)                │
└─────────────────────────────────────────────────┘
                        │
                   JSON-RPC
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │ Server A│    │ Server B│    │ Server C│
   │ (Files) │    │ (GitHub)│    │  (DB)   │
   └─────────┘    └─────────┘    └─────────┘
```

### 三种能力

| 类型 | 描述 | 示例 |
|------|------|------|
| **Tools** | LLM 可调用的函数 | 执行命令、API 调用 |
| **Resources** | 可读取的数据源 | 文件内容、数据库记录 |
| **Prompts** | 预定义的提示模板 | 代码审查、文档生成 |

---

## TypeScript 实现

### 项目结构

```
my-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts          # 入口点
│   ├── tools/            # Tools 定义
│   │   └── search.ts
│   ├── resources/        # Resources 定义
│   │   └── files.ts
│   └── prompts/          # Prompts 定义
│       └── review.ts
└── tests/
    └── server.test.ts
```

### package.json

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "bin": {
    "my-mcp-server": "dist/index.js"
  },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "latest",
    "zod": "latest"
  },
  "devDependencies": {
    "typescript": "latest",
    "tsx": "latest",
    "@types/node": "latest"
  }
}
```

### 基础 Server

```typescript
#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';

// 创建 Server 实例
const server = new Server(
  {
    name: 'my-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// 定义 Tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'search_files',
        description: 'Search for files matching a pattern',
        inputSchema: {
          type: 'object',
          properties: {
            pattern: {
              type: 'string',
              description: 'Glob pattern to match files',
            },
            directory: {
              type: 'string',
              description: 'Directory to search in',
            },
          },
          required: ['pattern'],
        },
      },
    ],
  };
});

// Tool 输入验证 Schema
const SearchFilesInput = z.object({
  pattern: z.string().min(1),
  directory: z.string().optional().default('.'),
});

// 处理 Tool 调用
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'search_files': {
      // 验证输入
      const input = SearchFilesInput.parse(args);

      // 安全检查: 防止路径遍历
      if (input.directory.includes('..')) {
        throw new Error('Directory traversal not allowed');
      }

      // 执行搜索
      const results = await searchFiles(input.pattern, input.directory);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(results, null, 2),
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// 定义 Resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: 'file:///config.json',
        name: 'Configuration',
        description: 'Application configuration file',
        mimeType: 'application/json',
      },
    ],
  };
});

// 处理 Resource 读取
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === 'file:///config.json') {
    const content = await fs.readFile('config.json', 'utf-8');
    return {
      contents: [
        {
          uri,
          mimeType: 'application/json',
          text: content,
        },
      ],
    };
  }

  throw new Error(`Resource not found: ${uri}`);
});

// 启动 Server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('MCP Server running on stdio');
}

main().catch(console.error);
```

---

## Python 实现

### 使用 FastMCP

```python
# server.py
from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("my-mcp-server")

class SearchInput(BaseModel):
    pattern: str
    directory: str = "."

@mcp.tool()
def search_files(input: SearchInput) -> list[str]:
    """Search for files matching a pattern.

    Args:
        input: Search parameters including pattern and directory

    Returns:
        List of matching file paths
    """
    import glob
    import os

    # 安全检查
    if ".." in input.directory:
        raise ValueError("Directory traversal not allowed")

    full_pattern = os.path.join(input.directory, input.pattern)
    return glob.glob(full_pattern, recursive=True)

@mcp.resource("file:///config.json")
def get_config() -> str:
    """Read application configuration."""
    with open("config.json") as f:
        return f.read()

@mcp.prompt()
def code_review(code: str) -> str:
    """Generate a code review prompt."""
    return f"""Please review the following code:

```
{code}
```

Focus on:
1. Security vulnerabilities
2. Performance issues
3. Code quality and maintainability
"""

if __name__ == "__main__":
    mcp.run()
```

---

## 安全最佳实践

### 输入验证

```typescript
// 1. 使用 Zod 定义严格的 Schema
const FilePathInput = z.object({
  path: z
    .string()
    .min(1)
    .refine((p) => !p.includes('..'), 'Path traversal not allowed')
    .refine((p) => !p.startsWith('/'), 'Absolute paths not allowed'),
});

// 2. 白名单目录
const ALLOWED_DIRS = ['/workspace', '/tmp'];

function validatePath(path: string): string {
  const resolved = path.resolve(path);
  if (!ALLOWED_DIRS.some((dir) => resolved.startsWith(dir))) {
    throw new Error('Access denied');
  }
  return resolved;
}
```

### 权限控制

```typescript
// 在 Server 元数据中声明需要的权限
const server = new Server({
  name: 'my-mcp-server',
  version: '1.0.0',
  permissions: {
    filesystem: {
      read: ['/workspace/**'],
      write: ['/workspace/output/**'],
    },
    network: {
      hosts: ['api.example.com'],
    },
  },
});
```

### 敏感数据处理

```typescript
// 不要在响应中暴露敏感信息
function sanitizeOutput(data: unknown): unknown {
  if (typeof data === 'object' && data !== null) {
    const sanitized = { ...data };
    delete sanitized.password;
    delete sanitized.apiKey;
    delete sanitized.secret;
    return sanitized;
  }
  return data;
}
```

---

## 测试

### 使用 MCP Inspector

```bash
# 安装 MCP Inspector
npx @modelcontextprotocol/inspector

# 运行你的 Server 进行测试
npx @modelcontextprotocol/inspector node dist/index.js
```

### 单元测试

```typescript
import { describe, it, expect } from 'vitest';
import { createTestClient } from './test-utils';

describe('search_files tool', () => {
  it('should find matching files', async () => {
    const client = await createTestClient();

    const result = await client.callTool('search_files', {
      pattern: '*.ts',
      directory: 'src',
    });

    expect(result.content[0].text).toContain('index.ts');
  });

  it('should reject path traversal', async () => {
    const client = await createTestClient();

    await expect(
      client.callTool('search_files', {
        pattern: '*.ts',
        directory: '../../../etc',
      })
    ).rejects.toThrow('Directory traversal not allowed');
  });
});
```

---

## 发布

### Claude Desktop 配置

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### NPM 发布

```bash
# 构建
npm run build

# 发布
npm publish
```

---

## Checklist

- [ ] 使用 Zod/Pydantic 验证所有输入
- [ ] 实现路径遍历防护
- [ ] 声明最小必要权限
- [ ] 每个 Tool 有清晰的描述
- [ ] 返回有意义的错误信息
- [ ] 使用 MCP Inspector 测试
- [ ] 编写单元测试
- [ ] 文档包含使用示例
```

---

## 实施计划

### 推荐顺序

1. **api-design** — 基础，其他 skill 都会用到
2. **database-patterns** — 与 api-design 配合使用
3. **auth-security** — 安全是核心需求
4. **mcp-server-development** — Claude Code 生态特定

### 工作量估计

| Skill | 文件数 | 复杂度 |
|-------|--------|--------|
| api-design | ~8 | 中 |
| auth-security | ~7 | 高 |
| database-patterns | ~6 | 中 |
| mcp-server-development | ~7 | 中 |

---

## Sources

### API Design
- [REST API Design Best Practices](https://www.postpilot.dev/blog/rest-api-design-best-practice-cheat-sheet)
- [OpenAPI Specification v3.2](https://spec.openapis.org/oas/v3.2.0.html)
- [GraphQL Federation](https://graphql.org/learn/federation/)
- [Apollo Federation Best Practices](https://www.apollographql.com/blog/introducing-the-apollo-federation-best-practices-series)
- [gRPC Error Handling](https://grpc.io/docs/guides/error/)

### Auth Security
- [RFC 9700 - OAuth 2.0 Security BCP](https://datatracker.ietf.org/doc/rfc9700/)
- [JWT Security Best Practices 2025](https://jwt.app/blog/jwt-best-practices/)
- [OAuth 2.1 Explained](https://vasundhara.io/blogs/oauth-2-1-explained-best-practices-for-web-and-mobile-app-security)
- [Auth0 Refresh Tokens Guide](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)

### Database Patterns
- [PostgreSQL JSONB Indexing](https://www.crunchydata.com/blog/indexing-jsonb-in-postgres)
- [Redis Caching Patterns - AWS](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)
- [Redis Cache-Aside Pattern](https://redis.io/blog/redis-smart-cache/)

### MCP Development
- [MCP Official Docs](https://modelcontextprotocol.io/quickstart/server)
- [MCP Tutorial - Towards Data Science](https://towardsdatascience.com/model-context-protocol-mcp-tutorial-build-your-first-mcp-server-in-6-steps/)
- [MCP Best Practices](https://modelcontextprotocol.info/docs/best-practices/)
