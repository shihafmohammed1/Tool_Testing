"""Run LOC count, isolation check, and optional tool validations."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from .count_loc import report_tool
from .profile_loader import list_profile_ids
from .validate_isolation import validate_profile

REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate all generated subject volumes")
    parser.add_argument("--profiles", nargs="*", default=None)
    parser.add_argument("--dry-run", action="store_true", help="LOC + isolation only")
    args = parser.parse_args()
    profile_ids = args.profiles or list_profile_ids()
    below = []
    isolation_failures = []
    for profile_id in profile_ids:
        row = report_tool(profile_id)
        if not row["target_met"]:
            below.append(profile_id)
        changed = validate_profile(profile_id)
        if changed:
            isolation_failures.append(profile_id)
    print("=== LOC ===")
    for profile_id in profile_ids:
        row = report_tool(profile_id)
        print(f"{profile_id}: {row['volume_lines']:,} volume lines")
    if below:
        print(f"\nBelow 50k: {', '.join(below)}")
    if isolation_failures:
        print(f"Isolation failures: {', '.join(isolation_failures)}")
        raise SystemExit(1)
    print("\nAll profiles passed isolation check.")
    if args.dry_run:
        return
    print("(Per-tool 100/100 gates should be run manually in each folder.)")


if __name__ == "__main__":
    main()
