"""Count executable Python source lines excluding tests and generated artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".venv",
    "venv",
    "env",
    "tests",
    "reports",
    "scripts",
    "build",
    "dist",
    "__pycache__",
    ".git",
    ".testmon",
}

EXCLUDE_FILES = {
    "setup.py",
}


def is_excluded(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    return path.name in EXCLUDE_FILES


def count_lines(root: Path) -> tuple[int, int, list[tuple[str, int]]]:
    total = 0
    files = 0
    per_file: list[tuple[str, int]] = []
    for path in sorted(root.rglob("*.py")):
        if is_excluded(path):
            continue
        rel = path.relative_to(root).as_posix()
        if not rel.startswith("src/"):
            continue
        lines = len(path.read_text(encoding="utf-8").splitlines())
        total += lines
        files += 1
        per_file.append((rel, lines))
    return total, files, per_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    total, files, per_file = count_lines(args.root)
    print(f"Source files: {files}")
    print(f"Source lines: {total}")
    if args.verbose:
        for rel, lines in per_file:
            print(f"  {rel}: {lines}")


if __name__ == "__main__":
    main()
