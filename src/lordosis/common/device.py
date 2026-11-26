"""Select the available compute device, AMP dtype and platform worker default."""

import platform

import torch


def pick_device() -> torch.device:
    """Choose CUDA first, then MPS, and otherwise CPU."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def amp_dtype(device: torch.device | None = None) -> torch.dtype | None:
    """Choose CUDA bf16/fp16, or None for fp32 on CPU/MPS.

    Future fp16 training must pair autocast with torch.amp.GradScaler.
    """
    selected = pick_device() if device is None else device
    if selected.type == "cuda":
        return torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    return None


def default_num_workers() -> int:
    """Default to zero DataLoader workers on Windows and four elsewhere."""
    return 0 if platform.system() == "Windows" else 4
