# User Research

## Research Methods Overview

### Qualitative vs Quantitative

```markdown
## Qualitative Research
**Purpose:** Understand WHY and HOW
**Output:** Insights, themes, motivations
**Sample Size:** Small (5-15 per segment)
**Methods:** Interviews, observations, ethnography

When to use:
- Exploratory research (new problem space)
- Understanding user motivations
- Discovering unarticulated needs
- Generating hypotheses to test

## Quantitative Research
**Purpose:** Measure WHAT, HOW MUCH, HOW MANY
**Output:** Numbers, statistics, percentages
**Sample Size:** Large (100+)
**Methods:** Surveys, analytics, experiments

When to use:
- Validating qualitative findings at scale
- Measuring prevalence of behaviors
- Prioritizing features
- A/B testing
- Tracking metrics over time
```

### Attitudinal vs Behavioral

```markdown
## Attitudinal (What People Say)
Methods: Surveys, interviews, focus groups
Captures: Opinions, preferences, intentions

Limitation: "Say-do" gap — people say one thing, do another

## Behavioral (What People Do)
Methods: Analytics, observation, usability tests
Captures: Actual behavior, task completion

Gold standard: Observe real behavior, not stated intentions
```

---

## User Interviews

### Interview Types

```markdown
## Discovery Interviews
**Goal:** Understand problem space, user needs
**Duration:** 45-60 minutes
**Participants:** Mix of users, non-users, churned users
**Questions:** Open-ended, exploratory

## Solution Validation Interviews
**Goal:** Test specific solution, get feedback on prototype
**Duration:** 30-45 minutes
**Participants:** Target users for this feature
**Questions:** Task-based, observational

## Contextual Inquiry
**Goal:** Observe users in their natural environment
**Duration:** 1-2 hours
**Location:** User's workplace/home
**Method:** Watch, ask questions as they work
```

### How Many Interviews?

```markdown
## Jakob Nielsen's Rule
5 users uncover ~85% of usability issues
15 users approach 100% (diminishing returns)

## For Discovery
- 5-8 users per user segment
- Multiple segments = multiply (e.g., 3 segments × 6 = 18 interviews)
- Stop when you hear repeated themes (saturation)

## For Continuous Discovery
- 3-5 interviews per week
- Ongoing, not one-time
- Mix of new insights + validation
```

### Interview Preparation

```markdown
## 1. Define Research Goals
What do you want to learn?
- Understand pain points with current workflow?
- Validate problem exists?
- Test solution concept?
- Prioritize features?

## 2. Create Discussion Guide
Outline topics, not rigid script
- Opening (5 min): Build rapport, explain purpose
- Background (10 min): Understand their context
- Main topics (25 min): Deep dive on research questions
- Closing (5 min): Ask final questions, thank them

## 3. Recruit Right Participants
Screening criteria:
- Demographics (role, company size, industry)
- Behavioral (uses similar tools, has problem you're solving)
- Psychographic (early adopter vs conservative)

Recruiting sources:
- Customer list (current users)
- Email list (prospects)
- LinkedIn outreach
- User research platforms (UserTesting, Respondent.io)
- Referrals from participants

Incentives:
- B2C: $50-100 gift card, 45-60 min
- B2B: $100-200 gift card or donation to charity
- Existing customers: Early access to features
```

### Interview Best Practices

