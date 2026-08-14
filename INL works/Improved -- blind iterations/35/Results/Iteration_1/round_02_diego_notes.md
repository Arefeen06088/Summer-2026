# Round 02 Diego Saturation Review Notes

## Scope

Reviewed only doc35 resources and permitted round files: the raw schematic image, component inventory/list, generated overlays, wire-node aids, inspection crops, Diego Round 01 outputs, and Jennifer Round 01 matrix/notes. No ground truth, evaluator output, validation metrics, scores, previous-doc feedback, or outside resources were used.

## Saturation Decision

I agree with Jennifer Round 01 and copied her matrix exactly to `round_02_diego_matrix.csv`.

No node or edge changes were made in Diego Round 02. Jennifer's stricter graph is the saturated recommendation from this review.

## Node Review

- All 144 inventory component labels remain retained.
- Diego Round 01's 35 visible named non-inventory nodes remain retained.
- Jennifer's added `HV-DRN-2106` node is visually supported on the sample panel drain path and avoids replacing a named drain valve with an anonymous wire node.
- No anonymous WN ids, unlabeled junctions, elbows, bends, continuation ticks, or line-number-only pipe labels were added.
- `PSV-2102` remains isolated. The component label is visible in the IA/tank crop, but its dashed route is not clearly endpointed to `VNT-2140` or another named node.

## Reviewed Edge Evidence

- IA/service water/DMW/TK-210: Jennifer's local IA, SW, DMW fill, tank drain, tank outlet, and level signal edges are supported. The removed `PSV-2102` - `VNT-2140`, `TK-210` - `LAHH-2101`, and `TK-210` - `LALL-2102` shortcuts are not clearly endpointed as direct edges.
- A/B cleanup trains: Solid process adjacency through `T-2101`, A/B strainers, pumps, check valves, hand valves, MOVs, `T-2102`/`T-2103`, `H-2102`, `T-2115`, `FT-2110`, `HV-2113`, and `T-2120` is supported. Jennifer's removed TS/PI-to-pump shortcuts are plausible associations but not clear terminal edges.
- Filters/HX/bypass: The bypass and A/B filter paths are correctly represented through visible `T-*` tie points. The service-water drain is locally attached to `HX-2120` via `HV-SW-DRAIN`, not to process tie `T-2131`. `TAL-2120` is better represented through `TT-2120O` than through `TI-2120` or `FCV-2125`.
- Chemical tank and injection pumps: Fill, tank instruments, pump suction/discharge, `T-2140`, `PI-2140`, `PCV-2132`, `FCV-2114`, `HV-2114`, `XV-2144`, `SV-2144`, and `INJ-2140` are visually plausible as Jennifer retained them. Removed `HS-2102` direct pump edges and `HV-2142B` - `R-2114` are better left as uncertain, not accepted.
- Sample, drain, and control bay: `HV-DRN-2106` is visible below `SAP-2101`, and Jennifer's `SAP-2101` - `HV-DRN-2106` - `H-DRN-2101` path is the most local named representation. The drain header around `CP-CHEM-2101` is better represented as `HV-DRN-2103` - `SV-2144` - `HV-DRN-2107`; the CP box is not treated as a process drain terminal. The control bay remains sparse and avoids a clique.

## Ambiguous / Plausible But Not Accepted

- `PSV-2102` landing to `VNT-2140` or another named node remains visually unclear.
- `PSV-2110` near `T-2130` remains plausible but not endpointed.
- Direct alarm-to-tank edges for `LAHH-2101` and `LALL-2102` remain functional associations rather than direct visual edges.
- TS/PI direct-to-pump edges on A/B cleanup pumps remain plausible but too aggressive.
- `TT-2120O` direct to `HX-2120` and `TAL-2120` direct to `TI-2120`/`FCV-2125` remain weaker than Jennifer's temperature/alarm chain.
- `HS-2102` direct to `P-2110A/B` remains a control-function possibility without a clear endpoint.
- `HV-2142B` - `R-2114` remains a weak branch interpretation around the lower injection stack.
- `CP-CHEM-2101` as a drain-header process terminal remains unsupported by the local drawing.

## Minimal Changes From Jennifer

None. `round_02_diego_matrix.csv` is an exact copy of `round_01_jennifer_matrix.csv`.

## Basic Validation Summary

- Matrix path: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\35\Results\Iteration_1\round_02_diego_matrix.csv`
- Nodes: 180 total = 144 inventory + 36 named non-inventory nodes.
- Unique undirected accepted edges: 202.
- Row/column labels identical and in the same order: True.
- Values restricted to 0/1: True.
- Symmetric: True.
- Diagonal zero: True.
- Isolated accepted nodes: `PSV-2102` only, justified because the component is visually supported but no named endpointed edge is clear enough.
