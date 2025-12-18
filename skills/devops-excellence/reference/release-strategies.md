# Release Strategies and Deployment Patterns

## Overview

**Key Statistics (2025):**
- 80% of Kubernetes outages stem from deployment errors
- Elite performers deploy multiple times per day with 0-15% failure rate
- 65% of organizations with real-time monitoring report faster incident resolution

## Strategy Comparison Matrix

| Strategy | Downtime | Cost | Rollback Speed | Complexity | Testing Isolation | Best For |
|----------|----------|------|----------------|------------|-------------------|----------|
| **Recreate** | High (minutes) | Very Low | N/A | Very Low | N/A | Dev/test only |
| **Rolling Update** | Minimal | Low | Medium | Low | No | Regular updates |
| **Blue-Green** | Zero | High (2x infra) | Instant | Medium | Yes | Critical systems |
| **Canary** | Zero | Medium | Fast | High | Partial | High-risk changes |
| **A/B Testing** | Zero | Medium | Fast | High | Yes | Feature experiments |

---

## Rolling Deployment

### How It Works

Gradually replace old version pods with new version, maintaining minimum availability.

```
Initial:  [v1] [v1] [v1] [v1] [v1] [v1] [v1] [v1] [v1] [v1]  (10 pods)

Step 1:   [v1] [v1] [v1] [v1] [v1] [v1] [v1] [v1] [v2] [v2]  (create 2 v2)
Step 2:   [v1] [v1] [v1] [v1] [v1] [v1] [v1] [v2] [v2]       (remove 1 v1)
Step 3:   [v1] [v1] [v1] [v1] [v1] [v1] [v2] [v2] [v2]       (repeat...)
...
Final:    [v2] [v2] [v2] [v2] [v2] [v2] [v2] [v2] [v2] [v2]  (all v2)
```

### Kubernetes Implementation

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 10

  # Rolling update strategy
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1  # Max 1 pod down at a time (90% availability)
      maxSurge: 2        # Max 2 extra pods during rollout

  selector:
    matchLabels:
      app: myapp

  template:
    metadata:
      labels:
        app: myapp
        version: v2.0
    spec:
      containers:
      - name: app
        image: myapp:v2.0
        ports:
        - containerPort: 8080

        # Health checks ensure new pods are healthy before old ones removed
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Deployment Process

```bash
# 1. Deploy new version
kubectl apply -f deployment.yaml
# or
kubectl set image deployment/myapp app=myapp:v2.0

# 2. Monitor rollout
kubectl rollout status deployment/myapp
# Output: Waiting for deployment "myapp" rollout to finish: 3 of 10 updated replicas are available...

# 3. Watch pods being replaced
kubectl get pods -w -l app=myapp

# 4. Pause rollout for manual verification (optional)
kubectl rollout pause deployment/myapp

# Verify new version is working correctly
curl http://myapp-v2-pod-ip:8080/health

# 5. Resume rollout
kubectl rollout resume deployment/myapp

# 6. Rollback if issues detected
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=3
```

### Pros and Cons

**Advantages:**
- No extra infrastructure required
- Built into Kubernetes (no additional tools)
- Gradual rollout reduces blast radius
- Automatic rollback on health check failures
- Works with autoscaling

**Disadvantages:**
- Both versions running simultaneously (compatibility required)
- Slower rollback compared to blue-green
- Can't test full new version in isolation
- Database schema changes tricky (must be backward compatible)

**When to Use:**
- Regular incremental updates
- Cost-conscious environments
- Applications supporting multiple concurrent versions
- Low-to-medium risk changes

---

## Blue-Green Deployment

### How It Works

Maintain two identical production environments. Route all traffic to one (Blue), deploy to the other (Green), then swap.

```
Initial State:
  [Load Balancer] → Blue Environment (v1.0) [LIVE]
                    Green Environment (idle)

Deploy to Green:
  [Load Balancer] → Blue Environment (v1.0) [LIVE]
                    Green Environment (v2.0) [TESTING]

Switch Traffic:
  [Load Balancer] → Green Environment (v2.0) [LIVE]
                    Blue Environment (v1.0) [STANDBY - instant rollback]

After Validation:
  [Load Balancer] → Green Environment (v2.0) [LIVE]
                    Blue Environment (v1.0) → becomes new Green (idle)
```

