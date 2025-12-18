# Incident Response and Management

## Incident Severity Levels

### Classification Matrix

| Level | User Impact | Response Time | Escalation | Examples |
|-------|-------------|---------------|------------|----------|
| **SEV-1** | Critical - Service down or major data loss | < 15 minutes | Immediate, all hands | Complete outage, security breach, data corruption |
| **SEV-2** | High - Significant feature degradation | < 1 hour | Page on-call | Partial outage, high error rate (>10%), payment failures |
| **SEV-3** | Medium - Minor impact with workaround | < 4 hours | Email/Slack | Single feature down, slow performance, elevated errors (>5%) |
| **SEV-4** | Low - Cosmetic, no functional impact | Next business day | Ticket | UI glitches, logging errors, non-critical alerts |

### Severity Decision Tree

```yaml
Is the service completely unavailable?
  YES → SEV-1

Is there a security breach or data loss?
  YES → SEV-1

Are core features unavailable or severely degraded?
  YES → SEV-2

Is there a workaround available?
  NO → SEV-2
  YES → Is customer impact moderate?
    YES → SEV-3
    NO → SEV-4

Is it only affecting internal systems?
  YES → Lower one level
```

## Incident Response Framework (IMAG)

### Roles and Responsibilities

```yaml
Incident Commander (IC):
  Responsibilities:
    - Overall incident coordination
    - Declare incident start and end
    - Make final decisions on mitigation strategies
    - Manage escalations
    - Communicate to executive leadership
    - Own postmortem completion

  Should NOT:
    - Debug technical issues directly
    - Implement fixes themselves
    - Get pulled into tactical work

  Key Skills:
    - Stay calm under pressure
    - Clear communication
    - Decisive decision-making

Operations Lead (OL):
  Responsibilities:
    - Technical investigation and debugging
    - Coordinate engineers working on mitigation
    - Implement fixes and deploy changes
    - Report status to IC every 15-30 minutes
    - Maintain incident timeline
    - Validate mitigation effectiveness

  Should NOT:
    - Communicate with customers
    - Make unilateral decisions about incident severity

Communications Lead (CL):
  Responsibilities:
    - Update status page
    - Internal stakeholder notifications
    - Customer communication (if customer-facing)
    - Manage Slack incident channel
    - Document timeline in real-time
    - Notify when incident is resolved

  Should NOT:
    - Get involved in technical debugging
    - Make decisions about mitigation

Subject Matter Expert (SME):
  Responsibilities:
    - Provide domain expertise
    - Assist Operations Lead with debugging
    - Implement specific fixes in their area
    - Review and approve changes

  Should NOT:
    - Take over IC or OL roles without handoff
```

### Incident Lifecycle

```
1. DETECTION
   ├─ Alert fires (automated)
   ├─ User report (manual)
   └─ Monitoring anomaly

2. TRIAGE (< 5 minutes)
   ├─ Assess severity
   ├─ Assign Incident Commander
   └─ Create incident channel

3. RESPONSE
   ├─ Assemble team (IC, OL, CL, SMEs)
   ├─ Create war room (Zoom/Slack)
   ├─ Begin investigation
   └─ Regular status updates (every 15-30 min)

4. MITIGATION
   ├─ Identify root cause
   ├─ Stop the bleeding (temporary fix)
   ├─ Monitor metrics for improvement
   └─ Validate customer impact reduced

5. RESOLUTION
   ├─ Permanent fix deployed
   ├─ Metrics back to normal
   ├─ Monitor for regression
   └─ Incident Commander declares resolved

6. POSTMORTEM
   ├─ Schedule within 48 hours
   ├─ Write blameless postmortem
   ├─ Identify action items
   └─ Share learnings

7. FOLLOW-UP
   ├─ Track action items to completion
   ├─ Update runbooks
   └─ Share with broader team
```

## On-Call Best Practices

### On-Call Rotation

```yaml
Rotation Schedule:
  - Duration: 1 week per rotation
  - Coverage: 24/7
  - Handoff: 15-minute sync at rotation change
  - Backup: Secondary on-call for escalation

Rotation Requirements:
  - Minimum 2 people per rotation (primary + secondary)
  - Balanced across timezones for global teams
  - No more than 1 rotation per month per person
  - Automatic escalation after 15 minutes

Compensation:
  - On-call pay ($X/day)
  - Time off in lieu (TOIL) for incidents after hours
  - Incident bonuses for SEV-1/SEV-2
```

### Escalation Policy

