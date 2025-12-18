# Cohort Analysis & Retention

## Overview

Retention is the single most important metric for product success. Cohort analysis reveals which users stick around and why, enabling you to build more engaging products.

**Key Insight:** A 5% increase in retention can lead to 25-95% increase in profits. Retaining users is far cheaper than acquiring new ones.

---

## What is Cohort Analysis?

### Definition

**Cohort analysis** groups users by shared characteristics (usually sign-up date) and tracks their behavior over time.

```markdown
Cohort = Group of users sharing a common characteristic

Common cohorts:
• Time-based: Users who signed up in January
• Acquisition: Users from Google Ads
• Behavioral: Users who completed onboarding
• Demographic: Users from California
```

### Why Cohort Analysis Matters

```markdown
✓ Reveals retention patterns over time
✓ Identifies product-market fit (PMF)
✓ Measures impact of product changes
✓ Compares quality across acquisition channels
✓ Validates growth strategies
✓ Predicts future revenue

Example:
Total active users = 10,000 (looks good!)
But: 9,000 are new this month, 1,000 from prior months
→ Terrible retention, unsustainable growth
```

---

## Types of Cohort Analysis

### 1. Acquisition Cohorts (Time-Based)

**Most common:** Group by sign-up date

```markdown
Cohort: Jan 2025 sign-ups
Track: How many return Day 1, 7, 30, 90?

Example Table:
| Cohort    | Size  | D1   | D7   | D30  | D90  |
|-----------|-------|------|------|------|------|
| Jan 2025  | 1000  | 60%  | 35%  | 20%  | 15%  |
| Dec 2024  | 950   | 58%  | 32%  | 18%  | 14%  |
| Nov 2024  | 900   | 55%  | 30%  | 16%  | 12%  |

Insight: Retention improving month-over-month! ✓
```

### 2. Behavioral Cohorts

**Group by actions taken**

```markdown
Examples:
• Users who completed onboarding
• Users who invited teammates
• Users who used Feature X
• Users who made first purchase

Purpose: Identify retention drivers

Example:
Cohort A: Completed onboarding → 80% D30 retention
Cohort B: Skipped onboarding → 20% D30 retention

Insight: Onboarding is critical! Focus here.
```

### 3. Acquisition Channel Cohorts

**Group by traffic source**

```markdown
Cohorts:
• Organic search
• Paid ads
• Referrals
• Social media
• Direct

Purpose: Measure channel quality

Example:
| Channel  | D30 Retention | CPA  | LTV  | LTV:CAC |
|----------|---------------|------|------|---------|
| Organic  | 40%           | $10  | $200 | 20:1    |
| Paid     | 25%           | $50  | $100 | 2:1     |
| Referral | 55%           | $5   | $300 | 60:1    |

Insight: Referrals = highest quality users
```

---

## Retention Calculation Methods

### Method 1: Classic Retention (Unbounded)

**Definition:** % of cohort active on Day N (regardless of gaps)

```
Day N Retention = Users active on Day N / Cohort size

Example:
Cohort: 1,000 users signed up Jan 1
Day 7: 350 users were active (anytime on Day 7)

Day 7 Retention = 350 / 1,000 = 35%
```

**Use case:** Standard retention metric

### Method 2: Bracket Retention (Range)

**Definition:** % of cohort active during period (e.g., Week 1 = Day 1-7)

```
Week N Retention = Users active in Week N / Cohort size

Example:
Cohort: 1,000 users signed up Jan 1
Week 1 (Day 1-7): 600 users active at least once

Week 1 Retention = 600 / 1,000 = 60%
```

**Use case:** More forgiving, accounts for usage patterns

### Method 3: N-Day Return Retention

**Definition:** % of cohort active on EXACTLY Day N (not before)

```
Day N Return = Users active Day N (not Day N-1) / Cohort size
```

**Use case:** Measure re-engagement campaigns

### Method 4: Rolling Retention

**Definition:** % of cohort active on Day N or any day after

```
Rolling Day N = Users active Day N or later / Cohort size
```

**Use case:** Best for measuring long-term engagement

---

## Retention Cohort Table

### Standard Format

```markdown
| Cohort     | Size | D0   | D1   | D7   | D14  | D30  | D60  | D90  |
|------------|------|------|------|------|------|------|------|------|
| 2025-01-01 | 1000 | 100% | 60%  | 35%  | 28%  | 20%  | 17%  | 15%  |
| 2025-01-02 | 1050 | 100% | 62%  | 37%  | 30%  | 22%  | 18%  | 16%  |
| 2025-01-03 | 980  | 100% | 58%  | 33%  | 26%  | 19%  | 16%  | 14%  |
| 2025-01-04 | 1100 | 100% | 64%  | 40%  | 32%  | 24%  | 20%  | 18%  |

Observations:
• Jan 4 cohort retains best (product improvement?)
• Typical pattern: sharp drop D0→D1, then gradual decline
• D90 retention stabilizing ~15-18% (core engaged users)
```

