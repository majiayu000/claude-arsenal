# BDD Guide — 共享行为驱动开发参考

> 本文件被 fixflow 和 optflow 共同引用，修改时请同时考虑两个工作流的需求。

## 何时使用 BDD

Use BDD if user requests it, or if requirements are unclear.

If user says "I don't understand BDD", explain first in simple terms:
- BDD means defining expected behavior before coding.
- Use `Given / When / Then`:
  - Given: starting context.
  - When: action/event.
  - Then: observable result.

## BDD Lite (default mode)

Use this lightweight sequence unless user asks for full formal BDD:
1. Extract 2-5 key behaviors from the request.
2. Write one `Scenario` per behavior.
3. Map each `Then` to at least one verification step.
4. Implement code.
5. Run mapped checks and confirm each `Then` is satisfied.

Create scenarios before implementation:

```gherkin
Feature: <capability>
  Scenario: <business behavior>
    Given <initial state>
    When <user/system action>
    Then <expected outcome>
```

## Scenario Quality Checklist

Each scenario should satisfy all:
- Single behavior focus (no mixed goals in one scenario).
- Observable `Then` (not implementation detail).
- Explicit preconditions in `Given`.
- Explicit trigger in `When`.
- At least one failure or edge scenario for risky behavior.

## Scenario Outline (for data-driven behavior)

Use `Scenario Outline` when same behavior repeats with different inputs:

```gherkin
Feature: Search filtering
  Scenario Outline: Filter by item type and tags
    Given the knowledge base has items of multiple types
    When I search with type "<type>" and tag "<tag>"
    Then I only get items matching "<type>" and "<tag>"

    Examples:
      | type      | tag      |
      | knowledge | rust     |
      | skill     | backend  |
```

## Map BDD to Test Layers

- Unit tests: validate pure logic behind `Then`.
- Integration tests: validate cross-module contract behaviors.
- API/contract tests: validate request/response and error semantics.
- E2E/smoke tests: validate user-visible critical scenarios.

Minimum rule: every high-priority scenario must be covered by at least one automated check.

## BDD Template

```gherkin
Feature: <feature name>
  Scenario: <main behavior>
    Given <context>
    When <action>
    Then <expected result>
```

Optional outline template:

```gherkin
Feature: <feature name>
  Scenario Outline: <repeated behavior>
    Given <context>
    When <action using "<input>">
    Then <expected "<output>">

    Examples:
      | input | output |
      | ...   | ...    |
```
