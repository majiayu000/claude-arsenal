/**
 * Shared type definitions
 */

/**
 * Result type for operations that can fail
 */
export type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export const Result = {
  ok: <T>(value: T): Result<T, never> => ({ ok: true, value }),
  err: <E>(error: E): Result<never, E> => ({ ok: false, error }),

  map: <T, U, E>(result: Result<T, E>, fn: (value: T) => U): Result<U, E> =>
    result.ok ? Result.ok(fn(result.value)) : result,

  unwrap: <T, E>(result: Result<T, E>): T => {
    if (!result.ok) throw result.error;
    return result.value;
  },
};

/**
 * Branded types for type-safe IDs
 */
export type Brand<T, B> = T & { readonly __brand: B };

export type UserId = Brand<string, 'UserId'>;
export type OrderId = Brand<string, 'OrderId'>;

/**
 * Utility types
 */
export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type AsyncResult<T, E = Error> = Promise<Result<T, E>>;
