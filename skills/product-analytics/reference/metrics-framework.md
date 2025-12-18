# Metrics Framework: North Star, AARRR & Key Metrics

## Overview

This guide covers the complete metrics framework for product analytics, including how to select, define, and track the right metrics for your product.

---

## North Star Metric Framework

### What is a North Star Metric?

The **North Star Metric (NSM)** is the single metric that best captures the core value your product delivers to customers. When your NSM grows sustainably, your business grows.

Created by Amplitude's Sean Ellis and popularized in the growth hacking community, the NSM provides:
- Single point of alignment across teams
- Clear measure of product value delivery
- Leading indicator of business success

### Characteristics of a Good NSM

```markdown
✓ Expresses value delivered to customers
✓ Represents vision and strategy
✓ Predicts long-term success
✓ Measurable and actionable
✓ Not a vanity metric
✓ Hard to game or manipulate
```

### NSM vs. Other Metrics

```markdown
## North Star Metric
• Spotify: Time Spent Listening
  → Captures engagement with core value (music)

## NOT North Star (Supporting Metrics)
• Sign-ups → Acquisition metric
• Revenue → Lagging indicator
• App downloads → Vanity metric
• Page views → Activity, not value

The NSM bridges user value and business outcomes.
```

### Real-World Examples

| Company | North Star Metric | Why It Works | Supporting Inputs |
|---------|------------------|--------------|-------------------|
| **Airbnb** | Nights Booked | Direct revenue + value delivered | Listings created, searches, bookings |
| **Spotify** | Time Spent Listening | Engagement = satisfaction | Daily actives, playlists, songs added |
| **Slack** | Daily Messages Sent | Team collaboration = core value | Teams created, members invited, integrations |
| **Facebook** | Monthly Active Users | Network effect foundation | Daily actives, posts, connections |
| **Amplitude** | Weekly Learning Users | Analytics insights = value | Queries run, charts created, shares |
| **Dropbox** | Active Users Sharing Files | Collaboration = growth driver | Files uploaded, shares, comments |
| **Medium** | Total Time Reading | Content consumption = value | Articles read, claps, follows |
| **Uber** | Rides Completed | Transaction = value to both sides | Riders, drivers, cities |
| **LinkedIn** | Weekly Active Users | Professional network engagement | Connections, messages, jobs |
| **Asana** | Tasks Completed | Productivity = core promise | Projects, teams, comments |

### How to Choose Your NSM

```markdown
## Step 1: Define Core Value Proposition
What is the "aha!" moment when users get value?

Examples:
• Slack: "Wow, my team is communicating so much faster!"
• Dropbox: "My files are accessible everywhere!"
• Airbnb: "I found the perfect place to stay!"

## Step 2: Find the Metric That Captures It
What behavior represents this value delivery?

Questions:
• When does the user get value?
• What action demonstrates they got value?
• Can we measure it consistently?

## Step 3: Validate Business Correlation
Does NSM growth → revenue growth?

Test:
• Plot NSM vs. revenue over time
• Look for correlation
• Validate causation (not just correlation)

## Step 4: Define Input Metrics
What drives the NSM?

Break down into 3-5 inputs:
• User actions that lead to NSM
• Metrics teams can directly influence
• Measurable and actionable
```

### NSM Tree Structure

```
           North Star Metric
                  ↓
         Time Spent Listening
                  ↓
    ┌─────────────┴─────────────┬─────────────┐
    ↓                           ↓             ↓
Daily Active    Playlists    Songs Added   Social
  Users          Created      to Library     Shares
    ↓              ↓              ↓            ↓
┌───┴───┐      ┌───┴───┐    ┌────┴────┐   ┌──┴──┐
New    Return  Create  Follow Discovery Rec  Share Collab
Users  Users   Personal List  Mode     Algos Posts Playlists

Each level = actionable for different teams
Bottom level = direct product/eng impact
```

### Common Mistakes

