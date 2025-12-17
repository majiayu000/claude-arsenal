---
name: typescript-project
description: Modern TypeScript project architecture guide for 2025. Use when creating new TS projects, setting up configurations, or designing project structure. Covers tech stack selection, layered architecture, and best practices.
---
# TypeScript Project Architecture

## Core Principles

- **Type safety first** — Strict mode, no `any`, Zod for runtime validation
- **ESM native** — ES Modules by default, Node 22+ / Bun
- **Layered architecture** — Separate lib/services/adapters
- **200-line limit** — No file exceeds 200 lines (see elegant-architecture skill)
- **Test reality** — Vitest/Bun test, minimal mocks

---

## Quick Start

### 1. Initialize Project

```bash
# Using Bun (recommended)
bun init
bun add -d typescript @types/bun

# Using Node.js
npm init -y
npm i -D typescript @types/node tsx
```

### 2. Apply Tech Stack

| Layer | 2025 Recommendation |
|-------|---------------------|
| Runtime | Bun / Node 22+ |
| Language | TypeScript 5.x (strict) |
| Validation | Zod |
| Testing | Vitest / Bun test |
| Build | tsup / bun build |
| Linting | Biome / ESLint + Prettier |

### 3. Use Standard Structure

```
project/
├── src/
│   ├── index.ts           # Entry point
│   ├── lib/               # Core utilities
│   │   ├── config.ts      # Configuration management
│   │   ├── errors.ts      # Custom error classes
│   │   ├── logger.ts      # Logging infrastructure
│   │   └── types.ts       # Shared type definitions
│   ├── services/          # Business logic
│   │   └── *.service.ts
│   └── adapters/          # External integrations
│       └── *.adapter.ts
├── tests/                 # Test files
│   └── *.test.ts
├── tsconfig.json
├── package.json
└── biome.json             # or eslint.config.js
```

---

## Architecture Layers

### lib/ — Core Infrastructure

Foundational code used across the entire application:

```typescript
// lib/types.ts — Shared type definitions
export interface Result<T, E = Error> {
  ok: boolean;
  data?: T;
  error?: E;
}

// lib/errors.ts — Custom errors
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// lib/config.ts — Configuration
export const config = {
  env: process.env.NODE_ENV || 'development',
  port: Number(process.env.PORT) || 3000,
  db: {
    url: process.env.DATABASE_URL!,
  },
} as const;

// lib/logger.ts — Logging (see structured-logging skill)
```

### services/ — Business Logic

Pure business logic with injected dependencies:

```typescript
// services/user.service.ts
export class UserService {
  constructor(private readonly userRepo: UserRepository) {}

  async create(input: CreateUserInput): Promise<User> {
    const existing = await this.userRepo.findByEmail(input.email);
    if (existing) throw new AppError('Email exists', 'USER_EXISTS', 409);
    return this.userRepo.save(User.create(input));
  }
}
```

### adapters/ — External Integrations

Interface with external systems (DB, APIs, file system):

```typescript
// adapters/postgres.adapter.ts
export class PostgresUserRepository implements UserRepository {
  constructor(private readonly db: Database) {}

  async findByEmail(email: string): Promise<User | null> {
    const row = await this.db.query('SELECT * FROM users WHERE email = $1', [email]);
    return row ? User.fromRow(row) : null;
  }
}
```

---

## Configuration Files

### tsconfig.json (2025)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### package.json

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "dev": "bun run --watch src/index.ts",
    "build": "bun build src/index.ts --outdir dist --target bun",
    "start": "bun dist/index.js",
    "test": "bun test",
    "typecheck": "tsc --noEmit"
  }
}
```

---

## Validation with Zod

```typescript
import { z } from 'zod';

// Define schemas
export const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().positive().optional(),
});

// Infer types from schemas
export type CreateUserInput = z.infer<typeof CreateUserSchema>;

// Validate at boundaries
export function validateInput<T>(schema: z.ZodType<T>, data: unknown): T {
  return schema.parse(data);
}
```

---

## Error Handling Pattern

```typescript
// lib/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'AppError';
    Error.captureStackTrace(this, this.constructor);
  }

  static notFound(resource: string, id: string) {
    return new AppError(`${resource} not found: ${id}`, 'NOT_FOUND', 404);
  }

  static validation(message: string, context?: Record<string, unknown>) {
    return new AppError(message, 'VALIDATION_ERROR', 400, context);
  }
}

// Usage
throw AppError.notFound('User', userId);
```

---

## Testing Strategy

```typescript
// tests/user.service.test.ts
import { describe, it, expect, beforeEach } from 'bun:test';
import { UserService } from '../src/services/user.service';
import { InMemoryUserRepository } from './helpers/in-memory-repo';

describe('UserService', () => {
  let service: UserService;
  let repo: InMemoryUserRepository;

  beforeEach(() => {
    repo = new InMemoryUserRepository();
    service = new UserService(repo);
  });

  it('creates user with valid input', async () => {
    const user = await service.create({
      email: 'test@example.com',
      name: 'Test User',
    });

    expect(user.email).toBe('test@example.com');
    expect(await repo.findByEmail('test@example.com')).toEqual(user);
  });

  it('rejects duplicate email', async () => {
    await service.create({ email: 'test@example.com', name: 'User 1' });

    expect(
      service.create({ email: 'test@example.com', name: 'User 2' })
    ).rejects.toThrow('Email exists');
  });
});
```

---

## Checklist

```markdown
## Project Setup
- [ ] TypeScript strict mode enabled
- [ ] ESM modules configured
- [ ] Biome/ESLint configured
- [ ] Testing framework ready

## Architecture
- [ ] lib/ for core utilities
- [ ] services/ for business logic
- [ ] adapters/ for external integrations
- [ ] Clear module boundaries

## Quality
- [ ] Zod schemas for validation
- [ ] Custom error classes
- [ ] Structured logging
- [ ] Tests for critical paths

## Build
- [ ] Build script configured
- [ ] Type checking in CI
- [ ] Tests in CI
```

---

## See Also

- [reference/architecture.md](reference/architecture.md) — Detailed architecture patterns
- [reference/tech-stack.md](reference/tech-stack.md) — Tech stack comparison
- [reference/patterns.md](reference/patterns.md) — Design patterns
- [elegant-architecture skill](../elegant-architecture.SKILL.md) — 200-line file limit
- [structured-logging skill](../structured-logging.SKILL.md) — Logging setup
