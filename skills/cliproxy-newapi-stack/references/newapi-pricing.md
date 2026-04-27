# NewAPI Pricing Semantics (calciumion/new-api v0.12.x)

NewAPI persists pricing as **deep-mergeable JSON blobs** in the `options` table (SQLite at
`/data/one-api.db`). Default values live in code; the persisted rows override on top.

## Three pricing keys

| Key | Type | Meaning |
|---|---|---|
| `ModelRatio` | `{model: float}` | Per-1M-token input price (USD), often divided by an internal scale on some forks. Verify with a probe request. |
| `CacheRatio` | `{model: float}` | **Multiplier on input price**. cached_input = input * CacheRatio. |
| `CompletionRatio` | `{model: float}` | **Multiplier on input price**. output = input * CompletionRatio. |
| `QuotaPerUnit` | `int` | Default `500000`. Means `1 USD = 500000 quota`. Used to convert model price to internal `quota` integer recorded in `logs.quota`. |
| `GroupRatio` / `group_ratio_setting.group_ratio` | `{group: float}` | Per-user-group multiplier. `default=1` typical. |

## Worked example

Target prices (USD per 1M tokens):
- input  `2.5`
- cached `0.25`  ← 0.1× of input
- output `15`    ← 6× of input

Write:
```json
"ModelRatio":      {"gpt-5.4": 2.5}
"CacheRatio":      {"gpt-5.4": 0.1}
"CompletionRatio": {"gpt-5.4": 6}
```

Probe with a real request and check `logs.quota`:
```sql
SELECT id, model_name, prompt_tokens, completion_tokens, quota
FROM logs ORDER BY id DESC LIMIT 3;
```
Compute expected `quota`:
```
expected = (prompt_tokens * input + completion_tokens * output) * (QuotaPerUnit / 1e6)
         = (prompt_tokens * 2.5  + completion_tokens * 15)    * 0.5
```
If observed roughly matches, mapping is correct. If observed is `~30×` higher, the fork uses an
**internal /2 scale** for ModelRatio — write `1.25` instead of `2.5` and re-probe.

## Pitfalls

- **CacheRatio is NOT a price** — writing `0.25` means cached = 0.25× input, not "cached costs 0.25 USD/1M".
- **CompletionRatio is NOT a price** — writing `15` means output = 15× input, ie a huge multiplier.
- **PUT via /api/option/ may silently no-op** on some installs. Direct SQLite write + container
  restart is the canonical fallback.
- **Defaults bleed through**: missing keys mean NewAPI uses its built-in default, which may be
  wildly wrong (e.g. `gpt-4`-class default applied to a `gpt-5.4` virtual model).
- **Scope to virtual models only**: CLIProxyAPI exposes virtual model names (e.g. `gpt-5.4`,
  `gpt-5.3-codex`). Do not write ratios for upstream raw names — they will not be billed.

## Restart requirement

After writing rows directly to SQLite, restart the container:
```
docker restart new-api
```
The merged in-memory map is rebuilt at startup.

## Related options

- `MinTopUp`, `StripeMinTopUp`, `StripeUnitPrice` — affect the user-facing top-up UI; do not
  change billing math.
- `general_setting.quota_display_type=USD` — only changes UI rendering; raw `quota` field stays
  integer in `logs`.
