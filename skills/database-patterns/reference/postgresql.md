# PostgreSQL Deep Dive

## Advanced Data Types

### Arrays

```sql
-- Array column
CREATE TABLE posts (
  id UUID PRIMARY KEY,
  title TEXT NOT NULL,
  tags TEXT[] DEFAULT '{}'
);

-- Insert
INSERT INTO posts (id, title, tags)
VALUES (uuid_generate_v4(), 'Hello', ARRAY['tech', 'tutorial']);

-- Query: Contains element
SELECT * FROM posts WHERE 'tech' = ANY(tags);

-- Query: Contains all elements
SELECT * FROM posts WHERE tags @> ARRAY['tech', 'tutorial'];

-- Index for array operations
CREATE INDEX idx_posts_tags ON posts USING GIN (tags);
```

### JSONB Operations

```sql
-- Access operators
SELECT
  metadata->>'name' as name,        -- Text extraction
  metadata->'address' as address,   -- JSON extraction
  metadata#>>'{address,city}' as city,  -- Nested text
  metadata @> '{"active": true}' as is_active  -- Containment
FROM users;

-- Update operations
UPDATE users SET metadata = metadata || '{"verified": true}';  -- Merge
UPDATE users SET metadata = metadata - 'oldField';              -- Remove key
UPDATE users SET metadata = jsonb_set(metadata, '{nested,key}', '"value"');

-- Array in JSONB
SELECT * FROM products
WHERE metadata->'features' ? 'waterproof';  -- Has element

-- JSONB aggregation
SELECT
  metadata->>'category' as category,
  COUNT(*) as count
FROM products
GROUP BY metadata->>'category';
```

### Full-Text Search

```sql
-- Create tsvector column
ALTER TABLE articles ADD COLUMN search_vector TSVECTOR;

-- Populate
UPDATE articles SET search_vector =
  setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
  setweight(to_tsvector('english', coalesce(body, '')), 'B');

-- Index
CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- Search
SELECT *, ts_rank(search_vector, query) as rank
FROM articles, plainto_tsquery('english', 'database optimization') query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- Auto-update trigger
CREATE TRIGGER articles_search_update
BEFORE INSERT OR UPDATE ON articles
FOR EACH ROW EXECUTE FUNCTION
  tsvector_update_trigger(search_vector, 'pg_catalog.english', title, body);
```

---

## Advanced Indexing

### Index Types Comparison

| Type | Use Case | Operations |
|------|----------|------------|
| B-Tree | Equality, range, sorting | `=`, `<`, `>`, `BETWEEN`, `ORDER BY` |
| Hash | Equality only | `=` |
| GIN | Arrays, JSONB, full-text | `@>`, `?`, `@@` |
| GiST | Geometric, range, full-text | `&&`, `@>`, `<->` |
| BRIN | Large sorted tables | Range queries on sequential data |

### Covering Indexes (Index-Only Scans)

```sql
-- Include non-key columns
CREATE INDEX idx_orders_covering ON orders (user_id, created_at)
INCLUDE (status, total);

-- Query uses index only (no table access)
SELECT status, total
FROM orders
WHERE user_id = $1 AND created_at > $2;
```

### Partial Indexes

```sql
-- Index only relevant rows
CREATE INDEX idx_pending_orders ON orders (created_at)
WHERE status = 'pending';

-- Much smaller than full index
-- Query must match WHERE clause
SELECT * FROM orders
WHERE status = 'pending' AND created_at > NOW() - INTERVAL '1 day';
```

### Expression Indexes

```sql
-- Index on expression
CREATE INDEX idx_users_email_lower ON users (LOWER(email));

-- Query must use same expression
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- JSONB field
CREATE INDEX idx_users_role ON users ((metadata->>'role'));
SELECT * FROM users WHERE metadata->>'role' = 'admin';
```

---

## Query Optimization

### EXPLAIN Output

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = $1;

-- Key metrics:
-- Planning Time: Query planning duration
-- Execution Time: Actual execution duration
-- Buffers: shared hit (cache) vs read (disk)
-- Rows: Estimated vs Actual
```

### Common Issues

```sql
-- ❌ Seq Scan on large table
Seq Scan on orders (cost=0.00..1234.00 rows=10000 width=100)
-- Fix: Add index on filter columns

