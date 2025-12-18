# Acceptance Criteria Patterns

## Overview

Acceptance criteria define the conditions that a feature must satisfy to be considered complete. They serve as a contract between the product team and development team, ensuring shared understanding of what "done" means.

---

## Why Acceptance Criteria Matter

### Benefits

```
For Product Managers:
✓ Clear definition of scope
✓ Prevents scope creep
✓ Basis for feature acceptance
✓ Requirements traceability

For Developers:
✓ Clear implementation guidance
✓ Testable conditions
✓ Reduces ambiguity
✓ Enables TDD/BDD

For QA:
✓ Test case foundation
✓ Coverage checklist
✓ Edge case identification
✓ Automation scenarios

For Stakeholders:
✓ Shared understanding
✓ Transparent progress
✓ Realistic expectations
```

---

## Given-When-Then Format (BDD)

**Structure:**
```
Given [precondition/context]
When [action/trigger]
Then [expected outcome]

And [additional context/outcome]
But [exception/constraint]
```

### Core Principles

#### Given: Preconditions
**Purpose:** Set the stage, establish context

**What to include:**
- User state (logged in, has items in cart)
- System state (database populated, API available)
- Environmental conditions (mobile device, slow connection)

**Tips:**
```
✓ Focus on relevant preconditions only
✓ Use real, concrete scenarios
✗ Don't include unnecessary context
✗ Don't describe how to set up the state
```

**Examples:**
```
✓ Given I'm logged in as a premium user
✓ Given I have 3 items in my shopping cart
✓ Given the product "Laptop Pro" is out of stock
✓ Given I'm on a mobile device with 3G connection

✗ Given I navigate to the login page, enter my credentials, click submit
   (Too detailed, this is the setup, not the precondition)
```

#### When: Action/Trigger
**Purpose:** Describe the user action or system event

**What to include:**
- Single, specific action
- User interaction (click, submit, swipe)
- System event (timeout, webhook received)

**Tips:**
```
✓ One action per When clause
✓ Use active voice
✗ Don't describe multiple actions
✗ Don't include implementation details
```

**Examples:**
```
✓ When I click "Add to Cart"
✓ When I submit the payment form
✓ When the session expires after 30 minutes
✓ When I swipe left on the notification

✗ When I click the blue button in the top-right corner
   (Too UI-specific, what if design changes?)

✗ When I click "Search" and enter "laptop" and press enter
   (Too many actions, split into separate scenarios)
```

#### Then: Expected Outcome
**Purpose:** Define observable results

**What to include:**
- What the user sees/experiences
- System state changes
- Messages, notifications, navigation
- Performance criteria

**Tips:**
```
✓ Make it testable and measurable
✓ Focus on user-observable outcomes
✗ Don't specify internal implementation
✗ Don't be vague or subjective
```

**Examples:**
```
✓ Then I see "Item added to cart" confirmation
✓ Then my cart count increases by 1
✓ Then I'm redirected to the checkout page
✓ Then the page loads within 2 seconds

✗ Then the database is updated
   (Internal detail, not user-observable)

✗ Then the user has a good experience
   (Too vague, not testable)
```

### Complete Examples

#### Example 1: Login

```gherkin
Scenario: Successful login with valid credentials
  Given I'm on the login page
  And I'm not currently logged in
  When I enter email "user@example.com"
  And I enter password "SecurePass123"
  And I click "Login"
  Then I'm redirected to my dashboard
  And I see "Welcome back, John!"
  And the session persists for 30 days

Scenario: Failed login with invalid password
  Given I'm on the login page
  When I enter email "user@example.com"
  And I enter an incorrect password
  And I click "Login"
  Then I remain on the login page
  And I see error message "Invalid email or password"
  And the password field is cleared
  And my account is not locked (< 5 failed attempts)

Scenario: Account lockout after multiple failed attempts
  Given I have failed to login 4 times in the last hour
  When I enter incorrect password again
  And I click "Login"
  Then I see error message "Account locked for 1 hour due to multiple failed attempts"
  And I see link "Reset password"
  And the login form is disabled
```

