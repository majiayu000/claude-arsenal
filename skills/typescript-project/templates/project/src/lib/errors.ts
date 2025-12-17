/**
 * Custom error classes
 */

export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'AppError';
    Error.captureStackTrace(this, this.constructor);
  }

  static notFound(resource: string, id: string): AppError {
    return new AppError(`${resource} not found: ${id}`, 'NOT_FOUND', 404, {
      resource,
      id,
    });
  }

  static validation(message: string, context?: Record<string, unknown>): AppError {
    return new AppError(message, 'VALIDATION_ERROR', 400, context);
  }

  static unauthorized(message = 'Unauthorized'): AppError {
    return new AppError(message, 'UNAUTHORIZED', 401);
  }

  static forbidden(message = 'Forbidden'): AppError {
    return new AppError(message, 'FORBIDDEN', 403);
  }

  static conflict(message: string, context?: Record<string, unknown>): AppError {
    return new AppError(message, 'CONFLICT', 409, context);
  }

  static internal(message: string, context?: Record<string, unknown>): AppError {
    return new AppError(message, 'INTERNAL_ERROR', 500, context);
  }

  toJSON() {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      statusCode: this.statusCode,
      context: this.context,
    };
  }
}

/**
 * Type guard for AppError
 */
export function isAppError(error: unknown): error is AppError {
  return error instanceof AppError;
}
