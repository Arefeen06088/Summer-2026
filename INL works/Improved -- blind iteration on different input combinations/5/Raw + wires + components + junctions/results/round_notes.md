# Document 5 Connectivity Extraction Notes

Allowed resource folder only:
`C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw + wires + components + junctions`

No Ground Truth or GT-derived feedback was used.

## Rounds

1. Diego high-recall extraction:
   - Proposed source, bus, safety-division, DC/UPS, relay, control-bay, and ground-grid nodes.
   - Used `VLV-MISV-A/B` before Jennifer corrected the raw-label spelling.
   - Matrix files:
     - `round_01_diego_high_recall_connectivity_matrix.csv`
     - `round_01_diego_high_recall_plus_uncertain_connectivity_matrix.csv`

2. Jennifer precision review:
   - Corrected `VLV-MISV-A/B` to `VLV-MSIV-A/B`.
   - Accepted five supported ATS/rectifier/load edges from Diego's uncertain set.
   - Rejected direct LC-to-ATS abstractions as final edges.
   - Left protection-bay dashed lines and GND-GRID dotted drops out of the final graph because endpoint pairing was not reliable without guessing.

3. Diego saturation review:
   - Agreed with Jennifer.
   - Final graph saturated at 112 nodes and 105 edges.

## Final Counts

- Nodes: 112
- Edges: 105
- Connectivity matrix is symmetric with zero diagonal.

## Token Usage

The official Responses input-token counting endpoint could not be called because no `OPENAI_API_KEY` is available in this environment. Token artifacts are therefore estimates:

- Text/context: manual round-specific estimates, with local tokenizer fallback available for small strings.
- Images/files: offline high-detail tile proxy based on image dimensions.
- Actual usage objects and reasoning-token counts were not exposed by the local multi-agent tool responses.
