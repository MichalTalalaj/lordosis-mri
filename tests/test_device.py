"""Exercise accelerator selection without allocating accelerator tensors."""

import pytest
import torch

from lordosis.common.device import amp_dtype, default_num_workers, pick_device


@pytest.mark.parametrize(
    ("cuda", "mps", "expected"),
    [(True, True, "cuda"), (False, True, "mps"), (False, False, "cpu")],
)
def test_device_priority(monkeypatch: pytest.MonkeyPatch, cuda: bool, mps: bool,
                         expected: str) -> None:
    """CUDA takes priority over MPS, which takes priority over CPU."""
    monkeypatch.setattr(torch.cuda, "is_available", lambda: cuda)
    monkeypatch.setattr(torch.backends.mps, "is_available", lambda: mps)
    assert pick_device() == torch.device(expected)


@pytest.mark.parametrize("supported", [True, False])
def test_cuda_amp_dtype(monkeypatch: pytest.MonkeyPatch, supported: bool) -> None:
    """Use bf16 when CUDA supports it and fp16 otherwise."""
    monkeypatch.setattr(torch.cuda, "is_bf16_supported", lambda: supported)
    assert amp_dtype(torch.device("cuda")) == (torch.bfloat16 if supported else torch.float16)


@pytest.mark.parametrize("device", ["cpu", "mps"])
def test_non_cuda_amp_is_disabled(device: str) -> None:
    """CPU/MPS fall back to fp32 represented by None."""
    assert amp_dtype(torch.device(device)) is None


def test_default_amp_uses_selected_device(monkeypatch: pytest.MonkeyPatch) -> None:
    """The no-argument helper respects CPU selection."""
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    monkeypatch.setattr(torch.backends.mps, "is_available", lambda: False)
    assert amp_dtype() is None


@pytest.mark.parametrize(("system", "expected"), [("Windows", 0), ("Linux", 4), ("Darwin", 4)])
def test_num_workers(monkeypatch: pytest.MonkeyPatch, system: str, expected: int) -> None:
    """Windows defaults to zero workers; other platforms default to four."""
    monkeypatch.setattr("lordosis.common.device.platform.system", lambda: system)
    assert default_num_workers() == expected
