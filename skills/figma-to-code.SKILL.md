---
name: figma-to-code
description: Extract Figma designs and generate production-ready React/Next.js components with TypeScript, Tailwind CSS, and pixel-perfect accuracy. Use when a user provides a Figma URL or asks to convert Figma designs to code.
---

# Figma to Code - Production-Ready Component Generator

## 🎯 Purpose

Extract **complete, lossless** design information from Figma and generate production-ready React/Next.js components with TypeScript and Tailwind CSS.

---

## 🚨 CRITICAL RULES - Read First!

### **Rule 1: NEVER Truncate Code**

Use **100% of Figma MCP output**. Every className, every property matters.

```tsx
// ✅ CORRECT: Keep ALL className from Figma MCP
<div className="absolute font-source-serif h-[108px] leading-[1.8] left-[100px] not-italic text-[20px] text-[rgba(29,38,45,0.8)] text-justify top-[210px] w-[1096px] whitespace-pre-wrap">

// ❌ WRONG: Removing any className
<div className="absolute left-[100px] top-[210px] font-source-serif text-[20px]">
```

### **Rule 2: Flatten `absolute contents` Structures**

**🔥 CRITICAL: Figma MCP returns nested `absolute contents` containers. `display: contents` makes the parent "disappear" - children are positioned relative to the nearest positioned ancestor (root)!**

**Key Insight: Children's positions are ALREADY absolute - DO NOT add parent's top/left!**

```tsx
// ❌ WRONG: Figma MCP output (has redundant parent wrapper)
<div className="absolute contents left-0 top-[41px]">
  <p className="absolute left-[100px] top-[41px]">TITLE</p>
  <div className="absolute left-0 top-[100px]">Line</div>
</div>

// ✅ CORRECT: Just remove the parent wrapper, keep children's positions AS-IS
<>
  <p className="absolute left-[100px] top-[41px]">TITLE</p>
  <div className="absolute left-0 top-[100px] w-[1920px] h-[1px] bg-[#C5CBCE] opacity-30" />
</>
```

**Position Handling Rules:**

| Parent Type | Child Position | Action |
|-------------|----------------|--------|
| `absolute contents` | Child has own `top/left` | **Keep child position AS-IS**, just remove parent |
| `absolute` (no contents) | Child has relative `top/left` | Calculate: `parent + child` |
| `relative` | Child has `top/left` | Calculate: `parent + child` |

**🔥 The Golden Rule:**
```
If parent has "contents" class → Child positions are already absolute → Keep AS-IS
If parent has NO "contents" class → Child positions are relative → Add parent + child
```

**Reference: Verified correct positions (from production HTML):**
- Header text: `top-[41px]` (not 82px)
- Header line: `top-[100px]` (not 141px)
- Footer line: `top-[980px]`
- Page number: `top-[1004px]`

### **Rule 3: Extract Dimensions from Metadata**

**NEVER hardcode dimensions!**

```typescript
// 1. Get metadata first
const metadata = await mcp__figma__get_metadata({
  fileKey: 'xxx',
  nodeId: '11:1420'
})

// 2. Extract from XML
// <frame width="1920" height="1080">
const pageWidth = 1920
const pageHeight = 1080

// 3. Use extracted values
<div className="w-[1920px] h-[1080px]">
```

### **Rule 4: Font Loading & Name Mapping**

**🔥 CRITICAL: Use Google Fonts CDN directly, NOT `next/font/google`!**

`next/font/google` generates CSS variables and self-hosts fonts, but the font rendering may differ from reference HTML that uses Google Fonts CDN directly. This causes:
- Different character widths (text wrapping issues)
- Different optical size handling for variable fonts

#### **4.1 Font Loading (layout.tsx)**

```tsx
// ❌ WRONG: Using next/font/google
import { Source_Serif_4, Kaisei_Tokumin } from 'next/font/google'
const sourceSerif = Source_Serif_4({ subsets: ['latin'], variable: '--font-source-serif' })
// This may render fonts differently than Google Fonts CDN!

// ✅ CORRECT: Use Google Fonts CDN directly in layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,200..900;1,8..60,200..900&family=Kaisei+Tokumin:wght@400;500;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

**Key:** Include `opsz` (optical size) axis for Source Serif 4 - this affects character widths!

#### **4.2 Font CSS (globals.css)**

```css
@layer utilities {
  /* Use direct font-family names, NOT CSS variables */
  .font-source-serif {
    font-family: 'Source Serif 4', serif;
  }
  .font-kaisei {
    font-family: 'Kaisei Tokumin', serif;
  }
}
```

#### **4.3 Font Name Mapping**

```typescript
// Figma MCP returns:
font-['Kaisei_Tokumin:ExtraBold',sans-serif]
font-['Source_Serif_Pro:SemiBold',sans-serif]

