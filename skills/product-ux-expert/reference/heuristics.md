# Nielsen's 10 Usability Heuristics - Deep Dive

## 1. Visibility of System Status

The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time.

### Good Examples

```
✓ Loading spinners with progress percentage
✓ "Saving..." → "Saved" confirmation
✓ Upload progress bar with time estimate
✓ Form field validation as you type
✓ Breadcrumb navigation showing location
✓ Order status tracking ("Shipped", "Out for delivery")
```

### Bad Examples

```
✗ Button clicked but no visual feedback
✗ Form submitted with no confirmation
✗ Page loading with no indicator
✗ Background sync with no notification
```

### Implementation Checklist

```markdown
- [ ] Every user action has immediate visual feedback
- [ ] Loading states show progress when possible
- [ ] Success/error states are clearly communicated
- [ ] Current location in navigation is visible
- [ ] System state changes are announced to screen readers
```

---

## 2. Match Between System and Real World

The design should speak the users' language. Use words, phrases, and concepts familiar to the user, rather than internal jargon.

### Good Examples

```
✓ "Shopping Cart" (not "Purchase Queue")
✓ "Your Files" (not "User Directory Assets")
✓ Calendar icons for date pickers
✓ Trash can icon for delete
✓ Heart icon for favorites/likes
```

### Bad Examples

```
✗ "Initiate session termination" (vs "Log out")
✗ "Null value detected in field" (vs "Please enter your email")
✗ Technical error codes shown to users
✗ Database field names in forms
```

### Language Guidelines

```
Technical Term         → User-Friendly Alternative
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Authenticate           → Sign in / Log in
Terminate session      → Log out / Sign out
Invalid input          → Please check your entry
Query                  → Search
Repository             → Storage / Files
Instantiate            → Create / Start
Null/undefined         → Not provided / Missing
```

---

## 3. User Control and Freedom

Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave the unwanted action without having to go through an extended process.

### Essential Controls

```
✓ Undo/Redo for all destructive actions
✓ Cancel button on dialogs
✓ Back navigation that works
✓ Clear all / Reset option
✓ Close button on modals (X and escape key)
✓ "Unsend" or grace period for sent messages
```

### Undo Patterns

```
Soft Delete (Recommended):
┌─────────────────────────────────────┐
│ Item deleted.         [Undo]        │
└─────────────────────────────────────┘
→ Shows toast for 10 seconds
→ Undo restores immediately
→ Permanent deletion after 30 days

Confirmation Dialog (Use Sparingly):
┌─────────────────────────────────────┐
│ Delete "Project Alpha"?             │
│                                     │
│ This will permanently delete all    │
│ files and cannot be undone.         │
│                                     │
│ [Cancel]            [Delete]        │
└─────────────────────────────────────┘
```

---

## 4. Consistency and Standards

Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions.

### Consistency Levels

```
1. Internal Consistency
   - Same terms throughout the product
   - Same interaction patterns everywhere
   - Same visual language (colors, icons, spacing)

2. External Consistency
   - Follow platform conventions (iOS/Android/Web)
   - Match user expectations from similar products
   - Use standard icons and gestures
```

### Common Conventions

```
Action              Standard Pattern
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary action      Bottom-right of modal
Secondary action    Left of primary button
Cancel              Leftmost button
Destructive         Red color, requires confirmation
Navigation          Top or left side
Search              Top-right with magnifying glass
Profile             Top-right avatar
Settings            Gear icon
```

---

## 5. Error Prevention

Good design prevents problems from occurring in the first place. Either eliminate error-prone conditions, or check for them and present users with a confirmation option.

### Prevention Strategies

```
1. Constraints
   ✓ Disable unavailable options
   ✓ Input masks for formatted data
   ✓ Date pickers instead of text input
   ✓ Dropdown for limited choices

2. Suggestions
   ✓ Autocomplete for known values
   ✓ "Did you mean...?" for typos
   ✓ Recent/popular choices first

3. Confirmation
   ✓ Confirm before destructive actions
   ✓ Show summary before final submission
   ✓ Preview before publishing
```

### Input Validation Examples

```html
<!-- Constrain input to valid format -->
<input
  type="tel"
  pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
  placeholder="123-456-7890"
/>

<!-- Provide real-time feedback -->
<input
  type="email"
  aria-describedby="email-hint"
/>
<span id="email-hint" role="status">
  Enter a valid email address
</span>
```

---

## 6. Recognition Rather Than Recall

Minimize the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the interface to another.

### Techniques