```markdown
## Before Interview
✓ Test recording setup (Zoom, Grain.co, Otter.ai)
✓ Review discussion guide
✓ Arrive 5 min early to build rapport
✓ Have pen and paper ready (notes + recording)

## Opening (First 5 Minutes)
✓ Introduce yourself and purpose
✓ Explain recording and consent
✓ Set expectations: "No wrong answers, we're learning"
✓ Build rapport with small talk

## During Interview
✓ Ask open-ended questions
  → "Tell me about the last time you..."
  → "Walk me through your process for..."
  → "What's most frustrating about...?"

✓ Follow the 5 Whys
  → Dig deeper by asking "Why?" 5 times
  → Uncover root cause, not surface symptoms

✓ Listen more than talk (80/20 rule)
  → Resist urge to fill silence
  → Pause after they finish — they'll often add more

✓ Ask about past behavior, not future hypotheticals
  ✓ "Tell me about the last time you searched for a product"
  ✗ "Would you use a feature that lets you...?"

✓ Look for workarounds
  → How do they solve problem today?
  → What tools/hacks have they cobbled together?

✓ Observe emotion and tone
  → Frustration, excitement, confusion
  → Body language (video calls)

## What NOT to Do
✗ Don't ask leading questions
  ✗ "Don't you think this feature would be useful?"
  ✓ "How would this fit into your workflow?"

✗ Don't pitch your solution
  → You're there to learn, not sell
  → Save pitching for later

✗ Don't ask "Would you use this?"
  → People lie (to be nice, or they don't know)
  → Instead: Show prototype, watch behavior

✗ Don't multi-task
  → Give full attention
  → Have co-worker take notes if needed

✗ Don't explain away their problems
  → "Oh that's a bug we're fixing"
  → Just listen and learn

## Closing (Last 5 Minutes)
✓ "Is there anything I didn't ask that I should have?"
✓ "Do you know others who might want to chat?"
✓ Thank them, explain next steps
✓ Send thank you email + incentive within 24 hours
```

### Sample Interview Questions

```markdown
## Background & Context
- "Tell me about your role and what you do day-to-day."
- "Walk me through a typical [workday/week]."
- "What tools do you currently use for [task]?"

## Problem Discovery
- "What's the most frustrating part of [process]?"
- "Tell me about the last time you struggled with [task]."
- "If you could wave a magic wand and fix one thing, what would it be?"
- "What workarounds have you created to deal with [problem]?"

## Current Solutions
- "How are you solving [problem] today?"
- "What do you like about [current tool]?"
- "What's missing from [current tool]?"
- "What would make you switch to a different solution?"

## Jobs-to-be-Done Style
- "When was the last time you [hired a product for this job]?"
- "What were you trying to accomplish?"
- "What else did you try before [current solution]?"
- "What would have to happen for you to stop using [current solution]?"

## Solution Validation
- "I'd like to show you a prototype. Think out loud as you explore."
- [After showing]: "What stands out to you?"
- "How would this fit into your current workflow?"
- "What's missing that you'd need to actually use this?"

## Prioritization
- "If you could only have one of these features, which would it be?"
- "What would you be willing to pay for this?"
- "How much time would this save you per week?"

## Closing
- "Who else should I talk to about this?"
- "Can I follow up with you in a few weeks to show progress?"
- "Is there anything I should have asked but didn't?"
```

---

## Surveys

### When to Use Surveys

```markdown
## Good Use Cases
✓ Validate findings from interviews at scale
✓ Measure satisfaction (NPS, CSAT, CES)
✓ Prioritize features (Kano surveys)
✓ Segment users by behavior/needs
✓ Track metrics over time

## Poor Use Cases
✗ Exploratory research (use interviews instead)
✗ Understanding "why" (need qualitative depth)
✗ Generating new insights (surveys confirm, not discover)
✗ Complex workflows (too nuanced for survey)
```

### Survey Design Best Practices