// ✅ Convert to Tailwind classes:
font-kaisei font-extrabold
font-source-serif font-semibold

// Font name corrections (Google Fonts 2024):
'Source Serif Pro' → 'Source Serif 4'
'Source Sans Pro' → 'Source Sans 3'
```

#### **4.4 Font Weight Mismatch Warning**

**⚠️ Figma's font weight names may NOT match CSS font-weights!**

Figma renders fonts differently than browsers. What Figma calls "Bold" might visually appear lighter than CSS `font-weight: 700`.

| Figma Weight Name | Expected CSS | May Actually Need |
|-------------------|--------------|-------------------|
| Regular | 400 | 400 |
| Medium | 500 | 500 |
| Bold | 700 | **500 or 600** (test visually!) |
| ExtraBold | 800 | **700** (test visually!) |

**Solution:** Always compare with Figma screenshot. If text looks too bold, try one weight lighter:
- `font-bold` (700) → try `font-medium` (500)
- `font-extrabold` (800) → try `font-bold` (700)

### **Rule 5: Critical CSS**

**Must add to globals.css:**

```css
body {
  overflow-x: auto; /* Allow horizontal scroll */
}

.page-container {
  min-width: max-content;  /* Prevent compression */
  display: inline-block;   /* Keep layout intact */
}
```

### **Rule 6: Replace Simple Images with CSS**

**Optimize line images:**

```tsx
// ❌ Before: Image-based line
<div className="absolute h-0 left-0 top-[100px] w-[1920px]">
  <div className="absolute inset-[-1px_0_0_0]">
    <img src={imgLine} />
  </div>
</div>

// ✅ After: CSS-based line
<div className="absolute left-0 top-[141px] w-[1920px] h-[1px] bg-[#C5CBCE] opacity-30" />
```

### **Rule 7: Inline SVG Assets**

```tsx
// ❌ Before: External image
<img src={imgVector} />

// ✅ After: Inline SVG
<svg viewBox="0 0 35 34" fill="none">
  <path d="M17.5 0L0 34..." fill="#1d262d"/>
</svg>
```

### **Rule 7.5: Remove Fixed Heights from Text Blocks**

**🔥 CRITICAL: Figma MCP outputs fixed heights for text blocks, but this causes line-wrapping issues!**

Font metrics differ between Figma's rendering and browser rendering (even with the same font family). Fixed heights can cause:
- Text overflow or clipping
- Different line counts than expected
- Layout breaks when font rendering differs slightly

```tsx
// ❌ WRONG: Figma MCP output with fixed height
<p className="absolute h-[72px] leading-[1.8] left-[100px] text-[20px] top-[570px] w-[1096px]">
  Long text that might wrap differently in browser...
</p>

// ✅ CORRECT: Remove h-[Xpx], let text flow naturally
<div className="absolute leading-[1.8] left-[100px] text-[20px] top-[570px] w-[1096px]">
  <p className="mb-0">Long text that might wrap differently in browser...</p>
</div>
```

**When to keep fixed heights:**
- Container elements (cards, boxes) - keep dimensions
- Table rows with single-line content - keep `h-[34px]`
- Images and icons - keep dimensions

**When to remove fixed heights:**
- Multi-line text paragraphs - ALWAYS remove `h-[Xpx]`
- Text blocks with `text-justify` - especially important
- Any text that could wrap differently

**Pattern: Use `<div>` wrapper with `<p className="mb-0">`:**
```tsx
// This matches reference HTML structure and ensures proper text flow
<div className="absolute font-source-serif leading-[1.8] left-[100px] text-[20px] top-[570px] w-[1096px]">
  <p className="mb-0">Text content here...</p>
