# Document 24 Round-04 Jennifer Notes

## Method And Constraints

- Inspected the raw schematic and allowed aids/crops only, with special focus on `labels__row3_col2.png` plus the raw, wires, and nodes versions of `row3_col2` and `row3_col3`.
- Did not use Ground Truth, evaluator outputs, previous-document connectivity, or GT-derived feedback.
- Did not use off-the-shelf OCR. Label decisions were made from raw visual inspection, with allowed overlays/indexes used only as aids.
- Preserved Diego's round-03 node set, edge set, node order, and adjacency matrix. No graph changes were made in round 04.

## Decisions Versus Diego Round-03

- Agreed with restoring `LOAD-SHED-CAB -- LAMP-ALM-A`. The raw central crop shows a dotted signal route dropping from the bottom of LOAD-SHED-CAB, running horizontally across the alarm lamp line, and making a visible short dotted drop into LAMP-ALM-A.
- Agreed with restoring `LOAD-SHED-CAB -- LAMP-ALM-B`. The same dotted route continues right and makes a visible short dotted drop into LAMP-ALM-B.
- Agreed with keeping `ESFAS-PNL-B -- LOAD-SHED-CAB` removed. In the right-side raw crop, ESFAS-PNL-B is supported by the solid DC feed, while the nearby dashed route runs down the right-side control path without visibly terminating into ESFAS-PNL-B or through a junction-dot-supported routed connection.

## Medium Edge Recheck

- Retained `CB-TIE-1 -- SYNC-CAB` and `SYNC-CAB -- LOAD-SHED-CAB`: the central dashed control/trip route visibly descends from the CB-TIE-1 area, passes through/along the SYNC-CAB routing channel, and continues into LOAD-SHED-CAB.
- Retained `ESFAS-PNL-A -- LOAD-SHED-CAB`, `TRIP-MOD-A -- LOAD-SHED-CAB`, and `TRIP-MOD-B -- LOAD-SHED-CAB`: each has a visible dashed control/trip route into the load-shed routed channel, but remains medium because the routing is not represented by a separately named junction.
- Retained `TB-RPS-A -- ANN-PNL-1` and `TB-RPS-B -- ANN-PNL-1`: the dotted RPS signal trunks continue toward the central annunciator signal path without an extra named intermediate component.
- Retained `LOAD-SHED-CAB -- ANN-PNL-1`: the dotted drop from LOAD-SHED-CAB continues to ANN-PNL-1, with no unsupported additional component inferred.
- No obvious overconnection was found in the reviewed CB-TIE-1/SYNC-CAB/LOAD-SHED-CAB/TB-RPS-A/B/ANN-PNL-1 cluster.

## Switch Label Confirmation

- Kept `SW-MAN-A` and `SW-MAN-B`. The raw top-left and top-right schematic text reads `SW-MAN-A` and `SW-MAN-B`; the allowed label overlay/index text `SW-PGA-A/B` was not adopted where it conflicts with raw visual text.

## Counts

- Node count: 200
- Edge count: 204
- Edge kind counts: `control_trip` 61, `dc_power` 11, `ground` 4, `power` 112, `signal` 16
- Confidence counts: `high` 194, `medium` 10

## Validation

- No unknown edge endpoints: passed
- No duplicate undirected pairs: passed
- Adjacency matrix symmetric: passed
- Adjacency matrix diagonal zero: passed

Round 04 saturates Diego round 03 without changing the matrix.
