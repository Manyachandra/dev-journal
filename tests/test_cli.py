from pathlib import Path

from dev_journal.config import Config
from dev_journal.parser import parse_text


def test_parse_entry_markers() -> None:
    cases = [
        ("#entry: shipped feature",
         "shipped feature"),
        ("[entry] fixed critical bug",
         "fixed critical bug"),
        ("entry: reviewed PR",
         "reviewed PR"),
        ("  * #entry cleaned up logs",
         "cleaned up logs"),
    ]
    for line, expected in cases:
        ent = parse_text("memory.md", line)
        assert ent is not None, f"failed on {line}"
        assert ent.message == expected


def test_skips_non_entries() -> None:
    assert parse_text("x.md", "some random line") is None
    assert parse_text("x.md", "# just a heading") is None


def test_config_paths(tmp_path: Path) -> None:
    f = tmp_path / ".journal.toml"
    f.write_text(f"{tmp_path}\n")
    cfg = Config(f)
    assert cfg.exists() is True
    paths = cfg.paths()
    assert paths == [tmp_path]
