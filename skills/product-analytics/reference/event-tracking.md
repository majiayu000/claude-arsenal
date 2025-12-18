# Event Tracking & Data Modeling

## Overview

Event tracking is the foundation of product analytics. Every user interaction becomes a structured data point that can be queried, analyzed, and acted upon.

**2025 Best Practice:** Start with your metrics, then work backward to the events you need. Don't track everything—track what matters.

---

## Event-Based Analytics

### What is Event-Based Analytics?

Event-based analytics tracks **discrete user actions** (events) rather than just pageviews. Each event captures:

- **What** happened (event name)
- **Who** did it (user ID)
- **When** it happened (timestamp)
- **Where** it happened (page, feature)
- **How** it happened (properties, context)

### Event vs. Pageview Tracking

```markdown
## Pageview-Only Tracking (Old Approach)
❌ User visited /pricing page → pageview count
   • Can't tell if they compared plans
   • Can't tell which plan they viewed
   • Can't correlate with conversion

## Event-Based Tracking (Modern Approach)
✓ User viewed pricing page → pricing_page_viewed
✓ User toggled plan comparison → plans_compared
✓ User clicked "Start Trial" → trial_started
   • Full user journey captured
   • Behavior patterns clear
   • Conversion attribution accurate
```

---

## Event Taxonomy

### Event Naming Standards

**Pattern:** `object_action`

```
Objects: user, project, file, payment, message, etc.
Actions: created, updated, deleted, viewed, clicked, shared, etc.

Examples:
✓ user_signed_up
✓ project_created
✓ file_uploaded
✓ payment_completed
✓ message_sent
✓ search_performed
```

### Naming Conventions

```yaml
Format: snake_case (recommended)
  user_signed_up, checkout_completed

Alternative: camelCase
  userSignedUp, checkoutCompleted

Alternative: Period-separated
  user.signed_up, checkout.completed

AVOID:
  ✗ Mixed case: User_SignedUp
  ✗ Spaces: "User Signed Up"
  ✗ Too vague: "click", "action"
  ✗ Too technical: "post_api_users_create_200"
```

### Event Categories

```markdown
## User Lifecycle Events
user_signed_up          → Registration complete
user_activated          → Completed first key action
user_invited_teammate   → Sent invitation
user_upgraded           → Changed to paid plan
user_downgraded         → Reduced plan
user_churned            → Canceled or became inactive

## Feature Interaction Events
feature_viewed          → User saw the feature
feature_enabled         → User turned on feature
feature_used            → User interacted with feature
feature_completed       → User finished feature workflow

## Content Events
content_created         → Post, file, project created
content_viewed          → Item viewed
content_edited          → Item updated
content_deleted         → Item removed
content_shared          → Shared with others
content_published       → Made public

## Commerce Events
product_viewed          → Product page viewed
product_added_to_cart   → Added to cart
cart_viewed             → Cart page opened
checkout_started        → Began checkout
payment_attempted       → Tried to pay
payment_completed       → Payment successful
payment_failed          → Payment error
order_shipped           → Fulfillment started
order_delivered         → Fulfillment complete

## Engagement Events
session_started         → User logged in
session_ended           → User logged out
page_viewed             → Page navigation
search_performed        → Search query
filter_applied          → Applied filter
notification_received   → Push/email received
notification_clicked    → Opened notification

## Social Events
user_followed           → Followed another user
message_sent            → Direct message
comment_posted          → Commented on content
like_added              → Liked content
share_completed         → Shared to social

## Error Events
error_occurred          → Application error
form_validation_failed  → Invalid input
api_request_failed      → Backend error
timeout_occurred        → Request timeout
```

---

## Event Properties

### Property Schema

```javascript
// Event structure
{
  event: "checkout_completed",
  timestamp: "2025-12-16T10:30:00.123Z",
  user_id: "usr_7b3f8e2a",
  session_id: "ses_4c9d1a5e",

  // Event-specific properties
  properties: {
    order_id: "ord_123456",
    total_amount: 149.99,
    currency: "USD",
    item_count: 3,
    payment_method: "credit_card",
    shipping_method: "express",
    coupon_code: "SAVE20",
    discount_amount: 30.00,
    tax_amount: 12.00,
    items: [
      { sku: "PROD-001", quantity: 2, price: 49.99 },
      { sku: "PROD-002", quantity: 1, price: 50.01 }
    ]
  },

  // Global context
  context: {
    app_version: "2.4.1",
    platform: "web",
    os: "macOS",
    browser: "Chrome",
    screen_size: "1920x1080",
    locale: "en-US",
    timezone: "America/New_York",
    utm_source: "google",
    utm_medium: "cpc",
    utm_campaign: "holiday_sale"
  }
}
```

### Property Naming

