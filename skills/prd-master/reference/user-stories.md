# User Story Writing Guide

## Overview

User stories are short, simple descriptions of a feature told from the perspective of the person who desires the new capability. They follow the format:

```
As a [persona/role],
I want to [action/goal],
So that [benefit/value].
```

User stories are intentionally brief because they're meant to spark detailed discussions between the development team, product owner, and stakeholders.

---

## The Three C's Framework

### 1. Card

The "Card" represents the physical or digital card containing the user story statement. Originally, Agile teams wrote stories on index cards to emphasize their simplicity and portability.

**Purpose:**
- Placeholder for conversation
- Quick reference during planning
- Easy to reorganize and prioritize

**Example Card:**
```
As a returning customer,
I want one-click reordering of past purchases,
So that I can save time on frequent orders.
```

### 2. Conversation

The "Conversation" is the most critical element. User stories are brief because detailed requirements emerge through discussion.

**Key conversations:**
- Why is this valuable to users?
- What are the edge cases?
- What are the technical constraints?
- How does this integrate with existing features?
- What happens when things go wrong?

**Example Discussion Points:**
```
Story: One-click reordering

Questions to discuss:
- Q: How far back in order history can users reorder?
- A: Last 12 months, up to 100 most recent orders

- Q: What if an item is out of stock?
- A: Show substitution suggestions or remove from cart with notification

- Q: Do we modify quantities or use original order exactly?
- A: Use original, but allow editing before checkout

- Q: How do we handle price changes?
- A: Show current price, indicate if different from original order
```

### 3. Confirmation

The "Confirmation" involves the acceptance criteria that define when a story is complete.

**Format:** Given-When-Then (see acceptance-criteria.md)

**Example:**
```
Acceptance Criteria:

Given I'm viewing my order history
When I click "Reorder" on a past order
Then all available items are added to my cart
And out-of-stock items show substitution suggestions
And I see a summary: "12 items added, 2 unavailable"

Given items in my cart from reorder
When I proceed to checkout
Then I see current prices (with indicators if changed)
And I can edit quantities before payment
```

---

## INVEST Criteria

Good user stories follow INVEST principles:

### Independent

Stories should stand alone with minimal dependencies on other stories.

```
❌ Dependent:
Story 1: "Create user profile database table"
Story 2: "Add user profile UI" (depends on Story 1)

✓ Independent:
"As a user, I want to create and edit my profile"
(Implementation details emerge in conversation)
```

### Negotiable

Details are flexible and emerge through conversation. Stories are not rigid contracts.

```
❌ Too prescriptive:
"As a user, I want a blue button in the top-right corner that opens
a modal dialog with a form containing Name, Email, and Bio fields
limited to 500 characters with a Save button that calls POST /api/profile"

✓ Negotiable:
"As a user, I want to update my profile information (name, email, bio)
so that others can learn about me"

→ UI design and implementation details are discussed later
```

### Valuable

Every story must deliver value to users or the business.

```
❌ No clear value:
"As a developer, I want to refactor the authentication module"

✓ Valuable:
"As a user, I want faster login (< 2s) so I can access my account quickly"

Note: Technical work is valid but frame it in terms of user/business value
```

### Estimable

The team must be able to estimate the effort required.

```
❌ Too vague to estimate:
"As a user, I want the system to be intelligent"

✓ Estimable:
"As a user, I want product recommendations based on my browsing history"

If story is not estimable:
- Break it down into smaller stories
- Do a spike/research story first
- Clarify unknowns through conversation
```

### Small

Stories should be completable within one sprint (typically 1-2 weeks).

```
❌ Too large (Epic):
"As a customer, I want a complete e-commerce checkout experience"

✓ Small stories:
- "As a customer, I want to add items to my shopping cart"
- "As a customer, I want to enter shipping address"
- "As a customer, I want to select payment method"
- "As a customer, I want to review order before purchase"
- "As a customer, I want to receive order confirmation"
```

### Testable

Clear acceptance criteria make stories testable.

```
❌ Not testable:
"As a user, I want a good search experience"

✓ Testable:
"As a user, I want search results within 500ms
with at least 90% relevance for common queries"

Acceptance criteria:
- Given I search for "laptop"
- When results load
- Then I see results within 500ms (p95)
- And top 5 results match "laptop" category
```

