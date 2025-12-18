# A/B Testing & Experimentation

## Overview

A/B testing (split testing) is the practice of comparing two or more variants to determine which performs better. This guide covers statistical best practices, common pitfalls, and 2025 trends in experimentation.

**2025 Reality:** 80% of A/B tests fail to produce a statistically significant winner, yet countless hours are spent acting on inconclusive results.

---

## Fundamentals

### What is A/B Testing?

```markdown
A/B Testing = Controlled experiment comparing variants

Setup:
• Control (A): Current experience
• Variant (B): Proposed change
• Random assignment: Users → A or B
• Measure: Which performs better?

Example:
Control:  Blue "Sign Up" button → 5% conversion
Variant:  Green "Get Started" button → 6% conversion
Result:   Green button wins (+20% lift)
```

### When to A/B Test

```markdown
✓ Test before building expensive features
✓ Optimize conversion funnels
✓ Validate design changes
✓ Test pricing changes
✓ Optimize email/push campaigns
✓ Test copy, CTAs, layouts

✗ Don't test without sufficient traffic
✗ Don't test if you can't implement winner
✗ Don't test if outcome doesn't matter
✗ Don't test radical product changes (use beta)
```

---

## Statistical Significance

### P-Value Explained

The **p-value** is the probability that the observed difference occurred by chance.

```
p-value < 0.05 (5%)
= Less than 5% chance result is random
= 95% confidence in the result
= Statistically significant

Standard thresholds:
• p ≤ 0.01: Highly significant (99% confidence)
• p ≤ 0.05: Significant (95% confidence)
• p > 0.05: Not significant (insufficient evidence)
```

### Type I and Type II Errors

```markdown
## Type I Error (False Positive)
Definition: Rejecting null hypothesis when it's true
Example: Concluding B is better when it's not
Controlled by: Significance level (α = 0.05)

Impact:
• Ship a "winning" variant that doesn't actually work
• Waste engineering time
• Potentially harm metrics

## Type II Error (False Negative)
Definition: Failing to reject null hypothesis when it's false
Example: Missing a real improvement
Controlled by: Statistical power (1 - β)

Impact:
• Miss opportunity to improve product
• Leave better variant unreleased
• Slow growth

## Optimal Balance
• α (significance) = 0.05 (5% false positive rate)
• Power = 0.80 (80% chance detecting real effect)
• This gives β = 0.20 (20% false negative rate)
```

### Statistical Power

**Power** is the probability of detecting a real effect if one exists.

```
Power = 1 - β (Type II error rate)

Standard: 80% power
= 80% chance of detecting real 5% lift
= Need sufficient sample size

Factors affecting power:
• Sample size (more = higher power)
• Effect size (larger effect = easier to detect)
• Significance level (lower α = lower power)
• Baseline conversion rate
```

### Sample Size Calculation

```
Minimum sample size depends on:
• Baseline conversion rate
• Minimum detectable effect (MDE)
• Significance level (α)
• Statistical power (1 - β)

Formula (simplified):
n = 16 × σ² / (MDE²)

Where σ² = p(1-p) for binomial outcomes

Example:
Baseline: 10% conversion
MDE: 2% (absolute), 20% (relative)
α = 0.05, Power = 0.80

Required: ~2,000 users per variant
```

### Online Sample Size Calculators

```markdown
• Optimizely: https://www.optimizely.com/sample-size-calculator/
• VWO: https://vwo.com/tools/ab-test-significance-calculator/
• Evan's Awesome A/B Tools: https://www.evanmiller.org/ab-testing/
```

---

## Running Experiments

### Experiment Design

```markdown
## 1. Hypothesis
Format: "If [change], then [impact], because [reasoning]"

Example:
"If we change the CTA from 'Sign Up' to 'Get Started',
then conversion will increase by 10%,
because 'Get Started' is more action-oriented and less committal"

## 2. Primary Metric
The ONE metric you're trying to move

Examples:
• Conversion rate (sign-ups / visitors)
• Click-through rate (CTR)
• Revenue per user
• Retention rate

## 3. Secondary Metrics
Supporting metrics to watch for side effects

Examples:
• Time on page
• Bounce rate
• Downstream conversions
• Revenue impact

## 4. Guardrail Metrics
Metrics that should NOT decrease

Examples:
• Overall revenue
• User satisfaction (NPS)
• Load time
• Error rate
```

### Test Setup

