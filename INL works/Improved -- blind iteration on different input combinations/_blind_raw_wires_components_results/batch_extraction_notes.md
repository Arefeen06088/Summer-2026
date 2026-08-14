# Blind Raw + Wires + Components Batch Notes

Generated: 2026-07-13T15:03:38

## Scope

Processed cases 1-35 under each case's `Raw + wires + components` folder.

## Resource Rule

Extraction used only raw schematic images, `wires_mask.png`, wire overlays as visual aids, and detected component/logical overlays from the selected folder. GT, GT-derived feedback, sibling resource folders, prior matrices, and evaluators were not read.

## Agents

- Diego: high-recall visual/geometric extractor; round 1 matrices preserve plausible wire contacts with evidence.
- Jennifer: precision reviewer; rounds 2 and 4 apply stricter contact evidence and avoid unlabeled high-degree overconnection.

## Artifacts

- Per case: `nodes_detected.csv`, four round connectivity matrices, four confidence matrices, four edge evidence CSVs, `connectivity_matrix_final.csv`, `connectivity_edges_final.csv`, `case_summary.json`, `extraction_notes.md`, and `token_performance_tracking.csv`.
- Batch: `batch_extraction_summary.csv`, `batch_round_summary.csv`, `batch_token_performance_tracking.csv`, and this note.

Completed cases: 35 / 35.
Missing cases: none.