```markdown
## Length
- Target: <10 minutes to complete
- Aim for: 10-15 questions max
- Mobile: 1 question per screen

## Question Order
1. Engaging question first (not demographics)
2. Most important questions in middle
3. Demographics at end (they'll quit if bored)
4. Logic/branching to keep relevant

## Question Types

### Multiple Choice
Best for: Categorization, segmentation
✓ "Which industry are you in?"
✓ "How often do you use [product]?"

Tip: Include "Other (please specify)" option

### Likert Scale (1-5 or 1-7)
Best for: Satisfaction, importance, agreement
✓ "How satisfied are you with [feature]?" (1=Very dissatisfied, 5=Very satisfied)
✓ "How important is [feature]?" (1=Not at all, 5=Critical)

Tip: Use consistent scales throughout survey

### Open-Ended
Best for: Qualitative insights, context
✓ "What's the main reason for your rating?"
✓ "What feature would you add if you could?"

Tip: Use sparingly (harder to analyze), place after closed questions

### Ranking
Best for: Prioritization
✓ "Rank these features by importance (1=most, 5=least)"

Tip: Limit to 5-7 items max

### Matrix Questions
Best for: Rating multiple items on same scale
Example: Rate these features on importance

Tip: Works better on desktop than mobile
```

### Avoiding Bias

```markdown
## Leading Questions ✗
✗ "How much do you love our new feature?"
✓ "How would you rate the new feature?" (1-5 scale)

## Double-Barreled Questions ✗
✗ "How satisfied are you with our speed and reliability?"
  → Asks two things at once
✓ Separate: "How satisfied are you with speed?" + "...with reliability?"

## Loaded Questions ✗
✗ "Do you agree that our competitors are inferior?"
✓ "How does our product compare to alternatives?"

## Forced Choice ✗
✗ "Do you prefer Feature A or Feature B?"
  → What if they want both, or neither?
✓ Include "Both", "Neither", "No preference" options

## Confusing Wording ✗
✗ "Rate the non-intuitive aspects of the UI"
✓ "Rate the ease of use of the interface" (1=Very difficult, 5=Very easy)
```

### Survey Distribution

```markdown
## In-App Surveys
Pros:
✓ High response rate (users are engaged)
✓ Contextual (ask about what they just did)
✓ Real-time feedback

Cons:
✗ Biased to active, engaged users
✗ Can interrupt user experience

Best for: Quick polls, NPS, feature feedback

Tools: Pendo, Appcues, Hotjar, Typeform

## Email Surveys
Pros:
✓ Broader reach (active + inactive users)
✓ Can reach non-users (prospects, churned)

Cons:
✗ Lower response rate (5-15% typical)
✗ May end up in spam

Best for: Longer surveys, churned user feedback

Tools: Typeform, SurveyMonkey, Qualtrics, Google Forms

## Tips for Higher Response Rates
✓ Personalize subject line: "[Name], we'd love your input"
✓ Explain why and how long: "2 min survey to improve [feature]"
✓ Incentivize: "$10 gift card for completed surveys"
✓ Send reminders: Day 3, Day 7 (to non-responders only)
✓ Show progress bar in survey
✓ Make mobile-friendly
✓ Follow up with summary of results
```

### Example: Kano Survey

```markdown
## Purpose
Categorize features as Basic, Performance, or Delighter

## Question Format
For each feature, ask TWO questions:

**Functional (feature present):**
"How would you feel if we HAD [feature]?"
- I like it
- I expect it
- I'm neutral
- I can tolerate it
- I dislike it

**Dysfunctional (feature absent):**
"How would you feel if we DIDN'T have [feature]?"
- I like it
- I expect it
- I'm neutral
- I can tolerate it
- I dislike it

## Analysis
Cross-reference answers to categorize:

| Dysfunctional → | Like | Expect | Neutral | Tolerate | Dislike |
|-----------------|------|--------|---------|----------|---------|
| **Functional ↓**|      |        |         |          |         |
| Like            | Q    | A      | A       | A        | P       |
| Expect          | R    | I      | I       | I        | M       |
| Neutral         | R    | I      | I       | I        | M       |
| Tolerate        | R    | I      | I       | I        | M       |
| Dislike         | R    | R      | R       | R        | Q       |

A = Attractive (Delighter)
M = Must-have (Basic)
P = Performance
I = Indifferent
R = Reverse (they don't want it!)
Q = Questionable (inconsistent answer)

## Prioritization
1. Must-haves (M) — Build first
2. Performance (P) — Core differentiators
3. Attractive (A) — Delighters if time allows
4. Indifferent (I) — Skip
5. Reverse (R) — Don't build!
```

