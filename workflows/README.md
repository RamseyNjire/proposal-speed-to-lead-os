# Workflows

- `active/`: current workflows in use
- `archive/`: old or superseded workflow exports

After editing a workflow in n8n, export JSON back into `active/` and commit it.

## v1 Transcript -> Gmail blueprints
The following blueprint files are scaffolded in `active/`:

1. `transcript-intake-TBD_CREATE_IN_N8N.json`
2. `insight-extractor-TBD_CREATE_IN_N8N.json`
3. `research-enricher-TBD_CREATE_IN_N8N.json`
4. `proposal-composer-TBD_CREATE_IN_N8N.json`
5. `human-qa-and-approval-TBD_CREATE_IN_N8N.json`
6. `gmail-send-and-followup-TBD_CREATE_IN_N8N.json`

## Live synced exports
The repository also stores live workflow exports with concrete IDs:
- `transcript-intake-H0x0TpT3WfPZxELo.json`
- `insight-extractor-56QURVglZdEYUyxQ.json`
- `research-enricher-Edwfev3WfHY72DP7.json`
- `proposal-composer-fdGPPZlrGjwCkWH8.json`
- `human-qa-and-approval-w1FE4HWHsATg3hfr.json`
- `gmail-send-and-followup-x3SEMzP1S94toYGp.json`

## Import order (fresh environment)
Import in this order so downstream execute-workflow dependencies already exist:

1. `gmail-send-and-followup`
2. `human-qa-and-approval`
3. `proposal-composer`
4. `research-enricher`
5. `insight-extractor`
6. `transcript-intake`

## Sync rule
After any n8n UI change:
1. Activate workflows as needed.
2. Run `./scripts/sync-project-workflows.sh`.
3. Commit updated JSON exports and corresponding doc updates in the same PR.
