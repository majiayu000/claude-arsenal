# Market Research

## TAM/SAM/SOM Framework

### Definitions

```markdown
TAM (Total Addressable Market)
→ The total market demand for a product/service
→ Entire universe of potential customers
→ Assumes no limitations (geography, price, distribution)

SAM (Serviceable Available Market)
→ Segment of TAM you can realistically target and serve
→ Accounts for geography, pricing, distribution constraints
→ The portion accessible to your business

SOM (Serviceable Obtainable Market)
→ Portion of SAM you can realistically capture
→ Based on competition, marketing/sales capabilities, market saturation
→ Your actual near-term opportunity (1-3 years)
```

### Calculation Methods

#### Top-Down Approach

```markdown
## Method
Start with industry reports and market research
Use third-party data (Gartner, Statista, IBISWorld)
Apply filters to narrow down

## Example: SaaS Project Management Tool
TAM = Global project management software market
    = $7.5 billion (per Gartner 2025)

SAM = Enterprise segment in North America
    = $7.5B × 40% (enterprise) × 30% (North America)
    = $900 million

SOM = Market share we can capture in Year 3
    = $900M × 3% (conservative market share)
    = $27 million

## Pros & Cons
✓ Fast, uses existing research
✓ Good for board presentations
✗ Less credible to investors (hand-wavy)
✗ Ignores your specific go-to-market
```

#### Bottom-Up Approach (Recommended)

```markdown
## Method
Calculate from the ground up using real data
Start with addressable customers and revenue per customer

## Formula
Market Size = # of potential customers × Average annual revenue per customer

## Example: B2B Analytics Platform
TAM:
- Total companies with 50+ employees in target countries
- 2 million companies
- Average contract value: $10,000/year
- TAM = 2M × $10,000 = $20 billion

SAM:
- Companies in our verticals (SaaS, e-commerce, fintech)
- 400,000 companies
- SAM = 400K × $10,000 = $4 billion

SOM (Year 1-3):
- Realistic customers we can acquire with our GTM
- Year 1: 100 customers = $1M
- Year 2: 500 customers = $5M
- Year 3: 2,000 customers = $20M

## Pros & Cons
✓ More credible to investors
✓ Based on specific, realistic assumptions
✓ Ties to your actual GTM strategy
✗ Requires more research
✗ Harder to estimate early-stage
```

### Calculating SOM

```markdown
## Method 1: Market Share
SOM = SAM × Expected market share

Example:
- SAM = $4 billion
- Expected market share in Year 3 = 0.5%
- SOM = $4B × 0.005 = $20 million

## Method 2: Bottoms-Up Sales Model
SOM = Sales capacity × Win rate × Deal size

Example:
- Sales team size: 10 AEs
- Deals per AE per year: 20
- Win rate: 25%
- Average deal size: $10,000

SOM = 10 × 20 × 0.25 × $10,000 = $500,000 (Year 1)

## Method 3: Customer Acquisition
SOM = Marketing spend / CAC × LTV

Example:
- Annual marketing budget: $500,000
- CAC: $5,000
- Customers acquired: 100
- ARPU: $10,000
- SOM = 100 × $10,000 = $1 million
```

### Best Practices (2025)

```markdown
## Update Regularly
- Review quarterly with new customer data
- Adjust when you get competitive intelligence
- Recalculate after pivots or new product launches

## Be Conservative
- Investors prefer realistic over optimistic
- Use conservative market share assumptions (2-5%, not 20%)
- Account for competition taking majority of market

## Show Your Work
- Document all assumptions clearly
- Cite sources for market size data
- Explain calculation methodology
- Show sensitivity analysis (best/base/worst case)

## TAM is Current, Not Future
- TAM is about current annual revenue opportunity
- Don't project where market will be in 10 years as TAM
- Use projections to support growth narrative, not as TAM itself

## Validate with Multiple Sources
- Cross-reference industry reports
- Interview customers about budget/spend
- Analyze competitor revenue (public companies)
- Survey target market about willingness to pay
```

