# Risk-Impact Scoring

Use this matrix to prioritize redundancy findings into execution phases.

## Scoring Dimensions

Rate each finding from 1 to 5:

- `impact`
  - 1: negligible
  - 3: moderate maintainability/correctness gain
  - 5: major correctness/architecture gain

- `effort`
  - 1: tiny localized change
  - 3: moderate multi-file change
  - 5: large cross-cutting change

- `risk`
  - 1: low regression risk
  - 3: medium risk requiring targeted tests
  - 5: high regression risk and compatibility sensitivity

- `confidence`
  - 1: weak evidence
  - 3: moderate evidence
  - 5: strong evidence from call paths/tests/warnings

## Priority Formula

Use:

`priority_score = (impact * confidence) - (effort + risk)`

Interpretation:
- Higher score => earlier execution.
- Negative score => hold for later phase unless mandatory for blocking reason.

## Phase Mapping

- `P0` (must do first)
  - High impact and high confidence, often correctness or entry-point drift.
- `P1` (high value next)
  - Meaningful maintainability wins with controlled risk.
- `P2` (cleanup/finalize)
  - Low impact or low confidence cleanup tasks.

## Example Table Template

```md
| id | finding | impact | effort | risk | confidence | score | phase |
|----|---------|--------|--------|------|------------|-------|-------|
| F1 | ...     | 5      | 2      | 2    | 5          | 21    | P0    |
| F2 | ...     | 3      | 3      | 3    | 4          | 6     | P1    |
```

## Gating Rules

- Do not schedule low-confidence high-risk changes before obtaining stronger evidence.
- Insert guard tests before refactoring high-risk P0/P1 findings.
- Re-score remaining findings after each phase if architecture assumptions change.
