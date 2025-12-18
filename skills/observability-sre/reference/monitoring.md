# Monitoring with Prometheus and Grafana

## Prometheus Architecture

### Core Components

```yaml
Prometheus Server:
  - Scrapes and stores time-series data
  - Executes PromQL queries
  - Evaluates alerting rules
  - Forwards alerts to Alertmanager

Exporters:
  - node_exporter: Hardware and OS metrics
  - kube-state-metrics: Kubernetes object states
  - blackbox_exporter: Endpoint probes
  - Custom exporters: Application metrics

Alertmanager:
  - Alert deduplication
  - Grouping and routing
  - Silences and inhibitions
  - Notification channels

Pushgateway:
  - For short-lived jobs
  - Batch jobs that can't be scraped
  - Use sparingly (anti-pattern for most cases)
```

### Scrape Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production-us-east-1'
    environment: 'prod'

# Alertmanager connection
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

# Recording and alerting rules
rule_files:
  - 'rules/recording/*.yml'
  - 'rules/alerting/*.yml'

scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node exporter (system metrics)
  - job_name: 'node'
    static_configs:
      - targets:
        - 'node1.internal:9100'
        - 'node2.internal:9100'

  # Kubernetes service discovery
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Only scrape pods with prometheus.io/scrape annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      # Use custom port if specified
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)
        replacement: $1:${1}
      # Add pod labels
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      # Add namespace
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      # Add pod name
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
```

### Application Metrics Instrumentation

```typescript
// Node.js with prom-client
import express from 'express';
import client from 'prom-client';

const app = express();

// Create a Registry
const register = new client.Registry();

// Add default metrics (CPU, memory, event loop lag)
client.collectDefaultMetrics({ register });

// Custom metrics
const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.001, 0.01, 0.1, 0.5, 1, 2, 5], // 1ms to 5s
  registers: [register],
});

const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status'],
  registers: [register],
});

const activeConnections = new client.Gauge({
  name: 'http_active_connections',
  help: 'Number of active HTTP connections',
  registers: [register],
});

// Middleware to track metrics
app.use((req, res, next) => {
  const start = Date.now();
  activeConnections.inc();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration.labels(req.method, req.route?.path || req.path, res.statusCode).observe(duration);
    httpRequestsTotal.labels(req.method, req.route?.path || req.path, res.statusCode).inc();
    activeConnections.dec();
  });

  next();
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.listen(3000);
```

## PromQL Query Language

### Basic Queries

```promql
# Instant vector - current value
http_requests_total

# With label filtering
http_requests_total{status="200", method="GET"}

# Regex matching
http_requests_total{status=~"2..", method!="OPTIONS"}

# Range vector - time series over duration
http_requests_total[5m]

# Rate of requests per second
rate(http_requests_total[5m])

# Sum across all instances
sum(rate(http_requests_total[5m]))

# Group by label
sum(rate(http_requests_total[5m])) by (method, status)
```

### Advanced Queries

```promql
# P95 latency from histogram
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)

# Error rate (5xx / total)
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# Requests per second by method
sum(rate(http_requests_total[5m])) by (method)

# CPU usage percentage
100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))

# Memory usage percentage
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

# Disk space remaining
node_filesystem_avail_bytes{mountpoint="/"}

# Predict when disk will be full (linear regression)
predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[1h], 4*3600) < 0
```

### Subqueries

```promql
# Max request rate in the last hour, sampled every 5 minutes
max_over_time(
  rate(http_requests_total[5m])[1h:5m]
)

# 99th percentile latency over the last 24 hours
quantile_over_time(0.99,
  http_request_duration_seconds[24h]
)
```

## Recording Rules

```yaml
# rules/recording/api_performance.yml
groups:
  - name: api_performance
    interval: 30s
    rules:
      # Request rate by service
      - record: job:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job, method)

      # Error rate by service
      - record: job:http_errors:rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
          /
          sum(rate(http_requests_total[5m])) by (job)

      # P50, P95, P99 latency
      - record: job:http_latency:p50
        expr: histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))

      - record: job:http_latency:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))

      - record: job:http_latency:p99
        expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))

      # Aggregation for federation
      - record: instance:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (instance)
