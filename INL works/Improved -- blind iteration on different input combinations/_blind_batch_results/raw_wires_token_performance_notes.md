# Raw + wires Token/Performance Notes

Run scope: cases 1-35, using only each case's `Raw + wires` input folder.

- Extraction used raw PNG, `wires_mask.png`, and `wires_mask_overlay.png`.
- OCR/component labels were generated from the raw PNG during this run.
- No GT, evaluator feedback, existing matrices, or GT-derived files were used for extraction.
- Diego round 1 stores high-recall matrices; Jennifer round 2 stores precision-reviewed matrices; Diego round 3 and Jennifer round 4 record saturation/agreement.
- Actual prompt/completion token counts are not exposed by this local Codex runtime, so token columns remain blank and runtime/node/edge counts are tracked instead.
- Targeted high-resolution reruns were applied to cases 2, 4, 14, 17, and 19 after the batch audit found sparse first-pass outputs.
