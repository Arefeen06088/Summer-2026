# Round 01 Jennifer Notes - Doc 28 Iteration 1

## Scope
I inspected only the doc 28 input resources, prepared inspection crops/artifacts, and Diego's round-01 proposal in `Results/Iteration_1`. The raw schematic was treated as primary evidence. OCR/component/wire overlays and prepared crops were used only as aids. No ground truth, evaluator output, score feedback, or other document/iteration resources were used.

## Summary
- Diego matrix checked as structurally valid: 188 nodes and 196 undirected edges.
- Jennifer refined matrix: 191 nodes and 193 undirected edges.
- Matrix validation: symmetric = true, diagonal zero = true, malformed values = false.
- Final isolated raw-visible inventory/control nodes with no precise supported edge: JB-101, JB-201, V-301, AIT-301, JB-301, DCS-001, CP-101, PLC-101.

## Label And Node Decisions
- Kept Diego's corrected `M-301` -> `MX-301`: the raw label inside the static mixer reads `MX-301`.
- Did not retain `TIC-203` as a separate node; the supported raw label in the temperature-control bypass area is `TCV-203`.
- Collapsed Diego's duplicated `CV-203`/`TCV-203` handling. The raw label on the bypass control valve reads `TCV-203`; I removed the unsupported separate `CV-203` node and kept `TCV-203` on the process line.
- Added raw-visible named connector/header nodes that Diego omitted but that have clear named endpoints: `H-SW-SUP`, `H-CCW-FLTR`, `H-VT-001`, and `OPC-501`.
- Kept Diego's raw-visible added nodes such as `H-N2-001`, `H-CCW-SUC`, `H-CCW-DIS`, `H-SW-RET`, `H-CCW-RET`, `H-CD-001`, `H-SMP-001`, `H-CD-REL`, `H-WW-001`, `H-DR-001`, `H-IA-001`, `VSR`, `TIE-IN`, `HV-103`, and `LI-301` where connected.
- Retained raw-visible inventory/control boxes even where I removed unsupported edges; isolated control boxes are left as nodes rather than inventing panel wiring.

## Changes From Diego
### Added Edges
- `TK-101` - `HV-103`: the TK-101 bottom/drain branch shows `HV-103` above `DV-101`; Diego connected the tank directly to `DV-101`.
- `H-SW-SUP` - `PSV-215`, `H-SW-SUP` - `HV-211A`, `H-SW-SUP` - `HV-211B`: visible SW supply header endpoints.
- `H-CCW-DIS` - `H-CCW-FLTR`: visible transition from discharge/filter outlet area into the filtered CCW header.
- `H-CCW-FLTR` - `HV-201A`, `H-CCW-FLTR` - `HV-201B`, `H-CCW-FLTR` - `HV-203`, `H-CCW-FLTR` - `HV-120`: downstream branches are visually on the filtered CCW header, not directly on every component of `H-CCW-DIS`.
- `H-VT-001` - `VV-151A`: visible named vent header feeding the VV-151/152/153/154 chain.
- `VSR` - `OPC-501`: visible off-page connector immediately downstream of `VSR`.

### Removed Or Replaced Edges
- Removed `TK-101` - `DV-101`; replaced by `TK-101` - `HV-103` and retained `HV-103` - `DV-101`.
- Removed `CV-203` - `TCV-203` with the `CV-203` duplicate node; the raw valve label is `TCV-203`.
- Removed `V-301` - `TK-301`; the calibration pot is raw-visible but I found no pipe or signal termination connecting it to TK-301.
- Removed `JB-101` - `DCS-001`, `JB-201` - `DCS-001`, and `JB-301` - `DCS-001`; dashed signal trunks pass near these boxes but do not visibly terminate on both endpoints.
- Removed `AIT-301` - `DCS-001` and `AIT-301` - `H-CD-001`; the analyzer is on/near signal routing, but I did not see a direct termination to DCS-001 or the chemical dosing header.
- Removed `CP-101` - `PLC-101` and `LCP-401` - `PLC-101`; the panel boxes are visible, but the dashed routing does not visibly terminate on both named boxes.
- Removed direct `H-CCW-DIS` edges to `HV-201A`, `HV-201B`, `HV-203`, and `HV-120`; these were re-anchored through `H-CCW-FLTR`.

## Retained Ambiguous Cases
- Tank level associations (`LSHH-101`, `LSLL-101`, `LT-101`, `LT-301`, `LI-301`, `LSL-301`, `LT-302`, `LT-401`, `LI-401`, `LSHH-401`, `LSL-401`) were retained where the local tank/instrument relationship is visually indicated, even when drawn with dashed instrumentation lines rather than process pipe.
- `H-CD-REL` is retained as the chemical relief header despite partial text obstruction.
- `P-301A` - `PSV-301` and `P-302` - `PSV-302` are retained as visible relief takeoffs to the chemical relief header.
- `LIC-401` - `LCP-401` is retained as an apparent local control-panel signal, but broader panel-to-PLC/CP edges were removed.
- `SOV-401` - `LSL-401` is retained because the LSL signal line visibly reaches the SOV area.

## Rejected Node/Edge Issues
- No anonymous wire nodes, WN IDs, elbows, or unlabeled junctions were introduced.
- Continuation marks (`C1`, `C2`, numbered triangles/bubbles) remain excluded.
- DCS/JB/PLC/CP panel routing was not clique-expanded; only visually terminating relationships were kept.
- Long headers are represented by adjacent named components or explicit named header nodes, not by complete cliques.

## Final Validation
- Node count: 191.
- Undirected edge count: 193.
- Symmetric: yes.
- Diagonal all zero: yes.
- Malformed values: no.
- Validation errors: none.
