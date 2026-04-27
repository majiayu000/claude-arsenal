#!/usr/bin/env bash
# Add a new OAuth account (codex/claude/qwen/iflow/gemini) to an existing
# CLIProxyAPI deployment by running OAuth locally and syncing the credential
# JSON to the VPS auth-dir. CLIProxyAPI watcher hot-loads the new file —
# no restart needed.
#
# Usage:
#   PROVIDER=codex SSH_TARGET=root@host SSH_KEY=~/.ssh/id_ed25519 \
#     CLIPROXY_LOCAL=/path/to/CLIProxyAPI \
#     ./add_codex_account.sh

set -euo pipefail

: "${PROVIDER:=codex}"   # one of: codex|claude|qwen|iflow|antigravity|gemini
: "${SSH_TARGET:?SSH_TARGET required}"
: "${SSH_KEY:=$HOME/.ssh/id_ed25519}"
: "${CLIPROXY_LOCAL:=$PWD}"
: "${LOCAL_AUTH_DIR:=$HOME/.cli-proxy-api}"
: "${REMOTE_AUTH_DIR:=/root/.cli-proxy-api}"

case "$PROVIDER" in
  codex)        FLAG=-codex-login        ;;
  claude)       FLAG=-claude-login       ;;
  qwen)         FLAG=-qwen-login         ;;
  iflow)        FLAG=-iflow-login        ;;
  antigravity)  FLAG=-antigravity-login  ;;
  gemini)       FLAG=-login              ;;
  *) echo "unknown PROVIDER=$PROVIDER" >&2; exit 2 ;;
esac

mkdir -p "$LOCAL_AUTH_DIR"
echo ">> Capturing existing credentials before login"
before=$(ls -1 "$LOCAL_AUTH_DIR"/${PROVIDER}-*.json 2>/dev/null | sort || true)

echo ">> Run OAuth in browser for the NEW account (logout/incognito as needed)"
( cd "$CLIPROXY_LOCAL" && go run ./cmd/server "$FLAG" -config config.yaml )

after=$(ls -1 "$LOCAL_AUTH_DIR"/${PROVIDER}-*.json 2>/dev/null | sort || true)
new=$(comm -13 <(echo "$before") <(echo "$after") || true)

if [ -z "$new" ]; then
  echo "no new credential file detected; aborting"
  exit 1
fi

echo ">> New credential(s):"
echo "$new"

echo ">> Syncing to $SSH_TARGET:$REMOTE_AUTH_DIR"
ssh -i "$SSH_KEY" "$SSH_TARGET" "mkdir -p '$REMOTE_AUTH_DIR'"
while IFS= read -r f; do
  [ -n "$f" ] && scp -i "$SSH_KEY" "$f" "$SSH_TARGET:$REMOTE_AUTH_DIR/"
done <<< "$new"

echo ">> Watcher should auto-load. Tailing log for confirmation..."
ssh -i "$SSH_KEY" "$SSH_TARGET" \
  "tail -n 100 /root/CLIProxyAPI/cli-proxy-api.log | grep -iE 'auth file changed|added' | tail -n 5"

echo ">> Listing remote credentials"
ssh -i "$SSH_KEY" "$SSH_TARGET" "ls -l '$REMOTE_AUTH_DIR'/${PROVIDER}-*.json"
