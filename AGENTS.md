# AGENTS.md — Can AI estimate lordosis directly from MRI?

Instructions for Codex (and any other coding agent) working in this repository.
Read this whole file before making changes. When this file and a prompt disagree,
ask before deviating.

---

## 1. Project in one paragraph

University team project (course: *Artificial Intelligence in Imaging Diagnostics*,
Topic 7). We train deep-learning models that take a **sagittal lumbar spine MRI**
and output the **lumbar lordosis angle in degrees** (image → angle regression, no
segmentation at inference). Our results will be compared, on the **same test set
and the same angle definition**, against Topic 6, which computes the angle
geometrically from vertebral body masks (Cobb angle from L1 and S1 endplates).
Final deliverables (15 Jan 2027): code (20 pts), a report following the
**TRIPOD+AI** checklist (20 pts) and a presentation (30 pts).

Course rules that affect code:
- Python only (PyTorch, SimpleITK/pydicom, scikit-learn, etc.).
- **No full copy of an existing public solution.** Adapting or using pretrained
  weights is allowed. When you adapt code from somewhere, put the source URL in a
  comment and add it to `docs/third_party.md`.
- Code must be documented (docstrings + README + notebooks that show results).

---

## 2. Status of open decisions (update this section when they are settled)

| Decision | Current assumption | Status |
|---|---|---|
| Dataset | Support **both** SPIDER (Zenodo 10159290, 3D `.mha`) and the Mendeley "Composite" mid-sagittal dataset (k3b363f3vz v2, 2D, L1–L5 + S1 masks, has angles). Code must be dataset-agnostic via the manifest (§6). | Waiting for lecturer |
| Ground-truth angles | Pluggable `angle_source`: `reference` (given by dataset), `auto_from_mask` (pre-label), `human` (verified/corrected). | Waiting for lecturer |
| Angle definition | **L1–S1**: angle between the superior endplate of L1 and the superior endplate of S1, degrees, positive = lordosis. L1–L5 must be selectable in config. | To confirm with lecturer + Topic 6 |
| SPIDER sacrum | SPIDER does not segment the sacrum and numbers vertebrae from the bottom (label 1 = most caudal *visible* lumbar vertebra, not necessarily L5). S1 superior endplate is approximated by the inferior border of the lowest IVD. Flag every such case. | To confirm |
| Test split | One frozen, patient-level split shared with Topic 6 (`data/splits/split_v1.json`). | To agree with Topic 6 |

Do not hard-code any of these: put them in config files.

---

## 3. Team and environments — code must run on all three

| Who | OS | Setup | GPU |
|---|---|---|---|
| Ula | Windows 11 | `uv` | RTX 5070 (12 GB, Blackwell sm_120) |
| Teammate B | Linux | `uv` | unknown / may be CPU |
| Teammate C | Google Colab | `pip` inside notebook | Colab GPU (often T4, no bf16) |

Rules:
- **PyTorch for the RTX 5070 needs a CUDA 12.8+ build** (PyTorch ≥ 2.7, `cu128`
  wheels). Configure this in `pyproject.toml` with a uv index
  (`https://download.pytorch.org/whl/cu128`, `explicit = true`) and
  `[tool.uv.sources]` for `torch` and `torchvision` on `win32` and `linux`.
- **Colab:** never reinstall torch. `notebooks/00_colab_setup.ipynb` clones the
  repo, runs `pip install -e . --no-deps`, then `pip install -r requirements-colab.txt`
  (everything except torch/torchvision), mounts Google Drive and sets `LORDOSIS_DATA_ROOT`.
- Paths: always `pathlib.Path`. Data location comes from env var
  `LORDOSIS_DATA_ROOT` (default `./data`). No absolute or OS-specific paths.
- Windows: every entry script needs `if __name__ == "__main__":`. DataLoader
  `num_workers` comes from config (default 0 on Windows, 4 elsewhere —
  `lordosis.common.device.default_num_workers()`).
- Device + precision: `lordosis.common.device` picks `cuda` → `mps` → `cpu`.
  Use autocast with **bf16 if supported, else fp16 with GradScaler** (T4), else fp32.