---

## User Story Templates

### Standard Template

```
As a [persona/role],
I want to [action/goal],
So that [benefit/value].
```

### Job-to-be-Done Template

```
When [situation],
I want to [action],
So I can [outcome].
```

**Example:**
```
When I'm shopping for gifts during the holidays,
I want to filter by price range and recipient age,
So I can quickly find appropriate gifts within budget.
```

### Feature-Driven Template

```
In order to [benefit],
As a [persona/role],
I want [action/goal].
```

**Example:**
```
In order to reduce cart abandonment,
As a product manager,
I want to offer guest checkout without account creation.
```

---

## Examples by Domain

### E-commerce

```
Story: Guest Checkout
As a first-time visitor,
I want to checkout without creating an account,
So that I can complete my purchase quickly.

Acceptance Criteria:
- Given I have items in cart and I'm not logged in
- When I click "Checkout"
- Then I see option: "Continue as Guest" or "Login"
- And I can complete purchase with just email, shipping, payment
- And I receive confirmation email with order tracking

---

Story: Wishlist
As a registered user,
I want to save items to a wishlist,
So that I can purchase them later or share with others.

Acceptance Criteria:
- Given I'm viewing a product
- When I click "Add to Wishlist" (heart icon)
- Then the item is saved to my wishlist
- And I can view all wishlist items on dedicated page
- And I can share wishlist via unique URL
- And I can move items from wishlist to cart
```

### SaaS Application

```
Story: SSO Integration
As an enterprise admin,
I want to enable Single Sign-On via SAML,
So that my team can access the app using company credentials.

Acceptance Criteria:
- Given I'm an account admin
- When I navigate to Settings > Authentication
- Then I can upload SAML metadata XML or enter IdP URL
- And I can test connection before enabling
- And I can require SSO for all team members
- And users see "Login with SSO" option on login page

---

Story: Usage Analytics
As a team lead,
I want to see which features my team uses most,
So that I can optimize workflows and training.

Acceptance Criteria:
- Given I'm on the Analytics dashboard
- When I select date range (last 7/30/90 days)
- Then I see top 10 features by usage count
- And I see per-user activity breakdown
- And I can export data as CSV
```

### Mobile App

```
Story: Offline Mode
As a mobile user with unreliable connectivity,
I want to access recent content offline,
So that I can work without internet.

Acceptance Criteria:
- Given I've viewed content while online
- When I lose internet connection
- Then I can still access last 50 viewed items
- And I see indicator: "Offline mode - showing cached content"
- And my edits sync automatically when connection restored

---

Story: Push Notifications
As a user who wants to stay updated,
I want to receive push notifications for important events,
So that I don't miss time-sensitive information.

Acceptance Criteria:
- Given I've enabled notifications in settings
- When a relevant event occurs (message, mention, deadline)
- Then I receive push notification on my device
- And tapping notification opens relevant screen
- And I can customize notification types in settings
```

---

## Breaking Down Epics

### Epic Decomposition Process

```
1. Identify the Epic
   "Enable marketplace for third-party sellers"

2. List major capabilities
   - Seller registration and verification
   - Product listing management
   - Order fulfillment
   - Payment processing
   - Seller analytics

3. Break into user stories
   For each capability, write stories from different perspectives

4. Prioritize using MoSCoW or RICE
   Determine which stories are MVP vs future phases
```

### Example: Marketplace Epic

```
Epic: Enable Marketplace for Third-Party Sellers

Must Have (MVP):
- As a seller, I want to register and verify my business
- As a seller, I want to list products with photos and descriptions
- As a buyer, I want to see which products are from third-party sellers
- As a seller, I want to receive notification of new orders
- As a buyer, I want to contact sellers with questions
- As a seller, I want to receive payment for fulfilled orders
- As platform admin, I want to review and approve new sellers

Should Have (Phase 2):
- As a seller, I want to bulk upload products via CSV
- As a seller, I want analytics on views and sales
- As a buyer, I want to filter by seller rating
- As a seller, I want to offer promotions and discounts
- As platform admin, I want to charge commission on sales

Could Have (Phase 3):
- As a seller, I want to integrate inventory with my existing system
- As a seller, I want to A/B test product descriptions
- As a buyer, I want to follow favorite sellers
- As a seller, I want automated repricing based on competition

Won't Have (Future):
- As a seller, I want to open a physical storefront
- Integration with international payment processors
```

