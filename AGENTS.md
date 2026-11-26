# AGENTS.md — Can AI estimate lordosis directly from MRI?

Instructions for Codex (and any other coding agent) working in this repository.
Read this whole file before making changes. When this file and a prompt disagree,
ask before deviating.

---

## 1. Project in one paragraph

University team project (course: *Artificial Intelligence in Imaging Diagnostics*,
Topic 7). We train a deep-learning model that takes a **sagittal lumbar spine MRI**
and outputs the **lumbar lordosis angle (L1–S1) in degrees**: image → angle regression,
no segmentation at inference. Reference angles are produced by an **AI-assisted labelling**
step: automatic pre-labels computed from the SPIDER masks, then checked and corrected by us.
The repo covers **only what the project requires** (labelling + compact 2D CNN +
required evaluation). Extensions are listed in `docs/extensions.md` and are not built
until the required scope is finished.

Topic 6 (geometric Cobb angle from masks) is a **separate team**. We share no data,
splits, labels or code with them. The two approaches are only contrasted at the final
presentations. Do not add any Topic 6 integration.

Deliverables (15 Jan 2027): code (20 pts), a report following the **TRIPOD+AI**
checklist (20 pts), a presentation (30 pts).

Course rules that affect code:
- Python only.
- **No full copy of an existing public solution.** Adapting code or using pretrained weights is
  allowed. Put the source URL in a comment and in `docs/third_party.md`.
- Code must be documented (docstrings + README + notebooks that show results).

---

## 2. Decisions

| Decision | Value | Status |
|---|---|---|
| Dataset | **SPIDER** (Zenodo record 10159290, CC BY 4.0) | Expected, confirm 27 Nov |
| Reference angles | **AI-assisted**: auto pre-labels from masks → human review (accept / correct / exclude) | Expected, confirm 27 Nov (also: review all cases or test set + sample) |
| Angle definition | **L1–S1**: L1 superior endplate vs S1 superior endplate, degrees, positive = lordosis | Expected, confirm 27 Nov |
| S1 in SPIDER | No sacrum mask → S1 superior endplate ≈ inferior border of the lowest IVD (L5–S1 disc); reviewer can correct | Expected, confirm 27 Nov |
| Test split | Our own, patient-level. Default: SPIDER's official *validation* studies = our test set; official *training* studies split by patient into train/val | Proposed |

Keep these values in config files, never hard-coded. When a status changes, update this table and `docs/decisions.md`.

---

## 3. Team and environments: code must run on all three

| Who | OS | Setup | GPU |
|---|---|---|---|
| Ula | Windows 11 | `uv` | RTX 5070 (12 GB, Blackwell sm_120) |
| Teammate B | Linux | `uv` | unknown / may be CPU |
| Teammate C | Google Colab | `pip` inside notebook | Colab GPU (often T4, no bf16) |

Rules:
- **PyTorch for the RTX 5070 needs a CUDA 12.8+ build** (`cu128` wheels) via the uv
  index in `pyproject.toml` for `win32` and `linux`.
- `requires-python = ">=3.12"`; `.python-version` = 3.12 for local work. Don't pin `<3.13`,
  because Colab may run a newer Python.
- **Colab:** never reinstall torch. `notebooks/00_colab_setup.ipynb` installs
  `pip install -e . --no-deps` + `requirements-colab.txt` (no torch, no jupyter/ipykernel).
- Paths: `pathlib.Path`; data location from env var `LORDOSIS_DATA_ROOT` (default `./data`).
- Windows: `if __name__ == "__main__":` in entry scripts; DataLoader workers via
  `lordosis.common.device.default_num_workers()` (0 on Windows).
- Precision: bf16 autocast if supported, else fp16 + GradScaler, else fp32.
- Deterministic mode sets `CUBLAS_WORKSPACE_CONFIG=:4096:8`.
- Python 3.12 locally, `ruff`, `pytest`, LF line endings.

---

## 4. Repository layout

