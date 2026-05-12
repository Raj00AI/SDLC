from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppPaths:
    root: Path

    @property
    def data_dir(self) -> Path:
        return self.root / ".data"

    @property
    def artifacts_dir(self) -> Path:
        return self.root / ".artifacts"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "catalyst.duckdb"


def get_paths() -> AppPaths:
    root = Path(__file__).resolve().parents[1]
    return AppPaths(root=root)