- Line endings: add `.gitattributes` with `* text=auto eol=lf`.
- Python 3.12. Formatting/linting with `ruff`. Tests with `pytest`.

---

## 4. Repository layout

```
lordosis-mri/
├── AGENTS.md
├── README.md                 # setup for Windows/Linux/Colab, how to run each tier
├── pyproject.toml            # uv project; extras: [main], [stretch], [dev]
├── uv.lock
├── requirements-colab.txt    # generated, no torch
├── .gitignore  .gitattributes
├── configs/
│   ├── data/                 # spider.yaml, composite.yaml
│   ├── must/                 # mean_baseline.yaml, resnet18.yaml
│   ├── main/                 # dino_multitask.yaml + ablation variants
│   └── stretch/              # volumetric.yaml, ensemble.yaml, loho.yaml
├── data/                     # GITIGNORED (only README.md + .gitkeep committed)
│   ├── raw/spider/  raw/composite/
│   ├── processed/            # manifest.csv, preprocessed slices (.npz)
│   ├── labels/               # angles_<source>_v<N>.csv
│   └── splits/               # split_v1.json (committed exception — small, shared)
├── src/lordosis/
│   ├── common/               # shared by ALL tiers
│   │   ├── config.py  device.py  seed.py
│   │   ├── io.py             # read .mha/.png/.nii, orientation canonicalisation
│   │   ├── manifest.py       # build/validate manifest.csv
│   │   ├── preprocessing.py  # slice selection, resampling, normalisation
│   │   ├── augment.py        # ANGLE-PRESERVING augmentations only (§7)
│   │   ├── geometry.py       # endplate extraction from masks, angle maths
│   │   ├── splits.py         # patient-level splits, k-fold
│   │   ├── datasets.py       # torch Dataset(s) reading the manifest
│   │   ├── metrics.py        # MAE, RMSE, bias, Bland–Altman, ICC, per-category
│   │   ├── plots.py          # Bland–Altman, scatter, overlays, error by category
│   │   └── explain.py        # Grad-CAM / attention maps
│   ├── labeling/             # AFTER the mid-term: pre-labels + review tool
│   │   ├── prelabel_from_masks.py
│   │   └── review_tool.py    # click/accept/correct endplates, writes labels CSV
│   ├── must/                 # TIER 1 — baseline (§8)
│   ├── main/                 # TIER 2 — foundation model + multi-task (§9)
│   └── stretch/              # TIER 3 — extras / ablations (§10)
├── scripts/
│   ├── download_spider.py
│   ├── build_manifest.py
│   └── preprocess.py
├── notebooks/
│   ├── 00_colab_setup.ipynb
│   ├── 01_eda_spider.ipynb
│   ├── 02_eda_composite.ipynb
│   ├── 10_must_results.ipynb
│   ├── 20_main_results.ipynb
│   └── 30_stretch_results.ipynb
├── tests/                    # pytest; must run on CPU in < 60 s, no real data
├── outputs/                  # GITIGNORED: runs/<tier>/<run_name>/
├── reports/figures/          # figures we want in slides/report (committed, small)
└── docs/
    ├── third_party.md        # sources of adapted code + pretrained weights
    ├── decisions.md          # dated log of decisions (dataset, labels, split…)
    └── tripod_ai_checklist.md
```

### Tier rules
- Tiers are built **in order: must → main → stretch.** Do not start a tier until
  the previous one trains, evaluates and has a results notebook.
- Code shared between tiers lives **only** in `src/lordosis/common/`. A tier may
  import from `common`, and `main`/`stretch` may import from lower tiers, never
  the other way round.
- Each tier folder has its own `README.md` (what it does, how to run, status).
- Each tier has `train.py` and `evaluate.py` runnable as modules:
  `uv run python -m lordosis.must.train --config configs/must/resnet18.yaml`.
- Dependencies: core deps in `[project.dependencies]`; tier-specific ones in
  extras (`main`: timm, peft; `stretch`: monai). Ask before adding anything heavy.

---

## 5. Run outputs (same format for every tier — Topic 6 will use it too)

