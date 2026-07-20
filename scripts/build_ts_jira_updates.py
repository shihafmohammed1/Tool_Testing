#!/usr/bin/env python3
"""Build TypeScript Jira update payloads from JS issue request files."""
import json
import re
from pathlib import Path

KEYS = {
    "lizard": "TP-2945",
    "sonarjs": "TP-2946",
    "plato": "TP-2947",
    "jscpd": "TP-2948",
    "jsinspect": "TP-2949",
    "complexity report": "TP-2950",
    "biome": "TP-2951",
    "eslint": "TP-2952",
    "eslint-plugin-security": "TP-2953",
    "snyk": "TP-2954",
    "cyclonedx-cdxgen": "TP-2955",
}

REQ_DIR = Path(__file__).resolve().parent / "data" / "js_jira_issue_requests"
OUT = Path(__file__).resolve().parent / "data" / "ts_jira_updates.json"


def to_typescript(text: str) -> str:
    text = text.replace("JavaScript tool", "TypeScript tool")
    text = text.replace("**JavaScript**", "**TypeScript**")
    text = text.replace("| Language focus | JavaScript |", "| Language focus | TypeScript |")
    text = text.replace("| JS Primary | JS Secondary |", "| TS Primary | TS Secondary |")
    text = text.replace("JavaScript column", "TypeScript column")
    text = text.replace("JavaScript repositories", "TypeScript repositories")
    text = text.replace("JavaScript repository", "TypeScript repository")
    text = text.replace("JavaScript projects", "TypeScript projects")
    text = text.replace("JavaScript repos", "TypeScript repos")
    text = text.replace("JavaScript lint", "TypeScript lint")
    text = text.replace("JavaScript SAST", "TypeScript SAST")
    text = text.replace("Primary JavaScript", "Primary TypeScript")
    text = text.replace("Secondary/support JavaScript", "Secondary/support TypeScript")
    text = text.replace("Secondary JavaScript", "Secondary TypeScript")
    text = text.replace("JavaScript tooling", "TypeScript tooling")
    text = re.sub(
        r"TypeScript secondary tool on (.+?); validate (.+?) on TypeScript",
        r"Secondary TypeScript tool on \1; validate \2 on TypeScript",
        text,
    )
    return text


def main() -> None:
    updates = []
    for stem, key in KEYS.items():
        path = REQ_DIR / f"{stem}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        labels = ["TypeScript" if lb == "JavaScript" else lb for lb in data["labels"]]
        updates.append(
            {
                "key": key,
                "fields": {
                    "summary": to_typescript(data["summary"]),
                    "description": to_typescript(data["description"]),
                    "labels": labels,
                },
            }
        )
    OUT.write_text(json.dumps(updates, ensure_ascii=False, indent=2), encoding="utf-8")
    print(len(updates), "updates ->", OUT)


if __name__ == "__main__":
    main()
