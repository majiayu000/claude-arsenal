# MCP Security Best Practices

## Input Validation

### Schema Validation with Zod

```typescript
import { z } from 'zod';

// File path validation
const FilePathSchema = z.string()
  .min(1)
  .max(500)
  .refine(p => !p.includes('..'), 'Path traversal not allowed')
  .refine(p => !p.startsWith('/'), 'Absolute paths not allowed')
  .refine(p => !/[<>:"|?*]/.test(p), 'Invalid path characters');

// Command validation
const CommandSchema = z.string()
  .max(1000)
  .refine(cmd => {
    const dangerous = ['rm -rf', 'sudo', 'chmod 777', 'curl | sh', 'wget | bash'];
    return !dangerous.some(d => cmd.includes(d));
  }, 'Dangerous command pattern');

// URL validation
const UrlSchema = z.string()
  .url()
  .refine(url => {
    const parsed = new URL(url);
    return ['http:', 'https:'].includes(parsed.protocol);
  }, 'Only HTTP(S) allowed')
  .refine(url => {
    const parsed = new URL(url);
    // Prevent SSRF to internal networks
    return !['localhost', '127.0.0.1', '0.0.0.0'].includes(parsed.hostname);
  }, 'Internal URLs not allowed');
```

### Type Coercion Prevention

```typescript
// Always parse, don't trust raw input
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const args = request.params.arguments;

  // ❌ Bad: Trust raw input
  const limit = args.limit;

  // ✅ Good: Parse with schema
  const parsed = InputSchema.parse(args);
  const limit = parsed.limit; // Properly typed
});
```

---

## Path Security

### Directory Whitelisting

```typescript
import path from 'path';
import fs from 'fs/promises';

const ALLOWED_DIRECTORIES = [
  process.env.WORKSPACE_DIR || '/workspace',
  '/tmp/mcp-server',
];

async function validateAndResolvePath(userPath: string): Promise<string> {
  // Resolve to absolute path
  const resolved = path.resolve(userPath);

  // Check against whitelist
  const isAllowed = ALLOWED_DIRECTORIES.some(dir =>
    resolved.startsWith(path.resolve(dir))
  );

  if (!isAllowed) {
    throw new SecurityError(`Access denied: ${userPath}`);
  }

  // Verify path exists and is accessible
  try {
    await fs.access(resolved, fs.constants.R_OK);
  } catch {
    throw new SecurityError(`Path not accessible: ${userPath}`);
  }

  return resolved;
}
```

### Symlink Resolution

```typescript
async function safeReadFile(filePath: string): Promise<string> {
  const validated = await validateAndResolvePath(filePath);

  // Resolve symlinks to prevent escape
  const realPath = await fs.realpath(validated);

  // Re-validate after symlink resolution
  const isStillAllowed = ALLOWED_DIRECTORIES.some(dir =>
    realPath.startsWith(path.resolve(dir))
  );

  if (!isStillAllowed) {
    throw new SecurityError('Symlink points outside allowed directories');
  }

  return fs.readFile(realPath, 'utf-8');
}
```

---

## Command Execution

### Shell Injection Prevention

```typescript
import { spawn } from 'child_process';

// ❌ BAD: Shell injection vulnerable
function badExecute(userInput: string) {
  exec(`ls ${userInput}`); // userInput could be "; rm -rf /"
}

// ✅ GOOD: No shell, arguments array
async function safeExecute(
  command: string,
  args: string[],
  cwd: string
): Promise<string> {
  return new Promise((resolve, reject) => {
    const process = spawn(command, args, {
      cwd,
      shell: false,  // Important: no shell
      timeout: 30000,
      maxBuffer: 1024 * 1024,
    });

    let stdout = '';
    let stderr = '';

    process.stdout.on('data', data => stdout += data);
    process.stderr.on('data', data => stderr += data);

    process.on('close', code => {
      if (code === 0) {
        resolve(stdout);
      } else {
        reject(new Error(`Command failed: ${stderr}`));
      }
    });
  });
}
```

### Command Whitelisting

```typescript
const ALLOWED_COMMANDS: Record<string, string[]> = {
  'git': ['status', 'log', 'diff', 'branch'],
  'npm': ['list', 'outdated', 'audit'],
  'ls': ['-la', '-lh'],
};

function validateCommand(command: string, args: string[]): void {
  if (!ALLOWED_COMMANDS[command]) {
    throw new SecurityError(`Command not allowed: ${command}`);
  }

  const allowedArgs = ALLOWED_COMMANDS[command];
  const invalidArgs = args.filter(arg =>
    !allowedArgs.some(allowed => arg.startsWith(allowed))
  );

  if (invalidArgs.length > 0) {
    throw new SecurityError(`Invalid arguments: ${invalidArgs.join(', ')}`);
  }
}
```