#### Example 2: E-commerce Checkout

```gherkin
Scenario: Successful payment with credit card
  Given I have 3 items in my cart totaling $150
  And I'm logged in with a saved shipping address
  When I click "Proceed to Checkout"
  And I select "Credit Card" as payment method
  And I enter valid credit card details
  And I click "Place Order"
  Then I see order confirmation page with order number
  And I receive confirmation email within 2 minutes
  And my cart is emptied
  And my credit card is charged $150
  And order status is "Processing"

Scenario: Payment declined
  Given I'm at the payment step with $150 order
  When I enter credit card details
  And I click "Place Order"
  And the payment is declined by the bank
  Then I remain on the payment page
  And I see error "Payment declined. Please try another card or payment method."
  And my cart items are preserved
  And no charge is made
  And no order is created

Scenario: Session timeout during checkout
  Given I'm at the payment step
  And I've been idle for 30 minutes
  When I click "Place Order"
  Then I'm redirected to login page
  And I see message "Your session expired. Please log in to continue."
  And my cart items are preserved
  And I'm redirected back to checkout after successful login
```

#### Example 3: Search Functionality

```gherkin
Scenario: Search with results
  Given I'm on the homepage
  And the product database has 1000+ products
  When I enter "laptop" in the search box
  And I press Enter
  Then I see search results page within 500ms
  And I see "Showing 1-20 of 156 results for 'laptop'"
  And results are sorted by relevance (default)
  And each result shows: image, title, price, rating

Scenario: Search with no results
  Given I'm on the search page
  When I search for "xyznonexistent12345"
  Then I see "No results found for 'xyznonexistent12345'"
  And I see "Try different keywords or check spelling"
  And I see suggested popular searches
  And I don't see any product results

Scenario: Search with filters applied
  Given I've searched for "laptop"
  And I see 156 results
  When I select price range "$500-$1000"
  And I select brand "Dell"
  Then results update without page reload
  And I see "Showing 1-12 of 32 results"
  And all results match both filters
  And selected filters are highlighted
```

---

## The "Three Amigos" Practice

**Participants:**
- Product Owner (business perspective)
- Developer (technical perspective)
- Tester (quality perspective)

**Process:**
```
1. Review user story together
2. Discuss scenarios and examples
3. Identify edge cases
4. Write acceptance criteria collaboratively
5. Confirm shared understanding

Benefits:
✓ Catches ambiguities early
✓ Multiple perspectives ensure completeness
✓ Shared ownership of quality
✓ Reduces rework
```

**Example Session:**

```
Story: Password Reset

Product Owner: "Users should be able to reset password via email"

Developer: "What if the email doesn't exist in our system?"
→ Add scenario for invalid email

Tester: "What if they click the reset link after 24 hours?"
→ Add scenario for expired link

Developer: "What about rate limiting? Can they request 100 resets?"
→ Add scenario for rate limiting (max 3 per hour)

Tester: "What if they're already logged in?"
→ Add scenario for logged-in state

Product Owner: "Do we require specific password complexity?"
→ Add criteria for password requirements

Result: 5 scenarios covering happy path + edge cases
```

---

## Best Practices

### 1. Keep Scenarios Focused

```
❌ Complex scenario with multiple behaviors:
Given I'm logged in
When I add item to cart
And I update quantity to 3
And I remove another item
And I apply discount code
And I proceed to checkout
Then... [complex validation]

✓ Split into focused scenarios:

Scenario 1: Add item to cart
Scenario 2: Update item quantity
Scenario 3: Remove item from cart
Scenario 4: Apply discount code
Scenario 5: Checkout with discount
```

**Why:** Easier to test, debug, and maintain

### 2. Maintain Clear Separation of Given/When/Then

