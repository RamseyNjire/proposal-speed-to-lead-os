# Google Sheets Schema (v1)

This project uses one spreadsheet as the operational datastore for transcript-to-proposal flow.

## Required Tabs
1. `Cases`
2. `Extracted_Insights`
3. `Research`
4. `Proposals`
5. `QA_Reviews`
6. `Activity_Log`

## Cases
- `case_id` (string, primary key)
- `transcript_id` (string)
- `client_name` (string)
- `client_email` (string)
- `website_url` (string)
- `status` (enum)
- `ingested_at_utc` (ISO-8601)
- `draft_due_at_utc` (ISO-8601)
- `draft_ready_at_utc` (ISO-8601, nullable)
- `approved_at_utc` (ISO-8601, nullable)
- `sent_at_utc` (ISO-8601, nullable)

## Extracted_Insights
- `case_id` (string, foreign key to Cases)
- `problem_summary` (string)
- `goal_summary` (string)
- `constraints_json` (stringified JSON array)
- `key_metrics_json` (stringified JSON object)
- `competitors_json` (stringified JSON array)
- `updated_at_utc` (ISO-8601)

## Research
- `case_id` (string, foreign key)
- `client_site_findings_json` (stringified JSON array)
- `competitor_findings_json` (stringified JSON array)
- `meta_ad_library_findings_json` (stringified JSON array)
- `updated_at_utc` (ISO-8601)

## Proposals
- `case_id` (string, foreign key)
- `proposal_subject` (string)
- `proposal_body_markdown` (string)
- `gmail_draft_id` (string, nullable)
- `status` (enum)
- `updated_at_utc` (ISO-8601)

## QA_Reviews
- `case_id` (string, foreign key)
- `qa_status` (enum: `APPROVED` | `REVISION_REQUESTED` | `PENDING`)
- `reviewer` (string)
- `review_notes` (string)
- `reviewed_at_utc` (ISO-8601)
- `founder_status` (enum: `APPROVED` | `REVISION_REQUESTED` | `PENDING`)

## Activity_Log
- `case_id` (string, foreign key)
- `event_type` (string)
- `status` (string)
- `details` (string)
- `created_at_utc` (ISO-8601)

## Status Enum (canonical)
- `NEW`
- `EXTRACTION_IN_PROGRESS`
- `RESEARCH_IN_PROGRESS`
- `DRAFT_READY`
- `QA_IN_REVIEW`
- `REVISION_REQUESTED`
- `APPROVAL_PENDING`
- `APPROVED`
- `SENT`
- `FOLLOWUP_DUE`

## SLA Rules
- Warning at 2 hours from `ingested_at_utc`
- Critical at 3.5 hours from `ingested_at_utc`
- Breach at 4 hours from `ingested_at_utc`
