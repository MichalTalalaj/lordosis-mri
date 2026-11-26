"""Preprocess selected images with angle-preserving geometry in the future."""

import argparse
from collections.abc import Sequence
from pathlib import Path


def main(argv: Sequence[str] | None = None) -> None:
    """Parse the planned config interface; workflow implementation is deferred."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True, help="Path to a YAML config")
    parser.add_argument(
        "--set", dest="overrides", action="append", default=[], metavar="KEY=VALUE",
        help="Planned dotted YAML override; repeat to override multiple keys",
    )
    parser.parse_args(argv)
    raise NotImplementedError("pending: dataset decision pending")


if __name__ == "__main__":
    main()
