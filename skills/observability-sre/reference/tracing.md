# Distributed Tracing with OpenTelemetry

## OpenTelemetry Overview

### What is OpenTelemetry?

OpenTelemetry (OTel) is a CNCF standard for collecting telemetry data:
- **Vendor-neutral** — Works with any backend (Jaeger, Tempo, Datadog, etc.)
- **Auto-instrumentation** — Automatic tracing for common frameworks
- **Unified API** — Single SDK for metrics, logs, and traces
- **Production-ready** — 79% of organizations use or are considering OTel

### Core Concepts

```yaml
Trace:
  - Entire journey of a request through the system
  - Unique trace ID shared by all related spans
  - Example: User checkout flow across 5 microservices

Span:
  - Single unit of work within a trace
  - Has start time, end time, attributes, events
  - Parent-child relationships form trace tree
  - Example: Database query within API handler

Context:
  - Metadata that flows across service boundaries
  - Contains trace ID, span ID, trace flags
  - Propagated via HTTP headers, message queues, etc.

Attributes:
  - Key-value pairs attached to spans
  - Describe the operation (http.method, db.statement)
  - Enable filtering and grouping in backends
```

## Auto-Instrumentation

### Node.js

```typescript
// instrumentation.ts - Load BEFORE any other imports
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'payment-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.2.3',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: 'production',
  }),

  traceExporter: new OTLPTraceExporter({
    // Send to OpenTelemetry Collector
    url: 'http://otel-collector:4318/v1/traces',
  }),

  instrumentations: [
    getNodeAutoInstrumentations({
      // Configure auto-instrumentation
      '@opentelemetry/instrumentation-http': {
        enabled: true,
        ignoreIncomingPaths: ['/health', '/metrics'],
      },
      '@opentelemetry/instrumentation-express': { enabled: true },
      '@opentelemetry/instrumentation-pg': { enabled: true }, // PostgreSQL
      '@opentelemetry/instrumentation-redis': { enabled: true },
      '@opentelemetry/instrumentation-mongodb': { enabled: true },
      '@opentelemetry/instrumentation-aws-sdk': { enabled: true },
      '@opentelemetry/instrumentation-fs': { enabled: false }, // Too noisy
    }),
  ],
});

sdk.start();

// Graceful shutdown
process.on('SIGTERM', async () => {
  await sdk.shutdown();
  process.exit(0);
});

// Now import your app
import './app';
```

### Python

```python
# Auto-instrumentation via CLI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Configure resource
resource = Resource(attributes={
    "service.name": "payment-service",
    "service.version": "1.2.3",
    "deployment.environment": "production",
})

# Setup tracer provider
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(
    endpoint="http://otel-collector:4317",
))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Auto-instrument libraries
FlaskInstrumentor().instrument()
RequestsInstrumentor().instrument()
SQLAlchemyInstrumentor().instrument()

# Or use CLI: opentelemetry-instrument python app.py
```

### Go

```go
package main

import (
    "context"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.17.0"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
    "go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc"
)

func initTracer() func() {
    ctx := context.Background()

    // Resource describes the service
    res, _ := resource.New(ctx,
        resource.WithAttributes(
            semconv.ServiceName("payment-service"),
            semconv.ServiceVersion("1.2.3"),
            semconv.DeploymentEnvironment("production"),
        ),
    )

    // OTLP exporter
    exporter, _ := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )

    // Tracer provider
    provider := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(res),
        sdktrace.WithSampler(sdktrace.ParentBased(
            sdktrace.TraceIDRatioBased(0.1), // 10% sampling
        )),
    )
    otel.SetTracerProvider(provider)

    return func() { provider.Shutdown(ctx) }
}

func main() {
    cleanup := initTracer()
    defer cleanup()

    // Auto-instrumented HTTP client
    client := &http.Client{
        Transport: otelhttp.NewTransport(http.DefaultTransport),
    }

    // Auto-instrumented HTTP server
    handler := otelhttp.NewHandler(http.HandlerFunc(handleRequest), "handleRequest")
    http.Handle("/", handler)

    http.ListenAndServe(":8080", nil)
}
```

