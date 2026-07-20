"""Write docs/STRUCTURE.md for each tool profile."""

from __future__ import annotations

from pathlib import Path

from .count_loc import report_tool
from .profile_loader import list_profile_ids, load_profile, tool_root

STRUCTURE_TEMPLATE = """# Repository Structure

This document describes how subject code, golden artifacts, and generated volume
are organized in this tool folder.

## Preserved golden paths (do not modify)

These paths support **100/100** platform validation and must remain unchanged when
regenerating subject volume:

- `sample_subject/` — curated training subject (where present)
- `platform/` — platform-facing metric JSON bundle (where present)
- Root metrics JSON (`metrics.json`, `platform_metrics.json`, tool-specific outputs)
- Tool-specific curated modules (e.g. mutation demo code, prod/test pairs)

## Subject volume (~50,000 LOC)

| Field | Value |
|-------|-------|
| **Profile** | `{profile_id}` |
| **Output directory** | `{output_dir}` |
| **Language** | `{language}` |
| **Current volume LOC** | {volume_lines:,} |
| **Target met (50k)** | {target_met} |

Generated code lives in an **isolated** directory and does not replace golden
training subjects.

### Regenerate subject volume

```bash
python scripts/generate_subject_code.py --target-lines 50000
python scripts/count_subject_lines.py
```

From repo root:

```bash
python -m scripts.codegen.run_all_generators --profiles {profile_id} --target-lines 50000
```

## Shared codegen

Profiles and generators live under [`scripts/codegen/`](../../scripts/codegen/)
at the repo root. See [`docs/REPO_LAYOUT.md`](../../docs/REPO_LAYOUT.md).
"""


def write_structure_doc(profile_id: str) -> Path:
    profile = load_profile(profile_id)
    root = tool_root(profile)
    docs_dir = root / "docs"
    docs_dir.mkdir(exist_ok=True)
    row = report_tool(profile_id)
    content = STRUCTURE_TEMPLATE.format(
        profile_id=profile_id,
        output_dir=profile["output_dir"],
        language=profile.get("language", "python"),
        volume_lines=row["volume_lines"],
        target_met="Yes" if row["target_met"] else "No",
    )
    path = docs_dir / "STRUCTURE.md"
    path.write_text(content, encoding="utf-8")
    return path


def main() -> None:
    for profile_id in list_profile_ids():
        path = write_structure_doc(profile_id)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