```

## Alerting Rules

```yaml
# rules/alerting/api_alerts.yml
groups:
  - name: api_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: job:http_errors:rate5m > 0.05  # 5% error rate
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on {{ $labels.job }}"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"

      # Critical error rate
      - alert: CriticalErrorRate
        expr: job:http_errors:rate5m > 0.10  # 10% error rate
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "CRITICAL: Error rate on {{ $labels.job }}"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 10%)"
          runbook_url: "https://wiki.example.com/runbooks/high-error-rate"

      # High latency
      - alert: HighLatency
        expr: job:http_latency:p95 > 0.5  # 500ms P95
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency on {{ $labels.job }}"
          description: "P95 latency is {{ $value }}s (threshold: 0.5s)"

      # Service down
      - alert: ServiceDown
        expr: up{job="api"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"

      # High memory usage
      - alert: HighMemoryUsage
        expr: |
          100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) > 90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | humanizePercentage }}"

      # Disk space low
      - alert: DiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} disk space remaining"

      # Disk will fill in 4 hours
      - alert: DiskWillFillSoon
        expr: predict_linear(node_filesystem_avail_bytes{mountpoint="/"}[1h], 4*3600) < 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Disk {{ $labels.mountpoint }} will fill in 4 hours"
          description: "Based on current usage trend"
```

## Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/XXX'
  pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'

# Templates for notifications
templates:
  - '/etc/alertmanager/templates/*.tmpl'

# Route alerts based on labels
route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'job']
  group_wait: 10s        # Wait before sending first notification
  group_interval: 10s    # Wait before sending batch of new alerts
  repeat_interval: 12h   # Wait before re-sending notification

  routes:
    # Critical alerts to PagerDuty
    - match:
        severity: critical
      receiver: 'pagerduty'
      group_wait: 0s
      repeat_interval: 5m

    # Database alerts to database team
    - match_re:
        job: '.*database.*'
      receiver: 'database-team'

    # Non-critical to Slack
    - match:
        severity: warning
      receiver: 'slack'

receivers:
  - name: 'default'
    email_configs:
      - to: 'ops@example.com'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '<PAGERDUTY_SERVICE_KEY>'
        description: '{{ .GroupLabels.alertname }}'
        severity: '{{ .CommonLabels.severity }}'

  - name: 'slack'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}\n{{ end }}'
        send_resolved: true

  - name: 'database-team'
    email_configs:
      - to: 'db-team@example.com'
    slack_configs:
      - channel: '#database-alerts'

# Inhibition rules - suppress alerts when others fire
inhibit_rules:
  # If service is down, don't alert on high latency
  - source_match:
      alertname: ServiceDown
    target_match:
      alertname: HighLatency
    equal: ['job', 'instance']
```

## Grafana Dashboards

### RED Dashboard for Services

```json
{
  "dashboard": {
    "title": "API Service - RED Metrics",
    "rows": [
      {
        "title": "Request Rate",
        "panels": [
          {
            "title": "Requests per Second",
            "targets": [
              {
                "expr": "sum(rate(http_requests_total{job=\"api\"}[5m])) by (method)"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Request Rate by Route",
            "targets": [
              {
                "expr": "topk(10, sum(rate(http_requests_total{job=\"api\"}[5m])) by (route))"
              }
            ],
            "type": "graph"
          }
        ]
      },
      {
        "title": "Error Rate",
        "panels": [
          {
            "title": "Error Rate %",
            "targets": [
              {
                "expr": "100 * (sum(rate(http_requests_total{job=\"api\",status=~\"5..\"}[5m])) / sum(rate(http_requests_total{job=\"api\"}[5m])))"
              }
            ],
            "type": "graph",
            "fieldConfig": {
              "defaults": {
                "unit": "percent"
              }
            }
          },
          {
            "title": "Errors by Status Code",
            "targets": [
              {
                "expr": "sum(rate(http_requests_total{job=\"api\",status=~\"5..\"}[5m])) by (status)"
              }
            ],
            "type": "graph"
          }
        ]
      },
      {
        "title": "Duration (Latency)",
        "panels": [
          {
            "title": "Request Latency Percentiles",
            "targets": [
              {
                "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{job=\"api\"}[5m])) by (le))",
                "legendFormat": "P50"
              },
              {
                "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job=\"api\"}[5m])) by (le))",
                "legendFormat": "P95"
              },
              {
                "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{job=\"api\"}[5m])) by (le))",
                "legendFormat": "P99"
              }
            ],
            "type": "graph",
            "fieldConfig": {
              "defaults": {
                "unit": "s"
              }
            }
          }
        ]
      }
    ]
  }
}
```

### USE Dashboard for Resources

