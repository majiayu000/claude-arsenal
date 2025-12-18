# Structured Logging Best Practices

## Logging Principles

### 2025 Standards

- **Structured Format** — JSON for machine parsing
- **Consistent Schema** — Same fields across all services
- **Correlation IDs** — Link logs to traces
- **Appropriate Levels** — Don't log everything at INFO
- **Low Cardinality Labels** — For Loki indexing
- **Sensitive Data** — Never log PII, secrets, tokens
- **Retention Policy** — Define and enforce log lifecycle

## Structured Logging Libraries

### Node.js (Pino)

```typescript
import pino from 'pino';
import { trace } from '@opentelemetry/api';

// Configure logger
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,

  // Inject trace context
  mixin() {
    const span = trace.getActiveSpan();
    if (!span) return {};

    const { traceId, spanId } = span.spanContext();
    return {
      trace_id: traceId,
      span_id: spanId,
    };
  },

  // Redact sensitive fields
  redact: {
    paths: [
      'password',
      'token',
      'api_key',
      'secret',
      'authorization',
      'credit_card',
      '*.password',
      '*.token',
    ],
    censor: '[REDACTED]',
  },
});

// Child logger with context
const requestLogger = logger.child({
  request_id: 'req_abc123',
  user_id: 'user_456',
});

// Log examples
logger.info('Application started');

logger.info(
  {
    user_id: '123',
    action: 'login',
    ip_address: '192.168.1.1',
  },
  'User logged in'
);

logger.error(
  {
    error: {
      message: err.message,
      stack: err.stack,
      code: err.code,
    },
    context: { order_id: 'ord_789' },
  },
  'Payment processing failed'
);

// Output:
// {"level":"info","time":"2025-01-15T10:30:00.000Z","msg":"Application started"}
// {"level":"info","time":"2025-01-15T10:30:01.000Z","trace_id":"abc123","span_id":"def456","user_id":"123","action":"login","ip_address":"192.168.1.1","msg":"User logged in"}
```

### Python (structlog)

```python
import structlog
from opentelemetry import trace

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        # Add trace context
        lambda _, __, event_dict: add_trace_context(event_dict),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

def add_trace_context(event_dict):
    span = trace.get_current_span()
    if span.is_recording():
        ctx = span.get_span_context()
        event_dict['trace_id'] = format(ctx.trace_id, '032x')
        event_dict['span_id'] = format(ctx.span_id, '016x')
    return event_dict

logger = structlog.get_logger()

# Log examples
logger.info("application_started")

logger.info(
    "user_logged_in",
    user_id="123",
    action="login",
    ip_address="192.168.1.1"
)

try:
    process_payment()
except Exception as e:
    logger.error(
        "payment_processing_failed",
        exc_info=True,
        order_id="ord_789",
        amount=99.99
    )
```

### Go (zap)

```go
package main

import (
    "go.uber.org/zap"
    "go.uber.org/zap/zapcore"
    "go.opentelemetry.io/otel/trace"
)

func newLogger() *zap.Logger {
    config := zap.Config{
        Level:       zap.NewAtomicLevelAt(zap.InfoLevel),
        Development: false,
        Encoding:    "json",
        EncoderConfig: zapcore.EncoderConfig{
            TimeKey:        "time",
            LevelKey:       "level",
            NameKey:        "logger",
            CallerKey:      "caller",
            MessageKey:     "msg",
            StacktraceKey:  "stacktrace",
            LineEnding:     zapcore.DefaultLineEnding,
            EncodeLevel:    zapcore.LowercaseLevelEncoder,
            EncodeTime:     zapcore.ISO8601TimeEncoder,
            EncodeDuration: zapcore.SecondsDurationEncoder,
            EncodeCaller:   zapcore.ShortCallerEncoder,
        },
        OutputPaths:      []string{"stdout"},
        ErrorOutputPaths: []string{"stderr"},
    }

    logger, _ := config.Build()
    return logger
}

func logWithTrace(logger *zap.Logger, span trace.Span) *zap.Logger {
    ctx := span.SpanContext()
    return logger.With(
        zap.String("trace_id", ctx.TraceID().String()),
        zap.String("span_id", ctx.SpanID().String()),
    )
}

func main() {
    logger := newLogger()
    defer logger.Sync()

    logger.Info("application started")

    logger.Info("user logged in",
        zap.String("user_id", "123"),
        zap.String("action", "login"),
        zap.String("ip_address", "192.168.1.1"),
    )

    logger.Error("payment processing failed",
        zap.Error(err),
        zap.String("order_id", "ord_789"),
        zap.Float64("amount", 99.99),
    )
}
```

## Log Levels

### Standard Levels and Usage

