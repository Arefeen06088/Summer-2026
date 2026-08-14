# Document 18 Connectivity Extraction Notes

Only the raw schematic, wires mask, wires mask overlay, and generated crops under `Raw + wires` were used. Existing result/validation files were not opened or used. No GT-derived feedback or off-the-shelf OCR was used.

## Final Result

- Nodes: 200
- Edges: 201
- Symmetric matrix: True
- Diagonal zero: True

## Round Progress

- `round1_diego`: 200 nodes, 201 edges.
- `round1_jennifer`: 200 nodes, 201 edges.
- `round2_diego`: 200 nodes, 201 edges.
- `round2_jennifer`: 200 nodes, 201 edges.

## Precision Decisions

- Corrected Diego R1 label `PNL-TC-C7` to visually supported `PNL-IC-C7`.
- Kept `TB-RPS-A` inline on the A-side solid feeder and also on the dashed PT/RPS control chain.
- Kept UAT lower breaker stubs as dangling from `TR-UAT-1A/B`; no `CB-UAT-A/B` to 4160 bus edges were added.
- Kept `TB-RPS-B` only on the dashed PT/control chain; no `TB-RPS-B--TR-480-D1` edge was added.
- Kept compact RPS relay harness edges through `PLC-RPS-A/B` and `RELAY-K102/K202`; no extra relay-to-relay or direct JB-to-annunciator edges were added.

## Token Estimate

- Expected total tokens estimated: 492920 (low 481620, high 512120).
