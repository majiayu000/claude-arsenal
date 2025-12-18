# Container and Kubernetes Best Practices

## Docker Best Practices

### Multi-Stage Builds Explained

**The Problem:** Node.js images with build tools are 900MB+. Production only needs the runtime.

**The Solution:** Separate build and runtime stages.

```dockerfile
# ============================================
# Stage 1: Dependencies (Build Stage)
# ============================================
FROM node:20-alpine AS dependencies
WORKDIR /app

# Copy package files only (better caching)
COPY package*.json ./

# Install ALL dependencies (dev + prod)
RUN npm ci

# ============================================
# Stage 2: Build Application
# ============================================
FROM dependencies AS builder
WORKDIR /app

# Copy source code
COPY . .

# Build application (TypeScript, webpack, etc.)
RUN npm run build

# Remove dev dependencies
RUN npm prune --production

# ============================================
# Stage 3: Runtime (Production Image)
# ============================================
FROM node:20-alpine AS runtime

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy only production dependencies
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules

# Copy built application
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

# Start application
CMD ["node", "dist/server.js"]
```

**Result:** 100MB final image (90% reduction) with same functionality.

---

### Security Hardening

#### 1. Use Minimal Base Images

```dockerfile
# ❌ BAD: Full OS image (1.2GB)
FROM ubuntu:22.04

# ⚠️  ACCEPTABLE: Official Node (180MB)
FROM node:20-alpine

# ✅ BETTER: Distroless (no shell, minimal attack surface)
FROM gcr.io/distroless/nodejs20-debian12

# ✅ BEST: Scratch (only app binary, <10MB)
FROM scratch
COPY --from=builder /app/binary /binary
ENTRYPOINT ["/binary"]
```

#### 2. Run as Non-Root User

```dockerfile
# ❌ BAD: Runs as root (UID 0)
FROM node:20-alpine
COPY . /app
CMD ["node", "server.js"]

# ✅ GOOD: Create and use non-root user
FROM node:20-alpine

# Create user with specific UID/GID
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set ownership
COPY --chown=nodejs:nodejs . /app

# Switch user
USER nodejs

CMD ["node", "server.js"]

# ✅ BEST: Use distroless with predefined user
FROM gcr.io/distroless/nodejs20-debian12
COPY --chown=65532:65532 /app /app
USER 65532  # nonroot user in distroless
```

#### 3. Read-Only Filesystem

```dockerfile
# Enable read-only root filesystem
FROM node:20-alpine
RUN adduser -S -u 1001 nodejs

# Create writable temp directory
RUN mkdir -p /tmp && chown nodejs:nodejs /tmp

USER nodejs
WORKDIR /app
COPY --chown=nodejs:nodejs . .

# Run with read-only flag
# docker run --read-only --tmpfs /tmp myapp
```

#### 4. Resource Limits

```dockerfile
# Set memory and CPU limits
# docker run --memory="512m" --cpus="0.5" myapp

# In docker-compose.yml
services:
  app:
    image: myapp
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

#### 5. No Secrets in Layers

```dockerfile
# ❌ BAD: Secret in layer (visible in image history)
RUN curl -H "Authorization: Bearer secret-token" https://api.example.com/data

# ✅ GOOD: Use build secrets (BuildKit)
# docker buildx build --secret id=token,env=API_TOKEN .
RUN --mount=type=secret,id=token \
    curl -H "Authorization: Bearer $(cat /run/secrets/token)" https://api.example.com/data

# ✅ BEST: Fetch secrets at runtime
CMD ["sh", "-c", "export API_TOKEN=$(aws secretsmanager get-secret-value ...) && node server.js"]
```

#### 6. Vulnerability Scanning

```bash
# Scan image with Trivy
trivy image --severity HIGH,CRITICAL myapp:latest

