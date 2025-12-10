# Issue to PR Workflow Specification

> A standardized workflow for contributing to open source projects, from issue discovery to PR creation.

## Overview

This specification defines a 5-phase workflow for systematic open source contributions:

```
Issue Discovery → Analysis → Implementation → PR Creation → Follow-up
```

---

## Phase 1: Project Research

Before contributing, understand the project:

### 1.1 Read Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Project purpose, features, tech stack |
| `CONTRIBUTING.md` | Contribution guidelines |
| `CODE_OF_CONDUCT.md` | Community standards |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR format requirements |

### 1.2 Understand Development Setup

```bash
# Typical setup steps to look for:
# 1. Clone repository
# 2. Install dependencies
# 3. Run tests
# 4. Run linter
```

### 1.3 Analyze Recent PRs

Learn from merged PRs:
- Commit message style
- PR description format
- Review turnaround time
- Active maintainers

---

## Phase 2: Issue Selection

### 2.1 Filter Criteria

**Required (Must Have):**
- [ ] Status: `open`
- [ ] No linked PR (check "Development" section)
- [ ] No blocking labels: `wontfix`, `stale`, `duplicate`, `invalid`
- [ ] Not assigned (or assignment stale > 30 days)

**Preferred:**
- [ ] Has `good first issue` or `help wanted` label
- [ ] Has maintainer positive response
- [ ] Recent activity (< 6 months)
- [ ] Clear problem description
- [ ] Has reproduction steps (for bugs)

### 2.2 Difficulty Classification

| Level | Time | Characteristics | Examples |
|-------|------|-----------------|----------|
| **Easy** | 1-2h | Single file, clear fix | Type hints, typos, docs, simple params |
| **Medium** | 2-4h | 2-5 files, some investigation | Bug fixes, tests, small features |
| **Hard** | 4h+ | Architecture impact, multi-file | Performance, refactoring, new features |

### 2.3 Selection Priority

1. Easy issues with `good first issue` label
2. Easy issues with `help wanted` label
3. Easy issues with recent maintainer activity
4. Medium issues with clear reproduction steps

---

## Phase 3: Implementation

### 3.1 Branch Creation

```bash
# Sync with upstream
git checkout main
git pull origin main

# Create feature branch
git checkout -b <type>/<issue-number>-<short-description>
```

**Branch naming convention:**

| Type | Use Case | Example |
|------|----------|---------|
| `fix/` | Bug fixes | `fix/123-null-pointer` |
| `feat/` | New features | `feat/456-add-retry` |
| `docs/` | Documentation | `docs/789-update-readme` |
| `refactor/` | Code refactoring | `refactor/101-extract-util` |
| `test/` | Adding tests | `test/102-add-unit-tests` |

### 3.2 Issue Understanding

Before coding:
1. Read issue description completely
2. Read ALL comments for context
3. Check linked issues/PRs
4. Identify affected files
5. Understand expected vs actual behavior

### 3.3 Implementation Guidelines

**DO:**
- Make minimal changes to fix the issue
- Follow existing code patterns
- Match project code style
- Add tests if required by project

**DO NOT:**
- Refactor unrelated code
- Add unrelated features
- Change formatting of untouched code
- Add comments to unchanged code
- Fix unrelated bugs in same PR

### 3.4 Verification

```bash
# Run tests
pytest tests/ -v          # Python
npm test                  # Node.js
go test ./...             # Go
cargo test                # Rust

# Run linter
ruff check .              # Python
npm run lint              # Node.js
golangci-lint run         # Go
cargo clippy              # Rust
```

---

## Phase 4: PR Creation

### 4.1 Commit Message Format

```
<type>: <description> (#<issue-number>)

[Optional body explaining WHY, not WHAT]
```

**Types:**
| Type | Description |
|------|-------------|
| `fix` | Bug fix |
| `feat` | New feature |
| `docs` | Documentation only |
| `refactor` | Code refactoring |
| `test` | Adding tests |
| `chore` | Maintenance tasks |
| `perf` | Performance improvement |

**Examples:**
```
fix: handle null pointer in config parser (#123)

feat: add retry mechanism for API calls (#456)

docs: update installation instructions (#789)
```

**AI Signature (Optional):**

Some contributors choose to disclose AI assistance, others prefer not to. This is entirely optional:
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 4.2 Push Changes