-- ❌ Index not used
-- Possible causes:
-- 1. Statistics outdated → ANALYZE table
-- 2. Low selectivity → Consider partial index
-- 3. Type mismatch → Cast appropriately
-- 4. Function on column → Use expression index

-- ❌ Sort operation
Sort (cost=1000.00..1050.00 rows=10000 width=100)
  Sort Key: created_at
-- Fix: Add index matching ORDER BY

-- ❌ Nested Loop with many rows
Nested Loop (cost=0.00..100000.00 rows=1000000 width=200)
-- Fix: Ensure join columns are indexed
```

### Statistics

```sql
-- Update statistics
ANALYZE users;
ANALYZE orders;

-- View statistics
SELECT
  schemaname,
  tablename,
  n_live_tup,
  n_dead_tup,
  last_vacuum,
  last_analyze
FROM pg_stat_user_tables;

-- Adjust statistics target for important columns
ALTER TABLE orders ALTER COLUMN user_id SET STATISTICS 1000;
ANALYZE orders;
```

---

## Concurrency

### Isolation Levels

```sql
-- Read Committed (default)
-- Sees committed data at statement start
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Repeatable Read
-- Sees snapshot from transaction start
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Serializable
-- Full isolation, may fail with serialization error
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

### Locking

```sql
-- Row-level lock
SELECT * FROM accounts WHERE id = $1 FOR UPDATE;

-- Skip locked rows (useful for queue processing)
SELECT * FROM tasks
WHERE status = 'pending'
ORDER BY created_at
LIMIT 1
FOR UPDATE SKIP LOCKED;

-- Advisory locks (application-level)
SELECT pg_advisory_lock(hashtext('process-orders'));
-- ... do work ...
SELECT pg_advisory_unlock(hashtext('process-orders'));
```

### Deadlock Prevention

```sql
-- Always lock in consistent order
-- ❌ Bad: Different order in different transactions
-- Transaction 1: UPDATE accounts SET ... WHERE id = 1; UPDATE accounts SET ... WHERE id = 2;
-- Transaction 2: UPDATE accounts SET ... WHERE id = 2; UPDATE accounts SET ... WHERE id = 1;

-- ✅ Good: Same order everywhere
SELECT * FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;
```

---

## Partitioning

### Range Partitioning

```sql
CREATE TABLE events (
  id UUID NOT NULL,
  type TEXT NOT NULL,
  payload JSONB,
  created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE events_2025_01 PARTITION OF events
  FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE events_2025_02 PARTITION OF events
  FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Auto-create future partitions (pg_partman extension)
```

### List Partitioning

```sql
CREATE TABLE orders (
  id UUID NOT NULL,
  region TEXT NOT NULL,
  total NUMERIC(19,4)
) PARTITION BY LIST (region);

CREATE TABLE orders_us PARTITION OF orders FOR VALUES IN ('US');
CREATE TABLE orders_eu PARTITION OF orders FOR VALUES IN ('EU', 'UK');
CREATE TABLE orders_asia PARTITION OF orders FOR VALUES IN ('JP', 'CN', 'KR');
```

### Hash Partitioning

```sql
CREATE TABLE sessions (
  id UUID NOT NULL,
  user_id UUID NOT NULL,
  data JSONB
) PARTITION BY HASH (user_id);

CREATE TABLE sessions_0 PARTITION OF sessions FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE sessions_1 PARTITION OF sessions FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE sessions_2 PARTITION OF sessions FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE sessions_3 PARTITION OF sessions FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

---

## Performance Tuning

### Key Parameters

```sql
-- Memory
shared_buffers = '256MB'        -- 25% of RAM for dedicated server
effective_cache_size = '768MB'  -- 75% of RAM
work_mem = '64MB'               -- Per-operation memory
maintenance_work_mem = '128MB'  -- For VACUUM, CREATE INDEX

-- Connections
max_connections = 100           -- Keep low, use pooler

-- WAL
wal_buffers = '16MB'
checkpoint_completion_target = 0.9

-- Query planning
random_page_cost = 1.1          -- For SSD (default 4.0 for HDD)
effective_io_concurrency = 200  -- For SSD
```

### Connection Pooling with PgBouncer

```ini
[databases]
myapp = host=localhost dbname=myapp

[pgbouncer]
listen_port = 6432
auth_type = md5
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```
