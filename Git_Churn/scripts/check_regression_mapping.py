"""Verify regression suite mapping integrity."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.regression_registry import load_regression_mappings


def main() -> int:
    mappings = load_regression_mappings()
    if len(mappings) < 19:
        print(f"FAIL: Expected >= 19 mappings, got {len(mappings)}")
        return 1
    print(f"OK: {len(mappings)} prod-test mappings verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
