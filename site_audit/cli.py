from __future__ import annotations

import argparse
from pathlib import Path
import sys

from site_audit.scanner.walk import discover_html_files
from site_audit.parser.html_extract import extract_from_html_file, LinkRef
from site_audit.rules.noopener import check_noopener
from site_audit.reporter.markdown import render_markdown
from site_audit.reporter.json_out import render_json


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

    all_links: list[LinkRef] = []
    img_count = 0  # reserved for future rules

    for f in html_files:
        links, images = extract_from_html_file(f)
        all_links.extend(links)
        img_count += len(images)

    findings = check_noopener(all_links)

    if args.format == "json":
        print(render_json(len(html_files), findings))
    else:
        print(render_markdown(len(html_files), findings))

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
