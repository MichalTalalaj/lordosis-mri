# Can AI estimate lordosis directly from MRI?

University project: estimate the lumbar lordosis angle directly from sagittal MRI.
This repository currently contains scaffolding only.

## Windows setup (uv)

Install Python 3.12 and [uv](https://docs.astral.sh/uv/getting-started/installation/),
then run from the repository root:

```powershell
uv sync --extra dev
```

The explicit CUDA 12.8 PyTorch index supports the RTX 5070 requirement.

## Linux setup (uv)

With Python 3.12 and uv installed, run from the repository root:

```bash
uv sync --extra dev
```

Windows and Linux use cu128 wheels; the package also supports CPU execution.
Future tier dependencies can be installed with `--extra main` or `--extra stretch`.

## Colab setup

Open [notebooks/00_colab_setup.ipynb](notebooks/00_colab_setup.ipynb).
It clones this repository, installs the project without dependencies, installs
`requirements-colab.txt`, mounts Drive and sets `LORDOSIS_DATA_ROOT`.
It uses Colab's existing torch and torchvision installations.

## Data

TBD: waiting for dataset decision

Data paths will use `LORDOSIS_DATA_ROOT`, defaulting to `./data`.

## Training

TBD: waiting for dataset decision

Tier modules are stubs. Their CLI help is available, for example:

```bash
uv run python -m lordosis.must.train --help
```

Implement tiers in order: [must](src/lordosis/must/README.md),
[main](src/lordosis/main/README.md), [stretch](src/lordosis/stretch/README.md).

## Checks

```bash
uv run ruff check .
uv run pytest
```

Tests use synthetic inputs on CPU and require no data or model weights.
