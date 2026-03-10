# Changelog

Use concise operational entries for workflow/system changes.

## Change Entry Template
### YYYY-MM-DD
- Changed:
  - 
- Why:
  - 
- Risk:
  - Low / Medium / High
- Rollback:
  - 

---

## 2026-02-19
- Changed:
  - Added missing starter docs for inventory/changelog/system/contracts/security.
- Why:
  - Complete baseline documentation set expected by README/checklists.
- Risk:
  - Low (documentation only).
- Rollback:
  - Revert this commit.

## 2026-03-07
- Changed:
  - Replaced template placeholders in system docs with transcript-to-proposal architecture for `n8n + Google Sheets + Gmail`.
  - Added Mermaid end-to-end flow in `SYSTEM_OVERVIEW`, lifecycle state machine in `RUNBOOK`, and contract lineage in `DATA_CONTRACTS`.
  - Added required PDF-based proposal section ordering contract for composer output.
  - Replaced `WORKFLOW_INVENTORY` example row with six concrete workflow entries to create for v1.
  - Added transcript input and expected extraction fixtures in `fixtures/` for deterministic testing.
  - Added six n8n workflow JSON blueprints in `workflows/active/` covering intake, extraction, research, composition, human QA/approval, and Gmail send/follow-up.
  - Updated `workflows/README.md` with import order and integration checkpoint guidance.
  - Fixed `scripts/sync-project-workflows.sh` compatibility by replacing `mapfile` usage with a Bash-3-safe read loop.
  - Added `docs/GOOGLE_SHEETS_SCHEMA.md` with required tabs, columns, statuses, and SLA fields.
  - Added v1 workflow-ID placeholder block in `scripts/workflow-allowlist.txt` for faster allowlist population.
  - Added `scripts/setup-google-sheet.py` to provision Google Sheet tabs/headers via service account.
  - Added `scripts/import-workflow-blueprints.py` to create n8n workflows from local blueprints and optionally update allowlist IDs.
  - Added `docs/BOOTSTRAP.md` and linked bootstrap flow from root `README.md`.
  - Created six v1 workflows in n8n via API and synced real workflow IDs/exports into `workflows/active/`.
  - Updated `docs/WORKFLOW_INVENTORY.md` and `scripts/workflow-allowlist.txt` with live workflow IDs.
  - Removed unused `secrets/n8n-api-key.txt`; n8n scripts use `.env` (`N8N_BASE_URL`, `N8N_API_KEY`) as credential source.
  - Replaced workflow placeholder nodes with live `Google Sheets` append nodes and `Gmail` send nodes across all six v1 workflows.
  - Activated all six workflows in n8n and re-synced live JSON exports into `workflows/active/`.
  - Provisioned required Google Sheet tabs/headers in spreadsheet `1SG_oFl8fFwQgZ-Q-MnaRCHrklVZLxJWz4M3UCX9pdUM`.
  - Added webhook-base troubleshooting guidance in bootstrap/runbook docs for deployments where API and webhook domains differ.
  - Aligned proposal section contract to uploaded template headings: `Executive Summary`, `Scope of Services`, `Strategy and Approach`, `Budget and Pricing`, `Terms and Conditions`.
  - Rebuilt Glossier fixtures using direct transcript extraction from `discovery_call_glossier.docx` and added expected composer output fixture.
  - Added Glossier-based pinned test data to all six `*-TBD_CREATE_IN_N8N.json` workflow blueprints for deterministic stage testing.
  - Documented n8n API limitation: workflow `PUT` rejects `pinData`, so live synced exports remain unpinned.
  - Updated `proposal-composer` code node in synced workflow JSON to match the attached template section order.
- Why:
  - Establish a concrete, human-QA-first operating model for faster proposal turnaround from transcript input.
- Risk:
  - Medium (new workflow blueprints added; TODO nodes must be replaced with credentialed integrations before production use).
- Rollback:
  - Revert workflow blueprint + documentation changes in this entry.

## 2026-03-09
- Changed:
  - Fixed production QA approval path by assigning explicit `webhookId` values to `Human QA Webhook` and `QA Approval Link Webhook` in `human-qa-and-approval`.
  - Updated QA approval button URL in `proposal-composer` HTML email to `https://webhooks.intellom8.com/webhook/qa-approval-action`.
  - Re-activated affected workflows and re-synced live exports.
  - Updated core docs to reflect as-built deterministic flow, execute-workflow chaining, and approval-link behavior.
- Why:
  - Approval links were returning `404 webhook not registered`, blocking one-click approve flow.
- Risk:
  - Medium (touches production webhook registration and review/send routing behavior).
- Rollback:
  - Restore prior synced workflow JSON for `proposal-composer` and `human-qa-and-approval`, then re-activate workflows.
