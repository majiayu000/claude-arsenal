# Technology Selection & Evaluation

> Systematic framework for evaluating and selecting technologies, frameworks, and vendors.

## Why Systematic Evaluation Matters

**The cost of wrong technology choices**:
- Technical debt accumulates quickly
- Team productivity suffers
- Migration costs escalate over time
- Vendor lock-in limits flexibility

**The value of structured evaluation**:
- Reduces bias and gut-feel decisions
- Creates audit trail for future reference
- Aligns stakeholders on criteria
- Enables data-driven discussions

---

## Technology Evaluation Framework

### Six-Point Framework (Crosslake)

A business-driven, objective, and methodical framework for technology selection:

1. **Define Requirements** — What do you need?
2. **Identify Candidates** — What options exist?
3. **Establish Criteria** — How will you evaluate?
4. **Score & Weight** — Quantify each option
5. **Analyze Trade-offs** — Compare results
6. **Make Decision** — Document and commit

---

## Step 1: Define Requirements

### Functional Requirements

**What the technology must do**:

```markdown
## Functional Requirements

### Must Have (P0)
- [ ] Support 10K concurrent users
- [ ] REST API with OpenAPI spec
- [ ] Real-time data sync (WebSocket)
- [ ] Role-based access control
- [ ] Multi-tenancy support

### Should Have (P1)
- [ ] GraphQL API support
- [ ] Built-in caching
- [ ] Audit logging
- [ ] Batch processing

### Nice to Have (P2)
- [ ] Built-in admin UI
- [ ] Workflow engine
- [ ] Real-time analytics
```

### Non-Functional Requirements

**How it should perform**:

| Category | Requirement | Metric |
|----------|-------------|--------|
| **Performance** | Response time | <100ms (p95) |
| **Scalability** | Concurrent users | 10K active, 100K peak |
| **Availability** | Uptime | 99.9% (43 min downtime/month) |
| **Security** | Compliance | SOC 2, GDPR |
| **Reliability** | Data durability | 99.999999% (8 nines) |
| **Maintainability** | Learning curve | <1 week onboarding |

### Constraints

**What limits your choices**:

```markdown
## Constraints

### Budget
- One-time cost: <$10,000
- Annual cost: <$5,000/year
- Developer time: <2 weeks setup

### Technical
- Must run on AWS (no GCP/Azure)
- Must integrate with existing PostgreSQL
- Must support TypeScript

### Team
- Team size: 5 developers
- Skill level: Mid-level (2-5 years)
- No prior experience with technology X

### Timeline
- Production deployment: 3 months
- POC deadline: 2 weeks
```

---

## Step 2: Identify Candidates

### Research Methods

**1. Industry standards**:
- ThoughtWorks Tech Radar
- Stack Overflow Developer Survey
- GitHub trending projects
- Conference talks and blog posts

**2. Peer recommendations**:
- Ask in engineering communities
- LinkedIn polls
- Reddit (r/programming, language-specific subs)
- Team brainstorming

**3. Market research**:
- Gartner Magic Quadrant
- G2 reviews
- Vendor comparison sites

**4. Filtering criteria**:
- Active maintenance (commits in last 3 months)
- Reasonable adoption (>1K GitHub stars)
- Production-ready (v1.0+)
- Documentation quality

### Example: API Framework Selection