</div>
```

### **Rule 8: Table Pattern Detection & Conversion**

**🔥 CRITICAL: Figma designs tables using absolute positioning, NOT HTML `<table>` elements!**

#### **How to Detect Table Patterns**

Look for these characteristics in Figma MCP output:

```tsx
// Table pattern indicators:
// 1. Multiple rows with same height (e.g., h-[34px])
// 2. Repeating left positions across rows (columns)
// 3. Parent container with flex flex-col
// 4. Background color alternation (header vs data rows)

// Example Figma MCP output for a table:
<div className="flex flex-col w-[1792px]">
  {/* Header row - distinct background */}
  <div className="bg-[#decfba] h-[34px] relative">
    <p className="absolute left-[60px]">Label</p>
    <p className="absolute left-[418px]">Jun-26</p>
    <p className="absolute left-[669px]">Jun-26</p>
    <p className="absolute left-[920px]">Jun-26</p>
  </div>
  {/* Data rows - same structure, different content */}
  <div className="h-[34px] relative">
    <p className="absolute left-[60px]">Row Label</p>
    <p className="absolute left-[477px] -translate-x-full">$6,185,061</p>
    <p className="absolute left-[728px] -translate-x-full">$6,185,061</p>
  </div>
</div>
```

#### **Detection Checklist**

| Pattern | Indicator |
|---------|-----------|
| **Repeating structure** | Multiple divs with same `h-[Xpx]` |
| **Column alignment** | Same `left-[Xpx]` values across rows |
| **Header distinction** | First row has different `bg-[color]` |
| **Right-aligned numbers** | Uses `left-[Xpx] -translate-x-full` |
| **Container** | Parent has `flex flex-col` |

#### **Conversion Options**

**Option A: Follow Figma Exactly (RECOMMENDED)**

Keep absolute positioning from Figma MCP. This ensures pixel-perfect accuracy.

```tsx
// ✅ RECOMMENDED: Use Figma's absolute positioning
<div className="flex flex-col w-[1792px]">
  {/* Header */}
  <div className="bg-[#decfba] h-[34px] relative shrink-0">
    <p className="absolute left-[60px] top-[7px]">Year Ending</p>
    <p className="absolute left-[418px] top-[7px]">Jun-26</p>
    <p className="absolute left-[669px] top-[7px]">Jun-26</p>
    <p className="absolute left-[920px] top-[7px]">Jun-26</p>
  </div>
  {/* Data rows */}
  <div className="h-[34px] relative shrink-0">
    <p className="absolute left-[60px] top-[7px]">Revenue</p>
    <p className="absolute left-[477px] top-[7px] -translate-x-full">$6,185,061</p>
    <p className="absolute left-[728px] top-[7px] -translate-x-full">$6,185,061</p>
  </div>
</div>
```

**Option B: Convert to Semantic HTML Table (NOT RECOMMENDED)**

Only use if semantic HTML is explicitly required (accessibility, SEO).

⚠️ **Conversion Challenges:**
- Must calculate column widths from Figma positions
- HTML tables don't support Tailwind width on `<col>` (needs inline styles)
- React hydration requires `<thead>` and `<tbody>` wrappers
- `table-layout: fixed` required for precise column control
- Right-aligned values need `text-right` class on cells

```tsx
// ⚠️ ONLY if semantic HTML required - complex and error-prone
<table className="w-[1792px] table-fixed border-collapse">
  <colgroup>
    <col style={{ width: '358px' }} />  {/* 418 - 60 = 358 */}
    <col style={{ width: '251px' }} />  {/* 669 - 418 = 251 */}
    <col style={{ width: '251px' }} />  {/* 920 - 669 = 251 */}
    {/* Calculate each column width from left positions */}
  </colgroup>
  <thead>
    <tr className="bg-[#decfba] h-[34px]">
      <th className="text-left pl-[60px]">Year Ending</th>
      <th className="text-left">Jun-26</th>
      <th className="text-left">Jun-26</th>
    </tr>
  </thead>
  <tbody>
    <tr className="h-[34px]">
      <td className="pl-[60px]">Revenue</td>
      <td className="text-right pr-[calc(251px-59px)]">$6,185,061</td>
      <td className="text-right pr-[calc(251px-59px)]">$6,185,061</td>
    </tr>
  </tbody>
