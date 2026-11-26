"""Compute MAE, RMSE, bias, Bland–Altman limits, ICC and category errors in the future."""

from collections.abc import Sequence


def compute_metrics(angle_ref: Sequence[float], angle_pred: Sequence[float]) -> dict[str, float]:
    """Compute MAE, RMSE, bias, Bland–Altman limits, ICC and category errors in the future."""
    raise NotImplementedError("pending: evaluation conventions pending")
