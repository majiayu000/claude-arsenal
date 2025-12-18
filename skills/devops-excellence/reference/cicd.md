# CI/CD Pipeline Patterns

## GitHub Actions vs GitLab CI

### When to Choose Each

**GitHub Actions:**
- Already using GitHub for code hosting
- Need extensive marketplace of pre-built actions
- Simpler learning curve for beginners
- Event-driven workflows (issue comments, releases)
- Free for public repositories

**GitLab CI:**
- Need unified DevOps platform (issues, CI, security, etc.)
- Complex enterprise pipelines with dependencies
- Built-in security scanning and compliance
- Self-hosted GitLab instance
- Advanced features (parent-child pipelines, includes)

### Market Trends (2025)

- **80%+ adoption** of CI/CD tools is GitOps-adjacent (Jenkins, GitHub Actions, GitLab CI)
- **Legacy migrations** from Azure DevOps/Jenkins to GitHub Actions/GitLab CI ongoing
- **"It lives where code lives"** is primary selection criteria
- **AI integration** in 76% of teams for predictive failures and auto-fixes

---

## GitHub Actions Patterns

### Matrix Builds

```yaml
name: Multi-Platform Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
        exclude:
          # Skip old Node on Windows
          - os: windows-latest
            node: 18
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
```

### Conditional Execution

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./deploy.sh

  backend:
    # Only run if backend files changed
    if: contains(github.event.head_commit.modified, 'backend/')
    runs-on: ubuntu-latest
    steps:
      - name: Test backend
        run: npm run test:backend

  # Run on schedule (nightly builds)
  nightly:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
```

### Dependency Caching

```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      ~/.cache/pip
      ~/.m2/repository
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/requirements.txt', '**/pom.xml') }}
    restore-keys: |
      ${{ runner.os }}-deps-

- name: Install dependencies
  run: npm ci  # Uses cache if available
```

### Secrets Management

```yaml
# Never hardcode secrets!
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}

# Use OIDC for cloud credentials (recommended)
- name: Configure AWS Credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
    aws-region: us-east-1
    # No static keys - temporary credentials via OIDC!

# Environment-specific secrets
- name: Deploy to staging
  environment: staging  # Requires staging-specific secrets
  run: ./deploy.sh
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci && npm test

# .github/workflows/main.yml
name: Main Pipeline
on: [push]
jobs:
  test-node-18:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '18'
  test-node-20:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20'
```

---

## GitLab CI Patterns

### Pipeline Structure

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - security
  - deploy

# Global variables
variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

# Build job
build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main
    - merge_requests

# Parallel testing
unit-tests:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm run test:unit
  coverage: '/Coverage: \d+\.\d+/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

integration-tests:
  stage: test
  image: node:20
  services:
    - postgres:15
    - redis:7
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
  script:
    - npm run test:integration

# Security scanning (built-in)
sast:
  stage: security
  # Uses GitLab's built-in SAST analyzer
  include:
    - template: Security/SAST.gitlab-ci.yml

container_scanning:
  stage: security
  include:
    - template: Security/Container-Scanning.gitlab-ci.yml

# Environment-specific deployment
deploy:staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - kubectl set image deployment/myapp myapp=$DOCKER_IMAGE
  only:
    - develop

deploy:production:
  stage: deploy
  environment:
    name: production
    url: https://example.com
  when: manual  # Requires approval
  script:
    - kubectl set image deployment/myapp myapp=$DOCKER_IMAGE
  only:
    - main
```

### Parent-Child Pipelines

```yaml
# Parent pipeline
trigger-child:
  trigger:
    include: .gitlab/pipelines/child-pipeline.yml
    strategy: depend  # Wait for child to complete

# Dynamic child pipelines
generate-config:
  stage: build
  script:
    - ./generate-pipeline.sh > generated-pipeline.yml
  artifacts:
    paths:
      - generated-pipeline.yml

trigger-dynamic:
  stage: deploy
  trigger:
    include:
      - artifact: generated-pipeline.yml
        job: generate-config
```

### Advanced Caching

