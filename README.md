# site-audit-cli

A small, rule-based CLI tool to audit static sites.

This tool was created to keep a static portfolio site maintainable and consistent,
with lightweight checks that can run locally or in CI.

## Why

Static sites are simple, but they tend to accumulate small inconsistencies over time:
missing attributes, unsafe link patterns, or broken local references.

## Goals

- Provide a fast, local audit for static HTML sites
- Keep audit rules independent and easy to add or remove
- Make results usable both for humans and for CI automation

## Non-goals

- Replacing Lighthouse or performance analysis tools
- Automatically fixing issues
- Supporting dynamic or SSR-based frameworks (initially)

## Installation

```bash
pipx install .
```

## Usage

```bash
site-audit ./dist
site-audit ./dist --format markdown
site-audit ./dist --format json
```

## Planned checks (v0.1.0)

- noopener
- broken-links
- img-alt

## Architecture

Scanner / Rules / Reporter

## License

MIT
