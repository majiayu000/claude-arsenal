# Architecture Reference

## Table of Contents

1. [Layered Architecture](#layered-architecture)
2. [Directory Structure Patterns](#directory-structure-patterns)
3. [Module Organization](#module-organization)
4. [Dependency Flow](#dependency-flow)
5. [Composition Root](#composition-root)

---

## Layered Architecture

### Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      ENTRY POINTS                            │
│         CLI / HTTP Server / Message Queue Consumer           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       SERVICES                               │
│              Business Logic & Use Cases                      │
│         UserService, OrderService, PaymentService            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       ADAPTERS                               │
│              External System Integrations                    │
│      PostgresRepo, StripeGateway, S3Storage, RedisCache      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         LIB                                  │
│                  Core Infrastructure                         │
│         Config, Logger, Errors, Types, Utils                 │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility | Example |
|-------|----------------|---------|
| **Entry** | Handle I/O, routing, serialization | HTTP handlers, CLI commands |
| **Services** | Business rules, orchestration | `UserService.register()` |
| **Adapters** | External system communication | Database queries, API calls |
| **Lib** | Shared utilities, types | Config, logging, error classes |

### Dependency Rule

> **Dependencies point inward.** Entry → Services → Adapters → Lib

- Services depend on Adapter interfaces, not implementations
- Adapters depend on Lib, never on Services
- Lib depends on nothing internal

---

## Directory Structure Patterns

### Pattern A: Flat (Small Projects)

```
src/
├── index.ts
├── config.ts
├── logger.ts
├── types.ts
├── user.service.ts
├── user.repository.ts
└── user.controller.ts
```

Best for: < 10 files, single developer, simple CRUD

### Pattern B: Layered (Medium Projects)

```
src/
├── index.ts
├── lib/
│   ├── config.ts
│   ├── errors.ts
│   ├── logger.ts
│   └── types.ts
├── services/
│   ├── user.service.ts
│   └── order.service.ts
├── adapters/
│   ├── postgres/
│   │   ├── user.repository.ts
│   │   └── order.repository.ts
│   └── stripe/
│       └── payment.gateway.ts
└── http/
    ├── server.ts
    ├── routes/
    └── middleware/
```

Best for: 10-50 files, small team, multiple integrations

### Pattern C: Feature Modules (Large Projects)

```
src/
├── index.ts
├── shared/
│   ├── lib/
│   ├── types/
│   └── middleware/
├── modules/
│   ├── user/
│   │   ├── index.ts          # Public exports
│   │   ├── user.types.ts
│   │   ├── user.service.ts
│   │   ├── user.repository.ts
│   │   └── user.controller.ts
│   ├── order/
│   │   ├── index.ts
│   │   ├── order.types.ts
│   │   ├── order.service.ts
│   │   └── order.repository.ts
│   └── payment/
│       ├── index.ts
│       ├── payment.types.ts
│       └── payment.service.ts
└── http/
    └── server.ts
```

Best for: > 50 files, multiple teams, complex domain

---

## Module Organization

### Single File Module

```typescript
// user.service.ts (< 200 lines)
export interface UserService { ... }
export class UserServiceImpl implements UserService { ... }
export function createUserService(deps: UserServiceDeps): UserService { ... }
```

### Folder Module

When a module exceeds 200 lines, convert to folder:

```
user/
├── index.ts          # Public API only
├── types.ts          # Interfaces, types
├── service.ts        # Business logic
├── repository.ts     # Data access
├── validation.ts     # Input validation
└── errors.ts         # Domain-specific errors
```

### Index File Pattern

```typescript
// user/index.ts — Only exports, no implementation
export type { User, CreateUserInput, UserService } from './types';
export { UserServiceImpl } from './service';
export { PostgresUserRepository } from './repository';
export { createUserModule } from './factory';
```

---

## Dependency Flow

### Interface Segregation

```typescript
// services/user.service.ts
// Define what you NEED, not what exists
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<User>;
}

export class UserService {
  constructor(private readonly repo: UserRepository) {}
}

// adapters/postgres/user.repository.ts
// Implement what services need
export class PostgresUserRepository implements UserRepository {
  constructor(private readonly db: Database) {}

  async findById(id: string): Promise<User | null> { ... }
  async save(user: User): Promise<User> { ... }
}
```

### Dependency Injection

```typescript
// Constructor injection (preferred)
class OrderService {
  constructor(
    private readonly orderRepo: OrderRepository,
    private readonly userService: UserService,
    private readonly paymentGateway: PaymentGateway
  ) {}
}

// Factory function injection
function createOrderService(deps: {
  orderRepo: OrderRepository;
  userService: UserService;
  paymentGateway: PaymentGateway;
}): OrderService {
  return new OrderService(deps.orderRepo, deps.userService, deps.paymentGateway);
}
```

---

## Composition Root

Wire dependencies at application startup:

```typescript
// src/index.ts or src/container.ts
import { config } from './lib/config';
import { createDatabase } from './lib/database';
import { PostgresUserRepository } from './adapters/postgres/user.repository';
import { StripePaymentGateway } from './adapters/stripe/payment.gateway';
import { UserService } from './services/user.service';
import { OrderService } from './services/order.service';
import { createHttpServer } from './http/server';

export async function bootstrap() {
  // 1. Infrastructure
  const db = await createDatabase(config.db);

  // 2. Adapters
  const userRepo = new PostgresUserRepository(db);
  const paymentGateway = new StripePaymentGateway(config.stripe);

  // 3. Services
  const userService = new UserService(userRepo);
  const orderService = new OrderService(orderRepo, userService, paymentGateway);

  // 4. Entry points
  const server = createHttpServer({
    userService,
    orderService,
  });

  await server.listen(config.port);
}

bootstrap();
```

### Benefits

- All dependencies visible in one place
- Easy to swap implementations (testing, different environments)
- No hidden global state
- Clear startup sequence
