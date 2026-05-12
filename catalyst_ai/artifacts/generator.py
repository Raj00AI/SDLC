from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class GeneratedArtifact:
    name: str
    path: Path


def _ts() -> str:
    return datetime.utcnow().strftime("%Y%m%d-%H%M%S")


def write_text(artifacts_dir: Path, name: str, content: str, ext: str = "md") -> GeneratedArtifact:
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    path = artifacts_dir / f"{name}.{ext}"
    path.write_text(content, encoding="utf-8")
    return GeneratedArtifact(name=name, path=path)


def write_versioned(artifacts_dir: Path, base_name: str, content: str, ext: str = "md") -> GeneratedArtifact:
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    path = artifacts_dir / f"{base_name}-{_ts()}.{ext}"
    path.write_text(content, encoding="utf-8")
    return GeneratedArtifact(name=base_name, path=path)
