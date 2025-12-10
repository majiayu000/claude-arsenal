---
name: comprehensive-testing
description: Complete testing strategy covering TDD workflow, test pyramid, unit/integration/E2E/property testing, framework best practices (Jest, Vitest, pytest), mock strategies, and CI integration. Use when writing tests, reviewing test quality, or establishing testing standards.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---
# Comprehensive Testing

> Based on [Anthropic's Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) and community patterns

## Core Philosophy

> "Claude performs best when it has a clear target to iterate against—a test case provides concrete success criteria."

Testing is not about proving code works; it's about **designing code that is testable** and **documenting expected behavior**.

---

## Test Pyramid

```
        /\
       /  \        E2E Tests (10%)
      /----\       - Full user flows
     /      \      - Slowest, most brittle
    /--------\
   /          \    Integration Tests (20%)
  /------------\   - Component interaction
 /              \  - Real dependencies
/----------------\
       Unit Tests (70%)
       - Single function/method
       - Fast, isolated, many
```

| Level | Speed | Scope | When to Use |
|-------|-------|-------|-------------|
| Unit | <10ms | Single function | All logic |
| Integration | <1s | Multiple components | APIs, DB |
| E2E | <30s | Full flow | Critical paths |

---

## TDD Workflow (Anthropic Recommended)

### The 6-Step Process

```
1. WRITE TESTS FIRST
   ↓
2. VERIFY TESTS FAIL
   ↓
3. COMMIT TEST SUITE
   ↓
4. IMPLEMENT CODE
   ↓
5. VERIFY WITH SUBAGENT
   ↓
6. COMMIT IMPLEMENTATION
```

### Step 1: Write Tests First

```markdown
Be EXPLICIT about TDD to avoid mock implementations:

"I want to implement [feature] using TDD.
First, write tests for [expected behavior] with these input/output pairs:
- Input: X → Expected: Y
- Input: A → Expected: B
Do NOT create any implementation yet."
```

### Step 2: Verify Tests Fail

```bash
# Run tests and confirm they fail for the RIGHT reason
npm test  # or pytest, go test, etc.

# Expected: "function not found" or "undefined"
# NOT: syntax error, wrong import
```

### Step 3: Commit Test Suite

```bash
git add tests/
git commit -m "test: Add tests for [feature] (RED phase)"
```

### Step 4: Implement Incrementally

```markdown
"Now implement the code to make these tests pass.
Do NOT modify the tests.
Run tests after each change until all pass."
```

Claude will enter an autonomous loop:
```
Write code → Run tests → Analyze failures → Adjust → Repeat
```

### Step 5: Verify with Subagent

```markdown
"Use a subagent to independently verify the implementation:
- Is it overfitting to tests?
- Are edge cases handled?
- Is the code maintainable?"
```

### Step 6: Commit Implementation

```bash
git add src/
git commit -m "feat: Implement [feature] (GREEN phase)"
```

---

## Test Structure Patterns

### AAA Pattern (Arrange-Act-Assert)

```typescript
describe('UserService', () => {
  it('should create user with valid email', async () => {
    // Arrange - Setup test data and dependencies
    const userRepo = new InMemoryUserRepository();
    const service = new UserService(userRepo);
    const input = { email: 'test@example.com', name: 'Test' };

    // Act - Execute the code under test
    const user = await service.create(input);

    // Assert - Verify the results
    expect(user.email).toBe('test@example.com');
    expect(user.id).toBeDefined();
    expect(await userRepo.findById(user.id)).toEqual(user);
  });
});
```

### Given-When-Then Pattern

```python
def test_order_total_with_discount():
    """
    Given an order with items totaling $100
    When a 20% discount is applied
    Then the total should be $80
    """
    # Given
    order = Order()
    order.add_item(Item(price=50))
    order.add_item(Item(price=50))

    # When
    order.apply_discount(Percentage(20))

    # Then
    assert order.total == Money(80)
```

---

## Framework Best Practices

### Jest / Vitest (JavaScript/TypeScript)

```typescript
// Structure
describe('ModuleName', () => {
  describe('methodName', () => {
    it('should [expected behavior] when [condition]', () => {});
  });
});

// Setup/Teardown
beforeAll(async () => { /* one-time setup */ });
beforeEach(() => { /* per-test setup */ });
afterEach(() => { /* per-test cleanup */ });
afterAll(async () => { /* one-time cleanup */ });

// Async testing
it('handles async operations', async () => {
  const result = await asyncFunction();
  expect(result).toBe(expected);
});

// Error testing
it('throws on invalid input', () => {
  expect(() => validate(null)).toThrow('Input required');
});

// Snapshot testing (use sparingly)
it('renders correctly', () => {
  const tree = renderer.create(<Component />).toJSON();
  expect(tree).toMatchSnapshot();
});

// Table-driven tests
it.each([
  [1, 1, 2],
  [2, 2, 4],
  [0, 0, 0],
])('add(%i, %i) = %i', (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});
```

**vitest.config.ts:**
```typescript
export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        lines: 80,
        branches: 70,
        functions: 80,
      },
    },
  },
});
```

### pytest (Python)

```python
import pytest
from mymodule import Calculator

# Fixtures for dependency injection
@pytest.fixture
def calculator():
    return Calculator()

@pytest.fixture
def database():
    db = TestDatabase()
    yield db
    db.cleanup()

# Parametrized tests
@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (2, 2, 4),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(calculator, a, b, expected):
    assert calculator.add(a, b) == expected

# Exception testing
def test_divide_by_zero(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(1, 0)

# Async testing
@pytest.mark.asyncio
async def test_async_operation():
    result = await async_function()
    assert result == expected

# Markers for categorization
@pytest.mark.slow
@pytest.mark.integration
def test_database_connection(database):
    assert database.is_connected()
```

**conftest.py:**
```python
import pytest

@pytest.fixture(scope="session")
def database_url():
    return "postgresql://test:test@localhost/test"

@pytest.fixture(autouse=True)
def reset_database(database):
    yield
    database.rollback()
```

**pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --cov=src --cov-report=term-missing
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

### Go Testing

```go
package mypackage

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 1, 2, 3},
        {"zero values", 0, 0, 0},
        {"negative numbers", -1, -2, -3},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            assert.Equal(t, tt.expected, result)
        })
    }
}

// Table-driven with subtests
func TestUserService_Create(t *testing.T) {
    t.Run("creates user with valid input", func(t *testing.T) {
        repo := NewInMemoryRepo()
        svc := NewUserService(repo)

        user, err := svc.Create(CreateUserInput{Email: "test@example.com"})

        require.NoError(t, err)
        assert.NotEmpty(t, user.ID)
        assert.Equal(t, "test@example.com", user.Email)
    })

    t.Run("returns error for invalid email", func(t *testing.T) {
        repo := NewInMemoryRepo()
        svc := NewUserService(repo)

        _, err := svc.Create(CreateUserInput{Email: "invalid"})

        require.Error(t, err)
        assert.Contains(t, err.Error(), "invalid email")
    })
}
```

---

## Mock Strategy

### When to Mock

| Scenario | Mock? | Reason |
|----------|-------|--------|
| External APIs | ✅ Yes | Slow, unreliable, costs money |
| Time/Date | ✅ Yes | Non-deterministic |
| Random | ✅ Yes | Non-deterministic |
| Database (unit) | ✅ Yes | Slow, complex setup |
| Database (integration) | ❌ No | Test real behavior |
| Your own code | ⚠️ Rarely | Prefer real implementations |
| File system | ⚠️ Depends | Use temp dirs when possible |

### How to Mock

```typescript
// Jest - Mock module
jest.mock('./emailService', () => ({
  sendEmail: jest.fn().mockResolvedValue({ success: true }),
}));

// Jest - Mock function
const mockCallback = jest.fn();
mockCallback.mockReturnValue(42);

// Vitest - Spy
import { vi } from 'vitest';
const spy = vi.spyOn(console, 'log');

// Time mocking
beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date('2024-01-01'));
});

afterEach(() => {
  vi.useRealTimers();
});
```

```python
# pytest - Mock with unittest.mock
from unittest.mock import Mock, patch, MagicMock

@patch('mymodule.external_api.fetch')
def test_with_mocked_api(mock_fetch):
    mock_fetch.return_value = {'data': 'mocked'}
    result = my_function()
    assert result == expected
    mock_fetch.assert_called_once_with('expected_arg')

# Fixture-based mock
@pytest.fixture
def mock_email_service():
    service = Mock()
    service.send.return_value = True
    return service
```

### Prefer Test Doubles Over Mocks

```typescript
// ❌ Heavy mocking
const mockRepo = {
  findById: jest.fn().mockResolvedValue({ id: '1', name: 'Test' }),
  save: jest.fn().mockResolvedValue(undefined),
  delete: jest.fn().mockResolvedValue(undefined),
};

// ✅ In-memory implementation (test double)
class InMemoryUserRepository implements UserRepository {
  private users: Map<string, User> = new Map();

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) || null;
  }

  async save(user: User): Promise<User> {
    this.users.set(user.id, user);
    return user;
  }

  async delete(id: string): Promise<void> {
    this.users.delete(id);
  }
}
```

---

## Boundary Testing

### Test These Boundaries

```typescript
describe('boundary testing', () => {
  // Null/Undefined
  it('handles null input', () => {
    expect(() => process(null)).toThrow('Input required');
  });

  // Empty values
  it('handles empty string', () => {
    expect(validate('')).toBe(false);
  });

  it('handles empty array', () => {
    expect(sum([])).toBe(0);
  });

  // Zero values
  it('handles zero', () => {
    expect(divide(0, 5)).toBe(0);
  });

  it('handles divide by zero', () => {
    expect(() => divide(5, 0)).toThrow('Division by zero');
  });

  // Boundary values
  it('handles minimum value', () => {
    expect(clamp(Number.MIN_SAFE_INTEGER, 0, 100)).toBe(0);
  });

  it('handles maximum value', () => {
    expect(clamp(Number.MAX_SAFE_INTEGER, 0, 100)).toBe(100);
  });

  // Off-by-one
  it('includes boundary', () => {
    expect(isInRange(10, 0, 10)).toBe(true);  // inclusive
  });

  it('excludes just outside boundary', () => {
    expect(isInRange(11, 0, 10)).toBe(false);
  });

  // Type coercion
  it('handles string numbers', () => {
    expect(parsePositiveInt('42')).toBe(42);
    expect(() => parsePositiveInt('abc')).toThrow();
  });

  // Unicode/Special chars
  it('handles unicode', () => {
    expect(normalize('héllo')).toBe('hello');
  });

  it('handles emoji', () => {
    expect(charCount('👨‍👩‍👧‍👦')).toBe(1); // grapheme cluster
  });
});
```

### Error Scenario Checklist

```markdown
- [ ] Network failure
- [ ] Timeout
- [ ] Invalid input format
- [ ] Missing required fields
- [ ] Unauthorized access
- [ ] Resource not found
- [ ] Concurrent modification
- [ ] Disk full
- [ ] Out of memory
- [ ] Rate limit exceeded
```

---

## Property-Based Testing

### Concept

Instead of specific examples, define **properties that must hold for all inputs**.

```typescript
import fc from 'fast-check';

// Property: reversing twice returns original
test('reverse is involutory', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const reversed = reverse(reverse(arr));
      return deepEquals(arr, reversed);
    })
  );
});

// Property: sorted array is always ordered
test('sort produces ordered output', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted = sort(arr);
      for (let i = 1; i < sorted.length; i++) {
        if (sorted[i] < sorted[i - 1]) return false;
      }
      return true;
    })
  );
});

// Property: encoding then decoding returns original
test('JSON roundtrip', () => {
  fc.assert(
    fc.property(fc.jsonValue(), (value) => {
      const encoded = JSON.stringify(value);
      const decoded = JSON.parse(encoded);
      return deepEquals(value, decoded);
    })
  );
});
```

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    """Sorting twice gives same result as sorting once"""
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.text())
def test_encode_decode_roundtrip(s):
    """Base64 encoding/decoding preserves data"""
    encoded = base64.b64encode(s.encode())
    decoded = base64.b64decode(encoded).decode()
    assert decoded == s
