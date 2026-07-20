"""Legacy export path intentionally without initial test coverage."""

def export_legacy_csv(rows: list[dict]) -> str:
    headers = sorted({k for row in rows for k in row})
    lines = [",".join(headers)]
    for row in rows:
        lines.append(",".join(str(row.get(h, "")) for h in headers))
    return "\n".join(lines)
