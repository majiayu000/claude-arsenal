# Architecture Decision Records (ADR)

> Lightweight documentation for architectural decisions that provides historical context and rationale.

## What is an ADR?

An **Architecture Decision Record (ADR)** is a document that captures a single architectural decision and its rationale. The collection of ADRs forms the **decision log** for a project.

**Key characteristics**:
- **Single decision focus** — One ADR per decision, not multiple
- **Immutable** — Once accepted, ADRs are not edited (status changes only)
- **Lightweight** — Short documents (1-2 pages), quick to write
- **Version controlled** — Stored with code, tracked in git
- **Numbered sequentially** — Easy to reference (ADR-001, ADR-002, etc.)

---

## When to Create an ADR

### Write an ADR for:

**Structural decisions**:
- Choosing a database (PostgreSQL vs MongoDB)
- Selecting a framework (React vs Vue)
- Deciding on architecture style (monolith vs microservices)

**Technology decisions**:
- Programming language selection
- Cloud provider choice
- Third-party service integration

**Process decisions**:
- Branching strategy (GitFlow vs trunk-based)
- Deployment approach (blue-green vs canary)
- Testing strategy (TDD vs test-after)

### Skip ADRs for:

- Trivial decisions (library versions)
- Temporary experiments
- Team processes unrelated to code
- Decisions easily reversed without cost

**Rule of thumb**: If future developers will ask "Why did we choose X?", write an ADR.

---

## ADR Status Lifecycle

```
┌──────────┐
│ Proposed │ ─────┐
└──────────┘      │
                  ▼
            ┌──────────┐
            │ Accepted │ ─────┐
            └──────────┘      │
                  │           │
      ┌───────────┼───────────┘
      │           │
      ▼           ▼
┌──────────┐  ┌─────────────┐
│Superseded│  │ Deprecated  │
└──────────┘  └─────────────┘
      │              │
      └──────┬───────┘
             ▼
        (linked to new ADR)
```

**Status values**:
- **Proposed**: Draft, seeking feedback
- **Accepted**: Approved and in effect
- **Deprecated**: No longer recommended, but not replaced
- **Superseded**: Replaced by a newer ADR (include link)

---

## ADR Templates

### Template 1: Michael Nygard (Original)

**Sections**: Title, Status, Context, Decision, Consequences

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need to select a database for our order management system.

Requirements:
- Strong consistency (ACID transactions)
- Complex queries (joins, aggregations)
- Structured data with relationships
- Team has SQL experience

Constraints:
- Must support 10K transactions/second
- Budget: <$500/month for managed service
- Must integrate with existing data warehouse

## Decision
We will use PostgreSQL as our primary database.

Rationale:
- Mature RDBMS with excellent ACID compliance
- Supports complex queries and joins
- JSON/JSONB for semi-structured data
- Strong community and tooling ecosystem
- Available as managed service (AWS RDS, Google Cloud SQL)
- Team already familiar with SQL

## Consequences

**Positive**:
- Strong data integrity guarantees
- Powerful query capabilities for analytics
- Wide adoption (easy to hire talent)
- Excellent performance for OLTP workloads
- Free and open-source

**Negative**:
- Vertical scaling limits (though high enough for our needs)
- Requires careful indexing for performance
- Schema migrations need planning
- Not ideal for unstructured data (mitigated by JSONB)

**Neutral**:
- Need to set up replication for high availability
- Will use connection pooling (PgBouncer) for scalability
```

---

### Template 2: Y-Statement Format

**Format**: In the context of [use case], facing [concern], we decided for [option] to achieve [quality], accepting [downside].

```markdown
# ADR-002: Use JWT for API Authentication

## Status
Accepted

## Decision Statement
In the context of building a stateless API for mobile and web clients,
facing the need to scale horizontally without session affinity,
we decided for JWT-based authentication
to achieve stateless, scalable authentication,
accepting that we cannot instantly revoke individual tokens.

## Context
- Current session-based auth requires sticky sessions
- Scaling requires horizontal scaling across multiple servers
- Mobile apps need long-lived tokens
- Database queries for session validation are 30% of total load

## Consequences

**Benefits**:
- Stateless: No shared state between servers
- Scalable: Works across load-balanced instances
- Standards-based: RFC 7519, wide library support
- Self-contained: Reduces database lookups

**Risks**:
- Token revocation requires workarounds (short TTL + refresh tokens)
- Slightly larger payload than opaque tokens
- Requires careful secret management