---

## Data Protection

### Sensitive Data Filtering

```typescript
const SENSITIVE_PATTERNS = [
  /password/i,
  /secret/i,
  /api[_-]?key/i,
  /token/i,
  /credential/i,
  /private[_-]?key/i,
];

const SENSITIVE_FILE_PATTERNS = [
  /\.env$/,
  /\.pem$/,
  /\.key$/,
  /credentials/i,
  /secrets/i,
];

function isSensitiveKey(key: string): boolean {
  return SENSITIVE_PATTERNS.some(p => p.test(key));
}

function isSensitiveFile(filename: string): boolean {
  return SENSITIVE_FILE_PATTERNS.some(p => p.test(filename));
}

function sanitizeObject(obj: Record<string, unknown>): Record<string, unknown> {
  return Object.fromEntries(
    Object.entries(obj).map(([key, value]) => {
      if (isSensitiveKey(key)) {
        return [key, '[REDACTED]'];
      }
      if (typeof value === 'object' && value !== null) {
        return [key, sanitizeObject(value as Record<string, unknown>)];
      }
      return [key, value];
    })
  );
}
```

### Output Sanitization

```typescript
function sanitizeOutput(output: string): string {
  // Redact common secret patterns
  return output
    .replace(/(?<=password[=:]\s*)[^\s]+/gi, '[REDACTED]')
    .replace(/(?<=api[_-]?key[=:]\s*)[^\s]+/gi, '[REDACTED]')
    .replace(/(?<=token[=:]\s*)[^\s]+/gi, '[REDACTED]')
    .replace(/Bearer\s+[A-Za-z0-9\-._~+/]+=*/g, 'Bearer [REDACTED]')
    .replace(/sk-[a-zA-Z0-9]+/g, 'sk-[REDACTED]');
}
```

---

## Rate Limiting

```typescript
class RateLimiter {
  private requests = new Map<string, number[]>();

  constructor(
    private limit: number,
    private windowMs: number
  ) {}

  check(key: string): boolean {
    const now = Date.now();
    const windowStart = now - this.windowMs;

    // Get existing requests
    let timestamps = this.requests.get(key) || [];

    // Filter to current window
    timestamps = timestamps.filter(t => t > windowStart);

    if (timestamps.length >= this.limit) {
      return false;
    }

    // Add current request
    timestamps.push(now);
    this.requests.set(key, timestamps);

    return true;
  }
}

// Usage in server
const rateLimiter = new RateLimiter(100, 60000); // 100 req/min

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const clientId = request.params._meta?.clientId || 'anonymous';

  if (!rateLimiter.check(clientId)) {
    throw new Error('Rate limit exceeded');
  }

  // ... handle request
});
```

---

## Logging & Auditing

```typescript
interface AuditLog {
  timestamp: string;
  tool: string;
  input: Record<string, unknown>;
  output: string;
  success: boolean;
  duration: number;
}

const auditLogs: AuditLog[] = [];

async function auditedToolCall(
  toolName: string,
  input: Record<string, unknown>,
  handler: () => Promise<unknown>
): Promise<unknown> {
  const start = Date.now();
  let success = true;
  let result: unknown;

  try {
    result = await handler();
    return result;
  } catch (error) {
    success = false;
    throw error;
  } finally {
    auditLogs.push({
      timestamp: new Date().toISOString(),
      tool: toolName,
      input: sanitizeObject(input),
      output: success ? 'OK' : 'ERROR',
      success,
      duration: Date.now() - start,
    });
  }
}
```

---

## Error Handling

```typescript
class SecurityError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'SecurityError';
  }
}

function handleError(error: unknown): { content: Content[]; isError: true } {
  // Log full error internally
  console.error('Error:', error);

  // Return safe message to client
  let message = 'An error occurred';

  if (error instanceof SecurityError) {
    message = error.message; // Safe to expose
  } else if (error instanceof z.ZodError) {
    message = 'Invalid input parameters';
  } else if (error instanceof Error) {
    // Don't expose internal errors
    message = 'Internal server error';
  }

  return {
    content: [{ type: 'text', text: message }],
    isError: true,
  };
}
```