```javascript
// Example: Feature flag with A/B test
import { getVariant } from '@/lib/experiments';

function SignUpButton() {
  const variant = getVariant('signup-button-test', {
    control: 0.5,    // 50% traffic
    variant: 0.5     // 50% traffic
  });

  const buttonText = variant === 'variant'
    ? 'Get Started'    // Variant B
    : 'Sign Up';       // Control A

  const buttonColor = variant === 'variant'
    ? 'green'
    : 'blue';

  const handleClick = () => {
    // Track conversion
    track('signup_clicked', {
      variant: variant,
      button_text: buttonText,
      button_color: buttonColor
    });

    // Proceed with sign-up
    navigate('/signup');
  };

  return (
    <button
      onClick={handleClick}
      style={{ backgroundColor: buttonColor }}
    >
      {buttonText}
    </button>
  );
}
```

### Random Assignment

```markdown
## User-Level Randomization (Recommended)
• Assign each user consistently to A or B
• Same user always sees same variant
• Prevents confusion from variant switching

## Session-Level Randomization
• Each session gets random assignment
• Same user may see A then B
• Good for content testing, bad for UX changes

## Implementation (Hash-Based)
function getVariant(userId, experimentId) {
  const hash = md5(userId + experimentId);
  const bucket = parseInt(hash.substring(0, 8), 16) % 100;

  if (bucket < 50) return 'control';
  return 'variant';
}
```

### Test Duration

```markdown
## Minimum Duration Guidelines
• Run for at least 1-2 weeks
• Capture weekly patterns (weekday vs weekend)
• Account for seasonality
• Don't stop early just because you see significance

## When to Stop
✓ Reached required sample size
✓ Ran for minimum duration
✓ Result is statistically significant
✓ OR decided test is inconclusive

## Common Mistakes
❌ Peeking and stopping early
❌ Running indefinitely waiting for significance
❌ Not accounting for weekly cycles
```

---

## Frequentist vs. Bayesian

### Frequentist Approach (Traditional)

```markdown
## Philosophy
• Probability = long-run frequency
• Null hypothesis testing (p-values)
• Binary outcome: significant or not

## Process
1. Set α = 0.05 before test
2. Collect data
3. Calculate p-value
4. If p < 0.05 → reject null, B wins
5. If p ≥ 0.05 → fail to reject, inconclusive

## Pros
• Industry standard
• Well-understood
• Objective (no priors)

## Cons
• Binary outcome (significant or not)
• Misinterpreted p-values
• "Peeking" problem (checking early invalidates test)
```

### Bayesian Approach (Modern)

```markdown
## Philosophy
• Probability = degree of belief
• Updates beliefs with evidence
• Continuous probability estimates

## Process
1. Start with prior belief (e.g., 50/50)
2. Collect data
3. Update posterior probability
4. "B is 85% likely to be better than A"

## Pros
• Intuitive probabilities
• Can peek anytime (no invalidation)
• Incorporates prior knowledge
• Handles small samples better

## Cons
• Requires setting priors
• More complex to implement
• Less familiar to stakeholders

## 2025 Trend
Experimentation leaders are 270% more likely to grow when using
Bayesian or CUPED methods vs. basic frequentist A/B tests.
```

---

## Common Pitfalls

### 1. Peeking Problem

```markdown
Problem: Checking results repeatedly and stopping when significant

Why it's bad:
• Increases false positive rate (Type I error)
• Standard α = 0.05 no longer valid
• Random fluctuations look like significance early on

Solution:
• Wait until reaching required sample size
• Use sequential testing (if you must peek)
• Use Bayesian methods (peeking is valid)
```

### 2. Multiple Comparisons

```markdown
Problem: Testing many variants or metrics without correction

Example:
• Test 10 button colors
• Even if none work, ~40% chance of false positive

Why:
• With α = 0.05, each test has 5% false positive rate
• More tests = higher overall false positive rate

Solution:
• Bonferroni correction: α_adjusted = α / n
• Focus on primary metric
• Pre-register hypotheses
```

### 3. Sample Ratio Mismatch (SRM)

```markdown
Problem: Unequal split when expecting 50/50

Example:
• Expected: 50% control, 50% variant
• Observed: 48% control, 52% variant
• Chi-square test p < 0.05 → SRM detected!

Causes:
• Bug in randomization
• Variant has different load time (users leave)
• Bot traffic hitting only one variant
• Bucketing logic error

Solution:
• Check split before analyzing results
• Investigate and fix randomization
• Don't trust results if SRM exists
```

### 4. Novelty Effect

```markdown
Problem: Users react to change, not improvement

Example:
• Change button from blue to red
• Week 1: Conversions up 10% (users notice change)
• Week 4: Conversions return to baseline

Solution:
• Run tests for 2-4 weeks
• Check if effect persists
• Segment new vs. returning users
```

### 5. Ignoring Statistical Power

