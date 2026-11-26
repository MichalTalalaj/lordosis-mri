# Decisions

- 26 Nov 2026: scaffolding created; dataset/labels/angle definition/split pending lecturer and Topic 6
- 26 Nov 2026: Python is constrained to 3.12; uv.lock records resolved dependencies.
  Windows/Linux use the explicit cu128 torch/torchvision index as required.
- 26 Nov 2026: One placeholder YAML per config directory and only the Colab setup
  notebook are created, following the scaffold prompt's narrower scope. Other
  configs/notebooks and all data/model/labeling behavior remain deferred.
- 26 Nov 2026: CLI config overrides use dotted `key=value` strings with YAML values;
  mappings merge recursively, lists/scalars replace, and inputs are not mutated.
  Unresolved dataset, angle source/definition and split values remain null.
- 26 Nov 2026: AMP selects CUDA bf16 when supported, otherwise CUDA fp16;
  MPS/CPU use fp32 (dtype None). Future fp16 training must use GradScaler.
- 26 Nov 2026: requirements-colab.txt is generated from core and all optional
  dependencies, excluding torch/torchvision. It uses unpinned optional packages
  so Colab can retain its existing torch; the setup notebook constrains both
  installed torch versions during pip resolution to prevent replacement.
  Tier implementations remain deferred.
- 26 Nov 2026: Colab defaults to the current public GitHub remote. Optional
  `GITHUB_TOKEN` in Colab Secrets is passed via a temporary git askpass helper,
  never stored in the clone URL or printed. Drive data location is editable.
