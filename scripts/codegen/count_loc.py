"""Count lines of code in tool folders."""

from __future__ import annotations

import argparse
from pathlib import Path

from .profile_loader import REPO_ROOT, TOOL_FOLDER_BY_ID, list_profile_ids, load_profile, tool_root

CODE_EXTENSIONS = {
    "python": {".py"},
    "javascript": {".js", ".jsx", ".ts", ".tsx"},
}


def count_lines(path: Path, extensions: set[str]) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    total_lines = 0
    file_count = 0
    for file in path.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix.lower() not in extensions:
            continue
        if any(part in {".git", "__pycache__", "node_modules", ".venv"} for part in file.parts):
            continue
        total_lines += len(file.read_text(encoding="utf-8", errors="ignore").splitlines())
        file_count += 1
    return total_lines, file_count


def report_tool(profile_id: str) -> dict:
    profile = load_profile(profile_id)
    root = tool_root(profile)
    language = profile.get("language", "python")
    extensions = CODE_EXTENSIONS.get(language, CODE_EXTENSIONS["python"])
    volume_dir = root / profile["output_dir"]
    volume_lines, volume_files = count_lines(volume_dir, extensions)
    total_lines, total_files = count_lines(root, extensions)
    return {
        "profile": profile_id,
        "folder": root.name,
        "volume_lines": volume_lines,
        "volume_files": volume_files,
        "total_lines": total_lines,
        "total_files": total_files,
        "target_met": volume_lines >= 50000,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Count LOC in tool subject_volume directories")
    parser.add_argument("--profiles", nargs="*", default=None, help="Profile ids (default: all)")
    args = parser.parse_args()
    profile_ids = args.profiles or list_profile_ids()
    print(f"{'Profile':<22} {'Folder':<26} {'Volume LOC':>10} {'Total LOC':>10} {'50k':>5}")
    print("-" * 78)
    for profile_id in profile_ids:
        row = report_tool(profile_id)
        flag = "YES" if row["target_met"] else "no"
        print(
            f"{row['profile']:<22} {row['folder']:<26} {row['volume_lines']:>10,} "
            f"{row['total_lines']:>10,} {flag:>5}"
        )


if __name__ == "__main__":
    main()
