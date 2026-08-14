# Document 39 Round01 Diego Notes

## Scope and Inputs

- Extraction used only files inside `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\39\Raw + wires + junctions + OCR`.
- Raw schematic `raw -- npp_schematic_improved_no_overlap.png` was treated as authoritative.
- Aids inspected: `component_visual_ocr_labels.csv`, `component_labels_banners_overlay.png`, `wires_mask_overlay.png`, `wire_nodes_overlay.png`, `wire_nodes.csv`, and the `precision_review_crops` raw/wire/node crops.
- No off-the-shelf OCR and no GT/evaluator/feedback files were used.

## Node Decisions

- Included all visually/electrically plausible labeled physical components from the provided visual-label CSV: offsite sources, disconnects, transformers, breakers, EDGs, relays, 125 VDC/120 VAC stack equipment, MCCs, pumps, MOVs, field JBs, annunciator/recorder, and plant ground.
- Included the four visibly labeled busbars as logical electrical nodes:
  - `BUS-4160-A-DIV-I`
  - `BUS-4160-B-DIV-II`
  - `BUS-480-A`
  - `BUS-480-B`
- Included `CONTROL-ROOM-ANNUNCIATION` as a low-confidence logical control-route node because a labeled dashed run is drawn along the lower control-room annunciation area. Edges to this node are intentionally low-confidence where explicit terminal dots are not present.
- Did not create separate `125 VDC` or `120 VAC` logical bus nodes. The side stacks show routed conductors through named components, but no clearly labeled busbar comparable to the 4.16 kV and 480 V buses.

## Annotation-Only Text Not Used As Nodes

- `DIVISION-I-TRAIN-A-SAFETY-POWER` and `DIVISION-II-TRAIN-B-SAFETY-POWER`: boundary/title text.
- `NORMAL-OFFSITE-FEED-A` and `NORMAL-OFFSITE-FEED-B`: feed annotations on the 4.16 kV bus area.
- `LC-A` and `LC-B`: local/load-center route labels at the 480 V bus ends, not separate terminal blocks in the raw drawing.
- `N.O.-TIE`: tie-breaker state annotation; captured in the `CB-TIE-AB` edge notes rather than as a node.

## Connectivity Rules Applied

- Busbar connections are mediated through logical bus nodes. For example, `CB-1A`, `CB-DG-A`, `TR-480-A`, `RELAY-UV-A`, and `CB-TIE-AB` connect to `BUS-4160-A-DIV-I` rather than directly to each other.
- `BUS-4160-A-DIV-I` and `BUS-4160-B-DIV-II` are connected only through `CB-TIE-AB`; no direct bus-to-bus edge was added.
- `BUS-480-A` and `BUS-480-B` are visually separated and no direct edge was added.
- Crossings or near passes without a visible junction/terminal dot were not treated as connectivity.
- `GND-PLANT` is connected only to `BUS-480-A` as a ground/reference conductor visible below the right end of the A 480 V bus.

## Dashed / Control / DC Edges

- UV relay edges from the 4.16 kV buses were included as `dc_sensing` because dashed vertical conductors visibly drop from each bus to its relay.
- Battery-to-inverter side-stack edges were included as `dc_power` because the raw drawing shows dashed/DC-style vertical routing and the terminal schedule supports `BAT-A` to `INV-A` for DC on the A side.
- RPS-to-KA1/KB1 edges were included as `control` because the dashed routes visibly terminate at the relay blocks and the terminal schedule supports these interlocks.
- RPS-to-field-JB and field-JB-to-MOV edges were included as `control`; confidence is moderate where the long dashed bottom route is clear but explicit dots are sparse.
- `CONTROL-ROOM-ANNUNCIATION` route-membership edges are low-confidence. The direct dashed line from `ANN-CR01` to `REC-SOE01` is stronger and was included separately.

## Deliberately Not Added

- No direct edge from `RELAY-KA1` to `MCC-A1`, `PUMP-RHR-A`, or `PUMP-CS-A`; nearby solid pump feeders pass around the relay without a clear terminal dot.
- No direct edge from `RELAY-KB1` to `MCC-B*` or B-side loads; the visible dashed route is from `RPS-B` to `RELAY-KB1`.
- No direct `JB-A101` to `ANN-CR01` or `JB-B101` to `REC-SOE01` terminal-to-terminal edge; only low-confidence logical association through `CONTROL-ROOM-ANNUNCIATION` was retained.
- No edge from `GND-PLANT` to `BUS-480-B`; the raw drawing does not show a terminal connection to the B 480 V bus.
