# OAuth 2.1 Deep Dive

## RFC 9700 Summary

Published January 2025, consolidates security best practices from:
- RFC 6749 (OAuth 2.0)
- RFC 7636 (PKCE)
- RFC 8252 (Native Apps)
- RFC 6819 (Threat Model)
- Various security BCPs

---

## Grant Types

### Authorization Code (REQUIRED)

The only grant type for user authentication.

```
┌──────────┐     ┌───────────┐     ┌──────────────┐
│  Client  │────▶│   Auth    │────▶│   Resource   │
│   App    │◀────│  Server   │◀────│    Server    │
└──────────┘     └───────────┘     └──────────────┘

1. Client redirects to Auth Server with PKCE challenge
2. User authenticates
3. Auth Server redirects back with code
4. Client exchanges code + verifier for tokens
5. Client accesses Resource Server with access token
```

### Client Credentials

For server-to-server communication (no user context).

```typescript
const response = await fetch('https://auth.example.com/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    Authorization: `Basic ${btoa(`${clientId}:${clientSecret}`)}`,
  },
  body: new URLSearchParams({
    grant_type: 'client_credentials',
    scope: 'api:read api:write',
  }),
});
```

### Refresh Token

For obtaining new access tokens without re-authentication.

```typescript
const response = await fetch('https://auth.example.com/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: currentRefreshToken,
    client_id: CLIENT_ID,
  }),
});

const { access_token, refresh_token } = await response.json();
// IMPORTANT: Store new refresh_token, old one is invalidated
```

---

## PKCE Implementation

### Code Verifier Requirements

- Length: 43-128 characters
- Characters: `[A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"`
- Must be cryptographically random

```typescript
function generateCodeVerifier(): string {
  // 32 bytes = 43 base64url characters
  const buffer = crypto.randomBytes(32);
  return buffer.toString('base64url');
}
```

### Code Challenge

```typescript
// S256 method (REQUIRED if supported)
function generateCodeChallenge(verifier: string): string {
  return crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');
}

// Plain method (only if S256 not supported)
// NOT RECOMMENDED - only for legacy compatibility
function generatePlainChallenge(verifier: string): string {
  return verifier;
}
```

### Full PKCE Flow

```typescript
class PKCEFlow {
  private verifier: string;
  private state: string;

  constructor() {
    this.verifier = generateCodeVerifier();
    this.state = crypto.randomBytes(16).toString('hex');
  }

  getAuthorizationUrl(config: AuthConfig): string {
    const url = new URL(config.authorizationEndpoint);

    url.searchParams.set('response_type', 'code');
    url.searchParams.set('client_id', config.clientId);
    url.searchParams.set('redirect_uri', config.redirectUri);
    url.searchParams.set('scope', config.scope);
    url.searchParams.set('state', this.state);
    url.searchParams.set('code_challenge', generateCodeChallenge(this.verifier));
    url.searchParams.set('code_challenge_method', 'S256');

    // OpenID Connect
    if (config.scope.includes('openid')) {
      url.searchParams.set('nonce', crypto.randomBytes(16).toString('hex'));
    }

    return url.toString();
  }

  async exchangeCode(code: string, receivedState: string, config: AuthConfig): Promise<TokenResponse> {
    // Validate state
    if (receivedState !== this.state) {
      throw new Error('State mismatch - possible CSRF attack');
    }

    const response = await fetch(config.tokenEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        redirect_uri: config.redirectUri,
        client_id: config.clientId,
        code_verifier: this.verifier,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new AuthError(error.error_description || error.error);
    }

    return response.json();
  }
}
```

---

## Client Authentication

### Confidential Clients

```typescript
// Method 1: client_secret_basic (Header)
const credentials = btoa(`${clientId}:${clientSecret}`);
headers['Authorization'] = `Basic ${credentials}`;

// Method 2: client_secret_post (Body)
body.append('client_id', clientId);
body.append('client_secret', clientSecret);

// Method 3: private_key_jwt (Recommended for high security)
const assertion = await new SignJWT({
  iss: clientId,
  sub: clientId,
  aud: tokenEndpoint,
})
  .setProtectedHeader({ alg: 'ES256' })
  .setExpirationTime('5m')
  .setIssuedAt()
  .setJti(crypto.randomUUID())
  .sign(privateKey);

body.append('client_assertion_type', 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer');
body.append('client_assertion', assertion);
```

