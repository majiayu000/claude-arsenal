# Prioritization Frameworks

## Overview

Product prioritization is the process of determining the relative importance of features, projects, or initiatives to decide what to build next. Different frameworks suit different contexts, team sizes, and decision types.

---

## Framework Comparison

| Framework | Best For | Speed | Data Required | Output |
|-----------|----------|-------|---------------|--------|
| **RICE** | Many comparable features | Medium | High (metrics) | Numerical score |
| **ICE** | Quick decisions, experiments | Fast | Low (estimates) | Numerical score |
| **MoSCoW** | Release planning, MVP scope | Fast | Low (judgment) | Categories |
| **Kano** | Customer satisfaction | Slow | High (surveys) | Categories |
| **Value vs Effort** | Visual comparison | Fast | Low (estimates) | 2x2 matrix |
| **Cost of Delay** | Time-sensitive features | Medium | Medium (financial) | $/time |
| **Weighted Scoring** | Complex multi-criteria | Medium | Medium (custom) | Numerical score |

---

## RICE Framework

**Developed by:** Intercom

**Formula:**
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

### Components

#### Reach
**Definition:** How many people will this affect within a given time period?

**Measurement:**
- Users per quarter
- Transactions per month
- Pageviews per week

**Example:**
```
Feature: Password reset email
Reach = 5,000 users/quarter (estimated forgot password requests)

Feature: Dark mode
Reach = 50,000 users/quarter (all active users)

Feature: Export to PDF
Reach = 500 users/quarter (power users only)
```

**Tips:**
- Use real data from analytics when possible
- For new features, estimate conservatively
- Define time period consistently (per quarter recommended)

#### Impact
**Definition:** How much will this improve the outcome per person affected?

**Scale:**
```
3     = Massive impact
2     = High impact
1     = Medium impact
0.5   = Low impact
0.25  = Minimal impact
```

**Examples:**
```
Massive (3):
- Core product functionality (can't use product without it)
- Major conversion improvement (50%+ increase)
- Critical security fix

High (2):
- Significant UX improvement
- Notable performance increase (2x faster)
- Important compliance requirement

Medium (1):
- Moderate convenience improvement
- Incremental feature enhancement
- Nice-to-have functionality

Low (0.5):
- Small polish
- Minor optimization
- Rarely used edge case

Minimal (0.25):
- Cosmetic change
- Vanity metric improvement
- Internal tooling nice-to-have
```

**Tips:**
- Focus on user/business value, not effort
- Consider both immediate and long-term impact
- Be honest about incremental vs transformative changes

#### Confidence
**Definition:** How confident are you in your estimates?

**Scale:**
```
100%  = High confidence (strong data, validated assumptions)
80%   = Medium confidence (some data, reasonable estimates)
50%   = Low confidence (hypotheses, gut feel)
```

**Examples:**
```
High (100%):
- Feature request from 1000+ users
- A/B test showed 30% improvement
- Competitor has this and it's highly rated
- We have analytics data supporting need

Medium (80%):
- Feedback from 50+ users
- Industry best practice
- Small pilot test showed promise
- Reasonable assumptions based on similar features

Low (50%):
- Speculative new market
- Unvalidated hypothesis
- No clear precedent
- Gut feeling from stakeholders
```

**Tips:**
- Lower confidence for uncertain reach or impact
- Never use confidence to inflate weak ideas
- If confidence < 50%, consider research spike first

#### Effort
**Definition:** Total time investment from all team members

**Measurement:**
- Person-months (1 person working full-time for 1 month)
- Include: engineering, design, PM, QA, marketing

**Examples:**
```
0.5 person-months:
- Simple UI change, no backend work
- Adding a new field to existing form
- Basic content update

1 person-month:
- Small feature with frontend + backend
- Integration with existing API
- New dashboard page

2 person-months:
- Medium feature across multiple components
- New integration requiring coordination
- Performance optimization project

4+ person-months:
- Major new feature area
- Platform migration
- Multi-team coordination required
```

**Tips:**
- Include all roles (not just engineering)
- Account for testing, docs, deployment
- Round up for uncertainty
- Break down if >6 person-months

### Example Calculation

