Read AGENTS.md completely before doing anything. Then scaffold the repository for the mid-term phase. Do NOT implement any models yet: the must/main/stretch tiers are stubs for now.

## Goal of this task
A working, cross-platform repo (Windows + uv + RTX 5070, Linux + uv, Google Colab) with the shared `common` package, data download and manifest scripts for SPIDER, an EDA notebook that produces figures for our presentation, and passing tests.

## Steps
1. **Project setup**
   - `pyproject.toml` for uv, Python 3.12, package `lordosis` in `src/` layout.
   - Core deps: numpy, pandas, SimpleITK, scikit-image, scikit-learn, scipy, matplotlib, pyyaml, tqdm, torch, torchvision, grad-cam.
   - Extras: `main` = timm, peft; `stretch` = monai; `dev` = pytest, ruff, jupyter, ipykernel.
   - PyTorch from the cu128 index for `sys_platform == 'win32'` and `'linux'` using `[[tool.uv.index]]` (explicit) + `[tool.uv.sources]` (RTX 5070 needs CUDA 12.8+ builds).
   - `requirements-colab.txt` with everything except torch/torchvision.
   - `.gitignore` (data/, outputs/, checkpoints, .venv, __pycache__, .ipynb_checkpoints; keep `data/README.md`, `data/splits/`, `.gitkeep` files), `.gitattributes` (`* text=auto eol=lf`), ruff config.
2. **Folder structure** exactly as AGENTS.md §4, with a `README.md` in each of `src/lordosis/must`, `main`, `stretch`, `labeling` (purpose, planned files, status = "not started"), plus `data/README.md` (how to download SPIDER; Composite = on request, adapter pending) and `docs/decisions.md`, `docs/third_party.md`, `docs/tripod_ai_checklist.md` (checklist headings as a to-do list).
3. **`src/lordosis/common/`** (implement, with type hints and docstrings):
   - `config.py` (load YAML, merge overrides, save resolved copy), `device.py` (cuda→mps→cpu; `amp_dtype()` returns bf16 if supported else fp16 else None; `default_num_workers()` = 0 on Windows), `seed.py`.
   - `io.py`: read `.mha`/`.nii.gz`/`.png` with SimpleITK, return array + spacing + direction; canonical orientation via `sitk.DICOMOrient`.
   - `manifest.py`: schema from AGENTS.md §6, build + validate functions, dataset adapters (`spider` implemented, `composite` raises NotImplementedError with a clear message).
   - `preprocessing.py`: mid-sagittal slice selection (spinal-canal mask centre if available, else central index; `n_slices` 1 or 3), isotropic in-plane resampling BEFORE resize, percentile clip + z-score, pad-to-square, resize. Masks are resampled with nearest neighbour.
   - `augment.py`: only the angle-preserving transforms from §7; forbidden ones must not exist.
   - `geometry.py`: angle between two lines, `(cos 2θ, sin 2θ)` encode/decode, fit a line to the superior border of a binary vertebra mask (and to the inferior border of a disc mask, used for the SPIDER S1 approximation), Cobb angle from two lines.
   - `splits.py`: patient-level train/val/test + GroupKFold; writes/reads `data/splits/split_vN.json`; refuses to overwrite an existing split.
   - `metrics.py`: MAE, RMSE, bias, Bland–Altman (mean diff, LoA), ICC(2,1), Pearson r, per-category MAE with configurable thresholds.
   - `plots.py`: Bland–Altman, predicted-vs-reference scatter, slice + mask overlay, slice + endplate lines.
   - `datasets.py`: torch Dataset reading the manifest + labels CSV; works without labels (for EDA/inference).
   - `explain.py`: stub with a documented Grad-CAM function signature.
4. **Scripts**
   - `scripts/download_spider.py`: query the Zenodo API (`https://zenodo.org/api/records/10159290`) for the file list, then download images.zip, masks.zip, overview.csv and the gradings file into `$LORDOSIS_DATA_ROOT/raw/spider/`. Resume support, md5 check against the API values, extract, `--help`.
   - `scripts/build_manifest.py --dataset spider`: walks the extracted files, fills the manifest (sequence from filename, patient/study id, spacing, n_slices, centre/split from overview.csv, unique vertebra/disc label values, has_L1/has_S1 heuristics, `s1_approximated=True` for SPIDER), writes `data/processed/manifest.csv` and prints a summary.
   - `scripts/preprocess.py`: stub that will cache preprocessed slices as `.npz` (implement the CLI + one-case path).
5. **Notebooks** (thin: they call library code only)
   - `00_colab_setup.ipynb`: clone repo, `pip install -e . --no-deps`, `pip install -r requirements-colab.txt`, mount Drive, set `LORDOSIS_DATA_ROOT`, quick import test. Never reinstall torch.
   - `01_eda_spider.ipynb`: series and patients per sequence and per centre; spacing and slice-count tables and histograms; mask label values found (verify the label numbering empirically and write the findings into `docs/decisions.md`); how many cases have ≥5 lumbar vertebrae and a lowest disc; mid-sagittal overlays for 6 random cases (T1 and T2); one example with auto-fitted endplate lines and the resulting angle (illustration only, not labels). Save every figure to `reports/figures/eda_*.png` at 200 dpi.
6. **Tier stubs**: `must/`, `main/`, `stretch/` contain the files named in AGENTS.md §8–10 with module docstrings describing what they will do, and functions that raise NotImplementedError. Add placeholder configs in `configs/must|main|stretch/` and `configs/data/spider.yaml`, `composite.yaml`.
7. **Tests** (CPU only, no real data, < 60 s total):
   - geometry: known angles between synthetic lines; 2θ encoding round-trip and 180° symmetry; line fit on a synthetic rotated rectangle mask within 1°.
   - augment: every allowed transform keeps the angle between two synthetic lines within 0.5°.
   - preprocessing: anisotropic synthetic image with a known angle → after resampling + resize the measured angle is preserved within 1°.
   - splits: no patient appears in two splits; deterministic with a seed.
   - metrics: hand-computed values on small arrays.

## Rules
- Follow AGENTS.md (paths via `pathlib` + `LORDOSIS_DATA_ROOT`, `if __name__ == "__main__":` guards, no data in git, no absolute paths).
- Commit in logical steps with clear messages.
- Record every assumption in `docs/decisions.md` (dated).

## Done when
- `uv sync --extra dev` works on Windows and Linux; `uv run pytest` and `uv run ruff check .` pass.
- `uv run python scripts/download_spider.py --help` and `uv run python scripts/build_manifest.py --help` work.
- You finish with a short report: what was created, what is stubbed, test results, open questions.
