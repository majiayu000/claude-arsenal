#!/bin/bash
# codex-wrapper.sh - Wrapper script for calling Codex with common defaults
# Place in: ~/.claude/skills/codex-agent/scripts/

set -e

# Defaults
SANDBOX="${CODEX_SANDBOX:-read-only}"
OUTPUT_FORMAT=""
OUTPUT_FILE=""
SESSION=""
WORKDIR="${PWD}"

usage() {
    cat << EOF
Usage: codex-wrapper.sh [options] "<task>"

Options:
  -d, --dir <path>       Working directory (default: current)
  -s, --sandbox <mode>   Sandbox mode: read-only, workspace-write, danger-full-access
  -j, --json             Output as JSON
  -o, --output <file>    Save output to file
  -S, --session <id>     Use session ID for follow-up
  -f, --full-auto        Enable full-auto mode (workspace-write + auto-approve)
  -h, --help             Show this help

Examples:
  codex-wrapper.sh -d /path/to/project "Analyze the code"
  codex-wrapper.sh -j -s workspace-write "Fix the bug in main.ts"
  codex-wrapper.sh -S abc123 "Continue from where we left off"
EOF
    exit 0
}

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dir)
            WORKDIR="$2"
            shift 2
            ;;
        -s|--sandbox)
            SANDBOX="$2"
            shift 2
            ;;
        -j|--json)
            OUTPUT_FORMAT="--json"
            shift
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -S|--session)
            SESSION="$2"
            shift 2
            ;;
        -f|--full-auto)
            SANDBOX="workspace-write"
            FULL_AUTO="--full-auto"
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

set -- "${POSITIONAL_ARGS[@]}"

if [[ $# -eq 0 ]]; then
    echo "Error: Task description required"
    usage
fi

TASK="$1"

# Build command
CMD="codex exec"

if [[ -n "$SESSION" ]]; then
    CMD="codex exec resume $SESSION"
fi

CMD="$CMD -C \"$WORKDIR\" -s $SANDBOX"

if [[ -n "$OUTPUT_FORMAT" ]]; then
    CMD="$CMD $OUTPUT_FORMAT"
fi

if [[ -n "$OUTPUT_FILE" ]]; then
    CMD="$CMD -o \"$OUTPUT_FILE\""
fi

if [[ -n "$FULL_AUTO" ]]; then
    CMD="$CMD $FULL_AUTO"
fi

CMD="$CMD \"$TASK\""

# Execute
eval $CMD