</table>
```

#### **Column Width Calculation (for Option B)**

```typescript
// Given Figma left positions: [60, 418, 669, 920, 1173, 1391, 1619, 1792]
// Calculate column widths:
const positions = [60, 418, 669, 920, 1173, 1391, 1619, 1792]
const widths = positions.slice(1).map((pos, i) => pos - positions[i])
// Result: [358, 251, 251, 253, 218, 228, 173]
```

#### **Right-Alignment Pattern**

Figma uses a clever pattern for right-aligned numbers:

```tsx
// Figma pattern: position at right edge, then translate left by 100%
<p className="absolute left-[477px] -translate-x-full">$6,185,061</p>

// This means: the RIGHT edge of text is at left-[477px]
// The 477px is the column's right boundary (418 + 59 padding)

// For HTML table conversion, use:
<td className="text-right">$6,185,061</td>
```

#### **Why Option A is Better**

| Aspect | Option A (Absolute) | Option B (Table) |
|--------|---------------------|------------------|
| Accuracy | Pixel-perfect | Approximation |
| Complexity | Low | High |
| Maintainability | Easy | Difficult |
| Column widths | Automatic | Manual calculation |
| Right alignment | Built-in | Extra CSS needed |
| React hydration | No issues | Needs thead/tbody |

**🔥 Golden Rule: When in doubt, follow Figma MCP output exactly!**

#### **Creating Reusable Table Row Components**

When implementing tables with Option A, create a reusable `TableRow` component to reduce code duplication:

```tsx
/**
 * Table Component Documentation Template
 *
 * 🔥 Table Pattern: Uses Figma's absolute positioning (Rule 8 Option A)
 *
 * Column positions:
 * - Label column: left-[60px]
 * - Data headers: left-[418px], left-[669px], left-[920px], ...
 * - Data values (right-aligned): left-[477px], left-[728px], left-[979px], ...
 *   with -translate-x-full for right alignment
 *
 * Row types:
 * - Header: bg-[#decfba] font-semibold
 * - Section header: font-semibold (no bg)
 * - Data: text-[rgba(29,38,45,0.8)]
 * - Subtotal: bg-[#d7dee3] font-semibold
 * - Total: bg-[#232b32] text-white font-semibold
 */

// Define row variants based on Figma design
type RowVariant = 'header' | 'section' | 'data' | 'subtotal' | 'total'

