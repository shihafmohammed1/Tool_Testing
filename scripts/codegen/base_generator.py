"""Python subject-code generator (~50k LOC) for White Box tool folders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

DEFAULT_MODULES = [
    "auth",
    "users",
    "orders",
    "payments",
    "inventory",
    "reporting",
    "notifications",
    "file_processing",
    "validation",
    "utils",
]

DEFAULT_COMPLEXITY = {
    "low": (1, 5),
    "medium": (6, 10),
    "high": (11, 20),
    "very_high": (21, 35),
}

DOMAIN_ACTIONS: dict[str, list[str]] = {
    "auth": [
        "Authenticate credential",
        "Authorize role permission",
        "Validate session token",
        "Check MFA requirement",
        "Evaluate password policy",
    ],
    "users": [
        "Register user profile",
        "Update user preference",
        "Deactivate user account",
        "Merge duplicate profiles",
        "Calculate loyalty tier",
    ],
    "orders": [
        "Validate order line item",
        "Calculate order subtotal",
        "Apply promotional discount",
        "Determine shipping option",
        "Evaluate cancellation policy",
    ],
    "payments": [
        "Authorize card payment",
        "Process refund request",
        "Validate billing address",
        "Calculate transaction fee",
        "Detect fraudulent pattern",
    ],
    "inventory": [
        "Reserve stock quantity",
        "Calculate reorder point",
        "Evaluate warehouse capacity",
        "Track batch expiration",
        "Adjust safety stock level",
    ],
    "reporting": [
        "Aggregate daily sales",
        "Build executive summary",
        "Calculate margin report",
        "Generate compliance export",
        "Rank product performance",
    ],
    "notifications": [
        "Route email notification",
        "Schedule SMS delivery",
        "Evaluate push preference",
        "Throttle notification burst",
        "Render template variables",
    ],
    "file_processing": [
        "Parse CSV import row",
        "Validate file checksum",
        "Transform export format",
        "Archive processed document",
        "Detect malformed record",
    ],
    "validation": [
        "Validate email format",
        "Validate postal code",
        "Validate tax identifier",
        "Validate date range",
        "Validate schema field",
    ],
    "utils": [
        "Normalize identifier string",
        "Convert currency amount",
        "Hash stable dictionary",
        "Merge nested mapping",
        "Format business timestamp",
    ],
}


def _branch_block(var: str, count: int) -> str:
    lines = ["    score = 0"]
    for i in range(count):
        lines.append(f"    if {var} == {i}:")
        lines.append(f"        score += {i + 1}")
    lines.append("    else:")
    lines.append(f"        score += {count + 1}")
    return "\n".join(lines)


def _generate_function(
    module: str,
    func_name: str,
    complexity: str,
    index: int,
    domain_action: str,
    complexity_targets: dict[str, tuple[int, int]],
) -> str:
    low, high = complexity_targets[complexity]
    branch_count = 1 if complexity == "low" else max(2, high - 2)
    if complexity == "very_high":
        branch_count = min(28, high + 8)

    lines = [
        f"def {func_name}(value: int, context: dict | None = None) -> dict:",
        f'    """{domain_action} for {module} record {index}.',
        f"",
        f"    Complexity target: {complexity}.",
        f'    """',
        "    ctx = context or {}",
        "    result = {"
        f'        "module": "{module}",'
        f'        "index": {index},'
        '        "status": "pending",',
        "    }",
        _branch_block("value", branch_count),
        '    result["score"] = score',
        '    if ctx.get("validate"):',
        '        result["validated"] = value >= 0',
        '    if ctx.get("audit"):',
        f'        result["audit_id"] = f"audit-{{value}}-{index}"',
        "    return result",
    ]
    return "\n".join(lines)


