"""Generate realistic commerce platform source code for Testmon validation."""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "commerce_platform"

MODULES = [
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

COMPLEXITY_TARGETS = {
    "low": (1, 5),
    "medium": (6, 10),
    "high": (11, 20),
    "very_high": (21, 35),
}


def ensure_packages() -> None:
    for mod in MODULES:
        pkg = SRC / mod
        pkg.mkdir(parents=True, exist_ok=True)
        init = pkg / "__init__.py"
        if not init.exists():
            init.write_text(
                f'"""Commerce platform {mod.replace("_", " ")} module."""\n',
                encoding="utf-8",
            )
    (SRC / "__init__.py").write_text(
        '"""Commerce platform for Testmon cyclomatic complexity validation."""\n',
        encoding="utf-8",
    )


def branch_block(var: str, count: int) -> str:
    lines = ["    score = 0"]
    for i in range(count):
        lines.append(f"    if {var} == {i}:")
        lines.append(f"        score += {i + 1}")
    lines.append("    else:")
    lines.append(f"        score += {count + 1}")
    return "\n".join(lines)


def generate_function(
    module: str,
    func_name: str,
    complexity: str,
    index: int,
    domain_action: str,
) -> str:
    low, high = COMPLEXITY_TARGETS[complexity]
    branch_count = 1 if complexity == "low" else max(2, high - 2)
    if complexity == "very_high":
        branch_count = 28

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
        branch_block("value", branch_count),
        '    result["score"] = score',
        '    if ctx.get("validate"):',
        '        result["validated"] = value >= 0',
        '    if ctx.get("audit"):',
        f'        result["audit_id"] = f"audit-{{value}}-{index}"',
        "    return result",
    ]
    return "\n".join(lines)


def generate_service_class(module: str, class_index: int) -> str:
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