```markdown
Problem: Not enough traffic, test never reaches significance

Example:
• Need 10,000 users per variant
• Only have 1,000 users/month
• Test runs for years...

Solution:
• Calculate required sample size upfront
• Don't test if traffic insufficient
• Consider larger changes (bigger effect size)
• Combine multiple small changes
```

---

## Advanced Techniques

### CUPED (Controlled-Experiment Using Pre-Experiment Data)

```markdown
## What is CUPED?
Variance reduction technique using pre-experiment data

## How it Works
1. Measure metric before experiment (pre-period)
2. Use correlation between pre/post to reduce variance
3. Detect smaller effects with same sample size

## Benefit
• 2-3× variance reduction
• Faster experiment results
• Detect smaller lifts

## When to Use
• High correlation between pre/post metrics
• Want to detect small effects (<5%)
• Limited traffic

## 2025 Adoption
Used by Netflix, Microsoft, Booking.com
Becoming standard at experimentation-mature companies
```

### Multi-Armed Bandits

```markdown
## What is MAB?
Adaptive algorithm that shifts traffic to better variants

## How it Works
• Start: Equal traffic to all variants
• During: More traffic to better-performing variants
• End: Most traffic to winner

## Pros
• Minimize opportunity cost
• Good for content testing (headlines, images)
• Explores and exploits simultaneously

## Cons
• Not pure A/B test (less scientific)
• Can be slow to converge
• Doesn't give significance test

## When to Use
• High traffic, fast feedback
• Content optimization
• OK with "good enough" not "statistically proven"
```

### Holdout Groups

```markdown
## Purpose
Validate that shipped experiments actually worked

## Setup
• After A/B test, ship winning variant
• Keep 5-10% of users in control (holdout)
• Monitor long-term impact

## Example
• A/B test shows 5% conversion lift
• Ship to 90% of users
• Keep 10% in control
• After 6 months: Is lift still there?

## Why Important
• Novelty effects wear off
• Interaction effects with other changes
• Validates experiment program ROI
```

---

## Funnel Experiments

### Multi-Step Funnels

```markdown
## Challenge
Testing change in Step 2 affects Step 3, 4, 5...

Example Funnel:
Landing Page → Sign-Up → Onboarding → Activation → Payment

Test: Change onboarding (Step 3)

Metrics to measure:
• Step 3 completion (direct impact)
• Step 4 activation (downstream)
• Step 5 payment (ultimate goal)
• Overall funnel conversion

## Analysis
• Primary: Overall conversion (Landing → Payment)
• Secondary: Each step individually
• Check for trade-offs (better Step 3, worse Step 5?)
```

---

## Experiment Analysis

### Statistical Test Selection

```markdown
## Binary Outcomes (Conversion, Click)
Use: Two-proportion z-test

Example:
Control: 1000 users, 50 conversions (5.0%)
Variant: 1000 users, 60 conversions (6.0%)

H0: p_variant = p_control
HA: p_variant ≠ p_control

z-score = (6.0% - 5.0%) / SE
p-value = 0.032

Result: p < 0.05 → Significant!

## Continuous Outcomes (Revenue, Time)
Use: Two-sample t-test

Example:
Control: avg revenue = $50, σ = $20, n = 500
Variant: avg revenue = $55, σ = $22, n = 500

t-statistic = (55 - 50) / SE
p-value = 0.003

Result: p < 0.05 → Significant!
```

### Interpreting Results

```markdown
## Scenario 1: Clear Winner
• p < 0.05 (statistically significant)
• Practical significance (lift > 5%)
• No SRM issues
• Ran for sufficient duration

Action: Ship the winner

## Scenario 2: Inconclusive
• p > 0.05 (not significant)
• Small sample, short duration

Action: Run longer or accept inconclusive

## Scenario 3: Significant but Small
• p < 0.05 (significant)
• But lift is tiny (0.1%)

Action: Evaluate if worth engineering effort

## Scenario 4: Mixed Results
• Primary metric: No change
• Secondary metric: Big improvement

Action: Investigate, might have misidentified primary metric

## Scenario 5: Negative Result
• p < 0.05 (significant)
• But variant performed WORSE

Action: Don't ship, investigate why hypothesis failed
```

### Effect Size

```markdown
## Absolute vs. Relative Lift

Absolute Lift:
= Variant rate - Control rate
= 6% - 5% = 1 percentage point

Relative Lift:
= (Variant - Control) / Control × 100%
= (6% - 5%) / 5% × 100% = 20%

Report both:
"Variant increased conversion from 5% to 6%
(absolute lift: +1pp, relative lift: +20%)"

## Practical Significance
Statistical significance ≠ Practical significance

Example:
• Statistically significant: p = 0.001
• But only +0.1% conversion increase
• Engineering effort: 2 weeks
• Worth it? Probably not.

Consider:
• Implementation cost
• Maintenance burden
• Opportunity cost (what else could you build?)
```