---

## Ethnographic Research

### What is Ethnography?

```markdown
Ethnography = Observing users in their natural environment

Key difference from interviews:
- Interviews: What people SAY they do
- Ethnography: What people ACTUALLY do

Best for:
- Understanding context and environment
- Uncovering unconscious behaviors
- Seeing workarounds and hacks
- Discovering unstated needs
```

### Ethnographic Methods

```markdown
## Field Studies
Visit users in their workplace/home
Observe them performing tasks in real context

Duration: 1-3 hours per session
Sample size: 5-10 users per segment

Example:
- Observing nurses in hospital using EMR system
- Watching parents prepare meals with toddlers
- Shadowing sales reps during customer calls

## Contextual Inquiry
Hybrid: Observation + Interview
- Watch user perform task
- Ask questions as they work: "Why did you do that?"
- See environment, tools, interruptions

## Diary Studies
Users self-report over time (1-4 weeks)
- Daily log of behaviors, feelings, context
- Photos, videos, voice notes
- Captures longitudinal patterns

Tools: dscout, Indeemo, Ethnio

Example:
- Food diary for nutrition app
- Commute diary for transportation service
- Shopping diary for e-commerce research

## Fly-on-the-Wall Observation
Pure observation, minimal intervention
- No questions, just watch and take notes
- See unbiased, natural behavior
- Ask clarifying questions AFTER

Best for:
- Public spaces (retail, events)
- Avoiding observer effect
```

### Conducting Field Studies

```markdown
## Preparation
1. Define research goals
   - What behaviors are you studying?
   - What questions are you answering?

2. Recruit participants
   - Screen for target users
   - Schedule at their location
   - 1-2 hour blocks

3. Prepare materials
   - Camera/phone for photos (with permission)
   - Recording device for audio notes
   - Notebook for observations
   - Consent forms

## During Observation
✓ Arrive early, build rapport
✓ Start with brief intro and consent
✓ Take photo of environment (with permission)
✓ Observe before asking questions
✓ Note what they do, not just what they say
✓ Look for:
  - Workarounds and hacks
  - Points of friction
  - Emotions (frustration, delight)
  - Tools and artifacts
  - Interruptions and distractions
  - Environmental constraints

✓ Ask clarifying questions:
  - "Why did you do that?"
  - "What are you thinking right now?"
  - "Is this typical or unusual?"

## After Observation
✓ Debrief immediately (memory fades fast)
✓ Review photos and notes
✓ Identify patterns and themes
✓ Share findings with team
```

### Example Observation Notes

```markdown
## Participant 5 — Sarah, Marketing Manager
**Date:** 2025-12-16
**Location:** Office (open floor plan)
**Task:** Creating weekly marketing report

### Observations

**9:00 AM** — Opens laptop, 3 monitors on desk
- Monitor 1: Slack (constant notifications)
- Monitor 2: Google Analytics
- Monitor 3: Excel spreadsheet

**9:05** — Starts copying data from GA to Excel manually
- Uses calculator app to compute percentages
- Interrupted by Slack message, loses place
- Mutters "where was I?" and starts over

**9:15** — Gets data from 3rd tool (email platform)
- Exports CSV, opens in Excel, copy-pastes into main sheet
- Complains "this takes forever every week"

**9:20** — Creates charts in Excel
- Spends 5 min formatting (colors, fonts)
- "I have to redo this every time, can't save template"

**9:30** — Interrupted by coworker question
- Loses 10 minutes to conversation
- Returns to report, has to re-orient

**9:45** — Finishes report, exports as PDF
- Emails to 5 stakeholders individually
- "I wish this was automated"

### Insights
- **Pain point:** Manual data aggregation from 3 tools
- **Workaround:** Calculator app (wants formulas)
- **Time sink:** Formatting (wants templates)
- **Friction:** Constant interruptions break flow
- **Opportunity:** Automated reporting + distribution

### Photos
- [Photo of 3-monitor setup]
- [Screenshot of Excel template]
- [Sticky notes on monitor with formulas]
```

