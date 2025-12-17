# Redis Deep Dive

## Data Structures

### Strings

```redis
# Basic operations
SET user:123:name "John"
GET user:123:name

# With expiration
SET session:abc "data" EX 3600

# Atomic increment
INCR views:page:456
INCRBY views:page:456 10

# Set if not exists
SETNX lock:resource "holder"

# Multiple operations
MSET user:1:name "Alice" user:1:email "alice@test.com"
MGET user:1:name user:1:email
```

### Hashes

```redis
# Store object
HSET user:123 name "John" email "john@test.com" age 30

# Get field
HGET user:123 name

# Get all
HGETALL user:123

# Increment field
HINCRBY user:123 login_count 1

# Check existence
HEXISTS user:123 email
```

### Lists

```redis
# Queue (FIFO)
LPUSH queue:tasks "task1"
RPOP queue:tasks

# Stack (LIFO)
LPUSH stack:items "item1"
LPOP stack:items

# Blocking pop (for workers)
BRPOP queue:tasks 30

# Get range
LRANGE notifications:user:123 0 9
```

### Sets

```redis
# Add members
SADD online_users "user:123" "user:456"

# Check membership
SISMEMBER online_users "user:123"

# Get all
SMEMBERS online_users

# Set operations
SINTER tags:post:1 tags:post:2      # Intersection
SUNION tags:post:1 tags:post:2      # Union
SDIFF online_users premium_users    # Difference
```

### Sorted Sets

```redis
# Leaderboard
ZADD leaderboard 100 "player:1" 95 "player:2" 110 "player:3"

# Get top 10
ZREVRANGE leaderboard 0 9 WITHSCORES

# Get rank
ZREVRANK leaderboard "player:1"

# Score range
ZRANGEBYSCORE leaderboard 90 100

# Increment score
ZINCRBY leaderboard 5 "player:1"
```

### Streams

```redis
# Add entry
XADD events:orders * order_id "123" total "99.99"

# Read entries
XREAD COUNT 10 STREAMS events:orders 0

# Consumer groups
XGROUP CREATE events:orders processors $ MKSTREAM

# Read as consumer
XREADGROUP GROUP processors worker1 COUNT 1 STREAMS events:orders >

# Acknowledge processing
XACK events:orders processors <message-id>
```

---

## Patterns

### Distributed Lock

```typescript
async function acquireLock(
  redis: Redis,
  key: string,
  ttl: number
): Promise<string | null> {
  const token = crypto.randomUUID();
  const acquired = await redis.set(key, token, 'EX', ttl, 'NX');
  return acquired ? token : null;
}

async function releaseLock(
  redis: Redis,
  key: string,
  token: string
): Promise<boolean> {
  // Lua script for atomic check-and-delete
  const script = `
    if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
    else
      return 0
    end
  `;
  const result = await redis.eval(script, 1, key, token);
  return result === 1;
}

// Usage
const lock = await acquireLock(redis, 'lock:order:123', 30);
if (lock) {
  try {
    await processOrder();
  } finally {
    await releaseLock(redis, 'lock:order:123', lock);
  }
}
```

### Rate Limiting

```typescript
async function checkRateLimit(
  redis: Redis,
  key: string,
  limit: number,
  windowSeconds: number
): Promise<{ allowed: boolean; remaining: number }> {
  const current = await redis.incr(key);

  if (current === 1) {
    await redis.expire(key, windowSeconds);
  }

  return {
    allowed: current <= limit,
    remaining: Math.max(0, limit - current),
  };
}

// Sliding window rate limit
async function slidingWindowRateLimit(
  redis: Redis,
  key: string,
  limit: number,
  windowMs: number
): Promise<boolean> {
  const now = Date.now();
  const windowStart = now - windowMs;

  // Remove old entries
  await redis.zremrangebyscore(key, 0, windowStart);

  // Count current window
  const count = await redis.zcard(key);

  if (count < limit) {
    // Add new entry
    await redis.zadd(key, now, `${now}:${crypto.randomUUID()}`);
    await redis.pexpire(key, windowMs);
    return true;
  }

  return false;
}
```