---

## User Story Mapping

User story mapping helps visualize the user journey and identify all necessary stories.

### Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    User Activities (Top Row)                 │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   Discover   │   Evaluate   │   Purchase   │   Use/Support  │
├──────────────┼──────────────┼──────────────┼────────────────┤
│              │              │              │                │
│  Stories     │  Stories     │  Stories     │   Stories      │
│  (vertical)  │  (vertical)  │  (vertical)  │   (vertical)   │
│              │              │              │                │
│  ↓ MVP       │  ↓ MVP       │  ↓ MVP       │   ↓ MVP        │
│  ↓ Phase 2   │  ↓ Phase 2   │  ↓ Phase 2   │   ↓ Phase 2    │
│  ↓ Phase 3   │  ↓ Phase 3   │  ↓ Phase 3   │   ↓ Phase 3    │
└──────────────┴──────────────┴──────────────┴────────────────┘

Horizontal: User journey (left to right)
Vertical: Priority (top = MVP, bottom = nice-to-have)
```

### Example: Online Course Platform

```
Activity: Discover
MVP:
- Browse course catalog
- Search by keyword
- Filter by category
Phase 2:
- Personalized recommendations
- Course previews (video)
Phase 3:
- AI-powered course suggestions

Activity: Evaluate
MVP:
- View course details
- Read course reviews
- See instructor bio
Phase 2:
- Compare courses side-by-side
- Preview first lesson free
Phase 3:
- AI-generated course summaries

Activity: Purchase
MVP:
- Add course to cart
- Checkout with credit card
- Receive confirmation email
Phase 2:
- Apply discount codes
- Gift courses to others
Phase 3:
- Subscription bundles
- Corporate/team purchases

Activity: Learn
MVP:
- Watch video lessons
- Track progress
- Download course materials
Phase 2:
- Take quizzes
- Certificate of completion
- Discussion forums
Phase 3:
- Live Q&A sessions
- Peer code review
- Offline mobile app
```

---

## Common Mistakes

### 1. Too Technical

```
❌ "As a developer, I want to implement OAuth2 with JWT tokens"

✓ "As a user, I want to login securely without remembering multiple passwords,
   so I can access my account from any device"

Why: Focus on user value, not implementation details
```

### 2. Too Vague

```
❌ "As a user, I want the system to be fast"

✓ "As a user, I want search results to load within 500ms,
   so I can quickly find products without waiting"

Why: Vague stories aren't testable or estimable
```

### 3. Missing the "So That"

```
❌ "As a user, I want to filter products by price range"

✓ "As a budget-conscious shopper, I want to filter products by price range,
   so I only see items I can afford"

Why: The benefit clarifies the value and helps prioritization
```

### 4. Multiple Stories in One

```
❌ "As a user, I want to create an account, update my profile,
    change my password, and delete my account"

✓ Split into 4 stories:
- "As a new user, I want to create an account with email and password"
- "As a user, I want to update my profile information (name, bio, photo)"
- "As a user, I want to change my password for security"
- "As a user, I want to delete my account and all associated data"

Why: Smaller stories are easier to estimate, test, and complete
```

### 5. Implementation over Outcome

```
❌ "As a user, I want a dropdown menu in the navigation bar"

✓ "As a user, I want to easily navigate to different product categories,
   so I can browse relevant items"

Why: Let the team determine the best implementation (dropdown, mega menu, sidebar, etc.)
```

---

## User Story Workflow

### 1. Ideation

```
Sources:
- User research and interviews
- Customer support tickets
- Product analytics
- Competitive analysis
- Stakeholder requests
- Technical improvements