### Kubernetes Implementation

#### Method 1: Service Selector Switching

```yaml
# ============================================
# Blue Deployment (Current Production)
# ============================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 10
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: app
        image: myapp:v1.0
        ports:
        - containerPort: 8080

---
# ============================================
# Green Deployment (New Version)
# ============================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 10
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: app
        image: myapp:v2.0
        ports:
        - containerPort: 8080

---
# ============================================
# Service (Points to Blue Initially)
# ============================================
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # CHANGE TO 'green' TO SWITCH
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

**Switching Process:**

```bash
# 1. Deploy green environment
kubectl apply -f myapp-green-deployment.yaml

# 2. Wait for green pods to be ready
kubectl wait --for=condition=ready pod -l version=green --timeout=300s

# 3. Test green environment directly (before switching traffic)
kubectl port-forward deployment/myapp-green 8080:8080
curl http://localhost:8080/health

# 4. Switch service to green
kubectl patch service myapp -p '{"spec":{"selector":{"version":"green"}}}'

# 5. Monitor for issues (keep blue running)
# If problems detected:
kubectl patch service myapp -p '{"spec":{"selector":{"version":"blue"}}}'  # Instant rollback!

# 6. After validation, scale down blue
kubectl scale deployment myapp-blue --replicas=0
```

#### Method 2: Ingress/Route Switching

```yaml
# ============================================
# Blue Service
# ============================================
apiVersion: v1
kind: Service
metadata:
  name: myapp-blue
spec:
  selector:
    app: myapp
    version: blue
  ports:
  - port: 80
    targetPort: 8080

---
# ============================================
# Green Service
# ============================================
apiVersion: v1
kind: Service
metadata:
  name: myapp-green
spec:
  selector:
    app: myapp
    version: green
  ports:
  - port: 80
    targetPort: 8080

---
# ============================================
# Ingress (Switch backend)
# ============================================
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-blue  # CHANGE TO myapp-green TO SWITCH
            port:
              number: 80
```

### AWS/Cloud Implementation

**AWS with Application Load Balancer:**

```bash
# 1. Create two target groups (blue and green)
aws elbv2 create-target-group --name myapp-blue-tg ...
aws elbv2 create-target-group --name myapp-green-tg ...

# 2. Deploy to green target group
# (Update Auto Scaling Group or ECS service)

# 3. Switch ALB listener to green target group
aws elbv2 modify-listener \
  --listener-arn arn:aws:elasticloadbalancing:... \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:.../myapp-green-tg

# 4. Instant rollback if needed
aws elbv2 modify-listener ... TargetGroupArn=.../myapp-blue-tg
```

### Database Considerations

```sql
-- Problem: Blue uses schema v1, Green uses schema v2
-- Solution: Make migrations backward compatible

-- GOOD: Additive changes (v2 adds column, v1 ignores it)
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- BAD: Breaking changes
ALTER TABLE users DROP COLUMN email;  -- v1 will fail!

-- Pattern: Multi-phase migration
-- Phase 1: Add new column (both versions work)
ALTER TABLE users ADD COLUMN email_v2 VARCHAR(255);

-- Phase 2: Dual-write in code (write to both email and email_v2)

-- Phase 3: Backfill data
UPDATE users SET email_v2 = email WHERE email_v2 IS NULL;

-- Phase 4: Switch reads to email_v2

-- Phase 5: Drop old column (after both environments use email_v2)
ALTER TABLE users DROP COLUMN email;
```

### Pros and Cons

**Advantages:**
- Zero downtime
- Instant rollback (just switch back)
- Full testing of new environment before cutover
- Clean separation between versions
- Database can be tested in isolation

**Disadvantages:**
- Requires 2x infrastructure (expensive)
- Database migrations complex
- Syncing state between environments tricky
- Session/state management challenges

**When to Use:**
- Critical systems requiring instant rollback
- High-compliance environments
- Major version upgrades
- Budget allows for duplicate infrastructure

---

## Canary Deployment

### How It Works

Gradually shift traffic from old version to new version: 5% → 25% → 50% → 100%.

```
Step 1: Deploy canary (5% traffic)
  95% traffic → v1.0 [9 pods]
   5% traffic → v2.0 [1 pod]  ← Monitor metrics

