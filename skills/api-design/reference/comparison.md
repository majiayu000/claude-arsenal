# API Style Comparison

## Quick Decision Matrix

| Factor | REST | GraphQL | gRPC |
|--------|------|---------|------|
| Learning curve | Low | Medium | High |
| Browser support | Native | Native | Needs proxy |
| Tooling maturity | Excellent | Good | Good |
| Caching | HTTP native | Complex | Manual |
| File upload | Native | Complex | Native |
| Streaming | Limited | Subscriptions | Excellent |
| Type safety | Optional | Strong | Strong |
| Code generation | Optional | Common | Required |
| Performance | Good | Good | Excellent |

---

## Decision Tree

```
Start
  │
  ├─ Public API for external developers?
  │   └─ Yes → REST (simplicity, docs, caching)
  │
  ├─ Mobile/SPA with complex data needs?
  │   └─ Yes → GraphQL (flexible queries, reduced requests)
  │
  ├─ Internal microservices communication?
  │   └─ Yes → gRPC (performance, type safety)
  │
  ├─ Real-time bidirectional streaming?
  │   └─ Yes → gRPC (native streaming)
  │
  ├─ Browser-only with real-time updates?
  │   └─ Yes → GraphQL Subscriptions
  │
  └─ Simple CRUD with standard patterns?
      └─ Yes → REST (simplicity wins)
```

---

## Detailed Comparison

### Data Fetching

**REST**
```
# Multiple requests for related data
GET /users/123
GET /users/123/orders
GET /orders/456/items

# Or use query params (non-standard)
GET /users/123?include=orders,orders.items
```

**GraphQL**
```graphql
# Single request, exact data
query {
  user(id: "123") {
    name
    orders {
      id
      items { name price }
    }
  }
}
```

**gRPC**
```protobuf
// Need to design API carefully
rpc GetUserWithOrders(GetUserRequest) returns (UserWithOrders);
// Or make multiple calls (fast due to binary protocol)
```

### Over/Under Fetching

| Problem | REST | GraphQL | gRPC |
|---------|------|---------|------|
| Over-fetching | Common | Solved | Depends on design |
| Under-fetching | Common | Solved | Depends on design |
| N+1 requests | Common | Solved (DataLoader) | Manual batching |

---

### Versioning

**REST**
```
/v1/users  →  /v2/users
# Clear but requires migration
```

**GraphQL**
```graphql
# Field deprecation
type User {
  name: String @deprecated(reason: "Use displayName")
  displayName: String
}
# Continuous evolution without versions
```

**gRPC**
```
package api.v1;  →  package api.v2;
# Similar to REST
```

---

### Error Handling

**REST**
```json
// HTTP status codes + body
// 404 Not Found
{
  "type": "https://api.example.com/errors/not-found",
  "title": "User not found",
  "status": 404
}
```

**GraphQL**
```json
// Always 200, errors in response
{
  "data": null,
  "errors": [{
    "message": "User not found",
    "extensions": { "code": "NOT_FOUND" }
  }]
}
```

**gRPC**
```
// Status codes with details
INVALID_ARGUMENT: email format invalid
WITH_DETAILS: BadRequest { field_violations: [...] }
```

---

### Caching

**REST**
```
# Native HTTP caching
Cache-Control: max-age=3600
ETag: "abc123"
# CDN-friendly
```

**GraphQL**
```
# Complex - all requests are POST to same endpoint
# Solutions:
# - Persisted queries (GET with query hash)
# - Application-level caching
# - CDN with query normalization
```

**gRPC**
```
# No built-in caching
# Manual implementation required
# Often combined with Redis/Memcached
```

---

### Real-Time Updates

**REST**
```
# Polling (inefficient)
while (true) {
  GET /orders?since=timestamp
  sleep(5s)
}

# Server-Sent Events (unidirectional)
GET /events
Content-Type: text/event-stream
```

**GraphQL**
```graphql
# Subscriptions
subscription {
  orderUpdated(orderId: "123") {
    status
    updatedAt
  }
}
```

**gRPC**
```protobuf
# Bidirectional streaming
rpc WatchOrders(stream WatchRequest) returns (stream Order);
```

---

### File Uploads

**REST**
```
POST /files
Content-Type: multipart/form-data
# Native, simple
```

**GraphQL**
```
# Not in spec, various implementations
# graphql-upload package
# Separate REST endpoint common
```

**gRPC**
```protobuf
// Client streaming
rpc UploadFile(stream FileChunk) returns (UploadResponse);
// Native, efficient for large files
```

---

## Hybrid Architectures

### REST + GraphQL

```
┌─────────────────────────────────────────┐
│              API Gateway                 │
├─────────────────┬───────────────────────┤
│  REST Endpoints │   GraphQL Endpoint    │
│  /v1/auth       │   /graphql            │
│  /v1/webhooks   │                       │
│  /v1/files      │                       │
└─────────────────┴───────────────────────┘

Use REST for:
- Authentication endpoints
- Webhooks (simple payload)
- File uploads
- Health checks

Use GraphQL for:
- Complex data queries
- Frontend-driven development
```

### GraphQL + gRPC (BFF Pattern)

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ GraphQL
┌──────▼──────┐
│     BFF     │  ← GraphQL Gateway
└──────┬──────┘
       │ gRPC
┌──────▼──────┐
│ Microservices│
└─────────────┘

BFF aggregates gRPC services
Exposes unified GraphQL API
Handles auth, rate limiting
```

---

## Performance Benchmarks

| Metric | REST (JSON) | GraphQL | gRPC (Protobuf) |
|--------|-------------|---------|-----------------|
| Payload size | 1x | ~1x | 0.3-0.5x |
| Parse time | 1x | 1x | 0.1-0.3x |
| Latency | 1x | ~1x | 0.5-0.7x |
| Throughput | 1x | ~1x | 2-3x |

*Note: Actual results vary by use case*

---

## When NOT to Use

### REST
- Complex, deeply nested data requirements
- Real-time bidirectional communication
- Strict type safety requirements

### GraphQL
- Simple CRUD with few entities
- Heavy caching requirements
- Team unfamiliar with GraphQL
- File upload heavy applications

### gRPC
- Browser-only applications
- Public APIs (unless with gateway)
- Team lacks protobuf experience
- Heavy debugging/inspection needed
