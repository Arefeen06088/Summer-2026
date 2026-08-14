# Round 01 Jennifer Review - Doc 15

## Scope

Reviewed only the current doc 15 input resources, generated inspection aids/crops, and Diego round 01 proposal files. No ground truth, evaluator outputs, validation metrics, previous doc outputs, or GT-derived feedback were used.

## Node Decisions

- Kept Diego's stable node set: 183 nodes total.
- Retained all 163 detected component labels because none were clearly non-components on visual inspection.
- Kept the visually named buses: BUS-SWY-1/2, BUS-NSS-1/2, BUS-416A/B/C/D, BUS-480A/B/C/D, and BUS-DC-A/B/C/D.
- Kept MCC and GND component nodes from the detected inventory.
- Kept SEQ-1AB, RPS-AC-1, SEQ-2CD, and RPS-AC-2 as visual component-like control blocks. They are drawn as labeled blocks with dashed control wiring, not anonymous WN-* points.
- Did not add any anonymous wire-node endpoints.

## Accepted Edge Policy

Accepted edges are direct, visually supported solid power/bus/device-terminal connections. Dots on buses were treated as intentional junctions. Crossings without dots were not treated as connections.

Normally-open tie segments were kept only as solid drawn connections into and between the tie devices, with `solid_bus_tie_normally_open` edge type. No direct BUS-416A-to-BUS-416B or BUS-416C-to-BUS-416D edge was added.

Accepted edge count: 126.

## Removed Or Demoted From Diego High

- Demoted `BUS-NSS-1` -> `DG-1A` to uncertain. DG-1A visually touches/lies on the NSS bus line, but there is no explicit bus junction dot and the layout could represent a diesel source symbol drawn adjacent to the bus.
- Removed `BUS-NSS-1` -> `DG-1B` from accepted. The Div 1B/top-center-left crop shows a visible gap between BUS-NSS-1 and the DG-1B symbol; the clear solid connection is `DG-1B` -> `CB-DG-B`.
- Demoted `BUS-NSS-2` -> `DG-1C` to uncertain for the same visual-contact/no-dot concern as DG-1A.
- Removed `BUS-NSS-2` -> `DG-1D` from accepted. The Div 2B/top-right crop shows DG-1D separated from BUS-NSS-2; the clear solid connection is `DG-1D` -> `CB-DG-D`.

## Uncertain Edge Policy

All dashed control/trip/status paths were kept out of the accepted edge file and placed in `round_01_jennifer_uncertain.csv` when they were visually plausible. This includes:

- Dashed normal-feeder/diesel-breaker control spans.
- Dashed SEQ/RPS control block associations.
- Dashed breaker-to-relay paths.
- Long dashed relay-to-terminal-block routes.
- Dashed 125 VDC/control row paths, including BAT/CHG/BUS-DC/INV/CP/TB/JB and BUS-DC/GND references.

Uncertain edge count: 70.

## Verification

Endpoint audit passed: every accepted and uncertain edge endpoint exists in `round_01_jennifer_nodes.csv`.
