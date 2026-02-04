from __future__ import annotations

import argparse
from pathlib import Path
import sys

from site_audit.scanner.walk import discover_html_files
from site_audit.parser.html_extract import extract_from_html_file


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="site-audit",
        description="Audit a directory of static HTML files.",
    )
    p.add_argument(
        "path",
        type=Path,
        help="Directory (or .html file) to audit",
    )
    p.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    target: Path = args.path
    if not target.exists():
        print(f"ERROR: path not found: {target}", file=sys.stderr)
        return 2

    if target.is_file() and target.suffix.lower() != ".html":
        print(f"ERROR: file is not .html: {target}", file=sys.stderr)
        return 2

    html_files = discover_html_files(target)
    if not html_files:
        print(f"ERROR: no .html files found under: {target}", file=sys.stderr)
        return 2

    link_count = 0
    img_count = 0
    for f in html_files:
        links, images = extract_from_html_file(f)
        link_count += len(links)
        img_count += len(images)

    print(f"Found {len(html_files)} HTML file(s). Extracted {link_count} link(s), {img_count} image(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
