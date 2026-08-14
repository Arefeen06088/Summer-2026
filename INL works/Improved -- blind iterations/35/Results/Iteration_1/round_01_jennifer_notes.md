# Round 01 Jennifer Precision-Refined Connectivity Notes

## Scope

Reviewed only doc35 resources and doc35 round files: raw schematic, component inventory/list, Diego Round 01 matrix and notes, generated overlays, wire-node aids, and doc35 inspection crops. I did not use ground truth, evaluator outputs, validation metrics, previous score feedback, or resources outside doc35.

## Summary Of Changes From Diego

- Started from Diego's 179-node / 214-edge high-recall matrix.
- Kept all 144 inventory component labels.
- Kept Diego's 35 added non-inventory named endpoints/headers/tie points because each was visible and useful after review.
- Added one visible named drain valve node: `HV-DRN-2106`, visible on the sample panel drain path.
- Removed 17 Diego edges that were unsupported, overconnected, skipped named/local intermediates, or crossed without a clear connection.
- Added 5 local replacement/support edges: `TT-2120O`-`TAL-2120`, `HX-2120`-`HV-SW-DRAIN`, `HV-DRN-2103`-`SV-2144`, `SAP-2101`-`HV-DRN-2106`, and `HV-DRN-2106`-`H-DRN-2101`.
- Final matrix has 180 nodes and 202 undirected accepted edges.
- `TK-210` degree reduced from 10 to 8 by removing alarm-to-tank shortcuts through `LAHH-2101` and `LALL-2102`.
- `TK-2110` remains degree 7; its local fill, instrument, side-valve, vent, and drain connections are visible.

## Accepted Final Node Policy

- Retained all visually supported labels from the 144-row inventory unless an edge was unsupported; no inventory node was removed.
- Retained named non-inventory OPC endpoints, headers, visible T tie points, named vents/drains, sample/analyzer/control endpoints, and `HV-SW-DRAIN` where the raw schematic showed them as named objects.
- Added `HV-DRN-2106` because it is a visible named drain valve needed to represent the sample panel drain without an anonymous junction.
- Did not add ordinary OCR-missed instruments or fittings such as `PI-SW-2101` or `FLG-2110A/B`; those are visible but outside the requested non-inventory endpoint/header/tie/drain/control policy.
- Did not introduce WN ids, anonymous junctions, elbows, continuation ticks, or line-number-only labels.

## Edge Evidence By Region

### IA, Service Water, DMW, And TK-210

- Accepted the local IA chain `OPC-IA-2101` - `HV-IA-2101` - `PCV-IA-2101` - `IA-H-2101`, with `PI-IA-2101` local to `IA-H-2101`.
- Accepted service-water inlet as local named sequence `OPC-SW-2101` - `H-SW-2101` - `HV-SW-2101` - `STR-SW-2101` - `FT-SW-2101` - `FCV-SW-2101` - `HV-SW-2102` - `CV-SW-2101` - `OPC-SW-2102`, retaining local controller/final-element pairs where the dashed termination was clear.
- Accepted DMW fill chain `OPC-DMW-2101` - `HV-2150` - `FT-2150` - `FCV-2150` - `LV-2101` - `TK-210`, plus `FIC-2150` to `FT-2150`/`FCV-2150` and `LIC-2101` to `LT-2101`/`LV-2101`.
- Accepted `VNT-2101` - `HV-2103` - `TK-210`, tank drain `TK-210` - `HV-2104`, and outlet branch `TK-210` - `HV-1102`.
- Kept level switch/alarm pairs `LSHH-2101` - `LAHH-2101` and `LSL-2102` - `LALL-2102`, but did not connect alarm bubbles directly to the tank.

### A/B Cleanup Trains And Pump Discharge Header

- Accepted the solid process paths through each cleanup train: `T-2101` to `HV-2110A/B`, strainers, pumps, check valves, hand valves, MOVs, and visible `T-2102`/`T-2103` tie points.
- Accepted `T-2102` - `H-2102`, `T-2103` - `H-2102`, `H-2102` - `T-2115`, and `T-2115` - `FT-2110` - `HV-2113` - `T-2120`.
- Kept `PT-2110A` - `P-2101A` and `PT-2110B` - `P-2101B` because those vertical dashed endpoints land at the pump area.
- Kept TS/PT/PI local signal chains, but removed broad TS/PI-to-pump assumptions where the dashed route passed through the pump area without a clear local endpoint.
- Kept `HS-2101` to `FIC-SW-2101` and `MOV-2112A`, plus `HS-2102` to `MOV-2112B`, where local dashed/control terminations are visible.

