# Jennifer Round 01 Precision Review Notes

## Scope
- Reviewed only doc 21 input resources and doc 21 artifacts/results generated from those resources.
- Did not use ground truth, evaluator output, metric feedback, or anything derived from ground truth.
- Treated the raw schematic as primary evidence; overlays, component labels, wire masks, and crops were only aids.

## Node List
- Accepted Diego's node list unchanged.
- Node set remains the 183 labels from `component_labels_list.csv`, the 14 printed bus nodes, plus raw-visible `CB-204A` and `DS-401B`.
- `CB-204A` stays: the raw EDG-1B feeder visibly prints `CB-204A` between the BUS-201B tap and `DS-201B`.
- `DS-401B` stays: the raw DC/UPS B-side chain visibly prints `DS-401B` before `TR-DC-B` and `RECT-125B`.

## Edge Changes
- Removed 16 Diego edges.
- Added 0 edges.
- Changed rail treatment: ladder row starts were reduced to the single printed BUS-501 rail side that visibly feeds each row.

### Removed Edges
- `BAT-EDG-A` -- `BAT-EDG-B`: Removed: the two EDG battery dashed conductors are drawn as separate paths; no direct battery-to-battery junction is visible.
- `BAT-EDG-A` -- `CP-EDG-A`: Removed: dashed BAT-EDG-A conductor drops to the lower control-ladder area; it does not visibly terminate at CP-EDG-A.
- `BAT-EDG-B` -- `CP-EDG-B`: Removed: dashed BAT-EDG-B conductor drops to a lower ambiguous control path; it does not visibly terminate at CP-EDG-B.
- `BUS-501A` -- `CP-CCW-B`: Removed: CP-CCW-B dashed row starts at BUS-501B, not BUS-501A.
- `BUS-501A` -- `CP-EDG-B`: Removed: CP-EDG-B dashed row starts at BUS-501B, not BUS-501A.
- `BUS-501A` -- `CP-SI-B`: Removed: CP-SI-B row originates from the BUS-501B side; no A-rail junction dot is visible.
- `BUS-501A` -- `CP-SWGR`: Removed: CP-SWGR is connected by visible control/interlock lines, but no direct BUS-501A rail tap is visible.
- `BUS-501A` -- `ESFAS-B`: Removed: ESFAS-B dashed row starts at BUS-501B, not BUS-501A.
- `BUS-501A` -- `RPS-B`: Removed: RPS-B dashed row starts at BUS-501B, not BUS-501A.
- `BUS-501B` -- `CP-CCW-A`: Removed: CP-CCW-A dashed row starts at BUS-501A, not BUS-501B.
- `BUS-501B` -- `CP-CRD`: Removed: CP-CRD lower dashed row is visible from the BUS-501A side; no B-rail tap is visible.
- `BUS-501B` -- `CP-EDG-A`: Removed: CP-EDG-A dashed row starts at BUS-501A, not BUS-501B.
- `BUS-501B` -- `CP-SI-A`: Removed: CP-SI-A row originates from the BUS-501A side; no B-rail junction dot is visible.
- `BUS-501B` -- `CP-SWGR`: Removed: CP-SWGR is connected by visible control/interlock lines, but no direct BUS-501B rail tap is visible.
- `BUS-501B` -- `ESFAS-A`: Removed: ESFAS-A dashed row starts at BUS-501A, not BUS-501B.
- `BUS-501B` -- `RPS-A`: Removed: RPS-A dashed row starts at BUS-501A, not BUS-501B.

### Added Edges
- None.

## Retained Visual Support
- Retained upper switchgear/EDG edges, including `CB-204A`, because the raw top-switchgear crops show direct bus taps and serial feeder components.
- Retained 480 V transformer and MCC feeder/load edges; bus taps, breakers, MCC boxes, loads, and grounds are directly drawn.
- Retained `GND-1`/`GND-2` only on BUS-301A/B and `GND-5`/`GND-6` only on MCC-3A/B, matching the visible ground symbols.
- Retained DC/UPS chains for `DS-401A/B`, `DS-402A/B`, `INV-120C`, and `RECT-24C`; the raw schematic shows serial connections and direct bus outputs.
- Retained row-wise ladder chains and the visible vertical/top interlock links; no all-to-all ladder clique was added.

## Deliberately Excluded or Uncertain
- Excluded all direct `BAT-EDG-A/B` links. The dashed EDG battery paths are visible, but their named termination is ambiguous and they do not visibly land on `CP-EDG-A/B` or on each other.
- Excluded cross-rail ladder edges where a row only visibly starts from the opposite BUS-501 rail.
- Excluded direct BUS-501 rail edges to `CP-SWGR`; it has visible control/interlock wiring but no clear printed rail tap.
- Did not add a `BUS-501A` -- `BUS-501B` edge despite the lower dashed continuation shape, because the rails are printed as separate A/B buses and no explicit tie component is shown.

## Validation Summary
- Node count: 199
- Edge count: 204
- Symmetric: True
- Diagonal zero: True
- Row and column labels: identical and in the same order.
- Isolated nodes: `BAT-EDG-A`, `BAT-EDG-B`.