```
Feature: One-click Reorder

Reach: 10,000 customers/quarter
  → Active customers who have ordered before
  → Analytics show 40% reorder within 3 months

Impact: 2 (High)
  → Significantly reduces friction for repeat purchases
  → Expected to increase reorder rate by 25%
  → Competitive feature (Amazon has it)

Confidence: 80%
  → Customer survey showed strong interest (n=200)
  → We have data on reorder frequency
  → Implementation is straightforward (similar to "Add to Cart")

Effort: 1.5 person-months
  → 1 month engineering (frontend + backend)
  → 0.25 month design
  → 0.25 month PM + QA

RICE Score = (10,000 × 2 × 0.8) / 1.5 = 10,667
```

### RICE Scoring Table

| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|
| One-click reorder | 10,000 | 2 | 80% | 1.5 | 10,667 | 1 |
| Email notifications | 50,000 | 0.5 | 100% | 0.5 | 50,000 | 2 |
| Advanced search | 20,000 | 1 | 80% | 2 | 8,000 | 3 |
| Dark mode | 50,000 | 0.5 | 80% | 2 | 10,000 | 4 |
| Export to PDF | 500 | 2 | 100% | 1 | 1,000 | 5 |
| Social sharing | 5,000 | 0.5 | 50% | 1 | 1,250 | 6 |

### When to Use RICE

```
✓ Managing a large backlog (50+ features)
✓ Need quantitative comparison across diverse features
✓ Have access to user analytics and data
✓ Want to reduce bias in prioritization
✓ Building data-driven prioritization culture

✗ Very early stage (no usage data)
✗ Need immediate decision (too slow)
✗ Features are incomparable (different products/markets)
```

---

## ICE Framework

**Developed by:** Sean Ellis (Growth Hacking)

**Formula:**
```
ICE Score = (Impact + Confidence + Ease) / 3
```

### Components

#### Impact (1-10)
How much will this move the needle on your goals?

```
10: Game-changer, 10x improvement
8-9: Major improvement, 2-5x better
6-7: Significant improvement, 50-100% better
4-5: Moderate improvement, 20-50% better
2-3: Small improvement, 5-20% better
1: Minimal improvement, <5% better
```

#### Confidence (1-10)
How sure are you this will work?

```
10: Proven (we've done this before, or competitor has)
8-9: Strong evidence (user research, A/B test results)
6-7: Good indicators (analytics, customer feedback)
4-5: Educated guess (industry best practices)
2-3: Hypothesis (logical but unproven)
1: Wild guess (pure speculation)
```

#### Ease (1-10)
How easy is this to implement?

```
10: Trivial (config change, < 1 day)
8-9: Very easy (< 1 week, no dependencies)
6-7: Easy (1-2 weeks, minor coordination)
4-5: Moderate (2-4 weeks, some complexity)
2-3: Difficult (1-2 months, coordination needed)
1: Very difficult (3+ months, major effort)
```

### Example Calculation

```
Experiment: Add testimonials to pricing page

Impact: 7
  → Could increase conversions by 30-50%
  → Testimonials proven to build trust
  → Pricing page is high-traffic (10k/month)

Confidence: 8
  → We have customer testimonials ready
  → Competitor analysis shows this works
  → Social proof is well-documented tactic

Ease: 9
  → Just need to add HTML/CSS
  → Testimonials already collected
  → No backend work needed
  → Can ship in 2 days

ICE Score = (7 + 8 + 9) / 3 = 8.0
```

### ICE Scoring Table

| Experiment | Impact | Confidence | Ease | ICE Score | Priority |
|------------|--------|------------|------|-----------|----------|
| Add testimonials to pricing | 7 | 8 | 9 | 8.0 | 1 |
| Email drip campaign | 6 | 7 | 8 | 7.0 | 2 |
| A/B test CTA button color | 4 | 9 | 10 | 7.7 | 3 |
| Rebuild onboarding flow | 9 | 6 | 3 | 6.0 | 4 |
| Implement referral program | 8 | 5 | 4 | 5.7 | 5 |

### When to Use ICE

```
✓ Growth experiments and A/B tests
✓ Weekly backlog grooming
✓ Quick prioritization decisions
✓ Limited data available
✓ Speed matters more than precision
✓ Small, scrappy teams

✗ Complex, multi-year projects
✗ Need precise cost analysis
✗ Regulatory/compliance decisions
```

---

## MoSCoW Method

**Developed by:** Dai Clegg (Oracle)