```
lordosis-mri/
├── AGENTS.md  README.md  pyproject.toml  uv.lock  .python-version
├── requirements-colab.txt  .gitignore  .gitattributes
├── configs/
│   ├── data/spider.yaml          # paths, preprocessing, split settings
│   ├── labeling/prelabel.yaml    # endplate fitting + review settings
│   └── model/                    # mean_baseline.yaml, resnet18.yaml
├── data/                         # GITIGNORED except README.md, .gitkeep, splits/*.json
│   ├── raw/spider/
│   ├── processed/                # manifest.csv, cached slices (.npz)
│   ├── labels/                   # prelabels_vN.csv, angles_human_vN.csv
│   └── splits/                   # split_v1.json (committed once frozen)
├── src/lordosis/
│   ├── common/                   # config, device, seed, io, manifest, preprocessing,
│   │                             # augment, geometry, splits, datasets, metrics, plots
│   ├── labeling/                 # STEP 1: prelabel_from_masks.py, review_tool.py
│   └── model/                    # STEP 2: mean_baseline.py, models.py, train.py, evaluate.py
├── scripts/                      # download_spider.py, build_manifest.py, preprocess.py
├── notebooks/
│   ├── 00_colab_setup.ipynb
│   ├── 01_eda_spider.ipynb
│   ├── 02_labels_qc.ipynb        # auto vs human, inter-rater, exclusions
│   └── 10_model_results.ipynb
├── tests/                        # CPU only, synthetic data, < 60 s
├── outputs/                      # GITIGNORED: runs/<run_name>/
├── reports/figures/              # figures for slides/report (small, committed)
└── docs/                         # decisions.md, third_party.md, tripod_ai_checklist.md, extensions.md
```

Build order: **common → labeling → model.** Do not create folders or code for
extensions. `docs/extensions.md` is a plain list.

---

## 5. Run outputs

`outputs/runs/<YYYYMMDD-HHMM>_<run_name>/`: `config.yaml` (resolved), `git_commit.txt`,
`env.txt`, `metrics.json`, `predictions.csv`, `figures/`, `checkpoints/` (gitignored).

`predictions.csv`: `case_id, patient_id, split, method, angle_ref, angle_pred`.

---

## 6. Data conventions (SPIDER)

Facts from the SPIDER paper:
- 447 sagittal T1/T2/T2-SPACE series from 218 patients, 4 hospitals, `.mha` volumes
  + masks.
- Masks cover vertebrae, IVDs and the spinal canal; **no sacrum**.
- Vertebrae are numbered **from the bottom** (1 = most caudal visible lumbar vertebra,
  not necessarily L5).
- Spacing is about 3.15×0.24×0.24 to 9.63×1.06×1.23 mm (T2 SPACE 0.90×0.47×0.47 mm).
- `overview.csv` gives the official split (179 training / 39 validation studies).

The paper may not describe the label values exactly. **Check the real label values in
`01_eda_spider.ipynb` and record them in `docs/decisions.md`.**

**Manifest** `data/processed/manifest.csv`, one row per series:
`case_id, patient_id, sequence, center, official_split, image_path, mask_path,
spacing_x, spacing_y, spacing_z, n_slices, vertebra_labels, ivd_labels,
n_lumbar_vertebrae, exclude, exclude_reason`.

**Labels:**
- `data/labels/prelabels_vN.csv`: `case_id, slice_index, l1_line (x1,y1,x2,y2), s1_line,
  angle_deg, method_version, flags`
- `data/labels/angles_human_vN.csv`: same plus `status (accepted|corrected|excluded),
  annotator, seconds_spent, timestamp, notes`

Never overwrite a labels file; bump the version.

**Splits:** patient-level; all series of one patient in one split. Once frozen, the test set is
never used for training, tuning, early stopping or threshold choice.

---

## 7. Pre-processing and augmentation: angle-preserving rules (critical)