### Filters, HX, Bypass, And Service-Water Return

- Accepted visible tie/header points `T-2130`, `T-2120`, `T-2122A`, `T-2122B`, `T-2125`, `T-2131`, and `T-2132`.
- Accepted bypass path `T-2130` - `HV-2130` - `FCV-2130` - `HV-2131` - `T-2132` - `T-2131`.
- Accepted parallel filter paths from `T-2120` through `HV-2120A/B`, `FLT-2120A/B`, `HV-2121A/B`, `T-2122A/B`, and into `T-2125`.
- Accepted HX outlet path `T-2125` - `HV-2125` - `HX-2120` - `T-2131` - `MOV-2125` - `FCV-2125` - `R-2125` - `OPC-2102`.
- Corrected service-water drain adjacency to `HX-2120` - `HV-SW-DRAIN` - `DRN-SW-2101`; removed the unsupported `T-2131` - `HV-SW-DRAIN` association.
- Kept temperature chain `TT-2120I` - `TT-2120O` - `TAH-2120` and added `TT-2120O` - `TAL-2120`; kept `TI-2120` local to `HX-2120`.

### Chemical Tank And Injection Pumps

- Accepted chemical fill `OPC-CHEM-2101` - `HV-2140` - `FLT-2140` - `TK-2110`.
- Accepted `TK-2110` local connections to `LT-2110`, `LSH-2110`, `HV-2141`, `HV-2147`, `HV-2145`, and `HV-2146`; vent/drain labels are visible.
- Accepted suction and discharge process paths through `T-2110`, `P-2110A/B`, `CV-2140A/B`, `HV-2142A/B`, and `T-2140`.
- Accepted local control/process edges around `PI-2140`, `PCV-2132`, `FIC-2140`, `FI-2140`, `FCV-2114`, `HV-2114`, `XV-2144`, `R-2114`, `SV-2144`, and `INJ-2140` where visible.
- Removed the weak `HS-2102` to pump edges; `HS-2102` remains represented through local control endpoints rather than direct pump assumptions.

### Sample Panels, Drains, And Control Bay

- Accepted sample takeoffs `T-2125` - `HV-SAM-2101` - `SP-2101` - `SAP-2101`, `T-2122B` - `HV-SAM-2102` - `SP-2102` - `SAP-2101`, and `T-2131` - `HV-SAM-2103` - `SP-2103` - `SAP-2101`.
- Accepted analyzer chain `SAP-2101` - `AN-2101` - `AIC-2101`.
- Added visible sample panel drain `SAP-2101` - `HV-DRN-2106` - `H-DRN-2101`.
- Accepted closed drain header as local sequence through named valves and headers. Corrected the segment around the chemical control panel to `HV-DRN-2103` - `SV-2144` - `HV-DRN-2107`; the solid header visually passes by/through the CP box, but that is not a process terminal.
- Kept the control/data bay sparse: `XA-2140`/`CP-CHEM-2101`/`JB-2101`, `JB-2101` - `JB-2102` - `JBX-2103` - `PLC-2101` - `DCS-2101` - `OPC-DATA-2101`, plus the local `HS-2110`/`XA-2110`/`KQI-*` chain.

## Removed / Rejected Candidates