**Acronym:**
```
M = Must Have
S = Should Have
C = Could Have
W = Won't Have (this time)
```

### Categories

#### Must Have
**Definition:** Non-negotiable requirements. Without these, the product fails or cannot launch.

**Questions to ask:**
- Can we launch without this?
- What's the impact if we don't include it?
- Is this a legal/regulatory requirement?
- Does this deliver core value proposition?

**Examples:**
```
E-commerce MVP:
✓ Product catalog
✓ Shopping cart
✓ Checkout and payment
✓ Order confirmation
✓ User authentication

Reason: Can't run an e-commerce site without these
```

**Warning:** Resist putting everything here. Typically 60% of features at most.

#### Should Have
**Definition:** Important but not vital. Painful to omit, but workarounds exist.

**Questions to ask:**
- Is there a workaround if we skip this?
- Can we deliver value without it?
- Does this significantly improve the experience?

**Examples:**
```
E-commerce MVP:
✓ Product reviews
✓ Order tracking
✓ Email receipts
✓ Related product recommendations
✓ Wishlist

Reason: Valuable but not critical for launch. Can add in Phase 2.
```

**Typical allocation:** ~20% of features

#### Could Have
**Definition:** Nice to have. "Vitamins, not painkillers." Include only if time/resources allow.

**Questions to ask:**
- Does this delight users but isn't expected?
- Can we easily add this later?
- Is this more about "nice" than "necessary"?

**Examples:**
```
E-commerce MVP:
✓ Gift wrapping option
✓ Product comparison tool
✓ Social media sharing
✓ Save for later
✓ Advanced filters

Reason: Enhances experience but not expected in MVP
```

**Typical allocation:** ~10% of features

#### Won't Have
**Definition:** Explicitly out of scope for this release. Defer to future.

**Questions to ask:**
- Is this a future enhancement?
- Does this belong in a different product?
- Is this too ambitious for current timeline?

**Examples:**
```
E-commerce MVP:
✗ Augmented reality try-on
✗ Live chat support
✗ Loyalty points program
✗ Subscription boxes
✗ Mobile app (web-only for MVP)
✗ International shipping

Reason: Too complex for MVP, but potentially valuable later
```

**Purpose:** Setting expectations, preventing scope creep

### MoSCoW Template

```markdown
## MVP: E-commerce Platform

### Must Have (Critical for Launch)
- [ ] User registration and login
- [ ] Product catalog with search
- [ ] Shopping cart functionality
- [ ] Checkout flow (address, payment)
- [ ] Order confirmation and email
- [ ] Basic admin panel for product management
- [ ] Payment processing (Stripe)
- [ ] SSL and basic security

**Launch Blocker:** Cannot ship without these

### Should Have (Important but Not Critical)
- [ ] Product reviews and ratings
- [ ] Order history
- [ ] Order tracking integration
- [ ] Guest checkout (no account needed)
- [ ] Product image zoom
- [ ] Email marketing integration
- [ ] Discount codes

**Justification:** Significantly improve experience, but MVP functional without

### Could Have (Nice to Have)
- [ ] Wishlist functionality
- [ ] Product comparison
- [ ] Social sharing
- [ ] Gift wrapping options
- [ ] Advanced search filters (brand, price range, etc.)
- [ ] Save addresses for faster checkout
- [ ] Product recommendations

**Justification:** Polish features, can add post-launch based on feedback

### Won't Have (Future Phases)
- [ ] Mobile app (web responsive only)
- [ ] Live chat support
- [ ] Loyalty/rewards program
- [ ] Subscription/recurring orders
- [ ] AR virtual try-on
- [ ] International shipping (US only for MVP)
- [ ] Multi-language support

**Justification:** Out of scope for initial launch, revisit in Q3-Q4
```

### When to Use MoSCoW

```
✓ Sprint planning
✓ MVP scoping
✓ Release planning
✓ Stakeholder alignment (manage expectations)
✓ Time-boxed projects with fixed deadlines
✓ When you need clear go/no-go decisions

✗ Too many features to categorize (use RICE instead)
✗ Need quantitative prioritization
✗ All features feel critical (forces hard choices)
```

### MoSCoW Best Practices

