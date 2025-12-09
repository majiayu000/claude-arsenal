# Claude Arsenal

A comprehensive collection of Claude Code plugins, skills, agents, commands, and templates.

## Structure

```
claude-arsenal/
├── plugins/          # Complete plugin packages (installable via /plugin)
├── skills/           # Standalone SKILL.md files
├── commands/         # Slash command templates
├── agents/           # Agent definitions
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
mkdir -p ~/.claude/skills
curl -o ~/.claude/skills/<skill-name>.SKILL.md \
  https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/skills/<skill-name>.SKILL.md
```

### Install Commands

```bash
# Copy a command to your local commands directory
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/<command-name>.md \
  https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/commands/<command-name>.md
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

### Commands

| Command | Description |
|---------|-------------|
| *Coming soon* | - |

### Agents

| Agent | Description |
|-------|-------------|
| *Coming soon* | - |

### CLAUDE.md Templates

| Template | Description |
|----------|-------------|
| [`rust-project`](./claude-md/rust-project.md) | Rust/Cargo project configuration |

## Quick Start

### Install All Skills at Once

```bash
mkdir -p ~/.claude/skills

# Download all skills
for skill in test-driven-development systematic-debugging brainstorming git-commit-smart playwright-automation project-health-auditor; do
  curl -o ~/.claude/skills/${skill}.SKILL.md \
    https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/skills/${skill}.SKILL.md
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
- [Skills & Agents Analysis](./docs/skills-agents-analysis.md)

## Credits

This arsenal includes skills inspired by:

- [anthropics/skills](https://github.com/anthropics/skills) - Official Anthropic skills
- [obra/superpowers](https://github.com/obra/superpowers) - Battle-tested development skills
- [claude-code-plugins-plus](https://github.com/jeremylongshore/claude-code-plugins-plus) - Comprehensive plugin hub
- [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) - Browser automation
- [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) - Curated skills collection

## Contributing

Feel free to submit issues and pull requests.

## License

MIT License
