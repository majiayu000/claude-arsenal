# Auth Attack Prevention

## OAuth/OIDC Attacks

### Authorization Code Injection

**Attack**: Attacker intercepts authorization code and uses it.

**Prevention**:
```typescript
// PKCE prevents code injection
// Code is useless without code_verifier

// Also: Bind code to client
const code = {
  value: crypto.randomBytes(32).toString('base64url'),
  clientId: request.clientId,
  redirectUri: request.redirectUri,
  codeChallenge: request.codeChallenge,
  userId: authenticatedUser.id,
  expiresAt: Date.now() + 60000, // 1 minute
};

// Validate all parameters match during exchange
function validateCodeExchange(code, request) {
  if (code.clientId !== request.clientId) throw new Error();
  if (code.redirectUri !== request.redirectUri) throw new Error();
  // PKCE verification
  const challenge = sha256(request.codeVerifier);
  if (code.codeChallenge !== challenge) throw new Error();
}
```

### Redirect URI Manipulation

**Attack**: Attacker modifies redirect_uri to steal tokens.

**Prevention**:
```typescript
// Exact match only
function validateRedirectUri(requested: string, client: Client): boolean {
  return client.registeredRedirectUris.includes(requested);
}

// NO pattern matching
// NO subdomain wildcards
// NO path prefixes
```

### CSRF on Authorization Endpoint

**Attack**: Attacker tricks user into authorizing attacker's account.

**Prevention**:
```typescript
// Use state parameter
const state = crypto.randomBytes(32).toString('base64url');
sessionStorage.setItem('oauth_state', state);

// Validate on callback
if (callbackState !== sessionStorage.getItem('oauth_state')) {
  throw new Error('CSRF detected');
}
```

### Token Leakage via Referrer

**Attack**: Token in URL fragment leaked via Referer header.

**Prevention**:
```typescript
// Use Authorization Code flow (not Implicit)
// Tokens never in URL

// If tokens must be in URL (legacy):
res.setHeader('Referrer-Policy', 'no-referrer');
```

---

## JWT Attacks

### Algorithm Confusion

**Attack**: Change algorithm from RS256 to HS256, sign with public key.

**Prevention**:
```typescript
// ALWAYS specify allowed algorithms
const payload = jwt.verify(token, key, {
  algorithms: ['ES256'], // Explicit whitelist
});

// NEVER trust header.alg blindly
```

### None Algorithm

**Attack**: Set algorithm to "none", remove signature.

**Prevention**:
```typescript
// Reject 'none' algorithm
const allowedAlgorithms = ['ES256', 'RS256'];
if (!allowedAlgorithms.includes(header.alg)) {
  throw new Error('Invalid algorithm');
}
```

### Key Injection (JKU/X5U)

**Attack**: Inject malicious key URL in header.

**Prevention**:
```typescript
// Whitelist key sources
const trustedJwksSources = [
  'https://auth.example.com/.well-known/jwks.json',
];

// Or ignore jku/x5u entirely, use configured keys only
if (header.jku && !trustedJwksSources.includes(header.jku)) {
  throw new Error('Untrusted key source');
}
```

### Signature Stripping

**Attack**: Remove signature, modify payload.

**Prevention**:
```typescript
// Verify signature BEFORE parsing claims
// All JWT libraries should do this by default
const { payload } = await jwtVerify(token, key);

// Check token has 3 parts
const parts = token.split('.');
if (parts.length !== 3) {
  throw new Error('Invalid JWT structure');
}
```

---

## Session Attacks

### Session Fixation

**Attack**: Attacker sets victim's session ID before authentication.

**Prevention**:
```typescript
// Regenerate session ID after login
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body);

  // Destroy old session
  req.session.destroy();

  // Create new session with new ID
  req.session.regenerate((err) => {
    req.session.userId = user.id;
    res.redirect('/dashboard');
  });
});
```

### Session Hijacking

**Attack**: Steal session cookie via XSS or network sniffing.

