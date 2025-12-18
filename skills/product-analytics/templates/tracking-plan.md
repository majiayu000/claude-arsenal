# Event Tracking Plan Template

## Overview

**Product:** [Product Name]
**Last Updated:** [Date]
**Owner:** [Product Manager / Team]
**Version:** [1.0]

---

## Purpose

This tracking plan documents all analytics events tracked in [Product Name]. It serves as the single source of truth for:
- Event definitions and naming conventions
- Property schemas and data types
- Implementation locations
- Business purpose and usage

---

## Naming Conventions

### Event Naming

```
Pattern: object_action (snake_case)

Examples:
✓ user_signed_up
✓ project_created
✓ file_uploaded
✓ payment_completed

Format Rules:
• snake_case (lowercase, underscores)
• Past tense for completed actions
• Present tense for ongoing states
• Descriptive and specific
```

### Property Naming

```
Format: snake_case

Data Types:
• Strings: "value"
• Numbers: 123, 45.67
• Booleans: true, false
• Timestamps: ISO 8601 ("2025-12-16T10:30:00Z")
• Arrays: ["item1", "item2"]
• Objects: { key: "value" }
```

---

## Global Properties

These properties are included in **every event**:

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `event` | string | Yes | Event name | "user_signed_up" |
| `timestamp` | string | Yes | ISO 8601 timestamp | "2025-12-16T10:30:00.123Z" |
| `user_id` | string | Yes* | Unique user identifier | "usr_7b3f8e2a" |
| `anonymous_id` | string | Yes* | Anonymous identifier (pre-login) | "anon_4c9d1a5e" |
| `session_id` | string | Yes | Session identifier | "ses_9f2e3a1c" |

*Either `user_id` OR `anonymous_id` required

### Context Properties (Recommended)

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `app_version` | string | Application version | "2.4.1" |
| `platform` | string | Platform type | "web", "ios", "android" |
| `os` | string | Operating system | "macOS", "Windows", "iOS" |
| `browser` | string | Browser name | "Chrome", "Safari", "Firefox" |
| `screen_size` | string | Screen resolution | "1920x1080" |
| `locale` | string | User locale | "en-US", "es-ES" |
| `timezone` | string | User timezone | "America/New_York" |

### UTM Parameters (Marketing)

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `utm_source` | string | Traffic source | "google", "facebook" |
| `utm_medium` | string | Marketing medium | "cpc", "email", "social" |
| `utm_campaign` | string | Campaign name | "holiday_sale_2025" |
| `utm_term` | string | Paid keyword | "project management tool" |
| `utm_content` | string | Ad variant | "banner_a" |

---

## Event Catalog

### User Lifecycle Events

#### user_signed_up

**Description:** Triggered when user completes registration

**When to trigger:**
- After successful account creation
- Before redirect to onboarding

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `signup_method` | string | Yes | How user signed up | "email", "google", "github" |
| `plan` | string | Yes | Initial plan type | "free", "trial", "pro" |
| `referral_code` | string | No | Referral code used | "FRIEND20" |
| `trial_days` | number | No | Trial period length | 14 |

**Implementation:**
- **Platform:** Web, iOS, Android
- **Trigger:** `AuthService.createAccount()` success callback
- **Location:** `src/services/auth.ts` (line 145)

**Related Events:**
- `signup_started` (precedes)
- `user_activated` (follows)

**Used in Metrics:**
- Acquisition metrics
- Sign-up conversion rate
- Channel performance

**Example:**
```json
{
  "event": "user_signed_up",
  "timestamp": "2025-12-16T10:30:00.123Z",
  "user_id": "usr_7b3f8e2a",
  "properties": {
    "signup_method": "google",
    "plan": "trial",
    "trial_days": 14
  }
}
```

---

#### user_activated

**Description:** User completed first key action (activation milestone)

**When to trigger:**
- When user completes activation action
- Definition: Created first project OR invited first teammate

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `activation_action` | string | Yes | What action activated user | "project_created", "teammate_invited" |
| `time_to_activation_hours` | number | Yes | Hours from signup to activation | 2.5 |
| `onboarding_completed` | boolean | Yes | Completed onboarding flow? | true |

**Implementation:**
- **Platform:** Web, iOS, Android
- **Trigger:** First occurrence of activation action
- **Location:** `src/lib/analytics/activation.ts`

