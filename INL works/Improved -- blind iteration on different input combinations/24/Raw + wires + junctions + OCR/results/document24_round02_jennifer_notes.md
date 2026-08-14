# Document 24 Round-02 Jennifer Notes

## Method And Constraints

- Inspected the raw schematic first, then used only the allowed overlays, precision crops, component index, and wire-node aid.
- Did not use Ground Truth, evaluator outputs, previous-document connectivity, or GT-derived feedback.
- Did not use off-the-shelf OCR. Label decisions are from raw visual inspection and the allowed component index as an aid.
- Preserved Diego's 200-node order and node file. No nodes were added, removed, or renamed in round-02.

## Precision Changes From Diego

### Pruned Edges

- `ESFAS-PNL-B -- LOAD-SHED-CAB` (`control_trip`, medium): removed. In the raw bottom-right crop, the dashed load-shed route passes above/right of ESFAS-PNL-B but does not visibly terminate into the ESFAS panel.
- `LOAD-SHED-CAB -- LAMP-ALM-A` (`signal`, medium): removed. The dotted signal trunk passes above LAMP-ALM-A, but no dotted drop or terminal enters the alarm lamp circle.
- `LOAD-SHED-CAB -- LAMP-ALM-B` (`signal`, medium): removed. The dotted signal trunk passes above LAMP-ALM-B, but no dotted drop or terminal enters the alarm lamp circle.

### Accepted Medium Edges

- `CB-TIE-1 -- SYNC-CAB`: retained as medium. The central dashed control/trip route drops from CB-TIE-1 through the SYNC-CAB footprint, but the routing channel is not separately named.
- `SYNC-CAB -- LOAD-SHED-CAB`: retained as medium. The same dashed vertical route continues from SYNC-CAB to LOAD-SHED-CAB.
- `ESFAS-PNL-A -- LOAD-SHED-CAB`: retained as medium. A dashed line visibly leaves ESFAS-PNL-A and turns through the routed load-shed channel.
- `TRIP-MOD-A -- LOAD-SHED-CAB`: retained as medium. TRIP-MOD-A ties into the same dashed routed load-shed channel.
- `TRIP-MOD-B -- LOAD-SHED-CAB`: retained as medium. TRIP-MOD-B has a visible dashed run into the right-side load-shed routing channel.
- `TB-RPS-A -- ANN-PNL-1` and `TB-RPS-B -- ANN-PNL-1`: retained as medium. Both dotted RPS terminal-block trunks continue toward the central annunciator path, but no named intermediate junction is provided.
- `LOAD-SHED-CAB -- ANN-PNL-1`: retained as medium. The central dotted drop visibly runs from LOAD-SHED-CAB to ANN-PNL-1; the nearby crossing trunk has no named junction.

## Other Reviewed Areas

- Repeated feeder columns were retained: each bus-to-CB-to-DS-to-MCC-to-TB-to-load chain is solid power, and each MCC-to-relay / HS-to-relay control edge has a visible dashed run.
- Bottom DC/control areas were retained except for the B-side ESFAS-to-load-shed prune noted above. DC bus taps, inverter-to-AC-panel feeds, PNL-AC/RPS/TRIP-MOD links, RPS relay chains, instrument dotted trunks, and grounds match the raw line styles.
- Switch labels `SW-MAN-A` and `SW-MAN-B` were kept. The raw schematic reads `SW-MAN-A/B`; the aid/index `SW-PGA-A/B` labels remain rejected.
- Edge kinds remain legend-consistent: solid lines as `power` or `dc_power`, dashed lines as `control_trip`, dotted lines as `signal`, and ground symbols as `ground`.

## Remaining Ambiguities

- Central routed dashed/dotted trunks are represented as direct component-to-component edges only where the line visibly enters a named component. No anonymous wire nodes were introduced.
- The retained TB-RPS-to-ANN signal edges are still medium because the long dotted trunks have no explicit named intermediate branch node.
- The retained CB-TIE/SYNC/LOAD-SHED control edges are still medium because the vertical dashed route is a routed channel rather than a fully labeled terminal path.

## Counts

- Node count: 200
- Edge count: 202
- Node type counts: {'logical_bus': 6, 'physical_component': 194}
- Edge kind counts: {'control_trip': 61, 'dc_power': 11, 'ground': 4, 'power': 112, 'signal': 14}
- Confidence counts: {'high': 194, 'medium': 8}

## Validation

- No unknown edge endpoints: passed
- No duplicate undirected pairs: passed
- Adjacency matrix symmetric: passed
- Adjacency matrix diagonal zero: passed