Step 2: Increase to 25% (if metrics good)
  75% traffic → v1.0 [7 pods]
  25% traffic → v2.0 [3 pods]

Step 3: Increase to 50%
  50% traffic → v1.0 [5 pods]
  50% traffic → v2.0 [5 pods]

Step 4: Promote to 100%
 100% traffic → v2.0 [10 pods]
   0% traffic → v1.0 [removed]
```

### Implementation with Argo Rollouts

```yaml
# Install Argo Rollouts
# kubectl create namespace argo-rollouts
# kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 10

  strategy:
    canary:
      # Canary steps
      steps:
      - setWeight: 10        # Send 10% traffic to canary
      - pause: {duration: 5m}  # Wait 5 minutes

      - setWeight: 25        # Increase to 25%
      - pause: {duration: 10m}

      - setWeight: 50        # Increase to 50%
      - pause: {duration: 10m}

      - setWeight: 75        # Increase to 75%
      - pause: {duration: 5m}

      # If we reach here, promote to 100%

      # Optional: Analysis template (automated promotion/rollback)
      analysis:
        templates:
        - templateName: success-rate
        startingStep: 1  # Run analysis after first step
        args:
        - name: service-name
          value: myapp

      # Traffic routing (choose one)
      trafficRouting:
        # Option 1: Istio
        istio:
          virtualService:
            name: myapp-vsvc
          destinationRule:
            name: myapp-dest
            canarySubsetName: canary
            stableSubsetName: stable

        # Option 2: NGINX Ingress
        nginx:
          stableIngress: myapp
          annotationPrefix: nginx.ingress.kubernetes.io

  selector:
    matchLabels:
      app: myapp

  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:v2.0
        ports:
        - containerPort: 8080

---
# AnalysisTemplate: Automated success rate check
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name

  metrics:
  - name: success-rate
    interval: 1m
    successCondition: result >= 0.95  # 95% success rate required
    failureLimit: 3  # Rollback after 3 failed checks
    provider:
      prometheus:
        address: http://prometheus.monitoring:9090
        query: |
          sum(rate(http_requests_total{
            service="{{args.service-name}}",
            status=~"2.."
          }[1m]))
          /
          sum(rate(http_requests_total{
            service="{{args.service-name}}"
          }[1m]))
```

### Canary Commands

```bash
# Deploy canary
kubectl apply -f rollout.yaml

# Watch rollout progress
kubectl argo rollouts get rollout myapp --watch

# Promote to next step (if paused)
kubectl argo rollouts promote myapp

# Abort and rollback
kubectl argo rollouts abort myapp
kubectl argo rollouts undo myapp

# Set image
kubectl argo rollouts set image myapp app=myapp:v2.1
```

### Manual Canary with Kubernetes

```yaml
# ============================================
# Stable Deployment (90% of pods)
# ============================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
      track: stable
  template:
    metadata:
      labels:
        app: myapp
        track: stable
        version: v1.0
    spec:
      containers:
      - name: app
        image: myapp:v1.0

---
# ============================================
# Canary Deployment (10% of pods)
# ============================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
      track: canary
  template:
    metadata:
      labels:
        app: myapp
        track: canary
        version: v2.0
    spec:
      containers:
      - name: app
        image: myapp:v2.0

---
# ============================================
# Service (routes to both stable and canary)
# ============================================
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp  # Matches both stable and canary
  ports:
  - port: 80
    targetPort: 8080
```

**Gradually increase canary:**

```bash
# 10% canary (1/10 pods)
kubectl scale deployment myapp-canary --replicas=1

# 25% canary (3/12 pods)
kubectl scale deployment myapp-stable --replicas=9
kubectl scale deployment myapp-canary --replicas=3

# 50% canary
kubectl scale deployment myapp-stable --replicas=5
kubectl scale deployment myapp-canary --replicas=5

