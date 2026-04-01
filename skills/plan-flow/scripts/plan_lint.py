#!/usr/bin/env python3
"""Lint docs/plan markdown files for step-state workflow quality gates."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple


STEP_HEADER_RE = re.compile(r"^###\s+Step\s+")
STEP_ID_RE = re.compile(r"^###\s+Step\s+([A-Za-z]+\d+)\b")
STATUS_RE = re.compile(r"^\s*-\s*状态:\s*`?([a-zA-Z_]+)`?\s*$")
TEST_SECTION_RE = re.compile(r"^\s*-\s*步骤级测试命令[:：]\s*$")
COMMAND_ITEM_RE = re.compile(r"^\s*-\s+`[^`]+`\s*$")
COMMAND_ITEM_WITH_NOTE_RE = re.compile(r"^\s*-\s+`[^`]+`.*$")
SECTION_BULLET_RE = re.compile(r"^\s*-\s*[^`].*[:：]\s*$")
EXEC_LOG_SECTION_RE = re.compile(r"^##\s+\d+\.\s*执行日志")
EXEC_LOG_STEP_RE = re.compile(r"^\s*-\s*Step\s+([A-Za-z]+\d+):\s*`?([a-zA-Z_]+)`?\s*$")
VALID_STATUSES = {"pending", "in_progress", "completed", "blocked"}


@dataclass
class StepBlock:
    title: str
    step_id: str | None
    start_line: int
    lines: List[str]
    status: str | None = None

    def has_test_commands(self) -> bool:
        in_test_section = False
        command_count = 0
        for line in self.lines:
            if TEST_SECTION_RE.match(line):
                in_test_section = True
                continue
            if in_test_section and line.startswith("### "):
                break
            if in_test_section and (
                COMMAND_ITEM_RE.match(line) or COMMAND_ITEM_WITH_NOTE_RE.match(line)
            ):
                command_count += 1
                continue
            if in_test_section and SECTION_BULLET_RE.match(line):
                # End test command block when next subsection bullet appears.
                in_test_section = False
                continue
        return command_count > 0


def parse_steps(text: str) -> List[StepBlock]:
    lines = text.splitlines()
    steps: List[StepBlock] = []
    current: StepBlock | None = None

    for i, line in enumerate(lines, start=1):
        if STEP_HEADER_RE.match(line):
            if current is not None:
                steps.append(current)
            step_id_match = STEP_ID_RE.match(line.strip())
            current = StepBlock(
                title=line.strip(),
                step_id=step_id_match.group(1) if step_id_match else None,
                start_line=i,
                lines=[],
            )
            continue
        if current is not None:
            current.lines.append(line)

    if current is not None:
        steps.append(current)

    for step in steps:
        for line in step.lines:
            m = STATUS_RE.match(line)
            if m:
                step.status = m.group(1).strip()
                break
    return steps


def parse_execution_logs(text: str) -> Tuple[bool, Dict[str, Set[str]]]:
    in_exec_log = False
    found_exec_log_section = False
    step_statuses: Dict[str, Set[str]] = {}

    for line in text.splitlines():
        if EXEC_LOG_SECTION_RE.match(line):
            in_exec_log = True
            found_exec_log_section = True
            continue
        if in_exec_log and line.startswith("## "):
            break
        if not in_exec_log:
            continue
        m = EXEC_LOG_STEP_RE.match(line)
        if m:
            step_id = m.group(1)
            status = m.group(2)
            step_statuses.setdefault(step_id, set()).add(status)

    return found_exec_log_section, step_statuses


def lint_steps(
    steps: List[StepBlock],
    found_exec_log_section: bool,
    log_step_statuses: Dict[str, Set[str]],
) -> int:
    errors: List[str] = []
    warnings: List[str] = []

    if not steps:
        errors.append("No step headers found (`### Step ...`).")

    in_progress_count = 0
    completed_count = 0
    for step in steps:
        if step.status is None:
            errors.append(f"{step.title} (line {step.start_line}): missing `- 状态:` field.")
            continue
        if step.status not in VALID_STATUSES:
            errors.append(
                f"{step.title} (line {step.start_line}): invalid status `{step.status}` "
                f"(expected one of {sorted(VALID_STATUSES)})."
            )
            continue
        if step.status == "in_progress":
            in_progress_count += 1
        if step.status == "completed":
            completed_count += 1
            if not step.has_test_commands():
                errors.append(
                    f"{step.title} (line {step.start_line}): `completed` step has no detected test commands."
                )
            if step.step_id is None:
                errors.append(
                    f"{step.title} (line {step.start_line}): cannot derive Step ID for execution-log matching."
                )
            elif step.step_id not in log_step_statuses:
                errors.append(
                    f"{step.title} (line {step.start_line}): missing execution log entry for completed step `{step.step_id}`."
                )
            elif "completed" not in log_step_statuses[step.step_id]:
                errors.append(
                    f"{step.title} (line {step.start_line}): execution log for `{step.step_id}` exists but is not marked `completed`."
                )

    if in_progress_count > 1:
        errors.append(f"Found {in_progress_count} `in_progress` steps; expected at most 1.")
    if completed_count == len(steps) and in_progress_count != 0:
        warnings.append("All steps are completed but `in_progress` still exists.")
    if completed_count > 0 and not found_exec_log_section:
        errors.append(
            "No execution log section found (`## <n>. 执行日志...`) but completed steps exist."
        )

    known_step_ids = {step.step_id for step in steps if step.step_id}
    for logged_step_id in sorted(log_step_statuses.keys()):
        if logged_step_id not in known_step_ids:
            warnings.append(
                f"Execution log has Step `{logged_step_id}` not present in step headers."
            )

    for warn in warnings:
        print(f"[WARN] {warn}")
    for err in errors:
        print(f"[ERR]  {err}")

    if not errors:
        print(
            f"[OK] Lint passed: {len(steps)} steps, "
            f"{completed_count} completed, {in_progress_count} in_progress."
        )
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a docs/plan markdown file.")
    parser.add_argument("plan_file", help="Path to docs/plan markdown file")
    args = parser.parse_args()

    plan_path = Path(args.plan_file)
    if not plan_path.exists():
        print(f"[ERR] Plan file not found: {plan_path}")
        return 1

    text = plan_path.read_text(encoding="utf-8")
    steps = parse_steps(text)
    found_exec_log_section, log_step_statuses = parse_execution_logs(text)
    return lint_steps(steps, found_exec_log_section, log_step_statuses)


if __name__ == "__main__":
    sys.exit(main())
