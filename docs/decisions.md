# Decisions

- 26 Nov 2026: Scope reduced to SPIDER only, AI-assisted L1–S1 labelling,
  a training-mean baseline and one compact 2D CNN (ImageNet ResNet-18), plus
  required evaluation. Earlier main/stretch tiers and Composite/Mendeley dataset
  candidates are superseded. No Topic 6 data, labels, splits, code or integration
  are shared; the approaches may only be contrasted at the final presentations.
  Optional ideas are listed only in `docs/extensions.md` until required work is done.
- 26 Nov 2026: Expected decisions, to confirm on 27 Nov: SPIDER (Zenodo 10159290,
  CC BY 4.0); AI-assisted pre-labels followed by human accept/correct/exclude review
  (all cases vs test set plus sample still undecided); L1–S1 angle between the L1
  and S1 superior endplates, positive for lordosis; approximate S1's superior
  endplate with the inferior border of the lowest IVD because SPIDER has no sacrum
  mask, with human correction allowed. AGENTS.md decision statuses remain unchanged.
- 26 Nov 2026: Proposed patient-level split: official SPIDER validation studies
  become our test set; official training studies are divided into train/validation.
  No split is created or frozen during cleanup. No test data is used for decisions.
- 26 Nov 2026: Config placeholders are now `data/spider.yaml`,
  `labeling/prelabel.yaml`, `model/mean_baseline.yaml` and `model/resnet18.yaml`.
  Only the values authorized by the cleanup prompt are filled; all other settings
  remain null. Confirm actual vertebra/IVD/canal label values in the future EDA
  notebook before implementing mask processing.
- 26 Nov 2026: Cleanup changes structure and documentation only, apart from the
  requested environment/determinism fixes. Common data stubs are retained;
  labelling/model functions still raise `NotImplementedError`. Build order is
  common → labelling → model. Only the existing Colab setup notebook is retained;
  EDA, label QC and model-results notebooks remain pending implementation.
- 26 Nov 2026: Superseding the initial Python upper bound: package requirement is
  now Python >=3.12, with `.python-version` selecting 3.12 locally. Windows/Linux
  retain the explicit cu128 torch/torchvision index. `uv.lock` is regenerated.
  Deterministic seeding sets the default CUDA workspace config to `:4096:8` before
  enabling deterministic algorithms, preserving an existing environment value.
- 26 Nov 2026: CLI config overrides use dotted `key=value` strings with YAML values;
  mappings merge recursively, lists/scalars replace, and inputs are not mutated.
- 26 Nov 2026: AMP selects CUDA bf16 when supported, otherwise CUDA fp16;
  MPS/CPU use fp32 (dtype None). Future fp16 training must use GradScaler.
- 26 Nov 2026: Superseding the initial optional-dependency export:
  `requirements-colab.txt` contains core runtime dependencies only, excluding
  torch/torchvision and jupyter/ipykernel. Colab installs the project with
  `--no-deps`, then installs that file with existing torch versions constrained.
- 26 Nov 2026: Colab defaults to the current public GitHub remote. Optional
  `GITHUB_TOKEN` in Colab Secrets is passed via a temporary git askpass helper,
  never stored in the clone URL or printed. Drive data location is editable.
- 26 Nov 2026: The completed cleanup prompt and obsolete scaffold prompt are
  replaced by status notices so outdated instructions no longer contradict the
  current scaffold. Their original text remains available in Git history.
