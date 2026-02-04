from __future__ import annotations

import argparse
from pathlib import Path
import sys


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="site-audit",
        description="Audit a directory of static HTML files (wiring only).",
    )
    p.add_argument(
        "path",
        type=Path,
        help="Directory (or file) to audit",
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

    # Phase 2: wiring only. Actual scanning/rules/reporting comes in Phase 3.
    print(f"site-audit: target={target} format={args.format}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
