/**
 * In-memory repository implementation
 *
 * Useful for:
 * - Testing without external dependencies
 * - Prototyping before adding a real database
 * - Simple applications that don't need persistence
 */

import type { Example, ExampleRepository } from '../services/example.service.js';

export class InMemoryExampleRepository implements ExampleRepository {
  private store = new Map<string, Example>();

  async findById(id: string): Promise<Example | null> {
    return this.store.get(id) ?? null;
  }

  async findAll(): Promise<Example[]> {
    return Array.from(this.store.values());
  }

  async save(example: Example): Promise<Example> {
    this.store.set(example.id, example);
    return example;
  }

  async delete(id: string): Promise<void> {
    this.store.delete(id);
  }

  // Test helpers
  clear(): void {
    this.store.clear();
  }

  size(): number {
    return this.store.size;
  }
}