```

---

## Async Testing

### Patterns

```typescript
// Wait for promise
it('resolves with data', async () => {
  const result = await fetchData();
  expect(result).toBeDefined();
});

// Wait for rejection
it('rejects with error', async () => {
  await expect(failingOperation()).rejects.toThrow('Error message');
});

// Timeout handling
it('times out after 5s', async () => {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);

  try {
    await fetch(url, { signal: controller.signal });
  } finally {
    clearTimeout(timeout);
  }
}, 10000);

// Polling/Retry
it('eventually succeeds', async () => {
  await waitFor(async () => {
    const status = await getStatus();
    expect(status).toBe('ready');
  }, { timeout: 5000, interval: 100 });
});

// ❌ NEVER use fixed sleep
it('bad: uses sleep', async () => {
  await doSomething();
  await sleep(1000);  // NEVER DO THIS
  expect(result).toBe(expected);
});

// ✅ Use proper waiting
it('good: polls for condition', async () => {
  await doSomething();
  await waitFor(() => expect(getResult()).toBe(expected));
});
```

---

## Test Data Management

### Fixtures

```typescript
// Shared test data
const fixtures = {
  validUser: {
    id: 'user-1',
    email: 'test@example.com',
    name: 'Test User',
  },
  adminUser: {
    id: 'admin-1',
    email: 'admin@example.com',
    name: 'Admin User',
    role: 'admin',
  },
};
```

### Factories

```typescript
// Factory function
function createUser(overrides: Partial<User> = {}): User {
  return {
    id: `user-${Math.random().toString(36).slice(2)}`,
    email: 'test@example.com',
    name: 'Test User',
    createdAt: new Date(),
    ...overrides,
  };
}

