# JWT Deep Dive

## Token Types

### Access Token

Short-lived, used for API authorization.

```typescript
interface AccessToken {
  // Header
  alg: 'ES256';
  typ: 'at+jwt';  // RFC 9068
  kid: string;

  // Payload
  iss: string;    // https://auth.example.com
  sub: string;    // User ID
  aud: string;    // https://api.example.com
  exp: number;    // 15 minutes from now
  iat: number;
  jti: string;    // Unique ID
  scope: string;  // 'read write'
  client_id: string;
}
```

### Refresh Token

Longer-lived, used to obtain new access tokens.

```typescript
// Can be JWT or opaque string
// Opaque recommended (stored server-side)
const refreshToken = crypto.randomBytes(32).toString('base64url');

// If JWT, use longer expiration
interface RefreshToken {
  alg: 'ES256';
  typ: 'rt+jwt';

  iss: string;
  sub: string;
  aud: string;
  exp: number;    // 7-30 days
  iat: number;
  jti: string;
}
```

### ID Token (OpenID Connect)

Contains user identity information.

```typescript
interface IdToken {
  // Header
  alg: 'ES256';
  typ: 'JWT';
  kid: string;

  // Payload
  iss: string;
  sub: string;          // Unique user identifier
  aud: string;          // Client ID
  exp: number;
  iat: number;
  auth_time: number;    // When user authenticated
  nonce: string;        // Replay protection

  // Optional claims
  name?: string;
  email?: string;
  email_verified?: boolean;
  picture?: string;
}
```

---

## Signing & Verification

### Key Management

```typescript
import { generateKeyPair, exportJWK, importJWK } from 'jose';

// Generate key pair
async function generateSigningKey() {
  const { publicKey, privateKey } = await generateKeyPair('ES256', {
    extractable: true,
  });

  const publicJwk = await exportJWK(publicKey);
  const privateJwk = await exportJWK(privateKey);

  // Add key ID
  const kid = crypto.randomUUID();
  publicJwk.kid = kid;
  privateJwk.kid = kid;
  publicJwk.use = 'sig';
  privateJwk.use = 'sig';
  publicJwk.alg = 'ES256';
  privateJwk.alg = 'ES256';

  return { publicJwk, privateJwk, kid };
}
```

### Key Rotation

```typescript
class KeyManager {
  private keys: Map<string, CryptoKeyPair> = new Map();
  private currentKeyId: string;

  async rotate() {
    const { publicJwk, privateJwk, kid } = await generateSigningKey();
    const publicKey = await importJWK(publicJwk, 'ES256');
    const privateKey = await importJWK(privateJwk, 'ES256');

    this.keys.set(kid, { publicKey, privateKey });
    this.currentKeyId = kid;

    // Keep old keys for verification (token lifetime)
    // Remove after 2x max token lifetime
  }

  getSigningKey(): { key: CryptoKey; kid: string } {
    return {
      key: this.keys.get(this.currentKeyId)!.privateKey,
      kid: this.currentKeyId,
    };
  }

  getVerificationKey(kid: string): CryptoKey | undefined {
    return this.keys.get(kid)?.publicKey;
  }

  getJWKS(): { keys: JsonWebKey[] } {
    return {
      keys: Array.from(this.keys.entries()).map(([kid, pair]) => ({
        ...pair.publicKey,
        kid,
      })),
    };
  }
}
```

### JWKS Endpoint

```typescript
// GET /.well-known/jwks.json
app.get('/.well-known/jwks.json', (req, res) => {
  res.json(keyManager.getJWKS());
});

// Client fetches and caches JWKS
import { createRemoteJWKSet } from 'jose';

const JWKS = createRemoteJWKSet(
  new URL('https://auth.example.com/.well-known/jwks.json')
);

const { payload } = await jwtVerify(token, JWKS, {
  algorithms: ['ES256'],
  issuer: 'https://auth.example.com',
});
```

---

## Claim Validation

### Required Validations

