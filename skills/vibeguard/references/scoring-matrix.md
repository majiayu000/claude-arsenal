# Risk Scoring Matrix

Use this matrix to prioritize findings before implementation.

## Dimensions

Score each finding from 1 to 5.

### Impact
- 1: cosmetic or low-value cleanup
- 2: readability or minor developer-experience improvement
- 3: meaningful maintainability or correctness improvement
- 4: affects core behavior, data quality, or reliability
- 5: severe defect, major regression risk, or architecture-level issue

### Effort
- 1: tiny localized edit
- 2: small change across a few files
- 3: medium cross-module change
- 4: large refactor or migration
- 5: broad, high-cost system change

### Risk
- 1: very unlikely to regress
- 2: limited blast radius
- 3: requires targeted verification
- 4: touches critical paths or contracts
- 5: highly sensitive, compatibility-heavy, or hard to roll back

### Confidence
- 1: weak intuition only
- 2: indirect evidence
- 3: partial path or symptom evidence
- 4: strong code, test, or log evidence
- 5: fully traced and reproducible

## Formula

```text
priority_score = (impact * confidence) - (effort + risk)
```

Higher scores should be handled earlier.

## Priority Bands

| Band | Score | Meaning |
|------|-------|---------|
| P0 | 12+ | High-confidence, high-impact work |
| P1 | 4-11 | Valuable and actionable |
| P2 | 0-3 | Cleanup, follow-up, or lower urgency |
| P3 | Below 0 | Do not schedule without stronger evidence |

## Gating Rules

1. High-risk findings do not become P0 without strong evidence.
2. Low-confidence findings stay out of execution plans.
3. Re-score the backlog after major architectural changes.
4. If a fix is risky, add verification before widening scope.

## Template

```markdown
| id | finding | impact | effort | risk | confidence | score | priority |
|----|---------|--------|--------|------|------------|-------|----------|
| F1 | ...     | 5      | 2      | 2    | 5          | 21    | P0       |
| F2 | ...     | 3      | 3      | 3    | 4          | 6     | P1       |
```
