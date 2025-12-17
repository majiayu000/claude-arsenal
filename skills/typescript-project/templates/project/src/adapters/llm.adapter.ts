/**
 * LLM Adapter - Unified interface for all LLM providers via LiteLLM proxy
 *
 * Uses OpenAI SDK to connect to LiteLLM proxy, which supports:
 * - OpenAI (gpt-4o, gpt-4-turbo, etc.)
 * - Anthropic (claude-3-opus, claude-3-sonnet, etc.)
 * - Google (gemini-pro, gemini-ultra, etc.)
 * - Azure OpenAI
 * - AWS Bedrock
 * - And 100+ more providers
 *
 * @see https://docs.litellm.ai/docs/providers
 */

import { OpenAI } from 'openai';
import { config } from '../lib/config.js';
import { createLogger } from '../lib/logger.js';

const log = createLogger('llm');

// Connect to LiteLLM proxy using OpenAI-compatible SDK
const client = new OpenAI({
  baseURL: config.llm.baseUrl,
  apiKey: config.llm.apiKey,
});

export interface CompletionOptions {
  model?: string;
  temperature?: number;
  maxTokens?: number;
  systemPrompt?: string;
}

export interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

/**
 * Generate a chat completion
 */
export async function complete(
  prompt: string,
  options: CompletionOptions = {}
): Promise<string> {
  const {
    model = config.llm.defaultModel,
    temperature = 0.7,
    maxTokens = 1000,
    systemPrompt,
  } = options;

  const messages: Message[] = [];
  if (systemPrompt) {
    messages.push({ role: 'system', content: systemPrompt });
  }
  messages.push({ role: 'user', content: prompt });

  return chat(messages, { model, temperature, maxTokens });
}

/**
 * Multi-turn chat completion
 */
export async function chat(
  messages: Message[],
  options: Omit<CompletionOptions, 'systemPrompt'> = {}
): Promise<string> {
  const {
    model = config.llm.defaultModel,
    temperature = 0.7,
    maxTokens = 1000,
  } = options;

  log.debug('LLM request', { model, messageCount: messages.length });

  const response = await client.chat.completions.create({
    model,
    messages,
    temperature,
    max_tokens: maxTokens,
  });

  const content = response.choices[0]?.message?.content ?? '';

  log.debug('LLM response', {
    model,
    tokens: response.usage?.total_tokens,
  });

  return content;
}

/**
 * Stream chat completion
 */
export async function* stream(
  messages: Message[],
  options: Omit<CompletionOptions, 'systemPrompt'> = {}
): AsyncGenerator<string> {
  const {
    model = config.llm.defaultModel,
    temperature = 0.7,
    maxTokens = 1000,
  } = options;

  const response = await client.chat.completions.create({
    model,
    messages,
    temperature,
    max_tokens: maxTokens,
    stream: true,
  });

  for await (const chunk of response) {
    const content = chunk.choices[0]?.delta?.content;
    if (content) {
      yield content;
    }
  }
}