---

## Porter's Five Forces

### Overview

Framework for analyzing competitive intensity and industry profitability.

```
           THREAT OF NEW ENTRANTS
                    ↓
SUPPLIER POWER ← INDUSTRY → BUYER POWER
                 RIVALRY
                    ↑
           THREAT OF SUBSTITUTES
```

### The Five Forces

#### 1. Competitive Rivalry

**Questions to Answer:**
- How many competitors exist?
- How similar are their products?
- What's the industry growth rate?
- What are exit barriers?

**High Rivalry Indicators:**
```
• Many competitors of similar size
• Slow industry growth
• High fixed costs (must maintain volume)
• Low differentiation (commoditized)
• High exit barriers (expensive to shut down)
```

**Analysis Example: E-commerce**
```markdown
Rivalry: HIGH
- Amazon, Walmart, Target, and thousands of smaller players
- Low switching costs for customers
- Commoditized products
- Aggressive price competition
→ Impact: Low margins, need differentiation strategy
```

#### 2. Threat of New Entrants

**Questions to Answer:**
- How easy is it for new competitors to enter?
- What are the barriers to entry?
- Are there economies of scale?
- Is the market attractive to new entrants?

**Barriers to Entry:**
```
• Capital requirements (high = barrier)
• Economies of scale (incumbents have advantage)
• Brand loyalty (hard to overcome)
• Regulatory requirements (licenses, approvals)
• Access to distribution channels
• Proprietary technology/patents
• Network effects (more users = more valuable)
```

**Analysis Example: Social Media**
```markdown
Threat: LOW
- High barriers: network effects (Facebook, Instagram)
- Requires massive user base to be useful
- High customer acquisition costs
- Established brands with loyal users
→ Impact: Incumbents protected, focus on retention not acquisition
```

#### 3. Bargaining Power of Suppliers

**Questions to Answer:**
- How many suppliers exist?
- How unique are their products?
- What's the cost of switching suppliers?
- Could suppliers forward-integrate?

**High Supplier Power Indicators:**
```
• Few suppliers, many buyers
• Unique or differentiated inputs
• High switching costs
• Suppliers could sell directly to end customers
• No substitute inputs available
```

**Analysis Example: Smartphone Manufacturing**
```markdown
Supplier Power: MEDIUM-HIGH
- Limited chip suppliers (TSMC, Samsung, Intel)
- Specialized components (camera sensors, displays)
- High switching costs for new supplier qualification
→ Impact: Negotiate long-term contracts, diversify suppliers
```

#### 4. Bargaining Power of Buyers

**Questions to Answer:**
- How concentrated are buyers vs sellers?
- How price-sensitive are customers?
- How differentiated is the product?
- What are switching costs?

**High Buyer Power Indicators:**
```
• Few buyers, many sellers
• Buyers purchase in large volumes
• Products are standardized (commoditized)
• Low switching costs
• Buyers have full information (price transparency)
• Buyers could backward-integrate (make it themselves)
```

**Analysis Example: Enterprise SaaS**
```markdown
Buyer Power: MEDIUM
- Large enterprises have significant negotiating power
- Can switch vendors (though with some pain)
- Demand discounts for multi-year contracts
- Require extensive customization
→ Impact: Offer clear differentiation, focus on switching costs
```

#### 5. Threat of Substitutes

**Questions to Answer:**
- What alternative solutions exist?
- How do they compare on price/performance?
- What's the switching cost to substitutes?
- What are emerging technologies?

**High Threat Indicators:**
```
• Many substitute products available
• Substitutes offer better price/performance
• Low switching costs
• Substitutes from different industries (disruptive)
```

**Analysis Example: Taxi Services**
```markdown
Threat: HIGH
- Uber/Lyft disrupted traditional taxis
- Similar service, better UX, lower price
- Zero switching cost (just download app)
- Public transit, bikes, scooters also substitutes
→ Impact: Traditional taxis must innovate or exit
```

### Applying Porter's Five Forces

