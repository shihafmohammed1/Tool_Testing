#!/usr/bin/env python3
"""Download SharePoint audit workbook, fill audit data, and upload back."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from sharepoint_graph import DEFAULT_SHARE_URL, download_workbook

SCRIPTS_DIR = Path(__file__).resolve().parent
CACHE_DIR = SCRIPTS_DIR / "data"
DOWNLOAD_PATH = CACHE_DIR / "sharepoint_audit_workbook.xlsx"
GENERATOR = SCRIPTS_DIR / "generate_whitebox_audit_excel.py"


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync White Box audit data to SharePoint Excel")
    parser.add_argument("--share-url", default=DEFAULT_SHARE_URL, help="SharePoint sharing URL")
    parser.add_argument("--download-only", action="store_true", help="Only download workbook for inspection")
    parser.add_argument("--fill-local", action="store_true", help="Fill downloaded copy without uploading")
    parser.add_argument("--force", action="store_true", help="Overwrite manual columns like ETA")
    args = parser.parse_args()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1/3: Downloading SharePoint workbook (device login if needed)...")
    item, path = download_workbook(args.share_url, DOWNLOAD_PATH)
    print(f"  Downloaded: {item.name}")
    print(f"  Local copy: {path}")
    print(f"  SharePoint: {item.web_url}")

    if args.download_only:
        print("Download-only mode complete.")
        return

    print("Step 2/3: Filling audit data into existing sheet layout...")
    fill_cmd = [
        sys.executable,
        str(GENERATOR),
        "--input",
        str(path),
        "--output",
        str(path),
        "--team-sheet",
    ]
    if args.force:
        fill_cmd.append("--no-preserve-manual")
    subprocess.run(fill_cmd, check=True)

    if args.fill_local:
        print(f"Fill-local mode complete. Updated file: {path}")
        print("Upload this file to SharePoint and share with Edit access for teammates.")
        print(f"  SharePoint: {args.share_url}")
        return

    print("Upload the updated file to SharePoint manually, then share with teammates (Edit access).")
    print(f"  Local file: {path}")
    print(f"  SharePoint: {args.share_url}")


if __name__ == "__main__":
    main()