---

## Experimentation Culture

### Organizational Maturity

```markdown
## Level 1: Ad-Hoc Testing
• No formal process
• Tests run occasionally
• Inconsistent methodology

## Level 2: Systematic Testing
• Regular A/B tests
• Documentation
• Consistent statistical methods

## Level 3: Experimentation Platform
• Centralized tooling
• Self-service for teams
• Automated analysis

## Level 4: Advanced Methods
• CUPED, Bayesian methods
• Holdout groups
• Causal inference

## 2025 Survey Finding
Teams with shared metrics and reporting frameworks were
significantly more likely to launch impactful experiments faster.
```

### Best Practices

```markdown
1. Document everything
   • Hypothesis
   • Expected impact
   • Sample size calculation
   • Results and learnings

2. Learn from failures
   • 80% of tests fail
   • Failed tests teach what DOESN'T work
   • Share learnings across teams

3. Align on thresholds
   • Marketing: 90% confidence OK?
   • Product: 95% required?
   • Standardize to avoid friction

4. Velocity matters
   • More experiments = more learning
   • Don't overthink small tests
   • Fail fast, iterate quickly

5. Build institutional knowledge
   • Track all experiments
   • Analyze patterns (what works?)
   • Create playbooks
```

---

## Tools

### Experimentation Platforms

| Tool | Best For | Pricing | Key Features |
|------|----------|---------|--------------|
| **Optimizely** | Enterprise | $$$ | Visual editor, full-stack |
| **VWO** | Marketing | $$ | Easy setup, heatmaps |
| **Google Optimize** | Small teams | Free | GA integration (being sunset) |
| **Statsig** | Engineering | $$ | Feature flags, analytics |
| **LaunchDarkly** | Feature flags | $$$ | Progressive rollouts |
| **GrowthBook** | Open source | Free/$ | Self-hosted, Bayesian |
| **Amplitude Experiment** | Product teams | $$ | Integrated with Amplitude |

### Statistical Analysis

```python
# Python: Two-proportion z-test
from scipy import stats

# Control: 50/1000 = 5%
# Variant: 60/1000 = 6%

control_conversions = 50
control_total = 1000
variant_conversions = 60
variant_total = 1000

# Two-proportion z-test
z_stat, p_value = stats.proportions_ztest(
    [variant_conversions, control_conversions],
    [variant_total, control_total]
)

print(f"z-statistic: {z_stat:.3f}")
print(f"p-value: {p_value:.3f}")

if p_value < 0.05:
    print("Statistically significant!")
else:
    print("Not significant")
```

```r
# R: Two-proportion test
control <- c(50, 950)  # 50 conversions, 950 non-conversions
variant <- c(60, 940)  # 60 conversions, 940 non-conversions

result <- prop.test(c(60, 50), c(1000, 1000))
print(result)
```

---

## 2025 Trends

### 1. Bayesian Methods Adoption

```markdown
• Easier to interpret ("85% chance B is better")
• Can peek without invalidating results
• Better for small samples
• Tools: Statsig, GrowthBook, VWO
```

### 2. CUPED/Variance Reduction

```markdown
• 2-3× faster experiments
• Standard at Netflix, Booking.com, Microsoft
• Requires pre-period data
• Advanced technique becoming mainstream
```

### 3. Causal Inference

```markdown
• Beyond correlation → causation
• Synthetic controls
• Difference-in-differences
• Academic methods entering industry
```

### 4. AI-Powered Experimentation

```markdown
• Auto-generate test ideas
• Predict experiment outcomes
• Anomaly detection
• Automated interpretation
```

---

## Checklist

```markdown
## Before Experiment
- [ ] Hypothesis clearly stated
- [ ] Primary metric defined
- [ ] Secondary/guardrail metrics identified
- [ ] Sample size calculated
- [ ] Minimum duration determined
- [ ] Random assignment validated
- [ ] Implementation QA'd

## During Experiment
- [ ] Monitor for SRM (sample ratio mismatch)
- [ ] Check for technical issues
- [ ] Don't peek and stop early
- [ ] Track experiment in central log

## After Experiment
- [ ] Wait for required sample size
- [ ] Check statistical significance (p-value)
- [ ] Evaluate practical significance (effect size)
- [ ] Review secondary metrics
- [ ] Document results and learnings
- [ ] Make ship/no-ship decision
- [ ] Share results with team
```
