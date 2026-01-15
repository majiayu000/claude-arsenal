# Claude-Codex Skill

A Claude Code skill that **enforces Codex-based code review** - Claude must use Codex for all code reviews, then apply fixes based on Codex's feedback.

## Core Workflow

```
Code Review Request
       ↓
   ┌───────────────────┐
   │  Codex Reviews    │  ← Claude calls Codex CLI
   │  (read-only)      │
   └───────────────────┘
       ↓
   ┌───────────────────┐
   │  Codex Feedback   │  ← Issues with file:line:severity
   └───────────────────┘
       ↓
   ┌───────────────────┐
   │  Claude Applies   │  ← Claude fixes code using Edit tool
   │  Fixes            │
   └───────────────────┘
       ↓
   ┌───────────────────┐
   │  (Optional)       │  ← Codex re-verifies
   │  Re-verify        │
   └───────────────────┘
```

## Features

- **Mandatory Code Review**: All code reviews MUST go through Codex first
- **Guided Fixes**: Claude applies fixes based on Codex's specific feedback
- **Structured Output**: Codex provides file paths, line numbers, and severity levels
- **Re-verification**: Optional second pass to confirm fixes

## Prerequisites

### Install Codex CLI

```bash
# Via npm
npm install -g @openai/codex

# Via Homebrew (macOS)
brew install --cask codex
```

### Authenticate

```bash
codex login
```

## Installation

### Option 1: User-level (all projects)

```bash
cp -r claude-codex-skill ~/.claude/skills/codex-agent
```

### Option 2: Project-level

```bash
mkdir -p .claude/skills
cp -r claude-codex-skill .claude/skills/codex-agent
```

## Usage

When you ask Claude to review code, it will:

1. **Call Codex** to perform the review
2. **Parse feedback** from Codex (file, line, severity, issue, fix)
3. **Apply fixes** using Edit tool
4. **Optionally re-verify** with Codex

### Example Prompts

```
Review my authentication code and fix any issues
```

```
Do a security review of src/api/ and apply the fixes
```

```
Review the recent changes and fix problems Codex finds
```

## Workflow Details

### Step 1: Codex Review

Claude executes:
```bash
codex exec -C /project -s read-only -o /tmp/codex-review.md \
  "Review src/auth/. Check for security, performance, code quality.
   Provide file paths, line numbers, and specific fixes."
```

### Step 2: Parse Feedback

Codex outputs structured feedback:
```
- File: src/auth/login.ts
- Line: 45
- Severity: high
- Issue: SQL injection vulnerability
- Fix: Use parameterized query instead of string concatenation
```

### Step 3: Claude Applies Fixes

Claude reads the file, applies the fix with Edit tool:
```
old_string: `SELECT * FROM users WHERE id = '${userId}'`
new_string: `SELECT * FROM users WHERE id = $1`, [userId]
```

### Step 4: Re-verify (Optional)

```bash
codex exec -C /project -s read-only \
  "Verify fixes in src/auth/login.ts. Confirm SQL injection is resolved."
```

## File Structure

```
claude-codex-skill/
├── SKILL.md           # Main skill with mandatory workflow
├── sandbox-modes.md   # Sandbox security documentation
├── examples.md        # Usage examples
├── advanced.md        # Advanced configuration
├── scripts/
│   ├── codex-wrapper.sh   # Helper wrapper script
│   └── check-codex.sh     # Installation checker
└── README.md          # This file
```

## Configuration

### Recommended Permissions

Add to `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(codex:*)"
    ]
  }
}
```

## Sandbox Modes

| Mode | Description |
|------|-------------|
| `read-only` | No file writes (used for reviews) |
| `workspace-write` | Write to project directory |
| `danger-full-access` | Unrestricted (use with caution) |

## Troubleshooting

### Codex not found

```bash
npm install -g @openai/codex
```

### Authentication issues

```bash
codex logout
codex login
```

## License

MIT

## References

- [OpenAI Codex CLI](https://github.com/openai/codex)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Codex Documentation](https://developers.openai.com/codex)
