# Document 36 Round 02 Jennifer Notes

## Scope and Evidence

- Worked only inside the allowed doc36 folder.
- Used the raw schematic, wire/node overlays, component_visual_ocr_labels.csv, precision review crops, wire_nodes.csv, and Diego round01 outputs.
- Did not use Ground Truth, evaluator output, or off-the-shelf OCR.
- Treated the raw schematic and component_visual_ocr_labels.csv as authoritative. Did not use component_labels_banners_overlay.png for naming because it is inconsistent with the raw schematic.

## Kept / Removed / Renamed Summary

- Nodes kept: all 55 Diego round01 nodes.
- Node renames: none.
- Included edges kept from round01: 60.
- Edge removals from included graph: 2 low-confidence fan control candidates remain in the edge CSV with round_action=remove:
  - PNL-ESF-A -- FAN-CONTAIN-A
  - PNL-ESF-B -- FAN-CONTAIN-B
- Reason for removals: the dashed control lanes pass below/near the fan labels, but I do not see a clear dashed contact from the ESF panel routes into the fan symbols or fan port dots. Under the precision rule, nearby lane proximity is not enough support.

## Requested Checks

- Confirmed logical bus names: BUS-13K-A, BUS-13K-B, BUS-4K-A, BUS-4K-B, BUS-480-A, BUS-480-B, BUS-DC125-A, BUS-DC125-B.
- Confirmed no direct BUS-13K-A -- BUS-13K-B or BUS-4K-A -- BUS-4K-B edge is included; both A/B ties are represented only through CB-13-TIE and CB-4K-TIE.
- CB-13-TIE -- PNL-RPS-1 remains included as a medium-confidence control_interlock. The dashed RPS TRIP route is visible from the 13 kV tie area down toward the RPS panel side, though label/border interruptions keep confidence at medium.
- CB-4K-TIE -- PNL-RPS-1 remains included as high-confidence control_interlock, not power. The visible RPS LOCKOUT/control relation drops from the tie breaker to PNL-RPS-1.
- PNL-ESF-A -- PUMP-AFW-A and PNL-ESF-B -- PUMP-AFW-B remain included as medium-confidence control_interlock edges. The pump drops connect into the dashed control lanes routed to the ESF panel sides.
- PNL-ESF-A -- VALVE-MOV-A and PNL-ESF-B -- VALVE-MOV-B remain included as medium-confidence control_interlock edges. The MOV drops are visibly tied to dashed control lanes routed to the ESF panels.
- PNL-ESF-A -- FAN-CONTAIN-A and PNL-ESF-B -- FAN-CONTAIN-B were removed from the included graph. The nearby dashed lanes are visible, but the device-side fan contacts are not.
- Confirmed inverter/ESF paths: INV-120A -- PNL-ESF-A and INV-120B -- PNL-ESF-B are solid, visually supported feeds.
- Confirmed DC topology: RECT-125A, BAT-125A, and INV-120A connect to BUS-DC125-A; RECT-125B, BAT-125B, and INV-120B connect to BUS-DC125-B.
- No crossing-without-dot was intentionally converted into an included edge during round02.

## Final Counts

- Nodes: 55.
- Edge CSV rows: 62 total.
- Included edge rows used by matrix: 60.
- Removed edge rows ignored by matrix: 2.
- Included edge kind counts: 48 power_feeder, 4 bus_tie, 8 control_interlock.

## Validation

- Matrix builder command run:
  - python codes\build_matrix_from_edges.py results\document36_round02_jennifer_edges.csv results\document36_round02_jennifer_nodes.csv results\document36_round02_jennifer_adjacency_matrix.csv results\document36_round02_jennifer_matrix_summary.json
- Unknown endpoints: none.
- Duplicate included undirected pairs: none.
- Matrix symmetry: passed.
- Matrix diagonal zero: passed.
- Matrix size: 55 x 55.
- Unique included undirected edges: 60.

## Remaining Uncertainty

- CB-13-TIE -- PNL-RPS-1 remains medium confidence because the dashed RPS TRIP path is visible but partly interrupted by labels/keep-out borders.
- AFW pump control edges remain medium confidence because their control routes share lower dashed lanes before entering the ESF panel-side route.
- The removed fan control candidates could only be restored if higher-resolution visual evidence showed a clear fan-side dashed contact; it is not visible enough in the allowed review crops.
