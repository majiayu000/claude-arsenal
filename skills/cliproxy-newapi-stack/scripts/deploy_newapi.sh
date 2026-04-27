#!/usr/bin/env bash
# Deploy NewAPI (calciumion/new-api) Docker container on a Linux VPS.
#
# Usage:
#   SSH_TARGET=root@1.2.3.4 SSH_KEY=~/.ssh/id_ed25519 PORT=8200 ./deploy_newapi.sh
#
# Idempotent: safe to re-run. Pulls latest image, recreates container if exists.

set -euo pipefail

: "${SSH_TARGET:?SSH_TARGET required (e.g. root@1.2.3.4)}"
: "${SSH_KEY:=$HOME/.ssh/id_ed25519}"
: "${PORT:=8200}"
: "${DATA_DIR:=/root/newapi/data}"
: "${LOGS_DIR:=/root/newapi/logs}"
: "${IMAGE:=calciumion/new-api:latest}"
: "${TZ_VAL:=Asia/Shanghai}"

ssh -i "$SSH_KEY" "$SSH_TARGET" "
  set -e
  command -v docker >/dev/null || { apt-get update && apt-get install -y docker.io; }
  systemctl enable --now docker
  mkdir -p '$DATA_DIR' '$LOGS_DIR'
  docker pull '$IMAGE'
  docker rm -f new-api 2>/dev/null || true
  docker run -d --name new-api --restart unless-stopped \
    -p '$PORT':3000 \
    -e TZ='$TZ_VAL' \
    -v '$DATA_DIR':/data \
    -v '$LOGS_DIR':/app/logs \
    '$IMAGE'
  for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 2
    if curl -fsS -o /dev/null http://127.0.0.1:'$PORT'/api/setup; then
      echo NewAPI ready on port $PORT
      exit 0
    fi
  done
  echo NewAPI did not become ready, recent logs: >&2
  docker logs --tail 50 new-api >&2
  exit 1
"
