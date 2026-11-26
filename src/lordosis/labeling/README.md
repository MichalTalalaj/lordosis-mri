# STEP 1 — AI-assisted labelling

Status: **not started**. Functions remain stubs raising `NotImplementedError`.
Build after common infrastructure, before STEP 2 angle regression, and after
lecturer confirmation of the expected decisions on 27 Nov.

- `prelabel_from_masks.py`: use the isotropically resampled mid-sagittal slice,
  count vertebrae from the bottom, flag ambiguous anatomy or missing structures,
  and robustly fit the L1 superior and lowest IVD inferior borders. Compute the
  L1–S1 angle and write a new versioned pre-label CSV plus case overlay PNGs.
- `review_tool.py`: matplotlib slice/line/angle display, draggable endpoints,
  accept/exclude keys with exclusion reasons, case navigation and autosave.
  Record review status, annotator, elapsed time, timestamp and notes in a new
  human-label CSV version. Support a second annotator on a subset.

Never overwrite an existing labels file. The planned labels QC notebook will
compare auto vs human angles, inter-rater MAE/ICC, exclusions and angle distributions.
