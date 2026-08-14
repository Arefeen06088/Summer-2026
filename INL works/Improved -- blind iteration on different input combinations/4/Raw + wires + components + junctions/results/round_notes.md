# Document 4 Connectivity Extraction Notes

Allowed resource folder only:
`C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\4\Raw + wires + components + junctions`

No Ground Truth or GT-derived feedback was used.

## Rounds

1. Diego high-recall extraction:
   - Proposed the main source, bus, feeder, load-center, DC/UPS, and control topology.
   - Marked several plausible dashed/control/ground candidates as uncertain.
   - Matrix files:
     - `round_01_diego_high_recall_connectivity_matrix.csv` uses Diego's committed edge list.
     - `round_01_diego_high_recall_plus_uncertain_connectivity_matrix.csv` additionally includes his uncertain edge candidates.

2. Jennifer precision review:
   - Kept the main power topology.
   - Added GND-NG-A and GND-NG-B as named nodes with transformer ground edges.
   - Accepted relay-to-terminal-block and annunciator-to-recorder dashed control edges where endpoints visibly terminate.
   - Rejected dashed crossings near CB-LC-B/CB-LC-B2 and BUS-UPS-B because they do not visibly terminate there.

3. Diego saturation review:
   - Agreed with Jennifer.
   - Final graph saturated at 120 nodes and 123 edges.

## Final Counts

- Nodes: 120
- Edges: 123
- Connectivity matrix is symmetric with zero diagonal.

## Token Usage

The official Responses input-token counting endpoint could not be called because no `OPENAI_API_KEY` is available in this environment. Token artifacts are therefore local estimates:

- Text: `tiktoken` using `o200k_base` when available.
- Images/files: offline high-detail tile proxy based on image dimensions.
- Actual usage objects, cached input tokens, output tokens, and reasoning tokens were not exposed by the local multi-agent tool responses.
