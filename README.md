# Claude Arsenal

A comprehensive collection of Claude Code skills, agents, commands, and templates for modern software development.

## Structure

```
claude-arsenal/
├── skills/           # Standalone skills (SKILL.md files)
├── agents/           # Agent definitions
├── commands/         # Slash command templates
├── workflows/        # Workflow specifications
├── claude-md/        # CLAUDE.md project templates
├── hooks/            # Hook configurations
└── docs/             # Documentation
```

## Installation

### Install Skills

Skills can be installed globally (all projects) or locally (single project).

#### Option 1: Global Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/majiayu000/claude-arsenal.git

# Create symlinks for skills you want (new format: directory-based)
ln -s $(pwd)/claude-arsenal/skills/typescript-project ~/.claude/skills/typescript-project
ln -s $(pwd)/claude-arsenal/skills/devops-excellence ~/.claude/skills/devops-excellence

# For old format skills (single file), create directory first
mkdir -p ~/.claude/skills/test-driven-development
ln -s $(pwd)/claude-arsenal/skills/test-driven-development.SKILL.md ~/.claude/skills/test-driven-development/SKILL.md
```

#### Option 2: Copy Files Directly

```bash
# New format skills (directory-based)
cp -r skills/typescript-project ~/.claude/skills/

# Old format skills (single file) - need to create directory
mkdir -p ~/.claude/skills/test-driven-development
cp skills/test-driven-development.SKILL.md ~/.claude/skills/test-driven-development/SKILL.md
```

#### Option 3: Project-Local Installation

```bash
# In your project root
mkdir -p .claude/skills
cp -r /path/to/claude-arsenal/skills/typescript-project .claude/skills/
```

### Verify Installation

In Claude Code, type `/skills` to see installed skills.

### Install Agents

```bash
mkdir -p ~/.claude/agents

# Download agents
for agent in tech-lead-orchestrator code-archaeologist backend-typescript-architect senior-code-reviewer kubernetes-specialist security-auditor opensource-contributor; do
  curl -o ~/.claude/agents/${agent}.md \
    https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/agents/${agent}.md
done
```

## Available Skills

### Development Architecture (Language-Specific)

| Skill | Description | Key Features |
|-------|-------------|--------------|
| [`typescript-project`](./skills/typescript-project/) | Modern TypeScript project architecture | ESM, Zod, Biome, LiteLLM, No Backwards Compatibility |
| [`python-project`](./skills/python-project/) | Python project with modern tooling | uv, Pydantic, Ruff, pyproject.toml |
| [`rust-project`](./skills/rust-project/) | Rust application architecture | Cargo, error handling, async patterns |
| [`golang-web`](./skills/golang-web/) | Go web application patterns | Chi/Echo, sqlc, structured logging |
| [`zig-project`](./skills/zig-project/) | Zig project structure | Build system, memory management |

### Mobile & Cross-Platform

| Skill | Description | Key Features |
|-------|-------------|--------------|
| [`harmonyos-app`](./skills/harmonyos-app/) | HarmonyOS application development | ArkTS, ArkUI, Stage Model, Distributed Capabilities |
| [`app-ui-design`](./skills/app-ui-design/) | Mobile app UI design for iOS/Android | Material Design 3, HIG, Accessibility, Color Theory |

### Product Lifecycle

| Skill | Description | Hard Rules |
|-------|-------------|------------|
| [`prd-master`](./skills/prd-master/) | PRD writing, user stories, prioritization | No Vague Metrics, INVEST-Compliant Stories |
| [`product-discovery`](./skills/product-discovery/) | Market research, user interviews, JTBD | Evidence-Based Decisions, No Solution-First |
| [`technical-spec`](./skills/technical-spec/) | Design docs, ADR, C4 model | Alternatives Required, Diagrams Required |
| [`product-analytics`](./skills/product-analytics/) | Event tracking, AARRR, A/B testing | No PII in Events, Object_Action Naming |
| [`devops-excellence`](./skills/devops-excellence/) | CI/CD, Docker, Kubernetes, GitOps | No Static Credentials, No Root Containers |
| [`observability-sre`](./skills/observability-sre/) | Monitoring, logging, tracing, SLO/SLI | Symptom-Based Alerts, Low Cardinality Labels |

### API & Backend

| Skill | Description |
|-------|-------------|
| [`api-design`](./skills/api-design/) | RESTful API design patterns, OpenAPI |
| [`auth-security`](./skills/auth-security/) | Authentication, authorization, security best practices |
| [`database-patterns`](./skills/database-patterns/) | Database design, migrations, query optimization |
| [`mcp-server-development`](./skills/mcp-server-development/) | Model Context Protocol server development |

### Development Practices

| Skill | Description | Source |
|-------|-------------|--------|
| [`test-driven-development`](./skills/test-driven-development.SKILL.md) | TDD with RED-GREEN-REFACTOR cycle | [obra/superpowers](https://github.com/obra/superpowers) |
| [`systematic-debugging`](./skills/systematic-debugging.SKILL.md) | 4-phase debugging framework | [obra/superpowers](https://github.com/obra/superpowers) |
| [`brainstorming`](./skills/brainstorming.SKILL.md) | Socratic design refinement | [obra/superpowers](https://github.com/obra/superpowers) |
| [`elegant-architecture`](./skills/elegant-architecture.SKILL.md) | Clean architecture with 200-line file limit | Custom |
| [`comprehensive-testing`](./skills/comprehensive-testing.SKILL.md) | Complete testing strategy: TDD, test pyramid, mocking | [Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) |

### Tooling & Workflow

| Skill | Description | Source |
|-------|-------------|--------|
| [`git-commit-smart`](./skills/git-commit-smart.SKILL.md) | Conventional commit message generation | [plugins-plus](https://github.com/jeremylongshore/claude-code-plugins-plus) |
| [`playwright-automation`](./skills/playwright-automation.SKILL.md) | Browser automation and testing | [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) |
| [`project-health-auditor`](./skills/project-health-auditor.SKILL.md) | Codebase health analysis | [plugins-plus](https://github.com/jeremylongshore/claude-code-plugins-plus) |
| [`structured-logging`](./skills/structured-logging.SKILL.md) | JSON logging with OpenTelemetry correlation | Custom |
| [`product-ux-expert`](./skills/product-ux-expert/) | UX evaluation and design guidance | Custom |

## Available Agents

| Agent | Description | Source |
|-------|-------------|--------|
| [`tech-lead-orchestrator`](./agents/tech-lead-orchestrator.md) | Coordinates multi-step tasks, delegates to specialists | [vijaythecoder](https://github.com/vijaythecoder/awesome-claude-agents) |
| [`code-archaeologist`](./agents/code-archaeologist.md) | Explores and documents legacy/unfamiliar codebases | [vijaythecoder](https://github.com/vijaythecoder/awesome-claude-agents) |
| [`backend-typescript-architect`](./agents/backend-typescript-architect.md) | Senior TS architect for Bun/Node.js, API design | [Community](https://github.com/hesreallyhim/a-list-of-claude-code-agents) |
| [`senior-code-reviewer`](./agents/senior-code-reviewer.md) | 15+ years exp, security, performance, architecture | [Community](https://github.com/hesreallyhim/a-list-of-claude-code-agents) |
| [`kubernetes-specialist`](./agents/kubernetes-specialist.md) | K8s manifests, Helm, GitOps, security policies | [VoltAgent](https://github.com/VoltAgent/awesome-claude-code-subagents) |
| [`security-auditor`](./agents/security-auditor.md) | OWASP Top 10, SAST, vulnerability assessment | [VoltAgent](https://github.com/VoltAgent/awesome-claude-code-subagents) |
| [`opensource-contributor`](./agents/opensource-contributor.md) | Systematic open source contribution workflow | Custom |

## Quick Start

### Install All Product Lifecycle Skills

```bash
# Clone repository
git clone https://github.com/majiayu000/claude-arsenal.git
cd claude-arsenal

