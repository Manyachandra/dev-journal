import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ENTRY_PATTERN = re.compile(
    r"^(?:\s*\*\s*)?(?:#entry|\[entry\]|entry)\s*:?\s*(.+)$", re.IGNORECASE
)


@dataclass(frozen=True)
class Entry:
    author: str
    date: str
    path: str
    raw: str
    message: str


def parse_text(file_path: str, line: str) -> Entry | None:
    m = ENTRY_PATTERN.match(line)
    if not m:
        return None
    path = Path(file_path).resolve().as_posix()
    try:
        d = datetime.now().date().isoformat()
    except Exception:
        d = ""
    return Entry(author="", date=str(d), path=str(path), raw=line.strip(), message=m.group(1).strip())


def _date_iso(s: str) -> str:
    try:
        if s:
            datetime.strptime(s, "%Y-%m-%d")
            return s
    except Exception:
        pass
    return ""


def git_log(repo: Path, author: str, since: str) -> list[Entry]:
    entries: list[Entry] = []
    fmt = "%H|%an|%ad|%s"
    cmd = ["git", "-C", str(repo), "log", f"--format={fmt}", "--date=short"]
    env = dict(__import__("os").environ)
    env["FILTER_BRANCH_SQUELCH_WARNING"] = "1"
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT, env=env)
    except subprocess.CalledProcessError as exc:
        return entries
    for line in out.splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        sha, an, dt, msg = parts
        m = re.search(r"(?:#entry|\[entry\]|entry)\s*:?\s*(.+)", msg, re.IGNORECASE)
        if not m:
            continue
        if author and an != author:
            continue
        if since and _date_iso(dt) < _date_iso(since):
            continue
        entries.append(
            Entry(author=an, date=dt, path=str(repo), raw=msg, message=m.group(1).strip())
        )
    return entries
