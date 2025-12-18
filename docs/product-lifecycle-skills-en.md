# Product Lifecycle Skills Roadmap

## Overview

This document describes the Claude Code Skills system that covers the entire product development lifecycle from discovery to deployment. These skills are designed to provide professional guidance for product managers, developers, and teams at every stage of product development.

---

## Product Lifecycle Stages

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Product Development Lifecycle                        │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│ Discovery│Definition│  Design  │ Develop  │   Test   │ Release  │ Operate  │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ product- │ prd-     │ product- │ Language │ compre-  │ devops-  │ observ-  │
│ discovery│ master   │ ux-expert│ skills   │ hensive- │ excellen-│ ability- │
│          │          │          │ api-     │ testing  │ ce       │ sre      │
│          │          │          │ design   │          │          │          │
│          │          │          │ tech-    │          │          │          │
│          │          │          │ spec     │          │          │          │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
                                                                       │
                                                                       ▼
                                                              ┌────────────────┐
                                                              │ product-       │
                                                              │ analytics      │
                                                              │ (Growth &      │
                                                              │  Optimization) │
                                                              └────────────────┘
```

---

## Skills Detailed Description

### 1. product-discovery

**Stage:** Discovery
**Goal:** Identify market opportunities and validate product ideas

| Capability | Description |
|------------|-------------|
| Market Research | TAM/SAM/SOM analysis, Porter's Five Forces |
| User Research | User interviews, surveys, ethnography |
| Competitive Analysis | Feature matrix, positioning map, SWOT |
| Opportunity Identification | Jobs-to-be-Done, Kano model |
| MVP Validation | Lean Startup methodology, hypothesis testing |

**Deliverables:**
- Market Analysis Report
- User Personas
- Competitive Analysis Matrix
- Value Proposition Canvas

---

### 2. prd-master

**Stage:** Definition
**Goal:** Transform product ideas into executable requirements

| Capability | Description |
|------------|-------------|
| PRD Writing | Standard PRD structure and templates |
| User Stories | As a... I want... So that... |
| Acceptance Criteria | Given/When/Then format |
| Prioritization | RICE, MoSCoW, Kano |
| Requirements Breakdown | Epic → Story → Task |

**Deliverables:**
- PRD Document
- User Story Map
- Priority Matrix
- Release Plan

---

### 3. product-ux-expert ✅ Completed

**Stage:** Design
**Goal:** Design excellent user experiences

| Capability | Description |
|------------|-------------|
| Usability Evaluation | Nielsen's 10 Heuristics |
| Accessibility | WCAG 2.2 AA Compliance |
| Cognitive Psychology | Hick's Law, Fitts's Law |
| User Journey | Journey Mapping |

---

### 4. technical-spec

**Stage:** Development (Early)
**Goal:** Make correct technical decisions

| Capability | Description |
|------------|-------------|
| Design Documents | RFC/Design Doc writing |
| Technology Selection | Evaluation matrix, trade-off analysis |
| Architecture Design | C4 model, architecture diagrams |
| Risk Assessment | Identification and mitigation strategies |

**Deliverables:**
- Technical Design Document
- Architecture Decision Records (ADR)
- API Definition Document
- Milestone Plan

---

### 5. devops-excellence

**Stage:** Release
**Goal:** Release products reliably and efficiently

| Capability | Description |
|------------|-------------|
| CI/CD | GitHub Actions, GitLab CI |
| Containerization | Docker, Kubernetes |
| IaC | Terraform, Pulumi |
| Release Strategies | Blue-green, Canary, Rolling |
| Security Scanning | SAST, DAST, SCA |

**Deliverables:**
- CI/CD Configuration Templates
- Dockerfile Best Practices
- Kubernetes Manifests
- Release Checklist

---

### 6. observability-sre

**Stage:** Operations
**Goal:** Keep systems running stably

| Capability | Description |
|------------|-------------|
| Monitoring | Prometheus, Grafana, Datadog |
| Logging | ELK, Loki, Structured Logging |
| Tracing | Jaeger, Zipkin, OpenTelemetry |
| SRE Practices | SLO/SLI/SLA, Incident Response |
| Chaos Engineering | Fault injection, resilience testing |

**Deliverables:**
- Monitoring Dashboards
- Alert Rules
- Runbooks
- Postmortem Templates

---

### 7. product-analytics

**Stage:** Growth
**Goal:** Drive product decisions with data

| Capability | Description |
|------------|-------------|
| Event Tracking | Events, properties, naming conventions |
| Metrics Framework | North Star Metric, AARRR |
| Funnel Analysis | Conversion optimization |
| A/B Testing | Experiment design, statistical significance |
| Retention Analysis | Cohort analysis, lifecycle |

**Deliverables:**
- Event Tracking Specification
- Metrics Dashboard Design
- A/B Test Plan
- Data Analysis Report

---

## Existing Skills (Completed)

| Skill | Category | Status |
|-------|----------|--------|
| typescript-project | Development | ✅ |
| golang-web | Development | ✅ |
| rust-project | Development | ✅ |
| python-project | Development | ✅ |
| zig-project | Development | ✅ |
| api-design | Development | ✅ |
| auth-security | Development | ✅ |
| database-patterns | Development | ✅ |
| product-ux-expert | Design | ✅ |
| comprehensive-testing | Testing | ✅ |
| mcp-server-development | Development | ✅ |

---

## Usage

```bash
# Install skill globally
cp -r skills/<skill-name> ~/.claude/skills/

# Or use in project
mkdir -p .claude/skills
cp -r skills/<skill-name> .claude/skills/
```

---

## Roadmap

| Stage | Skill | Priority | Status |
|-------|-------|----------|--------|
| Definition | prd-master | P0 | Pending |
| Release | devops-excellence | P0 | Pending |
| Operations | observability-sre | P1 | Pending |
| Growth | product-analytics | P1 | Pending |
| Discovery | product-discovery | P2 | Pending |
| Development | technical-spec | P2 | Pending |
