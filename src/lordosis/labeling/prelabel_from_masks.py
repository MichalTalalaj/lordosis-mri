"""STEP 1: plan AI-assisted L1–S1 pre-labels from SPIDER masks."""


def prelabel_from_masks(config: dict[str, object]) -> None:
    """Plan pre-labels on the same isotropically resampled mid-sagittal slice as the model.

    Count vertebrae from the bottom to identify L5 and L1. Flag suspected transitional
    anatomy, L1 out of view or a missing lowest disc. Robustly fit the L1 superior
    border and lowest IVD inferior border (S1 approximation), then compute the
    positive lordosis angle. Save a new versioned CSV and an overlay PNG per case.
    """
    raise NotImplementedError("pending: SPIDER mask pre-labelling after lecturer confirmation")
