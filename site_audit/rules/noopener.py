from __future__ import annotations

from site_audit.parser.html_extract import LinkRef
from site_audit.rules.finding import Finding

RULE_ID = "link-noopener"


def check_noopener(links: list[LinkRef]) -> list[Finding]:
    """Find <a target='_blank'> links missing rel=noopener."""
    findings: list[Finding] = []
    for l in links:
        if (l.target or "").lower() != "_blank":
            continue
        rel = (l.rel or "").lower()
        tokens = {t for t in rel.replace(",", " ").split() if t}
        if "noopener" in tokens:
            continue
        findings.append(
            Finding(
                rule_id=RULE_ID,
                file=l.file,
                href=l.href,
                message="target=_blank without rel=noopener",
            )
        )
    return findings
