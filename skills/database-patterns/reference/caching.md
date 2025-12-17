# Caching Strategies

## Pattern Comparison

| Pattern | Consistency | Write Latency | Read Latency | Complexity |
|---------|-------------|---------------|--------------|------------|
| Cache-Aside | Eventual | Low | Variable | Low |
| Write-Through | Strong | High | Low | Medium |
| Write-Behind | Eventual | Very Low | Low | High |
| Read-Through | Eventual | Low | Low | Medium |

---

## Cache-Aside (Lazy Loading)

Most common pattern. Application manages both cache and database.

```typescript
class CacheAsideRepository<T> {
  constructor(
    private cache: Redis,
    private db: Database,
    private ttl: number = 900
  ) {}

  async get(id: string): Promise<T | null> {
    const cacheKey = this.getCacheKey(id);

    // 1. Try cache
    const cached = await this.cache.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // 2. Miss: load from DB
    const data = await this.db.findById(id);
    if (!data) {
      return null;
    }

    // 3. Populate cache
    await this.cache.set(cacheKey, JSON.stringify(data), 'EX', this.ttl);

    return data;
  }

  async update(id: string, data: Partial<T>): Promise<T> {
    // 1. Update database
    const updated = await this.db.update(id, data);

    // 2. Invalidate cache (don't update - avoids inconsistency)
    await this.cache.del(this.getCacheKey(id));

    return updated;
  }

  async delete(id: string): Promise<void> {
    await Promise.all([
      this.db.delete(id),
      this.cache.del(this.getCacheKey(id)),
    ]);
  }

  private getCacheKey(id: string): string {
    return `entity:${id}`;
  }
}
```

**Pros:**
- Simple to implement
- Resilient to cache failures
- Only caches accessed data

**Cons:**
- First request always slow
- Potential inconsistency window

---

## Write-Through

Every write goes to both cache and database synchronously.

```typescript
class WriteThroughRepository<T> {
  async save(id: string, data: T): Promise<T> {
    // Write to both synchronously
    const saved = await this.db.save(id, data);
    await this.cache.set(
      this.getCacheKey(id),
      JSON.stringify(saved),
      'EX',
      this.ttl
    );
    return saved;
  }

  async get(id: string): Promise<T | null> {
    // Try cache first
    const cached = await this.cache.get(this.getCacheKey(id));
    if (cached) {
      return JSON.parse(cached);
    }

    // Load and cache
    const data = await this.db.findById(id);
    if (data) {
      await this.cache.set(
        this.getCacheKey(id),
        JSON.stringify(data),
        'EX',
        this.ttl
      );
    }
    return data;
  }
}
```

**Pros:**
- Cache always consistent with DB
- Reads always fast after first write

**Cons:**
- Higher write latency
- Cache may contain unused data

---

## Write-Behind (Write-Back)

Writes go to cache immediately, database updated asynchronously.

```typescript
class WriteBehindRepository<T> {
  private writeQueue: Map<string, T> = new Map();
  private flushInterval: NodeJS.Timer;

  constructor() {
    // Periodic flush to database
    this.flushInterval = setInterval(() => this.flush(), 1000);
  }

  async save(id: string, data: T): Promise<void> {
    // Write to cache immediately
    await this.cache.set(
      this.getCacheKey(id),
      JSON.stringify(data),
      'EX',
      this.ttl
    );

    // Queue for DB write
    this.writeQueue.set(id, data);
  }

  private async flush(): Promise<void> {
    if (this.writeQueue.size === 0) return;

    const batch = new Map(this.writeQueue);
    this.writeQueue.clear();

    // Batch write to database
    await this.db.batchUpsert(Array.from(batch.entries()));
  }

  async shutdown(): Promise<void> {
    clearInterval(this.flushInterval);
    await this.flush(); // Final flush
  }
}
```

**Pros:**
- Extremely low write latency
- Batches DB writes efficiently

**Cons:**
- Risk of data loss (cache failure before flush)
- Complex error handling
- Eventual consistency

---

## Cache Invalidation Strategies

### Time-Based (TTL)

```typescript
// Simple but may serve stale data
await redis.set('key', 'value', 'EX', 300); // 5 minutes
```

### Event-Based

```typescript
// Invalidate on mutations
async function updateUser(id: string, data: UpdateInput) {
  await db.user.update({ where: { id }, data });

  // Invalidate all related caches
  await redis.del(`user:${id}`);
  await redis.del(`user:${id}:profile`);
  await redis.del(`users:list`); // List cache
}
```