```yaml
# PagerDuty/Opsgenie config
Escalation Levels:
  Level 1 (0 min):
    - Primary on-call engineer
    - Alert: SMS, Phone call, Push notification
    - Timeout: 15 minutes

  Level 2 (15 min):
    - Secondary on-call engineer
    - Alert: Same as Level 1
    - Timeout: 15 minutes

  Level 3 (30 min):
    - Team lead / Manager
    - Alert: Same as Level 1
    - Timeout: 15 minutes

  Level 4 (45 min):
    - Director / VP Engineering
    - Alert: SMS, Phone call
    - Continuous escalation until acknowledged

Alert Channels:
  - SEV-1: Phone call (loops until answered)
  - SEV-2: Push notification + SMS
  - SEV-3: Slack notification
  - SEV-4: Email
```

### Runbooks and Playbooks

```markdown
# Runbook Template: High API Error Rate

## Symptoms
- Alert: "HighErrorRate" firing
- Dashboard: Error rate > 5%
- Customer reports: 500 errors

## Severity
- Error rate 5-10% → SEV-3
- Error rate 10-20% → SEV-2
- Error rate > 20% → SEV-1

## Investigation Steps

### 1. Check Service Health
```bash
# Check pod status
kubectl get pods -n production -l app=api

# Check recent deployments
kubectl rollout history deployment/api -n production

# Check pod logs for errors
kubectl logs -n production -l app=api --tail=100 | grep ERROR
```

### 2. Check Dependencies
```bash
# Database connectivity
kubectl exec -n production <api-pod> -- nc -zv postgres 5432

# Redis connectivity
kubectl exec -n production <api-pod> -- nc -zv redis 6379

# External API health
curl https://partner-api.example.com/health
```

### 3. Check Resource Usage
```promql
# CPU usage
100 * (1 - avg(rate(container_cpu_usage_seconds_total{pod=~"api.*"}[5m])))

# Memory usage
container_memory_usage_bytes{pod=~"api.*"} / container_spec_memory_limit_bytes{pod=~"api.*"}

# Database connections
pg_stat_activity_count
```

## Common Causes

### 1. Recent Deployment
**Fix:** Rollback to previous version
```bash
kubectl rollout undo deployment/api -n production
```

### 2. Database Connection Pool Exhausted
**Fix:** Increase pool size temporarily
```bash
kubectl set env deployment/api -n production DB_POOL_SIZE=100
```

### 3. External API Down
**Fix:** Enable circuit breaker
```bash
kubectl set env deployment/api -n production CIRCUIT_BREAKER_ENABLED=true
```

### 4. High Traffic Spike
**Fix:** Scale up pods
```bash
kubectl scale deployment/api -n production --replicas=20
```

## Escalation
If error rate doesn't improve within 30 minutes:
- Escalate to @backend-team
- Contact @database-team if DB-related
- Page @on-call-manager for SEV-1

## Related Runbooks
- [Database Connection Issues](database-connection-issues.md)
- [High Latency Investigation](high-latency.md)
- [Kubernetes Pod Troubleshooting](k8s-pod-troubleshooting.md)
```

## Incident Communication

### Status Page Updates

```yaml
# Statuspage.io / Atlassian Statuspage

Initial Update (< 15 minutes):
  Status: Investigating
  Template: |
    We are investigating reports of [issue description].
    We will provide an update within 30 minutes.

  Example: |
    We are investigating reports of elevated error rates on the API.
    Some users may experience failures when processing payments.
    We will provide an update within 30 minutes.

Ongoing Updates (every 30 minutes):
  Status: Identified / Monitoring
  Template: |
    We have identified the cause as [brief explanation].
    We are currently [mitigation action].
    Expected resolution: [timeframe or "unknown"].

  Example: |
    We have identified the cause as database connection pool exhaustion.
    We are currently increasing connection limits and scaling the database.
    Expected resolution: 45 minutes.

Resolution Update:
  Status: Resolved
  Template: |
    The issue has been resolved.
    [What was fixed].
    If you continue to experience issues, please contact support.

  Example: |
    The issue has been resolved at 14:30 UTC.
    We increased database connection limits and optimized query performance.
    If you continue to experience issues, please contact support at support@example.com.

Postmortem (within 72 hours):
  Status: Postmortem
  Template: |
    We have published a postmortem about the incident on [date].
    Read more: [link]
```

### Internal Communication

