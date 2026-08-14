# Document 26 Connectivity Extraction

Blind visual extraction using only the raw schematic and derived visual aids in the resource folder. No GT, GT-derived feedback, or OCR tools were used.

## Rounds

1. Diego high-recall extraction captured the 4.16 kV A/B source buses, transformer feeders, 480 V load-center branches, 125 VDC buses, inverter buses, 120N buses, relays, terminal blocks, and PTs. Low-confidence dashed trunk guesses were kept as round-1 proposed edges only.
2. Jennifer accepted the main graph, excluded Diego's speculative dashed trunks, and initially proposed two RPS-panel to 120N-bus edges.
3. Diego rejected the two added RPS-to-120N edges after focused lower-control review.
4. Jennifer final confirmation removed those two edges and made no other graph changes.

## Final Matrix

- Nodes: 200
- Round 1 Diego edges: 211
- Round 2 Jennifer edges: 203
- Round 3 Diego edges: 201
- Round 4 Jennifer final edges: 201
- Matrix file: `final_connectivity_matrix.csv`
- Edge file: `final_edges.csv`

## Key Precision Decisions

- Buses are explicit nodes; devices sharing a bus are connected to the bus node, not to each other as a clique.
- Wire labels such as `480-A-11`, `4-416-A-01`, `DC-A-INV`, and `120-A-N` are treated as wire identifiers, not component nodes.
- `RPS-PNL-A--BUS-120N-A` and `RPS-PNL-B--BUS-120N-B` were removed after final review.
- Clear dashed/instrument paths retained: `RPS-PNL-*--TB-UPS-*`, `RELAY-K7*--TB-RPS-*`, and `TB-RPS-*--PT-*`.

## Token Estimation

The OpenAI Responses input-token counting endpoint was not called because no API key is available in this environment. Actual usage objects were not exposed by the Codex subagent tooling. The estimate uses local text token estimation plus high-detail image tile estimates.

- Estimated input tokens: 64069
- Estimated image/file input tokens: 48280
- Expected output tokens: 11680
- Estimated reasoning tokens: 6400
- Expected total tokens: 82149
