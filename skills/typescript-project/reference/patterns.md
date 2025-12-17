# Design Patterns Reference

## Table of Contents

1. [Result Pattern](#result-pattern)
2. [Repository Pattern](#repository-pattern)
3. [Factory Pattern](#factory-pattern)
4. [Strategy Pattern](#strategy-pattern)
5. [Builder Pattern](#builder-pattern)
6. [Middleware Pattern](#middleware-pattern)
7. [Event-Driven Pattern](#event-driven-pattern)

---

## Result Pattern

Handle success/failure without exceptions:

```typescript
// lib/result.ts
export type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export const Result = {
  ok: <T>(value: T): Result<T, never> => ({ ok: true, value }),
  err: <E>(error: E): Result<never, E> => ({ ok: false, error }),

  map: <T, U, E>(result: Result<T, E>, fn: (value: T) => U): Result<U, E> =>
    result.ok ? Result.ok(fn(result.value)) : result,

  flatMap: <T, U, E>(
    result: Result<T, E>,
    fn: (value: T) => Result<U, E>
  ): Result<U, E> => (result.ok ? fn(result.value) : result),

  unwrap: <T, E>(result: Result<T, E>): T => {
    if (!result.ok) throw result.error;
    return result.value;
  },
};

// Usage
async function findUser(id: string): Promise<Result<User, AppError>> {
  const user = await db.users.findById(id);
  if (!user) return Result.err(AppError.notFound('User', id));
  return Result.ok(user);
}

const result = await findUser('123');
if (!result.ok) {
  return res.status(404).json({ error: result.error.message });
}
const user = result.value;
```

---

## Repository Pattern

Abstract data access behind interfaces:

```typescript
// types/repository.ts
export interface Repository<T, ID = string> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<void>;
}

// services/user.repository.ts
export interface UserRepository extends Repository<User> {
  findByEmail(email: string): Promise<User | null>;
  findByRole(role: UserRole): Promise<User[]>;
}

// adapters/postgres/user.repository.ts
export class PostgresUserRepository implements UserRepository {
  constructor(private readonly db: Database) {}

  async findById(id: string): Promise<User | null> {
    const row = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return row ? this.toEntity(row) : null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const row = await this.db.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    return row ? this.toEntity(row) : null;
  }

  async save(user: User): Promise<User> {
    const row = await this.db.query(
      `INSERT INTO users (id, email, name, created_at)
       VALUES ($1, $2, $3, $4)
       ON CONFLICT (id) DO UPDATE SET email = $2, name = $3
       RETURNING *`,
      [user.id, user.email, user.name, user.createdAt]
    );
    return this.toEntity(row);
  }

  private toEntity(row: UserRow): User {
    return new User(row.id, row.email, row.name, row.created_at);
  }
}

// Testing with in-memory implementation
export class InMemoryUserRepository implements UserRepository {
  private users = new Map<string, User>();

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) ?? null;
  }

  async save(user: User): Promise<User> {
    this.users.set(user.id, user);
    return user;
  }
  // ...
}
```

---

## Factory Pattern

Encapsulate complex object creation:

```typescript
// Simple Factory
export function createLogger(config: LogConfig): Logger {
  const transports: Transport[] = [];

  if (config.console) {
    transports.push(new ConsoleTransport(config.level));
  }
  if (config.file) {
    transports.push(new FileTransport(config.file));
  }
  if (config.remote) {
    transports.push(new RemoteTransport(config.remote));
  }

  return new Logger(transports);
}

// Factory with Registry
class NotificationFactory {
  private registry = new Map<string, NotificationBuilder>();

  register(type: string, builder: NotificationBuilder) {
    this.registry.set(type, builder);
  }

  create(type: string, data: NotificationData): Notification {
    const builder = this.registry.get(type);
    if (!builder) throw new Error(`Unknown type: ${type}`);
    return builder(data);
  }
}

const factory = new NotificationFactory();
factory.register('email', (data) => new EmailNotification(data));
factory.register('sms', (data) => new SmsNotification(data));
factory.register('push', (data) => new PushNotification(data));

const notification = factory.create('email', { to: 'user@example.com' });

// Abstract Factory
interface DatabaseFactory {
  createConnection(): Connection;
  createQueryBuilder(): QueryBuilder;
  createMigrator(): Migrator;
}

class PostgresFactory implements DatabaseFactory {
  createConnection() { return new PostgresConnection(); }
  createQueryBuilder() { return new PostgresQueryBuilder(); }
  createMigrator() { return new PostgresMigrator(); }
}

class SqliteFactory implements DatabaseFactory {
  createConnection() { return new SqliteConnection(); }
  createQueryBuilder() { return new SqliteQueryBuilder(); }
  createMigrator() { return new SqliteMigrator(); }
}
```

---

## Strategy Pattern

Swap algorithms at runtime:

```typescript
// Define strategy interface
interface PricingStrategy {
  calculate(order: Order): Money;
}

// Concrete strategies
class StandardPricing implements PricingStrategy {
  calculate(order: Order): Money {
    return order.items.reduce(
      (sum, item) => sum.add(item.price.multiply(item.quantity)),
      Money.zero()
    );
  }
}

class DiscountPricing implements PricingStrategy {
  constructor(private readonly discount: Percentage) {}

  calculate(order: Order): Money {
    const subtotal = new StandardPricing().calculate(order);
    return subtotal.subtract(subtotal.multiply(this.discount));
  }
}

class TieredPricing implements PricingStrategy {
  calculate(order: Order): Money {
    const subtotal = new StandardPricing().calculate(order);
    const discount = this.getTierDiscount(subtotal);
    return subtotal.subtract(subtotal.multiply(discount));
  }

  private getTierDiscount(amount: Money): Percentage {
    if (amount.greaterThan(Money.of(1000))) return Percentage.of(20);
    if (amount.greaterThan(Money.of(500))) return Percentage.of(10);
    if (amount.greaterThan(Money.of(100))) return Percentage.of(5);
    return Percentage.zero();
  }
}

// Context
class OrderProcessor {
  constructor(private strategy: PricingStrategy) {}

  setStrategy(strategy: PricingStrategy) {
    this.strategy = strategy;
  }

  process(order: Order): ProcessedOrder {
    const total = this.strategy.calculate(order);
    return { ...order, total };
  }
}

// Usage
const processor = new OrderProcessor(new StandardPricing());
processor.setStrategy(new DiscountPricing(Percentage.of(15)));
const result = processor.process(order);
```

---

## Builder Pattern

Construct complex objects step by step:

```typescript
// Fluent Builder
class QueryBuilder<T> {
  private query: QueryConfig = { table: '', conditions: [], orderBy: [] };

  from(table: string): this {
    this.query.table = table;
    return this;
  }

  where(field: string, op: Operator, value: unknown): this {
    this.query.conditions.push({ field, op, value });
    return this;
  }

  orderBy(field: string, direction: 'asc' | 'desc' = 'asc'): this {
    this.query.orderBy.push({ field, direction });
    return this;
  }

  limit(n: number): this {
    this.query.limit = n;
    return this;
  }

  build(): Query<T> {
    if (!this.query.table) throw new Error('Table required');
    return new Query(this.query);
  }
}

// Usage
const query = new QueryBuilder<User>()
  .from('users')
  .where('status', '=', 'active')
  .where('age', '>', 18)
  .orderBy('createdAt', 'desc')
  .limit(10)
  .build();

// Builder with Director
class HttpRequestBuilder {
  private request: Partial<HttpRequest> = {};

  method(m: HttpMethod): this {
    this.request.method = m;
    return this;
  }

  url(u: string): this {
    this.request.url = u;
    return this;
  }

  header(key: string, value: string): this {
    this.request.headers = { ...this.request.headers, [key]: value };
    return this;
  }

  json(data: unknown): this {
    this.request.body = JSON.stringify(data);
    return this.header('Content-Type', 'application/json');
  }

  build(): HttpRequest {
    if (!this.request.method || !this.request.url) {
      throw new Error('Method and URL required');
    }
    return this.request as HttpRequest;
  }
}

// Director for common patterns
const ApiRequest = {
  get: (url: string) =>
    new HttpRequestBuilder().method('GET').url(url).build(),

  postJson: (url: string, data: unknown) =>
    new HttpRequestBuilder().method('POST').url(url).json(data).build(),
};
```

---

## Middleware Pattern

Chain processing functions:

```typescript
// Type definitions
type Next = () => Promise<void>;
type Middleware<C> = (ctx: C, next: Next) => Promise<void>;

// Middleware composer
function compose<C>(middlewares: Middleware<C>[]): Middleware<C> {
  return async (ctx, next) => {
    let index = -1;

    async function dispatch(i: number): Promise<void> {
      if (i <= index) throw new Error('next() called multiple times');
      index = i;

      const fn = i < middlewares.length ? middlewares[i] : next;
      if (fn) await fn(ctx, () => dispatch(i + 1));
    }

    await dispatch(0);
  };
}

// Example middlewares
const logger: Middleware<Context> = async (ctx, next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  console.log(`${ctx.method} ${ctx.path} - ${ms}ms`);
};

const errorHandler: Middleware<Context> = async (ctx, next) => {
  try {
    await next();
  } catch (error) {
    ctx.status = error.statusCode || 500;
    ctx.body = { error: error.message };
  }
};

const auth: Middleware<Context> = async (ctx, next) => {
  const token = ctx.headers.authorization?.replace('Bearer ', '');
  if (!token) throw new UnauthorizedError();
  ctx.user = await verifyToken(token);
  await next();
};

// Usage
const app = compose([errorHandler, logger, auth, router]);
```

---

## Event-Driven Pattern

Decouple components with events:

```typescript
// Event definitions
interface DomainEvents {
  'user.created': { userId: string; email: string };
  'user.verified': { userId: string };
  'order.placed': { orderId: string; userId: string; total: number };
  'order.shipped': { orderId: string; trackingNumber: string };
}

// Type-safe event emitter
class EventBus<Events extends Record<string, unknown>> {
  private handlers = new Map<keyof Events, Set<Function>>();

  on<K extends keyof Events>(
    event: K,
    handler: (payload: Events[K]) => void | Promise<void>
  ): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);

    return () => this.handlers.get(event)?.delete(handler);
  }

  async emit<K extends keyof Events>(event: K, payload: Events[K]): Promise<void> {
    const handlers = this.handlers.get(event);
    if (!handlers) return;

    await Promise.all(
      Array.from(handlers).map((handler) => handler(payload))
    );
  }
}

// Usage
const events = new EventBus<DomainEvents>();

// Subscribe
events.on('user.created', async ({ userId, email }) => {
  await sendWelcomeEmail(email);
});

events.on('user.created', async ({ userId }) => {
  await createDefaultSettings(userId);
});

events.on('order.placed', async ({ orderId, userId }) => {
  await notifyUser(userId, `Order ${orderId} confirmed`);
});

// Emit from service
class UserService {
  constructor(
    private readonly repo: UserRepository,
    private readonly events: EventBus<DomainEvents>
  ) {}

  async create(input: CreateUserInput): Promise<User> {
    const user = await this.repo.save(User.create(input));
    await this.events.emit('user.created', {
      userId: user.id,
      email: user.email,
    });
    return user;
  }
}
```

---

## Pattern Selection Guide

| Scenario | Pattern |
|----------|---------|
| Handle errors without exceptions | Result |
| Abstract data access | Repository |
| Complex object creation | Factory |
| Swappable algorithms | Strategy |
| Step-by-step construction | Builder |
| Request/response processing | Middleware |
| Decouple components | Event-Driven |
