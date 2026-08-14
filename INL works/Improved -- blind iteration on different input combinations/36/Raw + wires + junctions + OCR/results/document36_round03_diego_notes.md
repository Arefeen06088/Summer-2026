# Document 36 Round 03 Diego Notes

## Scope and Evidence

- Worked only inside the allowed doc36 folder.
- Reviewed Diego round01 nodes/edges/notes and Jennifer round02 nodes/edges/matrix/notes.
- Re-inspected the allowed raw and wire crops, especially raw__row3_col1.png, raw__row3_col2.png, raw__row3_col3.png, raw__bottom_left.png, raw__bottom_right.png, raw__row1_col2.png, raw__row2_col2.png, and wires__full_sheet.png.
- Did not use Ground Truth, evaluator output, outside data, or off-the-shelf OCR.
- Continued to treat the raw schematic and component_visual_ocr_labels.csv as authoritative for names.

## Round03 Decision

- I agree with Jennifer round02.
- Copied Jennifer round02 nodes exactly to document36_round03_diego_nodes.csv.
- Copied Jennifer round02 edges exactly to document36_round03_diego_edges.csv.
- Edge set is saturated with round02: no included edges were added or removed in round03.

## Fan Control Saturation Review

- Did not restore PNL-ESF-A -- FAN-CONTAIN-A.
  - raw__bottom_left.png and raw__row3_col2.png show dashed lanes near FAN-CONTAIN-A, but no clear dashed fan-side contact into the fan symbol, fan port dot, or label-adjacent terminal.
  - wires__full_sheet.png also shows proximity rather than a clear fan control contact.
- Did not restore PNL-ESF-B -- FAN-CONTAIN-B.
  - raw__bottom_right.png and raw__row3_col3.png show dashed lanes near FAN-CONTAIN-B, but no clear dashed fan-side contact into the fan symbol, fan port dot, or label-adjacent terminal.
  - wires__full_sheet.png does not reveal a missed fan-side contact.
- Both fan control candidates remain in the edge CSV as round_action=remove, matching Jennifer round02, and are ignored by the matrix helper.

## Medium Edge Review

- CB-13-TIE -- PNL-RPS-1 remains included at medium confidence.
  - raw__row1_col2.png shows the dashed RPS TRIP route leaving the CB-13-TIE area; raw__row2_col2.png shows the route continuing toward PNL-RPS-1.
  - Label and keep-out-border interruptions keep confidence at medium.
- PNL-ESF-A -- PUMP-AFW-A and PNL-ESF-B -- PUMP-AFW-B remain included at medium confidence.
  - raw__row3_col1.png, raw__row3_col2.png, and raw__row3_col3.png show AFW drops into the lower dashed control lanes that route toward the ESF panel sides.
- PNL-ESF-A -- VALVE-MOV-A and PNL-ESF-B -- VALVE-MOV-B remain included at medium confidence.
  - raw__bottom_left.png and raw__bottom_right.png show MOV dashed drops into the ESF control lanes.
- No new direct PNL-RPS-1 to ESF-panel edge was added.

## Validation Summary

- Nodes: 55 total, including 47 physical components and 8 logical busbar nodes.
- Edge CSV rows: 62 total.
- Included edge rows used by matrix: 60.
- Removed edge rows ignored by matrix: 2.
- Included edge kinds: 48 power_feeder, 4 bus_tie, and 8 control_interlock.
- Matrix validation passed: no unknown endpoints, no duplicate included undirected pairs, symmetric 55 by 55 matrix, and zero diagonal.