```yaml
snake_case preferred:
  total_amount, user_id, created_at

Data types:
  Strings:    "pro", "credit_card", "monthly"
  Numbers:    99.99, 5, 1000
  Booleans:   true, false
  Timestamps: "2025-12-16T10:30:00.123Z" (ISO 8601)
  Arrays:     ["tag1", "tag2"]
  Objects:    { plan: "pro", price: 29.99 }

AVOID:
  ✗ Inconsistent naming: totalAmount vs total_amount
  ✗ String numbers: "99.99" (use 99.99)
  ✗ Ambiguous booleans: "yes", "1", "Y" (use true/false)
  ✗ Non-standard dates: "12/16/2025" (use ISO 8601)
```

### Required vs. Optional Properties

```javascript
// Required for ALL events
{
  event: string,          // Event name
  timestamp: string,      // ISO 8601
  user_id: string,        // User identifier (or anonymous_id)
}

// Recommended for context
{
  session_id: string,     // Session tracking
  app_version: string,    // Version tracking
  platform: string,       // "web", "ios", "android"
}

// Event-specific (varies by event)
{
  properties: {
    // Whatever makes sense for this event
  }
}
```

---

## Tracking Plan

### What is a Tracking Plan?

A **tracking plan** is a living document that defines:

1. **What events to track** (event catalog)
2. **What properties each event has** (schema)
3. **Where events are triggered** (implementation location)
4. **Why we track them** (business purpose)

### Benefits

```
✓ Single source of truth for analytics
✓ Consistent naming across teams
✓ Clear implementation specs for engineers
✓ Data quality and governance
✓ Easier debugging and validation
```

### Tracking Plan Structure

```markdown
## Event: checkout_completed

**Category:** Commerce
**Description:** Triggered when user successfully completes payment

**When to trigger:**
- After payment processor confirms success
- Before order confirmation page loads

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| order_id | string | Yes | Unique order identifier | "ord_123456" |
| total_amount | number | Yes | Order total in dollars | 149.99 |
| currency | string | Yes | ISO currency code | "USD" |
| item_count | number | Yes | Number of items | 3 |
| payment_method | string | Yes | Payment type | "credit_card" |
| discount_amount | number | No | Discount applied | 30.00 |
| coupon_code | string | No | Coupon used | "SAVE20" |

**Implementation:**
- Platform: Web, iOS, Android
- Triggered by: `PaymentService.processPayment()` success callback
- Code location: `src/services/payment.ts`

**Related events:**
- checkout_started (precedes)
- order_shipped (follows)

**Metrics using this event:**
- Revenue metrics
- Conversion rate
- Average order value
```

---

## Event Implementation

### Client-Side vs. Server-Side Tracking

```markdown
## Client-Side (Browser/App)
✓ Rich user context (device, browser, screen size)
✓ User interactions (clicks, scrolls, form fills)
✓ Real-time behavior tracking
✗ Can be blocked by ad blockers
✗ Unreliable for critical business events
✗ Privacy concerns (cookies, fingerprinting)

## Server-Side (Backend)
✓ Reliable (no ad blockers)
✓ Secure (no client manipulation)
✓ Critical business events (payments, conversions)
✓ Privacy-friendly (no cookies)
✗ Less user context
✗ Can't track client-side interactions directly

## Best Practice: Hybrid Approach
- Client-side: UI interactions, engagement, behavior
- Server-side: Transactions, conversions, critical actions
- Validate critical events on both sides
```

### Implementation Examples

#### JavaScript (Web)

```javascript
// Using Amplitude
amplitude.track('checkout_completed', {
  order_id: 'ord_123456',
  total_amount: 149.99,
  currency: 'USD',
  item_count: 3,
  payment_method: 'credit_card'
});

// Using Mixpanel
mixpanel.track('checkout_completed', {
  order_id: 'ord_123456',
  total_amount: 149.99,
  currency: 'USD',
  item_count: 3,
  payment_method: 'credit_card'
});

// Using Segment (works with many destinations)
analytics.track('checkout_completed', {
  order_id: 'ord_123456',
  total_amount: 149.99,
  currency: 'USD',
  item_count: 3,
  payment_method: 'credit_card'
});

// Custom implementation
function track(event, properties = {}) {
  const payload = {
    event,
    timestamp: new Date().toISOString(),
    user_id: getCurrentUserId(),
    session_id: getSessionId(),
    properties,
    context: {
      app_version: APP_VERSION,
      platform: 'web',
      url: window.location.href,
      referrer: document.referrer,
      user_agent: navigator.userAgent,
      screen_size: `${window.screen.width}x${window.screen.height}`
    }
  };

  // Send to analytics service
  fetch('/api/analytics/events', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
}
```

#### Python (Server-Side)

