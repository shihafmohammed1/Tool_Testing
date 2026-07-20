# Repository Structure

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
| **Profile** | `semgrep-bandit` |
| **Output directory** | `src/subject_volume` |
| **Language** | `python` |
| **Current volume LOC** | 50,339 |
| **Target met (50k)** | Yes |

Generated code lives in an **isolated** directory and does not replace golden
training subjects.

### Regenerate subject volume

```bash
python scripts/generate_subject_code.py --target-lines 50000
python scripts/count_subject_lines.py
```

From repo root:

```bash
python -m scripts.codegen.run_all_generators --profiles semgrep-bandit --target-lines 50000
```

## Shared codegen

Profiles and generators live under [`scripts/codegen/`](../../scripts/codegen/)
at the repo root. See [`docs/REPO_LAYOUT.md`](../../docs/REPO_LAYOUT.md).