```markdown
❌ Choosing Revenue as NSM
• Revenue is a lagging indicator
• Doesn't capture user value directly
• Use as validation, not NSM

❌ Picking Multiple NSMs
• Defeats the purpose of "North Star"
• Creates conflicting priorities
• Choose ONE, support with inputs

❌ Selecting a Vanity Metric
• Sign-ups look good but don't show value
• Downloads don't equal engagement
• Focus on value delivery, not top-of-funnel

❌ Gaming the Metric
• If NSM = page views, add unnecessary clicks
• If NSM = sessions, force re-logins
• Choose metrics that align incentives

❌ Ignoring Input Metrics
• NSM without inputs = just a dashboard
• Teams need actionable metrics
• Break down into influenceable components
```

---

## AARRR Framework Deep Dive

### Framework Overview

**AARRR (Pirate Metrics)** was created by Dave McClure to track the customer lifecycle:

```
ACQUISITION → ACTIVATION → RETENTION → REFERRAL → REVENUE
```

Each stage has specific metrics, goals, and optimization strategies.

---

### 1. Acquisition

**Definition:** How users discover and arrive at your product.

#### Key Metrics

```markdown
• Traffic sources (organic, paid, referral, social, direct)
• Visitors per channel
• Cost Per Acquisition (CPA) per channel
• Sign-up conversion rate per channel
• Channel ROI = Revenue / Cost
```

#### Acquisition Channels

```markdown
## Organic
• SEO (Google, Bing)
• Content marketing
• Brand search

## Paid
• Google Ads (search, display)
• Facebook/Instagram Ads
• LinkedIn Ads
• Sponsored content

## Referral
• Word of mouth
• Referral programs
• Affiliate marketing

## Social
• Organic social posts
• Influencer marketing
• Community engagement

## Direct
• Direct traffic (bookmarks, typed URL)
• Email marketing
• Retargeting
```

#### Optimization Strategies

```markdown
1. Measure channel quality, not just volume
   → Users from Channel A may have 2x retention vs. Channel B
   → Optimize for LTV, not just CPA

2. Track full funnel per channel
   → Organic: Visit → Sign-up → Activation → Retention
   → Paid: Click → Land → Sign-up → Activation → Retention

3. Calculate channel LTV:CAC
   → LTV:CAC > 3:1 = Good channel
   → < 1:1 = Unsustainable

4. Attribution modeling
   → Last-click: Credit final touchpoint
   → First-click: Credit initial discovery
   → Linear: Equal credit all touchpoints
   → Data-driven: ML-based attribution
```

#### Acquisition Formulas

```
Cost Per Acquisition (CPA)
= Total Marketing Spend / Number of Customers Acquired

Channel Conversion Rate
= (Sign-ups from Channel / Visitors from Channel) × 100%

Channel ROI
= (Revenue from Channel - Cost) / Cost × 100%

Example:
Spent $10,000 on Google Ads
Acquired 200 customers
Average LTV = $300

CPA = $10,000 / 200 = $50
LTV:CAC = $300 / $50 = 6:1 (Excellent!)
```

---

### 2. Activation

**Definition:** When users experience the core value of your product ("aha!" moment).

#### Key Metrics

```markdown
• Activation rate (% users reaching "aha!" moment)
• Time to activation (median time to first value)
• Setup completion rate
• Feature adoption rate
• Tutorial completion rate
```

#### Defining Activation

```markdown
Activation is NOT:
❌ Sign-up completion
❌ Email verification
❌ Profile creation

Activation IS:
✓ First meaningful action
✓ Core value delivered
✓ User gets "aha!" moment

Examples:
• Slack: Team sends 2,000 messages
• Twitter: Follow 30 users
• Dropbox: Upload first file and access from another device
• LinkedIn: Connect with 5 people
• Asana: Create first project and assign tasks
• Figma: Invite teammate and collaborate on design
```

#### Activation Funnel