**Mitigations**:
- Use short-lived access tokens (15min)
- Implement refresh token rotation
- Store refresh tokens in Redis with TTL
- Use RS256 (asymmetric) for better key distribution
```

---

### Template 3: MADR (Markdown ADR)

**Sections**: Title, Status, Context, Considered Options, Decision, Pros/Cons, Consequences

```markdown
# ADR-003: Event Streaming Platform Selection

## Status
Accepted

## Context and Problem Statement
We need an event streaming platform for real-time order processing and event-driven architecture.

**Requirements**:
- Handle 50K events/second
- Guaranteed message delivery
- Event replay capability
- Multi-consumer support

**Decision drivers**:
- Performance and scalability
- Operational complexity
- Cost (managed service)
- Team expertise

## Considered Options

### Option 1: Apache Kafka
**Pros**:
- Industry standard for event streaming
- Excellent performance (millions of messages/second)
- Strong durability guarantees
- Event replay via log retention
- Available as managed service (Confluent Cloud, AWS MSK)

**Cons**:
- Complex to operate (Zookeeper, partitioning)
- Steep learning curve
- Higher operational cost

### Option 2: RabbitMQ
**Pros**:
- Simpler to set up and operate
- Good performance for our scale
- Team already familiar
- Lower cost

**Cons**:
- Not designed for event streaming (more queue-oriented)
- Limited event replay capability
- Lower throughput than Kafka

### Option 3: AWS Kinesis
**Pros**:
- Fully managed (no operational burden)
- Good integration with AWS ecosystem
- Auto-scaling

**Cons**:
- Vendor lock-in
- Higher cost at scale
- Less flexible than Kafka
- Limited retention (7 days max)

## Decision
We will use **Apache Kafka** via AWS MSK (Managed Streaming for Kafka).

**Rationale**:
- Best fit for event streaming use case
- Scalable to our growth projections
- Event replay is critical for our analytics pipeline
- MSK reduces operational burden
- Worth the learning curve for long-term benefits

## Consequences

**Positive**:
- Future-proof: Can scale to millions of events/second
- Event sourcing capabilities for audit log
- Enables real-time analytics and ML pipelines

**Negative**:
- Team needs training (budgeted 2 weeks)
- Higher cost: $500/month for MSK vs $200 for RabbitMQ
- More complex monitoring and alerting setup

**Actions**:
- [ ] Set up AWS MSK cluster (3 brokers)
- [ ] Create Kafka training plan for team
- [ ] Implement monitoring with Prometheus + Grafana
- [ ] Document topic naming conventions
- [ ] Set up schema registry (Confluent Schema Registry)
```

---

## Best Practices

### 1. Keep ADRs Short

**Target**: 1-2 pages
**Focus**: Decision and rationale, not implementation details
**Link**: Reference design docs for details

```markdown
✅ GOOD:
"We chose PostgreSQL for its ACID compliance and complex query support."

❌ TOO DETAILED:
"We configured PostgreSQL with these 15 parameters: shared_buffers=256MB,
effective_cache_size=1GB, ... and created these indexes: ..."
```

### 2. One Decision Per ADR

```markdown
❌ BAD: "Database and Caching Strategy"
   (Two decisions: database choice AND caching approach)

✅ GOOD:
   - ADR-001: "Use PostgreSQL for Primary Database"
   - ADR-002: "Use Redis for Caching Layer"
```

### 3. Immutable After Acceptance

**Don't edit approved ADRs**. Instead:
- Change status to "Superseded by ADR-XXX"
- Create new ADR with updated decision
- Preserves historical context

```markdown
# ADR-001: Use REST for API Design

## Status
~~Accepted~~ Superseded by ADR-015

## Context
...original content remains unchanged...

## Superseded By
ADR-015: Migrate to GraphQL for API Design
Reason: Client needs changed, now require flexible queries
Date: 2025-06-01
```

### 4. Store with Code

```bash
# Directory structure
docs/
└── architecture/
    └── ADRs/
        ├── 001-postgresql-database.md
        ├── 002-jwt-authentication.md
        ├── 003-kafka-event-streaming.md
        └── template.md
```

### 5. Use Consistent Numbering

- Zero-padded: `001`, `002`, ..., `010`, `011`
- Sequential (no gaps)
- Never reuse numbers

### 6. Include Dates

```markdown
## Status
Accepted (2025-12-18)

