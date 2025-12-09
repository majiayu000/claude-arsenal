---
name: test-driven-development
description: Enforces TDD discipline with RED-GREEN-REFACTOR cycle. Use when writing new features, fixing bugs, or refactoring code. Ensures tests genuinely verify behavior.
---
# Test-Driven Development (TDD)

> From [obra/superpowers](https://github.com/obra/superpowers)

## Core Principle

Write tests before implementation. Watch them fail. Write minimal code to pass.

**THE IRON LAW: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**

## When to Apply TDD

- New features
- Bug fixes
- Refactoring
- Any behavior changes

## The Red-Green-Refactor Cycle

### RED: Write a Failing Test

1. Write ONE minimal test demonstrating desired behavior
2. Use clear, descriptive test names
3. Use real code, avoid unnecessary mocks
4. Test should fail for the RIGHT reason

```
# Verify RED
- Run the test
- Confirm it fails
- Confirm failure is NOT due to syntax errors
- Confirm you're not testing existing functionality
```

### GREEN: Make It Pass

1. Write the SIMPLEST code that makes the test pass
2. Don't add extra features
3. Don't optimize yet
4. Just make it work

```
# Verify GREEN
- Run all tests
- Confirm new test passes
- Confirm no other tests broke
```

### REFACTOR: Clean Up

1. Improve code quality while keeping tests green
2. Remove duplication
3. Improve naming
4. Extract helpers if needed
5. Run tests after each change

## Why This Order Matters

Tests written AFTER implementation:
- Pass immediately (proves nothing)
- You never see them fail
- Cannot verify they test what matters
- Manual testing is NOT a substitute

## Common Rationalizations to REJECT

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code still breaks |
| "I'll write tests after" | Post-implementation tests pass immediately |
| "Already manually tested" | Manual testing lacks systematic rigor |
| "Deleting work is wasteful" | Unverified code is technical debt |
| "Keep as reference" | You'll adapt it; that's testing-after |

## Red Flags Requiring RESTART

If any of these occur, DELETE the code and start over:

- Writing code before tests
- Tests passing immediately on first run
- Rationalizing "just this once"
- Planning to "test later"
- Keeping pre-written code "as reference"

## Example Workflow

```bash
# 1. RED - Write failing test
def test_user_can_login_with_valid_credentials():
    user = create_user(email="test@example.com", password="secret")
    result = login(email="test@example.com", password="secret")
    assert result.success == True
    assert result.user == user

# 2. Run test - MUST FAIL
# 3. GREEN - Implement minimal code
def login(email, password):
    user = User.find_by_email(email)
    if user and user.check_password(password):
        return LoginResult(success=True, user=user)
    return LoginResult(success=False, user=None)

# 4. Run test - MUST PASS
# 5. REFACTOR - Clean up if needed
```

## Summary

1. Write test first
2. Watch it fail
3. Write minimal code to pass
4. Refactor while green
5. Repeat