```markdown
Step 1: Sign-up completed
        ↓ 90% proceed
Step 2: Email verified
        ↓ 70% proceed
Step 3: Profile completed
        ↓ 60% proceed
Step 4: First action (ACTIVATION)
        ↓
Overall activation rate: 90% × 70% × 60% = 38%

Optimization focus: Biggest drop-off = Step 2 → Step 3
```

#### Optimization Strategies

```markdown
1. Shorten time to value
   → Remove unnecessary onboarding steps
   → Pre-populate data where possible
   → Progressive disclosure (show features as needed)

2. Personalize onboarding
   → Role-based flows (developer, marketer, designer)
   → Use case-based setup
   → Show relevant examples

3. Use in-app guidance
   → Interactive tutorials
   → Tooltips and walkthroughs
   → Progress indicators

4. Celebrate activation
   → Confetti animation
   → Achievement unlocked
   → Email: "You did it!"

5. Measure activation cohorts
   → Users activated in < 1 hour: 80% retain
   → Users activated in 1-24 hours: 50% retain
   → Users activated in 24+ hours: 20% retain
   → Focus on fast activation
```

#### Activation Formulas

```
Activation Rate
= (Users who completed activation action / Total sign-ups) × 100%

Time to Activation
= Median time between sign-up and activation event

Activation Funnel Conversion
= (Users completing final step / Users starting funnel) × 100%

Example:
1,000 sign-ups this month
600 reached activation (first project created)
Median time: 3.2 hours

Activation rate = 600 / 1,000 = 60%
Time to activation = 3.2 hours
```

---

### 3. Retention

**Definition:** When users come back and continue using the product.

#### Key Metrics

```markdown
• Day 1/7/30 retention rate
• Weekly/Monthly Active Users (WAU/MAU)
• Churn rate (% users who stop using)
• Cohort retention curves
• Feature stickiness (DAU/MAU ratio)
• Usage frequency (sessions per user)
```

#### Retention Curves

```markdown
## Good Retention Curve
100% ┐
     │╲
 80% │ ╲___________  ← Flattens (users retain)
     │
 60% │
     └──────────────────────
      D1  D7  D30  D60  D90

## Bad Retention Curve
100% ┐
     │╲
 80% │ ╲
     │  ╲
 20% │   ╲___________  ← Keeps dropping
     └──────────────────────
      D1  D7  D30  D60  D90

Goal: Curve flattens = found core engaged users
```

#### Retention Benchmarks by Industry

```markdown
## Consumer Apps (B2C)
Day 1:  60-80%
Day 7:  30-50%
Day 30: 15-30%

## SaaS (B2B)
Day 1:  70-90%
Day 7:  50-70%
Day 30: 40-60%

## Social Networks
Day 1:  50-70%
Day 7:  40-60%
Day 30: 30-50%

## Gaming
Day 1:  40-60%
Day 7:  20-40%
Day 30: 10-20%

Note: Varies widely by product type and market
```

#### Optimization Strategies

```markdown
1. Identify retention drivers
   → Which features do retained users use?
   → Correlation analysis: feature usage vs. retention
   → Encourage high-retention behaviors

2. Re-engagement campaigns
   → Email: "You haven't logged in for 7 days"
   → Push notifications: "Your team posted an update"
   → In-app messages: "New features available"

3. Habit formation
   → Daily streaks (Duolingo)
   → Email digests (daily/weekly)
   → Reminder notifications

4. Prevent churn
   → Identify at-risk users (low engagement)
   → Proactive outreach
   → Offer help, incentives

5. Improve product stickiness
   → Add integrations (harder to leave)
   → Data network effects (more data = more value)
   → Social features (friends keep you engaged)
```

#### Retention Formulas

