# SLO Definition Template

## Service: [Service Name]

**Owner:** [Team Name]
**Last Updated:** [Date]
**Review Frequency:** Quarterly

---

## Service Overview

**Description:** [Brief description of what this service does]

**User Journey:** [Describe the critical user paths this service supports]

**Dependencies:**
- [Upstream service 1]
- [Upstream service 2]
- [Database/cache/queue]

---

## SLIs (Service Level Indicators)

### 1. Availability

**Definition:** Percentage of successful requests over total requests

**Measurement:**
```promql
# Recording rule
- record: slo:service_availability:ratio
  expr: |
    sum(rate(http_requests_total{service="my-service",status!~"5.."}[5m]))
    /
    sum(rate(http_requests_total{service="my-service"}[5m]))
```

**Data Source:** Prometheus metrics from application instrumentation

**Valid Requests:**
- Include: All HTTP requests to API endpoints
- Exclude: Health checks (`/health`, `/ready`)
- Exclude: Internal monitoring requests

**Success Criteria:**
- HTTP status codes 200-499 (4xx are user errors, not service errors)
- Response received within timeout (30 seconds)

---

### 2. Latency

**Definition:** Percentage of requests completed within target latency

**Measurement:**
```promql
# P95 latency
- record: slo:service_latency:p95
  expr: |
    histogram_quantile(0.95,
      sum(rate(http_request_duration_seconds_bucket{service="my-service"}[5m])) by (le)
    )

# Percentage of requests under 200ms
- record: slo:service_latency:success_ratio
  expr: |
    sum(rate(http_request_duration_seconds_bucket{service="my-service",le="0.2"}[5m]))
    /
    sum(rate(http_request_duration_seconds_count{service="my-service"}[5m]))
```

**Target:** 95% of requests complete in < 200ms (P95 latency)

**Measurement Window:** 5-minute rolling window

**Breakdown by Endpoint:**
- `GET /users` - 100ms
- `POST /orders` - 200ms
- `GET /search` - 500ms (complex query)

---

### 3. Error Rate

**Definition:** Percentage of requests that result in server errors

**Measurement:**
```promql
# Error rate
- record: slo:service_errors:rate
  expr: |
    sum(rate(http_requests_total{service="my-service",status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total{service="my-service"}[5m]))
```

**Error Types Counted:**
- 5xx HTTP status codes
- Request timeouts
- Circuit breaker open
- Database connection failures

**Error Types Excluded:**
- 4xx client errors (user mistakes)
- Validation errors
- Authentication failures (user input)

---

## SLOs (Service Level Objectives)

### Production SLOs

| SLI | Target | Measurement Window | Error Budget (Monthly) |
|-----|--------|-------------------|----------------------|
| **Availability** | 99.9% ("three nines") | 30 days | 43.2 minutes downtime |
| **Latency (P95)** | < 200ms for 95% of requests | 30 days | 5% of requests may be slower |
| **Error Rate** | < 0.1% | 30 days | 0.1% of requests may error |

### Per-Endpoint SLOs

| Endpoint | Availability | Latency (P95) | Notes |
|----------|--------------|---------------|-------|
| `GET /users/:id` | 99.95% | 100ms | Critical path |
| `POST /orders` | 99.9% | 200ms | Payment flow |
| `GET /search` | 99.5% | 500ms | Complex queries, less critical |
| `POST /analytics` | 99.0% | 1000ms | Async processing |

---

## Error Budget

### Calculation

```python
SLO = 99.9%
Error_Budget = 100% - 99.9% = 0.1%

# Monthly (30 days)
Total_Minutes = 30 * 24 * 60 = 43,200 minutes
Allowed_Downtime = 43,200 * 0.001 = 43.2 minutes

# Weekly
Weekly_Minutes = 7 * 24 * 60 = 10,080 minutes
Weekly_Allowed_Downtime = 10,080 * 0.001 = 10.08 minutes
```

### Error Budget Policy

| Budget Remaining | Action |
|-----------------|--------|
| **> 75%** | Normal operations. Ship features, experiment freely. |
| **50-75%** | Be cautious. Require additional testing for risky changes. |
| **25-50%** | Slow down. Focus on reliability improvements. Defer non-critical features. |
| **< 25%** | **FREEZE DEPLOYS**. Only critical bug fixes and reliability improvements. |
| **0%** | Emergency: All hands on deck for reliability. No new features. |

### Burn Rate Alerts

```yaml
# Multi-window burn rate alerting
# Based on Google SRE Workbook

- alert: SLOBurnRateCritical
  # Burning 14.4x (will exhaust budget in 2 days)
  expr: |
    (
      slo:service_availability:ratio < 0.856  # 99.9% - (14.4 * 0.1%) = 98.56%
      and
      slo:service_availability:ratio_1h < 0.856
    )
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "Burning error budget at 14.4x rate"
    description: "At current rate, will exhaust monthly budget in 2 days"

- alert: SLOBurnRateHigh
  # Burning 6x (will exhaust budget in 5 days)
  expr: |
    (
      slo:service_availability:ratio < 0.94  # 99.9% - (6 * 0.1%) = 99.4%
      and
      slo:service_availability:ratio_6h < 0.94
    )
  for: 15m
  labels:
    severity: warning
  annotations:
    summary: "Burning error budget at 6x rate"

- alert: SLOBurnRateModerate
  # Burning 3x (will exhaust budget in 10 days)
  expr: |
    (
      slo:service_availability:ratio < 0.97  # 99.9% - (3 * 0.1%) = 99.7%
      and
      slo:service_availability:ratio_1d < 0.97
    )
  for: 1h
  labels:
    severity: warning
```

