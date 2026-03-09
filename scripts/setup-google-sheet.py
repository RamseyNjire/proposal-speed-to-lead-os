#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


REQUIRED_TABS = {
    "Cases": [
        "case_id",
        "transcript_id",
        "client_name",
        "client_email",
        "website_url",
        "status",
        "ingested_at_utc",
        "draft_due_at_utc",
        "draft_ready_at_utc",
        "approved_at_utc",
        "sent_at_utc",
    ],
    "Extracted_Insights": [
        "case_id",
        "problem_summary",
        "goal_summary",
        "constraints_json",
        "key_metrics_json",
        "competitors_json",
        "updated_at_utc",
    ],
    "Research": [
        "case_id",
        "client_site_findings_json",
        "competitor_findings_json",
        "meta_ad_library_findings_json",
        "updated_at_utc",
    ],
    "Proposals": [
        "case_id",
        "proposal_subject",
        "proposal_body_markdown",
        "gmail_draft_id",
        "status",
        "updated_at_utc",
    ],
    "QA_Reviews": [
        "case_id",
        "qa_status",
        "reviewer",
        "review_notes",
        "reviewed_at_utc",
        "founder_status",
    ],
    "Activity_Log": [
        "case_id",
        "event_type",
        "status",
        "details",
        "created_at_utc",
    ],
}


def load_env(path: Path) -> dict:
    data = {}
    if not path.exists():
        return data
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip()
    return data


def extract_sheet_id(value: str) -> str:
    value = value.strip()
    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", value)
    if m:
        return m.group(1)
    return value


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create required tabs + headers for transcript-to-proposal project sheet."
    )
    parser.add_argument(
        "--spreadsheet",
        default="",
        help="Spreadsheet ID or URL. Defaults to GOOGLE_SHEETS_SPREADSHEET_ID from .env",
    )
    parser.add_argument(
        "--service-account",
        default="secrets/google-service-account.json",
        help="Path to service account JSON file",
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env file",
    )
    args = parser.parse_args()

    env = load_env(Path(args.env_file))
    spreadsheet_raw = args.spreadsheet or env.get("GOOGLE_SHEETS_SPREADSHEET_ID", "")
    if not spreadsheet_raw:
        fail("Spreadsheet ID/URL not provided and GOOGLE_SHEETS_SPREADSHEET_ID is empty.")

    spreadsheet_id = extract_sheet_id(spreadsheet_raw)
    sa_path = Path(args.service_account)
    if not sa_path.exists():
        fail(f"Service account file not found: {sa_path}")

    try:
        sa_data = json.loads(sa_path.read_text())
    except Exception as exc:
        fail(f"Invalid service account JSON: {exc}")

    if "replace_me" in json.dumps(sa_data).lower():
        fail(f"Service account file still has placeholder values: {sa_path}")

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(str(sa_path), scopes=scopes)

    try:
        service = build("sheets", "v4", credentials=creds)
        spreadsheet = (
            service.spreadsheets()
            .get(spreadsheetId=spreadsheet_id, fields="sheets.properties.title")
            .execute()
        )
    except HttpError as exc:
        fail(f"Unable to access spreadsheet {spreadsheet_id}: {exc}")

    existing = {s["properties"]["title"] for s in spreadsheet.get("sheets", [])}
    missing = [title for title in REQUIRED_TABS if title not in existing]

    if missing:
        requests = [{"addSheet": {"properties": {"title": title}}} for title in missing]
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body={"requests": requests}
        ).execute()
        print(f"Added tabs: {', '.join(missing)}")
    else:
        print("All required tabs already exist.")

    for tab, headers in REQUIRED_TABS.items():
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"'{tab}'!A1",
            valueInputOption="RAW",
            body={"values": [headers]},
        ).execute()

    freeze_requests = [
        {
            "updateSheetProperties": {
                "properties": {"title": tab, "gridProperties": {"frozenRowCount": 1}},
                "fields": "gridProperties.frozenRowCount",
            }
        }
        for tab in REQUIRED_TABS
    ]
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={"requests": freeze_requests}
    ).execute()

    print(f"Sheet provisioning complete for spreadsheet: {spreadsheet_id}")
    print("Tabs and header rows are ready.")


if __name__ == "__main__":
    main()
