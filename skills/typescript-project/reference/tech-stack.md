# Tech Stack Reference

## Table of Contents

1. [Version Strategy](#version-strategy)
2. [Runtime](#runtime)
3. [Build Tools](#build-tools)
4. [Validation](#validation)
5. [Testing](#testing)
6. [Linting & Formatting](#linting--formatting)
7. [Database](#database)
8. [HTTP Framework](#http-framework)
9. [Decision Matrix](#decision-matrix)

---

## Version Strategy

> **Always use `latest`. This document describes capabilities, not version numbers.**

### Why No Pinned Versions

- Version numbers become outdated immediately
- `bun add` / `npm i` automatically fetches latest stable
- Lock files ensure reproducible builds
- Breaking changes are expected and handled by reading changelogs

### How to Stay Current

```bash
# Check outdated packages
bun outdated
npm outdated

# Upgrade all to latest
bun update --latest
npm update --latest

# Check for breaking changes
# Read CHANGELOG.md or release notes before major upgrades
```

### Package Installation

```bash
# Always install without version specifier
bun add zod                    # Gets latest
bun add -d @biomejs/biome      # Gets latest

# Never do this in templates
bun add zod@3.23.0             # Pinned = outdated tomorrow
```

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

**Zod 4+ Features:**
- 57% smaller bundle size
- 20x faster type-checking in IDE
- `z.templateLiteral()` for template literal types
- `@zod/mini` for edge/serverless (minimal bundle)

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

**Pros:** Smaller bundle than Zod (use when bundle size is critical)

### Comparison

| Library | Performance | DX | Best For |
|---------|-------------|-----|----------|
| Zod | Excellent | Excellent | Default choice |
| Valibot | Excellent | Good | Bundle-critical |
| @zod/mini | Excellent | Good | Edge/serverless |

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
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "assists": { "enabled": true },
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

**Biome 2.0+ Features:**
- Type-aware linting without TypeScript compiler
- Multi-file analysis and project indexing
- 340+ lint rules
- CSS and GraphQL support
- 97% Prettier compatibility

**Pros:** 100x faster than ESLint + Prettier, single tool

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

### For New Projects

| Layer | Recommended | Alternative |
|-------|-------------|-------------|
| Runtime | Bun | Node.js (LTS) |
| Build | bun build / tsup | unbuild |
| Validation | Zod | Valibot / @zod/mini |
| Testing | Bun test / Vitest | Node test runner |
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
