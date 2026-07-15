# Dev Journal CLI 🗒️

A focused CLI tool for engineering journals, weekly summaries, and reflection across Git history, local journal files, and hand-written notes.

## About

Dev Journal CLI ingests commit messages, local journal files, and team notes, then produces sanitized journals and summaries. It is designed for developers who want a lightweight, scriptable way to reflect on what they shipped, learned, and broke.

## Features

- **Git-backed journals**: Extract journal entries directly from Git history with a simple message convention.
- **File-backed journals**: Ingest hand-written journal files with lightweight markers.
- **Integration**: works with `dev-journal init PATH` to configure local journal directories.
- **ASCII summary**: Parseable, human-readable summary output.
- **Filtering**: `--since`, `--author`, and `--path` filters for targeted reports.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Initialize journal config
dev-journal init .

# Show journal for a date range
dev-journal analyze --since 2026-07-01

# Summarize journal entries by date
dev-journal summarize --since 2026-07-01
```

## Project Structure

```text
dev-journal/
├── pyproject.toml
├── README.md
├── dev_journal/
│   ├── __init__.py
│   ├── cli.py
│   ├── parser.py
│   ├── analyzer.py
│   └── summarizer.py
└── tests/
    └── test_cli.py
```

## Tags / Keywords

`cli` `journal` `git` `developer-tools` `weekly-summary` `reflection` `python` `engineering`
