#!/usr/bin/env node
/**
 * MCP Server Template
 * A starting point for building MCP servers
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';
import fs from 'fs/promises';
import path from 'path';

// ============================================
// Configuration
// ============================================

const SERVER_NAME = 'my-mcp-server';
const SERVER_VERSION = '1.0.0';

// Security: Allowed directories for file operations
const ALLOWED_DIRS = [
  process.env.WORKSPACE_DIR || process.cwd(),
];

// ============================================
// Input Schemas
// ============================================

const SearchFilesInput = z.object({
  pattern: z.string().min(1).max(500),
  directory: z.string().default('.')
    .refine(d => !d.includes('..'), 'Path traversal not allowed'),
});

const ReadFileInput = z.object({
  path: z.string().min(1).max(500)
    .refine(p => !p.includes('..'), 'Path traversal not allowed'),
});

// ============================================
// Helpers
// ============================================

function validatePath(userPath: string): string {
  const resolved = path.resolve(userPath);
  const isAllowed = ALLOWED_DIRS.some(dir =>
    resolved.startsWith(path.resolve(dir))
  );

  if (!isAllowed) {
    throw new Error(`Access denied: path outside allowed directories`);
  }

  return resolved;
}

// ============================================
// Server Setup
// ============================================

const server = new Server(
  {
    name: SERVER_NAME,
    version: SERVER_VERSION,
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

// ============================================
// Tools
// ============================================

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
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
            description: 'Directory to search in (default: current)',
          },
        },
        required: ['pattern'],
      },
    },
    {
      name: 'read_file',
      description: 'Read contents of a file',
      inputSchema: {
        type: 'object',
        properties: {
          path: {
            type: 'string',
            description: 'Path to the file',
          },
        },
        required: ['path'],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'search_files': {
        const input = SearchFilesInput.parse(args);
        const dir = validatePath(input.directory);

        // Simple file search (in production, use glob library)
        const files = await fs.readdir(dir, { recursive: true });
        const matches = files.filter(f =>
          typeof f === 'string' && f.includes(input.pattern.replace('*', ''))
        );

        return {
          content: [{
            type: 'text',
            text: JSON.stringify(matches.slice(0, 100), null, 2),
          }],
        };
      }

      case 'read_file': {
        const input = ReadFileInput.parse(args);
        const filePath = validatePath(input.path);
        const content = await fs.readFile(filePath, 'utf-8');

        return {
          content: [{ type: 'text', text: content }],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    return {
      content: [{ type: 'text', text: `Error: ${message}` }],
      isError: true,
    };
  }
});

// ============================================
// Resources
// ============================================

server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: 'config://settings',
      name: 'Server Settings',
      description: 'Current server configuration',
      mimeType: 'application/json',
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === 'config://settings') {
    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify({
          serverName: SERVER_NAME,
          version: SERVER_VERSION,
          allowedDirs: ALLOWED_DIRS,
        }, null, 2),
      }],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});

// ============================================
// Prompts
// ============================================

server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: 'code_review',
      description: 'Generate a code review prompt for a file',
      arguments: [
        {
          name: 'file_path',
          description: 'Path to the file to review',
          required: true,
        },
      ],
    },
  ],
}));

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'code_review') {
    const filePath = args?.file_path as string;
    if (!filePath) {
      throw new Error('file_path is required');
    }

    const validPath = validatePath(filePath);
    const code = await fs.readFile(validPath, 'utf-8');

    return {
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: `Please review the following code from ${filePath}:

\`\`\`
${code}
\`\`\`

Provide feedback on:
1. Code quality and readability
2. Potential bugs or issues
3. Performance considerations
4. Suggestions for improvement`,
          },
        },
      ],
    };
  }

  throw new Error(`Unknown prompt: ${name}`);
});

// ============================================
// Start Server
// ============================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`${SERVER_NAME} v${SERVER_VERSION} running on stdio`);
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