```
❌ Blurred separation:
Given I'm on the login page
When I enter credentials and click login
Then I'm logged in

✓ Clear separation:
Given I'm on the login page
When I enter valid credentials
And I click "Login"
Then I'm redirected to dashboard
And I see "Welcome back, [Name]"
And session cookie is set for 30 days
```

**Why:** Clearer intent, better for automation, easier to understand

### 3. Avoid UI-Specific Details

```
❌ Too UI-specific:
Then I see a blue button labeled "Submit" in the bottom-right corner
And there's a spinner icon when loading
And the font is 16px Helvetica

✓ Behavior-focused:
Then I see confirmation "Order placed successfully"
And I can download invoice as PDF
And order appears in "Order History"
```

**Why:** UI can change, behavior should remain stable

### 4. Include Edge Cases and Error Scenarios

```
Don't just test the happy path!

For any feature, consider:
✓ Success case (happy path)
✓ Validation errors
✓ Network failures
✓ Timeouts
✓ Permission issues
✓ Concurrent users
✓ Edge inputs (empty, max length, special characters)
```

**Example: File Upload**

```gherkin
Scenario: Successful file upload
  Given I'm on the upload page
  When I select a PDF file (2MB)
  And I click "Upload"
  Then I see upload progress bar
  And I see "Upload complete" within 5 seconds
  And file appears in my documents list

Scenario: Upload file exceeding size limit
  Given I'm on the upload page
  When I select a file larger than 10MB
  And I click "Upload"
  Then I see error "File too large. Maximum size is 10MB."
  And the file is not uploaded
  And I remain on the upload page

Scenario: Upload unsupported file type
  Given I'm on the upload page
  When I select an .exe file
  And I click "Upload"
  Then I see error "Unsupported file type. Please upload PDF, DOCX, or XLSX."
  And the file is not uploaded

Scenario: Upload fails due to network error
  Given I'm uploading a file
  When the network connection is lost mid-upload
  Then I see error "Upload failed. Please check your connection and try again."
  And I can retry the upload
  And the partial upload is cleaned up

Scenario: Malware detected in uploaded file
  Given I'm uploading a file
  When the file is scanned and malware is detected
  Then I see error "This file contains malware and cannot be uploaded."
  And the file is quarantined
  And security team is notified
```

### 5. Make Criteria Measurable and Testable

```
❌ Vague:
Then the page loads quickly
Then the user has a good experience
Then the design looks nice

✓ Measurable:
Then the page loads within 2 seconds (p95)
Then I see search results with >90% relevance
Then all elements pass WCAG 2.2 AA contrast requirements
```

### 6. Use Real Data and Examples

```
❌ Abstract:
Given I have some items in my cart
When I checkout
Then I see the total price

✓ Concrete:
Given I have 2 "Laptop Pro" ($999 each) in my cart
And I have 1 "Mouse" ($29) in my cart
When I proceed to checkout
Then I see subtotal: $2,027
And I see tax (8%): $162.16
And I see total: $2,189.16
```

**Why:** Concrete examples are easier to verify and automate

### 7. Cover Multiple User Roles

```
Different users may have different acceptance criteria:

Scenario: Admin can delete any comment
  Given I'm logged in as an admin
  When I view any user's comment
  Then I see "Delete" button
  And I can delete the comment
  And the user is notified

Scenario: Regular user can only delete own comments
  Given I'm logged in as a regular user
  When I view my own comment
  Then I see "Delete" button
  But when I view another user's comment
  Then I don't see "Delete" button
```

---

## Alternative Formats

### Rule-Oriented Format

For complex business rules, use a table:

```
Feature: Shipping Cost Calculation

| Order Total | Shipping Method | Destination | Shipping Cost |
|-------------|-----------------|-------------|---------------|
| $0-$25      | Standard        | US          | $5.99         |
| $0-$25      | Express         | US          | $12.99        |
| $25-$100    | Standard        | US          | $3.99         |
| $25-$100    | Express         | US          | $9.99         |
| $100+       | Standard        | US          | Free          |
| $100+       | Express         | US          | $6.99         |
| Any         | Any             | International| $19.99       |

Scenario: Calculate shipping for $30 order
  Given I have $30 worth of items in cart
  And I'm shipping to US address
  When I select "Standard Shipping"
  Then I see shipping cost: $3.99
```