# Install product lifecycle skills
for skill in prd-master product-discovery technical-spec product-analytics devops-excellence observability-sre; do
  ln -sf $(pwd)/skills/${skill} ~/.claude/skills/${skill}
done
```

### Install All Development Skills

```bash
# New format skills (directory-based)
for skill in typescript-project python-project rust-project golang-web api-design auth-security database-patterns; do
  ln -sf $(pwd)/skills/${skill} ~/.claude/skills/${skill}
done

# Old format skills (file-based)
for skill in test-driven-development systematic-debugging brainstorming elegant-architecture comprehensive-testing git-commit-smart playwright-automation project-health-auditor; do
  mkdir -p ~/.claude/skills/${skill}
  ln -sf $(pwd)/skills/${skill}.SKILL.md ~/.claude/skills/${skill}/SKILL.md
done
```

## Skill Design Philosophy

All skills in this arsenal follow these principles:

1. **Hard Rules** - Each skill has mandatory constraints (❌ FORBIDDEN / ✅ REQUIRED)
2. **Testable** - Skills can be validated using the [skill testing guide](./docs/skill-testing-guide.md)
3. **Practical Examples** - Real code examples, not just theory
4. **Checklists** - Actionable verification checklists

## Documentation

- [Skill Testing Guide](./docs/skill-testing-guide.md) - How to validate skills are working
- [Skill Optimization Report](./docs/skill-optimization-report.md) - Analysis of skill effectiveness
- [Product Lifecycle Skills (EN)](./docs/product-lifecycle-skills-en.md) - Product lifecycle coverage
- [Product Lifecycle Skills (中文)](./docs/product-lifecycle-skills-zh.md) - 产品生命周期覆盖
- [Installation Guide](./docs/installation.md)
- [Creating Plugins](./docs/creating-plugins.md)

## Credits

This arsenal includes skills and agents inspired by:

- [anthropics/skills](https://github.com/anthropics/skills) - Official Anthropic skills
- [obra/superpowers](https://github.com/obra/superpowers) - Battle-tested development skills
- [claude-code-plugins-plus](https://github.com/jeremylongshore/claude-code-plugins-plus) - Comprehensive plugin hub
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) - 115+ production-ready agents
- [vijaythecoder/awesome-claude-agents](https://github.com/vijaythecoder/awesome-claude-agents) - Orchestrated agent team
- [hesreallyhim/a-list-of-claude-code-agents](https://github.com/hesreallyhim/a-list-of-claude-code-agents) - Community-submitted agents
- [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) - Browser automation

## Contributing

Feel free to submit issues and pull requests.

## License

MIT License
