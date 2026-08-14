# Round 01 Jennifer Review Notes - Doc 24

## Evidence Boundary
- Used only doc 24 input resources and artifacts derived from those resources: raw schematic PNG, wire masks/overlays, component inventory, Diego round 1 matrix/notes, and doc 24 inspection crops.
- Raw schematic was treated as primary evidence. Overlays, wire masks, labels, and crops were used only as aids.
- No ground truth, evaluator output, metric feedback, or derived scoring information was used.

## Node List Decision
- Accepted Diego's node set size and structure: physical components plus the six compact printed bus nodes `BUS-101A`, `BUS-101B`, `BUS-201A`, `BUS-201B`, `DC-BUS-125A`, and `DC-BUS-125B`.
- Corrected the two DG manual switch labels from the inventory names to the raw schematic text: `SW-PGA-A` -> `SW-MAN-A`, and `SW-PGA-B` -> `SW-MAN-B`. The zoom crops clearly read `SW-MAN-A` and `SW-MAN-B`; these are relabels of the same physical switch symbols, not added components.
- Did not add descriptive bus text such as voltage/control-power/raceway descriptions. No WN IDs, unlabeled junctions, section titles, feeder notes, or boundaries were added.
- Retained `SYNC-CAB` as a visible physical cabinet node, but left it isolated after removing the unsupported tie-breaker edge.

## Edge Changes From Diego
- Changed `TB-DG-A -- SW-PGA-A` to `TB-DG-A -- SW-MAN-A`: same dashed DG manual-control path, corrected to the raw printed switch label.
- Changed `TB-DG-B -- SW-PGA-B` to `TB-DG-B -- SW-MAN-B`: same dashed DG manual-control path, corrected to the raw printed switch label.
- Removed `CB-TIE-1 -- SYNC-CAB`: the raw zoom shows `SYNC-CAB` next to a dashed routing/channel boundary, with no unambiguous direct electrical/control lead from `CB-TIE-1`.
- Removed `ESFAS-PNL-B -- LOAD-SHED-CAB`: the B-side crop shows `PNL-DC-B -- ESFAS-PNL-B` and DC bus taps, but no visible dashed control run from `ESFAS-PNL-B` to `LOAD-SHED-CAB`. Diego's B-side load-shed edge appeared to be symmetry fill rather than visual evidence.
- Added no new edges.

## Kept Edges Reviewed As Supported
- Kept the top source paths: `OFFSITE-1 -- CB-101A -- TR-SAT-1A -- BUS-101A`, `OFFSITE-2 -- CB-101B -- TR-SAT-1B -- BUS-101B`, `EDG-1A -- CB-DG1A -- BUS-101A`, and `EDG-1B -- CB-DG1B -- BUS-101B`.
- Kept the DG manual-control paths as `SW-MAN-A -- TB-DG-A -- CB-DG1A` and `SW-MAN-B -- TB-DG-B -- CB-DG1B`.
- Kept the bus tie as `BUS-101A -- CB-TIE-1 -- BUS-101B`.
- Kept safety transformer feeds: `BUS-101A -- CB-201A -- TR-1A -- CB-202A -- BUS-201A` and `BUS-101B -- CB-201B -- TR-1B -- CB-202B -- BUS-201B`.
- Kept each MCC feeder chain `BUS-201* -- CB-* -- DS-* -- MCC-* -- TB-* -- load`, with dashed control simplified as `MCC-* -- RELAY-K*` and `HS-* -- RELAY-K*`. I did not add `MCC-* -- HS-*` clique edges.
- Kept DC bus taps to batteries, chargers, inverters, DC panels, A-side `METER-V1`, panel grounds, `PNL-DC-* -- ESFAS-PNL-*`, and `INV-120* -- PNL-AC-*`.
- Kept instrument/RPS paths `PT/LT/FT -- JB-401* -- TB-RPS-* -- RPS-PNL-*`, JB grounds, AC/RPS/trip/relay chains, RPS-to-annunciator signal simplifications, and `ANN-PNL-1 -- SEQ-REC-1`.
- Kept `LOAD-SHED-CAB -- TDR-1`, `LOAD-SHED-CAB -- TDR-2`, `LOAD-SHED-CAB -- LAMP-ALM-A`, and `LOAD-SHED-CAB -- LAMP-ALM-B`; the cabinet has visible dashed/dotted routes to those named endpoints.
- Kept `ESFAS-PNL-A -- LOAD-SHED-CAB` and `ESFAS-PNL-A -- TRIP-MOD-A`; both A-side dashed routes are visible.

## Remaining Uncertain Cases
- `SYNC-CAB` is excluded from connectivity, despite being retained as a node, because the visible dashed line reads as routing/channel context rather than a definite connection.
- `ESFAS-PNL-B -- LOAD-SHED-CAB` is excluded; possible A/B functional symmetry was not used as evidence.
- RPS-to-annunciator edges are included as named-endpoint simplifications of dotted signal routes; unlabeled junctions along those routes were deliberately not modeled.
- Load-shed-to-alarm edges are included as named-endpoint simplifications of the visible dotted alarm route.

## Validation Summary
- Node count: 200.
- Unique undirected edge count: 200.
- Rows and columns have same names/order: True.
- Symmetric: True.
- Diagonal zero: True.
- Isolated nodes: 1 (SYNC-CAB).
- Output matrix: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\24\Results\Iteration_1\round_01_jennifer_matrix.csv`
- Output notes: `C:\Asif_all_python_projects\INL\Improved -- blind iterations\24\Results\Iteration_1\round_01_jennifer_notes.md`
