# Document 15 Connectivity Extraction Report

Source policy: only raw schematic and derived visual aids from the provided resource folder were used. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.

## Final Matrix

- Final node count: 183
- Final accepted edge count: 194
- Matrix file: `final_connectivity_matrix.csv`
- Sparse edge file: `final_sparse_edges.csv`

## Round Summary

| Round | Agent | Nodes | Edges | Summary |
|---|---:|---:|---:|---|
| round01_diego | Diego | 183 | 194 | Accepted all visually landed power, DC, ground, MCC relay, and local tie-control edges; kept DG-to-NSS and cross-side tie-control edges uncertain. |
| round01_jennifer | Jennifer | 183 | 194 | Accepted Diego's edge set unchanged; confirmed uncertain DG-to-NSS and cross-side SEQ/RPS cases should not be promoted. |
| round02_diego | Diego | 183 | 194 | Rechecked Jennifer's unchanged set and agreed the extraction was saturated. |
| round02_jennifer | Jennifer | 183 | 194 | Final signoff: accepted edge set unchanged and remaining ambiguous cases excluded. |

## Final Precision Decisions

- Kept all Diego R1 accepted edges after Jennifer's visual review.
- Accepted only landed DG-to-`CB-DG-*` feeders, not DG-to-`BUS-NSS-*` overlaps.
- Accepted only direct SEQ/RPS dashed landings: DG-side for A/C and NF-side for B/D.
- Kept MCC `CB-*` to `RLY-*` dashed control edges because each is visibly landed.
- Kept only `RLY-*06` onward terminal-block control edges because only those continue to `TB-1*`.

## Excluded Or Still Uncertain

- DG-1A,BUS-NSS-1,P - DG overlaps/touches NSS bus row; vertical DG-to-CB-DG-A feeder is the clean landed source edge
- DG-1B,BUS-NSS-1,P - DG overlaps/touches NSS bus row; vertical DG-to-CB-DG-B feeder is the clean landed source edge
- DG-1C,BUS-NSS-2,P - DG overlaps/touches NSS bus row; vertical DG-to-CB-DG-C feeder is the clean landed source edge
- DG-1D,BUS-NSS-2,P - DG overlaps/touches NSS bus row; vertical DG-to-CB-DG-D feeder is the clean landed source edge
- Cross-side SEQ/RPS candidates - possible only through shared dashed nets, not direct clean landings