def domain_actions(module: str) -> list[str]:
    actions = {
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
    return actions[module]


def generate_module_file(module: str, file_index: int) -> str:
    actions = domain_actions(module)
    complexities = ["low", "medium", "high", "very_high"]
    classes = [generate_service_class(module, file_index * 3 + c) for c in range(3)]
    functions = []
    for class_offset in range(3):
        class_index = file_index * 3 + class_offset
        for method_index in range(5):
            action = actions[method_index]
            cx = complexities[(class_offset + method_index) % len(complexities)]
            functions.append(
                generate_function(
                    module,
                    f"process_{class_index}_{method_index}",
                    cx,
                    file_index * 10 + class_offset * 5 + method_index,
                    action,
                )
            )
    header = "\n".join(
        [
            f'"""Generated {module} business logic segment {file_index}."""',
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


def write_core_handcrafted() -> None:
    """Write intentional markers and shared utilities for Testmon scenarios."""
    auth_file = SRC / "auth" / "session.py"
    auth_file.write_text(
        textwrap.dedent(
            '''
            """Authentication session management."""
            from __future__ import annotations

            import hashlib
            from datetime import datetime, timedelta
            from typing import Any


            class SessionError(Exception):
                pass


            def create_session_token(user_id: str, secret: str) -> str:
                """Low complexity session token creator - TESTMON_LOW_COMPLEXITY_TARGET."""
                if not user_id:
                    raise SessionError("user_id required")
                payload = f"{user_id}:{secret}"
                return hashlib.sha256(payload.encode()).hexdigest()


            def validate_session_expiry(issued_at: datetime, ttl_hours: int = 24) -> bool:
                if ttl_hours <= 0:
                    return False
                return datetime.utcnow() <= issued_at + timedelta(hours=ttl_hours)


            def enrich_session_metadata(session: dict[str, Any]) -> dict[str, Any]:
                session = dict(session)
                session.setdefault("created_at", datetime.utcnow().isoformat())
                session.setdefault("active", True)
                return session
            '''
        ).strip()
        + "\n",
        encoding="utf-8",
    )

    orders_file = SRC / "orders" / "pricing_engine.py"
    regions = [
        ("US", "1.0"),
        ("EU", "1.05"),
        ("APAC", "1.10"),
        ("LATAM", "1.15"),
        ("MEA", "1.20"),
        ("CA", "1.25"),
        ("UK", "1.30"),
        ("AU", "1.35"),
        ("IN", "1.40"),
        ("JP", "1.45"),
        ("BR", "1.50"),
        ("MX", "1.55"),
        ("SG", "1.60"),
        ("DE", "1.65"),
        ("FR", "1.70"),
    ]
    lines = [
        '"""Order pricing engine with high cyclomatic complexity."""',
        "from __future__ import annotations",
        "",
        "from decimal import Decimal",
        "from typing import Any",
        "",
        "",
        "def calculate_regional_price(",
        "    base_price: Decimal,",
        "    region: str,",
        "    customer_tier: str,",
        "    promo_code: str | None,",
        "    quantity: int,",
        "    is_wholesale: bool,",
        ") -> Decimal:",
        '    """High complexity pricing - TESTMON_HIGH_COMPLEXITY_TARGET."""',
        "    if base_price < 0:",
        '        raise ValueError("base_price must be non-negative")',
        '    multiplier = Decimal("1.0")',
        '    if region == "DEFAULT":',
        '        multiplier = Decimal("1.0")',
    ]
    for code, value in regions:
        lines.append(f'    elif region == "{code}":')
        lines.append(f'        multiplier = Decimal("{value}")')
    lines.extend(
        [
            "    else:",
            '        multiplier = Decimal("1.25")',
            "",
            '    if customer_tier == "gold":',
            '        multiplier *= Decimal("0.90")',
            '    elif customer_tier == "silver":',
            '        multiplier *= Decimal("0.95")',
            '    elif customer_tier == "bronze":',
            '        multiplier *= Decimal("0.98")',
            "",
            '    if promo_code == "SAVE10":',
            '        multiplier *= Decimal("0.90")',
            '    elif promo_code == "SAVE20":',
            '        multiplier *= Decimal("0.80")',
            '    elif promo_code == "FREESHIP":',
            '        multiplier *= Decimal("0.97")',
            "",
            "    if quantity > 100:",
            '        multiplier *= Decimal("0.85")',
            "    elif quantity > 50:",
            '        multiplier *= Decimal("0.90")',
            "    elif quantity > 10:",
            '        multiplier *= Decimal("0.95")',
            "",
            "    if is_wholesale:",
            '        multiplier *= Decimal("0.88")',
            "",
            '    return (base_price * multiplier).quantize(Decimal("0.01"))',
            "",
            "",
            "def pricing_audit_snapshot(inputs: dict[str, Any], total: Decimal) -> dict[str, Any]:",
            '    return {"inputs": inputs, "total": str(total), "engine": "pricing_engine"}',
            "",
        ]
    )
    orders_file.write_text("\n".join(lines), encoding="utf-8")

    utils_file = SRC / "utils" / "shared.py"
    utils_file.write_text(
        textwrap.dedent(
            '''
            """Shared utilities used across modules - TESTMON_SHARED_UTILITY_TARGET."""
            from __future__ import annotations

            import re
            from typing import Any


            IDENTIFIER_PATTERN = re.compile(r"^[A-Z0-9_-]{3,64}$")


            def normalize_identifier(value: str) -> str:
                """Normalize business identifiers for cross-module usage."""
                cleaned = value.strip().upper().replace(" ", "_")
                if not IDENTIFIER_PATTERN.match(cleaned):
                    raise ValueError(f"invalid identifier: {value}")
                return cleaned


            def merge_context(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
                merged = dict(base)
                for key, val in extra.items():
                    if val is not None:
                        merged[key] = val
                return merged


            def stable_sort_key(record: dict[str, Any]) -> tuple:
                return (
                    record.get("priority", 99),
                    record.get("created_at", ""),
                    record.get("id", ""),
                )
            '''
        ).strip()
        + "\n",
        encoding="utf-8",
    )

    uncovered_file = SRC / "reporting" / "legacy_export.py"
    uncovered_file.write_text(
        textwrap.dedent(
            '''
            """Legacy export path intentionally without initial test coverage."""

            def export_legacy_csv(rows: list[dict]) -> str:
                headers = sorted({k for row in rows for k in row})
                lines = [",".join(headers)]
                for row in rows:
                    lines.append(",".join(str(row.get(h, "")) for h in headers))
                return "\\n".join(lines)
            '''
        ).strip()
        + "\n",
        encoding="utf-8",
    )


def generate(target_lines: int) -> int:
    ensure_packages()
    write_core_handcrafted()

    lines_written = 0
    file_index = 0
    while lines_written < target_lines:
        for module in MODULES:
            if lines_written >= target_lines:
                break
            content = generate_module_file(module, file_index)
            path = SRC / module / f"segment_{file_index:03d}.py"
            path.write_text(content, encoding="utf-8")
            lines_written += len(content.splitlines())
        file_index += 1
    return lines_written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-lines", type=int, default=50000)
    args = parser.parse_args()
    total = generate(args.target_lines)
    print(f"Generated approximately {total} source lines under {SRC}")


if __name__ == "__main__":
    main()
