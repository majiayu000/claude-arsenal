---
name: mcp-server-development
description: MCP (Model Context Protocol) Server development guide. Use when building Claude Code extensions. Covers Tools, Resources, Prompts capabilities.
---
# MCP Server Development

## Core Principles

- **Single Responsibility** — Each server focuses on one domain
- **Minimal Permissions** — Request only necessary access
- **Input Validation** — Strictly validate all user input
- **Error Handling** — Return meaningful error messages
- **Idempotent Design** — Tools should be idempotent when possible
- **Clear Documentation** — Every Tool/Resource has a clear description

---

## MCP Architecture

```
┌─────────────────────────────────────────────────┐
│                   MCP Host                       │
│            (Claude Desktop / IDE)                │
└─────────────────────────────────────────────────┘
                        │
                   JSON-RPC 2.0
                   (stdio / HTTP)
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │ Server A│    │ Server B│    │ Server C│
   │ (Files) │    │ (GitHub)│    │  (DB)   │
   └─────────┘    └─────────┘    └─────────┘
```

### Three Capabilities

| Type | Description | Example |
|------|-------------|---------|
| **Tools** | Functions LLM can call | Execute commands, API calls |
| **Resources** | Data sources to read | File contents, DB records |
| **Prompts** | Pre-defined templates | Code review, doc generation |

---

## Quick Start

### 1. Initialize Project

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
```

### 2. Project Structure

```
my-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts          # Entry point
│   ├── tools/            # Tool definitions
│   │   └── search.ts
│   ├── resources/        # Resource definitions
│   │   └── files.ts
│   └── prompts/          # Prompt templates
│       └── review.ts
└── tests/
    └── server.test.ts
```

### 3. Basic Server

```typescript
#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';

const server = new Server(
  { name: 'my-mcp-server', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'hello',
      description: 'Say hello to someone',
      inputSchema: {
        type: 'object',
        properties: {
          name: { type: 'string', description: 'Name to greet' },
        },
        required: ['name'],
      },
    },
  ],
}));

// Handle tool calls
const HelloInput = z.object({ name: z.string().min(1) });

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === 'hello') {
    const { name } = HelloInput.parse(request.params.arguments);
    return {
      content: [{ type: 'text', text: `Hello, ${name}!` }],
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server
const transport = new StdioServerTransport();
server.connect(transport);
```

---

## Tools

### Definition

```typescript
{
  name: 'search_files',
  description: 'Search for files matching a glob pattern',
  inputSchema: {
    type: 'object',
    properties: {
      pattern: {
        type: 'string',
        description: 'Glob pattern (e.g., "**/*.ts")',
      },
      directory: {
        type: 'string',
        description: 'Directory to search in',
        default: '.',
      },
    },
    required: ['pattern'],
  },
}
```

### Input Validation

```typescript
import { z } from 'zod';

const SearchFilesInput = z.object({
  pattern: z.string().min(1).max(500),
  directory: z.string().default('.')
    .refine(d => !d.includes('..'), 'Path traversal not allowed'),
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'search_files': {
      const input = SearchFilesInput.parse(args);
      const results = await glob(input.pattern, { cwd: input.directory });
      return {
        content: [{ type: 'text', text: JSON.stringify(results, null, 2) }],
      };
    }
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});
```

### Response Types

```typescript
// Text response
return {
  content: [{ type: 'text', text: 'Result here' }],
};

// Multiple content blocks
return {
  content: [
    { type: 'text', text: 'File contents:' },
    { type: 'text', text: fileContent },
  ],
};

// Image (base64)
return {
  content: [{
    type: 'image',
    data: base64EncodedImage,
    mimeType: 'image/png',
  }],
};

// Error (use isError flag)
return {
  content: [{ type: 'text', text: 'Error: File not found' }],
  isError: true,
};
```

---

## Resources

### Definition

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: 'file:///config.json',
      name: 'Configuration',
      description: 'Application configuration file',
      mimeType: 'application/json',
    },
    {
      uri: 'db://users',
      name: 'Users Table',
      description: 'Database users table',
      mimeType: 'application/json',
    },
  ],
}));
```

### Reading Resources

```typescript
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === 'file:///config.json') {
    const content = await fs.readFile('config.json', 'utf-8');
    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: content,
      }],
    };
  }

  if (uri.startsWith('db://')) {
    const table = uri.replace('db://', '');
    const data = await db.query(`SELECT * FROM ${table} LIMIT 100`);
    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify(data, null, 2),
      }],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```

### Resource Templates

```typescript
server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => ({
  resourceTemplates: [
    {
      uriTemplate: 'file:///{path}',
      name: 'File',
      description: 'Read any file by path',
      mimeType: 'text/plain',
    },
  ],
}));
```

---

## Prompts

### Definition

```typescript
server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: 'code_review',
      description: 'Generate a code review for the given file',
      arguments: [
        {
          name: 'file_path',
          description: 'Path to the file to review',
          required: true,
        },
        {
          name: 'focus',
          description: 'Areas to focus on (security, performance, etc.)',
          required: false,
        },
      ],
    },
  ],
}));
```

### Getting Prompts

```typescript
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'code_review') {
    const filePath = args?.file_path as string;
    const focus = args?.focus as string || 'general';
    const code = await fs.readFile(filePath, 'utf-8');

    return {
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: `Please review the following code with a focus on ${focus}:

\`\`\`
${code}
\`\`\`

Provide feedback on:
1. Code quality
2. Potential bugs
3. Suggestions for improvement`,
          },
        },
      ],
    };
  }

  throw new Error(`Unknown prompt: ${name}`);
});
```

---

## Security

### Path Traversal Prevention

```typescript
import path from 'path';