# Scan in CI/CD
docker build -t myapp:$VERSION .
trivy image --exit-code 1 --severity CRITICAL myapp:$VERSION
```

---

### Layer Caching Optimization

**Docker builds layers sequentially. A change invalidates all subsequent layers.**

```dockerfile
# ❌ BAD: Source code changes invalidate dependency install
FROM node:20-alpine
WORKDIR /app
COPY . .                    # Changes frequently
RUN npm ci                  # Re-runs on every code change!
RUN npm run build

# ✅ GOOD: Dependencies cached separately
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./       # Changes infrequently
RUN npm ci                  # Cached unless package.json changes
COPY . .                    # Source code changes don't affect deps
RUN npm run build
```

**Ordering principle:** Put frequently changing files at the bottom.

```dockerfile
# Order by change frequency (least to most)
COPY package*.json ./           # Changes rarely
RUN npm ci
COPY tsconfig.json ./           # Changes occasionally
COPY src/ ./src/                # Changes frequently
RUN npm run build
```

---

### .dockerignore Best Practices

```
# Version Control
.git/
.gitignore
.gitattributes

# Dependencies (install fresh in container)
node_modules/
vendor/
__pycache__/
*.pyc
.venv/

# Build artifacts
dist/
build/
*.o
*.so

# Environment files
.env
.env.*
!.env.example

# Secrets
secrets/
*.key
*.pem
*.crt
credentials.json

# Documentation
README.md
CHANGELOG.md
docs/

# Development files
.vscode/
.idea/
*.swp
*.swo

# Testing
tests/
test/
spec/
coverage/
*.test.js
*.spec.ts

# CI/CD
.github/
.gitlab-ci.yml
Jenkinsfile
docker-compose.yml
Dockerfile*

# OS files
.DS_Store
Thumbs.db

# Logs
logs/
*.log
npm-debug.log*
```

---

## Kubernetes Best Practices

### 1. Resource Management (Right-Sizing)

**Problem:** 99.94% of clusters are over-provisioned (average CPU: 10%, memory: 23%).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0
        resources:
          # REQUESTS: Guaranteed allocation (scheduling decision)
          requests:
            memory: "256Mi"   # Needs at least 256MB
            cpu: "200m"       # Needs 0.2 CPU cores

          # LIMITS: Maximum allowed (OOM kill/throttle)
          limits:
            memory: "512Mi"   # Killed if exceeds 512MB
            cpu: "500m"       # Throttled if exceeds 0.5 cores
```

**How to determine values:**

```bash
# 1. Start with conservative estimates
requests:
  memory: "128Mi"
  cpu: "100m"

# 2. Monitor actual usage
kubectl top pod myapp-xyz

# 3. Use Vertical Pod Autoscaler (VPA) for recommendations
kubectl get vpa myapp -o yaml

# 4. Or use Goldilocks for right-sizing suggestions
# Analyzes VPA and provides recommendations
```

**Resource Units:**
- CPU: `1000m` = 1 CPU core = 1 vCPU
- Memory: `1Mi` = 1 Mebibyte = 1.048576 MB

---

### 2. Health Checks (Probes)

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0
        ports:
        - containerPort: 8080

        # STARTUP PROBE: Has the application started?
        # Used for slow-starting applications
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          initialDelaySeconds: 0
          periodSeconds: 10
          failureThreshold: 30  # 30*10s = 5 minutes for slow startup
          # Runs BEFORE liveness and readiness probes

        # LIVENESS PROBE: Is the application alive?
        # Restart container if fails
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3   # Restart after 3 consecutive failures
          successThreshold: 1

        # READINESS PROBE: Can it receive traffic?
        # Remove from service if fails
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
          successThreshold: 1   # Add to service after 1 success
```

**Health Endpoint Implementation:**

```typescript
// Express.js example
app.get('/startup', (req, res) => {
  // Check if database connections established, migrations run
  if (!db.isConnected() || !migrationsComplete) {
    return res.status(503).send('Not ready');
  }
  res.status(200).send('Started');
});

app.get('/health', (req, res) => {
  // Deep health check - is app functioning?
  if (!canProcessRequests()) {
    return res.status(503).send('Unhealthy');
  }
  res.status(200).send('Healthy');
});