### Session Storage

```typescript
interface Session {
  userId: string;
  createdAt: number;
  data: Record<string, unknown>;
}

async function createSession(
  redis: Redis,
  userId: string,
  data: Record<string, unknown>
): Promise<string> {
  const sessionId = crypto.randomUUID();
  const session: Session = {
    userId,
    createdAt: Date.now(),
    data,
  };

  await redis.set(
    `session:${sessionId}`,
    JSON.stringify(session),
    'EX',
    86400 // 24 hours
  );

  // Track user sessions
  await redis.sadd(`user:${userId}:sessions`, sessionId);

  return sessionId;
}

async function getSession(redis: Redis, sessionId: string): Promise<Session | null> {
  const data = await redis.get(`session:${sessionId}`);
  return data ? JSON.parse(data) : null;
}

async function destroyAllUserSessions(redis: Redis, userId: string): Promise<void> {
  const sessions = await redis.smembers(`user:${userId}:sessions`);
  if (sessions.length > 0) {
    await redis.del(...sessions.map(s => `session:${s}`));
    await redis.del(`user:${userId}:sessions`);
  }
}
```

### Pub/Sub

```typescript
// Publisher
async function publishEvent(redis: Redis, channel: string, event: unknown) {
  await redis.publish(channel, JSON.stringify(event));
}

// Subscriber
function subscribeToEvents(redis: Redis, channel: string, handler: (event: unknown) => void) {
  const subscriber = redis.duplicate();

  subscriber.subscribe(channel, (err) => {
    if (err) throw err;
  });

  subscriber.on('message', (ch, message) => {
    if (ch === channel) {
      handler(JSON.parse(message));
    }
  });

  return () => subscriber.unsubscribe(channel);
}
```

---

## Lua Scripting

### Atomic Operations

```lua
-- Conditional update
-- KEYS[1] = key, ARGV[1] = expected, ARGV[2] = new value
local current = redis.call('GET', KEYS[1])
if current == ARGV[1] then
  redis.call('SET', KEYS[1], ARGV[2])
  return 1
else
  return 0
end
```

```typescript
// Usage
const script = `...`;
const result = await redis.eval(script, 1, 'key', 'expected', 'newValue');
```

### Increment with Max

```lua
-- Increment but don't exceed max
-- KEYS[1] = key, ARGV[1] = increment, ARGV[2] = max
local current = tonumber(redis.call('GET', KEYS[1]) or '0')
local increment = tonumber(ARGV[1])
local max = tonumber(ARGV[2])

local new_value = math.min(current + increment, max)
redis.call('SET', KEYS[1], new_value)
return new_value
```

---

## Cluster & High Availability

### Sentinel (HA)

```typescript
import Redis from 'ioredis';

const redis = new Redis({
  sentinels: [
    { host: 'sentinel-1', port: 26379 },
    { host: 'sentinel-2', port: 26379 },
    { host: 'sentinel-3', port: 26379 },
  ],
  name: 'mymaster',
});
```

### Cluster

```typescript
import Redis from 'ioredis';

const cluster = new Redis.Cluster([
  { host: 'node-1', port: 6379 },
  { host: 'node-2', port: 6379 },
  { host: 'node-3', port: 6379 },
]);

// Use hash tags for co-location
// Keys with same {tag} go to same slot
await cluster.set('user:{123}:profile', '...');
await cluster.set('user:{123}:settings', '...');
```

---

## Monitoring

### Key Metrics

```redis
# Memory usage
INFO memory

# Connected clients
INFO clients

# Operations per second
INFO stats

# Slow queries
SLOWLOG GET 10

# Key statistics
DBSIZE
INFO keyspace
```

### Memory Analysis

```redis
# Memory usage by key
MEMORY USAGE key_name

# Find big keys
redis-cli --bigkeys

# Memory doctor
MEMORY DOCTOR
```
