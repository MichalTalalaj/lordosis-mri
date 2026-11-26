"""Provide torch datasets backed by the series manifest in the future."""

from pathlib import Path


class LordosisDataset:
    """Read preprocessed images and selected angle targets in the future."""

    def __init__(self, manifest_path: Path, config: dict[str, object]) -> None:
        """Initialise the future dataset from a manifest and resolved settings."""
        raise NotImplementedError("pending: dataset and label conventions pending")
