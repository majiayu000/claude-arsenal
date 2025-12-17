# GraphQL Deep Dive

## Schema Design

### Naming Conventions

```graphql
# Types: PascalCase
type User { ... }
type OrderItem { ... }

# Fields: camelCase
type User {
  firstName: String!
  lastName: String!
  createdAt: DateTime!
}

# Enums: SCREAMING_SNAKE_CASE values
enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
}

# Input types: suffix with Input
input CreateUserInput {
  email: String!
  name: String!
}

# Payload types: suffix with Payload
type CreateUserPayload {
  user: User!
}
```

### Nullability Strategy

```graphql
# Non-null by default for required fields
type User {
  id: ID!           # Always present
  email: String!    # Required
  phone: String     # Optional (nullable)
}

# Lists
type User {
  orders: [Order!]!     # Non-null list of non-null items
  tags: [String!]       # Nullable list of non-null strings
  metadata: [String]    # Nullable list of nullable strings (avoid)
}
```

---

## Pagination Patterns

### Relay Cursor Connections

```graphql
type Query {
  users(
    first: Int
    after: String
    last: Int
    before: String
    filter: UserFilter
  ): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### Usage

```graphql
# First page
query {
  users(first: 20) {
    edges {
      node { id name }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}

# Next page
query {
  users(first: 20, after: "cursor_from_previous_page") {
    ...
  }
}
```

---

## Error Handling

### Union-Based Errors

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserResult!
}

union CreateUserResult =
  | CreateUserSuccess
  | ValidationError
  | UnauthorizedError

type CreateUserSuccess {
  user: User!
}

type ValidationError implements Error {
  message: String!
  code: String!
  field: String
}

type UnauthorizedError implements Error {
  message: String!
  code: String!
}

interface Error {
  message: String!
  code: String!
}
```

### Client Handling

```typescript
const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      ... on CreateUserSuccess {
        user { id name }
      }
      ... on ValidationError {
        message
        field
      }
      ... on UnauthorizedError {
        message
      }
    }
  }
`;

// Type-safe handling
const result = await client.mutate({ mutation: CREATE_USER, variables });
if (result.data.createUser.__typename === 'CreateUserSuccess') {
  const user = result.data.createUser.user;
} else {
  const error = result.data.createUser;
  console.error(error.message);
}
```

---

## Federation

### Subgraph Definition

```graphql
# Users subgraph
type User @key(fields: "id") {
  id: ID!
  email: String!
  name: String!
}

type Query {
  user(id: ID!): User
  users: [User!]!
}
```

```graphql
# Orders subgraph
type Order @key(fields: "id") {
  id: ID!
  total: Float!
  user: User!
}

# Extend User from another subgraph
extend type User @key(fields: "id") {
  id: ID! @external
  orders: [Order!]!
}

type Query {
  order(id: ID!): Order
}
```

### Federation Directives

| Directive | Purpose |
|-----------|---------|
| `@key` | Define entity's primary key |
| `@external` | Field defined in another subgraph |
| `@requires` | Fields needed to resolve this field |
| `@provides` | Fields this resolver can provide |
| `@extends` | Extend type from another subgraph |

---

## Performance

### Query Complexity Limiting

```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const complexityRule = createComplexityLimitRule(1000, {
  scalarCost: 1,
  objectCost: 2,
  listFactor: 10,
});

const server = new ApolloServer({
  validationRules: [complexityRule],
});
```

### Depth Limiting

```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  validationRules: [depthLimit(10)],
});
```

### DataLoader for N+1

```typescript
import DataLoader from 'dataloader';

// Create loader per request
function createLoaders() {
  return {
    user: new DataLoader(async (ids: string[]) => {
      const users = await db.user.findMany({
        where: { id: { in: ids } },
      });
      // Maintain order
      return ids.map(id => users.find(u => u.id === id) || null);
    }),
  };
}

// Use in resolver
const resolvers = {
  Order: {
    user: (order, _, { loaders }) => loaders.user.load(order.userId),
  },
};
```

### Persisted Queries

```typescript
// Client sends hash instead of full query
const link = createPersistedQueryLink({ sha256 });

// Server caches query by hash
const server = new ApolloServer({
  persistedQueries: {
    cache: new RedisCache(),
  },
});
```

---

## Subscriptions

### Definition

```graphql
type Subscription {
  orderUpdated(orderId: ID!): Order!
  newOrders: Order!
}
```

### Implementation

```typescript
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();

const resolvers = {
  Mutation: {
    updateOrder: async (_, { id, input }) => {
      const order = await db.order.update({ where: { id }, data: input });
      pubsub.publish(`ORDER_UPDATED_${id}`, { orderUpdated: order });
      return order;
    },
  },
  Subscription: {
    orderUpdated: {
      subscribe: (_, { orderId }) =>
        pubsub.asyncIterator(`ORDER_UPDATED_${orderId}`),
    },
  },
};
```

---

## Security

### Query Allowlist (Production)

```typescript
// Only allow pre-approved queries
const allowedQueries = new Map([
  ['abc123', 'query GetUser($id: ID!) { user(id: $id) { id name } }'],
]);

const server = new ApolloServer({
  plugins: [{
    requestDidStart() {
      return {
        didResolveOperation({ request }) {
          if (!allowedQueries.has(request.extensions?.persistedQuery?.sha256Hash)) {
            throw new Error('Query not allowed');
          }
        },
      };
    },
  }],
});
```

### Field-Level Authorization

```typescript
const resolvers = {
  User: {
    email: (user, _, { currentUser }) => {
      if (currentUser.id !== user.id && !currentUser.isAdmin) {
        throw new ForbiddenError('Cannot view email');
      }
      return user.email;
    },
  },
};
```
