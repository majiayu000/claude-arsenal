#!/usr/bin/env python3
"""Write/merge ModelRatio / CacheRatio / CompletionRatio overrides into NewAPI SQLite.

NewAPI v0.12.x merges the persisted `options` rows on top of the in-memory defaults.
This script reads the current values, deep-merges patches, writes them back,
then restarts the container so the new values are loaded.

Pricing semantics (CRITICAL — easy to get wrong):
  ModelRatio       = USD per 1M input tokens / 2  (NewAPI internal scale)
                     User-facing rule: if your target input price is X USD/1M,
                     write X / 2  e.g. input 2.5 -> ModelRatio 1.25.
                     BUT: many docs treat ModelRatio as the input price directly
                     for OpenAI-compatible providers. Verify with a test request
                     and check logs.quota matches expectation.
  CacheRatio       = cached_input / input  (relative multiplier)
                     If cached input is 0.1x of input, write 0.1.
  CompletionRatio  = output / input (relative multiplier)
                     If output is 6x of input, write 6.

Usage:
  SSH_TARGET=root@host  SSH_KEY=~/.ssh/id_ed25519  ./set_pricing.py \
      --model gpt-5.4         --input 2.5  --cached 0.25 --output 15 \
      --model gpt-5.3-codex   --input 1.75 --cached 0.175 --output 14

The script computes the three ratios from raw USD/1M prices.
"""
import argparse
import json
import os
import shlex
import subprocess
import sys


def run_ssh(target: str, key: str, command: str) -> str:
    cmd = ["ssh", "-i", key, target, command]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise SystemExit(f"ssh failed: {' '.join(shlex.quote(c) for c in cmd)}")
    return result.stdout


def build_remote_python(updates: dict, db_path: str) -> str:
    """Return a heredoc Python program executed on the VPS."""
    payload = json.dumps(updates, ensure_ascii=False)
    program = f"""
import sqlite3, json, sys
DB = {json.dumps(db_path)}
patches = json.loads({json.dumps(payload)})
conn = sqlite3.connect(DB)
cur = conn.cursor()
for key, patch in patches.items():
    row = cur.execute("SELECT value FROM options WHERE key=?", (key,)).fetchone()
    data = json.loads(row[0]) if row and row[0] else {{}}
    data.update(patch)
    value = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    cur.execute(
        "INSERT INTO options(key, value) VALUES(?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )
conn.commit()
for key in ("ModelRatio", "CacheRatio", "CompletionRatio"):
    row = cur.execute("SELECT value FROM options WHERE key=?", (key,)).fetchone()
    if row:
        sample = {{m: json.loads(row[0]).get(m) for m in patches.get(key, {{}}).keys()}}
        print(key, sample)
conn.close()
"""
    return f"python3 - <<'PY'{program}\nPY"


def main() -> int:
    p = argparse.ArgumentParser(description="NewAPI pricing override writer")
    p.add_argument(
        "--model",
        action="append",
        required=True,
        dest="models",
        help="Model name (repeatable). Each --model must be followed by --input/--cached/--output.",
    )
    p.add_argument("--input", type=float, action="append", required=True, dest="inputs",
                   help="Input price USD per 1M tokens (repeatable, paired with --model)")
    p.add_argument("--cached", type=float, action="append", default=[], dest="cacheds",
                   help="Cached input price USD per 1M tokens")
    p.add_argument("--output", type=float, action="append", required=True, dest="outputs",
                   help="Output price USD per 1M tokens")
    p.add_argument("--ratio-divisor", type=float, default=2.0,
                   help="ModelRatio = input / divisor. Default 2 for NewAPI v0.12.x "
                        "(OneAPI internal-scale convention: ModelRatio*2 == USD/1M). "
                        "Set 1 if your fork uses raw USD/1M.")
    p.add_argument("--db", default="/root/newapi/data/one-api.db")
    p.add_argument("--restart", default="new-api",
                   help="docker container name to restart after write (set empty to skip)")
    args = p.parse_args()

    target = os.environ.get("SSH_TARGET")
    key = os.environ.get("SSH_KEY", os.path.expanduser("~/.ssh/id_ed25519"))
    if not target:
        sys.stderr.write("SSH_TARGET env required\n")
        return 2

    n = len(args.models)
    if not (len(args.inputs) == len(args.outputs) == n):
        sys.stderr.write("--model / --input / --output must appear the same number of times\n")
        return 2
    if args.cacheds and len(args.cacheds) != n:
        sys.stderr.write("--cached must appear 0 times or once per --model\n")
        return 2

    model_ratio: dict = {}
    cache_ratio: dict = {}
    completion_ratio: dict = {}
    for i, model in enumerate(args.models):
        inp = args.inputs[i]
        out = args.outputs[i]
        cached = args.cacheds[i] if args.cacheds else None
        model_ratio[model] = inp / args.ratio_divisor
        completion_ratio[model] = out / inp if inp else 0
        if cached is not None and inp:
            cache_ratio[model] = cached / inp

    updates = {"ModelRatio": model_ratio, "CompletionRatio": completion_ratio}
    if cache_ratio:
        updates["CacheRatio"] = cache_ratio

    print("Computed ratios:")
    print(json.dumps(updates, ensure_ascii=False, indent=2))

    print(f"Applying to {target}:{args.db}")
    out = run_ssh(target, key, build_remote_python(updates, args.db))
    print(out)

    if args.restart:
        print(f"Restarting container {args.restart}")
        run_ssh(target, key, f"docker restart {shlex.quote(args.restart)} >/dev/null")
    print("Done. Verify with verify_stack.sh.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