1. Canonicalise orientation (SimpleITK `DICOMOrient`): superior up, anterior in a fixed direction.
2. Mid-sagittal slice: centre of the spinal-canal mask (fallback: central index). The same slice
   is used for labelling and for the model.
3. **Resample to isotropic in-plane spacing (default 0.5 mm) BEFORE any resize**, because
   non-square pixels distort angles. Masks use nearest neighbour.
4. Intensity: clip to the [0.5, 99.5] percentiles, z-score per image.
5. Pad to square (no stretching), resize to `image_size` (default 256).

Allowed augmentation: rotation (±15°), translation, **uniform** scaling (0.9–1.1),
intensity (gamma, contrast, noise, blur). **Forbidden:** anisotropic scaling, shear,
elastic deformation, vertical flip; horizontal flip off by default.
`tests/test_augment.py` checks that allowed transforms keep the angle between two lines within 0.5°.

---

## 8. STEP 1: AI-assisted labelling (`src/lordosis/labeling/`)

`prelabel_from_masks.py`:
1. Use the mid-sagittal slice from §7 (after resampling).
2. Identify vertebrae by counting from the bottom: lowest lumbar label = L5, fifth from the bottom = L1.
   Flag the case (`flags`) when the vertebra count or shape suggests a transitional vertebra,
   L1 out of view, or a missing lowest disc.
3. **L1 line:** robust line fit (e.g. RANSAC or PCA on the upper boundary pixels) to the
   superior border of the L1 mask. **S1 line:** the same on the inferior border of the lowest IVD.
4. Angle between the lines (`common/geometry.py`), positive = lordosis.
5. Write `prelabels_vN.csv` plus an overlay PNG per case for quick review.

`review_tool.py` (matplotlib, runs locally on Windows/Linux):
- Shows the slice, both lines and the angle.
- Keys: accept / exclude (with reason). Drag line endpoints to correct.
  Next/previous case, autosave.
- Writes `angles_human_vN.csv` with annotator name and time per case.
- Mode for a second annotator on a subset (inter-rater agreement).

`notebooks/02_labels_qc.ipynb`:
- auto vs human difference (MAE, % corrected)
- inter-rater MAE/ICC
- exclusions by reason
- angle distribution

---

## 9. STEP 2: model (`src/lordosis/model/`), the required scope

- `mean_baseline.py`: predicts the training-set mean angle (the floor every model must beat).
- `models.py`: ResNet-18 (torchvision, ImageNet weights). 1-channel input repeated to 3;
  final layer `Linear(512, 1)`.
- `train.py`:
  - AdamW, cosine LR with warm-up, L1 or Huber loss (config)
  - early stopping on **val MAE**
  - AMP per §3, seed control, best checkpoint
  - CLI `uv run python -m lordosis.model.train --config configs/model/resnet18.yaml [--set key=value]`
- `evaluate.py`:
  - writes `metrics.json` and `predictions.csv`
  - **MAE, RMSE, bias** (mean signed error), **Bland–Altman** plot (mean difference, 95% limits)
  - predicted-vs-reference scatter
  - **visual validation per category**: hypo / normal / hyper lordosis (thresholds in config,
    because supine MRI angles are lower than standing X-ray norms) with example images
    showing reference vs predicted values
- Done when `notebooks/10_model_results.ipynb` shows test results for the mean baseline vs
  ResNet-18 with all plots.

---

## 10. Working rules for agents

- Small, focused changes. Before finishing, run `uv run ruff check .` and `uv run pytest` and report the results.
- Type hints and docstrings on public functions. Notebooks only call library code.
- Never commit data, checkpoints or `outputs/`. Never print patient metadata.
- Seed everything. Never use the test split for any decision; if a task seems to need it, stop and ask.
- Stay inside the required scope (§8–9). Ideas beyond it go into `docs/extensions.md` as one line, not code.
- Record assumptions (dated) in `docs/decisions.md`.
- Prefer well-known libraries (torchvision, SimpleITK, scikit-image, scikit-learn) and cite
  adapted code in `docs/third_party.md`.