```typescript
async function validateToken(token: string): Promise<TokenPayload> {
  // 1. Decode and verify signature
  const { payload, protectedHeader } = await jwtVerify(token, getKey, {
    algorithms: ['ES256'],
  });

  // 2. Validate issuer
  if (payload.iss !== 'https://auth.example.com') {
    throw new Error('Invalid issuer');
  }

  // 3. Validate audience
  const validAudiences = ['https://api.example.com'];
  if (!validAudiences.includes(payload.aud as string)) {
    throw new Error('Invalid audience');
  }

  // 4. Validate expiration (handled by jwtVerify)
  // 5. Validate not before (handled by jwtVerify)

  // 6. Validate token type
  if (protectedHeader.typ !== 'at+jwt') {
    throw new Error('Invalid token type');
  }

  // 7. Validate required claims exist
  if (!payload.sub || !payload.scope) {
    throw new Error('Missing required claims');
  }

  return payload as TokenPayload;
}
```

### Custom Claim Validation

```typescript
function validateScope(payload: TokenPayload, required: string[]): void {
  const tokenScopes = (payload.scope as string).split(' ');
  const missing = required.filter(s => !tokenScopes.includes(s));

  if (missing.length > 0) {
    throw new InsufficientScopeError(missing);
  }
}

function validateRoles(payload: TokenPayload, required: string[]): void {
  const userRoles = payload.roles || [];
  const missing = required.filter(r => !userRoles.includes(r));

  if (missing.length > 0) {
    throw new InsufficientRoleError(missing);
  }
}
```

---

## Security Patterns

### Audience Restriction

```typescript
// Different tokens for different APIs
const apiAudiences = {
  'https://api.example.com': ['read', 'write'],
  'https://admin.example.com': ['admin'],
  'https://internal.example.com': ['internal'],
};

// Validate audience matches the API being accessed
function validateAudienceForApi(token: TokenPayload, apiUrl: string): void {
  if (token.aud !== apiUrl) {
    throw new Error(`Token not valid for ${apiUrl}`);
  }
}
```

### Token Binding

```typescript
// Bind token to client fingerprint
interface BoundToken extends TokenPayload {
  cnf: {
    'x5t#S256': string;  // Certificate thumbprint
    jkt: string;          // JWK thumbprint (for DPoP)
  };
}

// Validate binding
function validateTokenBinding(token: BoundToken, clientJwk: JsonWebKey): void {
  const thumbprint = await calculateJwkThumbprint(clientJwk, 'sha256');
  if (token.cnf.jkt !== thumbprint) {
    throw new Error('Token not bound to this client');
  }
}
```

### Phantom Token Pattern

```typescript
// Public: Opaque reference token
// Internal: JWT with full claims

// Token endpoint returns opaque token
app.post('/token', (req, res) => {
  const jwt = generateFullJwt(user);
  const reference = crypto.randomBytes(32).toString('base64url');

  // Store mapping
  await redis.set(`token:${reference}`, jwt, 'EX', 900);

  res.json({ access_token: reference, token_type: 'Bearer' });
});

// API Gateway exchanges for JWT
async function exchangeToken(reference: string): Promise<string> {
  const jwt = await redis.get(`token:${reference}`);
  if (!jwt) throw new Error('Invalid token');
  return jwt;
}
```

---

## Common Vulnerabilities

### Algorithm Confusion

```typescript
// VULNERABLE: Accepts algorithm from header
const decoded = jwt.verify(token, secret);

// SECURE: Explicit algorithm
const decoded = jwt.verify(token, key, { algorithms: ['ES256'] });

// VULNERABLE: Accepts 'none' algorithm
// SECURE: Never allow 'none'
```

### Key Confusion

```typescript
// VULNERABLE: Symmetric key treated as public key
// Attacker signs with public key, server verifies with same key

// SECURE: Different key types for different algorithms
function getVerificationKey(header: JWTHeader) {
  if (header.alg.startsWith('RS') || header.alg.startsWith('ES')) {
    return asymmetricPublicKey;
  } else if (header.alg.startsWith('HS')) {
    return symmetricSecret;
  }
  throw new Error('Unsupported algorithm');
}
```

### JKU/X5U Injection

```typescript
// VULNERABLE: Fetches key from untrusted URL in header
const { jku } = header;
const keys = await fetch(jku).then(r => r.json());

// SECURE: Whitelist allowed key URLs
const allowedJku = ['https://auth.example.com/.well-known/jwks.json'];
if (!allowedJku.includes(header.jku)) {
  throw new Error('Untrusted key source');
}
```

### Weak Secrets

```typescript
// VULNERABLE: Short, predictable secret
const secret = 'password123';

// SECURE: Cryptographically random, sufficient length
const secret = crypto.randomBytes(32).toString('base64');
// Or use asymmetric keys (preferred)
```