### Checklist Format

For simpler features, a checklist may be sufficient:

```
## File Upload Acceptance Criteria

### Functional
- [ ] Supports file types: PDF, DOCX, XLSX
- [ ] Maximum file size: 10MB
- [ ] Shows upload progress bar (0-100%)
- [ ] Displays file name and size after upload
- [ ] Allows removing uploaded files before submission
- [ ] Scans files for malware before processing

### Validation & Errors
- [ ] Shows error for unsupported file types
- [ ] Shows error for files exceeding size limit
- [ ] Shows error for network failures with retry option
- [ ] Clears partially uploaded files on error

### Performance
- [ ] Upload completes within 10 seconds for 10MB file (WiFi)
- [ ] Supports multiple file uploads (up to 5 at once)

### Security
- [ ] Files are scanned for viruses/malware
- [ ] Files are stored with randomized names
- [ ] Only authenticated users can upload
- [ ] Files are encrypted at rest

### Accessibility
- [ ] Keyboard accessible (tab navigation, enter to select)
- [ ] Screen reader announces upload progress
- [ ] Error messages are read by screen readers
- [ ] Works with browser accessibility tools

### Cross-browser/Device
- [ ] Works on Chrome, Firefox, Safari, Edge (latest 2 versions)
- [ ] Works on iOS Safari and Android Chrome
- [ ] Responsive design (mobile, tablet, desktop)
```

---

## BDD Tools & Automation

### Gherkin Syntax

Gherkin is the language used for BDD scenarios:

```gherkin
Feature: User Login
  As a registered user
  I want to log in to my account
  So that I can access my personalized dashboard

  Background:
    Given the application is running
    And the database is seeded with test users

  Scenario: Successful login
    Given I'm on the login page
    When I enter username "john@example.com"
    And I enter password "SecurePass123"
    And I click "Login"
    Then I should see "Welcome back, John!"
    And I should be on the dashboard page

  Scenario Outline: Login with invalid credentials
    Given I'm on the login page
    When I enter username "<username>"
    And I enter password "<password>"
    And I click "Login"
    Then I should see error "<error_message>"

    Examples:
      | username            | password      | error_message              |
      | invalid@example.com | SecurePass123 | Invalid email or password  |
      | john@example.com    | wrongpass     | Invalid email or password  |
      |                     | SecurePass123 | Email is required          |
      | john@example.com    |               | Password is required       |
```

### Automation Tools

| Language | Tool | Description |
|----------|------|-------------|
| JavaScript/TypeScript | Cucumber.js | Gherkin-based BDD framework |
| JavaScript/TypeScript | Playwright | Modern E2E testing with BDD support |
| Python | Behave | Gherkin for Python |
| Ruby | Cucumber | Original BDD tool |
| Java | Cucumber JVM | Java implementation |
| C# | SpecFlow | .NET BDD framework |

### Example: Cucumber.js

```javascript
// features/login.feature
Feature: User Login

  Scenario: Successful login
    Given I'm on the login page
    When I enter email "user@example.com"
    And I enter password "SecurePass123"
    And I click "Login"
    Then I should see "Welcome back"

// features/step_definitions/login.steps.js
const { Given, When, Then } = require('@cucumber/cucumber');
const { expect } = require('chai');

Given('I\'m on the login page', async function() {
  await this.page.goto('https://example.com/login');
});

When('I enter email {string}', async function(email) {
  await this.page.fill('input[name="email"]', email);
});

When('I enter password {string}', async function(password) {
  await this.page.fill('input[name="password"]', password);
});

When('I click {string}', async function(buttonText) {
  await this.page.click(`button:has-text("${buttonText}")`);
});

Then('I should see {string}', async function(text) {
  const content = await this.page.textContent('body');
  expect(content).to.include(text);
});
```