```yaml
TRACE (10):
  Usage: Extremely detailed debugging
  Example: "Function entry/exit", "Variable values at each step"
  Production: Disabled
  Development: Use sparingly

DEBUG (20):
  Usage: Diagnostic information
  Example: "Query executed", "Cache miss", "Retry attempt"
  Production: Disabled or very limited
  Development: Common

INFO (30):
  Usage: Normal operational events
  Example: "Server started", "Request completed", "Job processed"
  Production: Default level
  Development: Common

WARN (40):
  Usage: Potentially harmful situations
  Example: "Deprecated API used", "Retry threshold approaching", "Slow query"
  Production: Always logged
  Development: Always logged

ERROR (50):
  Usage: Error events that allow continued execution
  Example: "API call failed", "Database timeout", "Validation error"
  Production: Always logged, may trigger alerts
  Development: Always logged

FATAL (60):
  Usage: Severe errors causing process termination
  Example: "Cannot connect to database", "Out of memory", "Critical failure"
  Production: Always logged, triggers critical alerts
  Development: Always logged
```

### Level Selection Guidelines

```typescript
// WRONG: Everything at INFO
logger.info('Function started');              // Too verbose
logger.info('Checking cache');                // Too verbose
logger.info({ result }, 'Cache hit');         // Too verbose
logger.info('Processing payment');            // OK, but could be DEBUG
logger.info('Payment successful');            // OK

// RIGHT: Appropriate levels
logger.debug('Entering processPayment function');
logger.debug({ cacheKey }, 'Checking cache');
logger.debug({ result }, 'Cache hit');
logger.info({ order_id, amount }, 'Payment processed');  // Business event
logger.warn({ retries: 2 }, 'Payment service slow');
logger.error({ error }, 'Payment failed');

// Business events → INFO
// System health → WARN
// Failures → ERROR
// Diagnostics → DEBUG
```

## Grafana Loki Setup

### Architecture

```
Applications → Promtail → Loki → Grafana
                ↓
            (Optional)
         OpenTelemetry Collector
```

### Loki Configuration

```yaml
# loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

# Retention configuration
limits_config:
  retention_period: 744h  # 31 days

  # Prevent high cardinality issues
  max_streams_per_user: 10000
  max_global_streams_per_user: 100000

  # Query limits
  max_query_length: 721h  # 30 days
  max_query_parallelism: 32

  # Ingestion limits
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20
  per_stream_rate_limit: 3MB

# Compactor for retention enforcement
compactor:
  working_directory: /loki/compactor
  shared_store: filesystem
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150

# Query frontend for caching
query_range:
  results_cache:
    cache:
      embedded_cache:
        enabled: true
        max_size_mb: 100
```

### Promtail Configuration

```yaml
# promtail-config.yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # Docker container logs
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      # Container name as label
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
      # Container labels as Loki labels
      - source_labels: ['__meta_docker_container_label_com_docker_compose_service']
        target_label: 'service'
    pipeline_stages:
      # Parse JSON logs
      - json:
          expressions:
            level: level
            msg: msg
            trace_id: trace_id
            user_id: user_id
      # Extract level as label (LOW cardinality)
      - labels:
          level:
      # Only log trace_id, not as label (HIGH cardinality)
      - output:
          source: msg

  # Kubernetes pods
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Only pods with logging=enabled annotation
      - source_labels:
          - __meta_kubernetes_pod_annotation_logging_enabled
        action: keep
        regex: true
      # Add namespace
      - source_labels:
          - __meta_kubernetes_namespace
        target_label: namespace
      # Add pod name
      - source_labels:
          - __meta_kubernetes_pod_name
        target_label: pod
      # Add app label
      - source_labels:
          - __meta_kubernetes_pod_label_app
        target_label: app
      # Path to pod logs
      - source_labels:
          - __meta_kubernetes_pod_uid
          - __meta_kubernetes_pod_container_name
        target_label: __path__
        separator: /
        replacement: /var/log/pods/*$1/*.log
    pipeline_stages:
      # Parse JSON
      - json:
          expressions:
            level: level
            trace_id: trace_id
            msg: msg
      # Extract log level
      - labels:
          level:
      # Drop noisy logs
      - match:
          selector: '{level="debug"}'
          action: drop

  # System logs
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*.log
```

### LogQL Queries

