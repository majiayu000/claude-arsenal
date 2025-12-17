# gRPC Deep Dive

## Proto Design

### Package Structure

```
proto/
├── api/
│   └── v1/
│       ├── user.proto
│       ├── order.proto
│       └── common.proto
└── buf.yaml
```

### Style Guide

```protobuf
syntax = "proto3";

package api.v1;

option go_package = "github.com/myorg/myapp/gen/go/api/v1";
option java_package = "com.myorg.myapp.api.v1";

import "google/protobuf/timestamp.proto";
import "google/protobuf/field_mask.proto";

// Service names: PascalCase + "Service"
service UserService {
  // Method names: PascalCase verbs
  rpc GetUser(GetUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc UpdateUser(UpdateUserRequest) returns (User);
  rpc DeleteUser(DeleteUserRequest) returns (google.protobuf.Empty);
}

// Message names: PascalCase
// Request/Response: Method name + Request/Response
message GetUserRequest {
  string id = 1;
}

// Field names: snake_case
message User {
  string id = 1;
  string email = 2;
  string display_name = 3;
  UserStatus status = 4;
  google.protobuf.Timestamp created_at = 5;
  google.protobuf.Timestamp updated_at = 6;
}

// Enum: PascalCase, values SCREAMING_SNAKE_CASE
// First value must be UNSPECIFIED = 0
enum UserStatus {
  USER_STATUS_UNSPECIFIED = 0;
  USER_STATUS_ACTIVE = 1;
  USER_STATUS_INACTIVE = 2;
  USER_STATUS_SUSPENDED = 3;
}
```

### Field Numbers

```protobuf
message User {
  // 1-15: Frequently used fields (1 byte encoding)
  string id = 1;
  string email = 2;
  string name = 3;

  // 16-2047: Less common fields (2 byte encoding)
  string bio = 16;
  repeated string tags = 17;

  // Reserved: Never reuse deleted field numbers
  reserved 4, 5, 10 to 12;
  reserved "old_field", "deprecated_field";
}
```

---

## Pagination

```protobuf
message ListUsersRequest {
  int32 page_size = 1;      // Max items per page
  string page_token = 2;    // Opaque cursor
  UserFilter filter = 3;
}

message ListUsersResponse {
  repeated User users = 1;
  string next_page_token = 2;  // Empty if no more pages
  int32 total_count = 3;       // Optional: total matching items
}

message UserFilter {
  optional string status = 1;
  optional string role = 2;
  optional string search = 3;
}
```

---

## Streaming Patterns

### Server Streaming

```protobuf
service ReportService {
  // Server sends multiple responses
  rpc GenerateReport(ReportRequest) returns (stream ReportChunk);
}

message ReportChunk {
  bytes data = 1;
  int32 sequence = 2;
  bool is_last = 3;
}
```

```typescript
// Client
const stream = client.generateReport({ type: 'annual' });
for await (const chunk of stream) {
  processChunk(chunk.data);
  if (chunk.isLast) break;
}
```

### Client Streaming

```protobuf
service UploadService {
  // Client sends multiple requests
  rpc UploadFile(stream FileChunk) returns (UploadResponse);
}
```

```typescript
// Client
const call = client.uploadFile((err, response) => {
  if (err) throw err;
  console.log('Uploaded:', response.fileId);
});

for (const chunk of fileChunks) {
  call.write({ data: chunk, sequence: i });
}
call.end();
```

### Bidirectional Streaming

```protobuf
service ChatService {
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}
```

```typescript
// Client
const call = client.chat();

call.on('data', (message) => {
  console.log('Received:', message.content);
});

call.write({ content: 'Hello' });
call.write({ content: 'How are you?' });
```

---

## Error Handling

### Standard Status Codes

