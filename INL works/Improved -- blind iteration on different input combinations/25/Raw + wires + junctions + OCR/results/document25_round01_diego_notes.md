# Document 25 Round 01 Diego Notes

## Method

- Inspected the raw schematic first (`raw -- synthetic_npp_electrical_schematic_revised_v4.png`) before using overlays.
- Used allowed aids only: component label/index crops, `component_visual_ocr_labels.csv`, `wire_nodes.csv`, `wires_mask_overlay.png`, and `wire_nodes_overlay.png`.
- Did not use Ground Truth, evaluator outputs, previous-document connectivity, or off-the-shelf OCR.
- Modeled named bus backbones as explicit logical nodes: SWYD-115KV, BUS-4160-A/B/C, BUS-480-1A/B/C, BUS-125DC-A/B, RPS TRIP BUS, PNL A/B TIE, and the two 480V charger feeder arrows.
- Did not create anonymous wire-node junctions. Crossings without visible junction dots were treated as non-connections.

## Counts

- Node count: 204
- Edge count: 211
- Node type counts: {'logical_bus': 9, 'logical_external_feeder': 2, 'logical_signal_bus': 2, 'physical_component': 191}
- Edge kind counts: {'control_interlock_trip': 30, 'dc_power': 9, 'external_feeder': 2, 'ground_reference': 3, 'instrument_signal': 2, 'power': 165}
- Confidence counts: {'high': 199, 'low': 3, 'medium': 9}
- Physical component count from index: 191
- Logical named node count added: 13

## Assumptions

- Breakers, disconnect switches, transformers, relays, panels, chargers, batteries, inverters, MCCs, and loads are treated as graph nodes with edges to visually adjacent conductors or named bus backbones.
- BUS-4160-A/B/C, BUS-480-1A/B/C, BUS-125DC-A/B, and SWYD-115KV are treated as connection backbones rather than expanding every visible tap into separate anonymous junctions.
- Duplicate visible taps between the same two named nodes, such as repeated vertical taps from BUS-480-1A to MCC-A1, were collapsed into one undirected edge.
- The first 4160 feeder branch in each train is high-recall modeled as feeding both the transformer path (TR-480-1A/B/C to CB-52-48A/B/C to BUS-480-1A/B/C) and the RHR motor-starter path, because the raw geometry shows the transformer and starter sharing the branch column.

## Ambiguous Or Lower-Confidence Items

- DS-4A01/DS-4B01/DS-4C01 to TR-480-1A/B/C are medium confidence because the transformer winding is visually adjacent to the first feeder column and the 480V breaker path, but the pin topology is compressed.
- 480V CHGR-B FEEDER to CHGR-125-1B is medium confidence because the dashed feeder is routed through a long lower lane and the endpoint is less direct than the A charger feeder.
- PNL-RPS-A to CHGR-125-1B is medium confidence; the dashed line and label are visible in the same lower control lane but the exact pin entrance is tight.
- RELAY-K501A/RELAY-K501B to RPS TRIP BUS are medium confidence where the dashed relay routes share the named trip-bus lane.
- CB-4A01/CB-4B01/CB-4C01 to RPS TRIP BUS are low-to-medium confidence high-recall inclusions from the dashed W022/W025/W028 first-feeder control/interlock routes.
- TC-52-4A to CB-52-4A is low confidence because it is inferred from the visible tag reference plus trip-coil semantics, not from a direct same-sheet hardwire to the breaker symbol.
- RELAY-K501A to INV-120-1B is medium confidence from the solid routed line in the bottom band that drops toward the INV-120-1B block.

## Rejected Or Not Modeled

- Unnamed blue/orange/purple topology nodes from `wire_nodes.csv` were not added as graph nodes unless a visible label named the bus/feeder/tie.
- Title block, revisions, notes, border grid, legend example symbols, and reference drawing text were not modeled as components or edges.
- Crossings without junction dots were not connected, including routed lower dashed lanes that visibly cross vertical conductors without a connection dot.
- Label leader ticks and component callout lines were not modeled as electrical connections.

## Validation

- Unknown nodes in edges: 0
- Duplicate undirected pairs: 0
- Symmetric adjacency matrix: True
- Diagonal zero: True