```
Day N Retention
= (Users active on Day N / Users in cohort) × 100%

Churn Rate
= (Users at start - Users at end) / Users at start × 100%

Stickiness (DAU/MAU Ratio)
= (DAU / MAU) × 100%
• 20%+ = Very sticky (users engage 6+ days/month)
• 10-20% = Moderate
• <10% = Low engagement

Example:
Cohort: 1,000 users signed up Jan 1
Day 7: 350 returned
Day 30: 200 returned

Day 7 retention = 350 / 1,000 = 35%
Day 30 retention = 200 / 1,000 = 20%
```

---

### 4. Referral

**Definition:** When users recommend your product to others.

#### Key Metrics

```markdown
• Viral coefficient (K-factor)
• Referral rate (% users who refer)
• Invites sent per user
• Invite acceptance rate
• Net Promoter Score (NPS)
• Viral cycle time
```

#### Viral Coefficient (K-Factor)

```
K = (% users inviting) × (avg invites per user) × (invite conversion rate)

K > 1: Viral growth (each user brings >1 new user)
K = 1: Replacement growth
K < 1: Need paid acquisition

Example:
20% of users send invites
Average 5 invites per user
30% invitation acceptance

K = 0.20 × 5 × 0.30 = 0.30

Interpretation: Each user brings 0.30 new users
→ Need paid acquisition to grow
```

#### Viral Cycle Time

```
Viral Cycle Time = Time from sign-up to sending first invite

Shorter = Faster growth

Example:
K = 0.5, cycle time = 7 days
100 users → +50 in week 1 → +25 in week 2 → +13 in week 3

K = 0.5, cycle time = 1 day
100 users → +50 in day 1 → +25 in day 2 → +13 in day 3

Same K, but daily cycle = 7× faster growth
```

#### Referral Mechanisms

```markdown
## Inherent Virality (Built into product)
• Zoom: Invite to meeting → receiver must install
• Google Docs: Share document → receiver must sign up
• WhatsApp: Message friend → network effect

## Incentivized Referral (Rewards)
• Dropbox: Refer friend → both get extra storage
• Airbnb: Refer host/guest → both get credits
• Uber: Give $10 off → get $10 off

## Social Sharing (Content distribution)
• Canva: Share design → branded footer
• Loom: Share video → "Record your own with Loom"
• Medium: Article → "Read more on Medium"

## Word of Mouth (Organic)
• Slack: Teams talk about productivity
• Notion: Users share templates
• Figma: Designers showcase work
```

#### Optimization Strategies

```markdown
1. Make sharing valuable for sharer
   → Collaboration requires inviting others
   → Sharing creates accountability (fitness app)
   → Social validation (post achievements)

2. Make sharing easy
   → One-click invite
   → Import contacts
   → Shareable links

3. Incentivize appropriately
   → Two-sided incentives (both get reward)
   → Reward upon conversion, not just invite
   → Avoid spam (rate limits)

4. Measure and optimize
   → A/B test invite copy
   → Test reward amounts
   → Optimize timing (when to prompt invite)
```

---

### 5. Revenue

**Definition:** When users generate business value (paying customers).

#### Key Metrics

```markdown
• Monthly Recurring Revenue (MRR)
• Annual Recurring Revenue (ARR)
• Average Revenue Per User (ARPU)
• Customer Lifetime Value (LTV)
• Customer Acquisition Cost (CAC)
• LTV:CAC ratio
• Conversion to paid rate
• Revenue churn
• Expansion revenue
```

#### Revenue Formulas

```
Monthly Recurring Revenue (MRR)
= Sum of all monthly subscription values

Annual Recurring Revenue (ARR)
= MRR × 12

Average Revenue Per User (ARPU)
= Total revenue / Number of paying users

Customer Lifetime Value (LTV)
= ARPU × Average lifetime (months)

OR

LTV = ARPU × Gross Margin % / Monthly Churn Rate

Customer Acquisition Cost (CAC)
= Total sales & marketing spend / New customers

LTV:CAC Ratio
= LTV / CAC
• >3:1 = Healthy (for every $1 spent, get $3+ back)
• 1:1 = Unsustainable (not profitable)

Payback Period
= CAC / (ARPU × Gross Margin %)
• <12 months = Good
• 12-18 months = Acceptable
• >18 months = Risky
```