```yaml
Slack Incident Channel:
  Naming: incident-2025-01-15-api-errors
  Pin: Incident details, severity, IC, OL, CL
  Updates: Every 15-30 minutes from CL

  Template:
    ━━━━━━━━━━━━━━━━━━━━━━━━
    🚨 INCIDENT DECLARED
    ━━━━━━━━━━━━━━━━━━━━━━━━
    Severity: SEV-2
    Started: 2025-01-15 14:00 UTC

    Incident Commander: @jane
    Operations Lead: @john
    Communications Lead: @alice

    Summary: High API error rate (15%)
    Impact: Payment processing failures

    War Room: https://zoom.us/j/123456789
    Dashboard: https://grafana.example.com/incident-123
    ━━━━━━━━━━━━━━━━━━━━━━━━

  Status Updates (every 15-30 min):
    [14:30] Update from OL: Identified database connection issue.
            Increasing pool size from 50 → 100. Deploying now.

    [14:45] Update from OL: Deployment complete. Error rate dropped to 8%.
            Monitoring for further improvement.

    [15:00] Update from IC: Error rate back to normal (0.5%).
            Preparing to declare incident resolved.
```

## Alert Fatigue Prevention

### Symptom-Based Alerting

```yaml
# GOOD: Alert on user-facing symptoms
- alert: UserFacingErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total[5m])) > 0.05
  annotations:
    summary: "Users experiencing high error rate ({{ $value | humanizePercentage }})"

# BAD: Alert on internal causes that may not affect users
- alert: CPUHigh
  expr: cpu_usage > 70%
  # Might not impact users at all

# GOOD: SLO-based alerting
- alert: SLOBurnRateTooHigh
  expr: slo:api_availability:ratio < 0.999
  for: 5m
  annotations:
    summary: "Burning error budget too fast"
```

### Alert Grouping and Deduplication

```yaml
# Alertmanager config
route:
  group_by: ['alertname', 'cluster']
  group_wait: 10s        # Wait for similar alerts
  group_interval: 10s    # Batch additional alerts
  repeat_interval: 4h    # Don't re-alert for 4 hours

  routes:
    - match:
        severity: critical
      repeat_interval: 15m  # More frequent for critical
```

### Alert Tuning

```yaml
# Use 'for' to avoid flapping
- alert: HighErrorRate
  expr: error_rate > 0.05
  for: 5m  # Must be true for 5 minutes
  annotations:
    summary: "Sustained high error rate"

# Inhibit lower-priority alerts
inhibit_rules:
  - source_match:
      alertname: ServiceDown
    target_match:
      alertname: HighLatency
    equal: ['service']
```

## Blameless Postmortems

### Postmortem Template

```markdown
# Postmortem: [Brief Title]

**Date:** 2025-01-15
**Authors:** Jane Doe (IC), John Smith (OL)
**Status:** Complete
**Severity:** SEV-2

## Executive Summary
One-paragraph summary of what happened, impact, and resolution.

Example: On January 15, 2025, our API experienced a 15% error rate for
1 hour and 45 minutes, affecting approximately 15,000 users attempting to
process payments. The incident was caused by database connection pool
exhaustion during a traffic spike. We resolved the issue by increasing
connection limits and implementing auto-scaling.

## Impact
- **Duration:** 1 hour 45 minutes (14:00 - 15:45 UTC)
- **Users Affected:** ~15,000 users
- **Error Rate:** 15% peak, 8% sustained
- **Revenue Impact:** Estimated $12,000 in failed transactions
- **SLO Impact:** Consumed 40% of monthly error budget
- **Data Loss:** None

## Timeline (All times UTC)
- **14:00** - Alert: "HighErrorRate" fires (error rate 12%)
- **14:02** - Jane assigned as IC, incident channel created
- **14:05** - John (OL) begins investigation
- **14:10** - Identified: Database connection pool exhausted (50/50 connections in use)
- **14:15** - First mitigation: Increased pool size to 75 connections
- **14:20** - Error rate decreased to 10%
- **14:25** - Second mitigation: Increased to 100 connections
- **14:30** - Error rate decreased to 8%
- **14:35** - Implemented auto-scaling based on connection usage
- **14:45** - Error rate back to normal (0.5%)
- **15:00** - Monitoring for regression
- **15:45** - Incident declared resolved

## Root Cause
The API's database connection pool was configured with a static size of 50
connections, which was adequate for average traffic but insufficient for
peak loads. On January 15, traffic spiked to 3x normal levels due to a
marketing campaign. Once all 50 connections were in use, new requests
queued and eventually timed out, resulting in 500 errors to users.

**Contributing Factors:**
1. No auto-scaling for database connection pool
2. No alert on connection pool saturation
3. Inadequate load testing (only tested at 2x normal load)
4. Marketing campaign not communicated to engineering

## What Went Well
- Alert fired within 2 minutes of elevated errors
- IC assigned immediately, clear command structure
- Root cause identified in 10 minutes
- Mitigation applied quickly (first fix in 15 minutes)
- No data loss or corruption
- Good communication with stakeholders

## What Went Wrong
- No proactive monitoring of connection pool usage
- Static connection pool configuration (should be dynamic)
- Load testing didn't cover 3x traffic scenarios
- Marketing campaign not coordinated with engineering
- No circuit breaker to fail fast instead of queueing

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Add Prometheus metrics for DB connection pool usage | @john | Jan 18 | ✅ Done |
| Implement auto-scaling for connection pool | @alice | Jan 22 | 🔄 In Progress |
| Add alert: connection pool > 80% | @jane | Jan 17 | ✅ Done |
| Load test at 5x traffic | @bob | Jan 25 | ⏳ Not Started |
| Document connection pool tuning in runbook | @john | Jan 20 | ✅ Done |
| Create process for eng/marketing coordination | @jane | Jan 30 | ⏳ Not Started |
| Implement circuit breaker for DB calls | @alice | Feb 5 | ⏳ Not Started |

## Lessons Learned
1. **Static limits are failure points** - Any statically configured resource
   limit will eventually be exceeded under load. Use auto-scaling.

2. **Test at higher multiples** - If you expect 2x traffic, test at 5x.
   Real-world spikes can exceed expectations.

3. **Monitor saturation, not just errors** - By the time error rate spiked,
   the connection pool had been saturated for minutes. Earlier detection
   would have enabled proactive mitigation.

4. **Cross-functional communication matters** - Marketing campaigns that
   drive traffic need engineering input on infrastructure capacity.

## Related Incidents
- 2024-11-10: Similar issue with Redis connection pool (SEV-3)
- 2024-09-05: Database timeout during Black Friday (SEV-1)

## Appendix
- [Grafana dashboard during incident](https://grafana.example.com/incident-123)
- [Slack incident channel](https://slack.com/incident-2025-01-15-api-errors)
- [Runbook: Database connection issues](runbooks/database-connections.md)
```

