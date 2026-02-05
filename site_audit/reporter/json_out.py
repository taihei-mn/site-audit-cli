from __future__ import annotations

import json
from site_audit.rules.finding import Finding


def render_json(scanned_files: int, findings: list[Finding]) -> str:
    payload = {
        "scanned_files": scanned_files,
        "findings": [
            {
                "rule_id": f.rule_id,
                "file": str(f.file),
                "message": f.message,
                "href": f.href,
            }
            for f in findings
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