### Heatmap Visualization

```
        D1   D7   D14  D30  D60  D90
Jan-01  🟢   🟡   🟡   🟠   🟠   🔴
Jan-02  🟢   🟢   🟡   🟡   🟠   🟠
Jan-03  🟢   🟡   🟠   🟠   🔴   🔴
Jan-04  🟢   🟢   🟢   🟡   🟡   🟠

🟢 = High retention (>50%)
🟡 = Medium (30-50%)
🟠 = Low (15-30%)
🔴 = Very low (<15%)
```

---

## Retention Curves

### The Ideal Curve

```
100% ┐
     │╲
 80% │ ╲
     │  ╲_________ ← Flattens = found core users
 60% │
     │
 40% │
     │
 20% │
     │
  0% └─────────────────────────────────
     D0  D1  D7   D30   D60   D90  D180

Good retention curve:
• Sharp initial drop (casual users churn)
• Flattens (core engaged users remain)
• Plateau = product-market fit
```

### Bad Retention Curves

```markdown
## Continuous Decline (No PMF)
100% ┐
     │╲
     │ ╲
     │  ╲
     │   ╲
     │    ╲______
  0% └─────────────────
     D0  D1  D7  D30

Problem: Never flattens, users keep churning
Diagnosis: No product-market fit
Action: Rethink product, find core value

## Smile Curve (Re-engagement)
100% ┐
     │╲
 50% │ ╲___/─── ← Rises back up
     │
  0% └─────────────────
     D0  D1  D7  D30

Pattern: Drop then rise
Diagnosis: Effective re-engagement (email, push)
OR: Subscription renewal cycle
Action: Optimize re-engagement campaigns
```

---

## Retention Benchmarks

### By Product Type

```markdown
## Consumer Social (Facebook, Instagram, TikTok)
D1:  60-80%
D7:  40-60%
D30: 30-50%

## SaaS B2B (Slack, Asana, Notion)
D1:  70-90%
D7:  50-70%
D30: 40-60%

## E-commerce (Amazon, Shopify stores)
D1:  20-40%
D7:  10-25%
D30: 5-15%

## Gaming (Mobile games)
D1:  40-60%
D7:  20-40%
D30: 10-20%

## Fintech (Banking, Investment apps)
D1:  60-80%
D7:  50-70%
D30: 40-60%

Note: Wide variance based on product category and quality
```

### "Good" Retention Thresholds

```markdown
## General Guidelines
D1 retention:
• >70% = Excellent
• 50-70% = Good
• 30-50% = Average
• <30% = Poor

D30 retention:
• >40% = Excellent (strong PMF)
• 25-40% = Good
• 15-25% = Average
• <15% = Poor (PMF questionable)

Retention curve shape:
• Flattens by D30-60 = Good (found core users)
• Continuous decline = Bad (no engaged user base)
```

---

## Analyzing Retention

### Cohort Comparison

```markdown
## Question: Did new feature improve retention?

Analysis:
| Cohort       | Feature | D30 Retention |
|--------------|---------|---------------|
| Pre-launch   | No      | 18%           |
| Post-launch  | Yes     | 25%           |

Result: +7pp improvement!

## Question: Which channel has best retention?

Analysis:
| Channel      | D30 Retention |
|--------------|---------------|
| Organic      | 35%           |
| Paid ads     | 20%           |
| Referrals    | 50%           |

Insight: Referrals >> Organic >> Paid
Action: Invest in referral program
```

### Segmentation

```markdown
Break cohorts into segments:

By user properties:
• Geography: US vs EU vs Asia
• Plan: Free vs Pro vs Enterprise
• Company size: SMB vs Mid-market vs Enterprise

By behavior:
• Activated vs Not activated
• Used Feature X vs Didn't use
• Invited teammates vs Solo user

Example:
| Segment              | D30 Retention |
|----------------------|---------------|
| Invited teammates    | 60%           |
| Didn't invite        | 15%           |

Insight: Collaboration = retention driver
Action: Encourage invites during onboarding
```

---

## Improving Retention

### Identify Retention Drivers

