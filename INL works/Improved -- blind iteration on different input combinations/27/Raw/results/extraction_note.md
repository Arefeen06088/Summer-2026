# Case 27 Connectivity Extraction Note

Generated: 2026-07-14T12:14:45

## Scope

- Raw resource: `raw -- synthetic_npp_electrical_schematic_readable.png`
- Extraction used only the raw schematic and crops derived from that raw schematic under `codes/crops`.
- Sibling derived-resource folders and any ground-truth material were not opened or used.

## Subagent Rounds

1. Diego high-recall pass: proposed the full component set, kept visually plausible DC/battery/charger extras, and misread `GND-EO-A/B` as `GND-EQ-A/B`.
2. Jennifer precision pass: corrected the ground labels to `GND-EO-A/B`, removed unsupported direct charger-to-battery and `DS-B01 -- BAT-125B` edges, and accepted the A10 battery chain plus the continuous 125 VDC bus.
3. Diego saturation pass: AGREED with Jennifer's precision graph.
4. Jennifer final confirmation: AGREED.

## Final Decisions

- Final rows are component/node labels only.
- Wire route captions, titles, notes, grid markings, legend labels, and unlabeled tick marks are excluded as rows.
- Direct drawn adjacencies are encoded, not transitive closure across an entire bus.
- `BAT-125A` is modeled in the A10 branch: `DS-A10 -- BAT-125A -- JB-A10`.
- `BAT-125B` is modeled as a separate battery tied to `DC-BUS-125B`, not part of the B01 pump branch.
- `DC-BUS-125A` and `DC-BUS-125B` are retained as separate labels with a direct edge because they are drawn on a continuous horizontal bus.

## Counts

- Final nodes: 200
- Final undirected component edges: 203
- Matrix is symmetric with zero diagonal: True

## Round Artifact Counts

| Round | Nodes | Edges |
| --- | ---: | ---: |
| `round_01_diego_high_recall` | 200 | 204 |
| `round_02_jennifer_precision` | 200 | 203 |
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
