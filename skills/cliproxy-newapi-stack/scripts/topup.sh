#!/usr/bin/env bash
# Top up a NewAPI user's quota directly in SQLite (admin API does not always persist).
#
# Usage:
#   SSH_TARGET=root@host SSH_KEY=~/.ssh/id_ed25519 ./topup.sh <user_id> <quota>
# Example: ./topup.sh 1 1000000000   # 1B quota = USD 2000 at QuotaPerUnit=500000

set -euo pipefail

: "${SSH_TARGET:?SSH_TARGET required}"
: "${SSH_KEY:=$HOME/.ssh/id_ed25519}"
: "${DB:=/root/newapi/data/one-api.db}"
: "${CONTAINER:=new-api}"

USER_ID="${1:?user_id required}"
QUOTA="${2:?quota integer required}"

ssh -i "$SSH_KEY" "$SSH_TARGET" "
  set -e
  sqlite3 '$DB' \"UPDATE users SET quota=$QUOTA WHERE id=$USER_ID;\"
  sqlite3 -header -column '$DB' \"SELECT id, username, quota, used_quota FROM users WHERE id=$USER_ID;\"
  docker restart '$CONTAINER' >/dev/null
  echo restarted '$CONTAINER'
"