---

## When NOT to Use Given-When-Then

GWT is not always the right format:

### 1. System-Level Requirements

```
❌ Given the system is deployed
When the server receives 10,000 requests/second
Then response time is < 100ms

✓ Better format:
Performance requirement: System must handle 10,000 req/s with p95 latency < 100ms
```

### 2. Non-Functional Requirements

```
❌ Given the user uploads a file
When malware is detected
Then the file is quarantined

✓ Better format:
Security requirement: All uploaded files must be scanned for malware before storage
```

### 3. Simple UI/UX Constraints

```
❌ Given I'm viewing a button
When the button is focused
Then it has a 2px blue outline

✓ Better format:
Accessibility: All interactive elements must have visible focus indicator (WCAG 2.2)
```

### 4. Technical Implementation Details

```
❌ Given the database is initialized
When a user record is created
Then it's stored in the users table with encrypted password

✓ Better format:
Technical requirement: User passwords must be hashed using bcrypt (cost factor 12)
```

---

## Templates

### Basic Template

```gherkin
Scenario: [Descriptive name]
  Given [precondition]
  When [action]
  Then [expected result]
```

### Extended Template

```gherkin
Scenario: [Descriptive name]
  Given [precondition 1]
  And [precondition 2]
  When [action 1]
  And [action 2]
  Then [expected result 1]
  And [expected result 2]
  But [exception or constraint]
```

### Scenario Outline Template

```gherkin
Scenario Outline: [Descriptive name with variable]
  Given [precondition with <variable>]
  When [action with <variable>]
  Then [expected result with <variable>]

  Examples:
    | variable1 | variable2 | variable3 |
    | value1    | value2    | value3    |
    | value4    | value5    | value6    |
```

---

## Checklist

```markdown
## Acceptance Criteria Quality Check

### Format & Structure
- [ ] Uses Given-When-Then format (or appropriate alternative)
- [ ] Clear separation of precondition, action, outcome
- [ ] One behavior per scenario
- [ ] Concrete examples, not abstract descriptions

### Coverage
- [ ] Happy path covered
- [ ] Error scenarios covered
- [ ] Edge cases identified
- [ ] Different user roles considered
- [ ] Performance criteria specified (if applicable)
- [ ] Security requirements included (if applicable)

### Clarity
- [ ] Testable and measurable
- [ ] No UI-specific implementation details
- [ ] Uses real data and examples
- [ ] Understandable by all team members
- [ ] No ambiguous language

### Technical
- [ ] Can be automated
- [ ] No blurred Given/When/Then boundaries
- [ ] Realistic scenarios (grounded in actual use)
- [ ] Linked to user story
- [ ] Reviewed by Three Amigos (PO, Dev, QA)
```

---

## Common Pitfalls

### 1. Implementation in Acceptance Criteria

```
❌ Then the API returns HTTP 200 with JSON payload containing user_id

✓ Then I see my profile information displayed correctly
```

### 2. Too Many Steps

```
❌ When I click A, then B, then C, then D, then E...

✓ Break into multiple scenarios
```

### 3. Vague Outcomes

```
❌ Then the user is happy
❌ Then it works correctly

✓ Then I see confirmation message "Order placed successfully"
✓ Then the order appears in "Order History" with status "Processing"
```

### 4. Missing Error Cases

```
❌ Only writing happy path

✓ Include: validation errors, timeouts, permission denied, etc.
```

### 5. Coupling to Current UI

```
❌ Then I see a modal dialog with a blue "OK" button

✓ Then I see confirmation dialog with option to proceed or cancel
```

---

## See Also

- [reference/user-stories.md](user-stories.md) — User story writing guide
- [templates/prd-template.md](../templates/prd-template.md) — Complete PRD template
- BDD documentation: https://cucumber.io/docs/bdd/
- Gherkin syntax: https://cucumber.io/docs/gherkin/
