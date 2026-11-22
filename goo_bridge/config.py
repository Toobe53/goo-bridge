# SPDX-License-Identifier: GPL-3.0-or-later
"""Configuration and platform paths for GOO Bridge."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


APP_NAME = "goo-bridge"
CONFIG_VERSION = 1


def home_directory() -> Path:
    """Return the per-user GOO Bridge state directory.

    ``GOO_BRIDGE_HOME`` overrides the default, which keeps tests and portable
    installations from touching the real home directory.
    """
    override = os.environ.get("GOO_BRIDGE_HOME")
    if override:
        return Path(override).expanduser()
    if sys.platform == "win32":
        base = os.environ.get("APPDATA") or os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base) / "GOO Bridge"
        return Path.home() / "AppData" / "Roaming" / "GOO Bridge"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "GOO Bridge"
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "goo-bridge"
    return Path.home() / ".config" / "goo-bridge"


def config_path() -> Path:
    return home_directory() / "config.json"


@dataclass
class RemoteProfile:
    """A remote render host as stored in ``config.json``."""

    name: str
    host: str
    user: str
    port: int = 22
    key: str = ""
    blender: str = "blender"
    workspace: str = "~/.goo-bridge"
    python: str = "python3"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RemoteProfile":
        return cls(
            name=str(data.get("name", "")),
            host=str(data.get("host", "")),
            user=str(data.get("user", "")),
            port=int(data.get("port", 22)),
            key=str(data.get("key", "")),
            blender=str(data.get("blender", "blender")),
            workspace=str(data.get("workspace", "~/.goo-bridge")),
            python=str(data.get("python", "python3")),
        )


@dataclass
class Config:
    blender: str = ""
    language: str = "en_US"
    remote: list[RemoteProfile] = field(default_factory=list)
    version: int = CONFIG_VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["remote"] = [profile.to_dict() for profile in self.remote]
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        profiles = [
            RemoteProfile.from_dict(item)
            for item in data.get("remote", [])
            if isinstance(item, dict)
        ]
        return cls(
            blender=str(data.get("blender", "")),
            language=str(data.get("language", "en_US")),
            remote=profiles,
            version=int(data.get("version", CONFIG_VERSION)),
        )

    def profile(self, name: str) -> RemoteProfile:
        for item in self.remote:
            if item.name == name:
                return item
        raise KeyError(f"unknown remote profile: {name!r}")

    def set_profile(self, profile: RemoteProfile) -> None:
        for index, item in enumerate(self.remote):
            if item.name == profile.name:
                self.remote[index] = profile
                return
        self.remote.append(profile)


def load_config(path: Path | None = None) -> Config:
    target = path or config_path()
    try:
        text = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return Config()
    except OSError:
        return Config()
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return Config()
    if not isinstance(data, dict):
        return Config()
    return Config.from_dict(data)


def save_config(config: Config, path: Path | None = None) -> Path:
    target = path or config_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(config.to_dict(), indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    return target
