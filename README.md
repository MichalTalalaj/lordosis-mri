# Can AI estimate lordosis directly from MRI?

University project: estimate the L1–S1 lumbar lordosis angle directly from sagittal
lumbar spine MRI with one compact 2D CNN. Reference angles are planned from
AI-assisted mask pre-labels followed by human review.

This repository contains scaffolding only. Data preparation, labelling, training
and evaluation remain unimplemented pending the expected decisions on 27 Nov.

## Windows and Linux setup (uv)

Install Python 3.12 and [uv](https://docs.astral.sh/uv/getting-started/installation/),
then run from the repository root:

```bash
uv sync --extra dev
```

`.python-version` selects Python 3.12 locally; the package supports Python 3.12
and newer. Windows and Linux use the explicit CUDA 12.8 PyTorch index for the
RTX 5070 requirement. CPU execution is also supported.

## Colab setup

Open [notebooks/00_colab_setup.ipynb](notebooks/00_colab_setup.ipynb).
It clones this repository, runs `pip install -e . --no-deps`, installs the core
runtime dependencies from `requirements-colab.txt`, mounts Drive and sets
`LORDOSIS_DATA_ROOT`. It retains Colab's installed torch and torchvision.
Python 3.12 or newer is supported.

## Data

SPIDER (Zenodo 10159290), download script pending.
Source: [Zenodo record 10159290](https://zenodo.org/records/10159290), CC BY 4.0.
See [data/README.md](data/README.md) for the expected folders.
Data paths will use `LORDOSIS_DATA_ROOT`, defaulting to `./data`.

The proposed patient-level split reserves official validation studies for testing
and divides official training studies into train/validation. Once frozen, the
test set is reserved for final evaluation. No split has been created.

## Layout and build order

Build **common → labeling → model**:

```text
configs/
  data/spider.yaml
  labeling/prelabel.yaml
  model/mean_baseline.yaml, resnet18.yaml
src/lordosis/
  common/          shared infrastructure and data/geometry stubs
  labeling/        STEP 1: mask pre-labels and human review stubs
  model/           STEP 2: mean baseline and ResNet-18 stubs
scripts/           download, manifest and preprocessing stubs
data/              raw/spider, processed, labels and splits
notebooks/         Colab setup; EDA, label QC and results notebooks pending
tests/             synthetic CPU checks
outputs/runs/      future run artifacts, ignored by Git
reports/figures/   small report/presentation figures
docs/              decisions, sources and TRIPOD+AI checklist
```

Start with [common](src/lordosis/common), then
[STEP 1 labelling](src/lordosis/labeling/README.md), then
[STEP 2 angle regression](src/lordosis/model/README.md).
See [docs/extensions.md](docs/extensions.md) for the deferred backlog.

## Planned commands

CLI help works without data or weights:

```bash
uv run python -m lordosis.model.train --help
uv run python -m lordosis.model.evaluate --help
```

The intended training interface is:

```bash
uv run python -m lordosis.model.train --config configs/model/resnet18.yaml
uv run python -m lordosis.model.train --config configs/model/resnet18.yaml --set seed=42
```

Training and evaluation currently raise `NotImplementedError`. Config placeholders
contain only the permitted expected values; unresolved settings remain `null`.
Future runs save resolved config, Git commit, environment, metrics, predictions,
figures and checkpoints under `outputs/runs/<YYYYMMDD-HHMM>_<run_name>/`.

## Checks

```bash
uv run ruff check .
uv run pytest
```

Tests use synthetic inputs on CPU and require no data or model weights.