```promql
# Basic text search
{namespace="production", app="api"} |= "error"

# JSON parsing and filtering
{app="api"}
  | json
  | level="error"
  | user_id="123"

# Regex filtering
{app="api"} |~ "error|failed|timeout"

# Line format (extract specific fields)
{app="api"}
  | json
  | line_format "{{.time}} {{.level}} {{.msg}}"

# Log rate (logs per second)
rate({app="api"}[5m])

# Count logs by level
sum by (level) (
  count_over_time({namespace="production"}[1h])
)

# Error percentage
sum(rate({app="api", level="error"}[5m]))
/
sum(rate({app="api"}[5m]))

# Top 10 error messages
topk(10,
  sum by (msg) (
    count_over_time({level="error"} | json [1h])
  )
)

# Logs with specific trace ID (correlation)
{namespace="production"}
  | json
  | trace_id="abc123def456"

# Slow requests (>1s latency)
{app="api"}
  | json
  | duration > 1000
  | line_format "{{.method}} {{.path}} took {{.duration}}ms"

# Pattern matching
{app="api"}
  | pattern `<_> level=<level> msg="<msg>"`
  | level="error"
```

## ELK Stack (Alternative to Loki)

### When to Use ELK vs Loki

```yaml
Use Loki when:
  - Cost-sensitive (10x cheaper than ELK)
  - Already using Prometheus/Grafana
  - Simple log queries (grep-like)
  - Cloud-native/Kubernetes environment

Use ELK when:
  - Advanced full-text search needed
  - Complex log analytics and aggregations
  - Security/compliance (detailed audit logs)
  - Multiple data sources beyond logs
```

### Elasticsearch Configuration

```yaml
# elasticsearch.yml
cluster.name: logging-cluster
node.name: node-1
network.host: 0.0.0.0

# Index lifecycle management
xpack.ilm.enabled: true

# Security
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
```

### Logstash Pipeline

```ruby
# logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  # Parse JSON logs
  json {
    source => "message"
  }

  # Add timestamp
  date {
    match => ["time", "ISO8601"]
    target => "@timestamp"
  }

  # Grok for non-JSON logs
  grok {
    match => {
      "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:msg}"
    }
  }

  # GeoIP enrichment
  geoip {
    source => "ip_address"
  }

  # Remove sensitive fields
  mutate {
    remove_field => ["password", "token", "api_key"]
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
    user => "elastic"
    password => "${ELASTIC_PASSWORD}"
  }
}
```

### Filebeat Configuration

```yaml
# filebeat.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/app/*.log
    json.keys_under_root: true
    json.add_error_key: true
    fields:
      app: api
      environment: production

  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'

processors:
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~

output.logstash:
  hosts: ["logstash:5044"]

# Or directly to Elasticsearch
# output.elasticsearch:
#   hosts: ["http://elasticsearch:9200"]
#   index: "logs-%{+yyyy.MM.dd}"
```

## Best Practices

### Cardinality Management

```yaml
# LOW cardinality labels (good for Loki)
Good labels:
  - namespace (5-20 values)
  - app/service (10-50 values)
  - level (5 values: trace, debug, info, warn, error)
  - environment (3-5 values: dev, staging, prod)

# HIGH cardinality data (keep in log body)
Bad labels:
  - user_id (millions of values)
  - request_id (unique per request)
  - trace_id (unique per trace)
  - session_id (millions of values)
  - ip_address (thousands of values)

# Rule: Keep total label combinations < 10,000
# Example: 5 namespaces × 20 apps × 5 levels = 500 combinations ✓
```

### Sensitive Data Handling

```typescript
// Redact sensitive data
const logger = pino({
  redact: {
    paths: [
      'req.headers.authorization',
      'req.headers.cookie',
      'password',
      'creditCard',
      'ssn',
      '*.password',
      '*.token',
      '*.secret',
    ],
    censor: '[REDACTED]',
  },
});

// Custom serializers
const logger = pino({
  serializers: {
    user: (user) => ({
      id: user.id,
      email: user.email.replace(/(.{2}).*(@.*)/, '$1***$2'), // ma***@example.com
      // Omit sensitive fields
    }),
  },
});
```

### Log Rotation

```bash
# logrotate config
/var/log/app/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 app app
    postrotate
        # Signal app to reopen log file
        killall -SIGUSR1 app
    endscript
}
```

### Sampling for High-Volume Logs

```typescript
// Sample debug logs (keep 10%)
const shouldLog = (level: string) => {
  if (level !== 'debug') return true;
  return Math.random() < 0.1; // 10% sample rate
};

if (shouldLog('debug')) {
  logger.debug({ details }, 'Debug information');
}

// Or use structured sampling
const logger = pino({
  level: 'debug',
  hooks: {
    logMethod(inputArgs, method, level) {
      // Sample debug logs
      if (level === 20 && Math.random() > 0.1) {
        return; // Skip this log
      }
      return method.apply(this, inputArgs);
    },
  },
});
```

This logging guide provides production-ready structured logging configurations for comprehensive log management with Loki and ELK.
