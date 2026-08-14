# Document 36 Round 04 Jennifer Final Sign-Off

## Scope and Evidence

- Worked only inside the allowed doc36 folder.
- Used round02 Jennifer files, round03 Diego files, raw schematic crops, wire/node overlays, and provided CSV aids.
- Did not use Ground Truth, GT-derived feedback, evaluator outputs, outside data, or off-the-shelf OCR.
- Continued to treat the raw schematic and component_visual_ocr_labels.csv labels as authoritative.

## Round03 to Round04 Comparison

- Round03 nodes match round02 Jennifer nodes exactly.
- Round03 edges match round02 Jennifer edges exactly.
- Round04 nodes were copied exactly from round03.
- Round04 edges were copied exactly from round03.
- Saturation decision: no visually necessary correction was found in final review.
- Edge set changed from round03: no.

## Final Precision Checks

- CB-13-TIE -- PNL-RPS-1 remains included as medium-confidence control_interlock. The dashed RPS TRIP route is visible from the 13 kV tie area toward PNL-RPS-1, but route interruptions keep confidence at medium.
- PNL-ESF-A -- PUMP-AFW-A remains included as medium-confidence control_interlock. The AFW-A dashed drop reaches the lower control lane that routes toward the PNL-ESF-A side.
- PNL-ESF-A -- VALVE-MOV-A remains included as medium-confidence control_interlock. The MOV-A dashed drop is visibly tied into the A-train ESF control lane.
- PNL-ESF-B -- PUMP-AFW-B remains included as medium-confidence control_interlock. The AFW-B dashed drop reaches the lower control lane that routes toward the PNL-ESF-B side.
- PNL-ESF-B -- VALVE-MOV-B remains included as medium-confidence control_interlock. The MOV-B dashed drop is visibly tied into the B-train ESF control lane.
- PNL-ESF-A -- FAN-CONTAIN-A remains excluded with round_action=remove. No clear fan-side dashed contact is visible.
- PNL-ESF-B -- FAN-CONTAIN-B remains excluded with round_action=remove. No clear fan-side dashed contact is visible.
- Confirmed logical bus names: BUS-13K-A, BUS-13K-B, BUS-4K-A, BUS-4K-B, BUS-480-A, BUS-480-B, BUS-DC125-A, BUS-DC125-B.
- Confirmed A/B bus ties are represented through tie breaker nodes only: CB-13-TIE and CB-4K-TIE. No direct included BUS-13K-A -- BUS-13K-B or BUS-4K-A -- BUS-4K-B edge is present.
- Confirmed inverter/DC topology: RECT-125A, BAT-125A, and INV-120A connect to BUS-DC125-A; RECT-125B, BAT-125B, and INV-120B connect to BUS-DC125-B; INV-120A feeds PNL-ESF-A and INV-120B feeds PNL-ESF-B.
- No crossing-without-dot connection was added.

## Final Counts

- Nodes: 55.
- Edge CSV rows: 62.
- Included edge rows used by matrix: 60.
- Removed edge rows ignored by matrix: 2.
- Included edge kind counts: 48 power_feeder, 4 bus_tie, 8 control_interlock.

## Validation

- Matrix builder command run:
  - python codes\build_matrix_from_edges.py results\document36_round04_jennifer_edges.csv results\document36_round04_jennifer_nodes.csv results\document36_round04_jennifer_adjacency_matrix.csv results\document36_round04_jennifer_matrix_summary.json
- Unknown endpoints: none.
- Duplicate included undirected pairs: none.
- Matrix symmetry: passed.
- Matrix diagonal zero: passed.
- Matrix size: 55 x 55.
- Unique included undirected edges: 60.

## Remaining Uncertainty

- The only retained medium-confidence items are the RPS trip route and AFW/MOV control routes listed above.
- The fan control candidates are excluded because the final pass still shows nearby dashed lane proximity rather than clear fan-side contact.
