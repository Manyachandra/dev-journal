import sys
from pathlib import Path

from dev_journal.config import Config
from dev_journal.summarizer import summarize


DEFAULT_CONFIG = ".journal.toml"


def command_init(path: str = ".") -> int:
    target = Path(path).resolve()
    config_file = target / DEFAULT_CONFIG
    if not config_file.exists():
        config_file.write_text(f"# dev-journal config\n{target.as_posix()}\n")
        print(f"Initialized journal config at {config_file}")
    else:
        print(f"Config already exists at {config_file}")
    return 0


def command_analyze(seed: str = ".", since: str = "", author: str = "", config_path: str | None = None) -> int:
    cfg = Config(Path(config_path or DEFAULT_CONFIG).resolve())
    seed_path = Path(seed).resolve()
    from dev_journal.analyzer import analyze

    entries = analyze(cfg, seed_path, author, since)
    for e in entries:
        src = e.path if e.path else "unknown"
        owner = e.author or "unknown"
        print(f"- [{src}] ({owner}) [{e.date}]: {e.message}")
    return 0


def command_summarize(seed: str = ".", since: str = "", author: str = "", config_path: str | None = None) -> int:
    cfg = Config(Path(config_path or DEFAULT_CONFIG).resolve())
    seed_path = Path(seed).resolve()
    output = summarize(cfg, seed_path, author, since)
    print(output)
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        return command_summarize()

    cmd = argv[0]
    rest = argv[1:]

    config_path = None
    if cmd == "init":
        path = rest[0] if rest else "."
        return command_init(path)
    if cmd in {"analyze", "summarize"}:
        since = ""
        author = ""
        seed = rest[0] if rest else "."
        it = rest[1:]
        while it:
            token = it.pop(0)
            if token == "--config" and it:
                config_path = it.pop(0)
            elif token == "--since" and it:
                since = it.pop(0)
            elif token == "--author" and it:
                author = it.pop(0)
        if cmd == "analyze":
            return command_analyze(seed, since, author, config_path)
        return command_summarize(seed, since, author, config_path)

    print(f"Unknown command: {cmd}")
    return 1
