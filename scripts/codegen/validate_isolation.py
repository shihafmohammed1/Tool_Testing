"""Verify golden paths were not modified during generation."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from .profile_loader import REPO_ROOT, list_profile_ids, load_profile, tool_root

PROTECTED_SUFFIXES = (
    "platform_metrics.json",
    "metrics.json",
    "dashboard_metrics.json",
)

PROTECTED_DIRS = (
    "platform",
    "fixtures",
    "sample_subject",
    "artifacts/training",
)


def git_diff_paths(repo_root: Path, rel_paths: list[str]) -> list[str]:
    if not (repo_root / ".git").exists():
        return []
    cmd = ["git", "diff", "--name-only", "--", *rel_paths]
    result = subprocess.run(
        cmd,
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def protected_paths(profile_id: str) -> list[str]:
    profile = load_profile(profile_id)
    root = tool_root(profile)
    rel_root = root.relative_to(REPO_ROOT).as_posix()
    paths = [f"{rel_root}/sample_subject"]
    for name in PROTECTED_DIRS:
        paths.append(f"{rel_root}/{name}")
    if profile_id == "cosmic-ray":
        paths.append(f"{rel_root}/src/testable_demo")
    if profile_id == "git-churn":
        paths.append(f"{rel_root}/src/metrics")
        paths.append(f"{rel_root}/src/models.py")
        paths.append(f"{rel_root}/src/repo_loader.py")
    for suffix in PROTECTED_SUFFIXES:
        paths.append(f"{rel_root}/{suffix}")
    return paths


def validate_profile(profile_id: str) -> list[str]:
    changed = git_diff_paths(REPO_ROOT, protected_paths(profile_id))
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate golden paths unchanged after generation")
    parser.add_argument("--profiles", nargs="*", default=None)
    args = parser.parse_args()
    profile_ids = args.profiles or list_profile_ids()
    failures = []
    for profile_id in profile_ids:
        changed = validate_profile(profile_id)
        if changed:
            failures.append((profile_id, changed))
            print(f"FAIL {profile_id}: {len(changed)} protected path(s) changed")
            for path in changed[:5]:
                print(f"  - {path}")
        else:
            print(f"OK   {profile_id}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
