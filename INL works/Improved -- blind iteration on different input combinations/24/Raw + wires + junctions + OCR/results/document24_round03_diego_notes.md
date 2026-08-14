# Document 24 Round-03 Diego Notes

## Method And Constraints

- Inspected Jennifer's round-02 precision changes visually against the raw schematic and the allowed overlays/crops/index only.
- Did not use Ground Truth, evaluator outputs, previous-document connectivity, or GT-derived feedback.
- Did not use off-the-shelf OCR. Switch label decisions are from raw visual text, with the allowed index used only as a location aid.
- Preserved Jennifer's node set and node order. No nodes were added, removed, or renamed.

## Result Versus Jennifer Round-02

I changed Jennifer's round-02 graph by restoring two of the three pruned edges:

- Restored `LOAD-SHED-CAB -- LAMP-ALM-A` as `signal`, medium. The raw central bottom crop shows a dotted route leaving the bottom of LOAD-SHED-CAB, teeing into the upper lamp signal trunk, and a short dotted drop into LAMP-ALM-A.
- Restored `LOAD-SHED-CAB -- LAMP-ALM-B` as `signal`, medium. The same visible dotted route tees into the lamp trunk and has a short dotted drop into LAMP-ALM-B.
- Kept Jennifer's removal of `ESFAS-PNL-B -- LOAD-SHED-CAB`. The B-side raw crop shows the dashed routed control path near ESFAS-PNL-B/Train B, but I do not see a direct dashed termination into ESFAS-PNL-B; ESFAS-PNL-B is visibly tied to PNL-DC-B by the solid DC feed only.

## Retained Medium Routed Edges

- `CB-TIE-1 -- SYNC-CAB`: retained. The central dashed route drops from the CB-TIE-1 area through the clear routing channel and reaches the SYNC-CAB footprint.
- `SYNC-CAB -- LOAD-SHED-CAB`: retained. The same dashed routed channel continues down toward LOAD-SHED-CAB.
- `ESFAS-PNL-A -- LOAD-SHED-CAB`: retained. A dashed control/trip route visibly leaves ESFAS-PNL-A and turns into the load-shed routed channel.
- `TRIP-MOD-A -- LOAD-SHED-CAB`: retained. TRIP-MOD-A is tied into the dashed routed channel leading to LOAD-SHED-CAB.
- `TRIP-MOD-B -- LOAD-SHED-CAB`: retained. TRIP-MOD-B has a visible dashed run to the right-side load-shed routing channel.
- `TB-RPS-A -- ANN-PNL-1` and `TB-RPS-B -- ANN-PNL-1`: retained. The dotted RPS terminal-block trunks run toward the central annunciator signal path without a named intermediate node.
- `LOAD-SHED-CAB -- ANN-PNL-1`: retained. The dotted signal drop from LOAD-SHED-CAB continues down to ANN-PNL-1.

## Switch Labels

- Kept `SW-MAN-A` and `SW-MAN-B` in the node file and edges. The raw top-left and top-right crops read `SW-MAN-A/B`; the allowed index labels `SW-PGA-A/B` are not adopted.

## Counts

- Node count: 200
- Edge count: 204
- Edge kind counts: {'control_trip': 61, 'dc_power': 11, 'ground': 4, 'power': 112, 'signal': 16}
- Confidence counts: {'high': 194, 'medium': 10}

## Validation

- No unknown edge endpoints: passed
- No duplicate undirected pairs: passed
- Adjacency matrix symmetric: passed
- Adjacency matrix diagonal zero: passed
