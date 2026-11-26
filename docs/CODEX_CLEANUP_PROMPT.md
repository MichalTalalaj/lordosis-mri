AGENTS.md has been replaced with a new version. Read it completely first. The project scope is now limited to the required work: SPIDER only, AI-assisted L1–S1 labelling, one compact 2D CNN, no Topic 6 integration, no extension tiers. Bring the existing scaffold in line with the new AGENTS.md. This is a cleanup/restructure task: **do not implement new functionality.**

## Remove
- `src/lordosis/main/` and `src/lordosis/stretch/` (whole folders), `configs/main/`, `configs/stretch/`.
- `src/lordosis/common/explain.py`, and any Topic 6 references (e.g. `compare_topic6`).
- The `main` and `stretch` optional-dependency extras in `pyproject.toml`, and timm/peft/monai from `requirements-colab.txt`.
- `data/raw/composite/` and every mention of the Composite/Mendeley dataset.

## Rename / restructure
- `src/lordosis/must/` → `src/lordosis/model/` (update imports, tests, README links, CLI examples: `python -m lordosis.model.train`).
- Configs → `configs/data/spider.yaml`, `configs/labeling/prelabel.yaml`, `configs/model/mean_baseline.yaml`, `configs/model/resnet18.yaml`. They are placeholders with the keys implied by AGENTS.md §6–9. Pre-fill only the decided/expected values (`dataset: spider`, `angle_definition: L1-S1`, `angle_source: ai_assisted`, `s1_approximation: lowest_ivd_inferior_border`, `image_size: 256`, `in_plane_spacing_mm: 0.5`, `allow_hflip: false`), each with a comment `# expected, confirm 27 Nov` where AGENTS.md §2 says so. Everything else stays `null`.
- Labelling stubs per AGENTS.md §8: `labeling/prelabel_from_masks.py`, `labeling/review_tool.py` (docstrings describing the planned behaviour, functions raising `NotImplementedError("pending: …")`), plus `labeling/README.md` marked as STEP 1.
- `model/README.md` marked as STEP 2, describing the required scope only.
- Remove `explain.py` from `common/__init__.py` if it is listed there. Keep the other `common/` stubs.

## Fixes
1. `pyproject.toml`: `requires-python = ">=3.12"`; add `.python-version` with `3.12`; re-lock with `uv lock`.
2. `requirements-colab.txt`: core runtime deps only (no torch/torchvision, no jupyter/ipykernel; pytest/ruff are fine).
3. `.gitignore`: allow `data/splits/*.json` to be committed (keep the rest of `data/` ignored).
4. `common/seed.py`: when `deterministic=True`, call `os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")` before enabling deterministic algorithms; extend the seed test to check the variable is set.

## Docs
- `README.md`: update the layout overview and run commands (common → labeling → model). Data section: "SPIDER (Zenodo 10159290), download script pending". Remove tier/extension mentions except a pointer to `docs/extensions.md`.
- `data/README.md`: SPIDER only (source, licence CC BY 4.0, expected folder `data/raw/spider/`, download pending).
- New `docs/extensions.md`: short bullet backlog: DINOv2/foundation encoder, multi-task endplate/segmentation heads, uncertainty output, Grad-CAM, 2.5D/3D input, ensembles + TTA, leave-one-hospital-out, T1↔T2 transfer. Mark it "not in scope until the required work is done".
- `docs/decisions.md`: add a dated entry (26 Nov 2026) summarising this scope reduction and the expected decisions from AGENTS.md §2. Remove/annotate earlier entries that mention main/stretch tiers or Composite.
- `notebooks/00_colab_setup.ipynb`: keep, just make sure it still works with the new requirements file and has no references to removed extras.

## Rules
- Do not create a split file, download data, or implement labelling/model logic.
- Small logical commits, e.g. "Remove extension tiers and Topic 6/Composite references", "Rename must to model", "Restructure configs", "Fix Python pin, Colab requirements, split ignore, CUDA determinism", "Update docs for reduced scope".
- Before the final commit: `uv sync --extra dev`, `uv run ruff check .`, `uv run pytest`. All must pass. Then `git push origin main`.

## Done when
- The tree matches AGENTS.md §4. No `main/`, `stretch/`, `explain.py`, Composite or Topic 6 references remain (check with `git grep -i -E "stretch|composite|topic.?6|dinov2|explain"`; only `docs/extensions.md`, `docs/decisions.md` and AGENTS.md may mention them).
- `uv run python -m lordosis.model.train --help` works; tests and ruff pass.
- Finish with a short report: what was removed/renamed, test + ruff results, the git grep output.
