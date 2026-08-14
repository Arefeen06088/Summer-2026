# Document 25 Connectivity Extraction

Blind visual extraction using only the raw schematic and derived visual aids in the resource folder. No GT, GT-derived feedback, or OCR tools were used.

## Rounds

1. Diego high-recall extraction captured the three train 4.16 kV layout, 480 V MCC branches, and bottom 125 VDC/RPS section.
2. Jennifer corrected source labels, accepted visually supported RPS tie/trip-coil routes, and rejected overconnections.
3. Diego convergence review was run against Jennifer's final graph.
4. Jennifer final confirmation was run after Diego's convergence reply.

## Final Matrix

- Nodes: 204
- Final accepted undirected edges: 205
- Matrix file: `final_connectivity_matrix.csv`
- Edge file: `final_edges.csv`

## Key Precision Decisions

- `SWYD-115KV` is the top source bus.
- Train C source is `TR-SAT-1 -> CB-52-4C -> BUS-4160-C`; no `FDR-13C` node was added.
- `MCC-T1 -- MCC-T2` and `PNL-ESF-T05 -- RECT-RPS-T06` were excluded.
- `PNL-RPS-A -- PNL-A/B-TIE -- PNL-RPS-B`, `RELAY-K501A -- TC-52-4A`, and `RELAY-K501B -- TC-52-4A` were retained as visually supported.

## Token Estimation

The OpenAI Responses input-token counting endpoint was not called because no API key is available in this environment. Actual usage objects were not exposed by the Codex subagent notification/tooling. The local estimate uses text estimates plus high-detail image tile sizing.

- Estimated input tokens: 55250
- Estimated image input tokens: 37570
- Expected output tokens: 11850
- Estimated reasoning tokens: 5700
- Expected total tokens: 72800
