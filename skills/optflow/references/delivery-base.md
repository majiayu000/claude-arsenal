# Delivery Base — 共享交付流程

fixflow 和 optflow 共享的交付步骤基础。两者通过引用本文件复用通用流程。

## Define Ready Criteria (DoR)

- Restate scope, constraints, and expected outputs.
- Record backward-compatibility mode: `required` or `not required`.
- Record validation scope:
  - Step-level checks.
  - Final full checks.
- Record commit policy: `final_only` / `per_step` / `milestone`.
- Commit policy mapping:
  - If user asks grouped commits by stage, use `milestone`.
  - If user asks a single final commit only, use `final_only`.
  - Otherwise default to `per_step` (each step: modify -> test -> commit).
- Record commit requirement and expected message style.
- Record dirty-worktree baseline (what existed before this run).
- Record blockers (permissions, missing env vars, unavailable services).

## Build Complete Plan Before Editing

- Build a numbered plan covering all required changes.
- Order by risk/dependency:
  - Correctness/data integrity.
  - Security.
  - API/contract alignment.
  - UX/docs/cleanup.
- Define done condition for each step.
- Keep only one `in_progress` step at any time.

## Execute Step by Step

- Implement one step fully before moving to the next.
- Include code, related config/docs, and immediate verification in the same step.
- For `per_step` (default):
  - Stage only files for current step.
  - Run step-level checks.
  - Commit immediately after step checks pass.
  - Record step -> commit hash mapping.
- For `final_only`:
  - Still run step-level checks before moving on.
  - Delay commit until final validation completes.
- For `milestone`:
  - Run step-level checks for each step.
  - Commit at defined milestone boundaries.
- Update plan status after each completed step.
- Continue automatically until all steps are done.

## Apply No-Backward-Compatibility Mode (When Requested)

- Remove old paths, shims, adapters, and dual contracts.
- Prefer one clear implementation path.
- Treat breaking changes as intentional scope, not regressions.
- Document breaking impact in final report.

## Validate with Test Matrix

Run checks per step and again at the end. Use continuous verification.

Verification loop (per step):
1. Run relevant checks immediately after code change.
2. If any check fails -> fix root cause -> rerun ALL affected checks.
3. Only proceed to next step when ALL checks pass.
4. Maximum 3 fix attempts per check failure. If still failing after 3 attempts, stop and report.

Minimum matrix:
- Core logic: unit tests.
- Cross-module behavior: integration tests.
- Build health: compile/typecheck/build.
- Contract safety: API/serialization checks.
- Regression smoke: key user flow.

Failure loop:
1. Capture exact failing command/output.
2. Fix root cause.
3. Rerun failed check.
4. Rerun dependent checks.
5. Continue only when green.

## Commit and Handoff

- Stage only relevant files from this run.
- Use a clear, scope-aligned commit message format.
- Commit behavior by policy:
  - `per_step` (default): each step must be tested and committed before next step starts.
  - `final_only`: single commit after final validation passes.
  - `milestone`: commit at each planned milestone boundary.
- Report:
  - Change summary.
  - Validation commands + outcomes.
  - Breaking changes (if any).
  - Commit list (ordered).
  - Any remaining pre-existing dirty files (if not part of current scope).

## Output Templates

### Plan Template

```text
Goal:
Constraints:
- Backward compatibility: <required|not required>
- Commit policy: <final_only|per_step|milestone>
- Validation scope: <...>
- Dirty baseline: <pre-existing files>

Steps:
1. <step> (done condition: <...>)
2. <step> (done condition: <...>)
...
```

### Final Report Template

```text
Completed:
- <item>

Validation:
- <command>: <pass/fail + key result>

Breaking Changes:
- <none | list>

Commits:
- <hash> <message> (step/milestone/final)
```

## Guardrails

- Do not stop at planning when implementation is expected.
- Do not leave partially completed plan steps.
- Do not defer required testing when it can be run now.
- Do not default to `final_only`; use `per_step` unless user explicitly asks otherwise.
- Do not move to the next plan step before committing when `commit_policy = per_step`.
- Do not claim compatibility if user explicitly requested no compatibility work.
- Do not include unrelated pre-existing dirty files in commits.
- Do not hand off without concrete validation evidence.
