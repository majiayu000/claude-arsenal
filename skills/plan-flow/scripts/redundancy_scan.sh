#!/usr/bin/env bash
set -euo pipefail

target_dir="${1:-src}"

if [[ ! -d "${target_dir}" ]]; then
  echo "[ERR] target directory not found: ${target_dir}" >&2
  exit 1
fi

echo "# Redundancy Scan Report"
echo
echo "- target: \`${target_dir}\`"
echo "- generated_at: $(date '+%Y-%m-%d %H:%M:%S')"
echo

echo "## 1) Duplicate exported type names"
dup_names="$(rg -n --no-heading 'pub (struct|enum|trait) [A-Za-z_][A-Za-z0-9_]*' "${target_dir}" \
  | sed -E 's/.*pub (struct|enum|trait) ([A-Za-z_][A-Za-z0-9_]*).*/\2/' \
  | sort \
  | uniq -d || true)"

if [[ -z "${dup_names}" ]]; then
  echo "- none found"
else
  while IFS= read -r name; do
    [[ -z "${name}" ]] && continue
    echo "- \`${name}\`"
    rg -n --no-heading "pub (struct|enum|trait) ${name}\\b" "${target_dir}" | sed 's/^/  - /'
  done <<< "${dup_names}"
fi
echo

echo "## 2) Parallel builder/factory hints"
rg -n --no-heading 'create_.*client|build_.*client|factory|registry|from_config' "${target_dir}" | sed 's/^/- /' | head -n 120 || true
echo

echo "## 3) Legacy/dead-code hints"
rg -n --no-heading 'allow\(dead_code\)|legacy|deprecated|TODO.*remove|unused' "${target_dir}" | sed 's/^/- /' | head -n 160 || true
echo

echo "## 4) Next action"
echo "- Convert high-confidence items into finding IDs (F1/F2/...)."
echo "- Record evidence and risk per finding."
echo "- Score with references/risk-impact-scoring.md and map to P0/P1/P2."