### Version-Based

```typescript
// Include version in cache key
async function getUser(id: string) {
  const version = await redis.get(`user:${id}:version`);
  const cacheKey = `user:${id}:v${version}`;

  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // ... load and cache
}

async function updateUser(id: string, data: UpdateInput) {
  await db.user.update({ where: { id }, data });
  await redis.incr(`user:${id}:version`); // Increment version
}
```

---

## Cache Problems & Solutions

### Cache Stampede

Many requests hit cache miss simultaneously.

```typescript
// Solution: Distributed lock
async function getWithLock(id: string): Promise<Data> {
  const cacheKey = `data:${id}`;
  const lockKey = `lock:data:${id}`;

  // Check cache
  let data = await redis.get(cacheKey);
  if (data) return JSON.parse(data);

  // Try to acquire lock
  const locked = await redis.set(lockKey, '1', 'EX', 10, 'NX');

  if (locked) {
    try {
      // Double check
      data = await redis.get(cacheKey);
      if (data) return JSON.parse(data);

      // Load and cache
      const fresh = await loadFromDB(id);
      await redis.set(cacheKey, JSON.stringify(fresh), 'EX', 300);
      return fresh;
    } finally {
      await redis.del(lockKey);
    }
  } else {
    // Wait for other process to populate
    await sleep(100);
    return getWithLock(id);
  }
}
```

### Cache Penetration

Queries for non-existent data always hit database.

```typescript
// Solution: Cache negative results
async function getUserSafe(id: string): Promise<User | null> {
  const cached = await redis.get(`user:${id}`);

  if (cached === 'NULL') return null; // Cached non-existence
  if (cached) return JSON.parse(cached);

  const user = await db.user.findUnique({ where: { id } });

  if (user) {
    await redis.set(`user:${id}`, JSON.stringify(user), 'EX', 300);
  } else {
    await redis.set(`user:${id}`, 'NULL', 'EX', 60); // Short TTL for negative
  }

  return user;
}

// Solution: Bloom filter
// Pre-check if ID can possibly exist
```

### Cache Avalanche

Many cache entries expire at once.

```typescript
// Solution: Jittered TTL
function getJitteredTTL(baseTTL: number): number {
  const jitter = Math.random() * 60; // 0-60 seconds
  return baseTTL + jitter;
}

await redis.set('key', 'value', 'EX', getJitteredTTL(300));
```

### Hot Key

Single key receives excessive traffic.

```typescript
// Solution: Local cache + Redis
const localCache = new Map<string, { data: string; expires: number }>();

async function getHotKey(key: string): Promise<string> {
  // Check local cache first
  const local = localCache.get(key);
  if (local && local.expires > Date.now()) {
    return local.data;
  }

  // Check Redis
  const data = await redis.get(key);
  if (data) {
    // Cache locally with short TTL
    localCache.set(key, { data, expires: Date.now() + 1000 });
    return data;
  }

  // Load from source...
}
```

---

## Multi-Level Caching

```
┌─────────────┐
│  L1: Local  │  In-process, < 1ms
│   (Memory)  │  Size: 100MB
└──────┬──────┘
       │ miss
       ▼
┌─────────────┐
│ L2: Redis   │  Network, ~1ms
│  (Remote)   │  Size: 10GB
└──────┬──────┘
       │ miss
       ▼
┌─────────────┐
│ L3: Database│  Disk, ~10ms
└─────────────┘
```

```typescript
class MultiLevelCache<T> {
  private l1 = new Map<string, { data: T; expires: number }>();
  private l2: Redis;

  async get(key: string): Promise<T | null> {
    // L1: Local memory
    const l1Data = this.l1.get(key);
    if (l1Data && l1Data.expires > Date.now()) {
      return l1Data.data;
    }

    // L2: Redis
    const l2Data = await this.l2.get(key);
    if (l2Data) {
      const parsed = JSON.parse(l2Data);
      // Promote to L1
      this.l1.set(key, { data: parsed, expires: Date.now() + 1000 });
      return parsed;
    }

    return null;
  }

  async set(key: string, value: T, ttl: number): Promise<void> {
    // Write to both levels
    this.l1.set(key, { data: value, expires: Date.now() + 1000 });
    await this.l2.set(key, JSON.stringify(value), 'EX', ttl);
  }
}
```
