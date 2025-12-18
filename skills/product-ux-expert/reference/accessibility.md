# WCAG 2.2 Accessibility Guide

## Compliance Levels

```
Level A    — Minimum accessibility (legal baseline)
Level AA   — Standard target (recommended, EAA required)
Level AAA  — Enhanced accessibility (aspirational)
```

**Note:** European Accessibility Act (EAA) requires WCAG 2.2 AA compliance as of June 2025.

---

## Perceivable

### 1.1 Text Alternatives

```html
<!-- Good: Descriptive alt text -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2 2024" />

<!-- Good: Decorative image -->
<img src="decoration.png" alt="" role="presentation" />

<!-- Good: Complex image with long description -->
<figure>
  <img src="complex-diagram.png" alt="System architecture diagram"
       aria-describedby="diagram-desc" />
  <figcaption id="diagram-desc">
    The system consists of three layers: presentation,
    business logic, and data access...
  </figcaption>
</figure>

<!-- Icon buttons need labels -->
<button aria-label="Close dialog">
  <svg><!-- X icon --></svg>
</button>
```

### 1.2 Time-Based Media

```html
<!-- Video with captions and transcript -->
<video controls>
  <source src="tutorial.mp4" type="video/mp4" />
  <track kind="captions" src="captions.vtt" srclang="en" label="English" />
</video>
<details>
  <summary>Transcript</summary>
  <p>Full transcript of video content...</p>
</details>
```

### 1.3 Adaptable

```html
<!-- Semantic structure -->
<main>
  <article>
    <h1>Page Title</h1>
    <section aria-labelledby="section1">
      <h2 id="section1">Section Title</h2>
      <p>Content...</p>
    </section>
  </article>
</main>

<!-- Form with proper labels -->
<form>
  <div>
    <label for="email">Email Address</label>
    <input type="email" id="email" name="email"
           aria-describedby="email-hint" required />
    <span id="email-hint">We'll never share your email</span>
  </div>
</form>

<!-- Data tables with headers -->
<table>
  <caption>Monthly Sales Report</caption>
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">January</th>
      <td>$10,000</td>
    </tr>
  </tbody>
</table>
```

### 1.4 Distinguishable

```css
/* Color contrast requirements */
/* Normal text: 4.5:1 ratio minimum */
/* Large text (18pt or 14pt bold): 3:1 ratio minimum */
/* UI components and graphics: 3:1 ratio minimum */

.text-primary {
  color: #1a1a1a; /* On white: 14.4:1 ✓ */
}

.text-secondary {
  color: #595959; /* On white: 7.0:1 ✓ */
}

.text-disabled {
  color: #767676; /* On white: 4.54:1 ✓ (minimum) */
}

/* Focus indicators (WCAG 2.2) */
:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

@media (prefers-contrast: more) {
  :root {
    --border-color: #000000;
    --text-secondary: #1a1a1a;
  }
}
```

---

## Operable

### 2.1 Keyboard Accessible

```html
<!-- All interactive elements must be keyboard accessible -->
<button onclick="submit()">Submit</button> <!-- ✓ Native keyboard support -->

<!-- Custom interactive elements need tabindex and key handlers -->
<div role="button"
     tabindex="0"
     onclick="doAction()"
     onkeydown="handleKey(event)">
  Custom Button
</div>

<script>
function handleKey(event) {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    doAction();
  }
}
</script>

<!-- Skip links for keyboard navigation -->
<a href="#main-content" class="skip-link">Skip to main content</a>
<nav>...</nav>
<main id="main-content">...</main>

<style>
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  left: 10px;
  top: 10px;
  z-index: 9999;
  background: #000;
  color: #fff;
  padding: 8px 16px;
}
</style>
```

### 2.2 Enough Time

```javascript
// Auto-refresh with user control
let refreshTimeout;

function startAutoRefresh() {
  refreshTimeout = setTimeout(refreshData, 30000);
}

function pauseAutoRefresh() {
  clearTimeout(refreshTimeout);
  showNotification('Auto-refresh paused. Click to resume.');
}

// Session timeout with warning
function showTimeoutWarning() {
  // Show 2 minutes before timeout
  const dialog = document.getElementById('timeout-warning');
  dialog.showModal();
  // Focus the "extend session" button
  dialog.querySelector('#extend-button').focus();
}
```

### 2.4 Navigable

```html
<!-- Page title describes content -->
<title>Edit Profile - Settings - MyApp</title>

<!-- Focus order matches visual order -->
<form>
  <input tabindex="0" /> <!-- Natural order -->
  <input tabindex="0" />
  <button tabindex="0">Submit</button>
</form>

<!-- Avoid positive tabindex values -->
<!-- ❌ Bad: <input tabindex="2" /> -->

<!-- Link purpose is clear -->
<a href="/report.pdf">Download Q4 2024 Financial Report (PDF, 2.5MB)</a>

<!-- Multiple navigation methods -->
<nav aria-label="Main">...</nav>
<nav aria-label="Breadcrumb">...</nav>
<form role="search">...</form>
<nav aria-label="Pagination">...</nav>
```

### 2.5 Input Modalities (WCAG 2.2)