```
1. Timebox the release
   "This is our 3-month MVP timeline"

2. Set percentages
   Max 60% Must, 20% Should, 20% Could

3. Be ruthless with "Must Have"
   If you can launch without it, it's not a Must

4. Document "Won't Have" clearly
   Prevents re-litigation and scope creep

5. Revisit after each release
   Today's "Won't Have" might be tomorrow's "Must Have"
```

---

## Kano Model

**Developed by:** Noriaki Kano (1984)

**Purpose:** Categorize features by their effect on customer satisfaction

### Categories

```
                    Satisfaction
                         ↑
                         |
        Delighters       |
              ___---'''  |
         _---''          |
    _---'                |
___/_____________________|___________________→ Implementation
                         |    ___---'''
                         |_---''  Performance
                     _---'
                 _---
             _---'     Basic Needs
```

#### Basic Needs (Must-Haves)
**Characteristics:**
- Assumed by users, not explicitly requested
- Absence = dissatisfaction
- Presence = neutral (expected)
- Threshold: must meet minimum standard

**Examples:**
```
Website:
- Site loads (doesn't crash)
- Checkout works
- Secure payment processing
- Mobile responsive

Hotel:
- Clean room
- Hot water
- WiFi
- Safe environment

Car:
- Brakes work
- Doors lock
- Engine starts
```

**Implication:** Must deliver these, but investing beyond minimum doesn't increase satisfaction.

#### Performance Needs (Satisfiers)
**Characteristics:**
- More is better (linear relationship)
- Absence = dissatisfaction
- Presence = satisfaction
- Competitive differentiator

**Examples:**
```
Website:
- Page load speed (faster = better)
- Product selection (more = better)
- Payment options (more = better)
- Customer service response time (faster = better)

Hotel:
- Room size (bigger = better)
- Breakfast options (more = better)
- Check-in speed (faster = better)

Car:
- Fuel efficiency (better MPG = better)
- Cargo space (more = better)
- Horsepower (more = better)
```

**Implication:** Invest strategically. Balance cost vs satisfaction gain.

#### Delighters (Exciters)
**Characteristics:**
- Unexpected features that wow
- Absence = neutral (not expected)
- Presence = high satisfaction
- Novelty fades over time (becomes performance/basic)

**Examples:**
```
Website:
- Free shipping
- Personalized recommendations
- Surprise discount at checkout
- Proactive support (before you ask)

Hotel:
- Welcome drink
- Room upgrade
- Handwritten note
- Local recommendations

Car:
- Heated steering wheel
- Panoramic sunroof
- Self-parking
- Massage seats
```

**Implication:** Creates competitive advantage and brand loyalty. But expensive to maintain as they become expected.

#### Indifferent
**Characteristics:**
- Users don't care either way
- No impact on satisfaction

**Examples:**
```
Website:
- Animated logo
- Excessive theme customization
- Social media share count
- Company history timeline

Hotel:
- Hotel mascot
- Corporate mission statement in room
- Lobby art installation

Car:
- Engine sound customization
- Ambient lighting (for many users)
```

**Implication:** Don't invest resources here. Remove or deprioritize.

### Kano Survey Method

**Question Pairs:**

For each feature, ask two questions:

```
Functional (feature present):
"How would you feel if we HAD [feature]?"

Dysfunctional (feature absent):
"How would you feel if we DIDN'T have [feature]?"

Answer choices:
1. I like it
2. I expect it
3. I'm neutral
4. I can tolerate it
5. I dislike it
```

**Mapping Responses:**

| Functional → <br> Dysfunctional ↓ | Like | Expect | Neutral | Tolerate | Dislike |
|---|---|---|---|---|---|
| **Like** | Questionable | Delighter | Delighter | Delighter | Performance |
| **Expect** | Reverse | Indifferent | Indifferent | Indifferent | Basic |
| **Neutral** | Reverse | Indifferent | Indifferent | Indifferent | Basic |
| **Tolerate** | Reverse | Indifferent | Indifferent | Indifferent | Basic |
| **Dislike** | Reverse | Reverse | Reverse | Reverse | Questionable |

**Example Survey:**

```
Feature: Free 2-day shipping

Q1 (Functional): How would you feel if we offered free 2-day shipping?
User response: "I like it"

Q2 (Dysfunctional): How would you feel if we DIDN'T offer free 2-day shipping?
User response: "I expect it"

Result: Performance feature (linear satisfaction)

---

Feature: Handwritten thank-you note with order

Q1 (Functional): How would you feel if you received a handwritten thank-you note?
User response: "I like it"

Q2 (Dysfunctional): How would you feel if you didn't receive one?
User response: "I'm neutral"

Result: Delighter (unexpected, creates delight)
```