```sql
-- SQL: Find behaviors correlated with retention
WITH retained_users AS (
  SELECT DISTINCT user_id
  FROM events
  WHERE event_name = 'session_started'
    AND user_id IN (
      SELECT user_id FROM users
      WHERE created_at >= '2025-01-01'
    )
    AND timestamp >= (
      SELECT created_at + INTERVAL '30 days'
      FROM users u WHERE u.user_id = events.user_id
    )
),
feature_usage AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'invited_teammate' THEN 1 ELSE 0 END) as invited,
    MAX(CASE WHEN event_name = 'created_project' THEN 1 ELSE 0 END) as created_project,
    MAX(CASE WHEN event_name = 'integrated_slack' THEN 1 ELSE 0 END) as integrated
  FROM events
  WHERE event_name IN ('invited_teammate', 'created_project', 'integrated_slack')
  GROUP BY user_id
)
SELECT
  'invited_teammate' as feature,
  SUM(CASE WHEN r.user_id IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as retention_rate
FROM feature_usage f
LEFT JOIN retained_users r ON f.user_id = r.user_id
WHERE f.invited = 1

UNION ALL

SELECT
  'created_project',
  SUM(CASE WHEN r.user_id IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
FROM feature_usage f
LEFT JOIN retained_users r ON f.user_id = r.user_id
WHERE f.created_project = 1

UNION ALL

SELECT
  'integrated_slack',
  SUM(CASE WHEN r.user_id IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
FROM feature_usage f
LEFT JOIN retained_users r ON f.user_id = r.user_id
WHERE f.integrated = 1;

-- Results might show:
-- invited_teammate: 65% retention
-- created_project: 45% retention
-- integrated_slack: 75% retention
-- → Focus on Slack integration!
```

### Activation Impact on Retention

```markdown
## Hypothesis: Faster activation = Better retention

Analysis:
| Time to Activate | Cohort Size | D30 Retention |
|------------------|-------------|---------------|
| < 1 hour         | 2000        | 50%           |
| 1-24 hours       | 3000        | 35%           |
| 24+ hours        | 1500        | 15%           |
| Never activated  | 1000        | 3%            |

Insight: Speed to activation critical
Action: Streamline onboarding, reduce time to first value
```

### Re-engagement Strategies

```markdown
## Email Campaigns
Trigger: User inactive for 7 days
Subject: "We miss you! Here's what's new"
Content: Product updates, tips, social proof

Trigger: User inactive for 30 days
Subject: "Your team is waiting for you"
Content: Team activity, missed messages

## Push Notifications
Trigger: Friend posts update
Message: "Alice shared a new project"

Trigger: Weekly digest
Message: "5 new features this week"

## In-App Messaging
Trigger: Login after 14 days
Message: "Welcome back! Check out these new features"

## Retargeting Ads
Target: Churned users (inactive 60+ days)
Message: "Come back and see what's changed"
Offer: Discount or incentive
```

### Habit Formation

```markdown
## Daily Streaks
Example: Duolingo
• Visual streak counter
• Reminder notifications
• Streak freeze (don't break it!)

Impact: Creates daily habit loop

## Email Digests
Frequency: Daily or weekly
Content: Personalized activity summary
Goal: Pull users back regularly

## Scheduled Notifications
Example: Fitness app
• Morning: "Time for your workout"
• Evening: "Log your meals"

Builds routine around product
```

---

## Churn Analysis

### What is Churn?

```markdown
Churn = When users stop using your product

Churn Rate = (Users lost / Total users at start) × 100%

Example:
Start of month: 1,000 users
End of month: 950 users
Churned: 50 users

Churn rate = 50 / 1,000 = 5%
```

### Churn Calculation Methods

```markdown
## User Churn
Churn Rate = Churned users / Total users

Example: 50 / 1,000 = 5% monthly churn

## Revenue Churn (SaaS)
MRR Churn Rate = Churned MRR / Starting MRR

Example:
Start: $100,000 MRR
Churned: $5,000 MRR
MRR Churn = $5,000 / $100,000 = 5%

## Net Revenue Retention (NRR)
NRR = (Starting MRR + Expansion - Churn) / Starting MRR

Example:
Starting MRR: $100,000
Expansion (upsells): +$10,000
Churned MRR: -$5,000

NRR = ($100,000 + $10,000 - $5,000) / $100,000 = 105%

NRR > 100% = Growing from existing customers! ✓
```

### Predicting Churn

```markdown
## At-Risk User Signals
• Login frequency dropped 50%
• Haven't used core feature in 14 days
• Support ticket: "How do I cancel?"
• Email open rate declined
• Team size decreased (removed seats)

## Churn Prediction Model
Use ML to score users 0-100 (likelihood to churn)

Features:
• Days since last login
• Feature usage frequency
• Support ticket count
• Payment failed attempts
• Engagement trend (increasing/decreasing)

Output: Churn risk score
→ Proactive outreach to high-risk users
```

### Preventing Churn

