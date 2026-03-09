# Fixtures

Use these fixtures to validate transcript ingestion and extraction behavior before wiring live traffic.

- `transcript_ingest_payload.example.json`
  - Canonical input payload for `transcript-intake`.
- `discovery_brief.expected.json`
  - Expected normalized output from `insight-extractor`.
- `transcript_ingest_payload.glossier.json`
  - Transcript-ingest fixture based on `/Users/app/Downloads/discovery_call_glossier.docx`.
- `discovery_brief.expected.glossier.json`
  - Expected extraction output for the Glossier transcript fixture.
- `proposal_section_draft.expected.glossier.json`
  - Expected proposal section ordering/content for composer-stage validation.

## Validation expectations
- Same `case_id` must be preserved across all downstream workflows.
- Extracted metrics and constraints should match expected values exactly.
- Proposal composer must include required section ordering from `docs/SYSTEM_OVERVIEW.md`.
