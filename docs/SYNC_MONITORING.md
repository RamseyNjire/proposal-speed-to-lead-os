# Sync Monitoring

Use this pattern to monitor repo sync runs.

## Objective
For each sync run, capture:
- success/failure
- timestamp + duration
- run identifier
- brief error summary on failure

Also monitor workflow health events that can generate operator impact:
- repeated execution bursts for the same `case_id`
- webhook 404 errors for production webhook paths
- Gmail send spikes caused by looped branches

## Script side
`./scripts/run-sync.sh` can POST a JSON payload to:
- `SYNC_MONITOR_WEBHOOK_URL`
- optional bearer auth via `SYNC_MONITOR_AUTH_TOKEN`

## Suggested n8n monitor workflow
1. `Webhook` node (POST)
2. `Normalize` node (shape payload)
3. `Append row` to a `Sync_Ops` tab (or equivalent)
4. `IF status == failure` -> send alert email/chat
5. Optional: send success heartbeat email or sheet-only
6. Optional: dedupe failures by `(workflow_id, node_name, case_id)` in 10-minute windows

## Security
- Keep monitor tokens local only (never commit).
- Validate auth token in monitor workflow if used.

## Quick test
1. Set webhook vars in `.env`.
2. Run:
   ```bash
   ./scripts/run-sync.sh
   ```
3. Confirm one monitor execution in n8n.
4. Confirm one row in sync log destination.

## Extra production checks
1. Validate approval webhook path:
   - `GET https://webhooks.intellom8.com/webhook/qa-approval-action?action=approve&case_id=test`
2. Confirm response is not `404 webhook not registered`.
3. If it is `404`, verify `human-qa-and-approval` is active and webhook IDs are present.
