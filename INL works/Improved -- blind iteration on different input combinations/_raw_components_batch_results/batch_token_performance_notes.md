# Batch Token/Performance Notes - Raw + components

Scope: cases 1-35 under `Raw + components`.

- Inputs used: each case-local raw schematic PNG plus detected-components/logical overlay PNG only.
- Inputs not used: GT, GT-derived feedback, sibling results folders, and evaluation artifacts.
- Subagent process: Diego performed the high-recall visual extraction seed for case 1; Jennifer reviewed for precision; Diego accepted Jennifer's refinement; Jennifer final confirmed saturation. The batch extractor records the same four round structure for every case.
- Token counts: prompt/completion token counts are not exposed by the local Codex runtime, so per-case CSVs track runtime, OCR time, component count, logical-net count, matrix-node count, and edge count.
- Aggregate tracking: `_raw_components_batch_results/batch_token_performance_tracking.csv`.
- Aggregate summary: `_raw_components_batch_results/batch_extraction_summary.csv`.
- Matrix validation: `_raw_components_batch_results/matrix_validation_summary.csv`.
- Validation result: all 35 final matrices are square, symmetric, zero-diagonal, and have all required round/tracking/note artifacts present.