`outputs/runs/<tier>/<YYYYMMDD-HHMM>_<run_name>/`:
- `config.yaml` (resolved copy), `git_commit.txt`, `env.txt`
- `metrics.json` (val/test MAE, RMSE, bias, LoA, ICC, per-category MAE)
- `predictions.csv` with columns:
  `case_id, patient_id, split, method, angle_ref, angle_pred, sigma_pred, angle_source`
  (`sigma_pred` empty if the model has no uncertainty)
- `checkpoints/` (gitignored), `figures/`

`method` names: `mean_baseline`, `resnet18`, `dino_multitask`, … Topic 6 writes
`geometric_cobb` into the same format so we can compare with one script.

---

## 6. Data conventions

**Manifest** `data/processed/manifest.csv`: one row per image series:
`case_id, patient_id, dataset, sequence (T1|T2|T2SPACE|unknown), center,
image_path, mask_path, spacing_x, spacing_y, spacing_z, n_slices, has_L1, has_S1,
s1_approximated (bool), exclude (bool), exclude_reason`.

**Labels** `data/labels/angles_<source>_v<N>.csv`:
`case_id, angle_deg, definition (L1-S1|L1-L5), source (reference|auto_from_mask|human),
annotator, timestamp, notes`. Never overwrite a labels file: bump the version.

**Splits**: patient-level. All series of a patient (e.g. T1 and T2) go into the same
split. `split_v1.json` is frozen once agreed; the **test set is never used for
training, tuning, early stopping or threshold choice.** Tuning uses validation
or k-fold CV on train+val.

SPIDER specifics: `.mha` volumes, voxel spacing ranges from about 3.15 × 0.24 ×
0.24 mm to 9.63 × 1.06 × 1.23 mm (T2 SPACE: 0.90 × 0.47 × 0.47 mm). It has
vertebra, IVD and spinal canal masks, no sacrum mask, and vertebra labels are
numbered from the bottom. The official split is in `overview.csv` (179 train / 39 validation studies).
Inspect the actual label values in `01_eda_spider.ipynb`. Do not trust this file
over the data.

---

## 7. Preprocessing and augmentation — angle-preserving rules (critical)

The label is an **angle**, so any transform that changes angles corrupts labels.

Preprocessing (`common/preprocessing.py`):
1. Canonicalise orientation (SimpleITK `DICOMOrient`) so all images face the
   same way: superior up, anterior in a fixed direction.
2. Select the mid-sagittal slice: centre of the spinal-canal mask if one is available,
   otherwise the central index. Option `n_slices: 1|3` (3 = 2.5D, adjacent slices
   as channels).
3. **Resample to isotropic in-plane spacing** (default 0.5 mm) BEFORE any resize.
   Non-square pixels distort angles.
4. Intensity: clip to [0.5, 99.5] percentiles, then z-score per image.
5. Pad to square (no stretching), then resize to `image_size` (must: 256;
   main: 448 = 32 × 14 for ViT/14).
6. Apply the same geometric transforms to masks and endplate targets.

Allowed augmentations: rotation (±15°), translation, **uniform** scaling
(0.9–1.1), intensity (gamma, contrast, Gaussian noise, bias field, blur).
**Forbidden:** anisotropic scaling, shear, elastic deformation, vertical flip.
Horizontal (anterior–posterior) flip is off by default (`allow_hflip: false`).
`tests/test_augment.py` must check that the allowed transforms keep the
angle between two synthetic lines within 0.5°.

---

## 8. TIER 1 — MUST (`src/lordosis/must/`)

Goal: a complete, honest baseline pipeline end-to-end. This is the minimum we
must deliver.

- `mean_baseline.py`: always predicts the training-set mean angle. This is the floor every model must beat.
- `models.py`: ResNet-18 (torchvision, ImageNet weights). The 1-channel input is
  repeated to 3 channels and the final layer is replaced with `Linear(512, 1)`.
- `train.py`: AdamW, cosine LR with warm-up, L1 or Huber loss (config), early
  stopping on **val MAE**, AMP per §3, seed control, checkpoint best model.
- `evaluate.py`: writes `metrics.json`, `predictions.csv`, Bland–Altman plot,
  predicted vs reference scatter, error by category (hypo / normal / hyper;
  thresholds in config because supine MRI values are lower than standing X-ray norms),
  Grad-CAM overlays for best/median/worst cases.
