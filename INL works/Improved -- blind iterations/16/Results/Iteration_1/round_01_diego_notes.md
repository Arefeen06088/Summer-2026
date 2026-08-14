# Round 01 Diego Notes - Doc 16 / Iteration 1

## Source Boundaries
- Used only doc 16 input resources and artifacts derived from those resources: raw schematic, OCR/component inventory, wire overlays, and inspection crops.
- Did not use any ground-truth, evaluator, scoring, metric, feedback, or derived-answer files.
- Node list/order is exactly the corrected `component_inventory_doc16.csv`: 168 physical schematic components plus 8 named logical bus nodes = 176 nodes.

## Title-Block Exclusion
- `PP-E1-480-125R` was excluded. The lower-right `ground_and_panel_bottom` crop shows it inside the drawing-number/title-block area beside `DWG NO.`, with no schematic component body or conductor connection.
- The corrected inventory already excludes this OCR/title metadata, and the generated matrix follows that corrected inventory.

## Extraction Rules Applied
- Named buses are used as bus nodes; feeders/components connect to the bus node without clique-expanding bus members.
- Anonymous `WN-*` points, unlabeled junction dots, pure crossings, line ticks, title/legend/note text, cable-route/enclosure borders, and unlisted title metadata were excluded.
- MCC branches were modeled as feeder breaker -> MCC -> branch breaker -> relay -> load -> ground or terminal block according to visible linework.
- For dashed/dotted control and signal lines, only visibly terminated named endpoints were retained; broad signal cliques were not created.

## Validation
- Node count: 176
- Edge count: 174
- Matrix symmetric: True
- Matrix diagonal zero: True
- Edge/matrix count agreement: True
- Unknown edge endpoints: 0
- Validation status: PASS

## Uncertain Candidates For Jennifer Review
- `BATT-125A` -- `CHGR-125A` (uncertain_visual): dc_vital_a raw: dashed DC line visibly terminates between BATT-125A and CHGR-125A
- `BATT-125B` -- `CHGR-125B` (uncertain_visual): dc_vital_b raw: dashed DC line visibly terminates between BATT-125B and CHGR-125B
- `CP-RPS-A` -- `PROT-UV-A` (uncertain_collapsed_through_unlisted_jb): control_protection_a raw: vertical control/protection conductor links CP-RPS-A area to PROT-UV-A
- `RELAY-86A` -- `TB-3A` (uncertain_routed_signal): control_protection_a raw: dashed control route from RELAY-86A to TB-3A
- `CP-RPS-B` -- `PROT-UV-B` (uncertain_collapsed_through_unlisted_jb): control_protection_b raw: vertical control/protection conductor links CP-RPS-B area to PROT-UV-B
- `RELAY-86B` -- `TB-3B` (uncertain_routed_signal): control_protection_b raw: dashed control route from RELAY-86B to TB-3B
- `MG-RPS-A` -- `FT-AFW101` (uncertain_visual): control_protection_a raw: vertical conductor from MG-RPS-A to FT-AFW101
- `RTD-RCS101` -- `BUS-120-RPS-B` (uncertain_visual): dc_vital_b/full raw: RTD-RCS101 vertical line terminates at BUS-120-RPS-B
- `XS-DOOR101` -- `JB-CONTAIN` (uncertain_routed_signal): control_protection_b raw: dotted signal route visibly terminates at XS-DOOR101 and JB-CONTAIN

## Deliberately Not Expanded
- `GND-NO` is retained as a visible named ground from the corrected inventory, but no direct edge was added to an inferred bus because its only immediate visible mate is the unmodeled `UCP-01`/grounding detail; direct bus-to-ground collapse should be reviewed before adding.
- Broad CP-DCS/CP-ANN signal fanouts across dashed and dotted routes were not clique-expanded. Candidate signal paths from `CP-DCS-01` toward instruments and from `CP-ANN-01` toward `JB-CONTAIN` should be reviewed on the raw crop before addition.
- Visible but inventory-excluded local boxes such as the small JB/RPS boxes were not added as nodes to preserve the 176-node intended inventory.
