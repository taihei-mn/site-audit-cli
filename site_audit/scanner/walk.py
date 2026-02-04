from __future__ import annotations

from pathlib import Path


def discover_html_files(target: Path) -> list[Path]:
    """Return a sorted list of HTML files to audit.

    Rules:
    - If target is a file: it must be a .html file.
    - If target is a directory: recursively collect **/*.html
    - If nothing is found, return an empty list (caller decides behavior).
    """
    target = target.resolve()

    if target.is_file():
        return [target] if target.suffix.lower() == ".html" else []

    if target.is_dir():
        files = [p for p in target.rglob("*.html") if p.is_file()]
        return sorted(set(p.resolve() for p in files))

    return []
