#!/usr/bin/env python3
import json
from pathlib import Path

payload = json.loads(
    Path(__file__).resolve().parent / "build" / "_tmp_js_jira_payload.json"
).read_text(encoding="utf-8")
)
out = Path(__file__).resolve().parent / "data" / "js_jira_issue_requests"
out.mkdir(parents=True, exist_ok=True)
for key, value in payload.items():
    if key.startswith("_"):
        continue
    safe = key.replace("/", "-")
    (out / f"{safe}.json").write_text(
        json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8"
    )
print(len(list(out.glob("*.json"))))
