"""Build and validate the dataset-agnostic series manifest in the future."""

from pathlib import Path


def build_manifest(config: dict[str, object]) -> None:
    """Build and validate the dataset-agnostic series manifest in the future."""
    raise NotImplementedError("pending: dataset decision pending")


def validate_manifest(path: Path) -> None:
    """Validate the future manifest schema and series entries."""
    raise NotImplementedError("pending: dataset and manifest conventions pending")
