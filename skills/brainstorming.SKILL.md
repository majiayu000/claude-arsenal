---
name: brainstorming
description: Collaborative design refinement through Socratic dialogue. Use when exploring ideas, designing features, or planning architecture. Not for mechanical implementation tasks.
---
# Brainstorming

> From [obra/superpowers](https://github.com/obra/superpowers)

## Purpose

Turn rough ideas into fully-formed designs through collaborative dialogue, NOT immediate implementation.

**Use for:** Exploring ideas, designing features, architecture decisions
**NOT for:** Clear mechanical processes with obvious implementation

## The Three Phases

### Phase 1: Understanding the Idea

1. **Review existing context**
   - Read relevant project files
   - Understand current architecture
   - Note constraints and requirements

2. **Ask clarifying questions**
   - ONE question at a time
   - Prefer multiple choice when possible
   - Open-ended questions are fine too
   - Wait for answer before next question

```
Good: "Should this feature support offline mode?
       A) Yes, full offline support
       B) Yes, limited offline (read-only)
       C) No, online only"

Bad: "What about offline support? And caching?
      Also, how should errors be handled?"
```

### Phase 2: Exploring Approaches

1. **Present 2-3 different solutions**
   - Each with clear trade-offs
   - Lead with recommended option
   - Explain reasoning

```markdown
## Approach A: Event-Driven (Recommended)
- Pros: Decoupled, scalable, easy to extend
- Cons: More complex debugging, eventual consistency
- Best for: Systems needing flexibility

## Approach B: Direct Integration
- Pros: Simple, immediate consistency
- Cons: Tight coupling, harder to scale
- Best for: Small, stable systems

## Approach C: Hybrid
- Pros: Balance of both
- Cons: Complexity of managing two patterns
- Best for: Gradual migration scenarios
```

2. **Discuss trade-offs**
   - Performance vs simplicity
   - Flexibility vs maintainability
   - Short-term vs long-term

### Phase 3: Presenting the Design

1. **Present in sections** (200-300 words each)
   - Architecture overview
   - Key components
   - Data flow
   - Error handling
   - Testing strategy

2. **Validate incrementally**
   - Get confirmation after each section
   - Adjust based on feedback
   - Don't dump everything at once

## Key Principles

### Ask Questions Sequentially

```
❌ Wrong:
"What's the expected load? How many users?
 What about mobile? Should it work offline?
 What's the budget? Timeline?"

✅ Right:
"What's the expected user load?
 A) <100 concurrent users
 B) 100-1000 concurrent users
 C) 1000+ concurrent users"
[Wait for answer]
"Given that load, should we prioritize...?"
```

### YAGNI Ruthlessly

Remove unnecessary features from ALL designs:
- Don't add "just in case" features
- Don't over-engineer for hypothetical scale
- Don't add flexibility that isn't needed yet

### Explore Before Deciding

Never jump to first solution:
- Consider at least 2-3 approaches
- Understand trade-offs of each
- Make informed recommendation

### Present Incrementally

Don't dump full design at once:
- Section by section
- Validate understanding
- Adjust as needed

## Follow-up Actions

After design is validated:

1. **Document the design**
   - Create design doc or ADR
   - Include key decisions and rationale

2. **Commit to version control**
   - Design docs belong in repo
   - Track changes over time

3. **Move to implementation planning**
   - Break into tasks
   - Estimate effort
   - Identify dependencies

## Example Session

```
User: "I want to add notifications to the app"