## Manual Instrumentation

### Creating Custom Spans

```typescript
import { trace, SpanStatusCode, SpanKind } from '@opentelemetry/api';

const tracer = trace.getTracer('payment-service', '1.0.0');

async function processPayment(orderId: string, amount: number) {
  // Start a new span
  return await tracer.startActiveSpan(
    'processPayment',
    {
      kind: SpanKind.INTERNAL,
      attributes: {
        'order.id': orderId,
        'payment.amount': amount,
        'payment.currency': 'USD',
      },
    },
    async (span) => {
      try {
        // Add events (logs within span)
        span.addEvent('validating payment');

        // Validate
        await validatePayment(orderId, amount);

        // Child span for external API call
        const result = await chargeCustomer(orderId, amount);

        // Update span attributes
        span.setAttribute('payment.transaction_id', result.transactionId);
        span.setAttribute('payment.status', 'completed');

        // Mark span as successful
        span.setStatus({ code: SpanStatusCode.OK });

        return result;
      } catch (error) {
        // Record exception
        span.recordException(error);
        span.setStatus({
          code: SpanStatusCode.ERROR,
          message: error.message,
        });

        throw error;
      } finally {
        // Always end the span
        span.end();
      }
    }
  );
}

async function chargeCustomer(orderId: string, amount: number) {
  return await tracer.startActiveSpan(
    'stripe.charge',
    {
      kind: SpanKind.CLIENT,
      attributes: {
        'stripe.method': 'charges.create',
        'http.url': 'https://api.stripe.com/v1/charges',
      },
    },
    async (span) => {
      const result = await stripe.charges.create({
        amount: amount * 100,
        currency: 'usd',
      });

      span.setAttribute('stripe.charge_id', result.id);
      span.end();

      return result;
    }
  );
}
```

### Span Types

```typescript
import { SpanKind } from '@opentelemetry/api';

// INTERNAL: Internal operations (default)
tracer.startActiveSpan('calculateTotal', { kind: SpanKind.INTERNAL });

// SERVER: Incoming request handler
tracer.startActiveSpan('handleRequest', { kind: SpanKind.SERVER });

// CLIENT: Outgoing request
tracer.startActiveSpan('fetchUser', { kind: SpanKind.CLIENT });

// PRODUCER: Message queue producer
tracer.startActiveSpan('publishMessage', { kind: SpanKind.PRODUCER });

// CONSUMER: Message queue consumer
tracer.startActiveSpan('processMessage', { kind: SpanKind.CONSUMER });
```

## Context Propagation

### HTTP Headers (W3C Trace Context)

```typescript
// Automatic propagation with auto-instrumentation
fetch('https://api.example.com/data', {
  // These headers are injected automatically:
  // traceparent: 00-<trace-id>-<span-id>-01
  // tracestate: vendor1=value1,vendor2=value2
});

// Manual propagation
import { propagation, context } from '@opentelemetry/api';

const carrier = {};
propagation.inject(context.active(), carrier);

// carrier now contains:
// {
//   traceparent: "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
// }

fetch('https://api.example.com/data', {
  headers: carrier,
});
```

### Message Queues

```typescript
// Producer: Inject trace context into message
import { propagation, context } from '@opentelemetry/api';

async function publishMessage(queue: string, data: any) {
  return await tracer.startActiveSpan('publishMessage', async (span) => {
    const carrier = {};
    propagation.inject(context.active(), carrier);

    await messageQueue.publish(queue, {
      data,
      headers: carrier, // Propagate trace context
    });

    span.end();
  });
}

// Consumer: Extract trace context from message
async function processMessage(message: Message) {
  const carrier = message.headers;
  const extractedContext = propagation.extract(context.active(), carrier);

  return await context.with(extractedContext, async () => {
    return await tracer.startActiveSpan('processMessage', async (span) => {
      // This span is now part of the original trace
      await handleMessage(message.data);
      span.end();
    });
  });
}
```

