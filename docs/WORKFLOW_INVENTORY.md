# Workflow Inventory

Track every workflow in scope for this project.

| Workflow Name | Workflow ID | Purpose | Trigger Type | Schedule/Timing | Inputs | Outputs | Dependencies | Notes |
|---|---|---|---|---|---|---|---|---|
| transcript-intake | H0x0TpT3WfPZxELo | Validates transcript payload, generates `case_id`, sets due time and fixed reviewer/approver emails | Webhook `POST /webhook/transcript-intake` | on incoming transcript | transcript ingest payload | `Cases` append row + normalized case payload | n8n webhook, Google Sheets | Branches to Sheets append and `insight-extractor` execute-workflow |
| insight-extractor | 56QURVglZdEYUyxQ | Builds deterministic discovery brief from transcript text | Execute Workflow Trigger + Webhook `POST /webhook/insight-extractor` | immediately after intake | normalized case payload | `DiscoveryBrief` + `Extracted_Insights` append row | n8n code node, Google Sheets | Branches to Sheets append and `research-enricher` execute-workflow |
| research-enricher | Edwfev3WfHY72DP7 | Produces deterministic research dossier stubs from available context | Execute Workflow Trigger + Webhook `POST /webhook/research-enricher` | immediately after extraction | `DiscoveryBrief` payload | `ResearchDossier` + `Research` append row | n8n code node, Google Sheets | Branches to Sheets append and `proposal-composer` execute-workflow |
| proposal-composer | fdGPPZlrGjwCkWH8 | Composes deterministic 5-section proposal and sends QA HTML review email | Execute Workflow Trigger + Webhook `POST /webhook/proposal-composer` | immediately after research | discovery + research payload | proposal body, `Proposals` append row, QA email | n8n code node, Gmail, Google Sheets | Sends QA email to `ramsey@intellom8.com` with approve link |
| human-qa-and-approval | w1FE4HWHsATg3hfr | Normalizes QA/founder decision, routes revise loop or approved send path | Execute Workflow Trigger + Webhook `POST /webhook/human-qa-and-approval` + Webhook `GET /webhook/qa-approval-action` | after composer email action or workflow call | proposal payload + action params | `QA_Reviews` append row or callback to composer/send | n8n if/code nodes, Google Sheets | `qa-approval-action` webhook IDs are required for production registration |
| gmail-send-and-followup | x3SEMzP1S94toYGp | Enforces approved-only sends and logs final activity | Execute Workflow Trigger + Webhook `POST /webhook/gmail-send-and-followup` | after approval | approved payload with `client_email` | Gmail send + `Activity_Log` append row | n8n guard code, Gmail, Google Sheets | Hard guard throws if `founder_status != APPROVED` |

## Rules
- Keep this file updated whenever a workflow is added, renamed, deleted, or re-scoped.
- Include exact workflow IDs from n8n.
- Keep schedule and trigger details explicit (with timezone where relevant).
- Keep webhook paths and trigger methods aligned with live workflow exports.