```python
from amplitude import Amplitude

# Initialize client
client = Amplitude(api_key='your_api_key')

# Track event
client.track({
    'event_type': 'checkout_completed',
    'user_id': 'usr_123',
    'event_properties': {
        'order_id': 'ord_123456',
        'total_amount': 149.99,
        'currency': 'USD',
        'item_count': 3,
        'payment_method': 'credit_card'
    },
    'time': int(time.time() * 1000)  # Unix timestamp in ms
})

# Using Mixpanel
from mixpanel import Mixpanel

mp = Mixpanel('your_token')
mp.track('usr_123', 'checkout_completed', {
    'order_id': 'ord_123456',
    'total_amount': 149.99,
    'currency': 'USD',
    'item_count': 3,
    'payment_method': 'credit_card'
})
```

#### React (Component Tracking)

```javascript
import { useEffect } from 'react';
import { track } from '@/lib/analytics';

function CheckoutPage() {
  // Track page view
  useEffect(() => {
    track('checkout_page_viewed', {
      step: 'payment'
    });
  }, []);

  // Track button click
  const handleSubmit = async (formData) => {
    track('checkout_submitted', {
      payment_method: formData.paymentMethod
    });

    try {
      const result = await processPayment(formData);

      // Track success
      track('checkout_completed', {
        order_id: result.orderId,
        total_amount: result.total,
        currency: 'USD',
        item_count: cart.items.length,
        payment_method: formData.paymentMethod
      });

    } catch (error) {
      // Track failure
      track('checkout_failed', {
        error_message: error.message,
        payment_method: formData.paymentMethod
      });
    }
  };

  return <CheckoutForm onSubmit={handleSubmit} />;
}
```

---

## Data Modeling

### Event Schema Design

```sql
-- Events table (fact table)
CREATE TABLE events (
  id BIGSERIAL PRIMARY KEY,
  event_name VARCHAR(255) NOT NULL,
  user_id VARCHAR(255),
  anonymous_id VARCHAR(255),
  session_id VARCHAR(255),
  timestamp TIMESTAMPTZ NOT NULL,
  properties JSONB,
  context JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_timestamp ON events(timestamp DESC);
CREATE INDEX idx_events_name_timestamp ON events(event_name, timestamp DESC);
CREATE INDEX idx_events_properties ON events USING GIN(properties);
```

### User Properties (Dimension Table)

```sql
-- Users table (dimension table)
CREATE TABLE users (
  user_id VARCHAR(255) PRIMARY KEY,
  email VARCHAR(255),
  created_at TIMESTAMPTZ,
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  plan VARCHAR(50),
  mrr DECIMAL(10,2),
  ltv DECIMAL(10,2),

  -- Computed properties
  first_seen_at TIMESTAMPTZ,
  last_seen_at TIMESTAMPTZ,
  total_sessions INT,
  total_events INT,

  -- Segmentation
  cohort_month VARCHAR(7),  -- '2025-12'
  acquisition_channel VARCHAR(100),

  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Common Queries

```sql
-- Daily active users
SELECT
  DATE(timestamp) as date,
  COUNT(DISTINCT user_id) as dau
FROM events
WHERE timestamp >= NOW() - INTERVAL '30 days'
GROUP BY DATE(timestamp)
ORDER BY date;

-- Event funnel
WITH funnel AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'page_viewed' THEN 1 ELSE 0 END) as viewed,
    MAX(CASE WHEN event_name = 'signup_started' THEN 1 ELSE 0 END) as started,
    MAX(CASE WHEN event_name = 'signup_completed' THEN 1 ELSE 0 END) as completed
  FROM events
  WHERE timestamp >= '2025-12-01'
  GROUP BY user_id
)
SELECT
  SUM(viewed) as step1_viewed,
  SUM(started) as step2_started,
  SUM(completed) as step3_completed,
  ROUND(100.0 * SUM(started) / NULLIF(SUM(viewed), 0), 2) as view_to_start_rate,
  ROUND(100.0 * SUM(completed) / NULLIF(SUM(started), 0), 2) as start_to_complete_rate
FROM funnel;

-- Top events by user
SELECT
  event_name,
  COUNT(*) as event_count,
  COUNT(DISTINCT user_id) as unique_users,
  ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT user_id), 2) as avg_per_user
FROM events
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY event_name
ORDER BY event_count DESC
LIMIT 20;
```

---

## Data Quality

### Validation & Testing

```javascript
// Event validation schema (using Zod)
import { z } from 'zod';

const CheckoutCompletedSchema = z.object({
  event: z.literal('checkout_completed'),
  timestamp: z.string().datetime(),
  user_id: z.string().min(1),
  properties: z.object({
    order_id: z.string().min(1),
    total_amount: z.number().positive(),
    currency: z.enum(['USD', 'EUR', 'GBP']),
    item_count: z.number().int().positive(),
    payment_method: z.enum(['credit_card', 'paypal', 'apple_pay'])
  })
});