---

## Persona Development

### What are Personas?

```markdown
Personas = Fictional characters representing user segments
Based on real research data, not assumptions

Purpose:
- Align team on who we're building for
- Make design decisions ("What would Sarah do?")
- Prioritize features for specific segments
- Communicate user needs to stakeholders

NOT just demographics — focus on:
- Goals and motivations
- Pain points and frustrations
- Behaviors and workflows
- Context and environment
```

### Creating Data-Driven Personas

```markdown
## Step 1: Conduct User Research
- Interview 30-50 users across segments
- Survey for quantitative validation
- Analyze usage data

## Step 2: Identify Patterns
Look for:
- Common goals
- Shared pain points
- Similar behaviors
- Demographic clusters

## Step 3: Cluster into Segments
Use criteria like:
- Job role (designer vs developer)
- Company size (SMB vs enterprise)
- Tech savviness (beginner vs expert)
- Use case (different jobs-to-be-done)

Typical result: 3-5 primary personas

## Step 4: Build Persona Profiles
For each persona, document:
- Name and photo (make them feel real)
- Demographics (age, role, company)
- Goals and motivations
- Pain points and frustrations
- Behaviors and workflows
- Quote that captures their mindset
- Tools they use
- How they discover/evaluate products

## Step 5: Validate with Real Users
- Share with customers: "Do you see yourself here?"
- Update based on feedback
- Refresh annually as users evolve
```

### Persona Template

```markdown
# Persona: [Name]

![Photo]

## Demographics
- **Age:** 32
- **Role:** Product Marketing Manager
- **Company:** Mid-size B2B SaaS (150 employees)
- **Location:** San Francisco, CA
- **Education:** MBA, Marketing

## Goals & Motivations
- Launch successful product campaigns
- Prove marketing ROI to leadership
- Understand customer behavior and preferences
- Stay ahead of market trends

## Pain Points & Frustrations
- Data scattered across 5+ tools, hard to synthesize
- Manual reporting takes 5 hours/week
- Can't prove which campaigns drive revenue
- Leadership wants faster insights

## Behaviors & Workflows
- Checks Google Analytics daily
- Creates weekly reports for CMO
- Runs 2-3 campaigns per month
- Collaborates with sales team on messaging
- Reads marketing blogs during commute

## Quote
*"I spend more time wrangling data than actually marketing. I need insights, not just raw numbers."*

## Tools & Tech Stack
- Google Analytics
- HubSpot (marketing automation)
- Salesforce (CRM)
- Slack (communication)
- Google Sheets (reporting)
- Figma (design review)

## Buying Journey
- **Discovery:** Google search, peer recommendations
- **Evaluation:** Free trial (must see value in 1 week)
- **Decision:** Needs buy-in from CMO and RevOps
- **Price sensitivity:** $500-2000/month budget
- **Deal breakers:** Steep learning curve, no integrations

## How We Help
Our product provides:
- Unified dashboard across all marketing tools
- Automated weekly reports (saves 5 hours)
- Attribution modeling (proves ROI)
- Real-time insights (no more waiting)
```

---

## Research Analysis & Synthesis

### Analyzing Qualitative Data

```markdown
## Thematic Analysis Process

### 1. Familiarization
- Review all interview notes and recordings
- Read through multiple times
- Immerse yourself in the data

### 2. Coding
- Identify interesting quotes and observations
- Tag with codes (labels): "pain point", "workaround", "delight"
- Use tools: Dovetail, Airtable, Miro, spreadsheet

### 3. Theme Generation
- Group similar codes into themes
- Look for patterns across interviews
- Name themes descriptively

Example themes:
- "Manual data entry is time-consuming and error-prone"
- "Users want real-time collaboration"
- "Onboarding is confusing for non-technical users"

### 4. Validation
- How many participants mentioned this? (frequency)
- How strongly did they feel? (intensity)
- Is this a real need or edge case?

### 5. Reporting
- Prioritize themes by importance and frequency
- Include supporting quotes
- Connect to product implications
```