// Usage
const user = createUser({ email: 'custom@example.com' });
```

### Builders

```typescript
class UserBuilder {
  private user: Partial<User> = {};

  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  withRole(role: Role): this {
    this.user.role = role;
    return this;
  }

  asAdmin(): this {
    return this.withRole('admin');
  }

  build(): User {
    return {
      id: this.user.id ?? generateId(),
      email: this.user.email ?? 'test@example.com',
      name: this.user.name ?? 'Test User',
      role: this.user.role ?? 'user',
      createdAt: new Date(),
    };
  }
}

// Usage
const admin = new UserBuilder().withEmail('admin@test.com').asAdmin().build();
```

---

## Coverage Strategy

### Targets

| Metric | Minimum | Target | Critical Path |
|--------|---------|--------|---------------|
| Line | 70% | 80% | 100% |
| Branch | 60% | 70% | 100% |
| Function | 70% | 80% | 100% |

### What to Cover First

```markdown
1. Business-critical logic
2. Complex algorithms
3. Error handling paths
4. Edge cases
5. Integration points
```

### What NOT to Cover

```markdown
- Third-party library code
- Generated code
- Configuration files
- Type definitions only
- Trivial getters/setters
```

---

## CI Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
          fail_ci_if_error: true

      - name: Check coverage thresholds
        run: |
          npm test -- --coverage --coverageThreshold='{
            "global": {
              "lines": 80,
              "branches": 70
            }
          }'
```