**Prevention**:
```typescript
// Secure cookie settings
app.use(session({
  cookie: {
    httpOnly: true,    // No JavaScript access
    secure: true,      // HTTPS only
    sameSite: 'strict', // No cross-site sending
    maxAge: 3600000,   // 1 hour
  },
  name: '__Host-session', // Cookie prefix for extra security
}));

// Bind session to client
req.session.userAgent = req.headers['user-agent'];
req.session.ip = req.ip;

// Validate on each request
if (req.session.userAgent !== req.headers['user-agent']) {
  req.session.destroy();
  throw new Error('Session binding mismatch');
}
```

---

## Token Attacks

### Refresh Token Theft

**Attack**: Steal refresh token, get unlimited access tokens.

**Prevention**:
```typescript
// Refresh token rotation
async function refresh(token: string) {
  const stored = await db.refreshToken.findUnique({ where: { token } });

  // Detect reuse (token already used)
  if (stored.usedAt) {
    // Revoke ALL user tokens
    await db.refreshToken.deleteMany({ where: { userId: stored.userId } });
    throw new Error('Token reuse detected - possible theft');
  }

  // Mark as used
  await db.refreshToken.update({
    where: { id: stored.id },
    data: { usedAt: new Date() },
  });

  // Issue new tokens
  return generateTokens(stored.userId);
}
```

### Token Replay

**Attack**: Reuse valid token for unauthorized requests.

**Prevention**:
```typescript
// Short-lived access tokens
const accessToken = jwt.sign(payload, key, { expiresIn: '15m' });

// Unique token ID
payload.jti = crypto.randomUUID();

// For high-security: One-time tokens
const usedTokens = new Set();
function validateOneTimeToken(token) {
  if (usedTokens.has(token.jti)) {
    throw new Error('Token already used');
  }
  usedTokens.add(token.jti);
}
```

### Token Sidejacking

**Attack**: Steal token in transit.

**Prevention**:
```typescript
// HTTPS everywhere
// HSTS header
res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');

// Token binding (DPoP)
const dpopProof = createDPoPProof(privateKey, method, url, accessToken);
```

---

## Brute Force Attacks

### Password Guessing

**Prevention**:
```typescript
// Rate limiting
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  keyGenerator: (req) => req.body.email,
});

// Account lockout
const MAX_FAILED_ATTEMPTS = 5;
const LOCKOUT_DURATION = 30 * 60 * 1000; // 30 minutes

async function login(email: string, password: string) {
  const user = await db.user.findUnique({ where: { email } });

  if (user.lockedUntil && user.lockedUntil > new Date()) {
    throw new Error('Account locked');
  }

  if (!await verifyPassword(password, user.passwordHash)) {
    await db.user.update({
      where: { id: user.id },
      data: {
        failedAttempts: { increment: 1 },
        lockedUntil: user.failedAttempts >= MAX_FAILED_ATTEMPTS - 1
          ? new Date(Date.now() + LOCKOUT_DURATION)
          : null,
      },
    });
    throw new Error('Invalid credentials');
  }

  // Reset on success
  await db.user.update({
    where: { id: user.id },
    data: { failedAttempts: 0, lockedUntil: null },
  });
}
```

### Token Guessing

**Prevention**:
```typescript
// Sufficient entropy
const token = crypto.randomBytes(32).toString('base64url');
// 256 bits of entropy - infeasible to guess

// Constant-time comparison
const isValid = crypto.timingSafeEqual(
  Buffer.from(providedToken),
  Buffer.from(storedToken)
);
```

---

## XSS and CSRF

### XSS Token Theft

**Prevention**:
```typescript
// HttpOnly cookies (tokens not accessible to JS)
res.cookie('token', token, { httpOnly: true });

// Content Security Policy
res.setHeader('Content-Security-Policy', [
  "default-src 'self'",
  "script-src 'self'",
].join('; '));

// Never store tokens in localStorage
// ❌ localStorage.setItem('token', token);
```

### CSRF Token Theft

**Prevention**:
```typescript
// SameSite cookies
res.cookie('session', token, {
  sameSite: 'strict', // or 'lax'
});

// CSRF token for non-GET requests
app.use(csrf());
app.use((req, res, next) => {
  res.locals.csrfToken = req.csrfToken();
  next();
});
```
