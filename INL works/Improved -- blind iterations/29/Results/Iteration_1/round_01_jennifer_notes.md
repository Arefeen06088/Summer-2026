# Doc 29 / Iteration 1 Jennifer Precision Review Notes

## Source Discipline
Used only doc 29 raw input resources and doc 29 prepared crops/overlays under:

- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\29\Input resources`
- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\29\Codes and artifacts`
- Diego round-01 proposal under `Results\Iteration_1`

No ground truth, evaluator output, score feedback, or resources from other documents/iterations were used. The raw schematic was treated as primary evidence; overlays and crops were used only as inspection aids.

## Concise Change Log From Diego

- Corrected four raw-visible logical/off-page labels:
  - `HDR-SMP-001` -> `HDR-SMP-101`
  - `HDR-CDR-001` -> `HDR-DRN-101`
  - `HDR-CHM-501` -> `HDR-CHM-201`
  - `OPC-CHM-FLL` -> `OPC-CHM-FILL`
- Removed inventory-derived node `P-120`; the raw label is `TP-120` on a black test point at the CCW discharge header, not a pump/component node.
- Removed unsupported edge `PCV-501 -- AG-201`.
- Added visually supported edge `PT-401 -- HDR-SW-102`.
- Kept Diego's adjacent process-path modeling otherwise, avoiding clique expansion along long headers.

## Accepted / Rejected Added Nodes

Accepted Diego added physical inline nodes:

- `R-101`, `R-401`

Accepted off-page connector nodes, with one spelling correction:

- `OPC-SW-IN`, `OPC-DMW-001`, `OPC-VNT-001`, `OPC-CCW-SUP-A`, `OPC-CCW-SUP-B`, `OPC-CCW-SUP-C`, `OPC-SW-OUT`, `OPC-CCW-RET-A`, `OPC-CCW-RET-B`, `OPC-CCW-RET-C`, `OPC-N2-001`, `OPC-CHM-FILL`, `OPC-SAMPLE-LAB`, `OPC-IA-001`, `OPC-RADWASTE`, `OPC-DRN-001`

Accepted named header/logical nodes, with three label corrections:

- `HDR-SW-101`, `HDR-VNT-101`, `HDR-REL-101`, `HDR-CCW-101`, `HDR-CCW-102`, `HDR-CCW-103`, `HDR-SW-102`, `HDR-CCW-104`, `HDR-CHM-201`, `HDR-SMP-101`, `HDR-DRN-101`, `HDR-IA-101`

Rejected/corrected Diego node labels:

- Rejected `HDR-SMP-001`; raw header label reads `HDR-SMP-101`.
- Rejected `HDR-CDR-001`; raw closed drain header label reads `HDR-DRN-101`.
- Rejected `HDR-CHM-501`; raw chemical dosing header label reads `HDR-CHM-201`.
- Rejected `OPC-CHM-FLL`; raw off-page connector reads `OPC-CHM-FILL`.

Inventory label issue:

- `P-120` was removed. The raw schematic shows `TP-120` beside a black test point on `HDR-CCW-102`; per extraction rules, black dots/test points are not retained as nodes.

## Removed Edges

- Removed `P-120 -- HDR-CCW-102` by removing node `P-120`; the visual object is the `TP-120` test point, not a supported component.
- Removed `PCV-501 -- AG-201`; the N2 line leaves `PCV-501` toward the tank area but does not visibly terminate on the `AG-201` agitator block. `AG-201 -- TK-201` remains supported by the agitator/tank depiction.

## Added Edges

- Added `PT-401 -- HDR-SW-102`; the raw crop shows a dashed pressure-tap line from `PT-401` directly to the service water outlet header.

## High-Risk Items Reviewed

- `LV-101 -- LSHH-101` retained. Close inspection shows a dashed route from `LSHH-101` up and over to the `LV-101` actuator bubble.
- `SP-101 -- HDR-SMP-101` retained. This is a dashed/specialty sample connection from the sample point down to the named sample header; retained as visually connected but noted as dashed/specialty, not solid process pipe.
- `DCS-001 -- CP-101 -- PLC-301`, `LIC-301 -- PLC-301`, and `PLC-301 -- DV-302` retained. The control-panel crop shows direct dashed control routing to the named boxes/valve area.
- `HDR-IA-101 -- LV-101` and `HDR-IA-101 -- PCV-501` retained. The instrument-air header and branches are raw-visible. No extra IA/LCS/pump-control branches were added.
- Service-water/HX modeling retained: `HDR-SW-101` through `HV-411A/B` to `HX-101A/B`, and `HX-101A/B` through `HV-412A/B` to `HDR-SW-102`. The HX/service-water area has close crossings, but the named header/valve/HX endpoints are visually useful and connected.
- TK-101/TK-201/TK-301 instrument associations retained where dashed lines visibly terminate on named instruments, tanks, panels, or valves.

## Ambiguous / Unchanged With Caution

- The N2 outlet downstream of `PCV-501` appears to serve the TK-201 area, but it does not visibly terminate on a named tank/nozzle/component in a way strong enough to add `PCV-501 -- TK-201`. No replacement edge was added.
- TK-301 closed-drain modeling remains somewhat crowded. `TK-301 -- HDR-DRN-101`, `DV-301 -- HDR-DRN-101`, and `SEP-301 -- HDR-DRN-101` are retained because the named closed drain header and sump/separator drain linework are visually connected in the wider crop; exact bypass/branch interpretation is low-certainty.
- Test-point labels such as `TP-120`, `TP-132A/B`, `TP-241A/B/C`, and `TP-501/502` were not retained as nodes.

## Final Validation Counts

- Nodes: 170 total.
- Undirected edges: 178.
- Blank top-left CSV cell: true.
- Row/column label order identical: true.
- Duplicate node names: false.
- Values limited to `0/1`: true.
- Symmetric matrix: true.
- Diagonal all zero: true.
- Isolated nodes: none.
