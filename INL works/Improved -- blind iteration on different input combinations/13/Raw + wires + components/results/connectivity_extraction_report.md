# Document 13 Connectivity Extraction Report

Source policy: only raw schematic and derived visual aids from the provided resource folder were used. No GT or GT-derived feedback was used.

## Final Matrix

- Final node count: 186
- Final accepted edge count: 183
- Matrix file: `final_connectivity_matrix.csv`
- Sparse edge file: `final_sparse_edges.csv`

## Round Summary

| Round | Agent | Nodes | Edges | Summary |
|---|---:|---:|---:|---|
| round01_diego | Diego | 197 | 195 | Initial high-recall extraction included label/continuation nodes and tentative JB-to-DC/voltage-label/local-I/O edges. |
| round01_jennifer | Jennifer | 187 | 183 | Removed label-only and continuation-only nodes/edges, kept only landed relay-control edges, but still listed isolated GND-B. |
| round02_diego | Diego | 186 | 183 | Agreed with Jennifer's corrected candidate and noted the isolated GND-B count issue. |
| round02_jennifer | Jennifer | 186 | 183 | Removed isolated GND-B for the final accepted/connected matrix. |

## Final Precision Changes

- Removed `125VDC-A/B/C/D` voltage-label nodes.
- Removed `LOCAL-IO-A/B/C/D` line-end label nodes.
- Removed continuation/destination annotations `CONTINUATION-125VDC-SHT-DC-2` and `ANNUNCIATOR-PPC`.
- Removed `JB-X1` to `DC-BUS-X` edges because the dashed/control route does not cleanly land on the DC bus.
- Removed isolated `GND-B` from the final accepted/connected matrix.
- Kept only relay-to-breaker dashed control edges that visibly land at a specific breaker/contact.

## Excluded Or Still Uncertain

- `125VDC-A/B/C/D voltage labels`
- `LOCAL-IO-A/B/C/D line-end labels`
- `CONTINUATION-125VDC-SHT-DC-2`
- `ANNUNCIATOR-PPC`
- `JB-X1,DC-BUS-X`
- `LC-480X,CHG-125X`
- `UPS-X,unlabeled output`
- `auto-start labels to EDGs`
- `ESFAS permissive note text to relays`
- `GND-A,GND-PLANT`
- `GND-B,GND-PLANT`
- `isolated GND-B node`