Capture in product backlog (unsorted)
```

### 2. Elaboration

```
During backlog refinement:
- Write user story in standard format
- Add context and rationale
- Identify acceptance criteria (draft)
- Attach design mockups (if available)
- List dependencies
```

### 3. Estimation

```
Team estimates effort:
- Planning poker (Fibonacci: 1, 2, 3, 5, 8, 13)
- T-shirt sizes (S, M, L, XL)
- Ideal days/hours

If estimate is too high → break down further
If too uncertain → create research spike
```

### 4. Prioritization

```
Apply prioritization framework:
- RICE scoring
- MoSCoW categorization
- Business value vs effort matrix

Move to sprint backlog when ready
```

### 5. Implementation

```
During sprint:
- Developer picks story from sprint backlog
- Discusses details with PM/designer
- Implements functionality
- Writes automated tests
- Creates pull request

Definition of Done:
- [ ] Code complete and reviewed
- [ ] Unit tests written (>80% coverage)
- [ ] Acceptance criteria verified
- [ ] No critical bugs
- [ ] Documentation updated
- [ ] Deployed to staging
```

### 6. Acceptance

```
Product owner verifies:
- All acceptance criteria met
- Edge cases handled
- Performance acceptable
- Accessible (WCAG 2.2 AA)

If approved → mark as Done
If issues found → create bug stories
```

---

## Tools for User Stories

| Tool | Best For | Key Features |
|------|----------|--------------|
| **Jira** | Enterprise Agile | Epics, stories, sprints, workflows |
| **Linear** | Engineering-focused teams | Fast, clean UI, GitHub integration |
| **Shortcut** | Small-medium teams | Simple, visual, story mapping |
| **Azure DevOps** | Microsoft ecosystem | Full ALM, backlogs, boards |
| **Pivotal Tracker** | Agile purists | Story points, velocity tracking |
| **Trello** | Simple projects | Kanban boards, easy collaboration |
| **ClickUp** | All-in-one | Docs, tasks, goals, time tracking |

---

## Best Practices

### 1. Write from User Perspective

```
✓ "As a customer, I want..."
✓ "As a seller, I want..."
✓ "As an admin, I want..."

Avoid:
✗ "The system shall..."
✗ "As a developer, I want..." (unless building dev tools)
```

### 2. Focus on One Persona per Story

```
❌ "As a buyer or seller, I want to message each other"

✓ Split into two perspectives:
- "As a buyer, I want to message the seller with questions about a product"
- "As a seller, I want to respond to buyer messages to increase sales"
```

### 3. Avoid UI Specifications

```
❌ "As a user, I want a red button labeled 'Submit' in the bottom-right corner"

✓ "As a user, I want to easily submit my form and receive confirmation"

Let design determine the UI implementation
```

### 4. Include Acceptance Criteria Early

```
Don't wait until sprint planning to add acceptance criteria.
Draft them during backlog refinement so the team can estimate accurately.

Basic draft is OK, details emerge during implementation.
```

### 5. Keep the Backlog Groomed

```
Regular refinement (weekly):
- Remove obsolete stories
- Break down large stories
- Update priorities
- Add missing acceptance criteria
- Clarify ambiguities

Goal: 2-3 sprints of refined stories ready to pull
```

### 6. Link to Supporting Artifacts

```
Attach to user story:
- Design mockups (Figma, Sketch)
- User research findings
- Analytics data
- Technical specs
- API documentation
- Related PRD sections
```

---

## Checklist

```markdown
## User Story Quality Check

### Format
- [ ] Follows "As a / I want / So that" format
- [ ] Written from user perspective (not system/developer)
- [ ] Includes clear benefit/value in "so that" clause

### INVEST Criteria
- [ ] Independent: Minimal dependencies
- [ ] Negotiable: Details flexible, not prescriptive
- [ ] Valuable: Clear user or business value
- [ ] Estimable: Team can estimate effort
- [ ] Small: Completable in one sprint
- [ ] Testable: Has acceptance criteria

### Acceptance Criteria
- [ ] Uses Given-When-Then format
- [ ] Covers happy path
- [ ] Includes error scenarios
- [ ] Defines edge cases
- [ ] Measurable and testable

### Supporting Information
- [ ] Context and rationale provided
- [ ] Link to designs (if available)
- [ ] Dependencies identified
- [ ] Estimated by team
- [ ] Prioritized in backlog
```
