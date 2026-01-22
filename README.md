<div align="center">
  <h1>Claude Arsenal</h1>
  <p><strong>39 Production-Ready Skills | 7 Specialized Agents | One Command Install</strong></p>

  <p>The most comprehensive skill library for Claude Code</p>

  <p>
    <a href="https://github.com/majiayu000/claude-arsenal/stargazers"><img src="https://img.shields.io/github/stars/majiayu000/claude-arsenal?style=flat-square&logo=github" alt="Stars"></a>
    <a href="https://github.com/majiayu000/claude-arsenal/blob/main/LICENSE"><img src="https://img.shields.io/github/license/majiayu000/claude-arsenal?style=flat-square" alt="License"></a>
    <img src="https://img.shields.io/badge/skills-39-blue?style=flat-square" alt="Skills">
    <img src="https://img.shields.io/badge/agents-7-green?style=flat-square" alt="Agents">
  </p>

  <p>
    <a href="#quick-start">Quick Start</a> •
    <a href="#skills">Skills</a> •
    <a href="#agents">Agents</a> •
    <a href="#contributing">Contributing</a> •
    <a href="./README_CN.md">中文</a>
  </p>
</div>

---

## Quick Start

### One-Line Install (All Skills)

```bash
curl -fsSL https://raw.githubusercontent.com/majiayu000/claude-arsenal/main/install.sh | bash
```

### Manual Install (Selective)

```bash
# Clone the repository
git clone https://github.com/majiayu000/claude-arsenal.git
cd claude-arsenal

# Install specific skills
./install.sh --skills typescript-project,python-project,devops-excellence

# Or install everything
./install.sh --all
```

### Verify Installation

In Claude Code, type `/` to see your installed skills.

---

## Skills

### Development Architecture

Build production-ready projects with language-specific best practices.

| Skill | Language | Key Features |
|-------|----------|--------------|
| [`typescript-project`](./skills/typescript-project/) | TypeScript | ESM, Zod, Biome, Clean Architecture |
| [`python-project`](./skills/python-project/) | Python | uv, Pydantic, Ruff, FastAPI |
| [`rust-project`](./skills/rust-project/) | Rust | Cargo workspace, error handling, async |
| [`golang-web`](./skills/golang-web/) | Go | Chi/Echo, sqlc, structured logging |
| [`zig-project`](./skills/zig-project/) | Zig | Build system, memory management |

### Product Lifecycle

End-to-end product development from discovery to deployment.

| Skill | Phase | What You Get |
|-------|-------|--------------|
| [`product-discovery`](./skills/product-discovery/) | Discovery | JTBD, user interviews, market research |
| [`prd-master`](./skills/prd-master/) | Definition | PRD writing, user stories, RICE prioritization |
| [`technical-spec`](./skills/technical-spec/) | Design | Design docs, ADR, C4 diagrams |
| [`product-analytics`](./skills/product-analytics/) | Growth | Event tracking, A/B testing, AARRR |
| [`devops-excellence`](./skills/devops-excellence/) | Deployment | CI/CD, Docker, Kubernetes, GitOps |
| [`observability-sre`](./skills/observability-sre/) | Operations | Monitoring, logging, tracing, SLO/SLI |

### API & Backend

| Skill | Description |
|-------|-------------|
| [`api-design`](./skills/api-design/) | REST/GraphQL/gRPC patterns, OpenAPI 3.2 |
| [`auth-security`](./skills/auth-security/) | OAuth 2.1, JWT, security best practices |
| [`database-patterns`](./skills/database-patterns/) | PostgreSQL, Redis, migrations, optimization |

### Development Practices