### Using Kano for Prioritization

```
1. Basic Needs
   Priority: Must deliver (P0)
   Investment: Minimum viable

   ✓ Ensure all basic needs met
   ✗ Don't over-invest beyond threshold

2. Performance Needs
   Priority: Competitive parity (P1)
   Investment: Strategic, data-driven

   ✓ Match or exceed competitors
   ✓ Measure ROI (satisfaction gain vs cost)

3. Delighters
   Priority: Differentiation (P2)
   Investment: Selective, high-impact

   ✓ Choose 2-3 signature delighters
   ✓ Monitor as they become expected over time
   ⚠ Delighters fade → Performance → Basic

4. Indifferent
   Priority: Remove or defer (P3)
   Investment: None

   ✓ Eliminate to reduce complexity
   ✓ Free up resources for delighters
```

### When to Use Kano

```
✓ Customer-driven product decisions
✓ Balancing must-haves vs innovation
✓ UX improvements
✓ Competitive differentiation strategy
✓ Long-term roadmap planning

✗ Early MVP (insufficient users to survey)
✗ Urgent decisions (too slow)
✗ Internal tools (different stakeholders)
```

---

## Value vs Effort Matrix

**Format:** 2x2 matrix

```
        High Value
            ↑
     Quick Wins │ Major Projects
    (Do First)  │  (Plan Carefully)
    ────────────┼────────────────→ High Effort
     Fill-Ins   │  Money Pits
    (Do Later)  │  (Avoid)
            ↓
        Low Value
```

### Quadrants

#### Quick Wins (High Value, Low Effort)
**Priority:** Do immediately
**Examples:**
- Fix critical bug
- Add missing "Forgot Password" link
- Enable Google Analytics
- Simple UI copy improvements

**Strategy:** Ship fast, measure impact

#### Major Projects (High Value, High Effort)
**Priority:** Plan carefully, allocate resources
**Examples:**
- Build new product line
- Platform migration
- Redesign checkout flow
- International expansion

**Strategy:** Break into phases, validate assumptions, long-term commitment

#### Fill-Ins (Low Value, Low Effort)
**Priority:** Do when capacity available
**Examples:**
- Update footer links
- Add tooltips
- Minor visual polish
- Internal tooling improvements

**Strategy:** Good for onboarding new team members, downtime between projects

#### Money Pits (Low Value, High Effort)
**Priority:** Avoid or deprioritize
**Examples:**
- Over-engineered solutions
- Gold-plating existing features
- Rarely requested features
- Vanity projects

**Strategy:** Eliminate, or find ways to reduce effort

### Example Matrix

```
Feature Mapping:

Quick Wins:
- Add "Save for Later" button (2 days, high request)
- Fix slow product search (3 days, impacts 80% users)
- Email order confirmations (1 week, expected feature)

Major Projects:
- Mobile app (6 months, 40% of traffic is mobile)
- Recommendation engine (3 months, proven to increase AOV)
- International shipping (4 months, TAM expansion)

Fill-Ins:
- Dark mode (1 week, 10% request rate)
- Social media sharing (3 days, low usage expected)
- Advanced filters (1 week, power users only)

Money Pits:
- Custom product configurator (3 months, <5% use case)
- Gamification (2 months, unproven value)
- AR try-on (4 months, insufficient hardware adoption)
```

### When to Use Value vs Effort

```
✓ Visual communication with stakeholders
✓ Quick prioritization exercises
✓ Workshops and brainstorming
✓ Portfolio management (balance quick wins vs big bets)

✗ Precise quantitative comparison
✗ Many similar features (hard to plot)
✗ Complex multi-dimensional decisions
```

---

## Cost of Delay (CD3)

**Purpose:** Quantify the cost of not shipping a feature

**Formula:**
```
CD3 Score = (User Value + Time Value + Risk Reduction) / Duration

Where:
- User Value: Impact on users (1-10)
- Time Value: Time sensitivity (1-10)
- Risk Reduction: Reduces business risk (1-10)
- Duration: Time to implement (months)
```

### When to Use