```markdown
## Step 1: Analyze Each Force
Rate each force as Low, Medium, or High
Document evidence and examples

## Step 2: Assess Industry Attractiveness
- Many "High" forces = Unattractive industry (low profitability)
- Many "Low" forces = Attractive industry (high profitability)

## Step 3: Identify Strategic Implications
For each force, define:
- How it impacts your business
- Actions to mitigate threats
- Opportunities to exploit

## Step 4: Monitor Over Time
- Industry dynamics change (new tech, regulations)
- Update analysis quarterly or semi-annually
- Watch for inflection points
```

### Porter's Five Forces Template

```markdown
# [Industry] Competitive Analysis

## 1. Competitive Rivalry: [HIGH/MEDIUM/LOW]
**Current State:**
- [# of competitors, market shares]
- [Product differentiation level]
- [Industry growth rate]

**Implications:**
- [Impact on pricing, margins]
- [Strategic response needed]

## 2. Threat of New Entrants: [HIGH/MEDIUM/LOW]
**Barriers to Entry:**
- Capital requirements: [HIGH/MEDIUM/LOW]
- Economies of scale: [HIGH/MEDIUM/LOW]
- Brand loyalty: [HIGH/MEDIUM/LOW]
- Regulatory: [HIGH/MEDIUM/LOW]

**Implications:**
- [How protected are incumbents?]
- [What to do to strengthen barriers?]

## 3. Supplier Bargaining Power: [HIGH/MEDIUM/LOW]
**Supplier Landscape:**
- [# of suppliers, concentration]
- [Switching costs]
- [Substitute inputs available?]

**Implications:**
- [Impact on costs, margins]
- [Supplier relationship strategy]

## 4. Buyer Bargaining Power: [HIGH/MEDIUM/LOW]
**Buyer Landscape:**
- [Buyer concentration vs seller]
- [Price sensitivity]
- [Switching costs]

**Implications:**
- [Pricing strategy]
- [How to reduce buyer power?]

## 5. Threat of Substitutes: [HIGH/MEDIUM/LOW]
**Substitute Products:**
- [What are they?]
- [How do they compare?]
- [Likelihood of customer switch?]

**Implications:**
- [Product positioning]
- [Innovation needed to stay ahead]

## Overall Industry Attractiveness: [HIGH/MEDIUM/LOW]
[Summary and strategic recommendations]
```

---

## 2025 Market Research Trends

### AI-Powered Market Intelligence

```markdown
## Tools & Capabilities
- **Crayon** — Tracks competitor moves (pricing, launches, hiring)
- **Glimpse** — Detects emerging trends from web/social data
- **Market Insights AI** — Generates competitor analysis + TAM/SAM/SOM
- **Delve AI** — Market analysis, audience segmentation

## Use Cases
✓ Real-time competitive alerts
✓ Automated trend detection
✓ Faster market sizing (hours vs weeks)
✓ Sentiment analysis at scale

## Best Practices
- Combine AI analysis with human judgment
- Validate AI findings with primary research
- Use for breadth, supplement with depth
```

### Continuous Market Monitoring

```markdown
## Modern Approach
Instead of annual market research reports:
- Real-time competitor tracking dashboards
- Weekly trend reports from AI tools
- Monthly customer advisory board meetings
- Quarterly deep-dive market analysis

## What to Track
- Competitor product launches
- Pricing changes
- Customer review sentiment
- Job postings (hiring trends)
- Web traffic patterns
- Social media buzz
- Funding announcements
```

### Privacy-First Research

```markdown
## Compliance Requirements
- GDPR (Europe): Consent, right to deletion
- CCPA (California): Opt-out, data transparency
- Cookie policies: First-party data focus

## Best Practices
✓ Anonymize research data
✓ Get explicit consent for surveys
✓ Offer opt-out mechanisms
✓ Be transparent about data usage
✓ Store securely, delete when no longer needed

✗ Don't share PII with third parties
✗ Don't track without consent
✗ Don't keep data longer than necessary
```