---

## Anti-Patterns to Avoid

```markdown
❌ Testing implementation, not behavior
   - Don't verify internal method calls
   - Test observable outputs only

❌ Over-mocking
   - Mocking everything tests nothing
   - Prefer real implementations or test doubles

❌ Test interdependence
   - Tests must run in any order
   - Each test must be isolated

❌ Hardcoded time
   - Use clock mocking
   - Inject time source

❌ Sleep/delay in tests
   - Use polling or async/await
   - Condition-based waiting

❌ Ignoring flaky tests
   - Fix or delete, never skip
   - Flaky tests erode trust

❌ Too much test setup
   - Indicates code design issues
   - Refactor code, not just tests

❌ Testing private methods
   - Test through public interface
   - If hard to test, refactor
```

---

## Testing Checklist

```markdown
## Before Writing Tests
- [ ] Understood requirements
- [ ] Identified test cases
- [ ] Determined test type (unit/integration/E2E)
- [ ] Planned test data

## Writing Tests
- [ ] Follows AAA or Given-When-Then
- [ ] Descriptive test names
- [ ] One assertion per concept
- [ ] Tests behavior, not implementation
- [ ] Covers happy path
- [ ] Covers error cases
- [ ] Covers boundary conditions

## Test Quality
- [ ] Tests are deterministic
- [ ] Tests are isolated
- [ ] Tests are fast
- [ ] No hardcoded values that will break
- [ ] Proper mocking (not over-mocking)

## Coverage
- [ ] Line coverage ≥ 80%
- [ ] Branch coverage ≥ 70%
- [ ] Critical paths at 100%

## CI/CD
- [ ] Tests run on every push
- [ ] Coverage reported
- [ ] Thresholds enforced
```

---

## Key Principles

1. **Tests are documentation** — They describe expected behavior
2. **Fast feedback** — Tests should run in seconds
3. **Deterministic** — Same input, same result, every time
4. **Independent** — No test depends on another
5. **Focused** — One test, one concept
6. **Maintainable** — Test code is production code

---

## Sources

- [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [TDD with Claude Code](https://thenewstack.io/claude-code-and-the-art-of-test-driven-development/)
- [Property-Based Fuzzing](https://www.mayhem.security/blog/property-based-fuzzing)
- [wshobson/agents Testing Patterns](https://github.com/wshobson/agents)