### Affinity Mapping

```markdown
## What is it?
Collaborative method to organize research findings into themes

## Process
1. Write each insight on a sticky note (or digital equivalent)
2. Put all notes on wall/board
3. As a team, group similar notes together
4. Name each group (theme)
5. Look for higher-order patterns (meta-themes)

## Tools
- Physical: Sticky notes + wall
- Digital: Miro, Mural, FigJam

## Tips
✓ Involve whole product trio (PM, design, engineering)
✓ Use direct quotes from users
✓ Don't force groupings — let patterns emerge
✓ Take photos to document process
```

### Research Repository

```markdown
## Why You Need One
- Centralized location for all research
- Prevents knowledge loss when people leave
- Enables searching across past research
- Democratizes insights across org

## What to Include
- Interview recordings and transcripts
- Survey results and analysis
- Personas and user journey maps
- Competitive analysis
- Opportunity assessments
- Research reports and decks

## Tools
- Dovetail (purpose-built research repository)
- Notion (flexible, customizable)
- Confluence (enterprise, integrates with Jira)
- Airtable (database-style organization)

## Tagging Strategy
Tag research by:
- User segment / persona
- Product area / feature
- Research method
- Date conducted
- Researcher

Example: `#persona-sarah #feature-reporting #interview #2025-Q4`
```

---

## 2025 Trends in User Research

### AI-Assisted Research

```markdown
## AI Capabilities
- **Transcription:** Grain.co, Otter.ai (real-time transcription)
- **Analysis:** Dovetail (AI tags themes automatically)
- **Synthesis:** ChatGPT (summarize 10 interviews)
- **Translation:** Real-time multilingual research

## Best Practices
✓ Use AI to speed up transcription and initial tagging
✓ Human researchers still do interpretation
✓ Validate AI-generated themes with real quotes
✗ Don't outsource judgment to AI
✗ Don't skip talking to real users

## Example Workflow
1. Conduct interview (human)
2. Auto-transcribe with Grain.co (AI)
3. AI suggests initial themes (AI)
4. Researcher reviews, refines, validates (human)
5. Team workshop to synthesize (human)
```

### Continuous Research Ops

```markdown
## Modern Approach
Research is continuous, not projects

Weekly:
- 5 customer interviews
- Survey touchpoints (NPS, feature feedback)
- Usability tests on prototypes

Monthly:
- Synthesize themes
- Update personas
- Share insights org-wide

Quarterly:
- Deep-dive studies
- Competitive analysis
- Market trends

## Research Democratization
Not just researchers do research:
- PMs conduct interviews
- Designers run usability tests
- Engineers watch user sessions
- CX shares customer feedback

Research team role:
- Train others on methods
- Maintain research quality
- Curate insights repository
- Run strategic deep-dives
```

### Privacy-First Research

```markdown
## Compliance (GDPR, CCPA)
✓ Get explicit consent before recording
✓ Anonymize data (remove PII)
✓ Store securely (encrypted, access-controlled)
✓ Delete data when no longer needed
✓ Allow participants to withdraw/delete their data

## Ethical Practices
✓ Be transparent about how data is used
✓ Compensate fairly for participants' time
✓ Protect vulnerable populations
✓ Report findings honestly (don't cherry-pick)
```

---

## See Also

- [market-research.md](market-research.md) — TAM/SAM/SOM, competitive analysis
- [competitive-analysis.md](competitive-analysis.md) — Competitive frameworks
- [opportunity-frameworks.md](opportunity-frameworks.md) — JTBD, Kano, Value Prop Canvas