## Last Updated
2025-12-18
```

### 7. Link Related ADRs

```markdown
## Related ADRs
- ADR-001: PostgreSQL Database (provides context)
- ADR-005: Caching Strategy (complements this decision)
- Supersedes: ADR-003: MongoDB Database (replaced)
```

---

## ADR Meetings Best Practices

### Meeting Structure (30-45 minutes)

**Amazon-style readout**:
1. **Silent reading (10-15 min)**: Everyone reads ADR
2. **Written comments**: Add inline comments to doc
3. **Discussion (20-30 min)**:
   - Address clarifying questions
   - Debate concerns
   - Evaluate alternatives
4. **Decision**: Accept, reject, or request changes

### Participant Selection

**Keep it lean** (<10 people):
- Decision owner (author)
- Tech lead or architect
- Representatives from affected teams
- Domain experts (security, ops, etc.)

**Don't invite**:
- People not impacted by decision
- Observers (share ADR async instead)

### Async-First Approach

**Prefer async review when possible**:
- Share ADR in Slack/email
- Give 2-3 days for comments
- Only schedule meeting if:
  - Significant disagreement
  - Complex trade-offs need discussion
  - High-stakes decision

---

## Tools for ADR Management

### CLI Tools

**adr-tools** (Command-line):
```bash
# Install
npm install -g adr-log

# Create new ADR
adr new "Use PostgreSQL for primary database"

# Creates: docs/adr/0001-use-postgresql-for-primary-database.md

# Supersede an ADR
adr new -s 1 "Migrate to Kubernetes"

# Generate ADR graph
adr generate graph | dot -Tpng > adr-graph.png
```

**Log4brains** (Static site generator):
```bash
# Install
npm install -g log4brains

# Initialize
log4brains init

# Create ADR
log4brains adr new

# Preview
log4brains preview

# Build static site
log4brains build
```

### Integration Tools

**Backstage ADR Plugin**:
- Visualize ADRs in Backstage catalog
- Search across all ADRs
- Link to related components

**Notion/Confluence**:
- Store ADRs as database entries
- Use templates for consistency
- Built-in commenting and approval workflow

---

## ADR Review Checklist

### Before Writing
- [ ] Decision is architecturally significant
- [ ] Impact is long-term (hard to reverse)
- [ ] Affects multiple teams or systems
- [ ] Will be referenced in the future

### While Writing
- [ ] Title is clear and decision-focused
- [ ] Status is explicit
- [ ] Context explains problem and constraints
- [ ] At least 2 alternatives are considered
- [ ] Decision rationale is clear
- [ ] Consequences (positive and negative) are listed
- [ ] Related ADRs are linked
- [ ] Date is included

### After Acceptance
- [ ] Status changed to "Accepted"
- [ ] ADR is committed to version control
- [ ] Team is notified (Slack, email)
- [ ] Linked from related documentation
- [ ] Implementation started or scheduled

---

## Common ADR Topics

### Technology Selection
- Programming language choice
- Framework selection (React vs Vue vs Svelte)
- Database selection (SQL vs NoSQL)
- Cloud provider (AWS vs GCP vs Azure)
- Monitoring stack (Prometheus, Datadog, New Relic)

### Architecture Patterns
- Monolith vs Microservices
- Event-driven vs Request-response
- Synchronous vs Asynchronous communication
- REST vs GraphQL vs gRPC
- CQRS and Event Sourcing

### Data Decisions
- Database schema design approach
- Caching strategy
- Data retention policy
- Backup and disaster recovery
- Data partitioning/sharding strategy

### Security & Compliance
- Authentication mechanism
- Authorization model (RBAC, ABAC)
- Encryption approach (at-rest, in-transit)
- Secret management (Vault, AWS Secrets Manager)
- Audit logging strategy

### Development Process
- Git branching strategy
- CI/CD pipeline design
- Testing strategy (TDD, BDD, test pyramid)
- Code review process
- Deployment strategy (blue-green, canary)

---

## Anti-Patterns

### ❌ The Retroactive ADR

**Problem**: Writing ADR after decision is implemented

**Why it's bad**: Not a decision document, just documentation

**Solution**: Write ADRs BEFORE or DURING decision process

---

### ❌ The Novel

**Problem**: 10-page ADR with excessive detail

**Why it's bad**: Too long to read, hard to maintain

**Solution**: Keep to 1-2 pages. Link to design docs for details.

---

### ❌ The Solo Decision

**Problem**: ADR written and accepted without review

**Why it's bad**: Misses diverse perspectives, poor buy-in

**Solution**: Always get peer review, especially from affected teams

---

### ❌ The Eternal Draft

**Problem**: ADR stuck in "Proposed" status for months

**Why it's bad**: Creates confusion about what's approved

**Solution**: Set deadline for decision (e.g., 2 weeks). Accept, reject, or withdraw.

---

### ❌ The Design Guide

**Problem**: ADR includes implementation instructions

**Why it's bad**: ADRs should be decision records, not how-to guides

**Solution**: Keep focus on decision rationale. Link to separate design docs.

---

### ❌ The Abandoned Decision Log

**Problem**: Team stops writing ADRs after initial enthusiasm

**Why it's bad**: Loses historical context, repeats past debates

**Solution**: Make ADRs part of definition of done for architectural changes

---

## Example: Complete ADR

```markdown
# ADR-004: Use Redis for Session Storage

