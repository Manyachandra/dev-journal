from collections import defaultdict
from dev_journal.analyzer import analyze
from dev_journal.config import Config


def summarize(config: Config, seed_path, author: str, since: str) -> str:
    entries = analyze(config, seed_path, author, since)
    if not entries:
        return "No journal entries found."

    lines = ["# Dev Journal Summary", ""]
    dates = sorted({e.date for e in entries})
    for d in dates:
        day = [d]
        day_entries = [e for e in entries if e.date == d]
        if author:
            day_entries = [e for e in day_entries if e.author == author]
            day.append(f"AUTHOR: {author}")
        day.append("")
        day.append(f"ENTRIES ({len(day_entries)})")
        for e in day_entries:
            src = e.path if e.path else "unknown"
            owner = e.author or "unknown"
            day.append(f"- [{src}] ({owner}): {e.message}")
        lines.append("\n".join(day))

    return "\n\n".join(lines)