// Reusable TableRow component
const TableRow = ({
  label,
  values,
  variant = 'data',
}: {
  label: string
  values?: string[]
  variant?: RowVariant
}) => {
  // Background colors from Figma
  const bgClass = {
    header: 'bg-[#decfba]',
    section: '',
    data: '',
    subtotal: 'bg-[#d7dee3]',
    total: 'bg-[#232b32]',
  }[variant]

  // Text styles from Figma
  const textClass = {
    header: 'font-source-serif font-semibold text-[#1d262d]',
    section: 'font-source-serif font-semibold text-[#1d262d]',
    data: 'font-source-serif text-[rgba(29,38,45,0.8)]',
    subtotal: 'font-source-serif font-semibold text-[#1d262d]',
    total: 'font-source-serif font-semibold text-white',
  }[variant]

  // 🔥 CRITICAL: Extract these positions from Figma MCP output!
  // Header positions (left-aligned column headers)
  const headerPositions = [
    'left-[418px]', 'left-[669px]', 'left-[920px]',
    'left-[1173px]', 'left-[1391px]', 'left-[1619px]'
  ]
  // Data value positions (right-aligned with -translate-x-full)
  const dataPositions = [
    'left-[477px]', 'left-[728px]', 'left-[979px]',
    'left-[1232px]', 'left-[1450px]', 'left-[1678px]'
  ]

  return (
    <div className={`${bgClass} ${textClass} h-[34px] leading-[20px] relative shrink-0 text-[20px] w-[1792px]`}>
      <p className="absolute left-[60px] top-[7px]">{label}</p>
      {values?.map((value, i) => (
        <p
          key={i}
          className={`absolute top-[7px] ${
            variant === 'header'
              ? headerPositions[i]
              : `${dataPositions[i]} text-right -translate-x-full`
          }`}
        >
          {value}
        </p>
      ))}
    </div>
  )
}
```

#### **Complete Table Component Example**

```tsx
export default function FinancialTable() {
  const headers = ['Jun-26', 'Jun-26', 'Jun-26', 'Jun-26', 'Jun-26', 'Jun-26']
  const dataValues = ['$6,185,061', '$6,185,061', '$6,185,061', '$6,185,061', '$6,185,061', '$6,185,061']

  return (
    <div className="page-container">
      <div className="bg-[#f8f7f5] relative w-[1920px] h-[1080px]">
        {/* Tables Container - positions from Figma */}
        <div className="absolute flex flex-col h-[728px] items-center left-[100px] top-[234px] w-[1720px]">
          <div className="flex flex-col gap-[48px] items-start relative shrink-0">
            {/* Table 1 */}
            <div className="flex flex-col items-start relative shrink-0">
              <TableRow label="Year Ending" values={headers} variant="header" />
              <TableRow label="Revenue" variant="section" />
              <TableRow label="Rental Income" values={dataValues} variant="data" />
              <TableRow label="Other Income" values={dataValues} variant="data" />
              <TableRow label="Total Revenue" values={dataValues} variant="subtotal" />
              <TableRow label="Net Operating Income" values={dataValues} variant="total" />
            </div>

            {/* Table 2 - separated by gap-[48px] */}
            <div className="flex flex-col items-start relative shrink-0">
              <TableRow label="Year Ending" values={headers} variant="header" />
              <TableRow label="Cash Flow" values={dataValues} variant="data" />
              <TableRow label="Total" values={dataValues} variant="total" />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

#### **Key Patterns Summary**

| Pattern | Implementation |
|---------|----------------|
| **Row height** | `h-[34px]` (extract from Figma) |
| **Row width** | `w-[1792px]` (extract from Figma) |
| **Label position** | `absolute left-[60px] top-[7px]` |
| **Header values** | `absolute left-[Xpx] top-[7px]` (left-aligned) |
| **Data values** | `absolute left-[Xpx] top-[7px] -translate-x-full` (right-aligned) |
| **Multiple tables** | Wrap in `flex flex-col gap-[48px]` |
| **Row variants** | Use object lookup for bg/text classes |

#### **Position Extraction Workflow**

```typescript
// 1. From Figma MCP output, find repeating left-[Xpx] patterns
// Header row example:
<p className="absolute left-[418px] top-[7px]">Jun-26</p>
<p className="absolute left-[669px] top-[7px]">Jun-26</p>
// → headerPositions = ['left-[418px]', 'left-[669px]', ...]

// 2. For data rows, find the translate-x-[-100%] pattern
<p className="absolute left-[477px] ... translate-x-[-100%]">$6,185,061</p>
<p className="absolute left-[728px] ... translate-x-[-100%]">$6,185,061</p>
// → dataPositions = ['left-[477px]', 'left-[728px]', ...]

// 3. Note: dataPositions are typically headerPositions + cell padding
// e.g., 477 = 418 + 59 (right edge of column)
```

---

## 📋 Complete Workflow

### **Phase 1: Extract Figma Data**

**🔥 CRITICAL: Save ALL MCP data to project directory for reuse!**

#### **Step 0: Create MCP Cache Directory**

All Figma MCP data must be saved to the project's `.figma-mcp/` directory:

```
project-root/
├── .figma-mcp/
│   ├── disclaimer/                 # Page name as folder (kebab-case)
│   │   ├── metadata.xml            # get_metadata result
│   │   ├── design-context.tsx      # get_design_context result (full code)
│   │   ├── screenshot.png          # get_screenshot result (if available)
│   │   └── info.json               # Node info (nodeId, name, dimensions, timestamp)
│   ├── financing-summary/
│   │   ├── metadata.xml
│   │   ├── design-context.tsx
│   │   └── info.json
│   └── README.md                   # Index of all cached pages
```

**Folder naming convention:**
- Use page name in kebab-case (e.g., `financing-summary`, `table-of-contents`)
- Keep `info.json` containing the `nodeId` for reference
- This makes the cache human-readable and easier to navigate

**Why cache MCP data:**
- Avoid repeated API calls (rate limits, latency)
- Full data preservation - no truncation or loss
- Easy debugging and reference
- Reproducible builds

#### **Step 1: Call Figma MCP Tools**

```typescript
// Call these in parallel
const [metadata, designContext, screenshot] = await Promise.all([
  mcp__figma__get_metadata({
    fileKey: 'DqEDSJTN6hW7rSw0fy6gq9',
    nodeId: '11-1420',
    clientLanguages: 'typescript',
    clientFrameworks: 'react,nextjs'
  }),
  mcp__figma__get_design_context({
    fileKey: 'DqEDSJTN6hW7rSw0fy6gq9',
    nodeId: '11-1420',
    clientLanguages: 'typescript',
    clientFrameworks: 'react,nextjs'
  }),
  mcp__figma__get_screenshot({
    fileKey: 'DqEDSJTN6hW7rSw0fy6gq9',
    nodeId: '11-1420',
    clientLanguages: 'typescript',
    clientFrameworks: 'react,nextjs'
  })
])

// Step 2: IMMEDIATELY save to project directory
// Save metadata.xml - contains positions, dimensions, node structure
// Save design-context.tsx - contains full generated code with all className
// Save info.json - contains node name, page dimensions, fetch timestamp
```

**Step 2: Extract Information**

From **metadata**:
```xml
<frame id="11:1420" width="1920" height="1080">
  <text id="11:1421" x="100" y="132" width="216" height="46" />
</frame>
```

From **design_context**:
```tsx
<div className="bg-[#f8f7f5] relative size-full">
  <p className="absolute font-kaisei font-extrabold ... text-[32px] ...">
    DISCLAIMER
  </p>
  <div className="absolute contents left-0 top-[41px]">
    {/* Nested structure - needs flattening */}
  </div>
</div>
```

---

### **Phase 2: Transform Figma MCP Output**

**Step 1: Flatten `absolute contents` Structures**

Algorithm:
```
1. Find all elements with className="absolute contents"
2. For each nested child:
   a. KEEP child's top/left AS-IS (parent with "contents" doesn't affect positioning!)
   b. Remove parent wrapper
   c. Replace <img> with CSS/SVG
```

Example transformation:
```tsx
// Input: Figma MCP output
<div className="absolute contents left-0 top-[41px]" data-node-id="11:1423">
  <div className="absolute h-0 left-0 top-[100px] w-[1920px]" data-node-id="11:1424">
    <div className="absolute inset-[-1px_0_0_0]">
      <img src={imgLine2} />
    </div>
  </div>
  <p className="absolute font-kaisei font-bold ... left-[100px] ... top-[41px]" data-node-id="11:1425">
    159-161 WEST 54TH STREET
  </p>
  <div className="absolute h-[34px] left-[1785px] top-[42px] w-[35px]" data-node-id="11:1426">
    <img src={imgVector} />
  </div>
</div>

// Output: Flattened React code
// 🔥 Parent has "contents" - children positions stay AS-IS!
// Line: top-[100px] (NOT 141px!)
// Text: top-[41px] (NOT 82px!)
// Logo: top-[42px] (NOT 83px!)

<>
  {/* Horizontal line - Replace img with CSS */}
  <div className="absolute left-0 top-[100px] w-[1920px] h-[1px] bg-[#C5CBCE] opacity-30" />

  {/* Title */}
  <p className="absolute font-kaisei font-bold leading-normal left-[100px] not-italic opacity-80 text-[#1d262d] text-[24px] top-[41px]">
    159-161 WEST 54TH STREET
  </p>

  {/* Logo - Inline SVG */}
  <svg viewBox="0 0 35 34" fill="none" className="absolute left-[1785px] top-[42px] w-[35px] h-[34px]">
    <path d="M17.5 0L0 34C8.10511..." fill="#1d262d"/>
  </svg>
</>
```

**Step 2: Convert Font Names**

```typescript
const convertFigmaFont = (className: string) => {
  return className
    .replace(/font-\['Kaisei_Tokumin:Bold',sans-serif\]/g, 'font-kaisei font-bold')
    .replace(/font-\['Kaisei_Tokumin:ExtraBold',sans-serif\]/g, 'font-kaisei font-extrabold')
    .replace(/font-\['Source_Serif_Pro:Regular',sans-serif\]/g, 'font-source-serif')
    .replace(/font-\['Source_Serif_Pro:SemiBold',sans-serif\]/g, 'font-source-serif font-semibold')
}
```

**Step 3: Simplify Nested Flex Containers (Optional)**

Remove redundant `flex flex-col` wrappers:

```tsx
// ❌ Figma MCP output (complex)
<div className="absolute bg-[#f1efeb] flex flex-col p-[24px]">
  <div className="flex flex-col">
    <div className="h-[51px]">Row 1</div>
    <div className="h-[51px]">Row 2</div>
  </div>
  <div className="h-[51px]">Row 3</div>
</div>

// ✅ Simplified (flat)
<div className="absolute bg-[#f1efeb] p-[24px]">
  <div className="h-[51px] relative w-full">Row 1</div>
  <div className="h-[51px] relative w-full">Row 2</div>
  <div className="h-[51px] relative w-full">Row 3</div>
</div>
```

---

### **Phase 3: Generate React Component**

**Template:**

```tsx
export default function PageName() {
  return (
    <div className="page-container">
      <div className="bg-[#f8f7f5] relative w-[1920px] h-[1080px]">
        {/* Insert flattened, optimized code here */}

        {/* All className preserved from Figma MCP */}
        {/* All positions calculated correctly */}
        {/* All fonts mapped */}
        {/* All images optimized */}
      </div>
    </div>
  )
}
```

---

### **Phase 4: Verify Against Screenshot**

**Checklist:**
- [ ] Page dimensions match (1920x1080)
- [ ] All text visible and positioned correctly
- [ ] Font sizes match Figma (text-[20px], text-[24px], text-[32px])
- [ ] Colors match exactly
- [ ] Spacing is pixel-perfect
- [ ] No layout compression (page-container CSS working)

**Compare with Figma screenshot side-by-side**

---

## 🎨 Font Configuration

**app/layout.tsx:**

```typescript
import { Source_Serif_4, Kaisei_Tokumin, Inter } from 'next/font/google'

const sourceSerif = Source_Serif_4({
  subsets: ['latin'],
  weight: ['200', '300', '400', '500', '600', '700', '800', '900'],
  variable: '--font-source-serif',
  display: 'swap',
})

const kaisei = Kaisei_Tokumin({
  subsets: ['latin'],
  weight: ['400', '500', '700', '800'],
  variable: '--font-kaisei',
  display: 'swap',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${sourceSerif.variable} ${kaisei.variable}`}>
      <body className="m-0 p-0 overflow-x-auto">{children}</body>
    </html>
  )
}
```

**app/globals.css:**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    overflow-x: auto;
  }
}

@layer utilities {
  .font-source-serif {
    font-family: var(--font-source-serif);
  }
  .font-kaisei {
    font-family: var(--font-kaisei);
  }
  .page-container {
    min-width: max-content;
    display: inline-block;
  }
}
```