## Status
Accepted (2025-12-18)

## Context

Our web application currently stores user sessions in PostgreSQL. This creates performance bottlenecks:

**Current situation**:
- Session lookup on every request adds 20-50ms latency
- Sessions table has 2M rows, growing 10K/day
- Database CPU at 60% (sessions are 30% of queries)

**Requirements**:
- Support 50K concurrent sessions
- Session lookup <5ms (p95)
- Session expiration (automatic cleanup)
- High availability (no single point of failure)

**Constraints**:
- Budget: <$200/month
- Must integrate with existing Node.js app
- Team comfortable with key-value stores

## Considered Options

### Option 1: Continue with PostgreSQL
**Pros**: No migration needed, familiar
**Cons**: Doesn't solve performance problem
**Verdict**: ❌ Doesn't meet latency requirement

### Option 2: Redis
**Pros**:
- Extremely fast (<1ms latency)
- Built-in TTL (auto-cleanup)
- Excellent Node.js libraries
- Affordable ($100/month for managed)

**Cons**:
- In-memory (need persistence config)
- Requires new infrastructure

**Verdict**: ✅ Best fit for requirements

### Option 3: Memcached
**Pros**:
- Fast (similar to Redis)
- Simple to operate

**Cons**:
- No persistence
- Limited data structures
- No built-in replication

**Verdict**: ❌ Redis is superset of features

## Decision

We will use **Redis** for session storage, specifically AWS ElastiCache (Redis).

**Configuration**:
- Cache node type: cache.t3.medium (2 vCPU, 3.09 GB)
- Multi-AZ with automatic failover
- Session TTL: 24 hours
- Persistence: AOF (Append-Only File) enabled

**Migration plan**:
- Phase 1: Dual-write to PostgreSQL + Redis (1 week)
- Phase 2: Read from Redis, fallback to PostgreSQL (1 week)
- Phase 3: Redis only, archive old sessions (1 week)

## Consequences

### Positive
- **Performance**: Session lookup reduced from 50ms to <2ms (25x improvement)
- **Scalability**: Redis can handle 100K+ ops/second
- **Simplicity**: Automatic TTL removes cleanup jobs
- **Cost**: Database CPU drops 30%, saves $150/month

### Negative
- **New dependency**: Adds Redis to infrastructure (monitoring, backups)
- **Data loss risk**: If Redis crashes, sessions lost (users re-login)
- **Learning curve**: Team needs Redis training (mitigated: 2 team members already know Redis)

### Neutral
- **Storage**: Sessions move from persistent to in-memory (acceptable trade-off)
- **Complexity**: Need to manage Redis alongside PostgreSQL

## Implementation Notes

**Libraries**:
- Node.js: `ioredis` (better TypeScript support than `redis`)
- Session middleware: `connect-redis`

**Monitoring**:
- CloudWatch metrics: CPU, memory, evictions
- Alert if cache hit rate <95%

**Disaster recovery**:
- Daily snapshots (RDB)
- AOF for durability
- Multi-AZ for automatic failover

## Related ADRs
- ADR-001: PostgreSQL for primary database
- ADR-005: Caching strategy (Redis also used for API caching)

## References
- [Redis Session Storage Patterns](https://redis.io/docs/manual/patterns/session-storage/)
- [AWS ElastiCache Best Practices](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/BestPractices.html)
```

---

## ADR Template

See [templates/adr-template.md](../templates/adr-template.md) for a copy-paste ready template.

---

## References

- [GitHub: joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)
- [AWS: Master ADRs - Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [Microsoft Azure: Maintain an ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [ADR GitHub Organization](https://adr.github.io/)
- [AWS Prescriptive Guidance: ADR Process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
