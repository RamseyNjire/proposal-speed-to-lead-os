# Bootstrap Guide (Transcript -> Gmail v1)

Use this to bring up the project from scratch.

## 1) Fill local secrets
- `.env`
  - `N8N_BASE_URL` (real n8n URL)
  - `N8N_API_KEY` (real n8n API key)
  - `GOOGLE_SHEETS_SPREADSHEET_ID` (or pass URL/ID to setup script)
- `secrets/google-service-account.json`
  - Real Google service account JSON with Sheets API access

## 2) Provision Google Sheet tabs + headers
```bash
./scripts/setup-google-sheet.py
```

Optional (pass URL/ID directly):
```bash
./scripts/setup-google-sheet.py --spreadsheet "https://docs.google.com/spreadsheets/d/1SG_oFl8fFwQgZ-Q-MnaRCHrklVZLxJWz4M3UCX9pdUM/edit"
```

## 3) Create n8n workflows from blueprints
```bash
./scripts/import-workflow-blueprints.py --write-allowlist
```

This creates workflows from:
- `workflows/active/*-TBD_CREATE_IN_N8N.json`

And appends created workflow IDs to:
- `scripts/workflow-allowlist.txt`

## 4) Pull normalized workflow exports from n8n
```bash
./scripts/sync-project-workflows.sh
```

## 5) Run pre-push checks
```bash
./scripts/prepush-check.sh
```

## Runtime note
- If `POST /webhook/<path>` on `N8N_BASE_URL` returns 404, your deployment is likely using a different public webhook base URL than API base.
- In that case, use the webhook URL shown in each n8n Webhook node UI for trigger testing.
- For this project, QA button links use `https://webhooks.intellom8.com/webhook/qa-approval-action`.
- If QA links return `webhook not registered`, re-deploy and re-activate `human-qa-and-approval` and confirm non-null webhook IDs.
- n8n public API updates currently reject `pinData`; Glossier test `pinData` is stored in `workflows/active/*-TBD_CREATE_IN_N8N.json` plus `fixtures/*.glossier.json`.