---

## SLA (Service Level Agreement)

**Customer Commitment:** 99.9% monthly availability

**Measurement:** Based on SLI availability metric

**Credits:**
- 99.9% - 99.0% availability: 10% service credit
- 99.0% - 95.0% availability: 25% service credit
- < 95.0% availability: 50% service credit

**Exclusions:**
- Planned maintenance (announced 7 days in advance)
- Customer-caused issues (invalid requests, quota exceeded)
- Force majeure (natural disasters, DDoS attacks)

**Claim Process:**
1. Customer submits ticket within 30 days
2. SRE team validates metrics
3. Credit applied to next invoice

---

## Dashboard

**Grafana Dashboard:** [Link to dashboard]

**Panels:**
1. Current availability (gauge)
2. 30-day availability trend (graph)
3. Error budget remaining (gauge + graph)
4. P95 latency by endpoint (graph)
5. Error rate (graph)
6. Request rate (graph)

**Example PromQL Queries:**

```promql
# Current availability (last 5 minutes)
avg_over_time(slo:service_availability:ratio[5m])

# 30-day availability
avg_over_time(slo:service_availability:ratio[30d])

# Error budget remaining
1 - (
  (1 - avg_over_time(slo:service_availability:ratio[30d]))
  /
  (1 - 0.999)  # SLO target
)

# Burn rate
(1 - slo:service_availability:ratio)
/
(1 - 0.999)
```

---

## Alerting Strategy

### Alert Hierarchy

1. **Symptom-based (SLO violations)** — Primary alerts
   - Alert when SLO is at risk (burn rate too high)
   - Page on-call for critical burn rate

2. **Cause-based (system health)** — Secondary alerts
   - Database connection pool saturation
   - High CPU/memory usage
   - External dependency failures
   - Send to Slack, don't page

### Alert Routing

```yaml
# Alertmanager config
routes:
  - match:
      alertname: SLOBurnRateCritical
    receiver: pagerduty-critical
    group_wait: 0s
    repeat_interval: 5m

  - match:
      alertname: SLOBurnRateHigh
    receiver: pagerduty-warning
    repeat_interval: 30m

  - match:
      alertname: SLOBurnRateModerate
    receiver: slack-alerts
    repeat_interval: 4h
```

---

## Review and Iteration

### Quarterly Review

**Review Date:** [First week of each quarter]

**Review Checklist:**
- [ ] Are SLOs still aligned with user expectations?
- [ ] Have there been repeated SLO violations?
- [ ] Is error budget consistently under/over-utilized?
- [ ] Do SLOs match actual system capabilities?
- [ ] Are there new critical user journeys to track?

**Adjustment Process:**
1. Review SLO violations from past quarter
2. Analyze error budget consumption trend
3. Gather user feedback on performance
4. Propose SLO adjustments (stricter or looser)
5. Get approval from product and engineering leads
6. Update SLO definitions and alerts
7. Communicate changes to stakeholders

### Historical SLO Performance

| Quarter | Availability | Latency (P95) | Error Budget Used | Notes |
|---------|--------------|---------------|-------------------|-------|
| Q4 2024 | 99.95% | 180ms | 25% | Excellent quarter |
| Q1 2025 | 99.87% | 210ms | 87% | Database incident consumed budget |
| Q2 2025 | 99.92% | 195ms | 60% | Improved after Q1 incident |

---

## Runbooks

**Related Runbooks:**
- [High Error Rate Investigation](../runbooks/high-error-rate.md)
- [Latency Debugging](../runbooks/latency-debugging.md)
- [Database Connection Issues](../runbooks/database-connections.md)

---

## Stakeholders

**Service Owner:** [Name, @slack]
**Product Manager:** [Name, @slack]
**On-Call Team:** [Team name]
**Escalation Contact:** [Manager name, @slack]

---

## Example: Filled-In SLO

### Service: Payment Processing API

**Owner:** Payment Team
**Last Updated:** 2025-01-15
**Review Frequency:** Quarterly

---

## SLOs (Service Level Objectives)

| SLI | Target | Current (30d) | Error Budget Used |
|-----|--------|---------------|-------------------|
| **Availability** | 99.9% | 99.92% | 20% |
| **Latency (P95)** | < 200ms | 185ms | ✅ Met |
| **Error Rate** | < 0.1% | 0.05% | 50% |

**Status:** ✅ All SLOs met
**Error Budget:** 80% remaining (safe to deploy)

---

## Recent SLO Violations

| Date | SLO Violated | Impact | Root Cause | Postmortem |
|------|--------------|--------|------------|------------|
| 2025-01-15 | Availability (99.87% for 2 hours) | 15,000 users | Database pool exhaustion | [Link](../postmortems/2025-01-15.md) |

---

## Notes

- This template should be customized for each service
- SLOs should be based on user expectations, not arbitrary numbers
- Start with looser SLOs and tighten over time
- Review and adjust quarterly based on actual performance
- Error budget is a tool for decision-making, not a punishment