```markdown
## Early Intervention
Trigger: User hasn't logged in for 7 days
Action: Email: "Need help getting started?"

Trigger: Usage declining
Action: In-app message: "Having trouble? Talk to us"

## Customer Success
High-value accounts:
• Dedicated customer success manager
• Quarterly business reviews
• Proactive check-ins

## Cancellation Flow
When user clicks "Cancel":
• Survey: "Why are you leaving?"
• Offer alternative: Downgrade vs cancel?
• Retention offer: 50% off for 3 months
• Make it easy to pause (not cancel)

## Win-Back Campaigns
Target: Churned users
Message: "We've improved based on your feedback"
Incentive: Free month, discount, new features
```

---

## Cohort Analysis in Practice

### SQL Queries

```sql
-- Retention cohort table
WITH cohorts AS (
  SELECT
    DATE_TRUNC('week', created_at) as cohort_week,
    user_id
  FROM users
  WHERE created_at >= '2025-01-01'
),
activity AS (
  SELECT
    DATE_TRUNC('week', timestamp) as activity_week,
    user_id
  FROM events
  WHERE event_name = 'session_started'
    AND timestamp >= '2025-01-01'
)
SELECT
  c.cohort_week,
  COUNT(DISTINCT c.user_id) as cohort_size,
  a.activity_week,
  FLOOR((EXTRACT(EPOCH FROM a.activity_week - c.cohort_week) / 604800)) as weeks_since_signup,
  COUNT(DISTINCT a.user_id) as active_users,
  ROUND(100.0 * COUNT(DISTINCT a.user_id) / COUNT(DISTINCT c.user_id), 2) as retention_pct
FROM cohorts c
LEFT JOIN activity a ON c.user_id = a.user_id
GROUP BY c.cohort_week, a.activity_week
ORDER BY c.cohort_week, weeks_since_signup;
```

### Python Analysis

```python
import pandas as pd
import numpy as np

# Load data
users = pd.read_sql("SELECT user_id, created_at FROM users", conn)
events = pd.read_sql("SELECT user_id, timestamp FROM events WHERE event_name = 'session_started'", conn)

# Create cohorts
users['cohort'] = users['created_at'].dt.to_period('M')

# Calculate retention
retention = []
for cohort in users['cohort'].unique():
    cohort_users = users[users['cohort'] == cohort]['user_id']
    cohort_size = len(cohort_users)

    for period in range(0, 12):  # 12 months
        target_month = cohort + period
        active_users = events[
            (events['user_id'].isin(cohort_users)) &
            (events['timestamp'].dt.to_period('M') == target_month)
        ]['user_id'].nunique()

        retention.append({
            'cohort': cohort,
            'period': period,
            'active_users': active_users,
            'cohort_size': cohort_size,
            'retention_pct': 100 * active_users / cohort_size
        })

retention_df = pd.DataFrame(retention)

# Pivot for heatmap
retention_pivot = retention_df.pivot(
    index='cohort',
    columns='period',
    values='retention_pct'
)

print(retention_pivot)
```

---

## 2025 Trends

### 1. Predictive Cohort Analytics

```markdown
• ML-powered churn prediction
• Automated cohort discovery
• Real-time retention scoring
• AI-generated insights
```

### 2. Product-Led Growth (PLG) Focus

```markdown
• Self-serve onboarding
• In-product activation
• Usage-based pricing
• Bottom-up adoption (user → team → enterprise)

Retention is THE metric for PLG companies
```

### 3. Privacy-First Cohort Analysis

```markdown
• Cookieless tracking
• Aggregated cohorts (privacy preserving)
• Differential privacy
• First-party data focus
```

### 4. Real-Time Cohort Monitoring

```markdown
• Sub-second cohort updates
• Live retention dashboards
• Instant alerts on retention drops
• Stream processing (Kafka, Flink)
```

---

## Tools

### Cohort Analysis Platforms

| Tool | Best For | Key Feature |
|------|----------|-------------|
| **Amplitude** | Product teams | Behavioral cohorts |
| **Mixpanel** | Product analytics | Retention reports |
| **PostHog** | Engineers | SQL-based cohorts |
| **Heap** | Retroactive analysis | Auto-capture |
| **Google Analytics 4** | Content sites | Cohort explorer |

---

## Checklist

```markdown
## Setup
- [ ] Define what "active" means (core action)
- [ ] Choose retention metric (Day 1, 7, 30)
- [ ] Set up event tracking
- [ ] Build cohort table/dashboard
- [ ] Establish baseline retention

## Analysis
- [ ] Monitor retention trends over time
- [ ] Compare cohorts (time, channel, behavior)
- [ ] Identify retention drivers (behavioral analysis)
- [ ] Segment high vs low retention users
- [ ] Calculate churn rate

## Action
- [ ] Optimize onboarding (activation)
- [ ] Build re-engagement campaigns
- [ ] Test retention improvements (A/B test)
- [ ] Implement churn prevention
- [ ] Measure impact of changes on retention
```
