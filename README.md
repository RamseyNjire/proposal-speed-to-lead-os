# Proposal Speed-to-Lead OS

Transcript-to-proposal automation system built with `n8n + Google Sheets + Gmail` and human approval gates.

## What this does
1. Accepts a transcript payload at webhook intake.
2. Extracts a discovery brief.
3. Builds a research dossier.
4. Composes a deterministic proposal draft.
5. Sends QA HTML email with approve/revision actions.
6. Sends client proposal only when approval status is `APPROVED`.
7. Logs lifecycle and activity in Google Sheets.

## Core principles
1. Sync-first: repo JSON mirrors live n8n workflows.
2. PR-first: no direct `main` pushes.
3. Docs-with-code: update docs in same PR as behavior changes.
4. Human-gated send: QA/founder control before client delivery.

## Quick start
1. Copy `.env.example` to `.env` and fill `N8N_BASE_URL`, `N8N_API_KEY`, `GOOGLE_SHEETS_SPREADSHEET_ID`.
2. Add Google service account JSON to `secrets/google-service-account.json`.
3. Provision sheet tabs/headers:
   ```bash
   ./scripts/setup-google-sheet.py
   ```
4. Sync workflows from n8n:
   ```bash
   ./scripts/sync-project-workflows.sh
   ```
5. Run checks:
   ```bash
   ./scripts/prepush-check.sh
   ```

## Key docs
- [System Overview](/Users/app/Documents/proposal-speed-to-lead-os/docs/SYSTEM_OVERVIEW.md)
- [Workflow Inventory](/Users/app/Documents/proposal-speed-to-lead-os/docs/WORKFLOW_INVENTORY.md)
- [Runbook](/Users/app/Documents/proposal-speed-to-lead-os/docs/RUNBOOK.md)
- [Data Contracts](/Users/app/Documents/proposal-speed-to-lead-os/docs/DATA_CONTRACTS.md)
- [Google Sheets Schema](/Users/app/Documents/proposal-speed-to-lead-os/docs/GOOGLE_SHEETS_SCHEMA.md)
- [Bootstrap Guide](/Users/app/Documents/proposal-speed-to-lead-os/docs/BOOTSTRAP.md)

## Repo layout
- `docs/`: architecture, operations, contracts.
- `workflows/active/`: live synced exports + blueprint JSONs.
- `scripts/`: sync/check/provision scripts.
- `fixtures/`: deterministic test payloads/expected outputs.
- `secrets/`: local-only secret files (gitignored).
