# Cognitive Psychology for UX Design

## Cognitive Load Theory

### The Three Types

```
INTRINSIC LOAD
├── Definition: Inherent complexity of the task
├── Example: Tax filing is complex by nature
├── Control: Simplify tasks, break into steps
└── Cannot be eliminated, only managed

EXTRANEOUS LOAD
├── Definition: Unnecessary complexity from poor design
├── Example: Confusing navigation, visual clutter
├── Control: Simplify UI, remove distractions
└── Should be eliminated entirely

GERMANE LOAD
├── Definition: Effort to build understanding
├── Example: Learning a new feature
├── Control: Progressive disclosure, good onboarding
└── Support this type of load
```

### Reducing Cognitive Load

```
1. Chunking
   Break information into digestible pieces

   ❌ 4111222233334444
   ✅ 4111 2222 3333 4444

2. Progressive Disclosure
   Show only what's needed at each step

   Step 1: Basic info    [Next →]
   Step 2: Details       [← Back] [Next →]
   Step 3: Review        [← Back] [Submit]

3. Recognition over Recall
   Show options instead of requiring memory

   ❌ Enter country code: [____]
   ✅ Select country: [🇺🇸 United States ▼]

4. Visual Hierarchy
   Guide attention to what matters

   ┌─────────────────────────┐
   │ PRIMARY ACTION          │ ← Most prominent
   ├─────────────────────────┤
   │ Secondary Action        │ ← Less prominent
   ├─────────────────────────┤
   │ tertiary action         │ ← Least prominent
   └─────────────────────────┘

5. Consistency
   Same patterns everywhere = less learning

   ✓ Edit icons always look the same
   ✓ Delete always requires confirmation
   ✓ Save is always in the same location
```

---

## Laws of UX

### Hick's Law

```
Time to decide = a + b × log₂(n)

Where n = number of choices

Implications:
• More choices = longer decision time
• Limit options to 5-7 items
• Use categorization for large sets
• Provide recommended/default option

Example:
❌ 20 plan options on pricing page
✅ 3 plans: Basic, Pro, Enterprise
   + "Which is right for me?" helper
```

### Fitts's Law

```
Time to target = a + b × log₂(1 + D/W)

Where D = distance, W = width

Implications:
• Large targets are easier to hit
• Close targets are faster to reach
• Corners and edges are infinite (on desktop)
• Touch targets: minimum 44×44px

Example:
❌ Small, spaced-out action buttons
✅ Full-width primary button on mobile
   ┌─────────────────────────────┐
   │       Complete Order        │
   └─────────────────────────────┘
```

### Miller's Law

```
Working memory capacity: 7 ± 2 items

Implications:
• Chunk related information
• Limit nav items to ~7
• Show progress in multi-step flows
• Don't require remembering across pages

Example:
❌ 15-field form on one page
✅ Multi-step form with progress:
   ○───●───○───○
   Personal  Address  Payment  Review
```

### Jakob's Law

```
Users spend most time on OTHER sites.
They expect your site to work like those.

Implications:
• Follow platform conventions
• Don't reinvent common patterns
• Test innovations carefully
• "Innovative" ≠ "Usable"

Example:
❌ Custom scrollbar behavior
❌ Unusual navigation patterns
❌ Non-standard icons
✅ Standard hamburger menu on mobile
✅ Cart icon in top-right
✅ Logo links to home
```

### Von Restorff Effect (Isolation Effect)

```
Items that stand out are more memorable.

Implications:
• Make CTAs visually distinct
• Use contrast for important elements
• Don't overuse — everything becomes nothing

Example:
┌─────────────────────────────────┐
│  Plan A      Plan B     Plan C  │
│  $10/mo      $20/mo     $30/mo  │
│                                 │
│ [Choose]   [Choose]   [Choose]  │
└─────────────────────────────────┘
                ↓
┌─────────────────────────────────┐
│  Plan A    ★ Plan B ★   Plan C  │
│  $10/mo      $20/mo     $30/mo  │
│            POPULAR              │
│ [Choose] [█ Choose █]  [Choose] │
└─────────────────────────────────┘
```

### Serial Position Effect

```
First (Primacy) and Last (Recency) items
are remembered best.

Implications:
• Put key info at start and end
• Most important nav items first/last
• Summarize key points at beginning and end

Example - Navigation:
✅ Home | Products | ... | Account | Help
   ↑ Start: Most used        End: Support ↑
```

### Zeigarnik Effect

```
Incomplete tasks are remembered better
than completed tasks.

Implications:
• Show progress to motivate completion
• Incomplete profiles nag at users
• Saved drafts keep users engaged

Example:
┌─────────────────────────────────┐
│ Your profile is 60% complete    │
│ ████████░░░░░░                 │
│ Add a photo to reach 80%        │
│ [Add Photo]                     │
└─────────────────────────────────┘
```