**Related Events:**
- `user_signed_up` (precedes)
- `project_created` OR `teammate_invited` (triggers this)

**Used in Metrics:**
- Activation rate
- Time to activation
- Onboarding conversion

---

### Feature Interaction Events

#### project_created

**Description:** User created a new project

**When to trigger:**
- After project successfully saved to database
- Before showing success message

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `project_id` | string | Yes | Unique project identifier | "prj_abc123" |
| `project_name` | string | No | Project name (masked PII) | First 20 chars only |
| `template_used` | string | No | Template used | "blank", "marketing", "engineering" |
| `is_first_project` | boolean | Yes | User's first project? | true |
| `team_id` | string | No | Team identifier (if team project) | "team_xyz789" |

**Implementation:**
- **Platform:** Web, iOS, Android
- **Trigger:** `ProjectService.create()` success
- **Location:** `src/services/projects.ts`

**Related Events:**
- `project_updated`
- `project_deleted`
- `user_activated` (may trigger)

**Used in Metrics:**
- Feature adoption
- Activation rate
- User engagement

---

#### file_uploaded

**Description:** User uploaded a file to project

**When to trigger:**
- After file upload completes
- Before showing in UI

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `file_id` | string | Yes | Unique file identifier | "file_def456" |
| `file_size_bytes` | number | Yes | File size in bytes | 2048576 |
| `file_type` | string | Yes | MIME type | "image/png", "application/pdf" |
| `project_id` | string | Yes | Project file uploaded to | "prj_abc123" |
| `upload_method` | string | Yes | Upload method | "drag_drop", "button", "paste" |
| `upload_duration_ms` | number | Yes | Time to upload | 1250 |

**Implementation:**
- **Platform:** Web, iOS, Android
- **Trigger:** `FileService.upload()` complete
- **Location:** `src/services/files.ts`

---

### Commerce Events

#### checkout_completed

**Description:** User successfully completed payment

**When to trigger:**
- After payment processor confirms success
- Before order confirmation page

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `order_id` | string | Yes | Unique order identifier | "ord_123456" |
| `total_amount` | number | Yes | Total in dollars | 149.99 |
| `currency` | string | Yes | ISO currency code | "USD" |
| `item_count` | number | Yes | Number of items | 3 |
| `payment_method` | string | Yes | Payment type | "credit_card", "paypal" |
| `plan` | string | Yes | Subscription plan | "pro", "enterprise" |
| `billing_cycle` | string | Yes | Billing frequency | "monthly", "annual" |
| `coupon_code` | string | No | Discount code used | "SAVE20" |
| `discount_amount` | number | No | Discount applied | 30.00 |
| `tax_amount` | number | No | Tax charged | 12.00 |

**Implementation:**
- **Platform:** Web (server-side)
- **Trigger:** `PaymentService.processPayment()` webhook
- **Location:** `src/api/webhooks/stripe.ts`

**Related Events:**
- `checkout_started` (precedes)
- `subscription_started` (follows)

**Used in Metrics:**
- Revenue (MRR, ARR)
- Conversion to paid
- Average order value

---

### Engagement Events

#### session_started

**Description:** User started a new session

**When to trigger:**
- On page load (web)
- On app launch (mobile)
- After 30 minutes of inactivity

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `session_id` | string | Yes | Session identifier | "ses_9f2e3a1c" |
| `session_count` | number | Yes | User's total session count | 42 |
| `days_since_signup` | number | Yes | Days since registration | 15 |
| `referrer` | string | No | Referrer URL | "https://google.com" |
| `landing_page` | string | Yes | Entry page | "/pricing" |

**Implementation:**
- **Platform:** Web, iOS, Android
- **Trigger:** Session initialization
- **Location:** `src/lib/analytics/session.ts`

**Used in Metrics:**
- Daily/Monthly Active Users
- Session frequency
- Retention

---

#### page_viewed

**Description:** User viewed a page

**When to trigger:**
- On page load (SPA route change)
- Only for significant pages (not every scroll)

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `page_path` | string | Yes | Page path (no query params) | "/dashboard" |
| `page_title` | string | Yes | Page title | "Dashboard - MyApp" |
| `referrer` | string | No | Previous page | "/projects" |
| `load_time_ms` | number | No | Page load time | 850 |

**Implementation:**
- **Platform:** Web
- **Trigger:** React Router navigation
- **Location:** `src/App.tsx` (route change listener)

---

### Error Events