| Code | Name | When to Use |
|------|------|-------------|
| 0 | OK | Success |
| 1 | CANCELLED | Client cancelled |
| 2 | UNKNOWN | Unknown error |
| 3 | INVALID_ARGUMENT | Bad request |
| 4 | DEADLINE_EXCEEDED | Timeout |
| 5 | NOT_FOUND | Resource not found |
| 6 | ALREADY_EXISTS | Duplicate |
| 7 | PERMISSION_DENIED | Forbidden |
| 8 | RESOURCE_EXHAUSTED | Rate limited |
| 9 | FAILED_PRECONDITION | Invalid state |
| 10 | ABORTED | Concurrency conflict |
| 11 | OUT_OF_RANGE | Invalid range |
| 12 | UNIMPLEMENTED | Not implemented |
| 13 | INTERNAL | Server error |
| 14 | UNAVAILABLE | Service down |
| 16 | UNAUTHENTICATED | Not authenticated |

### Rich Error Details

```protobuf
import "google/rpc/status.proto";
import "google/rpc/error_details.proto";

// Server-side (Go)
st := status.New(codes.InvalidArgument, "Invalid user data")
st, _ = st.WithDetails(
  &errdetails.BadRequest{
    FieldViolations: []*errdetails.BadRequest_FieldViolation{
      {Field: "email", Description: "Invalid email format"},
      {Field: "age", Description: "Must be positive"},
    },
  },
)
return nil, st.Err()
```

### Streaming Error Handling

```protobuf
// Embed errors in response for streams
message StreamResponse {
  oneof result {
    User user = 1;
    StreamError error = 2;
  }
}

message StreamError {
  string code = 1;
  string message = 2;
  map<string, string> metadata = 3;
}
```

---

## Interceptors

### Server Interceptors

```typescript
// Logging interceptor
function loggingInterceptor(call, callback) {
  const start = Date.now();
  const method = call.getPath();

  callback(null, (err, response) => {
    const duration = Date.now() - start;
    console.log(`${method} ${err ? 'ERROR' : 'OK'} ${duration}ms`);
  });
}

// Auth interceptor
function authInterceptor(call, callback) {
  const metadata = call.metadata;
  const token = metadata.get('authorization')[0];

  if (!token) {
    callback({
      code: grpc.status.UNAUTHENTICATED,
      message: 'Missing authorization',
    });
    return;
  }

  try {
    call.user = verifyToken(token);
    callback(null);
  } catch (err) {
    callback({
      code: grpc.status.UNAUTHENTICATED,
      message: 'Invalid token',
    });
  }
}
```

### Client Interceptors

```typescript
// Retry interceptor
const retryInterceptor = (options, nextCall) => {
  return new InterceptingCall(nextCall(options), {
    start: (metadata, listener, next) => {
      const retryListener = {
        onReceiveStatus: (status, next) => {
          if (shouldRetry(status.code)) {
            // Retry logic
          }
          next(status);
        },
      };
      next(metadata, retryListener);
    },
  });
};
```

---

## Deadlines & Timeouts

```typescript
// Always set deadlines
const deadline = new Date();
deadline.setSeconds(deadline.getSeconds() + 5);

const user = await client.getUser(
  { id: '123' },
  { deadline }
);

// Propagate deadlines in service-to-service calls
function handler(call, callback) {
  // Get remaining time from incoming call
  const deadline = call.getDeadline();

  // Pass to downstream service
  downstreamClient.getData(
    { id: call.request.id },
    { deadline },
    callback
  );
}
```

---

## Health Checking

```protobuf
// Standard health check protocol
package grpc.health.v1;

service Health {
  rpc Check(HealthCheckRequest) returns (HealthCheckResponse);
  rpc Watch(HealthCheckRequest) returns (stream HealthCheckResponse);
}

message HealthCheckRequest {
  string service = 1;
}

message HealthCheckResponse {
  enum ServingStatus {
    UNKNOWN = 0;
    SERVING = 1;
    NOT_SERVING = 2;
  }
  ServingStatus status = 1;
}
```

---

## Load Balancing

### Client-Side (Recommended)

```typescript
// Use round-robin or weighted load balancing
const client = new UserServiceClient(
  'dns:///users.service.local',
  grpc.credentials.createInsecure(),
  {
    'grpc.lb_policy_name': 'round_robin',
  }
);
```

### Service Mesh

- Istio, Linkerd handle load balancing transparently
- gRPC works well with service mesh proxies