### Peak-End Rule

```
People judge experiences by:
1. The most intense moment (peak)
2. How it ended

Implications:
• Invest in delightful moments
• End on a positive note
• Smooth the worst friction points

Example:
• Peak: Confetti animation on achievement
• End: Friendly thank-you message
• Bad: Error on final submit step (memorable pain)
```

---

## Gestalt Principles

### Proximity

```
Elements close together are perceived as groups.

❌ Ambiguous grouping:
   Label          Input
   Another Label  Input

✅ Clear grouping:
   Label
   Input

   Another Label
   Input
```

### Similarity

```
Similar elements are perceived as related.

Example - Form actions:
┌─────────────────────────────────┐
│ [Cancel]           [Save Draft] │
│                    [Publish ██] │
└─────────────────────────────────┘

Secondary actions look similar (outlined)
Primary action looks different (filled)
```

### Continuity

```
Eyes follow smooth lines and curves.

Example - Progress indicator:
○ ── ● ── ○ ── ○
Step 1  Step 2  Step 3  Step 4

Eyes follow the line through steps
```

### Closure

```
Mind completes incomplete shapes.

Example - Loading indicator:
   ◜ ◝
   ◟ ◞

Perceived as a spinning circle
```

### Common Region

```
Elements in same bounded area are grouped.

Example - Card component:
┌─────────────────┐
│ Title           │
│ Description     │
│ [Action]        │
└─────────────────┘

Boundary creates perceived group
```

### Figure-Ground

```
Elements perceived as foreground or background.

Example - Modal:
┌───────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ░░░┌──────────────────┐░░░░░ │
│ ░░░│    Modal Title   │░░░░░ │
│ ░░░│    Content here  │░░░░░ │
│ ░░░│    [Submit]      │░░░░░ │
│ ░░░└──────────────────┘░░░░░ │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
└───────────────────────────────┘

Modal = Figure, Dimmed page = Ground
```

---

## Decision Architecture

### Default Effect

```
Users tend to stick with defaults.

Implications:
• Set defaults thoughtfully
• Make the "right" choice the default
• Don't use dark patterns

Example:
□ Subscribe to newsletter ← Opt-in (ethical)
☑ Subscribe to newsletter ← Pre-checked (questionable)
```

### Choice Architecture

```
How choices are presented affects decisions.

Techniques:
1. Anchoring: Show high price first
2. Decoy: Add option to make another look better
3. Scarcity: "Only 3 left"
4. Social proof: "1,000 people bought this"

Ethical use:
✓ Help users make informed decisions
✓ Highlight genuinely good options
✗ Manipulate users against their interests
```

### Paradox of Choice

```
Too many options lead to:
• Decision paralysis
• Lower satisfaction
• Regret

Solutions:
• Curate options (max 3-5)
• Provide recommendations
• Allow filtering
• Show "popular" or "staff pick"
```

---

## Attention & Focus

### Attentional Spotlight

```
Attention is limited and focused.

Design for scanning:
• Clear visual hierarchy
• F-pattern for text-heavy pages
• Z-pattern for landing pages
• Key info in first 2-3 lines
```

### Banner Blindness

```
Users ignore elements that look like ads.

Avoid:
• Flashy, animated banners
• Rectangular ad-like shapes
• Placement in typical ad locations
• Stock photo + headline layouts
```

### Inattentional Blindness

```
Users miss things they're not looking for.

Implications:
• Highlight important changes
• Use motion to attract attention
• Announce status changes audibly
• Don't hide critical info

Example:
Save button changes:
[ Save ] → [ ✓ Saved! ]
Need visual indication of state change
```

---

## Practical Application Checklist

```markdown
## Cognitive Load Audit
- [ ] Is the interface visually clean?
- [ ] Are related items grouped together?
- [ ] Is information chunked appropriately?
- [ ] Are defaults set to reduce decisions?
- [ ] Is navigation consistent across pages?

## Attention Audit
- [ ] Is primary action obvious?
- [ ] Is visual hierarchy clear?
- [ ] Are important elements above the fold?
- [ ] Do animations serve a purpose?
- [ ] Is there appropriate whitespace?

## Memory Audit
- [ ] Can users complete tasks without memorizing?
- [ ] Are recently used items accessible?
- [ ] Is search/filter available for long lists?
- [ ] Are instructions visible when needed?

## Decision Audit
- [ ] Are choices limited to 5-7 options?
- [ ] Is there a recommended option?
- [ ] Are defaults helpful (not manipulative)?
- [ ] Is there a clear path to decision?
```