### Public Clients

- Mobile apps, SPAs, desktop apps
- Cannot store secrets securely
- MUST use PKCE
- client_id only (no secret)

---

## Redirect URI Validation

### Server-Side

```typescript
function validateRedirectUri(requested: string, registered: string[]): boolean {
  // MUST be exact match (no pattern matching)
  return registered.includes(requested);
}

// Avoid these patterns (security risks):
// ❌ Wildcard subdomains: https://*.example.com/callback
// ❌ Path prefix: https://example.com/callback/*
// ❌ Query parameter variations
```

### Registered URIs

```typescript
const registeredRedirectUris = [
  'https://app.example.com/callback',
  'https://staging.example.com/callback',
  // Mobile: Custom scheme
  'com.example.app://callback',
  // Desktop: Loopback
  'http://127.0.0.1/callback',
  'http://[::1]/callback',
];
```

---

## Token Response

### Standard Fields

```typescript
interface TokenResponse {
  access_token: string;
  token_type: 'Bearer' | 'DPoP';
  expires_in: number;           // Seconds until expiration
  refresh_token?: string;       // Optional
  scope?: string;               // May differ from requested
  id_token?: string;            // OpenID Connect
}
```

### Error Response

```typescript
interface TokenErrorResponse {
  error: 'invalid_request' | 'invalid_client' | 'invalid_grant' |
         'unauthorized_client' | 'unsupported_grant_type' | 'invalid_scope';
  error_description?: string;
  error_uri?: string;
}
```

---

## Scopes

### Design Guidelines

```typescript
// Resource-based scopes
const scopes = [
  'users:read',
  'users:write',
  'orders:read',
  'orders:write',
  'admin:full',
];

// Action-based scopes
const scopes = [
  'read',
  'write',
  'delete',
  'admin',
];

// OpenID Connect scopes
const oidcScopes = [
  'openid',   // Required for OIDC
  'profile',  // name, family_name, etc.
  'email',    // email, email_verified
  'address',  // address claim
  'phone',    // phone_number, phone_number_verified
];
```

### Scope Validation

```typescript
function validateScopes(requested: string[], allowed: string[]): string[] {
  // Return intersection of requested and allowed
  return requested.filter(scope => allowed.includes(scope));
}

function hasScope(tokenScopes: string, required: string): boolean {
  const scopes = tokenScopes.split(' ');
  return scopes.includes(required);
}
```

---

## Security Considerations

### State Parameter

```typescript
// Generate cryptographically random state
const state = crypto.randomBytes(32).toString('base64url');

// Store in session before redirect
session.oauthState = state;

// Validate on callback
if (callbackState !== session.oauthState) {
  throw new Error('Invalid state - CSRF detected');
}
```

### Nonce (OpenID Connect)

```typescript
// Include in authorization request
url.searchParams.set('nonce', crypto.randomBytes(16).toString('hex'));

// Validate in ID token
if (idToken.nonce !== session.nonce) {
  throw new Error('Invalid nonce - replay attack detected');
}
```

### Token Binding

```typescript
// DPoP (Demonstration of Proof of Possession)
// Binds tokens to client's key pair

// 1. Client generates key pair
const { publicKey, privateKey } = await crypto.subtle.generateKey(
  { name: 'ECDSA', namedCurve: 'P-256' },
  true,
  ['sign', 'verify']
);

// 2. Create DPoP proof for token request
const dpopProof = await createDPoPProof(privateKey, {
  htm: 'POST',
  htu: tokenEndpoint,
});

// 3. Include in token request
headers['DPoP'] = dpopProof;

// 4. Server binds token to public key
// 5. All API requests require fresh DPoP proof
```