## Sampling Strategies

### Head Sampling (at span creation)

```typescript
import { TraceIdRatioBasedSampler, ParentBasedSampler } from '@opentelemetry/sdk-trace-base';

// Sample 10% of traces
const sampler = new TraceIdRatioBasedSampler(0.1);

// Parent-based sampling (respect parent decision)
const parentBasedSampler = new ParentBasedSampler({
  root: new TraceIdRatioBasedSampler(0.1),
});

const provider = new NodeTracerProvider({
  sampler: parentBasedSampler,
});
```

### Tail Sampling (OpenTelemetry Collector)

```yaml
# otel-collector-config.yaml
processors:
  tail_sampling:
    decision_wait: 10s  # Wait to see full trace
    num_traces: 100000
    expected_new_traces_per_sec: 100

    policies:
      # Always sample errors
      - name: error-traces
        type: status_code
        status_code:
          status_codes: [ERROR]

      # Always sample slow requests (>1s)
      - name: slow-traces
        type: latency
        latency:
          threshold_ms: 1000

      # Sample traces with specific attributes
      - name: vip-users
        type: string_attribute
        string_attribute:
          key: user.tier
          values: [vip, premium]

      # Sample 5% of normal traffic
      - name: probabilistic
        type: probabilistic
        probabilistic:
          sampling_percentage: 5

receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [tail_sampling]
      exporters: [otlp/jaeger]
```

## OpenTelemetry Collector

### Configuration

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  # Add resource attributes
  resource:
    attributes:
      - key: cluster.name
        value: production
        action: insert

  # Batch spans for efficiency
  batch:
    timeout: 10s
    send_batch_size: 1024

  # Memory limiter to prevent OOM
  memory_limiter:
    check_interval: 1s
    limit_mib: 512

  # Sampling
  probabilistic_sampler:
    sampling_percentage: 10

  # Attribute manipulation
  attributes:
    actions:
      - key: http.url
        action: delete  # Remove sensitive URLs
      - key: db.statement
        action: delete  # Remove SQL queries

exporters:
  # Jaeger
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true

  # Tempo
  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true

  # Datadog
  datadog:
    api:
      key: ${DD_API_KEY}

  # Logging (for debugging)
  logging:
    loglevel: debug

extensions:
  health_check:
    endpoint: 0.0.0.0:13133
  pprof:
    endpoint: 0.0.0.0:1777

service:
  extensions: [health_check, pprof]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, probabilistic_sampler]
      exporters: [otlp/tempo, logging]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: otel-collector
spec:
  replicas: 3
  selector:
    matchLabels:
      app: otel-collector
  template:
    metadata:
      labels:
        app: otel-collector
    spec:
      containers:
      - name: otel-collector
        image: otel/opentelemetry-collector-contrib:0.91.0
        args:
          - "--config=/conf/otel-collector-config.yaml"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        volumeMounts:
        - name: config
          mountPath: /conf
        ports:
        - containerPort: 4317  # OTLP gRPC
        - containerPort: 4318  # OTLP HTTP
        - containerPort: 13133 # Health check
      volumes:
      - name: config
        configMap:
          name: otel-collector-config

---
apiVersion: v1
kind: Service
metadata:
  name: otel-collector
spec:
  selector:
    app: otel-collector
  ports:
  - name: otlp-grpc
    port: 4317
    targetPort: 4317
  - name: otlp-http
    port: 4318
    targetPort: 4318
```

## Trace Backends

### Grafana Tempo

```yaml
# tempo.yaml
server:
  http_listen_port: 3200

distributor:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317

ingester:
  trace_idle_period: 10s
  max_block_bytes: 1_000_000
  max_block_duration: 5m

