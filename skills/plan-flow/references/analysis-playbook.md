# Redundancy Analysis Playbook

Use this playbook to analyze duplicate/redundant design in any repo before writing implementation steps.

## 1. Scope and Baseline

- Confirm target scope:
  - Directories/modules included.
  - Explicitly excluded areas.
- Capture baseline:
  - Current branch.
  - Dirty files from `git status --short`.
  - Build/test constraints in current environment.

## 2. Build Architecture Inventory

Create a concise inventory table grouped by layer:

- Canonical models/types
- Factory/registry/entry points
- Adapters (route/service/provider/client)
- Infra abstractions (http/storage/cache/logging/config)

For each item, record:
- Source file
- Exported symbols
- Inbound callers (who uses it)
- Outbound dependencies (what it uses)

## 3. Detect Redundancy Patterns

Mark candidates by pattern:

1. Same concept, multiple definitions
- Example shape: multiple `*Context`, `*Config`, `*Message` with overlapping meaning.

2. Same responsibility, parallel implementations
- Example shape: multiple builder/factory paths with divergent defaults.

3. Multiple declaration sources for one feature
- Example shape: provider/module is declared in several places that drift independently.

4. Exported but unconnected path
- Module/type is public or compiled but unused in main flow.

5. Dead code and stale compatibility layer
- `allow(dead_code)` islands, legacy wrappers without active call paths.

## 4. Evidence Standard (Required)

A finding is valid only if it includes:
- File path(s) and symbol(s)
- Usage evidence (`rg`, compiler warnings, tests, or call path trace)
- Risk note (what may break if converged)
- Suggested canonical owner (which definition/path should remain)

No evidence, no plan entry.

## 5. Convergence Decision Rules

For each finding, choose one action:
- Keep as canonical.
- Merge into canonical.
- Replace caller paths and deprecate old path.
- Feature-gate or remove if truly unused.

Decision should include:
- Why this canonical path is preferred.
- What migration/compatibility shim is needed (if any).

## 6. Convert Findings into Plan Steps

Each step should:
- Focus on one convergence action.
- Touch a bounded file list.
- Include one targeted test and one health check.
- Define objective completion criteria.

Recommended order:
1. Add guard tests for drift-prone areas.
2. Converge creation/entry points.
3. Converge shared models.
4. Remove isolated redundant paths.
5. Run broader regression.

## 7. Reporting Format

At analysis end, output:
- Findings list (sorted by priority).
- Impact/effort/risk scoring table.
- Proposed phase plan (`P0`, `P1`, `P2`).
- Known unknowns and blocked validations.
