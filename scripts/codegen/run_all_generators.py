"""Run subject-code generation for all sub-50k tool profiles."""

from __future__ import annotations

import argparse

from .cli import generate_for_profile
from .count_loc import report_tool
from .profile_loader import list_profile_ids


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate subject volume for all tool profiles")
    parser.add_argument("--target-lines", type=int, default=50000)
    parser.add_argument("--profiles", nargs="*", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    profile_ids = args.profiles or list_profile_ids()
    for profile_id in profile_ids:
        if args.dry_run:
            row = report_tool(profile_id)
            print(f"DRY RUN {profile_id}: volume={row['volume_lines']:,} target={args.target_lines:,}")
            continue
        generate_for_profile(profile_id, args.target_lines)
    if not args.dry_run:
        print("\nLOC summary:")
        for profile_id in profile_ids:
            row = report_tool(profile_id)
            status = "OK" if row["target_met"] else "BELOW TARGET"
            print(f"  {profile_id}: {row['volume_lines']:,} lines [{status}]")


if __name__ == "__main__":
    main()