def _generate_service_class(module: str, class_index: int) -> str:
    class_name = f"{module.title().replace('_', '')}Service{class_index}"
    return "\n".join(
        [
            f"class {class_name}:",
            f'    """Service layer for {module.replace("_", " ")} operations."""',
            "",
            "    def __init__(self, tenant_id: str) -> None:",
            "        self.tenant_id = tenant_id",
            "        self._cache: dict[str, object] = {}",
            "",
            "    def health_check(self) -> bool:",
            "        return bool(self.tenant_id)",
        ]
    )


def _generate_module_file(
    module: str,
    file_index: int,
    *,
    complexity_targets: dict[str, tuple[int, int]],
    compact: bool = False,
) -> str:
    actions = DOMAIN_ACTIONS.get(module, DOMAIN_ACTIONS["utils"])
    complexities = ["low", "medium", "high", "very_high"]
    class_count = 1 if compact else 3
    method_count = 2 if compact else 5
    classes = [_generate_service_class(module, file_index * 3 + c) for c in range(class_count)]
    functions = []
    for class_offset in range(class_count):
        class_index = file_index * 3 + class_offset
        for method_index in range(method_count):
            action = actions[method_index % len(actions)]
            cx = complexities[(class_offset + method_index) % len(complexities)]
            functions.append(
                _generate_function(
                    module,
                    f"process_{class_index}_{method_index}",
                    cx,
                    file_index * 10 + class_offset * 5 + method_index,
                    action,
                    complexity_targets,
                )
            )
    header = "\n".join(
        [
            f'"""Generated {module} subject volume segment {file_index}."""',
            "from __future__ import annotations",
            "",
            "from typing import Any",
            "",
            "",
            f"class {module.title().replace('_', '')}Error(Exception):",
            f'    """Domain error for {module}."""',
            "",
            "",
            f"class {module.title().replace('_', '')}Context:",
            "    def __init__(self, tenant_id: str, metadata: dict[str, Any] | None = None) -> None:",
            "        self.tenant_id = tenant_id",
            "        self.metadata = metadata or {}",
            "",
        ]
    )
    parts = [header, "\n\n".join(classes)]
    parts.append("\n\n".join(functions))
    return "\n\n".join(parts) + "\n"


def _ensure_packages(src: Path, modules: list[str], package_doc: str) -> None:
    for mod in modules:
        pkg = src / mod
        pkg.mkdir(parents=True, exist_ok=True)
        init = pkg / "__init__.py"
        if not init.exists():
            init.write_text(
                f'"""Subject volume {mod.replace("_", " ")} module."""\n',
                encoding="utf-8",
            )
    root_init = src / "__init__.py"
    if not root_init.exists():
        root_init.write_text(f'"""{package_doc}"""\n', encoding="utf-8")


def generate_python(profile: dict[str, Any], target_lines: int) -> int:
    root = Path(profile["_tool_root"])
    src = root / profile["output_dir"]
    modules = profile.get("modules", DEFAULT_MODULES)
    max_file_lines = profile.get("max_file_lines", 1200)
    compact = max_file_lines <= 60
    raw_targets = profile.get("complexity_targets", DEFAULT_COMPLEXITY)
    complexity_targets = {k: tuple(v) for k, v in raw_targets.items()}
    package_doc = profile.get(
        "package_doc", f"Generated subject volume for {profile['tool_id']}."
    )

    _ensure_packages(src, modules, package_doc)

    lines_written = 0
    file_index = 0
    while lines_written < target_lines:
        for module in modules:
            if lines_written >= target_lines:
                break
            content = _generate_module_file(
                module,
                file_index,
                complexity_targets=complexity_targets,
                compact=compact,
            )
            content_lines = content.splitlines()
            if len(content_lines) > max_file_lines:
                content = "\n".join(content_lines[:max_file_lines]) + "\n"
                content_lines = content.splitlines()
            path = src / module / f"segment_{file_index:04d}.py"
            path.write_text(content, encoding="utf-8")
            lines_written += len(content_lines)
        file_index += 1
    return lines_written
