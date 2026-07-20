# Shared subject-code generation

Generates ~50,000 lines of isolated subject code under each tool folder without modifying golden artifacts.

## Usage

From repo root:

```bash
python -m scripts.codegen.run_all_generators --target-lines 50000
```

From a tool folder:

```bash
python scripts/generate_subject_code.py --target-lines 50000
```

## Profiles

Each JSON file in `profiles/` defines:

- `tool_id` / `tool_folder` — target directory under repo root
- `language` — `python` or `javascript`
- `output_dir` — usually `src/subject_volume` (or `subject_repos/generated-volume`)
- `max_file_lines` — 1200 default; 55 for Git_Churn; 80 for JSCPD

## Utilities

- `count_loc.py` — report volume and total LOC per profile
- `validate_isolation.py` — ensure `sample_subject/`, `platform/`, etc. unchanged
- `run_all_validations.py` — LOC + isolation orchestrator
