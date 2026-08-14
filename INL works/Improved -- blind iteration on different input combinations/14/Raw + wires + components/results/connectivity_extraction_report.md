# Document 14 Connectivity Extraction Report

Source policy: only raw schematic and derived visual aids from the provided resource folder were used. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.

## Final Matrix

- Final node count: 156
- Final accepted edge count: 157
- Matrix file: `final_connectivity_matrix.csv`
- Sparse edge file: `final_sparse_edges.csv`

## Round Summary

| Round | Agent | Nodes | Edges | Summary |
|---|---:|---:|---:|---|
| round01_diego | Diego | 178 | 174 | Initial proposal kept all plausible power/DC/signal/ground edges and accepted CB-to-relay dashed control edges; included several visible but isolated panel nodes. |
| round01_jennifer | Jennifer | 156 | 157 | Removed relay/control edges and isolated ambiguous panel nodes because the dashed conductors were adjacent or passing nearby without clean landed terminals. |
| round02_diego | Diego | 156 | 157 | Rechecked relay, panel, DC/UPS, and tie crops; agreed with Jennifer's corrected edge list unchanged. |
| round02_jennifer | Jennifer | 156 | 157 | Confirmed saturated/final unchanged; relay/panel/tie ambiguities remain excluded or uncertain. |

## Final Precision Changes

- Demoted all `CB-*` to `RELAY-*` control edges from Diego R1 because relay symbols were adjacent to dashed leads without clear landed terminals.
- Excluded isolated/ambiguous panel nodes `PANEL-ESF-A`, `PANEL-LS-A`, `PANEL-LS-B`, `PANEL-RPS-B`, and `PANEL-ESF-B`.
- Kept `PANEL-RPS-A` because the solid feeder visibly lands through it to `CHG-125A`.
- Kept `PANEL-MCR`, `PANEL-ANN`, and `CB-DC-TIE` dashed path because the vertical dashed route visibly lands through the two panel symbols to the DC tie breaker.

## Excluded Or Still Uncertain

- BUS-480A,CHG-125A,P - direct feed possible only if PANEL-RPS-A is crossed rather than landed
- All CB-* to RELAY-* dashed candidates - relay symbol adjacent to dashed lead, no clean landing
- All RELAY-* to panel candidates - dashed run heads toward panel bundle, no panel landing visible
- PANEL-ESF-A,PANEL-RPS-A,D - dashed conductors pass near panels without explicit landing
- PANEL-RPS-A,PANEL-LS-A,D - dashed conductors pass near panels without explicit landing
- PANEL-LS-B,PANEL-RPS-B,D - dashed conductors pass near panels without explicit landing
- PANEL-RPS-B,PANEL-ESF-B,D - dashed conductors pass near panels without explicit landing
