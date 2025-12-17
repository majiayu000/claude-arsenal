# MCP Protocol Details

## Overview

MCP uses JSON-RPC 2.0 over stdio or HTTP/SSE transport.

```
Client (Host)                    Server
     │                              │
     │──── initialize ─────────────▶│
     │◀─── result ─────────────────│
     │                              │
     │──── tools/list ─────────────▶│
     │◀─── tools ──────────────────│
     │                              │
     │──── tools/call ─────────────▶│
     │◀─── result ─────────────────│
```

---

## Message Types

### Request

```typescript
interface Request {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params?: unknown;
}
```

### Response

```typescript
interface Response {
  jsonrpc: '2.0';
  id: string | number;
  result?: unknown;
  error?: {
    code: number;
    message: string;
    data?: unknown;
  };
}
```

### Notification

```typescript
interface Notification {
  jsonrpc: '2.0';
  method: string;
  params?: unknown;
  // No id field
}
```

---

## Lifecycle Methods

### initialize

```typescript
// Request
{
  method: 'initialize',
  params: {
    protocolVersion: '2024-11-05',
    capabilities: {
      roots: { listChanged: true },
      sampling: {}
    },
    clientInfo: {
      name: 'claude-desktop',
      version: '1.0.0'
    }
  }
}

// Response
{
  result: {
    protocolVersion: '2024-11-05',
    capabilities: {
      tools: {},
      resources: {},
      prompts: {}
    },
    serverInfo: {
      name: 'my-server',
      version: '1.0.0'
    }
  }
}
```

### initialized (notification)

```typescript
// Client notifies server that initialization is complete
{
  method: 'notifications/initialized'
}
```

---

## Tool Methods

### tools/list

```typescript
// Request
{ method: 'tools/list' }

// Response
{
  result: {
    tools: [
      {
        name: 'search',
        description: 'Search for text',
        inputSchema: {
          type: 'object',
          properties: {
            query: { type: 'string' }
          },
          required: ['query']
        }
      }
    ]
  }
}
```

### tools/call

```typescript
// Request
{
  method: 'tools/call',
  params: {
    name: 'search',
    arguments: { query: 'hello' }
  }
}

// Response
{
  result: {
    content: [
      { type: 'text', text: 'Found 5 results' }
    ],
    isError: false
  }
}
```

---

## Resource Methods

### resources/list

```typescript
// Request
{ method: 'resources/list' }

// Response
{
  result: {
    resources: [
      {
        uri: 'file:///config.json',
        name: 'Config',
        description: 'Configuration file',
        mimeType: 'application/json'
      }
    ]
  }
}
```

### resources/read

```typescript
// Request
{
  method: 'resources/read',
  params: { uri: 'file:///config.json' }
}

// Response
{
  result: {
    contents: [
      {
        uri: 'file:///config.json',
        mimeType: 'application/json',
        text: '{"key": "value"}'
      }
    ]
  }
}
```

### resources/templates/list

```typescript
// Request
{ method: 'resources/templates/list' }

// Response
{
  result: {
    resourceTemplates: [
      {
        uriTemplate: 'file:///{path}',
        name: 'File',
        mimeType: 'text/plain'
      }
    ]
  }
}
```

---

## Prompt Methods

### prompts/list

```typescript
// Request
{ method: 'prompts/list' }

// Response
{
  result: {
    prompts: [
      {
        name: 'review',
        description: 'Code review prompt',
        arguments: [
          {
            name: 'file',
            description: 'File to review',
            required: true
          }
        ]
      }
    ]
  }
}
```

### prompts/get

```typescript
// Request
{
  method: 'prompts/get',
  params: {
    name: 'review',
    arguments: { file: 'main.ts' }
  }
}

// Response
{
  result: {
    description: 'Code review for main.ts',
    messages: [
      {
        role: 'user',
        content: {
          type: 'text',
          text: 'Please review this code...'
        }
      }
    ]
  }
}
```

---

## Content Types

### Text

```typescript
{
  type: 'text',
  text: 'Hello world'
}
```

### Image

```typescript
{
  type: 'image',
  data: 'base64-encoded-image-data',
  mimeType: 'image/png'
}
```

### Resource Reference

```typescript
{
  type: 'resource',
  resource: {
    uri: 'file:///path/to/file',
    mimeType: 'text/plain',
    text: 'file contents'
  }
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| -32700 | Parse error |
| -32600 | Invalid request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |

```typescript
// Error response
{
  jsonrpc: '2.0',
  id: 1,
  error: {
    code: -32602,
    message: 'Invalid parameters',
    data: {
      field: 'query',
      reason: 'Required field missing'
    }
  }
}
```

---

## Transports

### stdio

Default transport. Server reads from stdin, writes to stdout.

```typescript
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const transport = new StdioServerTransport();
await server.connect(transport);
```

### HTTP + SSE

For remote servers.

```typescript
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import express from 'express';

const app = express();
const transport = new SSEServerTransport('/sse', app);
await server.connect(transport);
app.listen(3000);
```

---

## Notifications

### Server → Client

```typescript
// Progress update
{
  method: 'notifications/progress',
  params: {
    progressToken: 'abc123',
    progress: 50,
    total: 100
  }
}

// Resource changed
{
  method: 'notifications/resources/list_changed'
}

// Tool changed
{
  method: 'notifications/tools/list_changed'
}
```

### Client → Server

```typescript
// Roots changed (working directories)
{
  method: 'notifications/roots/list_changed'
}
```