compactor:
  compaction:
    block_retention: 720h  # 30 days

storage:
  trace:
    backend: s3
    s3:
      bucket: tempo-traces
      endpoint: s3.amazonaws.com
    wal:
      path: /var/tempo/wal
    pool:
      max_workers: 100
      queue_depth: 10000
```

### Jaeger

```yaml
# Docker Compose
version: '3'
services:
  jaeger:
    image: jaegertracing/all-in-one:1.52
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    ports:
      - "16686:16686"  # UI
      - "4317:4317"    # OTLP gRPC
      - "4318:4318"    # OTLP HTTP
```

## Best Practices

### Span Naming

```typescript
// GOOD: Operation names, not URLs
tracer.startActiveSpan('GET /users/:id')
tracer.startActiveSpan('database.query')
tracer.startActiveSpan('stripe.charge')

// BAD: High cardinality, not useful
tracer.startActiveSpan('GET /users/12345')  // User ID in name
tracer.startActiveSpan('SELECT * FROM users WHERE id=12345')  // Full query
```

### Attribute Selection

```typescript
// Standard semantic conventions
span.setAttribute('http.method', 'GET');
span.setAttribute('http.status_code', 200);
span.setAttribute('http.url', 'https://api.example.com/users');
span.setAttribute('db.system', 'postgresql');
span.setAttribute('db.statement', 'SELECT * FROM users WHERE id = $1');
span.setAttribute('db.name', 'myapp');

// Business attributes
span.setAttribute('order.id', 'ord_123');
span.setAttribute('user.id', 'user_456');
span.setAttribute('payment.amount', 99.99);
span.setAttribute('payment.currency', 'USD');

// Avoid high-cardinality values in span names
// Put them in attributes instead
```

### Error Handling

```typescript
try {
  await doSomething();
  span.setStatus({ code: SpanStatusCode.OK });
} catch (error) {
  // Record full exception with stack trace
  span.recordException(error);

  // Set error status
  span.setStatus({
    code: SpanStatusCode.ERROR,
    message: error.message,
  });

  // Add error attributes
  span.setAttribute('error.type', error.constructor.name);
  span.setAttribute('error.handled', true);

  throw error;
}
```

### Performance Optimization

```typescript
// Limit span attributes
const limitConfig = {
  attributeValueLengthLimit: 1024,  // Max 1KB per attribute
  attributeCountLimit: 128,         // Max 128 attributes
  eventCountLimit: 128,             // Max 128 events
  linkCountLimit: 128,              // Max 128 links
};

// Batch export for efficiency
const exporter = new OTLPTraceExporter();
const processor = new BatchSpanProcessor(exporter, {
  maxQueueSize: 2048,
  maxExportBatchSize: 512,
  scheduledDelayMillis: 5000,  // Export every 5 seconds
});
```

## Trace Analysis Queries

### Grafana Tempo TraceQL

```promql
# Find slow traces
{ duration > 1s }

# Find errors
{ status = error }

# Find specific service
{ service.name = "payment-service" }

# Combine conditions
{
  service.name = "api" &&
  http.status_code >= 500 &&
  duration > 500ms
}

# Resource attributes
{ cluster.name = "production" && namespace = "default" }

# Span attributes
{ db.system = "postgresql" && db.statement =~ "SELECT.*users.*" }

# Count spans
{ service.name = "api" } | count() > 100
```

### Common Analysis Patterns

```promql
# Top 10 slowest endpoints
topk(10, {service.name="api"} | sort by duration desc)

# Error rate by service
rate({status=error}[5m]) by service.name

# P95 latency by endpoint
histogram_quantile(0.95, {service.name="api"}) by http.route

# Traces with database calls
{service.name="api"} | select(span.db.system)

# Find specific user's traces
{user.id="12345"}
```

This tracing guide provides production-ready OpenTelemetry configurations for comprehensive distributed tracing.
