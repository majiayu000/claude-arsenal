# REST API Deep Dive

## Request/Response Design

### Content Negotiation

```
# Request
Accept: application/json
Content-Type: application/json

# Response
Content-Type: application/json; charset=utf-8
```

### Standard Headers

| Header | Purpose | Example |
|--------|---------|---------|
| Authorization | Auth token | `Bearer eyJ...` |
| Accept | Response format | `application/json` |
| Content-Type | Request body format | `application/json` |
| Idempotency-Key | Prevent duplicates | UUID |
| X-Request-ID | Request tracing | UUID |
| X-RateLimit-* | Rate limit info | See below |

---

## Advanced Patterns

### Filtering

```
# Simple equality
GET /users?status=active

# Multiple values (OR)
GET /users?status=active,pending

# Comparison operators
GET /orders?total[gte]=100&total[lt]=1000
GET /users?created_at[after]=2025-01-01

# Full-text search
GET /products?q=laptop

# Nested filtering
GET /orders?user.country=US
```

### Sorting

```
# Single field
GET /users?sort=created_at

# Descending
GET /users?sort=-created_at

# Multiple fields
GET /users?sort=-created_at,name
```

### Field Selection (Sparse Fieldsets)

```
# Only return specific fields
GET /users?fields=id,name,email

# Nested fields
GET /orders?fields=id,total,user.name
```

### Embedding Related Resources

```
# Include related resources
GET /orders?include=user,items

# Response
{
  "data": {
    "id": "order-123",
    "total": 99.99,
    "user": { "id": "user-456", "name": "John" },
    "items": [...]
  }
}
```

---

## Bulk Operations

### Batch Create

```
POST /users/batch
Content-Type: application/json

{
  "users": [
    { "email": "a@test.com", "name": "User A" },
    { "email": "b@test.com", "name": "User B" }
  ]
}

// Response: 207 Multi-Status
{
  "results": [
    { "status": 201, "data": { "id": "1", ... } },
    { "status": 409, "error": { "message": "Email exists" } }
  ]
}
```

### Batch Update

```
PATCH /users/batch
Content-Type: application/json

{
  "updates": [
    { "id": "1", "status": "active" },
    { "id": "2", "status": "inactive" }
  ]
}
```

### Batch Delete

```
DELETE /users/batch
Content-Type: application/json

{
  "ids": ["1", "2", "3"]
}
```

---

## Long-Running Operations

### Async Pattern

```
# Start operation
POST /reports/generate
Content-Type: application/json

{ "type": "annual", "year": 2024 }

# Response: 202 Accepted
{
  "operationId": "op-123",
  "status": "pending",
  "statusUrl": "/operations/op-123"
}

# Poll for status
GET /operations/op-123

# Response (in progress)
{
  "operationId": "op-123",
  "status": "running",
  "progress": 45
}

# Response (complete)
{
  "operationId": "op-123",
  "status": "completed",
  "result": {
    "downloadUrl": "/reports/op-123/download"
  }
}
```

---

## HATEOAS (Hypermedia)

```json
{
  "data": {
    "id": "order-123",
    "status": "pending",
    "total": 99.99
  },
  "_links": {
    "self": { "href": "/orders/order-123" },
    "cancel": { "href": "/orders/order-123/cancel", "method": "POST" },
    "pay": { "href": "/orders/order-123/pay", "method": "POST" },
    "user": { "href": "/users/user-456" }
  }
}
```

---

## Caching

### Cache Headers

```
# Response headers
Cache-Control: private, max-age=3600
ETag: "abc123"
Last-Modified: Wed, 01 Jan 2025 00:00:00 GMT

# Conditional request
If-None-Match: "abc123"
If-Modified-Since: Wed, 01 Jan 2025 00:00:00 GMT

# Response if unchanged
304 Not Modified
```

### Cache Strategies

| Resource Type | Strategy |
|---------------|----------|
| Static config | `max-age=86400` (24h) |
| User data | `private, max-age=300` (5m) |
| List queries | `max-age=60` (1m) |
| Mutations | `no-store` |

---

## Webhooks

### Registration

```
POST /webhooks
Content-Type: application/json

{
  "url": "https://myapp.com/webhook",
  "events": ["order.created", "order.updated"],
  "secret": "whsec_..."
}
```

### Payload

```json
{
  "id": "evt_123",
  "type": "order.created",
  "created": "2025-01-15T10:30:00Z",
  "data": {
    "object": {
      "id": "order-456",
      "total": 99.99
    }
  }
}
```

### Signature Verification

```typescript
function verifyWebhook(payload: string, signature: string, secret: string): boolean {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(`sha256=${expected}`)
  );
}
```

---

## OpenAPI Best Practices

### Operation IDs

```yaml
paths:
  /users:
    get:
      operationId: listUsers  # camelCase, verb + noun
    post:
      operationId: createUser
  /users/{id}:
    get:
      operationId: getUser
    put:
      operationId: updateUser
    delete:
      operationId: deleteUser
```

### Reusable Components

```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email

  parameters:
    limitParam:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  responses:
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

### Tags for Organization

```yaml
tags:
  - name: Users
    description: User management
  - name: Orders
    description: Order operations

paths:
  /users:
    get:
      tags: [Users]
```
