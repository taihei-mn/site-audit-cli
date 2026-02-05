from __future__ import annotations

from site_audit.rules.finding import Finding


def render_markdown(scanned_files: int, findings: list[Finding]) -> str:
    lines: list[str] = []
    lines.append(f"Scanned {scanned_files} HTML file(s).")
    if not findings:
        lines.append("No issues found.")
        return "\n".join(lines)

    lines.append(f"Issues found: {len(findings)}")
    for f in findings:
        href = f.href or ""
        lines.append(f"- [{f.rule_id}] {f.file}: {f.message} ({href})")
    return "\n".join(lines)
