#!/usr/bin/env python3
"""Download SharePoint Excel via Microsoft Graph (device login)."""

from __future__ import annotations

import argparse
import base64
import sys
from dataclasses import dataclass
from pathlib import Path

import msal
import requests

DEFAULT_SHARE_URL = (
    "https://hopewellsolutions.sharepoint.com/:x:/s/Testable-ExecutionTeam/"
    "IQCzRy3rTrp7S6qtDgTt7weFAaOU4WltZoxASErJ7wTbhp4?e=hthT5g"
)
CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
AUTHORITY = "https://login.microsoftonline.com/organizations"
SCOPES = ["Files.Read.All", "User.Read"]
GRAPH_BASE = "https://graph.microsoft.com/v1.0"


@dataclass
class DriveItem:
    name: str
    web_url: str


def encode_share_url(share_url: str) -> str:
    encoded = base64.urlsafe_b64encode(share_url.encode("utf-8")).decode("utf-8").rstrip("=")
    return f"u!{encoded}"


def acquire_token() -> str:
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError(f"Device flow failed: {flow}")
    print(flow["message"])
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError(result.get("error_description", "Authentication failed"))
    return result["access_token"]


def resolve_share_item(token: str, share_url: str) -> DriveItem:
    share_id = encode_share_url(share_url)
    url = f"{GRAPH_BASE}/shares/{share_id}/driveItem"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=120)
    response.raise_for_status()
    payload = response.json()
    return DriveItem(name=payload.get("name", "workbook.xlsx"), web_url=payload.get("webUrl", share_url))


def download_workbook(share_url: str, dest: Path) -> tuple[DriveItem, Path]:
    token = acquire_token()
    item = resolve_share_item(token, share_url)
    share_id = encode_share_url(share_url)
    url = f"{GRAPH_BASE}/shares/{share_id}/driveItem/content"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=300)
    response.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(response.content)
    return item, dest


def main() -> None:
    parser = argparse.ArgumentParser(description="Download SharePoint workbook")
    parser.add_argument("--share-url", default=DEFAULT_SHARE_URL)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "data" / "sharepoint_audit_workbook.xlsx",
    )
    args = parser.parse_args()
    item, path = download_workbook(args.share_url, args.output)
    print(f"Downloaded: {item.name}")
    print(f"Saved to: {path}")
    print(f"SharePoint: {item.web_url}")


if __name__ == "__main__":
    main()