const ALLOWED_DIRS = ['/workspace', '/tmp'];

function validatePath(userPath: string): string {
  // Resolve to absolute path
  const resolved = path.resolve(userPath);

  // Check against whitelist
  const allowed = ALLOWED_DIRS.some(dir => resolved.startsWith(dir));
  if (!allowed) {
    throw new Error('Access denied: path outside allowed directories');
  }

  // Check for traversal attempts
  if (userPath.includes('..')) {
    throw new Error('Path traversal not allowed');
  }

  return resolved;
}
```

### Input Sanitization

```typescript
const SafeInput = z.object({
  query: z.string()
    .max(1000)
    .refine(s => !s.includes('DROP'), 'Invalid query'),

  filename: z.string()
    .regex(/^[\w\-\.]+$/, 'Invalid filename'),

  command: z.string()
    .refine(s => !['rm', 'sudo', 'chmod'].some(c => s.includes(c)),
      'Dangerous command not allowed'),
});
```

### Secrets Handling

```typescript
// Never expose secrets in responses
function sanitizeOutput(data: Record<string, unknown>): Record<string, unknown> {
  const sensitiveKeys = ['password', 'apiKey', 'secret', 'token', 'credentials'];

  return Object.fromEntries(
    Object.entries(data).filter(([key]) =>
      !sensitiveKeys.some(s => key.toLowerCase().includes(s))
    )
  );
}
```

---

## Testing

### MCP Inspector

```bash
# Install and run
npx @modelcontextprotocol/inspector node dist/index.js
```

### Unit Tests

```typescript
import { describe, it, expect, beforeAll } from 'vitest';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';

describe('MCP Server', () => {
  let client: Client;

  beforeAll(async () => {
    // Setup test client connected to server
    client = await createTestClient();
  });

  it('lists tools', async () => {
    const { tools } = await client.listTools();
    expect(tools).toContainEqual(
      expect.objectContaining({ name: 'search_files' })
    );
  });

  it('executes search_files tool', async () => {
    const result = await client.callTool('search_files', {
      pattern: '*.ts',
      directory: 'src',
    });
    expect(result.content[0].text).toContain('index.ts');
  });

  it('rejects path traversal', async () => {
    await expect(
      client.callTool('search_files', {
        pattern: '*.ts',
        directory: '../../../etc',
      })
    ).rejects.toThrow('Path traversal not allowed');
  });
});
```

---

## Deployment

### Claude Desktop Config

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

### NPM Publishing

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "my-mcp-server": "dist/index.js"
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsc",
    "prepublishOnly": "npm run build"
  }
}
```

```bash
npm publish
```

---

## Checklist

```markdown
## Implementation
- [ ] Tools have clear descriptions
- [ ] Input validated with Zod
- [ ] Path traversal protection
- [ ] Meaningful error messages
- [ ] No sensitive data in responses

## Testing
- [ ] MCP Inspector tested
- [ ] Unit tests for tools
- [ ] Security tests (path traversal, etc.)

## Documentation
- [ ] README with usage examples
- [ ] Tool parameters documented
- [ ] Installation instructions

## Deployment
- [ ] package.json bin configured
- [ ] TypeScript compiled
- [ ] NPM published (optional)
```

---

## See Also

- [reference/protocol.md](reference/protocol.md) — MCP protocol details
- [reference/security.md](reference/security.md) — Security best practices
- [reference/testing.md](reference/testing.md) — Testing strategies
