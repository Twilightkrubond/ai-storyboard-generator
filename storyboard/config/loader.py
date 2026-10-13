"""Config loading: defaults -> user file -> project overrides, merged in order."""
from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import tomli_w

from storyboard.utils.paths import app_config_dir, project_root

_DEFAULTS = Path(__file__).with_name("defaults.toml")


class ConfigError(RuntimeError):
    """Raised when a config file is malformed or a required key is missing."""


def _deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load_config(project_dir: Path | None = None) -> dict[str, Any]:
    """Return the merged config for a project.

    Order: package defaults, then `%APPDATA%/ai-storyboard-generator/local.toml`,
    then `<project>/storyboard.toml` if a project dir is given.
    """
    try:
        merged = tomllib.loads(_DEFAULTS.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:  # pragma: no cover - ships correct
        raise ConfigError(f"bundled defaults are corrupt: {exc}") from exc

    user_cfg = app_config_dir() / "local.toml"
    if user_cfg.exists():
        merged = _deep_merge(merged, tomllib.loads(user_cfg.read_text(encoding="utf-8")))

    if project_dir is not None:
        proj_cfg = project_root(project_dir) / "storyboard.toml"
        if proj_cfg.exists():
            merged = _deep_merge(merged, tomllib.loads(proj_cfg.read_text(encoding="utf-8")))

    return merged


def write_user_config(cfg: dict[str, Any]) -> Path:
    """Persist user config. Creates the app config dir if missing."""
    target = app_config_dir() / "local.toml"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(tomli_w.dumps(cfg), encoding="utf-8")
    return target