app.get('/ready', (req, res) => {
  // Can accept traffic? (dependencies available)
  if (!db.isConnected() || !cache.isConnected()) {
    return res.status(503).send('Not ready');
  }
  res.status(200).send('Ready');
});
```

---

### 3. ConfigMaps and Secrets

```yaml
# ============================================
# ConfigMap: Non-sensitive configuration
# ============================================
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  # Key-value pairs
  APP_ENV: production
  LOG_LEVEL: info
  FEATURE_FLAGS: '{"newUI": true}'

  # File content
  nginx.conf: |
    server {
      listen 80;
      location / {
        proxy_pass http://backend:8080;
      }
    }

---
# ============================================
# Secret: Sensitive data (base64 encoded)
# ============================================
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  # Automatically base64 encoded
  DATABASE_URL: postgresql://user:pass@db:5432/mydb
  API_KEY: abc123xyz

---
# ============================================
# Using ConfigMap and Secret
# ============================================
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0

        # Option 1: Environment variables from ConfigMap
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets

        # Option 2: Specific environment variables
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_URL

        # Option 3: Mount as files
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
        - name: secret-volume
          mountPath: /etc/secrets
          readOnly: true

      volumes:
      - name: config-volume
        configMap:
          name: app-config
      - name: secret-volume
        secret:
          secretName: app-secrets
```

**External Secrets (Recommended for Production):**

```yaml
# Use External Secrets Operator to sync from vault
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: app-secrets  # Creates K8s Secret
  data:
  - secretKey: DATABASE_URL
    remoteRef:
      key: prod/myapp/database-url
  - secretKey: API_KEY
    remoteRef:
      key: prod/myapp/api-key
```

---

### 4. Security Best Practices

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      # Service account with minimal permissions
      serviceAccountName: myapp-sa
      automountServiceAccountToken: false  # Don't auto-mount if not needed

      # Security context (pod level)
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: app
        image: myapp:1.0

        # Security context (container level)
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL  # Drop all capabilities
            add:
            - NET_BIND_SERVICE  # Only add specific capabilities needed

        # Read-only root filesystem requires writable volumes for temp files
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/.cache

      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
```

#### Network Policies (Zero Trust)

```yaml
# Deny all ingress traffic by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress

---
# Allow specific traffic to backend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-ingress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  # Allow from frontend pods
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080

  # Allow from ingress controller
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
```

#### Pod Security Standards

```yaml
# Enforce security standards at namespace level
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    # Enforce restricted security standard
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

---

### 5. Deployment Strategies

#### Rolling Update (Default)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1  # Max pods down: 10 - 1 = 9 available
      maxSurge: 2        # Max total pods: 10 + 2 = 12

  template:
    spec:
      containers:
      - name: app
        image: myapp:2.0

# Rollout process:
# 1. Create 2 new pods (v2.0) - total: 12 pods
# 2. Wait for new pods to be ready
# 3. Terminate 1 old pod (v1.0) - total: 11 pods
# 4. Repeat until all pods are v2.0
```

**Commands:**

```bash
# Deploy new version
kubectl set image deployment/myapp app=myapp:2.0

# Monitor rollout
kubectl rollout status deployment/myapp

# Pause rollout (for manual verification)
kubectl rollout pause deployment/myapp

# Resume rollout
kubectl rollout resume deployment/myapp

# Rollback to previous version
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=3

# View rollout history
kubectl rollout history deployment/myapp
```

#### Recreate Strategy

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  strategy:
    type: Recreate  # All pods stopped before new ones start

# Use ONLY for:
# - Development environments
# - Applications that can't run multiple versions simultaneously
# - Database schema changes requiring downtime
```

---

### 6. StatefulSets (for Stateful Applications)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres-headless
  replicas: 3
  selector:
    matchLabels:
      app: postgres

  # Volume claim templates (creates PVC for each pod)
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi

  template:
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data

# Pods created in order: postgres-0, postgres-1, postgres-2
# Stable network IDs: postgres-0.postgres-headless
# Persistent storage: Each pod has own PVC
```

