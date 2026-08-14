# Connectivity Extraction Report

Document: 19
Iteration: 1
Generated: 2026-07-15T06:44:54

## Inputs Used

- raw -- synthetic_npp_electrical_schematic_v3.png
- detected_components_overlay.png
- wires_mask.png
- wires_mask_overlay.png
- derived visual crops generated under results/visual_crops

No GT or GT-derived files were used. No off-the-shelf OCR was used.

## Round Summary

- Diego R1: high-recall extraction with accepted edges plus uncertain candidates.
- Jennifer R1: precision review removed visually unsupported candidates and corrected MOV601, lower DC/control, and RPS boundaries.
- Diego R2: agreed that Jennifer R1 was saturated with no additional edges.
- Jennifer R2: replied AGREE/SATURATED with no additional deltas.

## Final Counts

- Final nodes: 202
- Final accepted undirected edges: 200
- Uncertain/excluded candidate edges: 17

## Key Precision Decisions

- BUS-480-A/B are not connected to CTRL-PWR-DC-DIST-A/B because no explicit visible tap/junction is present.
- RELAY-A### nodes are connected to MCC-### only; no direct RELAY-A### to RELAY-K### connection is visible.
- MOV601 has separate VALVE-MOV601 to INST-601 and VALVE-MOV601 to LS-MOV601 branches; only LS-MOV601 continues to JB-601.
- PN-RPS-B is not connected to INST-RPS701 without a visible line.
- CHGR-125B crosses BUS-120AC-B without a junction dot, so no connection is recorded.

## Token Usage

Expected estimated total tokens across main-agent and subagent calls: 122300. See token_usage_estimate.md and usage_estimate.json for low/expected/high bounds and call-level estimates.

## Final Files

- final_sparse_edges.csv
- final_connectivity_matrix.csv
- round01_diego_sparse_edges.csv
- round01_diego_connectivity_matrix.csv
- round01_jennifer_sparse_edges.csv
- round01_jennifer_connectivity_matrix.csv
- round02_diego_sparse_edges.csv
- round02_diego_connectivity_matrix.csv
- round02_jennifer_sparse_edges.csv
- round02_jennifer_connectivity_matrix.csv
- uncertain_excluded_edges.csv