---

## 📦 Font Mapping Reference

```typescript
const FONT_MAPPINGS = {
  // Kaisei Tokumin
  "font-['Kaisei_Tokumin',sans-serif]": "font-kaisei",
  "font-['Kaisei_Tokumin:Bold',sans-serif]": "font-kaisei font-bold",
  "font-['Kaisei_Tokumin:ExtraBold',sans-serif]": "font-kaisei font-extrabold",

  // Source Serif Pro → Source Serif 4 (renamed 2024)
  "font-['Source_Serif_Pro',sans-serif]": "font-source-serif",
  "font-['Source_Serif_Pro:Regular',sans-serif]": "font-source-serif",
  "font-['Source_Serif_Pro:SemiBold',sans-serif]": "font-source-serif font-semibold",

  // Inter
  "font-['Inter',sans-serif]": "font-inter",
}
```

---

## ⚠️ Common Mistakes

1. ❌ **Adding parent+child positions when parent has "contents"** → Elements at wrong positions!
   - 🔥 If parent has `absolute contents`, child positions are ALREADY absolute - keep AS-IS!
2. ❌ **Not flattening `absolute contents`** → Wrapper causes issues
3. ❌ **Removing className** → Spacing/sizing wrong
4. ❌ **Hardcoding dimensions** → Not scalable
5. ❌ **Missing `page-container` CSS** → Layout compressed
6. ❌ **Wrong font names** → Fonts don't load
7. ❌ **Not comparing with screenshot** → Visual bugs
8. ❌ **Converting table-like layouts to HTML `<table>`** → Column alignment breaks!
   - 🔥 Figma uses absolute positioning for tables - keep it that way!
   - HTML table conversion requires manual column width calculation
   - Right-aligned values use `left-[Xpx] -translate-x-full`, not `text-right`
