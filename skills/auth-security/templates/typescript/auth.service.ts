/**
 * Authentication Service
 * OAuth 2.1 + JWT implementation following RFC 9700
 */

import { SignJWT, jwtVerify, createRemoteJWKSet, errors } from 'jose';
import crypto from 'crypto';

// ============================================
// Types
// ============================================

interface TokenPayload {
  iss: string;
  sub: string;
  aud: string;
  exp: number;
  iat: number;
  jti: string;
  scope: string;
}

interface TokenPair {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

interface PKCEChallenge {
  verifier: string;
  challenge: string;
}

// ============================================
// Configuration
// ============================================

const config = {
  issuer: process.env.AUTH_ISSUER || 'https://auth.example.com',
  audience: process.env.AUTH_AUDIENCE || 'https://api.example.com',
  accessTokenTTL: 15 * 60,      // 15 minutes
  refreshTokenTTL: 7 * 24 * 60 * 60, // 7 days
  algorithm: 'ES256' as const,
};

// ============================================
// PKCE
// ============================================

export function generatePKCE(): PKCEChallenge {
  const verifier = crypto.randomBytes(32).toString('base64url');
  const challenge = crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');

  return { verifier, challenge };
}

export function verifyPKCE(verifier: string, challenge: string): boolean {
  const computed = crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');

  return crypto.timingSafeEqual(
    Buffer.from(computed),
    Buffer.from(challenge)
  );
}

// ============================================
// Token Generation
// ============================================

export async function generateAccessToken(
  privateKey: CryptoKey,
  keyId: string,
  userId: string,
  scope: string
): Promise<string> {
  return new SignJWT({
    scope,
  })
    .setProtectedHeader({
      alg: config.algorithm,
      typ: 'at+jwt',
      kid: keyId,
    })
    .setIssuer(config.issuer)
    .setSubject(userId)
    .setAudience(config.audience)
    .setExpirationTime(`${config.accessTokenTTL}s`)
    .setIssuedAt()
    .setJti(crypto.randomUUID())
    .sign(privateKey);
}

export function generateRefreshToken(): string {
  return crypto.randomBytes(32).toString('base64url');
}

export async function generateTokenPair(
  privateKey: CryptoKey,
  keyId: string,
  userId: string,
  scope: string
): Promise<TokenPair> {
  const [accessToken, refreshToken] = await Promise.all([
    generateAccessToken(privateKey, keyId, userId, scope),
    Promise.resolve(generateRefreshToken()),
  ]);

  return {
    accessToken,
    refreshToken,
    expiresIn: config.accessTokenTTL,
  };
}

// ============================================
// Token Verification
// ============================================

const JWKS = createRemoteJWKSet(
  new URL(`${config.issuer}/.well-known/jwks.json`)
);

export async function verifyAccessToken(token: string): Promise<TokenPayload> {
  try {
    const { payload, protectedHeader } = await jwtVerify(token, JWKS, {
      // CRITICAL: Explicit algorithm whitelist
      algorithms: [config.algorithm],
      issuer: config.issuer,
      audience: config.audience,
      clockTolerance: 30,
    });

    // Validate token type
    if (protectedHeader.typ !== 'at+jwt') {
      throw new AuthError('Invalid token type', 'INVALID_TOKEN_TYPE');
    }

    // Validate required claims
    if (!payload.sub || !payload.scope) {
      throw new AuthError('Missing required claims', 'MISSING_CLAIMS');
    }

    return payload as TokenPayload;
  } catch (err) {
    if (err instanceof errors.JWTExpired) {
      throw new AuthError('Token expired', 'TOKEN_EXPIRED');
    }
    if (err instanceof errors.JWTClaimValidationFailed) {
      throw new AuthError('Invalid claims', 'INVALID_CLAIMS');
    }
    if (err instanceof AuthError) {
      throw err;
    }
    throw new AuthError('Invalid token', 'INVALID_TOKEN');
  }
}

// ============================================
// Scope Validation
// ============================================

export function validateScope(
  tokenScope: string,
  requiredScopes: string[]
): void {
  const scopes = tokenScope.split(' ');
  const missing = requiredScopes.filter(s => !scopes.includes(s));

  if (missing.length > 0) {
    throw new AuthError(
      `Missing scopes: ${missing.join(', ')}`,
      'INSUFFICIENT_SCOPE'
    );
  }
}

export function hasScope(tokenScope: string, scope: string): boolean {
  return tokenScope.split(' ').includes(scope);
}

// ============================================
// Refresh Token Rotation
// ============================================

interface StoredRefreshToken {
  id: string;
  token: string;
  userId: string;
  usedAt: Date | null;
  expiresAt: Date;
}

// In production, use database
const refreshTokenStore = new Map<string, StoredRefreshToken>();

export async function storeRefreshToken(
  token: string,
  userId: string
): Promise<void> {
  const hashed = hashToken(token);
  refreshTokenStore.set(hashed, {
    id: crypto.randomUUID(),
    token: hashed,
    userId,
    usedAt: null,
    expiresAt: new Date(Date.now() + config.refreshTokenTTL * 1000),
  });
}

export async function rotateRefreshToken(
  oldToken: string,
  privateKey: CryptoKey,
  keyId: string
): Promise<TokenPair> {
  const hashed = hashToken(oldToken);
  const stored = refreshTokenStore.get(hashed);

  if (!stored) {
    throw new AuthError('Invalid refresh token', 'INVALID_TOKEN');
  }

  // Check if already used (reuse detection)
  if (stored.usedAt) {
    // Potential token theft - revoke all user tokens
    revokeAllUserTokens(stored.userId);
    throw new AuthError('Token reuse detected', 'TOKEN_REUSE');
  }

  // Check expiration
  if (stored.expiresAt < new Date()) {
    throw new AuthError('Refresh token expired', 'TOKEN_EXPIRED');
  }

  // Mark as used
  stored.usedAt = new Date();

  // Generate new tokens
  const newTokens = await generateTokenPair(
    privateKey,
    keyId,
    stored.userId,
    'read write' // Get scope from stored token in production
  );

  // Store new refresh token
  await storeRefreshToken(newTokens.refreshToken, stored.userId);

  return newTokens;
}

// ============================================
// Token Revocation
// ============================================

export function revokeAllUserTokens(userId: string): void {
  for (const [key, token] of refreshTokenStore.entries()) {
    if (token.userId === userId) {
      refreshTokenStore.delete(key);
    }
  }
}

export function revokeRefreshToken(token: string): void {
  const hashed = hashToken(token);
  refreshTokenStore.delete(hashed);
}

// ============================================
// Utilities
// ============================================

function hashToken(token: string): string {
  return crypto.createHash('sha256').update(token).digest('hex');
}

// ============================================
// Errors
// ============================================

export class AuthError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 401
  ) {
    super(message);
    this.name = 'AuthError';
  }
}

// ============================================
// Middleware (Express example)
// ============================================

import type { Request, Response, NextFunction } from 'express';

declare global {
  namespace Express {
    interface Request {
      user?: TokenPayload;
    }
  }
}

export function authMiddleware(requiredScopes?: string[]) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const authHeader = req.headers.authorization;
      if (!authHeader?.startsWith('Bearer ')) {
        throw new AuthError('Missing authorization header', 'MISSING_AUTH');
      }

      const token = authHeader.slice(7);
      const payload = await verifyAccessToken(token);

      if (requiredScopes) {
        validateScope(payload.scope, requiredScopes);
      }

      req.user = payload;
      next();
    } catch (err) {
      if (err instanceof AuthError) {
        res.status(err.statusCode).json({
          error: err.code,
          message: err.message,
        });
      } else {
        res.status(500).json({ error: 'INTERNAL_ERROR' });
      }
    }
  };
}
