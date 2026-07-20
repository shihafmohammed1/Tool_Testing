"""Load generation profiles and resolve tool folder paths."""

from __future__ import annotations

import json
from pathlib import Path

PROFILES_DIR = Path(__file__).resolve().parent / "profiles"
REPO_ROOT = Path(__file__).resolve().parents[2]

TOOL_FOLDER_BY_ID: dict[str, str] = {
    "coverage-py": "coverage .py",
    "coverage-beniget": "coverage + beniget .py",
    "pip-audit": "Pip Audit.py",
    "semgrep-bandit": "semgrep .py",
    "pymcdc": "pymcdc.py",
    "randon-lizard": "randon-lizard",
    "git-churn": "Git_Churn",
    "cosmic-ray": "cosmic-ray",
    "jscpd": "JSCPD",
    "crosshair": "crosshair",
    "beniget": "Beniget",
    "coverage-py-stub": "Coverage.py",
}

SKIP_GENERATION = {"pylint", "testmon", "cognitive-ast"}


def list_profile_ids() -> list[str]:
    return sorted(p.stem for p in PROFILES_DIR.glob("*.json"))


def load_profile(profile_id: str) -> dict:
    path = PROFILES_DIR / f"{profile_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Profile not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def tool_root(profile: dict) -> Path:
    folder = profile.get("tool_folder") or TOOL_FOLDER_BY_ID[profile["tool_id"]]
    return REPO_ROOT / folder


def output_path(profile: dict) -> Path:
    return tool_root(profile) / profile["output_dir"]