9. ❌ **Keeping fixed heights `h-[Xpx]` on multi-line text blocks** → Text wrapping issues!
   - 🔥 Font metrics differ between Figma and browser - text may need more/fewer lines
   - Remove `h-[72px]`, `h-[108px]` etc. from text paragraphs
   - Keep only `top-[Xpx]` for positioning, let height be automatic
10. ❌ **Using `next/font/google` instead of Google Fonts CDN** → Character width differences!
    - 🔥 `next/font` may load fonts with different optical size settings
    - Use Google Fonts CDN directly in `<head>` for exact match with reference HTML
    - Include `opsz` axis for variable fonts: `Source+Serif+4:ital,opsz,wght@0,8..60,200..900`
11. ❌ **Trusting Figma's font weight names** → Text appears too bold/light!
    - 🔥 Figma "Bold" ≠ CSS `font-weight: 700` in visual appearance
    - Always compare with Figma screenshot, not just weight names
    - May need to use one weight lighter than Figma suggests
12. ❌ **Using `grid-cols-N` with equal columns for tables** → Text overlap/truncation!
    - 🔥 CSS Grid with equal columns (`grid-cols-4`) creates fixed-width columns
    - Long text like "Mortgage Placement Fee" can overflow in narrow columns
    - **Solution:** Use HTML `<table>` for auto-sizing columns, or specify custom column widths
    - Example: Instead of `grid-cols-4`, use `grid-cols-[200px_150px_250px_200px]`