---

### 7. Horizontal Pod Autoscaling (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 20
  metrics:
  # Scale based on CPU
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Target 70% CPU

  # Scale based on memory
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80

  # Scale based on custom metrics (requests per second)
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"

  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
      - type: Percent
        value: 50  # Scale down max 50% at a time
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100  # Double pods if needed
        periodSeconds: 15
```

---

### 8. Observability

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    metadata:
      annotations:
        # Prometheus scraping
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: app
        image: myapp:1.0

        # Expose metrics port
        ports:
        - name: metrics
          containerPort: 9090

        # Structured logging
        env:
        - name: LOG_FORMAT
          value: json
        - name: LOG_LEVEL
          value: info
```

**Application Metrics (Prometheus):**

```typescript
// Express.js with prom-client
import promClient from 'prom-client';

// Default metrics (CPU, memory, etc.)
promClient.collectDefaultMetrics();

// Custom metrics
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route', 'status_code']
});

app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    httpRequestDuration.labels(req.method, req.route?.path, res.statusCode)
      .observe((Date.now() - start) / 1000);
  });
  next();
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});
```

---

## Advanced Patterns

### Init Containers

```yaml
# Run initialization tasks before main container
spec:
  initContainers:
  # Wait for database to be ready
  - name: wait-for-db
    image: busybox
    command:
    - sh
    - -c
    - |
      until nc -z postgres 5432; do
        echo "Waiting for postgres..."
        sleep 2
      done

  # Run database migrations
  - name: migrate
    image: myapp:1.0
    command: ["npm", "run", "migrate"]
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: DATABASE_URL

  # Main application container starts AFTER init containers succeed
  containers:
  - name: app
    image: myapp:1.0
```

### Sidecar Pattern

```yaml
# Logging sidecar example
spec:
  containers:
  # Main application
  - name: app
    image: myapp:1.0
    volumeMounts:
    - name: logs
      mountPath: /var/log/app

  # Sidecar: ships logs to external system
  - name: log-shipper
    image: fluent/fluent-bit:2.0
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
      readOnly: true
    - name: fluent-config
      mountPath: /fluent-bit/etc/

  volumes:
  - name: logs
    emptyDir: {}
  - name: fluent-config
    configMap:
      name: fluent-bit-config
```

---

## Troubleshooting

### Pod Stuck in Pending

```bash
# Check events
kubectl describe pod myapp-xyz

# Common causes:
# - Insufficient resources (CPU/memory)
# - Node selector doesn't match any nodes
# - PersistentVolumeClaim not bound
# - Image pull secrets missing
```

### CrashLoopBackOff

```bash
# View logs
kubectl logs myapp-xyz
kubectl logs myapp-xyz --previous  # Previous container instance

# Common causes:
# - Application error on startup
# - Failed health checks
# - Missing dependencies
# - Incorrect command/args
```

### ImagePullBackOff

```bash
# Check image details
kubectl describe pod myapp-xyz

# Common causes:
# - Image doesn't exist
# - Typo in image name/tag
# - Private registry without imagePullSecrets
# - Rate limiting (Docker Hub)
```

### High Memory Usage

```bash
# Check current usage
kubectl top pod myapp-xyz

# Check if hitting limits
kubectl describe pod myapp-xyz | grep -A 5 Limits

# Solutions:
# - Increase memory limits
# - Fix memory leaks in application
# - Use Vertical Pod Autoscaler
```

---

## Kubernetes Cost Optimization

1. **Right-size resources** (use VPA/Goldilocks)
2. **Use Spot/Preemptible instances** for non-critical workloads
3. **Enable cluster autoscaler** to scale nodes
4. **Set resource quotas** per namespace
5. **Monitor unused resources** (Kubecost)
6. **Use PodDisruptionBudgets** for safe node draining
7. **Implement pod priority** for critical workloads

```yaml
# Resource quotas per namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: development
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    persistentvolumeclaims: "10"
```
