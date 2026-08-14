# Case 36 Connectivity Extraction Note

Generated: 2026-07-14T12:52:45

## Scope

- Raw resource: `raw -- synthetic_npp_electrical_schematic_v2.png`
- Extraction used only the raw schematic and crops derived from that raw schematic under `codes/crops`.
- Sibling derived-resource folders and any ground-truth material were not opened or used.

## Subagent Rounds

1. Diego high-recall pass: proposed the labeled equipment set plus route-node abstractions for dashed/control circuits and uncertain extras.
2. Jennifer precision pass: removed invented `CONTROL-*` route nodes, kept only labeled equipment/bus nodes, and converted visually supported control routes to direct edges between labeled endpoints.
3. Diego saturation pass: AGREED with Jennifer's precision graph.
4. Jennifer final confirmation: AGREED.

## Final Decisions

- Final rows are labeled equipment and logical buses only.
- Route labels, aliases, titles, legends, notes, enclosure text, bus tick marks, `TIE OPEN`, `EXC`, `RPS TRIP`, `RPS LOCKOUT`, `SU-A/B`, `EDG-A/B`, and `LC-*` tap aliases are excluded as nodes.
- Direct drawn adjacencies are encoded, not transitive closure across an entire bus.
- Control/dashed connections are retained only where the line visibly lands on labeled component endpoints.
- The RPS-to-ESF trunk candidate, fan dashed-control candidates, inverter/DC-bus dashed candidates, and direct `RECT/BAT/INV` edges not mediated by `BUS-DC125-*` are excluded.

## Counts

- Final nodes: 55
- Final undirected component edges: 60
- Matrix is symmetric with zero diagonal: True

## Round Artifact Counts

| Round | Nodes | Edges |
| --- | ---: | ---: |
| `round_01_diego_high_recall` | 60 | 74 |
| `round_02_jennifer_precision` | 55 | 60 |
| `round_03_diego_saturation` | 55 | 60 |
| `round_04_jennifer_agreement` | 55 | 60 |

## Token Accounting

- Actual model usage objects were not exposed by the Codex/subagent tool responses.
- `OPENAI_API_KEY` is unset, so the Responses input-token counting endpoint was not called.
- Low/expected/high estimates and endpoint-ready manifest are saved in:
  - `token_usage_estimates_by_call.csv`
  - `token_usage_summary_by_document.csv`
  - `responses_input_token_count_manifest.json`

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