#### error_occurred

**Description:** Application error occurred

**When to trigger:**
- On caught exceptions
- On API errors (4xx, 5xx)
- On validation failures

**Properties:**

| Property | Type | Required | Description | Example |
|----------|------|----------|-------------|---------|
| `error_type` | string | Yes | Error category | "api_error", "validation", "network" |
| `error_code` | string | No | Error code | "ERR_PAYMENT_FAILED" |
| `error_message` | string | Yes | Error description (sanitized) | "Payment declined" |
| `status_code` | number | No | HTTP status code | 500 |
| `endpoint` | string | No | API endpoint (if API error) | "/api/v1/projects" |
| `page_path` | string | Yes | Where error occurred | "/checkout" |

**Implementation:**
- **Platform:** Web, iOS, Android
- **Trigger:** Error boundary, catch blocks
- **Location:** `src/lib/analytics/errors.ts`

**Used in Metrics:**
- Error rate
- Reliability metrics
- User friction points

---

## Implementation Checklist

### Before Launch
- [ ] Event naming conventions documented
- [ ] All events reviewed by engineering
- [ ] Privacy review completed (no PII)
- [ ] Analytics SDK integrated
- [ ] Event validation implemented

### After Launch
- [ ] Events firing correctly (QA testing)
- [ ] Dashboards created
- [ ] No duplicate events
- [ ] Sample ratio correct (50/50 splits)
- [ ] Data quality monitoring active

### Ongoing
- [ ] Monthly tracking plan review
- [ ] Update for new features
- [ ] Deprecate unused events
- [ ] Validate data quality
- [ ] Document schema changes

---

## Privacy & Compliance

### PII Policy

**Never track:**
- Passwords
- Credit card numbers
- Social Security Numbers
- Full email addresses (hash or mask)
- Phone numbers (mask)
- Private keys, API tokens

**Masking Examples:**
```javascript
// Email: user@example.com → u***r@example.com
const maskEmail = (email) => {
  const [name, domain] = email.split('@');
  return `${name[0]}***${name[name.length - 1]}@${domain}`;
};

// Phone: 555-123-4567 → ****4567
const maskPhone = (phone) => `****${phone.slice(-4)}`;

// Credit card: 4242424242424242 → ****4242
const maskCard = (card) => `****${card.slice(-4)}`;
```

### GDPR/CCPA Compliance

- [ ] User consent obtained before tracking
- [ ] Opt-out mechanism available
- [ ] Data deletion process documented
- [ ] Data retention policy defined (365 days)
- [ ] User data export capability

---

## Testing

### Event Validation

```javascript
// Example: Zod schema for event validation
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
    payment_method: z.enum(['credit_card', 'paypal', 'apple_pay']),
    plan: z.string().min(1),
    billing_cycle: z.enum(['monthly', 'annual']),
    coupon_code: z.string().optional(),
    discount_amount: z.number().nonnegative().optional(),
    tax_amount: z.number().nonnegative().optional()
  })
});

// Use in code
function trackCheckoutCompleted(data) {
  const validated = CheckoutCompletedSchema.parse(data);
  sendToAnalytics(validated);
}
```

### QA Checklist

**For each event:**
- [ ] Event fires at correct time
- [ ] All required properties present
- [ ] Data types correct
- [ ] No PII in properties
- [ ] Consistent naming (snake_case)
- [ ] Appears in analytics tool
- [ ] Associated with correct user_id

---

## Analytics Tools

### Primary Platform
- **Tool:** [Amplitude / Mixpanel / PostHog]
- **Environment:** Production
- **API Key:** [Stored in env vars]

### Data Warehouse
- **Destination:** [Snowflake / BigQuery]
- **Pipeline:** [Segment / Fivetran]
- **Sync Frequency:** Real-time

### Dashboards
- **Product Metrics:** [Link to dashboard]
- **Growth Metrics:** [Link to dashboard]
- **Revenue Metrics:** [Link to dashboard]

---

## Changelog

### Version 1.0 (2025-12-16)
- Initial tracking plan
- Defined 15 core events
- Established naming conventions
- Privacy policy documented

### Future Versions
- Document changes here
- Track schema updates
- Note deprecated events

---

## Contact

**Questions or Updates:**
- Product Manager: [name@company.com]
- Engineering Lead: [name@company.com]
- Analytics Team: [analytics@company.com]

**Slack Channel:** #product-analytics
