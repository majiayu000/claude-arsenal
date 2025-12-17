/**
 * Example service template
 *
 * Services contain business logic and orchestrate operations.
 * They depend on repository/adapter interfaces, not implementations.
 */

import { z } from 'zod';
import { AppError, createLogger, type Result } from '../lib/index.js';

const log = createLogger('example-service');

// Input validation schemas
export const CreateExampleSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
});

export type CreateExampleInput = z.infer<typeof CreateExampleSchema>;

// Domain entity
export interface Example {
  id: string;
  name: string;
  description?: string;
  createdAt: Date;
}

// Repository interface (implemented by adapters)
export interface ExampleRepository {
  findById(id: string): Promise<Example | null>;
  findAll(): Promise<Example[]>;
  save(example: Example): Promise<Example>;
  delete(id: string): Promise<void>;
}

// Service implementation
export class ExampleService {
  constructor(private readonly repo: ExampleRepository) {}

  async create(input: CreateExampleInput): Promise<Result<Example, AppError>> {
    try {
      const validated = CreateExampleSchema.parse(input);

      const example: Example = {
        id: crypto.randomUUID(),
        name: validated.name,
        description: validated.description,
        createdAt: new Date(),
      };

      const saved = await this.repo.save(example);
      log.info('Example created', { id: saved.id });

      return { ok: true, value: saved };
    } catch (error) {
      if (error instanceof z.ZodError) {
        return {
          ok: false,
          error: AppError.validation('Invalid input', { issues: error.issues }),
        };
      }
      throw error;
    }
  }

  async findById(id: string): Promise<Result<Example, AppError>> {
    const example = await this.repo.findById(id);
    if (!example) {
      return { ok: false, error: AppError.notFound('Example', id) };
    }
    return { ok: true, value: example };
  }

  async findAll(): Promise<Example[]> {
    return this.repo.findAll();
  }

  async delete(id: string): Promise<Result<void, AppError>> {
    const existing = await this.repo.findById(id);
    if (!existing) {
      return { ok: false, error: AppError.notFound('Example', id) };
    }

    await this.repo.delete(id);
    log.info('Example deleted', { id });

    return { ok: true, value: undefined };
  }
}