**Initial candidates**:
1. Express.js (Node.js)
2. FastAPI (Python)
3. Gin (Go)
4. Spring Boot (Java)
5. ASP.NET Core (C#)

**After filtering** (team knows TypeScript, needs high performance):
1. Express.js
2. Fastify (faster alternative to Express)
3. NestJS (TypeScript-native)

---

## Step 3: Establish Evaluation Criteria

### Weighted Scoring Matrix

Define categories and weights based on project priorities:

| Category | Weight | Rationale |
|----------|--------|-----------|
| **Performance** | 25% | High-traffic API (critical) |
| **Developer Experience** | 20% | Team productivity matters |
| **Ecosystem** | 15% | Need plugins, libraries |
| **Community** | 10% | Support and resources |
| **Cost** | 10% | Budget-conscious |
| **Security** | 10% | Standard requirement |
| **Scalability** | 10% | Future growth |

**Total**: 100%

### Scoring Scale

Use consistent 1-5 scale:

| Score | Meaning | Description |
|-------|---------|-------------|
| 5 | Excellent | Exceeds requirements, best in class |
| 4 | Good | Meets all requirements well |
| 3 | Acceptable | Meets minimum requirements |
| 2 | Poor | Partially meets requirements |
| 1 | Unacceptable | Does not meet requirements |

---

## Step 4: Score & Weight

### Technology Evaluation Matrix

**Example: API Framework Comparison**

| Criteria | Weight | Express.js | Fastify | NestJS |
|----------|--------|------------|---------|--------|
| **Performance** | 25% | | | |
| Request throughput | | 3 | 5 | 4 |
| Response latency | | 3 | 5 | 4 |
| Memory usage | | 4 | 5 | 3 |
| **Developer Experience** | 20% | | | |
| Learning curve | | 5 | 4 | 3 |
| TypeScript support | | 3 | 4 | 5 |
| Developer tools | | 4 | 3 | 5 |
| **Ecosystem** | 15% | | | |
| Available plugins | | 5 | 3 | 4 |
| Integration options | | 5 | 4 | 4 |
| **Community** | 10% | | | |
| GitHub stars | | 5 | 4 | 5 |
| Active contributors | | 5 | 4 | 4 |
| Stack Overflow questions | | 5 | 3 | 4 |
| **Cost** | 10% | | | |
| Licensing | | 5 | 5 | 5 |
| Training resources | | 5 | 4 | 4 |
| **Security** | 10% | | | |
| Security track record | | 4 | 4 | 4 |
| Vulnerability response | | 4 | 4 | 4 |
| **Scalability** | 10% | | | |
| Horizontal scaling | | 4 | 5 | 4 |
| Vertical scaling | | 4 | 5 | 4 |

### Weighted Score Calculation

```
Weighted Score = Σ (Category Weight × Average Score in Category)

Express.js:
- Performance: 25% × 3.33 = 0.83
- Dev Experience: 20% × 4.00 = 0.80
- Ecosystem: 15% × 5.00 = 0.75
- Community: 10% × 5.00 = 0.50
- Cost: 10% × 5.00 = 0.50
- Security: 10% × 4.00 = 0.40
- Scalability: 10% × 4.00 = 0.40
TOTAL: 4.18 / 5.00

Fastify:
- Performance: 25% × 5.00 = 1.25
- Dev Experience: 20% × 3.67 = 0.73
- Ecosystem: 15% × 3.50 = 0.53
- Community: 10% × 3.67 = 0.37
- Cost: 10% × 4.50 = 0.45
- Security: 10% × 4.00 = 0.40
- Scalability: 10% × 5.00 = 0.50
TOTAL: 4.23 / 5.00

NestJS:
- Performance: 25% × 3.67 = 0.92
- Dev Experience: 20% × 4.33 = 0.87
- Ecosystem: 15% × 4.00 = 0.60
- Community: 10% × 4.33 = 0.43
- Cost: 10% × 4.50 = 0.45
- Security: 10% × 4.00 = 0.40
- Scalability: 10% × 4.00 = 0.40
TOTAL: 4.07 / 5.00
```

**Result**: Fastify scores highest (4.23), but NestJS is close (4.07).

---

## Step 5: Analyze Trade-offs

### Qualitative Analysis

**Beyond the numbers, consider**:

#### Fastify (Highest Score)

**Strengths**:
- Best performance (2x faster than Express)
- Excellent for high-throughput APIs
- Modern plugin architecture

**Weaknesses**:
- Smaller ecosystem than Express
- Less Stack Overflow content
- Team has no experience

**Best for**: Performance-critical APIs, teams valuing speed

---

#### NestJS (Close Second)

**Strengths**:
- Best TypeScript support (built for TS)
- Opinionated structure (less bikeshedding)
- Built-in testing, validation, ORM
- Growing rapidly in popularity

**Weaknesses**:
- Slightly slower than Fastify
- Higher learning curve
- More "magic" (decorators, DI)

**Best for**: Teams wanting structure, TypeScript-first projects

---

#### Express.js (Baseline)

**Strengths**:
- Most mature and stable
- Huge ecosystem
- Team already knows it
- Tons of resources

**Weaknesses**:
- Performance lags behind newer frameworks
- Minimal structure (have to build everything)
- TypeScript is bolted on, not native

**Best for**: Teams prioritizing stability and familiarity

---

### Decision Matrix

| Factor | Express | Fastify | NestJS |
|--------|---------|---------|--------|
| **Quantitative score** | 4.18 | **4.23** | 4.07 |
| **Team familiarity** | ✅ High | ❌ None | ⚠️ Some |
| **Migration risk** | ✅ Low | ⚠️ Medium | ⚠️ Medium |
| **Long-term support** | ✅ Proven | ⚠️ Growing | ✅ Strong |
| **Hiring ease** | ✅ Easy | ⚠️ Harder | ✅ Growing |

---

## Step 6: Make Decision

### Document the Decision

Create an ADR (Architecture Decision Record):

```markdown
# ADR-007: Use NestJS for API Framework

## Status
Accepted (2025-12-18)

## Context
We need to select a Node.js API framework for our new microservices.

Requirements:
- High performance (10K concurrent users)
- TypeScript-first
- Built-in validation and testing
- Team wants opinionated structure

## Decision
We will use **NestJS** as our API framework.

## Rationale

**Scoring results**:
- Fastify: 4.23 (highest performance)
- NestJS: 4.07 (best TypeScript support)
- Express: 4.18 (most familiar)

**Why NestJS over Fastify**:
- Despite slightly lower score, NestJS provides:
  - Better developer experience (TypeScript-native)
  - Built-in structure reduces decision fatigue
  - Growing community and job market
  - Performance is "good enough" (4.5K req/s vs Fastify's 6K)

**Why NestJS over Express**:
- TypeScript support is first-class, not bolted-on
- Opinionated structure reduces bikeshedding
- Built-in features (DI, decorators, validation)

## Consequences

**Positive**:
- Team productivity from built-in features
- Consistent code structure across services
- Strong TypeScript support

**Negative**:
- 2-week learning curve
- More "magic" than Express (decorators, DI)
- Slightly lower performance than Fastify (acceptable for our scale)

**Mitigations**:
- Budget 2 weeks for team training
- Create internal best practices guide
- Start with one service, expand if successful
```

### Create Proof of Concept (POC)

**Before full commitment**:

```markdown
## POC Plan (2 weeks)

### Week 1: Build
- [ ] Implement user CRUD API
- [ ] Add authentication (JWT)
- [ ] Set up validation
- [ ] Write unit tests
- [ ] Add OpenAPI docs

### Week 2: Evaluate
- [ ] Load test (JMeter, k6)
- [ ] Measure developer experience
- [ ] Document learnings
- [ ] Team feedback session

### Success Criteria
- [ ] Meets performance target (>1K req/s)
- [ ] Team feels productive
- [ ] No major blockers discovered
- [ ] Documentation is adequate

### Go/No-Go Decision
- ✅ Go if: POC successful, team confident
- ❌ No-Go if: Performance issues, team struggles
```

---

## Common Evaluation Scenarios

### Scenario 1: Database Selection

**Criteria weights for OLTP workload**:

| Criteria | Weight | Reasoning |
|----------|--------|-----------|
| ACID compliance | 25% | Financial data, need consistency |
| Query performance | 20% | Complex queries |
| Scalability | 15% | Growth to 100K users |
| Developer experience | 15% | Team productivity |
| Cost | 10% | Budget constraint |
| Community | 10% | Long-term support |
| Cloud integration | 5% | Using AWS |

**Candidates**: PostgreSQL, MySQL, MongoDB, DynamoDB

---

### Scenario 2: Frontend Framework

**Criteria weights for dashboard app**:

| Criteria | Weight | Reasoning |
|----------|--------|-----------|
| Developer experience | 25% | Team productivity |
| Component ecosystem | 20% | Need charts, tables |
| Performance | 15% | Real-time data |
| TypeScript support | 15% | Type safety |
| Learning curve | 10% | Team is mid-level |
| Community | 10% | Resources |
| Mobile support | 5% | Responsive only |

**Candidates**: React, Vue, Svelte, Angular

---

### Scenario 3: Cloud Provider

**Criteria weights for startup**:

| Criteria | Weight | Reasoning |
|----------|--------|-----------|
| Cost | 25% | Bootstrap budget |
| Ease of use | 20% | Small team |
| Managed services | 20% | Reduce ops burden |
| Scalability | 15% | Growth potential |
| Global availability | 10% | US + EU users |
| Developer tools | 10% | CI/CD, monitoring |

**Candidates**: AWS, GCP, Azure, DigitalOcean

---

## Build vs Buy Decision Framework

### When to Build

```markdown
✅ Build if:
- Core differentiator for business
- Requirements are highly specific
- Existing solutions don't fit
- Team has expertise
- Long-term cost of buying is high
- Need full control and customization
```

### When to Buy (or use SaaS)

```markdown
✅ Buy/SaaS if:
- Not a core competency
- Mature solutions exist
- Time to market is critical
- Team lacks expertise
- Operational burden is high
- Compliance/security is complex
```

### Cost-Benefit Analysis

```markdown
## Build vs Buy: Authentication System

### Build (In-house)
**One-time costs**:
- Development: 4 weeks × $10K/week = $40K
- Security audit: $5K
Total: $45K

**Recurring costs**:
- Maintenance: 1 day/month × $500 = $6K/year
- Infrastructure: $100/month = $1.2K/year
Total: $7.2K/year

**3-year TCO**: $45K + (3 × $7.2K) = $66.6K

---

### Buy (Auth0)
**One-time costs**:
- Integration: 1 week × $10K = $10K
Total: $10K

**Recurring costs**:
- Auth0 Essentials: $240/month = $2,880/year
- Support: $500/year
Total: $3,380/year

**3-year TCO**: $10K + (3 × $3,380) = $20,140K

---

### Decision: Buy (Auth0)
**Savings**: $66.6K - $20.1K = $46.5K over 3 years

**Other factors**:
- ✅ Faster time to market (1 week vs 4 weeks)
- ✅ Lower risk (Auth0 is battle-tested)
- ✅ Less operational burden
- ✅ Compliance included (SOC 2, GDPR)
- ⚠️ Vendor lock-in (mitigated by OAuth 2.0 standards)
```

---

## Risk Assessment

### Technology Adoption Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Learning curve** | Medium | Training, pair programming |
| **Vendor lock-in** | High | Use standards (SQL, REST), avoid proprietary APIs |
| **Performance issues** | High | Load testing in POC |
| **Abandoned project** | Medium | Check commit frequency, corporate backing |
| **Security vulnerabilities** | Critical | Security audit, dependency scanning |
| **Scalability limits** | Medium | Load test beyond requirements |
| **Integration issues** | Medium | Test integrations in POC |
| **Team resistance** | Medium | Involve team in decision, provide training |

---

## Evaluation Checklist

### Before Starting
- [ ] Requirements are documented (functional, non-functional)
- [ ] Constraints are clear (budget, timeline, team skills)
- [ ] Stakeholders are identified
- [ ] Evaluation criteria are agreed upon

### During Evaluation
- [ ] At least 3 candidates identified
- [ ] Criteria are weighted objectively
- [ ] Scoring is evidence-based (not gut feel)
- [ ] Team members participate in scoring
- [ ] Trade-offs are analyzed qualitatively
- [ ] POC is conducted for top candidates

### After Decision
- [ ] Decision is documented (ADR)
- [ ] Rationale is clear and defensible
- [ ] Team is aligned and bought in
- [ ] Migration plan is created
- [ ] Success metrics are defined
- [ ] Review date is scheduled (3-6 months)

---

## Anti-Patterns

### ❌ Resume-Driven Development

**Problem**: Choosing technology to add to resume, not solve problem

**Solution**: Focus on requirements, not hype

---

### ❌ Analysis Paralysis

**Problem**: Spending months evaluating, never deciding

**Solution**: Set deadline (2-4 weeks max), use POC to reduce uncertainty

---

### ❌ Cargo Cult Engineering

**Problem**: "Netflix uses X, so we should too"

**Solution**: Netflix has Netflix-scale problems. You don't.

---

### ❌ Gut Feel Decisions

**Problem**: "I like Y, let's use it" without evaluation

**Solution**: Use structured framework, quantify trade-offs

---

### ❌ Ignoring Total Cost of Ownership

**Problem**: Choosing "free" open-source, ignoring maintenance cost

**Solution**: Calculate TCO (development + operations + maintenance)

---

### ❌ Single-Criteria Optimization

**Problem**: Choosing fastest framework, ignoring developer experience

**Solution**: Balance multiple criteria with weights

---

## Templates

### Technology Evaluation Spreadsheet

```csv
Criteria,Weight,Candidate A,Candidate B,Candidate C
Performance,25%,,,
- Throughput,,4,5,3
- Latency,,4,5,4
Developer Experience,20%,,,
- Learning curve,,5,3,4
- Tooling,,4,4,5
Ecosystem,15%,,,
- Libraries,,5,3,4
- Integrations,,5,4,4
Community,10%,,,
- GitHub stars,,5,4,5
- Active contributors,,5,4,4
Cost,10%,,,
- Licensing,,5,5,5
- Training,,5,4,4
Security,10%,,,
- Track record,,4,4,4
- Vulnerability response,,4,4,4
Scalability,10%,,,
- Horizontal scaling,,4,5,4
- Vertical scaling,,4,5,4
```

### POC Evaluation Template

See [templates/tech-evaluation-poc.md](../templates/tech-evaluation-poc.md) for detailed POC template.

---

## References

- [Crosslake: Six-Point Framework for Technology Selection](https://crosslaketech.com/a-six-point-framework-for-selecting-the-right-technology/)
- [Meegle: Technology Stack Evaluation Matrix](https://www.meegle.com/en_us/advanced-templates/enterprise_architecture/technology_stack_evaluation_matrix)
- [Larksuite: Decision Matrix for IT Teams](https://www.larksuite.com/en_us/topics/project-management-methodologies-for-functional-teams/decision-matrix-for-information-technology-teams)
- [ThoughtWorks Tech Radar](https://www.thoughtworks.com/radar)
- [Stack Overflow Developer Survey](https://insights.stackoverflow.com/survey)
