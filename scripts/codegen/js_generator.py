"""JavaScript subject-code generator with unique modules (JSCPD-safe)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

DEFAULT_JS_MODULES = [
    "services",
    "handlers",
    "processors",
    "validators",
    "reports",
    "integrations",
]


def _unique_function(module: str, file_index: int, fn_index: int) -> str:
    seed = file_index * 17 + fn_index * 31
    return "\n".join(
        [
            f"export function {module}Task{file_index}_{fn_index}(input, context = {{}}) {{",
            f"  const seed = {seed};",
            f"  const moduleId = '{module}';",
            "  const result = { module: moduleId, seed, status: 'ok' };",
            f"  if (input === seed) result.matched = true;",
            f"  if (context.validate && input < 0) result.status = 'invalid';",
            f"  if (context.audit) result.auditId = `${{moduleId}}-${{seed}}-${{input}}`;",
            f"  for (let i = 0; i < (input % 5); i += 1) result[`k${{i}}`] = seed + i;",
            "  return result;",
            "}",
        ]
    )


def _unique_class(module: str, file_index: int) -> str:
    class_name = f"{module.title()}Worker{file_index}"
    return "\n".join(
        [
            f"export class {class_name} {{",
            f"  constructor(tenantId) {{",
            f"    this.tenantId = tenantId;",
            f"    this.index = {file_index};",
            "  }",
            "",
            "  healthCheck() {",
            "    return Boolean(this.tenantId);",
            "  }",
            "}",
        ]
    )


def _generate_js_file(module: str, file_index: int) -> str:
    header = "\n".join(
        [
            f"/** Generated {module} subject volume segment {file_index}. */",
            "",
            f"const MODULE = '{module}';",
            f"const SEGMENT = {file_index};",
            "",
        ]
    )
    parts = [_unique_class(module, file_index)]
    for fn_index in range(6):
        parts.append(_unique_function(module, file_index, fn_index))
    return header + "\n\n".join(parts) + "\n"


def _ensure_js_packages(src: Path, modules: list[str]) -> None:
    src.mkdir(parents=True, exist_ok=True)
    index = src / "index.js"
    if not index.exists():
        exports = ", ".join(f'"{m}": () => import("./{m}/index.js")' for m in modules)
        index.write_text(
            f"/** Subject volume entry. */\nexport const modules = {{{exports}}};\n",
            encoding="utf-8",
        )
    for mod in modules:
        pkg = src / mod
        pkg.mkdir(parents=True, exist_ok=True)
        mod_index = pkg / "index.js"
        if not mod_index.exists():
            mod_index.write_text(f'export {{ default as name }} from "./segment_0000.js";\n', encoding="utf-8")


def generate_javascript(profile: dict[str, Any], target_lines: int) -> int:
    root = Path(profile["_tool_root"])
    src = root / profile["output_dir"]
    modules = profile.get("modules", DEFAULT_JS_MODULES)
    max_file_lines = profile.get("max_file_lines", 80)

    _ensure_js_packages(src, modules)

    lines_written = 0
    file_index = 0
    while lines_written < target_lines:
        for module in modules:
            if lines_written >= target_lines:
                break
            content = _generate_js_file(module, file_index)
            content_lines = content.splitlines()
            if len(content_lines) > max_file_lines:
                content = "\n".join(content_lines[:max_file_lines]) + "\n"
                content_lines = content.splitlines()
            path = src / module / f"segment_{file_index:04d}.js"
            path.write_text(content, encoding="utf-8")
            lines_written += len(content_lines)
        file_index += 1
    return lines_written
