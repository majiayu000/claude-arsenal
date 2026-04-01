#!/usr/bin/env python3
"""Generate a docs/plan draft from redundancy scan findings."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Sequence


SECTION_HEADER_RE = re.compile(r"^##\s+(\d+)\)")
DUP_SYMBOL_RE = re.compile(r"^- `([^`]+)`\s*$")
BULLET_RE = re.compile(r"^\s*-\s+(.+)$")
FILE_PATH_RE = re.compile(r"([A-Za-z0-9_./-]+\.rs):\d+")
PHASE_ORDER = ["P0", "P1", "P2"]
PHASE_RANK = {phase: idx for idx, phase in enumerate(PHASE_ORDER)}
LEVEL_TO_SCORE = {"low": 1, "medium": 3, "high": 5}


@dataclass
class Finding:
    finding_id: str
    step_id: str
    category: str
    title: str
    symbol: str | None
    files: List[str]
    evidence: List[str]
    impact: str
    effort: int
    risk: str
    confidence: int
    priority_score: int
    phase: str
    canonical_hint: str


def read_scan_report(
    repo_path: Path, scan_report: Path | None, target_dir: str | None
) -> str:
    if scan_report is not None:
        return scan_report.read_text(encoding="utf-8")

    if target_dir is None:
        raise ValueError("Either --scan-report or --target-dir must be provided.")

    scan_script = Path(__file__).resolve().parent / "redundancy_scan.sh"
    if not scan_script.exists():
        raise FileNotFoundError(f"Scan script not found: {scan_script}")

    result = subprocess.run(
        [str(scan_script), target_dir],
        cwd=str(repo_path),
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def parse_sections(report_text: str) -> tuple[List[str], List[str], List[str]]:
    duplicate_lines: List[str] = []
    factory_lines: List[str] = []
    legacy_lines: List[str] = []
    section = ""

    for line in report_text.splitlines():
        section_match = SECTION_HEADER_RE.match(line)
        if section_match:
            section = section_match.group(1)
            continue

        if section == "1":
            duplicate_lines.append(line)
        elif section == "2":
            factory_lines.append(line)
        elif section == "3":
            legacy_lines.append(line)

    return duplicate_lines, factory_lines, legacy_lines


def extract_files(evidence_lines: Sequence[str]) -> List[str]:
    files: List[str] = []
    for line in evidence_lines:
        m = FILE_PATH_RE.search(line)
        if not m:
            continue
        path = m.group(1)
        if path not in files:
            files.append(path)
    return files


def parse_duplicate_findings(lines: Sequence[str]) -> List[Finding]:
    findings: List[Finding] = []
    current_symbol: str | None = None
    current_evidence: List[str] = []

    def flush() -> None:
        nonlocal current_symbol, current_evidence
        if current_symbol is None:
            return
        files = extract_files(current_evidence)
        count = len(files)
        impact = "high" if count >= 3 else "medium"
        risk = "medium"
        findings.append(
            Finding(
                finding_id="",
                step_id="",
                category="same-concept multi-def",
                title=f"收敛重复类型 `{current_symbol}` 定义",
                symbol=current_symbol,
                files=files,
                evidence=current_evidence[:3],
                impact=impact,
                effort=0,
                risk=risk,
                confidence=0,
                priority_score=0,
                phase="P2",
                canonical_hint=f"Select one canonical `{current_symbol}` owner and adapt callers.",
            )
        )
        current_symbol = None
        current_evidence = []

    for line in lines:
        symbol_match = DUP_SYMBOL_RE.match(line.strip())
        if symbol_match:
            flush()
            current_symbol = symbol_match.group(1)
            continue

        if current_symbol is None:
            continue

        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            current_evidence.append(bullet_match.group(1))

    flush()
    return findings


def parse_single_line_findings(
    lines: Sequence[str],
    category: str,
    title_prefix: str,
    impact: str,
    risk: str,
) -> List[Finding]:
    findings: List[Finding] = []
    seen_files: set[str] = set()

    for line in lines:
        bullet_match = BULLET_RE.match(line)
        if not bullet_match:
            continue
        evidence_text = bullet_match.group(1)
        file_match = FILE_PATH_RE.search(evidence_text)
        if not file_match:
            continue
        file_path = file_match.group(1)
        if file_path in seen_files:
            continue
        seen_files.add(file_path)
        short_name = Path(file_path).name
        findings.append(
            Finding(
                finding_id="",
                step_id="",
                category=category,
                title=f"{title_prefix} `{short_name}`",
                symbol=None,
                files=[file_path],
                evidence=[evidence_text],
                impact=impact,
                effort=0,
                risk=risk,
                confidence=0,
                priority_score=0,
                phase="P2",
                canonical_hint="Converge to a single path or mark deprecated with migration notes.",
            )
        )

    return findings


def pick_findings(
    duplicate_findings: List[Finding],
    factory_findings: List[Finding],
    legacy_findings: List[Finding],
    max_findings: int,
) -> List[Finding]:
    if max_findings < 1:
        return []

    dup_budget = max(1, max_findings // 2)
    remaining = max_findings - dup_budget
    factory_budget = remaining // 2
    legacy_budget = remaining - factory_budget

    selected: List[Finding] = []
    selected.extend(duplicate_findings[:dup_budget])
    selected.extend(factory_findings[:factory_budget])
    selected.extend(legacy_findings[:legacy_budget])

    overflow_sources = [
        duplicate_findings[dup_budget:],
        factory_findings[factory_budget:],
        legacy_findings[legacy_budget:],
    ]
    for source in overflow_sources:
        for finding in source:
            if len(selected) >= max_findings:
                return selected
            selected.append(finding)

    return selected[:max_findings]


def label_score(level: str) -> int:
    return LEVEL_TO_SCORE.get(level.strip().lower(), 1)


def assign_phase(priority_score: int) -> str:
    if priority_score >= 12:
        return "P0"
    if priority_score >= 4:
        return "P1"
    return "P2"


def estimate_effort(category: str, file_count: int) -> int:
    if category == "same-concept multi-def":
        if file_count <= 1:
            return 1
        if file_count == 2:
            return 3
        if file_count == 3:
            return 4
        return 5
    if category == "parallel-implementation":
        return 2 if file_count <= 1 else 3
    return 1 if file_count <= 1 else 2


def estimate_confidence(category: str, evidence_count: int, file_count: int) -> int:
    if category == "same-concept multi-def":
        if file_count >= 2 and evidence_count >= 2:
            return 5
        return 4
    if category == "parallel-implementation":
        return 3 if evidence_count >= 1 else 2
    return 3 if evidence_count >= 1 else 2


def enrich_and_sort_findings(findings: List[Finding]) -> None:
    for finding in findings:
        impact_score = label_score(finding.impact)
        risk_score = label_score(finding.risk)
        finding.effort = estimate_effort(finding.category, len(finding.files))
        finding.confidence = estimate_confidence(
            finding.category, len(finding.evidence), len(finding.files)
        )
        finding.priority_score = (impact_score * finding.confidence) - (
            finding.effort + risk_score
        )
        finding.phase = assign_phase(finding.priority_score)

    findings.sort(
        key=lambda finding: (
            PHASE_RANK.get(finding.phase, 99),
            -finding.priority_score,
            -label_score(finding.impact),
            finding.title,
        )
    )

    for idx, finding in enumerate(findings, start=1):
        finding.finding_id = f"F{idx}"
        finding.step_id = f"A{idx}"


def suggest_test_command(files: Sequence[str]) -> str:
    if not files:
        return "cargo test --lib"
    path = files[0]
    parts = path.split("/")
    if len(parts) < 3 or parts[0] != "src":
        return "cargo test --lib"
    module_parts = parts[1:-1]
    if not module_parts:
        return "cargo test --lib"
    target = "::".join(module_parts[:2])
    return f"cargo test {target} --lib"


def normalize_cell(value: str) -> str:
    return value.replace("|", "\\|").strip()


def phase_summary(findings: Sequence[Finding], phase: str) -> List[Finding]:
    return [finding for finding in findings if finding.phase == phase]


def render_plan(
    task_name: str,
    repo_path: Path,
    findings: List[Finding],
) -> str:
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    lines: List[str] = []

    lines.append(f"# {task_name} 执行计划（自动生成草案）")
    lines.append("")
    lines.append("- 计划版本: v1-draft")
    lines.append(f"- 创建时间: {today}")
    lines.append(f"- 适用仓库: `{repo_path}`")
    lines.append("- 生成方式: `findings_to_plan.py` from redundancy scan")
    lines.append("- 执行模式: 每步改动 -> 立即测试 -> 回写计划 -> 下一步")
    lines.append("")
    lines.append("## 0. 执行约束（DoR）")
    lines.append("")
    lines.append("- 目标: 收敛重复/冗余设计并保持主流程稳定。")
    lines.append("- 兼容性: required（默认向后兼容，除非步骤中明确说明）。")
    lines.append("- 提交策略: per_step（每步测试通过后再提交，可按用户要求调整）。")
    lines.append("- 测试策略:")
    lines.append("  - 步骤级: 每步至少 1 条定向测试 + 1 条健康检查。")
    lines.append("  - 阶段级: 每阶段完成后运行更广泛检查。")
    lines.append("  - 最终: 运行全量或可行最大范围回归。")
    lines.append("")
    lines.append("## 1. 分析结果（自动提取 + 评分）")
    lines.append("")
    lines.append("| id | 类别 | 文件与符号 | impact | effort | risk | confidence | score | phase | 证据 | 建议收敛方向 |")
    lines.append("|----|------|------------|--------|--------|------|------------|-------|-------|------|--------------|")

    if not findings:
        lines.append("| F1 | manual-review | <to-fill> | 1 | 1 | 1 | 1 | -1 | P2 | no parsed findings | add manual findings before implementation |")
    else:
        for finding in findings:
            file_and_symbol = ", ".join(finding.files[:2]) if finding.files else "<unknown>"
            if finding.symbol:
                file_and_symbol = f"{file_and_symbol}::{finding.symbol}"
            evidence = finding.evidence[0] if finding.evidence else "scan hint"
            lines.append(
                "| {fid} | {cat} | {fs} | {impact} | {effort} | {risk} | {confidence} | {score} | {phase} | {ev} | {hint} |".format(
                    fid=finding.finding_id,
                    cat=normalize_cell(finding.category),
                    fs=normalize_cell(file_and_symbol),
                    impact=label_score(finding.impact),
                    effort=finding.effort,
                    risk=label_score(finding.risk),
                    confidence=finding.confidence,
                    score=finding.priority_score,
                    phase=finding.phase,
                    ev=normalize_cell(evidence),
                    hint=normalize_cell(finding.canonical_hint),
                )
            )

    lines.append("")
    lines.append("## 2. 分阶段执行顺序（P0 -> P1 -> P2）")
    lines.append("")
    if not findings:
        lines.append("- P0: 0 steps")
        lines.append("- P1: 0 steps")
        lines.append("- P2: 1 step (manual evidence completion)")
    else:
        for phase in PHASE_ORDER:
            phase_items = phase_summary(findings, phase)
            lines.append(f"- {phase}: {len(phase_items)} steps")
            for finding in phase_items:
                lines.append(
                    f"  - Step {finding.step_id} <- {finding.finding_id} "
                    f"(score={finding.priority_score}): {finding.title}"
                )

    lines.append("")
    lines.append("## 3. 详细步骤（按 phase 排序）")
    lines.append("")

    if not findings:
        lines.append("### Step A1 补充分析证据并生成 findings")
        lines.append("")
        lines.append("- 状态: `in_progress`")
        lines.append("- 目标: 补齐 evidence 后再进入实现。")
        lines.append("- 预计改动文件:")
        lines.append("  - `plan/<this-file>.md`")
        lines.append("- 详细改动:")
        lines.append("  - 补充文件级证据、风险说明与 canonical 选择。")
        lines.append("- 步骤级测试命令:")
        lines.append("  - `cargo check --lib`")
        lines.append("- 完成判定:")
        lines.append("  - 至少 3 个高置信 findings 可映射到明确改动步骤。")
        lines.append("")
    else:
        first_step = True
        for phase in PHASE_ORDER:
            phase_items = phase_summary(findings, phase)
            if not phase_items:
                continue
            lines.append(f"#### 阶段 {phase}")
            lines.append("")
            for finding in phase_items:
                status = "in_progress" if first_step else "pending"
                first_step = False
                lines.append(f"### Step {finding.step_id} {finding.title}")
                lines.append("")
                lines.append(f"- 状态: `{status}`")
                lines.append(f"- 关联 finding: `{finding.finding_id}`")
                lines.append(f"- 优先级阶段: `{finding.phase}`")
                lines.append(
                    "- 评分: "
                    f"`impact={label_score(finding.impact)}`, "
                    f"`effort={finding.effort}`, "
                    f"`risk={label_score(finding.risk)}`, "
                    f"`confidence={finding.confidence}`, "
                    f"`score={finding.priority_score}`"
                )
                lines.append("- 目标: 收敛该 finding 对应的重复/冗余路径，并保持行为一致。")
                lines.append("- 预计改动文件:")
                if finding.files:
                    for path in finding.files[:4]:
                        lines.append(f"  - `{path}`")
                else:
                    lines.append("  - `<to-identify>`")
                lines.append("- 详细改动:")
                lines.append("  - 选定 canonical 定义/入口，并将其余路径改为复用或弃用。")
                lines.append("  - 为该收敛点补充守护测试，防止后续再次漂移。")
                lines.append("- 步骤级测试命令:")
                lines.append(f"  - `{suggest_test_command(finding.files)}`")
                lines.append("  - `cargo check --lib`")
                lines.append("- 完成判定:")
                lines.append("  - 仅保留一条主路径，旧路径已迁移或明确标注兼容层。")
                lines.append("  - 目标测试和健康检查均通过。")
                lines.append("")

    lines.append("## 4. 回归测试矩阵")
    lines.append("")
    lines.append("- 阶段完成检查:")
    lines.append("  - `cargo check --lib`")
    lines.append("- 最终检查:")
    lines.append("  - `cargo test --lib`")
    lines.append("")
    lines.append("## 5. 执行日志（每步完成后追加）")
    lines.append("")
    lines.append("- <YYYY-MM-DD>")
    lines.append("  - Step <ID>: `completed`")
    lines.append("    - 修改文件:")
    lines.append("      - `<file>`")
    lines.append("    - 主要改动:")
    lines.append("      - <summary>")
    lines.append("    - 执行测试:")
    lines.append("      - `<command>` -> pass/fail")
    lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a docs/plan draft from scan findings.")
    parser.add_argument("--scan-report", type=Path, help="Path to markdown scan report.")
    parser.add_argument("--target-dir", help="Target dir for running redundancy scan (e.g. src).")
    parser.add_argument("--output", type=Path, required=True, help="Output plan file path.")
    parser.add_argument("--task-name", default="冗余设计收敛", help="Plan title.")
    parser.add_argument("--repo-path", type=Path, default=Path.cwd(), help="Repository root path.")
    parser.add_argument("--max-findings", type=int, default=12, help="Max findings to include.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.scan_report is None and args.target_dir is None:
        print("[ERR] Provide either --scan-report or --target-dir.")
        return 1

    repo_path = args.repo_path.resolve()
    if args.scan_report is not None and not args.scan_report.exists():
        print(f"[ERR] Scan report not found: {args.scan_report}")
        return 1

    try:
        report_text = read_scan_report(repo_path, args.scan_report, args.target_dir)
    except (ValueError, FileNotFoundError, subprocess.CalledProcessError) as exc:
        print(f"[ERR] Failed to get scan report: {exc}")
        return 1

    duplicate_lines, factory_lines, legacy_lines = parse_sections(report_text)
    duplicate_findings = parse_duplicate_findings(duplicate_lines)
    factory_findings = parse_single_line_findings(
        factory_lines,
        category="parallel-implementation",
        title_prefix="收敛并行构造路径",
        impact="medium",
        risk="medium",
    )
    legacy_findings = parse_single_line_findings(
        legacy_lines,
        category="legacy-or-dead-code",
        title_prefix="清理 legacy/dead-code 线索",
        impact="low",
        risk="low",
    )

    findings = pick_findings(
        duplicate_findings,
        factory_findings,
        legacy_findings,
        max_findings=args.max_findings,
    )
    enrich_and_sort_findings(findings)

    plan_text = render_plan(args.task_name, repo_path, findings)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(plan_text, encoding="utf-8")
    print(f"[OK] Generated plan draft: {args.output}")
    print(
        "[INFO] findings selected: "
        f"duplicates={len(duplicate_findings)}, factory={len(factory_findings)}, legacy={len(legacy_findings)}, "
        f"used={len(findings)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
