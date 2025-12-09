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
| `rust-dev` | Rust development toolkit with best practices |
| `python-dev` | Python development toolkit |
| `typescript-dev` | TypeScript/JavaScript development toolkit |
| `devops` | DevOps and CI/CD utilities |

### Skills

| Skill | Description |
|-------|-------------|
| `code-review` | Comprehensive code review assistant |
| `security-audit` | Security vulnerability detection |
| `performance` | Performance optimization guidance |
| `refactoring` | Code refactoring assistance |

### Commands

| Command | Description |
|---------|-------------|
| `/review-pr` | Review a pull request |
| `/generate-tests` | Generate unit tests |
| `/explain` | Explain code in detail |

### Agents

| Agent | Description |
|-------|-------------|
| `architect` | Software architecture design |
| `debugger` | Debugging specialist |
| `reviewer` | Code review expert |

### CLAUDE.md Templates

| Template | Description |
|----------|-------------|
| `rust-project` | Rust/Cargo project configuration |
| `python-project` | Python project configuration |
| `typescript-project` | TypeScript project configuration |
| `monorepo` | Monorepo configuration |

## Contributing

Feel free to submit issues and pull requests.

## License

MIT License
