# STEP 2 — Angle regression

Status: **not started**. Modules remain explicit stubs raising `NotImplementedError`.
Build after common infrastructure and STEP 1 labelling.

- `mean_baseline.py`: predict the training-set mean angle.
- `models.py`: ImageNet ResNet-18, repeat one input channel to three, `Linear(512, 1)`.
- `train.py`: AdamW, cosine learning rate with warm-up, configured L1/Huber loss,
  early stopping on validation MAE, device-aware AMP, seed control and best checkpoint.
- `evaluate.py`: MAE, RMSE, bias, Bland–Altman limits and plot, predicted-vs-reference
  scatter, and hypo/normal/hyper examples with configured MRI category thresholds.

Planned outputs follow AGENTS.md: resolved config, commit/environment records,
metrics, predictions, figures and checkpoints under `outputs/runs/`.
Patient-level splits keep the test set out of training and tuning.

CLI help: `uv run python -m lordosis.model.train --help`.
Planned training command:

```bash
uv run python -m lordosis.model.train --config configs/model/resnet18.yaml
```
