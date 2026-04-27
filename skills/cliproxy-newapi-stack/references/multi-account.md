# Multi-Account Operations (CLIProxyAPI)

CLIProxyAPI auto-rotates across all credential JSON files in `auth-dir`. Adding accounts is
**file-system level** — no code, no restart.

## Add a new OAuth account

Use `scripts/add_codex_account.sh` (provider configurable) or do it manually:

1. **Local OAuth** (browser must be on the local machine):
   ```bash
   cd <CLIProxyAPI-local-clone>
   go run ./cmd/server -<provider>-login -config config.yaml
   ```
   - For each provider use the matching flag:
     `-codex-login` `-claude-login` `-qwen-login` `-iflow-login` `-antigravity-login` `-login`(Gemini)
   - **Critical**: log out of any previous account in the browser first, or use an incognito
     window — otherwise OAuth will silently re-bind to the existing session and overwrite the
     same credential file.

2. **Capture filename**:
   ```bash
   ls -lt ~/.cli-proxy-api/<provider>-*.json | head
   ```
   New file is named `<provider>-<email>-[ts].json`.

3. **Sync to VPS**:
   ```bash
   scp -i <KEY> ~/.cli-proxy-api/<file> root@<HOST>:/root/.cli-proxy-api/
   ```

4. **Watcher hot-loads it** — log lines:
   ```
   auth file changed (CREATE): <file>, processing incrementally
   auth file changed (WRITE):  <file>, processing incrementally
   ```
   No service restart needed.

## How load-balancing actually works

- Selector ranks accounts by availability + freshness; **does not** keep a strict round-robin.
- A single account can serve many requests in a row if others are cooled / unavailable.
- 429 / quota exhaustion marks an account temporarily unavailable; selector switches to peer.
- Routing distribution is therefore *load-aware*, not *fair-share*.

## Verify both accounts are recognized

After adding, scan the log:
```bash
grep -oE 'codex-[A-Za-z0-9._@+-]+\.json' /root/CLIProxyAPI/cli-proxy-api.log \
  | sort | uniq -c
```
You may see only the new account during the first batch — that means the older account is
under-quota or cooling. Force the older one to fire by waiting (cooldown expiry) or running
many requests; both should appear over time.

## Remove an account

1. `rm /root/.cli-proxy-api/<provider>-<email>.json`
2. Watcher logs `auth file changed (REMOVE): ...`
3. The selector drops it from the rotation immediately.

## Subscription required

OAuth login success ≠ usable. The account must hold a valid subscription:
- Codex / GPT-5 family → ChatGPT **Plus** or **Pro**
- Claude `claude-*` → Claude **Pro** or **Max** (depending on model tier)
- Gemini → corresponding Google AI Pro tier

Without subscription, OAuth completes and tokens save, but `/v1/chat/completions` returns 401 /
402. Always probe with one real request after sync.
