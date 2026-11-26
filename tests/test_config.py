"""Exercise YAML resolution without any dataset choices."""

from pathlib import Path

import pytest

from lordosis.common.config import load_config, merge_overrides, save_config


def test_load_merge_save_round_trip(tmp_path: Path) -> None:
    """CLI values preserve YAML types and nested settings through a saved copy."""
    source = tmp_path / "source.yaml"
    source.write_text("dataset: null\ntrain:\n  batch_size: 4\n  seed: 7\n", encoding="utf-8")
    resolved = load_config(source, ["train.batch_size=8", "enabled=true", "items=[1, 2]"])
    assert resolved == {
        "dataset": None,
        "train": {"batch_size": 8, "seed": 7},
        "enabled": True,
        "items": [1, 2],
    }
    destination = tmp_path / "run" / "config.yaml"
    save_config(resolved, destination)
    assert load_config(destination) == resolved


def test_merge_preserves_inputs_and_nested_siblings() -> None:
    """Nested mappings merge; lists replace; no caller-owned object changes."""
    original = {"train": {"seed": 7, "batch_size": 4}, "items": [1]}
    resolved = merge_overrides(original, ["train={batch_size: 8}", "items=[2, 3]"])
    assert resolved == {"train": {"seed": 7, "batch_size": 8}, "items": [2, 3]}
    resolved["items"].append(4)
    assert original == {"train": {"seed": 7, "batch_size": 4}, "items": [1]}


@pytest.mark.parametrize("override", ["missing-equals", "=1", "train..seed=7"])
def test_invalid_override_rejected(override: str) -> None:
    """Malformed CLI paths fail with a useful error."""
    with pytest.raises(ValueError, match="override"):
        merge_overrides({}, [override])


@pytest.mark.parametrize("content", ["[1, 2]", "42"])
def test_non_mapping_yaml_rejected(tmp_path: Path, content: str) -> None:
    """A resolved config must be a mapping."""
    path = tmp_path / "config.yaml"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError, match="mapping"):
        load_config(path)


def test_empty_yaml_is_empty_config(tmp_path: Path) -> None:
    """An empty placeholder remains usable as an empty mapping."""
    path = tmp_path / "empty.yaml"
    path.write_text("# TODO\n", encoding="utf-8")
    assert load_config(path) == {}
