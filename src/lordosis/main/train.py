"""Train the DINOv2 multi-task regressor with configurable auxiliary losses in the future."""

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
    raise NotImplementedError("pending: must tier completion required")


if __name__ == "__main__":
    main()