```bash
git add <changed-files>
git commit -m "<commit-message>"
git push origin <branch-name>
```

### 4.3 PR Template

```markdown
## Summary
Fixes #<issue-number>

<One paragraph explaining what this PR does and why>

## Changes
- <Change 1>
- <Change 2>
- <Change 3>

## Test Plan
- [ ] Existing tests pass
- [ ] Manual testing done
- [ ] New tests added (if applicable)

## Screenshots (if UI changes)
<Before/After screenshots>
```

**Note:** AI signature in PR body is optional. Omit if you prefer not to disclose AI assistance.

### 4.4 PR Checklist

Before submitting:
- [ ] PR title is descriptive
- [ ] Links to issue with `Fixes #xxx`
- [ ] Changes are explained
- [ ] Test plan is clear
- [ ] CI passes
- [ ] No merge conflicts

---

## Phase 5: Follow-up

### 5.1 CI Monitoring

After PR creation:
1. Wait for CI to complete
2. If CI fails:
   - Read failure logs
   - Fix issues locally
   - Push additional commits
   - Verify CI passes

### 5.2 Review Response

When maintainers review:
- Respond promptly to comments
- Make requested changes
- Explain if you disagree (respectfully)
- Push fixes as new commits (don't force push)

### 5.3 Merge

After approval:
- Maintainer will merge (don't ask repeatedly)
- Delete your branch after merge
- Celebrate!

---

## Skip Criteria

Skip an issue if:
- [ ] Requires architectural decisions by maintainer
- [ ] Has conflicting opinions in comments
- [ ] Would take > 4 hours
- [ ] Requires external dependency changes
- [ ] Is a feature request disguised as bug
- [ ] Has unclear or incomplete requirements
- [ ] Already has a PR in progress

**Document skipped issues with reason.**

---

## Quality Checklist

### Code Quality
- [ ] Follows existing code style
- [ ] No unnecessary changes
- [ ] No debug code left
- [ ] No commented-out code
- [ ] Meaningful variable names

### Git Hygiene
- [ ] Clear commit message
- [ ] Single logical change per commit
- [ ] No merge commits (use rebase)
- [ ] Branch name follows convention

### PR Quality
- [ ] Title is descriptive
- [ ] Links to issue
- [ ] Changes are explained
- [ ] Test plan is clear

---

## Metrics

Track your contribution effectiveness:

| Metric | Target | Description |
|--------|--------|-------------|
| Acceptance Rate | > 80% | PRs merged / PRs submitted |
| Time to Merge | < 2 weeks | From PR creation to merge |
| Review Iterations | < 3 | Rounds of review needed |
| CI Pass Rate | > 95% | First-time CI pass rate |

---

## Common Mistakes to Avoid

| Mistake | Why It's Bad | Solution |
|---------|--------------|----------|
| Too large PR | Hard to review, likely rejected | Split into smaller PRs |
| Unrelated changes | Confuses reviewers | One issue per PR |
| No tests | May break later | Add tests for changes |
| Force pushing | Loses review context | Use regular push |
| Arguing with reviewers | Burns bridges | Be respectful, explain calmly |
| Pinging maintainers | Annoying | Be patient |

---

## Templates

### Quick Bug Fix PR

```markdown
## Summary
Fixes #123

Fixed null pointer exception when config file is missing.

## Changes
- Added null check in `config.py:45`
- Return default config when file not found

## Test Plan
- [x] Existing tests pass
- [x] Tested manually with missing config file
```

### Documentation PR

```markdown
## Summary
Fixes #456

Updated installation docs to include Python 3.12 support.

## Changes
- Added Python 3.12 to supported versions
- Updated pip install command
- Fixed broken link to API docs

## Test Plan
- [x] Links verified working
- [x] Instructions tested on fresh environment
```

### Feature PR

```markdown
## Summary
Fixes #789

Added retry mechanism for failed API calls with exponential backoff.

## Changes
- New `RetryPolicy` class in `utils/retry.py`
- Applied retry to `ApiClient.fetch()` method
- Added configuration options: `max_retries`, `backoff_factor`

## Test Plan
- [x] Unit tests for RetryPolicy
- [x] Integration tests for ApiClient
- [x] Manual testing with unstable network

## Breaking Changes
None
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-10 | Initial specification |

---

## License

MIT License - Feel free to adapt for your projects.
