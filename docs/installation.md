# Installation Guide

## Prerequisites

- Claude Code CLI installed
- Git

## Installing Plugins

### Method 1: Via Plugin Marketplace (Recommended)

```bash
# Add the plugin as a marketplace source
/plugin marketplace add https://github.com/majiayu000/claude-arsenal/plugins/<plugin-name>

# Install the plugin
/plugin install <plugin-name>
```

### Method 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/majiayu000/claude-arsenal.git

# Add local plugin as marketplace
/plugin marketplace add /path/to/claude-arsenal/plugins/<plugin-name>

# Install
/plugin install <plugin-name>
```

## Installing Individual Components

### Skills

```bash
# Create skills directory if not exists
mkdir -p ~/.claude/skills

# Download a skill
curl -o ~/.claude/skills/<skill-name>.SKILL.md \
  https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/skills/<skill-name>.SKILL.md
```

### Commands

```bash
# Create commands directory if not exists
mkdir -p ~/.claude/commands

# Download a command
curl -o ~/.claude/commands/<command-name>.md \
  https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/commands/<command-name>.md
```

### Agents

```bash
# Create agents directory if not exists
mkdir -p ~/.claude/agents

# Download an agent
curl -o ~/.claude/agents/<agent-name>.md \
  https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/agents/<agent-name>.md
```

### CLAUDE.md Templates

```bash
# Download to your project root
curl -o ./CLAUDE.md \
  https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/claude-md/<template-name>.md
```

## Verification

After installation, verify components are loaded:

```bash
# Check installed plugins
/plugin list

# Check available commands
/help

# Ask Claude about available skills
"What skills do you have available?"
```

## Uninstallation

```bash
# Uninstall a plugin
/plugin uninstall <plugin-name>

# Remove a skill
rm ~/.claude/skills/<skill-name>.SKILL.md

# Remove a command
rm ~/.claude/commands/<command-name>.md
```
