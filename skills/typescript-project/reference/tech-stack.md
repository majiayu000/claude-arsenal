# Tech Stack Reference (2025)

## Table of Contents

1. [Runtime](#runtime)
2. [Build Tools](#build-tools)
3. [Validation](#validation)
4. [Testing](#testing)
5. [Linting & Formatting](#linting--formatting)
6. [Database](#database)
7. [HTTP Framework](#http-framework)
8. [Decision Matrix](#decision-matrix)

---

## Runtime

### Bun (Recommended for new projects)

```bash
# Install
curl -fsSL https://bun.sh/install | bash

# Create project
bun init

# Run
bun run src/index.ts

# Build
bun build src/index.ts --outdir dist --target bun
```

**Pros:**
- 4x faster than Node.js
- Native TypeScript support (no transpilation)
- Built-in bundler, test runner, package manager
- Drop-in Node.js compatibility

**Cons:**
- Younger ecosystem
- Some Node.js APIs not 100% compatible
- Less battle-tested in production

### Node.js 22+ (Stable choice)

```bash
# With tsx for TypeScript
npm i -D typescript tsx @types/node

# Run
npx tsx src/index.ts

# Or with ts-node
npx ts-node --esm src/index.ts
```

**Pros:**
- Most stable, battle-tested
- Largest ecosystem
- Native ESM support in v22+
- Built-in test runner

**Cons:**
- Slower than Bun
- Requires transpilation setup

### Recommendation

| Scenario | Choice |
|----------|--------|
| New project, greenfield | Bun |
| Enterprise, legacy integration | Node.js 22 |
| Serverless (AWS Lambda) | Node.js 22 |
| Edge functions (Cloudflare) | Bun |

---

## Build Tools

### tsup (Simple, fast)

```bash
npm i -D tsup
```

```typescript
// tsup.config.ts
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  clean: true,
  sourcemap: true,
});
```

**Best for:** Libraries, CLIs, simple projects

### unbuild (Universal)

```bash
npm i -D unbuild
```

```typescript
// build.config.ts
import { defineBuildConfig } from 'unbuild';

export default defineBuildConfig({
  entries: ['src/index'],
  declaration: true,
  clean: true,
  rollup: {
    emitCJS: true,
  },
});
```

**Best for:** Libraries needing CJS + ESM dual output

### Bun build (Zero config)

```bash
bun build src/index.ts --outdir dist --target bun
```

**Best for:** Bun-only projects, fastest builds

### Comparison

| Tool | Speed | Config | DTS | Watch |
|------|-------|--------|-----|-------|
| tsup | Fast | Minimal | Yes | Yes |
| unbuild | Medium | Minimal | Yes | No |
| bun build | Fastest | Zero | No | No |
| esbuild | Fastest | Manual | No | Yes |
| tsc | Slow | tsconfig | Yes | Yes |

---

## Validation

### Zod (Recommended)

```bash
bun add zod
```

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().positive().optional(),
  role: z.enum(['admin', 'user']).default('user'),
});

type User = z.infer<typeof UserSchema>;

// Parse (throws on error)
const user = UserSchema.parse(rawData);

// Safe parse (returns result)
const result = UserSchema.safeParse(rawData);
if (!result.success) {
  console.error(result.error.issues);
}
```

**Pros:**
- TypeScript-first design
- Excellent type inference
- Composable schemas
- Great error messages

### Valibot (Lightweight alternative)

```bash
bun add valibot
```

```typescript
import * as v from 'valibot';

const UserSchema = v.object({
  email: v.pipe(v.string(), v.email()),
  name: v.pipe(v.string(), v.minLength(2)),
});

type User = v.InferOutput<typeof UserSchema>;
```

**Pros:** 10x smaller bundle than Zod

### Comparison

| Library | Bundle Size | Performance | DX |
|---------|-------------|-------------|-----|
| Zod | ~12KB | Good | Excellent |
| Valibot | ~1KB | Excellent | Good |
| Yup | ~15KB | Slow | Good |
| io-ts | ~8KB | Good | Complex |

---

## Testing

### Vitest (Recommended for Node.js)

```bash
npm i -D vitest
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
    },
  },
});
```

```typescript
// user.test.ts
import { describe, it, expect, beforeEach } from 'vitest';

describe('UserService', () => {
  it('creates user', async () => {
    const user = await service.create({ email: 'test@test.com' });
    expect(user.email).toBe('test@test.com');
  });
});
```

### Bun Test (Recommended for Bun)

```typescript
// user.test.ts
import { describe, it, expect, beforeEach } from 'bun:test';

describe('UserService', () => {
  it('creates user', async () => {
    const user = await service.create({ email: 'test@test.com' });
    expect(user.email).toBe('test@test.com');
  });
});
```

```bash
bun test
bun test --coverage
```

### Comparison

| Framework | Speed | Watch | Coverage | Mocking |
|-----------|-------|-------|----------|---------|
| Vitest | Fast | Yes | V8/Istanbul | Built-in |
| Bun test | Fastest | Yes | Built-in | Built-in |
| Jest | Medium | Yes | Istanbul | Built-in |
| Node test | Fast | Yes | V8 | Manual |

---

## Linting & Formatting

### Biome (Recommended)

```bash
bun add -D @biomejs/biome
npx @biomejs/biome init
```

```json
// biome.json
{
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": { "recommended": true }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  }
}
```

**Pros:** Faster than ESLint + Prettier combined, single tool

### ESLint + Prettier (Traditional)

```bash
npm i -D eslint prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

**Pros:** Largest ecosystem, most plugins

### Comparison

| Tool | Speed | Plugins | Config |
|------|-------|---------|--------|
| Biome | 100x faster | Limited | Simple |
| ESLint | Slow | Extensive | Complex |
| oxlint | Fast | Growing | Simple |

---

## Database

### Drizzle ORM (Recommended)

```bash
bun add drizzle-orm
bun add -D drizzle-kit
```

```typescript
// schema.ts
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});

// queries
const allUsers = await db.select().from(users);
const user = await db.select().from(users).where(eq(users.id, 1));
```

**Pros:** Type-safe, SQL-like syntax, lightweight

### Prisma (Alternative)

```bash
npm i prisma @prisma/client
```

**Pros:** Great DX, migrations, Prisma Studio

**Cons:** Heavier, slower cold starts

### Comparison

| ORM | Type Safety | Performance | Learning Curve |
|-----|-------------|-------------|----------------|
| Drizzle | Excellent | Excellent | Medium |
| Prisma | Excellent | Good | Low |
| Kysely | Excellent | Excellent | Medium |
| TypeORM | Good | Medium | High |

---

## HTTP Framework

### Hono (Recommended)

```bash
bun add hono
```

```typescript
import { Hono } from 'hono';

const app = new Hono();

app.get('/users/:id', async (c) => {
  const id = c.req.param('id');
  const user = await userService.findById(id);
  return c.json(user);
});

export default app;
```

**Pros:** Ultrafast, works everywhere (Bun, Node, Cloudflare, Deno)

### Fastify (Alternative)

```bash
npm i fastify
```

**Pros:** Fast, mature ecosystem, validation built-in

### Comparison

| Framework | Performance | Ecosystem | Portability |
|-----------|-------------|-----------|-------------|
| Hono | Fastest | Growing | Universal |
| Fastify | Very Fast | Large | Node only |
| Express | Slow | Largest | Node only |
| Elysia | Fastest | Small | Bun only |

---

## Decision Matrix

### For New Projects (2025)

| Layer | Recommended | Alternative |
|-------|-------------|-------------|
| Runtime | Bun | Node.js 22 |
| Build | bun build / tsup | unbuild |
| Validation | Zod | Valibot |
| Testing | Bun test / Vitest | Jest |
| Linting | Biome | ESLint |
| Database | Drizzle | Prisma |
| HTTP | Hono | Fastify |

### Stack Combinations

**Speed-optimized (Bun stack):**
```
Bun + Hono + Drizzle + Zod + Biome
```

**Stability-optimized (Node stack):**
```
Node 22 + Fastify + Prisma + Zod + ESLint
```

**Minimal bundle (Edge stack):**
```
Bun + Hono + Valibot + Biome
```
