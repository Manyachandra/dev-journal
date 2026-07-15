from pathlib import Path
from dev_journal.parser import git_log, parse_text
from dev_journal.config import Config


def file_entries(config: Config, author: str, since: str) -> list:
    entries = []
    for p in config.paths():
        if not p.exists():
            continue
        if p.is_file() and p.suffix.lower() in {".md", ".txt", ".journal"}:
            try:
                lines = p.read_text().splitlines()
            except Exception:
                continue
            rel = p.as_posix()
            for line in lines:
                ent = parse_text(rel, line)
                if ent is None:
                    continue
                if author and ent.author != author:
                    continue
                if since and ent.date < since:
                    continue
                entries.append(ent)
        elif p.is_dir():
            for child in p.rglob("*"):
                if child.is_file() and child.suffix.lower() in {".md", ".txt", ".journal"}:
                    try:
                        text = child.read_text()
                    except Exception:
                        continue
                    rel = child.as_posix()
                    for line in text.splitlines():
                        ent = parse_text(rel, line)
                        if ent is None:
                            continue
                        if author and ent.author != author:
                            continue
                        if since and ent.date < since:
                            continue
                        entries.append(ent)
    return entries


def analyze(config: Config, seed_path: Path, author: str, since: str) -> list:
    seed = seed_path.resolve()
    git = git_log(seed, author, since)
    files = file_entries(config, author, since)
    combined = files + git
    combined.sort(key=lambda x: (x.date, x.author, x.message))
    return combined
