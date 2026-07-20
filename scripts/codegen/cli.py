"""CLI entrypoint for subject-code generation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .base_generator import generate_python
from .js_generator import generate_javascript
from .profile_loader import REPO_ROOT, list_profile_ids, load_profile, tool_root


def generate_for_profile(profile_id: str, target_lines: int) -> int:
    profile = load_profile(profile_id)
    profile["_tool_root"] = str(tool_root(profile))
    language = profile.get("language", "python")
    if language == "javascript":
        total = generate_javascript(profile, target_lines)
    else:
        total = generate_python(profile, target_lines)
    out = tool_root(profile) / profile["output_dir"]
    print(f"[{profile_id}] Generated ~{total} lines under {out}")
    return total


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate subject volume code for a tool folder")
    parser.add_argument(
        "--profile",
        default=None,
        help="Profile id (json filename without extension). Auto-detected from tool folder if omitted.",
    )
    parser.add_argument("--target-lines", type=int, default=50000)
    parser.add_argument(
        "--tool-root",
        type=Path,
        default=None,
        help="Tool folder root (for per-tool wrapper scripts)",
    )
    args = parser.parse_args(argv)

    profile_id = args.profile
    if profile_id is None and args.tool_root is not None:
        marker = args.tool_root / ".codegen-profile"
        if marker.exists():
            profile_id = marker.read_text(encoding="utf-8").strip()
    if profile_id is None:
        parser.error("--profile is required when not run from a tool wrapper")

    generate_for_profile(profile_id, args.target_lines)


if __name__ == "__main__":
    main()
