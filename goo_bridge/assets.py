# SPDX-License-Identifier: GPL-3.0-or-later
"""External asset inventory shared by analysis, local and remote rendering."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass
class Asset:
    path: str
    kind: str = ""
    name: str = ""
    exists: bool = False
    size: int = 0
    sha256: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def from_analysis(report: dict[str, Any]) -> list[Asset]:
    assets: list[Asset] = []
    for item in report.get("external_files") or []:
        if not isinstance(item, dict):
            continue
        path = str(item.get("path") or "")
        if not path:
            continue
        candidate = Path(path).expanduser()
        exists = candidate.is_file()
        assets.append(
            Asset(
                path=str(candidate),
                kind=str(item.get("kind") or ""),
                name=str(item.get("name") or ""),
                exists=exists,
                size=candidate.stat().st_size if exists else 0,
                sha256=sha256_file(candidate) if exists else "",
            )
        )
    return assets


def missing(assets: Iterable[Asset]) -> list[Asset]:
    return [asset for asset in assets if not asset.exists]


def manifest(assets: Iterable[Asset]) -> dict[str, Any]:
    items = [asset.to_dict() for asset in assets]
    return {
        "version": 1,
        "assets": items,
        "missing": [item["path"] for item in items if not item["exists"]],
        "total_bytes": sum(int(item["size"]) for item in items),
    }
