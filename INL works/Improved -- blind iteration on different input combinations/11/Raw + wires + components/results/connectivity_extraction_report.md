# Document 11 Connectivity Extraction Report

Source policy: only raw schematic and derived visual aids from the provided resource folder were used. No GT or GT-derived feedback was used.

## Final Matrix

- Final node count: 120
- Final accepted edge count: 136
- Matrix file: `final_connectivity_matrix.csv`
- Sparse edge file: `final_sparse_edges.csv`

## Round Summary

| Round | Agent | Nodes | Edges | Summary |
|---|---:|---:|---:|---|
| round01_diego | Diego | 124 | 132 | Initial high-recall extraction retained four *-SEC conductor labels as nodes and left ATS feeder/DC bus landings uncertain. |
| round01_jennifer | Jennifer | 120 | 136 | Removed conductor-label-only *-SEC nodes, promoted clear MCC-to-ATS and rectifier-to-DC-bus solid landings, kept SSPS dashed routes uncertain. |
| round02_diego | Diego | 120 | 136 | Saturation pass over Jennifer's corrected candidate. |
| round02_jennifer | Jennifer | 120 | 136 | Final precision signoff after Diego saturation response. |

## Final Corrections From Diego R1

- Removed `UAT1-SEC`, `SUT1-SEC`, `UAT2-SEC`, and `SUT2-SEC` as conductor labels rather than standalone nodes.
- Replaced the top-source paths with direct transformer-to-breaker edges.
- Accepted four solid MCC-to-ATS feeder landings.
- Accepted four rectifier-to-125 VDC bus landings.
- Kept dashed SSPS/RPS/ATS interlock routes, relay-to-SSPS routes, relay-to-4160-bus candidates, and ground-to-ground ties excluded/uncertain.

## Excluded Or Still Uncertain

- `PANEL-RPS-A,PANEL-SSPS,D`
- `PANEL-RPS-B,PANEL-SSPS,D`
- `ATS-480-A,PANEL-SSPS,D`
- `ATS-480-B,PANEL-SSPS,D`
- `RELAY-27A,PANEL-SSPS,D`
- `RELAY-27B,PANEL-SSPS,D`
- `RELAY-27C,PANEL-SSPS,D`
- `RELAY-27D,PANEL-SSPS,D`
- `RELAY-27A,BUS-4160-A,D`
- `RELAY-27B,BUS-4160-B,D`
- `RELAY-27C,BUS-4160-C,D`
- `RELAY-27D,BUS-4160-D,D`
- `GND-A,GND-B,G`
- `GND-C,GND-D,G`
