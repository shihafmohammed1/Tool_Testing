# White Box Repo Automation Scripts

Scripts for audit Excel generation, QA testcase exports, SharePoint sync, and shared subject-code generation.

## Layout

```text
scripts/
├── codegen/              # Shared ~50k LOC subject generator (see codegen/README.md)
├── testcases/            # QA validation .txt files for Python/Java tools
├── data/
│   ├── jira_whitebox_audit.json
│   └── js_jira_issue_requests/
├── build/                # Scratch/tmp outputs (gitignored)
├── generate_whitebox_audit_excel.py
├── generate_python_testcase_txt.py
├── generate_java_testcase_txt.py
├── sync_sharepoint_audit.py
└── sharepoint_graph.py
```

## Common commands

```bash
# Regenerate audit Excel
python scripts/generate_whitebox_audit_excel.py

# Regenerate Python QA testcase files (default: 5 tools)
python scripts/generate_python_testcase_txt.py

# Regenerate Java QA testcase files
python scripts/generate_java_testcase_txt.py

# Generate ~50k subject LOC for one tool (from tool folder)
python scripts/generate_subject_code.py --target-lines 50000

# Generate for all sub-50k tools
python scripts/codegen/run_all_generators.py --target-lines 50000

# Count LOC across tool folders
python scripts/codegen/count_loc.py
```

## Data flow

1. Strategy Excel + Jira JSON + git scan → `WhiteBox_Metrics_Data_Readiness_Audit.xlsx`
2. Strategy + Jira → `testcases/Python_Testcase_*.txt` and `Java_Testcase_*.txt`
3. Tool profiles in `codegen/profiles/` → `src/subject_volume/` in each tool folder
