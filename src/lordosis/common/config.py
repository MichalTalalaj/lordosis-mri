"""Load YAML configs, resolve dotted CLI overrides and save resolved copies."""

from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml


def _merge(target: dict[str, Any], updates: Mapping[str, Any]) -> None:
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _merge(target[key], value)
        else:
            target[key] = deepcopy(value)


def merge_overrides(
    config: Mapping[str, Any], overrides: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Return an independent config with dotted key=YAML-value CLI overrides.

    Mapping values merge recursively; scalars and lists replace earlier values.
    Later overrides win. Missing or scalar intermediate nodes become mappings.
    """
    resolved = deepcopy(dict(config))
    for override in overrides or ():
        key, separator, raw_value = override.partition("=")
        parts = key.split(".")
        if not separator or any(not part.strip() for part in parts):
            raise ValueError(f"Invalid config override: {override!r}; expected dotted.key=value")
        value = yaml.safe_load(raw_value)
        target = resolved
        for part in parts[:-1]:
            if not isinstance(target.get(part), dict):
                target[part] = {}
            target = target[part]
        _merge(target, {parts[-1]: value})
    return resolved


def load_config(path: Path, overrides: Sequence[str] | None = None) -> dict[str, Any]:
    """Read a YAML mapping and apply optional dotted CLI overrides."""
    with Path(path).open(encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
    if config is None:
        config = {}
    if not isinstance(config, dict):
        raise ValueError("Config YAML must contain a mapping")
    return merge_overrides(config, overrides)


def save_config(config: Mapping[str, Any], path: Path) -> None:
    """Write a resolved YAML copy, creating its parent directory if necessary."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as stream:
        yaml.safe_dump(dict(config), stream, sort_keys=False)
