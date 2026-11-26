# SPIDER data

Expected dataset: **SPIDER**, [Zenodo record 10159290](https://zenodo.org/records/10159290),
licence **CC BY 4.0**. Confirmation is expected on 27 Nov 2026.

Download pending: `scripts/download_spider.py` is a stub. Setup and tests do not
download data. The expected raw-data folder is `data/raw/spider/`.

Data paths will use `LORDOSIS_DATA_ROOT` (default `./data`):

- `raw/spider/`: source MRI volumes, masks and overview table.
- `processed/`: manifest and cached mid-sagittal slices.
- `labels/`: versioned automatic pre-labels and reviewed human angles.
- `splits/`: patient-level split JSON, committed only once frozen.

Check actual mask label values during EDA and record them in `docs/decisions.md`.
The proposed split reserves official validation studies for final testing.
Never overwrite label files; save a new version.

Data contents are ignored by Git, except this README, `.gitkeep` placeholders
and `splits/*.json`. No split file exists yet.