---

## Market Research Methods

### Primary Research

```markdown
## Definition
Research YOU conduct directly with customers/prospects

## Methods
- Customer interviews (1-on-1, 45-60 min)
- Surveys (quantitative validation)
- Focus groups (6-10 people, moderated discussion)
- Field studies (observe customers in their environment)
- Usability testing (watch people use product/prototype)

## Pros & Cons
✓ Tailored to your specific questions
✓ Direct access to target customers
✓ Deep, nuanced insights
✗ Time-consuming
✗ Expensive (recruiting, incentives)
✗ Requires research expertise
```

### Secondary Research

```markdown
## Definition
Research conducted by others that you analyze

## Sources
- Industry reports (Gartner, Forrester, IDC)
- Government data (census, labor statistics)
- Academic research
- Competitor websites, investor presentations
- News articles, trade publications
- App store reviews, G2/Capterra reviews

## Pros & Cons
✓ Fast and cheap (often free)
✓ Broad market view
✓ Historical trends available
✗ Not tailored to your questions
✗ May be outdated
✗ Quality varies
```

### Competitive Intelligence

```markdown
## What to Track
- Product features and pricing
- Marketing messaging and positioning
- Customer reviews (what they love/hate)
- Funding and financial performance
- Team size and key hires
- Partnerships and integrations
- Media coverage and PR strategy

## Sources
- Competitor websites (Wayback Machine for history)
- Job postings (engineering stack, priorities)
- LinkedIn (team growth, employee sentiment)
- Product Hunt, G2, Capterra (customer reviews)
- Investor presentations, SEC filings (public companies)
- Customer interviews ("What else did you evaluate?")

## Competitive Matrix Template
| Feature/Capability | Us | Competitor A | Competitor B |
|--------------------|-----|--------------|--------------|
| Pricing | $X/mo | $Y/mo | $Z/mo |
| Key differentiator | [Ours] | [Theirs] | [Theirs] |
| Target segment | [Ours] | [Theirs] | [Theirs] |
| Strengths | [...] | [...] | [...] |
| Weaknesses | [...] | [...] | [...] |
```

---

## Market Sizing Examples

### Example 1: B2B SaaS (Customer Support Software)

```markdown
## Bottom-Up TAM
Target: Companies with 10-500 employees in US
- Total companies: 500,000 (US Census Bureau)
- Average price: $2,400/year ($200/mo)
- TAM = 500,000 × $2,400 = $1.2 billion

## SAM (Serviceable Available Market)
Focus: Tech companies with high support volume
- Tech companies (10-500 employees): 50,000
- SAM = 50,000 × $2,400 = $120 million

## SOM (Year 1-3 Target)
Realistic capture based on sales capacity
- Year 1: 50 customers = $120,000
- Year 2: 200 customers = $480,000
- Year 3: 500 customers = $1.2 million
- 3-year SOM = $1.8 million
```

### Example 2: B2C Mobile App (Fitness)

```markdown
## Bottom-Up TAM
Target: Smartphone users interested in fitness (Global)
- Smartphone users globally: 6.8 billion
- % interested in fitness: 30% = 2 billion
- Average subscription: $10/month = $120/year
- TAM = 2B × $120 = $240 billion

## SAM (Serviceable Available Market)
Focus: English-speaking, iOS users in US/UK/Canada/Australia
- English-speaking iOS users in target countries: 150 million
- SAM = 150M × $120 = $18 billion

## SOM (Year 1-3)
Based on conversion funnel and marketing spend
- App installs Year 1: 100,000
- Conversion to paid: 5% = 5,000
- SOM Year 1 = 5,000 × $120 = $600,000
- Year 3 target: 50,000 paid users = $6 million
```

---

## See Also

- [competitive-analysis.md](competitive-analysis.md) — Deep dive on competitive frameworks
- [user-research.md](user-research.md) — Primary research methods
- [opportunity-frameworks.md](opportunity-frameworks.md) — JTBD, Kano, Value Prop Canvas