- Optional in this tier: 5-fold patient-level CV on train+val to report mean ± SD.
- Done when: `notebooks/10_must_results.ipynb` shows test metrics for
  mean_baseline vs resnet18 with all plots.

---

## 9. TIER 2 — MAIN (`src/lordosis/main/`)

Goal: a "geometry-aware direct regressor" that is still image → angle at inference.

- Backbone: **DINOv2 ViT-S/14** via timm (`vit_small_patch14_dinov2.lvd142m`),
  option ViT-B/14. Fine-tune strategy in config: `frozen | last_n_blocks | lora` (peft).
  Must fit in 12 GB with AMP: start with batch 16 at 448 px and gradient accumulation.
- Heads (`models.py`), each switchable in config for ablations:
  1. **Angle head with uncertainty:** outputs `mu`, `log_var`, trained with Gaussian NLL
     (option β-NLL). `sigma_pred` goes into predictions.csv.
  2. **Endplate orientation head:** predicts L1 and S1 superior-endplate directions.
     A line has no direction, so encode each as `(cos 2θ, sin 2θ)`.
     **Consistency loss** between `mu` and the angle derived from the two predicted endplates.
     Targets come from masks via `common/geometry.py`.
  3. **Auxiliary segmentation head (training only):** light decoder on patch tokens
     predicting vertebra masks where masks exist. It is masked out of the loss when no mask
     exists and is **not used at inference**.
- `losses.py`: weighted sum, weights in config.
- `evaluate.py`: everything from must, plus uncertainty quality (95% interval
  coverage, correlation of |error| with sigma), attention/Grad-CAM maps, and a
  comparison table vs must.
- Ablations (configs in `configs/main/`): no aux heads / +endplate / +seg / all;
  frozen vs last_n vs LoRA; DINOv2 vs ResNet-18; T1-only vs T2-only vs both.
- Done when: `notebooks/20_main_results.ipynb` has the ablation table and plots.

---

## 10. TIER 3 — STRETCH (`src/lordosis/stretch/`)

Only after main is done. Each item is independent; pick by value.
- `volumetric.py`: 3D input (SPIDER only), e.g. MONAI 3D ResNet on a cropped lumbar volume.
- `ensemble.py`: ensemble of k-fold / multi-seed models (mean + spread as uncertainty).
- `tta.py`: test-time augmentation with angle-preserving rotations.
- `loho.py`: leave-one-hospital-out evaluation (SPIDER has 4 centres).
- `cross_sequence.py`: train on T1 and test on T2, and the reverse.
- `compare_topic6.py`: joint analysis with Topic 6 predictions (paired errors, Bland–Altman
  A vs B, failure cases side by side). Move this to `common/` if it is needed earlier.

---

## 11. Labelling tooling (`src/lordosis/labeling/`, after the mid-term)

AI-assisted annotation: angles computed automatically from masks become **pre-labels**,
and a human accepts or corrects each one in `review_tool.py` (matplotlib or a
small local web UI showing the slice, the two fitted endplate lines and the angle;
drag endpoints to correct). The tool writes `angles_human_vN.csv`, logs time
per case, and supports a second pass by another annotator on a subset (for
inter-rater agreement). Do not build this before the lecturer confirms the labelling approach.

---

## 12. Working rules for agents

- Small, focused changes. Before finishing, run `uv run ruff check .` and
  `uv run pytest`, and report the results.
- Type hints and docstrings on public functions. No notebooks with logic that
  is not also in `src/`. Notebooks only call library code and show results.
- Never commit data, checkpoints or `outputs/`. Never print or log patient metadata.
- Seed everything (`common/seed.py`). Report mean ± SD over seeds/folds where cheap.
- Never touch the test split for any decision. If a task seems to need it, stop and ask.
- If something in §2 is still unresolved and blocks you, implement the
  configurable version and note the assumption in `docs/decisions.md`.
- Prefer well-known libraries (torchvision, timm, SimpleITK, scikit-image,
  pytorch-grad-cam) over custom implementations; cite them in `docs/third_party.md`.
