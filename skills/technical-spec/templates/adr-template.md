# ADR-XXX: [Short Title of Decision]

## Status
Proposed | Accepted | Deprecated | Superseded

**Date**: YYYY-MM-DD

**Supersedes**: [ADR-YYY](./YYY-previous-decision.md) _(if applicable)_

**Superseded by**: [ADR-ZZZ](./ZZZ-new-decision.md) _(if applicable)_

---

## Context

[Describe the context and background of the decision. What problem are we trying to solve? What constraints do we have?]

**Problem Statement**:
[1-2 paragraphs describing the problem]

**Requirements**:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Constraints**:
- [Constraint 1: e.g., budget, timeline, team skills]
- [Constraint 2]
- [Constraint 3]

**Current Situation** _(if applicable)_:
[Describe what exists today and why it's insufficient]

---

## Considered Options

### Option 1: [Name]

**Description**:
[How this option works]

**Pros**:
- ✅ [Advantage 1]
- ✅ [Advantage 2]
- ✅ [Advantage 3]

**Cons**:
- ❌ [Disadvantage 1]
- ❌ [Disadvantage 2]
- ❌ [Disadvantage 3]

**Cost/Effort**:
[Time, money, or complexity estimate]

---

### Option 2: [Name]

**Description**:
[How this option works]

**Pros**:
- ✅ [Advantage 1]
- ✅ [Advantage 2]
- ✅ [Advantage 3]

**Cons**:
- ❌ [Disadvantage 1]
- ❌ [Disadvantage 2]
- ❌ [Disadvantage 3]

**Cost/Effort**:
[Time, money, or complexity estimate]

---

### Option 3: [Name]

[Repeat for additional options]

---

## Decision

We will use **[Chosen Option]**.

### Rationale

[Explain why this option was selected over the alternatives. Reference specific requirements or constraints.]

**Key factors in the decision**:
1. [Factor 1: e.g., "Meets performance requirements while staying within budget"]
2. [Factor 2: e.g., "Team already has expertise in this technology"]
3. [Factor 3: e.g., "Lowest long-term maintenance burden"]

**Trade-offs accepted**:
- [Trade-off 1: What we're giving up for this choice]
- [Trade-off 2]

---

## Consequences

### Positive Consequences

- ✅ [Benefit 1]
- ✅ [Benefit 2]
- ✅ [Benefit 3]

### Negative Consequences

- ❌ [Drawback 1]
- ❌ [Drawback 2]
- ❌ [Drawback 3]

### Mitigations

[How we'll address the negative consequences]

| Negative Consequence | Mitigation Strategy |
|---------------------|---------------------|
| [Drawback 1] | [How we'll mitigate] |
| [Drawback 2] | [How we'll mitigate] |

### Neutral Consequences

- [Consequence that's neither good nor bad]
- [Another neutral impact]

---

## Implementation Notes

[Optional: Any important details about implementing this decision]

**Key actions**:
- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Action item 3]

**Timeline**:
- [Milestone 1]: [Date]
- [Milestone 2]: [Date]

**Dependencies**:
- [Dependency 1]
- [Dependency 2]

---

## Related ADRs

- [ADR-YYY: Related Decision 1](./YYY-related-decision.md)
- [ADR-ZZZ: Related Decision 2](./ZZZ-another-decision.md)

---

## References

- [External article or documentation](https://example.com)
- [Internal design doc](../design/design-doc.md)
- [Vendor comparison](https://example.com/comparison)

---

## Review & Approval

**Reviewers**:
- @tech-lead: Approved | Rejected | Comments
- @team-member-1: Approved | Rejected | Comments
- @security-team: Approved | Rejected | Comments

**Discussion**: [Link to discussion thread, if applicable]

**Approval Date**: YYYY-MM-DD

---

## Revisions

| Date | Author | Change |
|------|--------|--------|
| YYYY-MM-DD | @author | Initial draft |
| YYYY-MM-DD | @author | Updated based on feedback |
| YYYY-MM-DD | @author | Accepted |

---

## Alternative Templates

### Y-Statement Format (Compact)

Use this simplified format for straightforward decisions:

```markdown
# ADR-XXX: [Title]

## Status
Accepted

## Decision Statement

In the context of [use case/user story],
facing [concern],
we decided for [option]
to achieve [quality],
accepting [downside].

## Consequences

**Benefits**:
- [Benefit 1]
- [Benefit 2]

**Risks**:
- [Risk 1]
- [Risk 2]

**Mitigations**:
- [How we mitigate risks]
```

---

### Michael Nygard Format (Original)

Use this format for complex architectural decisions:

```markdown
# ADR-XXX: [Title]

## Status
Accepted

## Context

[Describe the forces at play: technical, political, social, project-local.
These forces are probably in tension and should be called out as such.
Leave no stone unturned: look at both sides of every trade-off.]

## Decision

[Describe the response to the forces. State the decision in full sentences,
with active voice: "We will ..."]

## Consequences

[Describe the resulting context after applying the decision. All consequences
should be listed, not just the "positive" ones. A decision may have positive,
negative, and neutral consequences.]
```

---

## Tips for Writing Good ADRs

1. **Keep it short** — 1-2 pages maximum
2. **Focus on the decision** — Not implementation details
3. **Show your work** — Include alternatives considered
4. **Be specific** — Avoid vague language
5. **Make it searchable** — Use clear titles and keywords
6. **Immutable after acceptance** — Change status, don't edit content
7. **Link to related docs** — Design docs, other ADRs
8. **Include dates** — When decided, when superseded
9. **Get peer review** — Multiple perspectives improve decisions
10. **Update status** — Keep status current (Proposed → Accepted → Superseded)
