Read AGENTS.md completely before doing anything. This task is **repository scaffolding only**. The dataset, labelling method, angle definition and test split are NOT decided yet (see AGENTS.md §2), so do not write anything that depends on them.

## In scope
1. **Project setup**
   - `pyproject.toml` for uv, Python 3.12, package `lordosis` in a `src/` layout.
   - Core deps: numpy, pandas, SimpleITK, scikit-image, scikit-learn, scipy, matplotlib, pyyaml, tqdm, torch, torchvision.
   - Extras: `main` = timm, peft; `stretch` = monai; `dev` = pytest, ruff, jupyter, ipykernel.
   - PyTorch from the cu128 index for `sys_platform == 'win32'` and `'linux'` via `[[tool.uv.index]]` (`explicit = true`) + `[tool.uv.sources]` (the RTX 5070 needs CUDA 12.8+ builds).
   - `requirements-colab.txt`: all deps except torch/torchvision.
   - `.gitignore` (data/, outputs/, checkpoints, .venv, __pycache__, .ipynb_checkpoints; keep `data/README.md` and `.gitkeep` files), `.gitattributes` (`* text=auto eol=lf`), ruff config in `pyproject.toml`.
2. **Folder structure** exactly as AGENTS.md §4. Empty data folders get a `.gitkeep`.
3. **READMEs and docs** (short, no invented facts):
   - Root `README.md`: project one-liner, setup for Windows (uv), Linux (uv) and Colab, how to run tests. Sections for data/training say "TBD: waiting for dataset decision".
   - `README.md` in `src/lordosis/must`, `main`, `stretch`, `labeling`: purpose (from AGENTS.md), planned files, status "not started".
   - `data/README.md`: candidate datasets (SPIDER, Mendeley Composite) listed as "pending decision", no download instructions yet.
   - `docs/decisions.md` (dated log; first entry: "26 Nov 2026: scaffolding created; dataset/labels/angle definition/split pending lecturer and Topic 6"), `docs/third_party.md` (empty table), `docs/tripod_ai_checklist.md` (TRIPOD+AI section headings as an unchecked to-do list).
4. **Infrastructure that is already known.** Implement these with type hints and docstrings:
   - `common/config.py`: load YAML, merge CLI overrides, save a resolved copy.
   - `common/device.py`: pick cuda → mps → cpu; `amp_dtype()` → bf16 if supported, else fp16, else None; `default_num_workers()` → 0 on Windows, 4 elsewhere.
   - `common/seed.py`: seed python/numpy/torch, deterministic flag.
5. **Stubs for everything else.** Every other module in AGENTS.md §4 and §8–11 (rest of `common/`, `labeling/`, `must/`, `main/`, `stretch/`, `scripts/`) is created with:
   - a module docstring describing what it WILL do (taken from AGENTS.md),
   - function/class signatures where obvious, bodies raising `NotImplementedError("pending: <reason>")`,
   - `train.py` / `evaluate.py` with an argparse CLI and `if __name__ == "__main__":` guard.
6. **Config placeholders**: `configs/data/`, `configs/must/`, `configs/main/`, `configs/stretch/` each get one YAML with the expected keys and `null`/TODO values (for example `dataset: null`, `angle_definition: L1-S1  # pending confirmation`).
7. **Notebooks**: `00_colab_setup.ipynb` only: clone repo (read a GitHub token from Colab Secrets if present), `pip install -e . --no-deps`, `pip install -r requirements-colab.txt`, mount Drive, set `LORDOSIS_DATA_ROOT`, import test, print device. Never reinstall torch. No other notebooks yet.
8. **Tests** (CPU only, no data, fast): package imports; config load/merge/save round-trip; `device` functions return valid values; seeding gives identical random numbers twice.

## Out of scope: do NOT do these
- No dataset download, manifest building, data loading or EDA code.
- No preprocessing, augmentation, geometry or metrics implementations (stubs only).
- Do not create any split file (`data/splits/split_v1.json`).
- No model code, no training, no labelling tool.
- Do not download any data or pretrained weights.

## Rules
- Follow AGENTS.md (pathlib + `LORDOSIS_DATA_ROOT`, no absolute paths, no data in git).
- Commit in logical steps with clear messages.
- If something is unclear, choose the minimal option and note it in `docs/decisions.md`.

## Done when
- `uv sync --extra dev` works; `uv run pytest` and `uv run ruff check .` pass.
- `uv run python -m lordosis.must.train --help` prints the CLI.
- You finish with a short report: files created, what is implemented vs stubbed, test results.