```yaml
# Cache between pipeline runs
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
  policy: pull-push  # Default

# Per-branch caching
cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - node_modules/

# Read-only cache for jobs that don't modify
test:
  cache:
    key: "$CI_COMMIT_REF_SLUG"
    paths:
      - node_modules/
    policy: pull  # Don't update cache
```

---

## Pipeline Optimization Strategies

### 1. Keep Builds Fast (10-Minute Rule)

**Every minute saved multiplies across all developers and commits.**

```yaml
# Before: 25-minute build
- install dependencies (8 min)
- run all tests (12 min)
- build docker image (5 min)

# After: 9-minute build
- install dependencies (2 min - cached)
- run tests in parallel (4 min - 3 parallel jobs)
- build docker image (3 min - multi-stage cache)
```

**Tactics:**
- Cache dependencies aggressively
- Run tests in parallel (split by test suite)
- Use incremental builds
- Skip unchanged modules (monorepo)
- Optimize Docker layer caching

### 2. Fail Fast

```yaml
# Run fast checks first
stages:
  - validate     # Linting, formatting (30s)
  - test-unit    # Unit tests (2 min)
  - test-integration  # Integration (5 min)
  - build        # Build artifacts (3 min)
  - deploy       # Deploy (2 min)

# Don't wait for slow jobs if fast ones fail
```

### 3. Conditional Job Execution

```yaml
# Skip jobs when not needed
jobs:
  frontend-tests:
    rules:
      - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
        changes:
          - frontend/**/*
          - package.json
    script: npm run test:frontend

  # Always run security scans
  security-scan:
    rules:
      - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      - if: '$CI_COMMIT_BRANCH == "main"'
```

### 4. Parallel Matrix Execution

```yaml
# GitHub Actions
test:
  strategy:
    matrix:
      shard: [1, 2, 3, 4]  # Split tests into 4 shards
  steps:
    - run: npm test -- --shard=${{ matrix.shard }}/4

# GitLab CI
test:
  parallel: 4
  script:
    - npm test -- --shard=$CI_NODE_INDEX/$CI_NODE_TOTAL
```

---

## Security Best Practices

### 1. Short-Lived Credentials

```yaml
# BAD: Static credentials
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_KEY }}

# GOOD: OIDC with temporary credentials
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/GitHubActions
    aws-region: us-east-1
    # Credentials expire in 1 hour
```

### 2. Protected Environments

```yaml
# GitHub Actions
environment:
  name: production
  # Requires:
  # - Manual approval from designated reviewers
  # - Can only run from 'main' branch
  # - Wait timer before deployment

# GitLab CI
deploy:production:
  environment:
    name: production
    deployment_tier: production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual  # Requires approval
  only:
    variables:
      - $CI_COMMIT_REF_PROTECTED == "true"
```

### 3. Masked Variables

```yaml
# GitLab: Mask secrets in logs
variables:
  DATABASE_PASSWORD:
    value: "supersecret"
    masked: true

# GitHub: Secrets are automatically masked
# Output: "***" instead of actual value
```

### 4. Dependency Scanning

```yaml
# Snyk integration
- name: Run Snyk to check for vulnerabilities
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: --severity-threshold=high --fail-on=upgradable

# Dependabot (GitHub native)
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule:
      interval: weekly
    open-pull-requests-limit: 10
```

---

## Culture and Process

### Shift from Blame to Learning

**Traditional (Blame Culture):**
- "Who broke production?"
- Individual accountability for failures
- Fear of deploying

**Modern (Learning Culture):**
- "What caused this failure?"
- Blameless postmortems
- Failure as learning opportunity
- Psychological safety to experiment

### Metrics That Matter

**Track these, not lines of code:**
- Deployment frequency
- Lead time for changes
- Mean time to recovery
- Change failure rate

**2025 Elite Performers:**
- Deploy multiple times per day
- < 1 hour from commit to production
- < 1 hour to recover from incidents
- 0-15% change failure rate

---

## Advanced Patterns

### Dynamic Pipeline Generation

```python
# generate-pipeline.py
import yaml

services = ['api', 'worker', 'frontend']
pipeline = {'stages': ['test', 'build', 'deploy']}

for service in services:
    pipeline[f'test-{service}'] = {
        'stage': 'test',
        'script': [f'npm run test --workspace={service}'],
        'only': {'changes': [f'{service}/**/*']}
    }

with open('.gitlab-ci.yml', 'w') as f:
    yaml.dump(pipeline, f)
```

