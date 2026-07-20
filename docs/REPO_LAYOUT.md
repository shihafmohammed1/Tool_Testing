# Testable White Box Repo Layout

Branch **`Python_1.1`** holds Python tool golden-reference folders. Each folder validates
White Box metrics at **100/100** using curated subjects, platform JSON, and verify scripts.

## Tool folder categories

| Category | Folders | Subject LOC |
|----------|---------|-------------|
| **Generated volume (shared codegen)** | 12 folders below 50k — see profiles | ~50,000 each in `src/subject_volume/` |
| **Already at scale** | `pylint/`, `TESTMON/` | ~55k / ~52k in existing `src/` |
| **Upstream fork (skip generation)** | `Cognitive-AST/` | ~93k (FastAPI) |

## Standard layout (platform-style tools)

```text
<tool>/
├── README.md
├── TESTING_TEAM.md              # or docs/TESTING_TEAM_GUIDE.md
├── sample_subject/              # preserved 100/100 training subject
├── src/subject_volume/          # NEW ~50k generated volume (isolated)
├── platform/                    # preserved platform JSON
├── config/
├── scripts/
│   ├── generate_subject_code.py # thin wrapper -> scripts/codegen/
│   └── count_subject_lines.py
├── tests/
├── .codegen-profile             # maps folder -> codegen profile id
└── docs/STRUCTURE.md
```

## Non-standard subject locations

| Folder | Volume path |
|--------|-------------|
| `crosshair/`, `Beniget/` | `subject_repos/generated-volume/` |
| `pylint/`, `TESTMON/` | existing `src/` (pre-scale) |
| `JSCPD/` | `src/subject_volume/` (JavaScript) |
| `Git_Churn/` | `src/subject_volume/` (max 55 lines/file) |

## Root automation (`scripts/`)

```text
scripts/
├── codegen/           # Shared generator, profiles, LOC tools
├── testcases/         # QA validation .txt files
├── data/              # Jira cache, JS issue payloads
└── build/             # Scratch outputs (gitignored)
```

### Common commands

```bash
# Generate 50k LOC for all sub-50k tools
python -m scripts.codegen.run_all_generators --target-lines 50000

# Count LOC per tool
python -m scripts.codegen.count_loc

# Validate golden paths unchanged
python -m scripts.codegen.validate_isolation

# Write docs/STRUCTURE.md in each tool folder
python -m scripts.codegen.write_structure_docs
```

## Design rules

1. **Never modify** `sample_subject/`, `platform/`, root metrics JSON, or tool-specific golden modules.
2. **All new volume** goes to `src/subject_volume/` (or `subject_repos/generated-volume/`).
3. **Folder names are canonical** — spaces in names like `coverage .py` match `TOOL_FOLDER_MAP` and golden repo URLs.
4. Re-run each tool's existing verify/trigger pipeline after regenerating volume.

## Profiles

JSON profiles in [`scripts/codegen/profiles/`](scripts/codegen/profiles/) define per-tool
language, output directory, and file-size constraints.