| Candidate | Action | Reason |
|---|---:|---|
| `PSV-2102` - `VNT-2140` | Removed | `PSV-2102` sits on a separate/unclear dashed route near the solid vent line; no clear endpoint to `VNT-2140`. |
| `TK-210` - `LAHH-2101` | Removed | Alarm bubble is paired to `LSHH-2101`; direct tank adjacency is an association shortcut. |
| `TK-210` - `LALL-2102` | Removed | Alarm bubble is paired to `LSL-2102`; direct tank adjacency is an association shortcut. |
| `TS-2110A` - `P-2101A` | Removed | Dashed route is not a clear pump endpoint; retained TS/PT local signal chain. |
| `PI-2110A` - `P-2101A` | Removed | Dashed route passes through pump area without clear endpoint. |
| `TS-2110B` - `P-2101B` | Removed | Dashed route is not a clear pump endpoint; retained TS/PT local signal chain. |
| `PI-2110B` - `P-2101B` | Removed | Dashed route passes through pump area without clear endpoint. |
| `PSV-2110` - `T-2130` | Removed | Relief landing near the filter/bypass inlet is visually plausible but not endpointed. |
| `TT-2120O` - `HX-2120` | Removed | Outlet temperature transmitter is carried through instrument chain; direct HX endpoint is less clear than `TT-2120I`/`TI-2120`. |
| `FCV-2125` - `TAL-2120` | Removed | Alarm line belongs to the TT/alarm chain, not directly to FCV. |
| `TAL-2120` - `TI-2120` | Removed | No direct local endpoint; added `TT-2120O` - `TAL-2120` instead. |
| `T-2131` - `HV-SW-DRAIN` | Removed | Cross-domain/crossing association; the visible local path is `HX-2120` - `HV-SW-DRAIN`. |
| `HS-2102` - `P-2110A` | Removed | Pump control landing is plausible but weak; no clear direct pump endpoint. |
| `HS-2102` - `P-2110B` | Removed | Pump control landing is plausible but weak; no clear direct pump endpoint. |
| `HV-2142B` - `R-2114` | Removed | Weak skip/branch interpretation around named `T-2140` and the vertical injection stack. |
| `HV-DRN-2103` - `CP-CHEM-2101` | Removed | Drain header passes by/through CP box; CP is not a process drain terminal. |
| `CP-CHEM-2101` - `SV-2144` | Removed | Same crossing/box issue; replaced by local drain valve sequence. |
| `PI-SW-2101` | Rejected as new node | Visible in raw crop but not inventory and not an allowed non-inventory endpoint/header/tie/drain/control node. |
| `FLG-2110A/B` | Rejected as new nodes | Visible fittings but not inventory and not needed under accepted non-inventory node policy. |

## Uncertain / Plausible But Not Accepted

| Candidate | Why left uncertain |
|---|---|
| `PSV-2102` landing | Label is visible, but local routing to a named endpoint is unclear; retained as isolated inventory node with no accepted edge. |
| `PSV-2110` - `T-2130` | Relief route is plausible near the bypass inlet, but the exact tap point is too small/ambiguous. |
| Direct alarm-to-vessel edges for `LAHH-2101`/`LALL-2102` | Functional association is plausible, but visible local signal pairing through the switches is stronger. |
| TS/PI direct-to-pump edges on A/B cleanup pumps | Pump association is plausible, but only the PT vertical landing was clear enough. |
| `TT-2120O` direct to `HX-2120` or `T-2131` | Outlet temperature relation is plausible, but the instrument chain is clearer than a direct equipment/tie edge. |
| `TAL-2120` direct to `FCV-2125` or `TI-2120` | Alarm association is plausible, but the visible dashed route supports `TT-2120O` - `TAL-2120`. |
| `HS-2102` direct to `P-2110A/B` | Control function is plausible, but exact pump landing is not endpointed. |
| `HV-2142B` - `R-2114` | Lower branch could be interpreted as nearby, but named `T-2140`/injection stack routing makes the direct edge too aggressive. |
| `CP-CHEM-2101` on the drain header | Line crossing/overlap is visible, but the CP box is not accepted as a fluid path component. |
| Additional ordinary missing instruments/fittings | Visible OCR misses exist, but adding them would exceed the accepted node policy for this refinement. |

## Basic Validation Summary

- Matrix path: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\35\Results\Iteration_1\round_01_jennifer_matrix.csv`
- Nodes: 180 total = 144 inventory + 36 named non-inventory nodes.
- Unique undirected accepted edges: 202.
- Row count equals column count: True.
- Row/column labels identical and in the same order: True.
- Values restricted to 0/1: True.
- Symmetric: True.
- Diagonal zero: True.
- Isolated accepted nodes: `PSV-2102` only, justified because the label is visually supported but no named endpointed edge is clear enough for precision acceptance.
- Minimum degree: 0 because of justified `PSV-2102`; maximum degree: 8.
- Key reviewed degrees: `TK-210` = 8, `TK-2110` = 7, `HX-2120` = 5, `CP-CHEM-2101` = 2, `HV-SW-DRAIN` = 2, `HV-DRN-2106` = 2.
