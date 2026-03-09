#!/usr/bin/env python3
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

import requests


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


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "workflow"


def api_request(base_url: str, api_key: str, method: str, path: str, body=None):
    url = base_url.rstrip("/") + path
    headers = {
        "X-N8N-API-KEY": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    resp = requests.request(method, url, headers=headers, json=body, timeout=60)
    if resp.status_code >= 400:
        raise RuntimeError(f"{method} {path} failed ({resp.status_code}): {resp.text[:500]}")
    if not resp.text.strip():
        return {}
    return resp.json()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create n8n workflows from local blueprint JSON files."
    )
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--pattern", default="workflows/active/*-TBD_CREATE_IN_N8N.json")
    parser.add_argument("--write-allowlist", action="store_true")
    parser.add_argument("--allowlist-file", default="scripts/workflow-allowlist.txt")
    args = parser.parse_args()

    env = load_env(Path(args.env_file))
    base_url = env.get("N8N_BASE_URL", "")
    api_key = env.get("N8N_API_KEY", "")

    if not base_url or "your-n8n-domain.example.com" in base_url:
        fail("N8N_BASE_URL missing or placeholder in .env")
    if not api_key or "replace_me" in api_key.lower():
        fail("N8N_API_KEY missing or placeholder in .env")

    files = sorted(glob.glob(args.pattern))
    if not files:
        fail(f"No blueprint files match pattern: {args.pattern}")

    listed = api_request(base_url, api_key, "GET", "/api/v1/workflows?limit=250")
    existing = {}
    for wf in listed.get("data", []):
        name = wf.get("name")
        wid = wf.get("id")
        if name and wid:
            existing[name] = str(wid)

    created = []
    skipped = []

    for wf_path in files:
        data = json.loads(Path(wf_path).read_text())
        name = data.get("name")
        if not name:
            raise RuntimeError(f"Missing workflow name in {wf_path}")

        if name in existing:
            skipped.append((name, existing[name]))
            continue

        payload = {
            "name": name,
            "nodes": data.get("nodes", []),
            "connections": data.get("connections", {}),
            "settings": data.get("settings", {}),
        }

        created_wf = api_request(base_url, api_key, "POST", "/api/v1/workflows", payload)
        wf_id = str(created_wf.get("id"))
        if not wf_id:
            raise RuntimeError(f"Create workflow succeeded but no id returned for {name}")

        out_name = f"{slugify(name)}-{wf_id}.json"
        out_path = Path("workflows/active") / out_name
        out_path.write_text(json.dumps(created_wf, indent=2) + "\n")
        created.append((name, wf_id, str(out_path)))

    if args.write_allowlist and created:
        allowlist = Path(args.allowlist_file)
        if not allowlist.exists():
            fail(f"Allowlist file not found: {allowlist}")
        existing_ids = {
            line.strip()
            for line in allowlist.read_text().splitlines()
            if line.strip() and not line.strip().startswith("#")
        }
        new_ids = [wid for _, wid, _ in created if wid not in existing_ids]
        if new_ids:
            with allowlist.open("a", encoding="utf-8") as f:
                for wid in new_ids:
                    f.write(f"{wid}\n")

    print("Created workflows:")
    for name, wf_id, out_path in created:
        print(f"- {name}: {wf_id} -> {out_path}")

    print("Skipped existing workflows:")
    for name, wf_id in skipped:
        print(f"- {name}: {wf_id}")

    if not created:
        print("No new workflows were created.")


if __name__ == "__main__":
    main()