### Pipeline as Code (Dagger)

```go
// Portable pipelines in code (not YAML)
package main

import (
    "dagger.io/dagger"
)

func Pipeline(ctx context.Context) error {
    client, _ := dagger.Connect(ctx)
    defer client.Close()

    // Build container
    container := client.Container().
        From("node:20").
        WithDirectory("/src", client.Host().Directory(".")).
        WithWorkdir("/src").
        WithExec([]string{"npm", "ci"}).
        WithExec([]string{"npm", "test"}).
        WithExec([]string{"npm", "run", "build"})

    // Export build artifacts
    _, err := container.Directory("/src/dist").Export(ctx, "./dist")
    return err
}
```

### GitOps Integration

```yaml
# Pipeline updates GitOps repo
deploy:
  stage: deploy
  script:
    # Clone GitOps repo
    - git clone https://github.com/myorg/k8s-manifests.git
    - cd k8s-manifests/apps/myapp/overlays/prod

    # Update image tag using kustomize
    - kustomize edit set image myapp=$DOCKER_IMAGE

    # Commit and push
    - git config user.name "CI Bot"
    - git config user.email "ci@example.com"
    - git add .
    - git commit -m "Update myapp to $DOCKER_IMAGE"
    - git push

    # ArgoCD auto-syncs cluster to new state
```

---

## Monitoring and Observability

### Pipeline Metrics

```yaml
# Send metrics to observability platform
- name: Report metrics
  if: always()  # Run even if previous steps fail
  run: |
    curl -X POST https://metrics.example.com/api/v1/metrics \
      -H "Content-Type: application/json" \
      -d '{
        "pipeline_id": "${{ github.run_id }}",
        "status": "${{ job.status }}",
        "duration_seconds": ${{ github.event.workflow_run.duration }},
        "branch": "${{ github.ref }}",
        "commit": "${{ github.sha }}",
        "repository": "${{ github.repository }}"
      }'
```

### Failure Notifications

```yaml
# Slack notification on failure
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Pipeline failed for ${{ github.repository }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Pipeline Failed*\n*Repo:* ${{ github.repository }}\n*Branch:* ${{ github.ref }}\n*Commit:* ${{ github.sha }}"
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": "View Logs",
                "url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
              }
            ]
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## Troubleshooting Common Issues

### Flaky Tests

```yaml
# Retry flaky tests automatically
- name: Run tests with retry
  uses: nick-invision/retry@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    retry_on: error
    command: npm test

# Or mark as flaky and track
- name: Run tests
  run: npm test || echo "FLAKY_TEST_FAILED=true" >> $GITHUB_ENV
  continue-on-error: true
```

### Out-of-Memory Errors

```yaml
# Increase Node memory limit
env:
  NODE_OPTIONS: --max-old-space-size=4096

# Use larger runner
runs-on: ubuntu-latest-8-cores  # GitHub hosted (paid)
# or
runs-on: self-hosted-large      # Self-hosted runner
```

### Slow Docker Builds

```yaml
# Use BuildKit with caching
- name: Build Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: myapp:${{ github.sha }}
    cache-from: type=registry,ref=myapp:buildcache
    cache-to: type=registry,ref=myapp:buildcache,mode=max
```

---

## Best Practices Summary

1. **Security First**
   - Use OIDC for cloud credentials
   - Mask all secrets
   - Scan dependencies and containers
   - Protect production branches

2. **Speed Matters**
   - Target < 10 minute builds
   - Cache aggressively
   - Parallelize jobs
   - Fail fast with early validation

3. **Reliability**
   - Retry flaky tests
   - Monitor pipeline metrics
   - Set up failure notifications
   - Document common issues

4. **Maintainability**
   - Keep pipeline configs DRY
   - Use reusable workflows
   - Version pipeline code
   - Review pipeline changes like code

5. **Culture**
   - Blameless postmortems
   - Track DORA metrics
   - Continuous improvement
   - Psychological safety to experiment