| Skill | Description | Origin |
|-------|-------------|--------|
| [`test-driven-development`](./skills/test-driven-development.SKILL.md) | RED-GREEN-REFACTOR cycle | [obra/superpowers](https://github.com/obra/superpowers) |
| [`systematic-debugging`](./skills/systematic-debugging.SKILL.md) | 4-phase debugging framework | [obra/superpowers](https://github.com/obra/superpowers) |
| [`elegant-architecture`](./skills/elegant-architecture.SKILL.md) | Clean architecture, 200-line file limit | Custom |
| [`comprehensive-testing`](./skills/comprehensive-testing.SKILL.md) | Test pyramid, TDD, mocking strategies | [Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) |
| [`brainstorming`](./skills/brainstorming.SKILL.md) | Socratic design refinement | [obra/superpowers](https://github.com/obra/superpowers) |

### UI/UX & Design

| Skill | Description |
|-------|-------------|
| [`app-ui-design`](./skills/app-ui-design/) | iOS/Android UI design, Material Design 3, HIG |
| [`product-ux-expert`](./skills/product-ux-expert/) | UX evaluation, heuristics, accessibility |
| [`frontend-design`](./skills/frontend-design/) | Web frontend design patterns |
| [`ui-designer`](./skills/ui-designer.SKILL.md) | Design system toolkit |
| [`figma-to-code`](./skills/figma-to-code.SKILL.md) | Figma to production-ready code |
| [`react-best-practices`](./skills/react-best-practices.SKILL.md) | React/Next.js performance optimization |
| [`artifacts-builder`](./skills/artifacts-builder/) | Claude.ai HTML artifacts |

### Tooling & Automation

| Skill | Description |
|-------|-------------|
| [`git-commit-smart`](./skills/git-commit-smart.SKILL.md) | Conventional commit generation |
| [`playwright-automation`](./skills/playwright-automation.SKILL.md) | Browser automation and testing |
| [`project-health-auditor`](./skills/project-health-auditor.SKILL.md) | Codebase health analysis |
| [`structured-logging`](./skills/structured-logging.SKILL.md) | JSON logging with OpenTelemetry |
| [`web-asset-generator`](./skills/web-asset-generator/) | Favicons, app icons, OG images |
| [`github-trending`](./skills/github-trending/) | GitHub trending analysis |

### Mobile & Cross-Platform

| Skill | Description |
|-------|-------------|
| [`harmonyos-app`](./skills/harmonyos-app/) | HarmonyOS with ArkTS, ArkUI, Stage Model |

### Rust Specific

| Skill | Description |
|-------|-------------|
| [`rust-best-practices`](./skills/rust-best-practices/) | Microsoft Rust guidelines, error handling |

---

## Agents

Specialized agents for complex tasks.

| Agent | Expertise | Use Case |
|-------|-----------|----------|
| [`tech-lead-orchestrator`](./agents/tech-lead-orchestrator.md) | Coordination | Multi-step tasks, delegation |
| [`code-archaeologist`](./agents/code-archaeologist.md) | Exploration | Legacy codebase documentation |
| [`backend-typescript-architect`](./agents/backend-typescript-architect.md) | Architecture | Bun/Node.js, API design |
| [`senior-code-reviewer`](./agents/senior-code-reviewer.md) | Review | Security, performance, architecture |
| [`kubernetes-specialist`](./agents/kubernetes-specialist.md) | Infrastructure | K8s, Helm, GitOps |
| [`security-auditor`](./agents/security-auditor.md) | Security | OWASP Top 10, SAST |
| [`opensource-contributor`](./agents/opensource-contributor.md) | Contribution | Open source workflow |

---

## Skill Design Philosophy

Every skill in Claude Arsenal follows these principles:

1. **Hard Rules** - Mandatory constraints with `FORBIDDEN` / `REQUIRED` markers
2. **Practical Examples** - Real code, not just theory
3. **Verification Checklists** - Actionable validation steps
4. **Battle-Tested** - Used in production environments

---

## Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](./docs/installation.md) | Detailed setup instructions |
| [Skill Testing Guide](./docs/skill-testing-guide.md) | How to validate skills work |
| [Creating Plugins](./docs/creating-plugins.md) | Build your own skills |
| [Product Lifecycle (EN)](./docs/product-lifecycle-skills-en.md) | Full lifecycle coverage |
| [Product Lifecycle (中文)](./docs/product-lifecycle-skills-zh.md) | 产品生命周期覆盖 |

---

## Credits

Built on the shoulders of giants:

- [anthropics/skills](https://github.com/anthropics/skills) - Official Anthropic skills
- [obra/superpowers](https://github.com/obra/superpowers) - Development methodology
- [claude-code-plugins-plus](https://github.com/jeremylongshore/claude-code-plugins-plus) - Plugin hub
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) - Agent collection

---

## Contributing

Contributions welcome! Please read our [Contributing Guide](./CONTRIBUTING.md) first.

- Found a bug? [Open an issue](https://github.com/majiayu000/claude-arsenal/issues)
- Have a skill idea? [Start a discussion](https://github.com/majiayu000/claude-arsenal/discussions)
- Want to contribute? [Submit a PR](https://github.com/majiayu000/claude-arsenal/pulls)

---

## License

[MIT License](./LICENSE) - Use freely in your projects.

---

<div align="center">
  <p>If this helps you, consider giving it a ⭐</p>
  <p>Made with ❤️ for the Claude Code community</p>
</div>
