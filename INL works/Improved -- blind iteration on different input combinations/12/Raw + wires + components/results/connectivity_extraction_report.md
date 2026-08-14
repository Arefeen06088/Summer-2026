# Document 12 Connectivity Extraction Report

Source policy: only raw schematic and derived visual aids from the provided resource folder were used. No GT or GT-derived feedback was used.

## Final Matrix

- Final node count: 160
- Final accepted edge count: 166
- Matrix file: `final_connectivity_matrix.csv`
- Sparse edge file: `final_sparse_edges.csv`

## Round Summary

| Round | Agent | Nodes | Edges | Summary |
|---|---:|---:|---:|---|
| round01_diego | Diego | 160 | 171 | Initial extraction included visible PT nodes with tentative PT-to-bus signal edges and several lower ESF/RPS signal/power candidates. |
| round01_jennifer | Jennifer | 160 | 166 | Kept node list, removed unlanded PT-to-bus and ESF-bus-to-panel edges, removed unlanded ESFAS-B-to-sequence-recorder edge, and corrected ANN-to-27 edge types. |
| round02_diego | Diego | 160 | 166 | Agreed with Jennifer's corrected final candidate. |
| round02_jennifer | Jennifer | 160 | 166 | Final precision signoff after Diego saturation response. |

## Final Precision Changes From Diego R1

- Removed unlanded PT-to-bus signal edges while retaining `PT-4160A` and `PT-4160B` as visible component nodes.
- Removed unlanded `BUS-120VAC-ESF` to `PNL-ESFAS-A/B` edges.
- Removed unlanded `PNL-ESFAS-B` to `SEQ-REC-1` signal edge.
- Changed `ANN-480A/B` to `RELAY-27A/B` from interlock type to dashed control type.
- Kept `SPARE-A2` because the visible spare box is landed by `DS-F015`.

## Excluded Or Still Uncertain

- `BUS-4KV-A,PT-4160A,SIG`
- `BUS-4KV-B,PT-4160B,SIG`
- `BUS-120VAC-ESF,PNL-ESFAS-A,P`
- `BUS-120VAC-ESF,PNL-ESFAS-B,P`
- `PNL-ESFAS-B,SEQ-REC-1,SIG`
- `CB-M1A,CB-M2A,I`
- `CB-M1B,CB-M2B,I`
- `CB-111,CB-211,I`
- `CB-112,CB-212,I`
- `ATS-INV,DC-BUS-A,D`
- `ATS-INV,DC-BUS-B,D`
- `BUS-120VAC-ESF,SEQ-REC-1,SIG`
- `TB-ANN-1,PNL-ESFAS-A,SIG`
- `ANN-480A,PNL-ESFAS-A,SIG`
- `ANN-480B,PNL-ESFAS-B,SIG`
- `RELAY-27A,RELAY-86A,D`
- `RELAY-27B,RELAY-86B,D`
- `TB-RPS-A,PNL-ESFAS-A,D`
- `TB-RPS-B,PNL-ESFAS-B,D`
- `ANN-480A,RELAY-50A,D`
- `ANN-480B,RELAY-50B,D`
- `BUS-480-C,MCC-2A,P`
- `BUS-480-D,MCC-2B,P`