# Promote (100% new version)
kubectl scale deployment myapp-stable --replicas=10
kubectl patch deployment myapp-stable -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","image":"myapp:v2.0"}]}}}}'
kubectl scale deployment myapp-canary --replicas=0
```

### Metrics-Based Automated Rollback

```yaml
# Flagger (progressive delivery operator)
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp

  service:
    port: 80
    targetPort: 8080

  analysis:
    interval: 1m
    threshold: 5  # Number of checks
    maxWeight: 50
    stepWeight: 10

    # Metrics for automated decision
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99  # Rollback if < 99% success
      interval: 1m

    - name: request-duration
      thresholdRange:
        max: 500  # Rollback if p99 latency > 500ms
      interval: 1m

    # Alert on canary failure
    webhooks:
    - name: slack-alert
      url: https://hooks.slack.com/services/YOUR/WEBHOOK
      type: pre-rollout
```

### Pros and Cons

**Advantages:**
- Lowest risk deployment strategy
- Gradual rollout limits blast radius
- Real production data for validation
- Automated rollback based on metrics
- Cost-effective (no duplicate infrastructure)

**Disadvantages:**
- Complex setup (requires service mesh or ingress controller)
- Longer deployment time
- Need robust monitoring and metrics
- Difficult to test all code paths with limited traffic

**When to Use:**
- High-risk changes (major refactors, new features)
- Customer-facing applications
- When you have strong observability
- Cost-conscious but need safety

---

## A/B Testing

### How It Works

Route traffic based on user attributes (not just percentage). Test different features with different user segments.

```
User Segment A (50%) → Version A (existing feature)
User Segment B (50%) → Version B (new feature)

Measure: conversion rate, engagement, revenue
```

### Implementation

```yaml
# Using Istio VirtualService for A/B testing
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp.example.com
  http:
  - match:
    # Route users with 'premium' cookie to version B
    - headers:
        cookie:
          regex: ".*tier=premium.*"
    route:
    - destination:
        host: myapp
        subset: version-b

  - match:
    # Route mobile users to version A
    - headers:
        user-agent:
          regex: ".*Mobile.*"
    route:
    - destination:
        host: myapp
        subset: version-a

  # Default: 50/50 split
  - route:
    - destination:
        host: myapp
        subset: version-a
      weight: 50
    - destination:
        host: myapp
        subset: version-b
      weight: 50
```

### Feature Flags for A/B Testing

```typescript
// LaunchDarkly example
import { LDClient } from 'launchdarkly-node-server-sdk';

const ldClient = LDClient.init(process.env.LD_SDK_KEY);

app.get('/checkout', async (req, res) => {
  const user = {
    key: req.user.id,
    email: req.user.email,
    custom: {
      tier: req.user.tier,  // 'free' or 'premium'
      country: req.user.country
    }
  };

  // A/B test: new checkout flow
  const showNewCheckout = await ldClient.variation(
    'new-checkout-ui',
    user,
    false  // Default
  );

  if (showNewCheckout) {
    res.render('checkout-v2', { user });
  } else {
    res.render('checkout-v1', { user });
  }

  // Track metrics
  analytics.track('checkout_viewed', {
    userId: user.key,
    variant: showNewCheckout ? 'new' : 'old'
  });
});
```

**LaunchDarkly Configuration:**

```json
{
  "name": "new-checkout-ui",
  "kind": "boolean",
  "targeting": {
    "rules": [
      {
        "variation": 1,
        "clauses": [
          {
            "attribute": "tier",
            "op": "in",
            "values": ["premium"]
          }
        ]
      },
      {
        "variation": 1,
        "clauses": [
          {
            "attribute": "country",
            "op": "in",
            "values": ["US", "CA"]
          }
        ]
      }
    ],
    "fallthrough": {
      "rollout": {
        "variations": [
          {"variation": 0, "weight": 50000},
          {"variation": 1, "weight": 50000}
        ]
      }
    }
  }
}
```

---

## Shadow Deployment (Dark Launch)

### How It Works

Send live traffic to new version WITHOUT exposing results to users. Compare responses/metrics.

```
Production Traffic → Primary (v1.0) → Response to User
                   ↘ Shadow (v2.0)  → Logged (not returned)