// Use in tracking
function trackCheckoutCompleted(data) {
  try {
    const validated = CheckoutCompletedSchema.parse(data);
    sendToAnalytics(validated);
  } catch (error) {
    console.error('Invalid event data:', error);
    // Send to error monitoring
  }
}
```

### Common Data Issues

```markdown
## Issue 1: Duplicate Events
Problem: Same event sent multiple times
Cause: Retry logic, double-clicks, network issues
Solution: Use idempotency keys, debounce client events

## Issue 2: Missing Properties
Problem: Events sent without required properties
Cause: Code bugs, schema changes, null values
Solution: Schema validation, required fields, tests

## Issue 3: Inconsistent Naming
Problem: "user_signup" vs "userSignup" vs "User Signed Up"
Cause: Multiple developers, no standards
Solution: Tracking plan, linting, code review

## Issue 4: Wrong Data Types
Problem: "99.99" (string) instead of 99.99 (number)
Cause: Type coercion, API inconsistencies
Solution: TypeScript, validation, testing

## Issue 5: PII in Events
Problem: Email, password, credit card in properties
Cause: Developer error, overly broad logging
Solution: PII scanning, masking, training
```

---

## Privacy & Compliance

### GDPR & CCPA Compliance

```markdown
## User Rights
1. Right to access: Provide all data for user_id
2. Right to deletion: Delete all events for user_id
3. Right to portability: Export user data
4. Right to opt-out: Stop tracking

## Implementation
- Hash or pseudonymize user_id
- Don't track PII in event properties
- Implement data deletion endpoints
- Provide opt-out mechanisms
- Document retention policies
```

### PII Masking

```javascript
// PII detection and masking
const maskEmail = (email) => {
  const [name, domain] = email.split('@');
  return `${name[0]}***@${domain}`;
};

const maskPhone = (phone) => `****${phone.slice(-4)}`;

const maskCreditCard = (card) => `****${card.slice(-4)}`;

// Sanitize event properties
function sanitizeProperties(properties) {
  const sanitized = { ...properties };

  // Remove known PII fields
  delete sanitized.email;
  delete sanitized.password;
  delete sanitized.credit_card;
  delete sanitized.ssn;

  // Mask if needed
  if (properties.email) {
    sanitized.email_domain = properties.email.split('@')[1];
  }

  if (properties.credit_card) {
    sanitized.card_last_4 = properties.credit_card.slice(-4);
    sanitized.card_type = detectCardType(properties.credit_card);
  }

  return sanitized;
}
```

---

## 2025 Trends

### 1. AI-Powered Analytics

```markdown
- Automated anomaly detection
- Predictive churn modeling
- Natural language queries ("Show me users who churned last month")
- Auto-generated insights
```

### 2. Privacy-First Tracking

```markdown
- Server-side tracking dominance
- Cookieless tracking
- Differential privacy
- On-device analytics (iOS, Android)
```

### 3. Real-Time Analytics

```markdown
- Stream processing (Kafka, Flink)
- Sub-second dashboards
- Real-time personalization
- Instant A/B test results
```

### 4. Warehouse-Native Analytics

```markdown
- Analytics tools run on your data warehouse
- No data copying (Snowflake, BigQuery, Databricks)
- SQL-based analysis
- Unified data model
```

---

## Tools Comparison

| Tool | Best For | Pricing Model | Key Feature |
|------|----------|---------------|-------------|
| **Amplitude** | Product teams, B2C | Event-based | Behavioral cohorts |
| **Mixpanel** | Product analytics | Event-based | Real-time dashboards |
| **PostHog** | Engineers, privacy | Self-hosted/cloud | Open source, full suite |
| **Segment** | Data infrastructure | MTU-based | CDP + integrations |
| **Google Analytics 4** | Content sites | Free | Universal, free tier |
| **Heap** | Auto-capture | Session-based | Retroactive analysis |

---

## Checklist

```markdown
## Tracking Plan
- [ ] Event naming convention documented
- [ ] All events cataloged with descriptions
- [ ] Property schemas defined
- [ ] Implementation locations specified
- [ ] Privacy review completed

## Implementation
- [ ] Analytics library integrated
- [ ] Critical events tracked server-side
- [ ] Event validation in place
- [ ] Error handling for failed sends
- [ ] Testing coverage for tracking code

## Data Quality
- [ ] Schema validation active
- [ ] Duplicate detection implemented
- [ ] PII masking in place
- [ ] Data retention policy defined
- [ ] Regular data quality audits

## Privacy
- [ ] GDPR/CCPA compliance reviewed
- [ ] User opt-out mechanism
- [ ] Data deletion process
- [ ] Privacy policy updated
- [ ] Team trained on PII handling
```
