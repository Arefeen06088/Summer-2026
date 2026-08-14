# Case 26 Connectivity Extraction Note

Generated: 2026-07-14T11:36:08

## Scope

- Raw resource: `raw -- synthetic_npp_electrical_schematic_v3(1).png`
- Extraction used only the raw schematic and crops derived from that raw schematic under `codes/crops`.
- Ground truth or GT-derived feedback was not used.

## Subagent Rounds

1. Diego high-recall pass: included the 200 component-node set and eight extra dashed-control candidates to preserve the visible 209-connection hypothesis.
2. Jennifer precision pass: accepted the 200 component-node set, rejected wire/route labels as nodes, and removed dashed MOV-control candidates where both component endpoints were not explicit.
3. Diego saturation pass: AGREED with Jennifer's precision graph despite the title-block count tension.
4. Jennifer final confirmation: AGREED.

## Final Decisions

- Final rows are component/node labels only.
- Wire tags, route labels, zone titles, notes, legends, and title-block text are excluded as rows.
- Excluded examples: `4-416-*`, `480-*`, `DC-A-INV`, `DC-B-INV`, `120-A-N`, `120-B-N`.
- Crossings without junction dots are not promoted to edges.
- The final precision matrix excludes Diego's eight dashed MOV-control candidates because Jennifer and Diego agreed they lack unambiguous component endpoints.

## Counts

- Final nodes: 200
- Final undirected component edges: 201
- Matrix is symmetric with zero diagonal.

The title block visibly states 200 components and 209 connections. Diego's round-1 high-recall matrix preserves a 209-edge candidate graph. The saturated Diego/Jennifer precision graph has 201 component-to-component edges after rejecting eight ambiguous dashed route candidates.

## Round Artifact Counts

| Round | Nodes | Edges |
| --- | ---: | ---: |
| `round_01_diego_high_recall` | 200 | 209 |
| `round_02_jennifer_precision` | 200 | 201 |
| `round_03_diego_saturation` | 200 | 201 |
| `round_04_jennifer_agreement` | 200 | 201 |

## Output Files

- `connectivity_matrix.csv`
- `final_connectivity_matrix.csv`
- `final_nodes.csv`
- `final_edges.csv`
- `connectivity_graph.json`
- `validation_summary.json`
- `round_01_diego_high_recall_matrix.csv`
- `round_02_jennifer_precision_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_agreement_matrix.csv`
- `token_performance_tracking.csv`
- `token_performance_traking.csv`