```
✓ Time-sensitive features (compliance deadlines, seasonal)
✓ Opportunity cost matters
✓ Trade-offs between speed and quality

Example:
Feature A: Low urgency, build in 3 months
Feature B: High urgency (competitor launched), build in 1 month

Even if A has higher value, B's time sensitivity may make it higher priority.
```

---

## Weighted Scoring

**Purpose:** Custom multi-criteria prioritization

### Setup

```
1. Define criteria (3-7 factors)
   Example:
   - User value (0-10)
   - Business value (0-10)
   - Strategic alignment (0-10)
   - Technical feasibility (0-10)
   - Effort (0-10, inverted)

2. Assign weights (must sum to 100%)
   Example:
   - User value: 30%
   - Business value: 30%
   - Strategic alignment: 20%
   - Technical feasibility: 10%
   - Effort: 10%

3. Score each feature
   Weighted Score = Σ (Score × Weight)
```

### Example

| Feature | User Value (30%) | Business Value (30%) | Strategic (20%) | Feasibility (10%) | Effort (10%) | Weighted Score |
|---------|---|---|---|---|---|---|
| Mobile app | 9 (2.7) | 8 (2.4) | 9 (1.8) | 7 (0.7) | 3 (0.3) | **7.9** |
| Dark mode | 6 (1.8) | 4 (1.2) | 3 (0.6) | 9 (0.9) | 8 (0.8) | **5.3** |
| SSO | 7 (2.1) | 9 (2.7) | 8 (1.6) | 6 (0.6) | 5 (0.5) | **7.5** |

### When to Use

```
✓ Complex decisions with multiple stakeholders
✓ Need to balance competing priorities
✓ Custom criteria (beyond standard frameworks)
✓ Transparent decision-making process

✗ Simple decisions (overkill)
✗ Fast-moving environments (too slow)
```

---

## Combining Frameworks

### Recommended Hybrid Approach

```
1. Use MoSCoW to define release scope
   → Separate must-haves from nice-to-haves
   → Set clear boundaries

2. Use RICE to rank must-haves
   → Quantitative comparison within release
   → Data-driven sequencing

3. Use ICE for quick experiments
   → Weekly grooming of growth backlog
   → Fast iteration cycle

4. Use Kano to validate balance
   → Ensure we have basics, performance, delighters
   → Don't over-invest in basics
   → Include some wow factors

Example:
- All "Must Have" → Score with RICE → Build in RICE order
- "Should Have" → Use ICE for quick wins
- Validate with Kano → Are we delighting users or just checking boxes?
```

---

## Best Practices

### 1. Be Consistent

```
✓ Use same framework for comparable items
✓ Define metrics clearly upfront
✓ Document assumptions

✗ Don't mix frameworks arbitrarily
✗ Don't change scoring mid-process
```

### 2. Update Regularly

```
Prioritization is not one-time:
- Weekly: Groom backlog, add new items
- Monthly: Re-score top priorities
- Quarterly: Revisit framework, adjust weights
```

### 3. Include Stakeholders

```
✓ PM leads, but doesn't decide alone
✓ Engineering estimates effort
✓ Design validates user value
✓ Leadership confirms strategic alignment
✓ Customers validate through research
```

### 4. Accept Imperfection

```
"All models are wrong, but some are useful"

✓ Frameworks guide decisions, don't make them
✓ Use judgment for ties or edge cases
✓ Be transparent about trade-offs
```

### 5. Document Decisions

```
For each prioritized feature:
- Score/category
- Rationale
- Assumptions
- Date decided
- Who decided

This creates accountability and learning for future decisions.
```

---

## Checklist

```markdown
## Prioritization Process

### Preparation
- [ ] Define decision scope (what are we prioritizing?)
- [ ] Choose appropriate framework(s)
- [ ] Gather necessary data (analytics, user research)
- [ ] Identify stakeholders for input

### Execution
- [ ] Score or categorize each feature
- [ ] Document assumptions and rationale
- [ ] Review for bias or gaps
- [ ] Validate with stakeholders

### Output
- [ ] Ranked or categorized backlog
- [ ] Clear next steps (what to build first)
- [ ] Documented trade-offs
- [ ] Communicated to team

### Review
- [ ] Schedule regular re-prioritization
- [ ] Track accuracy of estimates
- [ ] Adjust framework if needed
- [ ] Learn from outcomes
```