```json
{
  "dashboard": {
    "title": "Node Resources - USE Metrics",
    "templating": {
      "list": [
        {
          "name": "instance",
          "type": "query",
          "query": "label_values(node_cpu_seconds_total, instance)"
        }
      ]
    },
    "rows": [
      {
        "title": "Utilization",
        "panels": [
          {
            "title": "CPU Utilization %",
            "targets": [
              {
                "expr": "100 * (1 - avg(rate(node_cpu_seconds_total{mode=\"idle\",instance=\"$instance\"}[5m])))"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Memory Utilization %",
            "targets": [
              {
                "expr": "100 * (1 - (node_memory_MemAvailable_bytes{instance=\"$instance\"} / node_memory_MemTotal_bytes{instance=\"$instance\"}))"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Disk Utilization %",
            "targets": [
              {
                "expr": "100 * (1 - (node_filesystem_avail_bytes{instance=\"$instance\",mountpoint=\"/\"} / node_filesystem_size_bytes{instance=\"$instance\",mountpoint=\"/\"}))"
              }
            ],
            "type": "graph"
          }
        ]
      },
      {
        "title": "Saturation",
        "panels": [
          {
            "title": "Load Average (1m, 5m, 15m)",
            "targets": [
              {
                "expr": "node_load1{instance=\"$instance\"}",
                "legendFormat": "1m"
              },
              {
                "expr": "node_load5{instance=\"$instance\"}",
                "legendFormat": "5m"
              },
              {
                "expr": "node_load15{instance=\"$instance\"}",
                "legendFormat": "15m"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Disk I/O Utilization %",
            "targets": [
              {
                "expr": "rate(node_disk_io_time_seconds_total{instance=\"$instance\"}[5m]) * 100"
              }
            ],
            "type": "graph"
          }
        ]
      },
      {
        "title": "Errors",
        "panels": [
          {
            "title": "Network Errors",
            "targets": [
              {
                "expr": "rate(node_network_receive_errs_total{instance=\"$instance\"}[5m])",
                "legendFormat": "RX {{ device }}"
              },
              {
                "expr": "rate(node_network_transmit_errs_total{instance=\"$instance\"}[5m])",
                "legendFormat": "TX {{ device }}"
              }
            ],
            "type": "graph"
          }
        ]
      }
    ]
  }
}
```

## Performance Optimization

### Metric Cardinality

```yaml
# GOOD: Low cardinality labels
http_requests_total{method="GET", status="200", service="api"}
# Cardinality = methods (5) × statuses (10) × services (20) = 1,000

# BAD: High cardinality labels (DON'T DO THIS!)
http_requests_total{user_id="12345", session_id="abc..."}
# Cardinality = users (1M) × sessions (10M) = EXPLODES

# Rule: Limit label cardinality to < 10,000 combinations
# Use high-cardinality data in logs/traces, not metrics
```

### Query Optimization

```promql
# SLOW: Calculates rate for each series, then sums
sum(rate(http_requests_total[5m]))

# FAST: Sums first, then calculates rate (fewer series)
rate(sum(http_requests_total)[5m])

# SLOW: Large range for high-resolution data
rate(http_requests_total[1h])

# FAST: Smaller range with recording rules
rate(http_requests_total[5m])

# Use recording rules for dashboard queries
# Dashboards should query recording rules, not raw metrics
```

### Retention and Storage

```yaml
# Prometheus config
storage:
  tsdb:
    path: /prometheus/data
    retention.time: 15d  # Keep 15 days locally
    retention.size: 50GB # Or max 50GB

# Use remote write for long-term storage
remote_write:
  - url: "https://thanos.example.com/api/v1/receive"
    queue_config:
      capacity: 10000
      max_shards: 50
      min_shards: 1
      max_samples_per_send: 5000
      batch_send_deadline: 5s

# Thanos for long-term storage (years)
# VictoriaMetrics for cost-effective storage
# Cortex for multi-tenant setups
```

## Common Patterns

### Blackbox Monitoring

```yaml
# Probe endpoints from outside
scrape_configs:
  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
        - https://api.example.com/health
        - https://www.example.com
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115

# Check SSL certificate expiry
- alert: SSLCertExpiringSoon
  expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 30  # 30 days
  annotations:
    summary: "SSL certificate expires in {{ $value | humanizeDuration }}"
```

### Service Discovery

```yaml
# EC2 instances
- job_name: 'ec2'
  ec2_sd_configs:
    - region: us-east-1
      port: 9100
  relabel_configs:
    - source_labels: [__meta_ec2_tag_Name]
      target_label: instance
    - source_labels: [__meta_ec2_tag_Environment]
      target_label: environment

# Consul service discovery
- job_name: 'consul'
  consul_sd_configs:
    - server: 'consul.example.com:8500'
      services: ['web', 'api', 'database']
```

This monitoring guide provides production-ready Prometheus and Grafana configurations for comprehensive system observability.
