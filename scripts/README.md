# Scripts

Project automation scripts for workflow sync, validation, and bootstrap.

## Included scripts
- `scripts/sync-project-workflows.sh`
  - Pulls workflow JSON by ID allowlist into `workflows/active/`.
- `scripts/prepush-check.sh`
  - API sanity check + workflow scope check + secret pattern scan.
- `scripts/run-sync.sh`
  - Wrapper to run sync + checks and post success/failure to monitoring webhook.
- `scripts/install-git-hooks.sh`
  - Sets `core.hooksPath=.githooks`.
- `scripts/setup-google-sheet.py`
  - Creates required tabs + header columns in the project Google Sheet.
- `scripts/import-workflow-blueprints.py`
  - Creates n8n workflows from local `*-TBD_CREATE_IN_N8N.json` blueprints.

## Setup
1. Fill `.env` from `.env.example`.
2. Add workflow IDs to `scripts/workflow-allowlist.txt`.
3. Install hooks:
   ```bash
   ./scripts/install-git-hooks.sh
   ```

## Typical usage
```bash
./scripts/sync-project-workflows.sh
./scripts/prepush-check.sh
./scripts/run-sync.sh
./scripts/setup-google-sheet.py
```

Create workflows from blueprints (and append created IDs to allowlist):
```bash
./scripts/import-workflow-blueprints.py --write-allowlist
```

## Notes
- Keep scripts idempotent and safe by default.
- Keep allowlist strict to avoid importing unrelated workflows.
- `sync-project-workflows.sh` is Bash-3 compatible (no `mapfile` dependency).
