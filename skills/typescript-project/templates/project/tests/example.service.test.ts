/**
 * Example service tests
 *
 * Uses real implementations (in-memory repository) instead of mocks.
 * Tests actual behavior, not implementation details.
 */

import { describe, it, expect, beforeEach } from 'bun:test';
import { ExampleService } from '../src/services/example.service.js';
import { InMemoryExampleRepository } from '../src/adapters/in-memory.repository.js';

describe('ExampleService', () => {
  let service: ExampleService;
  let repo: InMemoryExampleRepository;

  beforeEach(() => {
    repo = new InMemoryExampleRepository();
    service = new ExampleService(repo);
  });

  describe('create', () => {
    it('creates example with valid input', async () => {
      const result = await service.create({
        name: 'Test Example',
        description: 'A test description',
      });

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.name).toBe('Test Example');
        expect(result.value.description).toBe('A test description');
        expect(result.value.id).toBeDefined();
        expect(result.value.createdAt).toBeInstanceOf(Date);
      }
    });

    it('rejects empty name', async () => {
      const result = await service.create({
        name: '',
      });

      expect(result.ok).toBe(false);
      if (!result.ok) {
        expect(result.error.code).toBe('VALIDATION_ERROR');
      }
    });

    it('persists to repository', async () => {
      const result = await service.create({ name: 'Persisted' });

      expect(result.ok).toBe(true);
      if (result.ok) {
        const found = await repo.findById(result.value.id);
        expect(found).toEqual(result.value);
      }
    });
  });

  describe('findById', () => {
    it('returns example when found', async () => {
      const created = await service.create({ name: 'Find Me' });
      if (!created.ok) throw new Error('Setup failed');

      const result = await service.findById(created.value.id);

      expect(result.ok).toBe(true);
      if (result.ok) {
        expect(result.value.name).toBe('Find Me');
      }
    });

    it('returns error when not found', async () => {
      const result = await service.findById('non-existent-id');

      expect(result.ok).toBe(false);
      if (!result.ok) {
        expect(result.error.code).toBe('NOT_FOUND');
      }
    });
  });

  describe('delete', () => {
    it('deletes existing example', async () => {
      const created = await service.create({ name: 'Delete Me' });
      if (!created.ok) throw new Error('Setup failed');

      const result = await service.delete(created.value.id);

      expect(result.ok).toBe(true);
      expect(await repo.findById(created.value.id)).toBeNull();
    });

    it('returns error for non-existent example', async () => {
      const result = await service.delete('non-existent-id');

      expect(result.ok).toBe(false);
      if (!result.ok) {
        expect(result.error.code).toBe('NOT_FOUND');
      }
    });
  });

  describe('findAll', () => {
    it('returns all examples', async () => {
      await service.create({ name: 'First' });
      await service.create({ name: 'Second' });
      await service.create({ name: 'Third' });

      const all = await service.findAll();

      expect(all).toHaveLength(3);
      expect(all.map((e) => e.name)).toContain('First');
      expect(all.map((e) => e.name)).toContain('Second');
      expect(all.map((e) => e.name)).toContain('Third');
    });

    it('returns empty array when no examples', async () => {
      const all = await service.findAll();
      expect(all).toHaveLength(0);
    });
  });
});
