"""Check reproducibility on CPU only."""

import random

import numpy as np
import pytest
import torch

from lordosis.common.seed import seed_everything


def test_seed_repeats_all_cpu_random_streams(monkeypatch: pytest.MonkeyPatch) -> None:
    """Resetting the same seed repeats Python, NumPy and torch draws."""
    previous = torch.are_deterministic_algorithms_enabled()
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    try:
        seed_everything(42, deterministic=True)
        first = (random.random(), np.random.rand(4), torch.rand(4))
        seed_everything(42, deterministic=True)
        second = (random.random(), np.random.rand(4), torch.rand(4))
        assert first[0] == second[0]
        np.testing.assert_array_equal(first[1], second[1])
        assert torch.equal(first[2], second[2])
        assert torch.are_deterministic_algorithms_enabled()
        seed_everything(7, deterministic=False)
        assert not torch.are_deterministic_algorithms_enabled()
        assert random.random() != first[0]
    finally:
        torch.use_deterministic_algorithms(previous)
