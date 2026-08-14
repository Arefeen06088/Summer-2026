# Case 25 Connectivity Extraction Note

Generated: 2026-07-14T11:19:15

## Scope

- Raw resource: `raw -- synthetic_npp_electrical_schematic_revised_v4.png`
- Extraction used only the raw schematic and crops derived from that raw schematic under `codes/crops`.
- Ground truth or GT-derived feedback was not used.

## Subagent Rounds

1. Diego high-recall pass: proposed all visually plausible components and edges, including four lower route labels as provisional logical nodes.
2. Jennifer precision pass: accepted the main source, 4.16kV, and 480V topology; rejected unsupported overconnections such as `MCC-X1 -- MCC-X2`, `CB-4X01 -- MS-X01`, and `DS-4X01 -- TR-480-1X`.
3. Diego saturation pass: identified `480V CHGR-A FEEDER`, `480V CHGR-B FEEDER`, `PNL A/B TIE`, and `RPS TRIP BUS` as route/lane labels rather than component rows.
4. Jennifer final confirmation: AGREED with the saturation correction.

## Final Decisions

- Final matrix rows are component/node names only.
- Excluded route/lane labels: `480V CHGR-A FEEDER`, `480V CHGR-B FEEDER`, `PNL A/B TIE`, `RPS TRIP BUS`.
- Replacement direct component edges: `BUS-480-1A -- CHGR-125-1A`, `BUS-480-1B -- CHGR-125-1B`, and `PNL-RPS-A -- PNL-RPS-B`.
- No direct `MCC-X1 -- MCC-X2` edge was kept; both MCC sections are independently fed from `BUS-480-1X`.
- No self-loops were used.

## Counts

- Final nodes: 200
- Final undirected component edges: 203
- Matrix is symmetric with zero diagonal.

The title block text mentions 200 components and 208 visible connections. The final component-node matrix has 200 rows and excludes five route/lane or continuation-level visible wires from row promotion, because those labels are not component names. This preserves the agreed component-only matrix while keeping the round files for audit.

## Round Artifact Counts

| Round | Nodes | Edges |
| --- | ---: | ---: |
| `round_01_diego_high_recall` | 204 | 207 |
| `round_02_jennifer_precision` | 204 | 207 |
| `round_03_diego_saturation` | 200 | 203 |
| `round_04_jennifer_agreement` | 200 | 203 |

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
