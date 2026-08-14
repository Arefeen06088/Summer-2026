# Document 24 Connectivity Extraction

Blind visual extraction using only the raw schematic and derived visual aids in the resource folder. No GT, GT-derived feedback, or OCR tools were used.

## Rounds

1. Diego high-recall extraction included visually plausible power, control, and signal edges plus seven low-confidence/uncertain extras.
2. Jennifer precision review retained the repeated feeder and DC/control structure, accepted `CB-TIE-1 -- SYNC-CAB`, and removed unsupported common-control overconnections.
3. Diego convergence review was run against Jennifer's correction.
4. Jennifer final confirmation was run after Diego's convergence reply.

## Final Matrix

- Nodes: 200
- Final accepted undirected edges: 214
- Matrix file: `final_connectivity_matrix.csv`
- Edge file: `final_edges.csv`

## Label Decisions

- Use `BUS-201A` and `BUS-201B`; adjacent long text is descriptive bus text.
- Use `PMP-LP208A/B`, `COMP-C209A/B`, and `VALVE-MV207A/B` as visible component labels.
- Use `METER-V1` only; no visible `METER-V2` was found.

## Token Estimation

The OpenAI Responses input-token counting endpoint was not called because no API key is available in this environment. Actual usage objects were not exposed by the Codex subagent notification/tooling. The local estimate uses `tiktoken` (`o200k_base`) for text when available and high-detail image tile sizing for image inputs.

- Estimated input tokens: 62365
- Estimated image input tokens: 46325
- Expected output tokens: 11050
- Estimated reasoning tokens: 5500
- Expected total tokens: 78915
