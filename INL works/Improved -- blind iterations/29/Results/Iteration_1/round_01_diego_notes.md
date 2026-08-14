# Doc 29 / Iteration 1 Diego Connectivity Notes

## Source Discipline
Used only doc 29 raw input resources and doc 29 generated inspection crops/overlays under `Input resources` and `Codes and artifacts`. The raw image `raw -- readable_synthetic_pid_ccw_v3_final.png` was primary evidence; overlays and `wire_nodes.csv` were aids only. No ground truth, evaluator output, score feedback, or other document/iteration resources were used.

## Node List Rationale
The matrix preserves all 141 inventory physical-component labels from `component_labels_list.csv` in inventory order. I added 30 raw-visible nodes needed to represent connected named terminals and headers without anonymous wire nodes.

Added raw-visible components beyond inventory: R-101, R-401.

Added off-page connector nodes: OPC-SW-IN, OPC-DMW-001, OPC-VNT-001, OPC-CCW-SUP-A, OPC-CCW-SUP-B, OPC-CCW-SUP-C, OPC-SW-OUT, OPC-CCW-RET-A, OPC-CCW-RET-B, OPC-CCW-RET-C, OPC-N2-001, OPC-CHM-FLL, OPC-SAMPLE-LAB, OPC-IA-001, OPC-RADWASTE, OPC-DRN-001.

Added named header/logical nodes: HDR-SW-101, HDR-VNT-101, HDR-REL-101, HDR-CCW-101, HDR-CCW-102, HDR-CCW-103, HDR-SW-102, HDR-CCW-104, HDR-CHM-501, HDR-SMP-001, HDR-CDR-001, HDR-IA-101.

Omitted as nodes: anonymous `WN-*`, elbows, black dots, t-sections, crossing points, continuation bubbles, boxed line numbers, and raw `TP-*` labels except where already embedded in an inventory node. These were treated as routing annotations.

## Inventory Labels Omitted Or Corrected
No inventory component was dropped. `R-101` and `R-401` were added because both are raw-visible inline components absent from the 141-item inventory. Inventory `P-120` visually aligns with a black point labeled `TP-120`; it was retained under the inventory name and connected only to `HDR-CCW-102`. The task context mentions `FIC-501`, but the inventory/raw analyzer crop show `FT-501`, `AIC-501`, and `AT-501`; no unsupported `FIC-501` node was added.

## Edge Evidence By Region
Top-left supply / TK-101: service-water path `OPC-SW-IN-HV-401-STR-401-FCV-401-HV-402-HDR-SW-101`; `FT-401-FIC-401-FCV-401` loop; makeup path `OPC-DMW-001-HV-100-MOV-100-LV-101-TK-101`; tank level signals among `LSHH/LIC/LT/LSLL-101`; relief/vent via `RD-101`, `PSV-101`, `HV-301`, `HDR-REL-101`, `HDR-VNT-101`, `HV-305`, `OPC-VNT-001`; suction/drain `TK-101-HV-101-STR-101-R-101-HDR-CCW-101` and `TK-101-DV-101`.

P-101 trains: A/B suction branches from `HDR-CCW-101` pass through `HV-111`, strainers, `HV-112`, pumps, check/MOV/HV discharge valves to `HDR-CCW-102`; `LCS-101A/B` connect to their pumps; `DV-102A` connects to `P-101A`.

Discharge / filters / HXs: `HDR-CCW-102` connects to `INJ-501`, retained `P-120`, and `HV-120-SB-120-FCV-101-HV-121`; `FT/FIC-101` controls `FCV-101`; A/B filter-HX trains run from `HV-121` through `HV-122/FLT/HV-123/HV-124/HX/CV/MOV` to `HDR-CCW-103`; service-water headers `HDR-SW-101/102` connect through `HV-411/412` to `HX-101A/B`.

Right supply/sample/return: `HDR-CCW-103` branches to `OPC-CCW-SUP-A/B/C`; `FT/FIC-231C` controls `FCV-231C`; sample branch `HDR-CCW-103-SV-101-SP-101-HDR-SMP-001` ties to `OPC-SAMPLE-LAB`; `HDR-CCW-104` branches through `HV-241A/B/C` to `OPC-CCW-RET-A/B/C`.

Mid controls: pressure-control path `HDR-CCW-102-CV-270-HV-271-FCV-270-HV-261-PCV-260-HV-260-HDR-CCW-104`; `PT/PIC-260` controls `PCV-260`; return/injection path `INJ-502-HV-251-MOV-250-TCV-250-HDR-CCW-104`; `TT/TIC-250` controls `TCV-250`.

Chemical dosing: `OPC-N2-001-NR-101-PCV-501-AG-201-TK-201`; `OPC-CHM-FLL-HV-501-FLT-201-TK-201`; `LIC/LT-201` to `TK-201`; `TK-201-HV-502-STR-201` branches to P-201A/B; pump outlets join `HDR-CHM-501`; `HDR-CHM-501-FCV-501-SV-501-NRV-501-MIX-501-HV-530-SB-501-HV-532-INJ-502`; `HV-531` is a connected side branch; visible `FT-501`, `AIC-501`, and `AT-501` signal edges are included.

Controls and drain/sump: `DCS-001-CP-101-PLC-301`; `LIC-301-LT-301-TK-301` and `LIC-301-PLC-301`; `PLC-301-DV-302` control candidate; `TK-301-P-301-DV-302-OPC-RADWASTE` with `LCS-301-P-301`; closed-drain header `HDR-CDR-001` connects `SEP-301`, `TK-301`, `DV-301`, and `OPC-DRN-001`; instrument air path `OPC-IA-001-FR-101-HDR-IA-101` plus visible actuator branches to `PCV-501` and `LV-101`.

## Ambiguous High-Recall Candidates For Jennifer Precision Review
- `P-120` appears raw-labeled as `TP-120`; retained only as an inventory node on `HDR-CCW-102`.
- `R-101` and `R-401` are raw-visible but absent from inventory; both were added as physical components.
- `HV-411/412` service-water branches are modeled through `HX-101A/B`; the filter/HX area has close crossings and port interpretation may need review.
- `PCV-501-AG-201` may represent N2/utility service to the tank/agitator assembly rather than direct process flow.
- `SP-101-HDR-SMP-001`, `PLC-301-DV-302`, and `HDR-IA-101` actuator branches are high-recall inclusions from visible named endpoints/signals.

## Final Validation Counts
- Nodes: 171 total = 141 inventory + 30 added.
- Undirected edges: 179.
- Matrix checks: blank top-left=True; row/column order identical=True; duplicate node names=False.
- Value checks: only `0/1` values=True; diagonal zero=True; symmetric=True.