13. ❌ **Flattening elements inside nested frames incorrectly** → Footnotes/elements at wrong position!
    - 🔥 Elements inside nested frames (NOT `absolute contents`) have RELATIVE positions
    - Must calculate: `parent frame top + child top` for absolute position
    - **Example from Figma MCP:**
      ```tsx
      // Figma structure:
      // - Frame 168 at top-[132px] (NOT contents!)
      //   - Footnote at top-[772px] (relative to Frame 168)

      // ❌ WRONG: Use child position directly
      <p className="absolute top-[772px]">Footnote text</p>

      // ✅ CORRECT: Calculate absolute position = 132 + 772 = 904px
      <p className="absolute top-[904px]">Footnote text</p>
      ```
    - **Key distinction:**
      - Parent has `absolute contents` → child positions already absolute → keep AS-IS
      - Parent has `absolute` (no contents) → child positions relative → ADD parent + child
    - **Real example (FINANCING SUMMARY page):**
      - Frame 168 (11:1506): `top-[132px]`
      - Footnote (11:1576): `top-[772px]` inside Frame 168
      - Absolute position: 132 + 772 = **904px** (NOT 772px or 1006px!)
      - Footer line: `top-[1011px]`
      - Gap: 1011 - 904 - 29 = **78px** clearance ✓

**Position Calculation Quick Check:**
| Parent Class | Child Action |
|-------------|--------------|
| `absolute contents` | Keep position AS-IS |
| `absolute` (no contents) | Add parent + child |

---

## 🎯 Success Criteria

A successful conversion has:
- ✅ Zero loss of design information
- ✅ All elements positioned correctly
- ✅ Fonts load and render correctly
- ✅ Colors match exactly
- ✅ Layout doesn't compress on any screen size
- ✅ Code is clean and maintainable
- ✅ Matches Figma screenshot pixel-perfectly

---

## 📝 Quick Reference

**Workflow Summary:**
1. Extract Figma data (metadata + design_context + screenshot)
2. Flatten all `absolute contents` structures (remove wrapper, keep children)
3. Handle positions correctly:
   - Parent has "contents" → Keep child position AS-IS
   - Parent has no "contents" → Calculate parent + child
4. Convert font names
5. Replace simple images with CSS
6. Inline SVG assets
7. Generate React component
8. Verify against screenshot

**Remember:**
- 🔥 `absolute contents` parent = children positions already absolute!
- 🔥 DO NOT add parent+child when parent has "contents"
- 🔥 Preserve ALL className
- 🔥 Add page-container CSS
- 🔥 Compare with screenshot
- 🔥 Table-like layouts: keep Figma's absolute positioning, don't convert to HTML `<table>`!
- 🔥 Use Google Fonts CDN directly, NOT `next/font/google`!
- 🔥 Remove fixed heights from multi-line text blocks!
- 🔥 Figma font weights may need adjustment - compare visually!

**Reference Positions (from verified HTML):**
```
Header text: top-[41px]
Header line: top-[100px]
Footer line: top-[980px]
Page number: top-[1004px]
```
