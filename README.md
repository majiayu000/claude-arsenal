# Claude Arsenal

A comprehensive collection of Claude Code plugins, skills, agents, commands, and templates.

## Structure

```
claude-arsenal/
├── plugins/          # Complete plugin packages (installable via /plugin)
├── skills/           # Standalone SKILL.md files
├── commands/         # Slash command templates
├── agents/           # Agent definitions
├── workflows/        # Workflow specifications
├── claude-md/        # CLAUDE.md project templates
├── hooks/            # Hook configurations
└── docs/             # Documentation
```

## Installation

### Install a Plugin

```bash
# Add this repository as a marketplace
/plugin marketplace add https://github.com/majiayu000/claude-arsenal/plugins/<plugin-name>

# Install the plugin
/plugin install <plugin-name>
```

### Install Individual Skills

```bash
# Copy a skill to your local skills directory
# Note: Skills must be in a subdirectory with SKILL.md inside
mkdir -p ~/.claude/skills/<skill-name>
curl -o ~/.claude/skills/<skill-name>/SKILL.md \
  https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/skills/<skill-name>.SKILL.md
```

### Install Agents

```bash
# Copy an agent to your local agents directory
mkdir -p ~/.claude/agents
curl -o ~/.claude/agents/<agent-name>.md \
  https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/agents/<agent-name>.md
```

### Use CLAUDE.md Templates

```bash
# Download a template for your project
curl -o ./CLAUDE.md \
  https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/claude-md/<template-name>.md
```

## Available Components

### Plugins

| Plugin | Description |
|--------|-------------|
| [`rust-dev`](./plugins/rust-dev) | Rust development toolkit with best practices |

### Skills

| Skill | Description | Source |
|-------|-------------|--------|
| [`test-driven-development`](./skills/test-driven-development.SKILL.md) | TDD with RED-GREEN-REFACTOR cycle | [obra/superpowers](https://github.com/obra/superpowers) |
| [`systematic-debugging`](./skills/systematic-debugging.SKILL.md) | 4-phase debugging framework | [obra/superpowers](https://github.com/obra/superpowers) |
| [`brainstorming`](./skills/brainstorming.SKILL.md) | Socratic design refinement | [obra/superpowers](https://github.com/obra/superpowers) |
| [`git-commit-smart`](./skills/git-commit-smart.SKILL.md) | Conventional commit message generation | [plugins-plus](https://github.com/jeremylongshore/claude-code-plugins-plus) |
| [`playwright-automation`](./skills/playwright-automation.SKILL.md) | Browser automation and testing | [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) |
| [`project-health-auditor`](./skills/project-health-auditor.SKILL.md) | Codebase health analysis | [plugins-plus](https://github.com/jeremylongshore/claude-code-plugins-plus) |
| [`elegant-architecture`](./skills/elegant-architecture.SKILL.md) | Clean architecture with 200-line file limit | Custom |
| [`comprehensive-testing`](./skills/comprehensive-testing.SKILL.md) | Complete testing strategy: TDD, test pyramid, mocking, CI | [Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) |

### Agents

| Agent | Description | Source |
|-------|-------------|--------|
| [`tech-lead-orchestrator`](./agents/tech-lead-orchestrator.md) | Coordinates multi-step tasks, delegates to specialists | [vijaythecoder](https://github.com/vijaythecoder/awesome-claude-agents) |
| [`code-archaeologist`](./agents/code-archaeologist.md) | Explores and documents legacy/unfamiliar codebases | [vijaythecoder](https://github.com/vijaythecoder/awesome-claude-agents) |
| [`backend-typescript-architect`](./agents/backend-typescript-architect.md) | Senior TS architect for Bun/Node.js, API design | [Community](https://github.com/hesreallyhim/a-list-of-claude-code-agents) |
| [`senior-code-reviewer`](./agents/senior-code-reviewer.md) | 15+ years exp, security, performance, architecture | [Community](https://github.com/hesreallyhim/a-list-of-claude-code-agents) |
| [`kubernetes-specialist`](./agents/kubernetes-specialist.md) | K8s manifests, Helm, GitOps, security policies | [VoltAgent](https://github.com/VoltAgent/awesome-claude-code-subagents) |
| [`security-auditor`](./agents/security-auditor.md) | OWASP Top 10, SAST, vulnerability assessment | [VoltAgent](https://github.com/VoltAgent/awesome-claude-code-subagents) |
| [`opensource-contributor`](./agents/opensource-contributor.md) | Systematic open source contribution workflow | Custom |

### Commands

| Command | Description |
|---------|-------------|
| *Coming soon* | - |

### CLAUDE.md Templates

| Template | Description |
|----------|-------------|
| [`rust-project`](./claude-md/rust-project.md) | Rust/Cargo project configuration |

## Quick Start

### Install All Skills at Once

```bash
# Download all skills (each skill needs its own subdirectory)
for skill in test-driven-development systematic-debugging brainstorming git-commit-smart playwright-automation project-health-auditor elegant-architecture comprehensive-testing; do
  mkdir -p ~/.claude/skills/${skill}
  curl -o ~/.claude/skills/${skill}/SKILL.md \
    https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/skills/${skill}.SKILL.md
done
```

### Install All Agents at Once

```bash
mkdir -p ~/.claude/agents

# Download all agents
for agent in tech-lead-orchestrator code-archaeologist backend-typescript-architect senior-code-reviewer kubernetes-specialist security-auditor opensource-contributor; do
  curl -o ~/.claude/agents/${agent}.md \
    https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/agents/${agent}.md
done
```

### Install Rust Plugin

```bash
/plugin marketplace add https://github.com/majiayu000/claude-arsenal/plugins/rust-dev
/plugin install rust-dev
```

## Documentation

- [Installation Guide](./docs/installation.md)
- [Creating Plugins](./docs/creating-plugins.md)
- [Skills Analysis](./docs/skills-agents-analysis.md)
- [Agents Analysis](./docs/agents-analysis.md)
- [Issue to PR Workflow](./workflows/issue-to-pr-workflow.md) - Standardized open source contribution workflow

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