```
✓ Show recently used items
✓ Display saved preferences
✓ Visible navigation (not hidden menus)
✓ Persistent search with history
✓ Auto-fill from previous entries
✓ Preview thumbnails for files
✓ Labels visible (not just icons)
```

### Before vs After

```
❌ Before (Recall Required):
   Enter product code: [          ]

✅ After (Recognition):
   Select product:
   ┌─────────────────────────────────┐
   │ 📦 Widget Pro - WP-2024        │
   │ 📦 Widget Basic - WB-2024      │
   │ 📦 Widget Enterprise - WE-2024 │
   └─────────────────────────────────┘

   Recent: Widget Pro, Widget Basic
```

---

## 7. Flexibility and Efficiency of Use

Accelerators — unseen by the novice user — may speed up the interaction for the expert user such that the design can cater to both inexperienced and experienced users.

### Expert Features

```
Keyboard Shortcuts:
Ctrl/Cmd + S     → Save
Ctrl/Cmd + Z     → Undo
Ctrl/Cmd + K     → Command palette
/                → Focus search

Power User Features:
- Bulk actions (select all, batch edit)
- Customizable workspace
- Saved filters/views
- Templates for common tasks
- API access for automation
```

### Progressive Disclosure

```
Level 1: Essential options visible
         [Basic Settings]

Level 2: Advanced options collapsed
         [▸ Advanced Settings]

Level 3: Power features in separate area
         Settings → Developer → API Keys
```

---

## 8. Aesthetic and Minimalist Design

Interfaces should not contain information which is irrelevant or rarely needed. Every extra unit of information competes with the relevant units and diminishes their relative visibility.

### Signal-to-Noise Ratio

```
High Signal (Keep):
- Primary action button
- Essential form fields
- Key information
- Clear navigation

Noise (Remove/Hide):
- Decorative elements that distract
- Rarely used options in main view
- Redundant labels/instructions
- Excessive icons and badges
```

### Visual Hierarchy

```
1. Primary    → Large, bold, high contrast
2. Secondary  → Medium size, normal weight
3. Tertiary   → Smaller, lower contrast
4. Disabled   → Muted, reduced opacity
```

---

## 9. Help Users Recognize, Diagnose, and Recover from Errors

Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution.

### Error Message Formula

```
[What happened] + [Why it happened] + [How to fix it]

❌ Bad:  "Error 422"
✅ Good: "We couldn't save your changes because your
         session expired. Please log in again and
         your work will be restored."

❌ Bad:  "Invalid input"
✅ Good: "Password must be at least 8 characters and
         include a number"
```

### Error State Design

```
┌─────────────────────────────────────────────┐
│ ⚠️ We couldn't process your payment         │
│                                             │
│ Your card was declined. This might be       │
│ because:                                    │
│ • Insufficient funds                        │
│ • Card expired                              │
│ • Incorrect card number                     │
│                                             │
│ [Try Again]  [Use Different Card]           │
└─────────────────────────────────────────────┘
```

---

## 10. Help and Documentation

Even though it is better if the system can be used without documentation, it may be necessary to provide help. Any such information should be easy to search, focused on the user's task, list concrete steps, and not be too large.

### Help Hierarchy

```
1. Inline Help (First)
   - Tooltips on hover/focus
   - Placeholder examples
   - Contextual hints

2. Embedded Help (Second)
   - "?" icons next to complex features
   - Learn more links
   - Onboarding tours

3. Documentation (Third)
   - Searchable help center
   - Step-by-step guides
   - Video tutorials

4. Human Support (Last Resort)
   - Live chat
   - Email support
   - Phone support
```

### Tooltip Best Practices

```
✓ Appear on hover AND focus (accessibility)
✓ Short and actionable (max 2 sentences)
✓ Positioned to not obscure related content
✓ Dismissable with Escape key
✓ Not required for essential functionality
```

---

## Heuristic Evaluation Scoring Template

```markdown
| Heuristic | Score (1-5) | Issues Found | Severity |
|-----------|-------------|--------------|----------|
| 1. System Status | | | |
| 2. Real World Match | | | |
| 3. User Control | | | |
| 4. Consistency | | | |
| 5. Error Prevention | | | |
| 6. Recognition > Recall | | | |
| 7. Flexibility | | | |
| 8. Minimalist Design | | | |
| 9. Error Recovery | | | |
| 10. Help & Docs | | | |

Score Key:
1 = Critical issues, unusable
2 = Major issues, significant friction
3 = Moderate issues, workable but frustrating
4 = Minor issues, mostly good
5 = Excellent, follows best practices
```