### Postmortem Best Practices

```yaml
Timing:
  - Schedule within 48 hours of resolution
  - Complete within 1 week
  - Review with team within 2 weeks

Facilitation:
  - Incident Commander facilitates
  - All responders attend
  - No managers in initial meeting (psychological safety)
  - 60-90 minute session

Focus Areas:
  - Timeline accuracy (facts, not opinions)
  - Root cause (not root person)
  - System gaps (not individual mistakes)
  - Process improvements (not blame)

Language:
  - "The system failed to..." (not "Bob forgot to...")
  - "We lacked visibility into..." (not "We should have known...")
  - "The process allowed..." (not "They didn't follow...")

Action Items:
  - Specific and measurable
  - Assigned owner and due date
  - Tracked to completion
  - Reviewed in next postmortem

Sharing:
  - Share with entire engineering org
  - Post on company wiki
  - Include in monthly all-hands
  - Add to runbook library
```

## Training and Drills

### Wheel of Misfortune

```yaml
Purpose:
  - Practice incident response in safe environment
  - Train new on-call engineers
  - Validate runbooks
  - Identify gaps in knowledge

Format:
  - 60-minute session
  - 1 facilitator, 3-5 participants
  - Use past incidents or hypothetical scenarios
  - Rotate roles (IC, OL, CL)

Process:
  1. Facilitator presents initial symptoms
  2. Participants ask questions (facilitator answers as if it's real)
  3. Participants investigate using real tools (read-only)
  4. Participants propose mitigations
  5. Facilitator reveals outcome
  6. Debrief: What went well, what to improve

Scenarios:
  - Database connection pool exhausted
  - Kubernetes node failure
  - DDoS attack
  - Certificate expiration
  - Cascading failure
```

### Failure Friday / Chaos Engineering

```yaml
Purpose:
  - Validate incident response readiness
  - Test systems under failure conditions
  - Train team on real-world scenarios

Schedule:
  - Weekly, Friday 2-4 PM (low-traffic window)
  - Announced 1 day in advance
  - IC on standby

Experiments:
  - Pod termination (10% of pods)
  - Network latency injection (100ms)
  - Database connection limit reduction
  - External API failures
  - Resource exhaustion (CPU/memory)

Success Criteria:
  - SLOs maintained during failure
  - Alerts fired appropriately
  - Team responded within SLA
  - Automatic recovery worked

Debrief:
  - Document findings
  - Update runbooks
  - Fix gaps discovered
```

This incident response guide provides production-ready processes for managing incidents effectively with blameless culture and continuous improvement.