Compare: latency, errors, response differences
```

### Implementation with Istio

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - route:
    - destination:
        host: myapp
        subset: v1  # Primary version
      weight: 100

    mirror:
      host: myapp
      subset: v2  # Shadow version (receives copy of traffic)
    mirrorPercentage:
      value: 100  # Mirror 100% of traffic
```

**Use Cases:**
- Performance testing with real traffic
- Validating new algorithms/models
- Testing infrastructure changes
- Comparing response times/resource usage

---

## Choosing the Right Strategy

### Decision Tree

```
Is this a critical production system?
├─ YES → Budget for 2x infrastructure?
│        ├─ YES → Blue-Green (instant rollback)
│        └─ NO  → Canary (gradual, metrics-based)
└─ NO  → Risk level?
         ├─ HIGH → Canary with feature flags
         ├─ MEDIUM → Rolling update
         └─ LOW → Rolling update or Recreate (dev/test)

Need to test business hypotheses?
└─ A/B Testing with feature flags

Need to validate performance before launch?
└─ Shadow deployment
```

### By Use Case

| Use Case | Recommended Strategy |
|----------|---------------------|
| Bug fix (low risk) | Rolling update |
| New feature (medium risk) | Canary deployment |
| Major refactor (high risk) | Canary with extensive monitoring |
| Database schema change | Blue-green with backward-compatible migration |
| Performance optimization | Shadow deployment first, then canary |
| Business experiment | A/B testing with feature flags |
| Compliance-critical system | Blue-green (audit trail, instant rollback) |
| Microservice update | Rolling update or canary |
| Frontend redesign | A/B testing (measure user engagement) |

---

## Best Practices

### 1. Always Have a Rollback Plan

```bash
# Document rollback procedure
# Example:
# Rollback for Blue-Green:
kubectl patch service myapp -p '{"spec":{"selector":{"version":"blue"}}}'

# Rollback for Rolling:
kubectl rollout undo deployment/myapp

# Rollback for Canary (Argo Rollouts):
kubectl argo rollouts abort myapp
kubectl argo rollouts undo myapp
```

### 2. Monitor Key Metrics

```yaml
# Essential metrics to track during deployment
- Error rate (4xx, 5xx responses)
- Latency (p50, p95, p99)
- Request rate
- Resource usage (CPU, memory)
- Business metrics (conversion, signups)
```

### 3. Automated Rollback Triggers

```yaml
# Set thresholds for auto-rollback
error_rate_threshold: 5%  # Rollback if > 5% errors
latency_p99_threshold: 1000ms  # Rollback if p99 > 1s
availability_threshold: 99.9%  # Rollback if < 99.9% uptime
```

### 4. Feature Flags for Large Changes

```typescript
// Decouple deployment from release
if (featureFlags.isEnabled('new-payment-flow', user)) {
  return newPaymentFlow(req);
} else {
  return oldPaymentFlow(req);
}

// Deploy with flag OFF → test in production → enable for 5% → ramp to 100%
```

### 5. Database Migration Strategy

```sql
-- Expand-Contract Pattern
-- Phase 1: EXPAND (add new schema, both versions work)
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);

-- Phase 2: Dual-write (application writes to both old and new)

-- Phase 3: Backfill data

-- Phase 4: CONTRACT (remove old schema after all apps migrated)
ALTER TABLE users DROP COLUMN phone;
```

---

## Common Pitfalls

1. **Stateful Apps Without Session Management**
   - Problem: User session on v1, next request hits v2
   - Solution: Sticky sessions or external session store (Redis)

2. **Database Compatibility Issues**
   - Problem: v2 schema breaks v1
   - Solution: Backward-compatible migrations, expand-contract pattern

3. **No Rollback Plan**
   - Problem: Deployment fails, no way to recover quickly
   - Solution: Document and test rollback before deploying

4. **Insufficient Monitoring**
   - Problem: Issues not detected during canary phase
   - Solution: Monitor error rates, latency, business metrics

5. **Too Aggressive Canary Ramp**
   - Problem: Jump from 10% to 100% too quickly
   - Solution: Gradual steps (10% → 25% → 50% → 75% → 100%)

6. **Ignoring Non-Functional Changes**
   - Problem: "Just a config change" causes outage
   - Solution: Treat all changes with same rigor
