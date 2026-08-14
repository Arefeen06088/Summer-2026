# Document 24 Round-01 Diego Notes

## Method

- Inspected the raw schematic first: `raw -- synthetic_npp_electrical_schematic_rev2.png`.
- Used allowed visual aids and precision crops only after raw inspection: component label overlay, wire/node overlays, and `precision_review_crops/*`.
- Used `component_visual_ocr_labels.csv` and `component_index_by_position.*` as allowed label/index aids, with raw visual correction where the aid disagreed with the drawing.
- Did not use Ground Truth, evaluator output, previous-document connectivity, or off-the-shelf OCR.
- Modeled named buses as explicit logical nodes: BUS-101A, BUS-101B, BUS-201A, BUS-201B, DC-BUS-125A, and DC-BUS-125B.
- Did not create anonymous wire nodes. Dotted/dashed routed trunks were represented as direct component-to-component edges where the visible line terminates at named components.
- Treated plain crossings without junction dots as non-connections.

## Counts

- Node count: 200
- Edge count: 205
- Node type counts: {'physical_component': 194, 'logical_bus': 6}
- Edge kind counts: {'power': 112, 'control_trip': 62, 'dc_power': 11, 'ground': 4, 'signal': 16}
- Confidence counts: {'high': 194, 'medium': 11}

## Assumptions

- `BUS-201A` and `BUS-201B` are the named lower 4.16 kV safety buses visible under CB-202A/B and feeding the nine 2A/2B feeder columns, even though the long bus annotation text also references safety bus 101A/101B normal/EDG sources.
- The two diesel-generator switch labels are visually read from the raw sheet as `SW-MAN-A` and `SW-MAN-B`; the overlay/index text `SW-PGA-A/B` was rejected for those two nodes.
- Solid lines are power/DC power; dashed lines are control/trip; dotted lines are signal, per the drawing legend.
- The repeated feeder columns were modeled consistently: bus -> breaker -> disconnect -> MCC -> terminal block -> load, plus MCC -> relay and hand-switch -> relay dashed control links.

## Ambiguous Or Lower-Confidence Items

- CB-TIE-1 -- SYNC-CAB (control_trip, medium): Dashed route descends from the CB-TIE-1 area through the central clear-routing channel toward SYNC-CAB; branch point is routed rather than labeled.
- SYNC-CAB -- LOAD-SHED-CAB (control_trip, medium): Central dashed routing channel continues from SYNC-CAB area toward LOAD-SHED-CAB; inferred from continuous dashed path.
- ESFAS-PNL-A -- LOAD-SHED-CAB (control_trip, medium): Dashed routed control/trip line leaves ESFAS-PNL-A region and turns toward LOAD-SHED-CAB; exact branch is routed in central channel.
- TRIP-MOD-A -- LOAD-SHED-CAB (control_trip, medium): Dashed control/trip route from TRIP-MOD-A top area joins the LOAD-SHED-CAB routed line; central branch lacks a dot but path is visually continuous.
- TB-RPS-A -- ANN-PNL-1 (signal, medium): Long dotted signal trunk from TB-RPS-A/RPS-PNL-A area continues toward ANN-PNL-1; no named intermediate node is shown.
- ESFAS-PNL-B -- LOAD-SHED-CAB (control_trip, medium): Dashed routed control/trip channel from ESFAS-PNL-B/Train B area returns toward LOAD-SHED-CAB; exact central branch is inferred from continuity.
- TRIP-MOD-B -- LOAD-SHED-CAB (control_trip, medium): Dashed control/trip route from TRIP-MOD-B joins the right-side load-shed routing channel.
- TB-RPS-B -- ANN-PNL-1 (signal, medium): Long dotted Train B signal trunk from TB-RPS-B/RPS-PNL-B area runs toward ANN-PNL-1/central annunciation; no named intermediate node is shown.
- LOAD-SHED-CAB -- LAMP-ALM-A (signal, medium): Dotted branch below LOAD-SHED-CAB visibly reaches the LAMP-ALM-A area; branch point is not individually named.
- LOAD-SHED-CAB -- LAMP-ALM-B (signal, medium): Dotted branch below LOAD-SHED-CAB visibly reaches the LAMP-ALM-B area; branch point is not individually named.
- LOAD-SHED-CAB -- ANN-PNL-1 (signal, medium): Dotted signal drop from LOAD-SHED-CAB continues to the ANN-PNL-1 dotted trunk; connection inferred by continuous routed line.

## Rejected Items

- Did not include the top-left `SYN` triangle or top-right `REV 2` triangle as graph nodes; they appear to be sheet annotations/markers rather than connected electrical components.
- Did not connect any wire crossings without visible junction dots.
- Did not add anonymous intermediate wire nodes for central routed dashed/dotted trunks.
- Did not use the aid labels `SW-PGA-A` or `SW-PGA-B`; raw visual text reads `SW-MAN-A` and `SW-MAN-B`.

## Validation

- No unknown edge endpoints: passed.
- No duplicate undirected pairs: passed.
- Adjacency matrix symmetric: passed.
- Adjacency matrix diagonal zero: passed.
