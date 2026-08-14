# Document 25 Round 02 Jennifer Notes

## Method

- Inspected the raw schematic first, then used only the allowed overlays/crops, `component_visual_ocr_labels.csv`, `wire_nodes.csv`, and Diego round-01 files.
- Did not use Ground Truth, evaluator outputs, previous-document connectivity, or off-the-shelf OCR.
- Preserved Diego's 204-node order and node labels. No node renames, additions, or removals were made.
- Treated crossings without dots as non-connections, following the drawing note.

## Counts

- Node count: 204
- Edge count: 205
- Edge kind counts: `control_interlock_trip: 17`, `dc_power: 9`, `external_feeder: 1`, `ground_reference: 3`, `instrument_signal: 2`, `power: 173`
- Confidence counts: `high: 201`, `medium: 4`

## Accepted From Round 01

- Kept the named logical bus/backbone nodes because the raw sheet visibly names them: `SWYD-115KV`, `BUS-4160-A/B/C`, `BUS-480-1A/B/C`, `BUS-125DC-A/B`, `RPS TRIP BUS`, `PNL A/B TIE`, and the two 480V charger feeder arrows.
- Kept the top source, UAT/SAT, EDG, bus tie, and bus tap paths. The raw schematic shows direct solid paths and visible bus taps; no-dot crossings were not joined.
- Kept `DS-4A01/DS-4B01/DS-4C01` to `TR-480-1A/B/C` as medium-confidence power edges. The first feeder column visibly splits through the transformer leg and the RHR motor-starter leg, although the pin geometry is compressed.
- Kept `PNL-RPS-A -- CHGR-125-1B` as a medium-confidence dashed control edge. The lower dashed route is visibly adjacent to and appears to enter the B charger area, but the terminal is tight.
- Kept `TC-52-4A -- RPS TRIP BUS` as a direct dashed trip-bus termination on the trip coil's right side.

## Pruned Or Replaced Edges

- Removed `480V CHGR-B FEEDER -- CHGR-125-1B`. The labelled feeder lane is visible, but it runs as a long routed dashed lane above the B charger without a clean direct terminal into the charger box.
- Removed `RELAY-K501A -- RPS TRIP BUS` and `RELAY-K501B -- RPS TRIP BUS`. The relays do not visibly terminate on the labelled trip-bus lane; their dashed routes terminate at `TC-52-4A`.
- Added direct replacements `RELAY-K501A -- TC-52-4A` and `RELAY-K501B -- TC-52-4A`, both as high-confidence `control_interlock_trip` edges.
- Removed `TC-52-4A -- CB-52-4A`. The tag name semantically references the breaker, but no same-sheet wire directly connects the trip coil to `CB-52-4A`.
- Removed `CB-4A01 -- RPS TRIP BUS`, `CB-4B01 -- RPS TRIP BUS`, and `CB-4C01 -- RPS TRIP BUS`. The dashed first-feeder routes pass near the first breakers, but the raw/nodes overlays do not show a direct breaker terminal to the named trip bus.
- Removed `RELAY-K501A -- INV-120-1B`. The solid route is near the relay label text, not visibly connected to the relay symbol.

## Edge Kind Corrections

Changed these MCC branch breaker-to-relay/fuse edges from `control_interlock_trip` to `power` because the visible segment from breaker to relay/fuse is solid. The downstream dashed segment to the MOV or panel remains `control_interlock_trip`.

- `CB-48A02 -- K-48A02`
- `CB-48A05 -- K-48A05`
- `CB-48A06 -- XFU-48A06`
- `CB-48B02 -- K-48B02`
- `CB-48B05 -- K-48B05`
- `CB-48B06 -- XFU-48B06`
- `CB-48C02 -- K-48C02`
- `CB-48C05 -- K-48C05`
- `CB-48C06 -- XFU-48C06`

## Remaining Ambiguities

- The first 4.16 kV feeder split to both the 480 V transformer and RHR motor starter is visually supported, but retained at medium confidence because the transformer/starter pin layout is compact.
- `PNL-RPS-A -- CHGR-125-1B` remains medium confidence due to the tight dashed-lane entry around the B charger.
- `480V CHGR-B FEEDER` remains as a visible named logical feeder node, but round 02 leaves it without an edge because the visible termination is ambiguous.

## Validation

- Unknown nodes in edges: 0
- Duplicate undirected pairs: 0
- Symmetric adjacency matrix: True
- Diagonal zero: True