```html
<!-- Target size minimum 24x24px -->
<style>
.btn, .link, [role="button"] {
  min-width: 24px;
  min-height: 24px;
  /* Better: 44x44px for touch targets */
}

/* Ensure spacing between targets */
.icon-button + .icon-button {
  margin-left: 8px; /* Prevents accidental activation */
}
</style>

<!-- Dragging alternatives (2.5.7) -->
<div class="sortable-list">
  <div class="item" draggable="true">
    <span class="handle" aria-label="Drag to reorder">⠿</span>
    <span>Item 1</span>
    <!-- Alternative: position buttons -->
    <button aria-label="Move up">↑</button>
    <button aria-label="Move down">↓</button>
  </div>
</div>
```

---

## Understandable

### 3.1 Readable

```html
<!-- Declare page language -->
<html lang="en">

<!-- Declare language changes -->
<p>The French word <span lang="fr">bonjour</span> means hello.</p>

<!-- Define abbreviations -->
<abbr title="World Wide Web Consortium">W3C</abbr>
```

### 3.2 Predictable

```html
<!-- Don't change context on focus -->
<!-- ❌ Bad: Select that navigates on change -->
<select onchange="location.href = this.value">
  <option value="/page1">Page 1</option>
</select>

<!-- ✓ Good: Explicit submit -->
<form action="/search">
  <select name="page">
    <option value="/page1">Page 1</option>
  </select>
  <button type="submit">Go</button>
</form>

<!-- Consistent navigation -->
<nav aria-label="Main" class="main-nav">
  <!-- Same order on every page -->
  <a href="/">Home</a>
  <a href="/products">Products</a>
  <a href="/about">About</a>
  <a href="/contact">Contact</a>
</nav>
```

### 3.3 Input Assistance

```html
<!-- Error identification -->
<div class="form-field error">
  <label for="email">Email</label>
  <input type="email" id="email"
         aria-invalid="true"
         aria-describedby="email-error" />
  <span id="email-error" role="alert">
    Please enter a valid email address (e.g., user@example.com)
  </span>
</div>

<!-- Required fields -->
<label for="name">
  Name <span aria-hidden="true">*</span>
  <span class="sr-only">required</span>
</label>
<input id="name" required aria-required="true" />

<!-- Input instructions -->
<label for="password">Password</label>
<input type="password" id="password"
       aria-describedby="password-requirements" />
<div id="password-requirements">
  Must contain:
  <ul>
    <li>At least 8 characters</li>
    <li>One uppercase letter</li>
    <li>One number</li>
  </ul>
</div>
```

---

## Robust

### 4.1 Compatible

```html
<!-- Valid HTML -->
<!-- No duplicate IDs -->
<div id="unique-id-1">...</div>
<div id="unique-id-2">...</div>

<!-- Proper ARIA usage -->
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel2">Tab 2</button>
</div>
<div role="tabpanel" id="panel1">Content 1</div>
<div role="tabpanel" id="panel2" hidden>Content 2</div>

<!-- Status messages announced -->
<div role="status" aria-live="polite">
  <!-- Dynamic content announced to screen readers -->
  3 items added to cart
</div>

<div role="alert" aria-live="assertive">
  <!-- Urgent messages interrupt -->
  Session will expire in 2 minutes
</div>
```

---

## Testing Tools

### Automated Testing

```bash
# axe-core (most comprehensive)
npm install @axe-core/cli
npx axe https://example.com

# pa11y
npm install pa11y
npx pa11y https://example.com

# Lighthouse
npx lighthouse https://example.com --only-categories=accessibility
```

### Manual Testing Checklist

```markdown
## Keyboard Testing
- [ ] Tab through all interactive elements
- [ ] Verify focus is always visible
- [ ] Check focus order matches visual order
- [ ] Test Enter/Space on buttons and links
- [ ] Test Escape to close modals
- [ ] Verify no keyboard traps

## Screen Reader Testing
- [ ] VoiceOver (macOS): Cmd + F5
- [ ] NVDA (Windows): Free download
- [ ] JAWS (Windows): Commercial

Test with each:
- [ ] Page title announced
- [ ] Headings navigable (H key)
- [ ] Links make sense out of context
- [ ] Form labels announced
- [ ] Error messages announced
- [ ] Dynamic content announced

## Visual Testing
- [ ] Zoom to 200% (no horizontal scroll)
- [ ] Test in Windows High Contrast mode
- [ ] Check color contrast ratios
- [ ] Verify focus indicators visible
- [ ] Test without images loaded
```

---

## Quick Reference Card

```
PERCEIVABLE
├── Alt text for images
├── Captions for video
├── Color contrast 4.5:1
├── Text resizable to 200%
└── No info by color alone

OPERABLE
├── Keyboard accessible
├── Focus visible (2px outline)
├── Skip navigation
├── No keyboard traps
├── Target size 24×24px min
└── Drag alternatives

UNDERSTANDABLE
├── Language declared
├── Consistent navigation
├── Error identification
├── Labels for inputs
└── Instructions provided

ROBUST
├── Valid HTML
├── ARIA used correctly
├── Status messages announced
└── Works with assistive tech
```
