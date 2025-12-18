# Multi-Stage Dockerfile with Security Best Practices
# This template demonstrates production-ready Docker image creation
# Final image size: ~100MB (vs 900MB+ without multi-stage)

# ============================================
# Stage 1: Base Dependencies
# ============================================
FROM node:20-alpine AS base

# Install security updates
RUN apk update && apk upgrade --no-cache

# Set working directory
WORKDIR /app

# ============================================
# Stage 2: Dependencies Installation
# ============================================
FROM base AS dependencies

# Copy package files only (better layer caching)
# Changes to source code won't invalidate this layer
COPY package.json package-lock.json ./

# Install ALL dependencies (dev + production)
# Use npm ci for reproducible builds (respects package-lock.json exactly)
RUN npm ci --only=production --ignore-scripts && \
    # Copy production dependencies to temp location
    cp -R node_modules /tmp/node_modules && \
    # Install dev dependencies for build stage
    npm ci --ignore-scripts

# ============================================
# Stage 3: Build Application
# ============================================
FROM dependencies AS builder

WORKDIR /app

# Copy application source
# Placed after dependency installation for better caching
COPY tsconfig.json ./
COPY src ./src
COPY public ./public

# Build application (TypeScript compilation, webpack, etc.)
RUN npm run build

# ============================================
# Stage 4: Production Runtime (Final Image)
# ============================================
FROM node:20-alpine AS runtime

# Install security updates and dumb-init (proper signal handling)
RUN apk update && \
    apk upgrade --no-cache && \
    apk add --no-cache dumb-init && \
    rm -rf /var/cache/apk/*

# Create non-root user with specific UID/GID
# UID/GID 1001 avoids conflicts with host systems
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs

# Set working directory
WORKDIR /app

# Create necessary directories with correct ownership
RUN mkdir -p /app/logs /app/tmp && \
    chown -R nodejs:nodejs /app

# Copy production dependencies from dependencies stage
COPY --from=dependencies --chown=nodejs:nodejs /tmp/node_modules ./node_modules

# Copy built application from builder stage
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/public ./public

# Copy package.json for metadata (version, etc.)
COPY --chown=nodejs:nodejs package.json ./

# Switch to non-root user
USER nodejs

# Expose application port
EXPOSE 3000

# Health check (Docker will mark container unhealthy if this fails)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

# Use dumb-init to handle signals properly (PID 1 problem)
ENTRYPOINT ["dumb-init", "--"]

# Start application
CMD ["node", "dist/server.js"]

# ============================================
# Security Labels (for auditing and scanning)
# ============================================
LABEL maintainer="devops@example.com"
LABEL org.opencontainers.image.source="https://github.com/myorg/myapp"
LABEL org.opencontainers.image.description="MyApp production image"
LABEL org.opencontainers.image.licenses="MIT"

# ============================================
# Alternative: Distroless Image (Maximum Security)
# ============================================
# Uncomment below for distroless variant (no shell, minimal attack surface)
# This is the most secure option but harder to debug

# FROM gcr.io/distroless/nodejs20-debian12 AS distroless-runtime
#
# # Copy production dependencies
# COPY --from=dependencies --chown=nonroot:nonroot /tmp/node_modules /app/node_modules
#
# # Copy built application
# COPY --from=builder --chown=nonroot:nonroot /app/dist /app/dist
# COPY --from=builder --chown=nonroot:nonroot /app/public /app/public
# COPY --chown=nonroot:nonroot package.json /app/
#
# WORKDIR /app
#
# # Distroless uses uid/gid 65532 (nonroot)
# USER nonroot
#
# EXPOSE 3000
#
# # No shell available, must use exec form
# CMD ["dist/server.js"]

# ============================================
# Build Instructions
# ============================================
# Build image:
#   docker build -t myapp:latest .
#
# Build with BuildKit for better caching:
#   DOCKER_BUILDKIT=1 docker build -t myapp:latest .
#
# Build with build secrets (for private npm packages):
#   docker buildx build --secret id=npmrc,src=$HOME/.npmrc -t myapp:latest .
#   Then in Dockerfile:
#   RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
#
# Run container:
#   docker run -d -p 3000:3000 \
#     --name myapp \
#     --read-only \
#     --tmpfs /tmp \
#     --tmpfs /app/logs \
#     --memory="512m" \
#     --cpus="0.5" \
#     --security-opt=no-new-privileges:true \
#     --cap-drop=ALL \
#     -e NODE_ENV=production \
#     -e DATABASE_URL=postgresql://... \
#     myapp:latest
#
# Scan for vulnerabilities:
#   trivy image myapp:latest
#   docker scout cves myapp:latest

# ============================================
# Best Practices Applied
# ============================================
# ✅ Multi-stage build (90% size reduction)
# ✅ Non-root user (UID 1001)
# ✅ Minimal base image (Alpine)
# ✅ Layer caching optimization (package.json before source)
# ✅ Health check configured
# ✅ Security labels
# ✅ Proper signal handling (dumb-init)
# ✅ No secrets in layers
# ✅ Security updates installed
# ✅ Specific file ownership
# ✅ Reproducible builds (npm ci)
# ✅ .dockerignore to exclude unnecessary files

# ============================================
# Common Issues and Solutions
# ============================================
# Issue: "Permission denied" errors
# Solution: Ensure files are owned by nodejs user (use COPY --chown)
#
# Issue: Container doesn't stop gracefully
# Solution: Use dumb-init or tini as PID 1
#
# Issue: Large image size
# Solution: Use multi-stage builds, .dockerignore, alpine base
#
# Issue: "npm WARN" during build
# Solution: Use npm ci instead of npm install, ignore-scripts flag
#
# Issue: Security vulnerabilities in base image
# Solution: Regularly update base image, scan with Trivy
