import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    config_path: Path

    def exists(self) -> bool:
        return self.config_path.exists()

    def paths(self) -> list[Path]:
        paths: list[Path] = []
        if self.exists():
            lines = self.config_path.read_text().splitlines()
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                paths.append(Path(line))
        return paths