#### Revenue Optimization

```markdown
## Increase Conversion Rate
• Optimize pricing page
• Add social proof (testimonials, logos)
• Offer free trial (reduce friction)
• Transparent pricing (no "Contact sales")

## Increase ARPU
• Upsell to higher tiers
• Cross-sell additional products
• Usage-based pricing (more usage = more revenue)
• Annual vs. monthly (discount for commitment)

## Reduce Churn
• Improve product value
• Customer success programs
• Proactive support
• Prevent cancellations (retention offers)

## Expansion Revenue
• Seat expansion (more users)
• Feature upsells
• Add-ons and integrations
• Enterprise contracts
```

#### SaaS Metrics

```markdown
## Monthly Metrics
New MRR:        +$10,000  (new customers)
Expansion MRR:  +$3,000   (upsells/upgrades)
Churned MRR:    -$2,000   (cancellations)
Contraction MRR: -$500    (downgrades)

Net New MRR = +$10,000 + $3,000 - $2,000 - $500 = +$10,500

## Growth Metrics
MRR Growth Rate = (Net New MRR / Starting MRR) × 100%
Quick Ratio = (New + Expansion) / (Churned + Contraction)
• >4 = Excellent
• 2-4 = Good
• <1 = Shrinking
```

---

## Additional Key Metrics

### Engagement Metrics

```
Session Duration
= Average time between session start and end

Pages Per Session
= Average page views per visit

Bounce Rate
= (Single-page sessions / Total sessions) × 100%

Feature Adoption
= (Users using feature / Total active users) × 100%
```

### Conversion Metrics

```
Conversion Rate
= (Conversions / Visitors) × 100%

Qualified Lead Rate
= (Qualified leads / Total leads) × 100%

Sales Cycle Length
= Average days from first touch to closed deal
```

---

## Metric Selection Guide

### Choosing the Right Metrics

```markdown
## For Startups (Pre-PMF)
Focus: Retention + Activation
• Are users coming back?
• Are they getting value?
→ Ignore revenue/growth until retention stabilizes

## For Growth Stage
Focus: AARRR + NSM
• North Star Metric
• AARRR funnel optimization
• Channel efficiency (LTV:CAC)

## For Enterprise
Focus: Expansion + Net Revenue Retention
• Account expansion (seats, features)
• NRR (Net Revenue Retention) > 100%
• Customer health scores
```

### Metrics Anti-Patterns

```markdown
❌ Vanity Metrics
• Total users (includes churned)
• Total downloads (not active users)
• Page views (no business impact)

✓ Actionable Metrics
• Active users (engaged recently)
• Retained users (came back)
• Converted users (paid)

❌ Too Many Metrics
• Tracking 50+ KPIs
• No clear priorities
• Analysis paralysis

✓ Focused Metrics
• 1 North Star
• 3-5 supporting inputs
• AARRR framework

❌ Lagging Indicators Only
• Revenue (happens after value delivery)
• Churn (user already lost)

✓ Mix of Leading + Lagging
• Leading: Feature usage, engagement
• Lagging: Revenue, churn
```

---

## Checklist

```markdown
## North Star Metric
- [ ] NSM defined and documented
- [ ] Validated correlation with revenue
- [ ] Input metrics identified (3-5)
- [ ] Dashboards tracking NSM + inputs
- [ ] Team aligned on NSM

## AARRR Framework
- [ ] Acquisition channels tracked
- [ ] Activation event defined
- [ ] Retention curves analyzed
- [ ] Referral mechanism in place
- [ ] Revenue metrics monitored

## Metric Hygiene
- [ ] Definitions documented
- [ ] Calculation methods clear
- [ ] Consistent across teams
- [ ] Regular reporting cadence
- [ ] Avoid vanity metrics
```
