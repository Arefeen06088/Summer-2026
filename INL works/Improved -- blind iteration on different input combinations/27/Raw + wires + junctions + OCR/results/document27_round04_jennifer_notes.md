# Document 27 Round 04 Jennifer Final Sign-Off Notes

## Scope

- Final precision saturation review used only the allowed document-27 folder: round02 Jennifer outputs, round03 Diego outputs, local raw/label/wire/node crops, CSV aids, and `codes/build_matrix_from_edges.py`.
- No Ground Truth, GT-derived feedback, evaluator outputs, outside data, or off-the-shelf OCR were used.

## Round04 Decision

- Round03 nodes, edges, and adjacency matrix match round02 exactly.
- No visually necessary correction was found in the final medium-edge review.
- Round04 nodes were copied exactly from `results/document27_round03_diego_nodes.csv`.
- Round04 edges were copied exactly from `results/document27_round03_diego_edges.csv`.
- Edge set changed from round03: no.
- Final status: saturated under the blind-review constraints.

## Final Medium-Edge Review

- `BUS-480-A -- CHGR-125A`: kept medium; the A charger has a visible solid tap from the A bus area, but the tap is unlabelled as a separate breaker branch.
- `BUS-480-B -- CHGR-125B`: kept medium; the B charger has the same visible solid tap pattern, also unlabelled as a separate breaker branch.
- `DC-BUS-125A -- DC-BUS-125B`: kept medium; the horizontal DC bus band is visually continuous with filled taps, while A/B logical separation remains schematic-style.
- `DC-BUS-125A -- PANEL-CTRL-MAIN`: kept medium; one visible dashed/status tap descends from the DC bus band to the central CTRL panel. No separate `DC-BUS-125B -- PANEL-CTRL-MAIN` edge was restored.
- `BUS-480-C -- GND-EQ-A`: kept medium; dash-dot DC/ground style continues to the labelled left ground symbol.
- `BUS-480-D -- GND-EQ-B`: kept medium; dash-dot DC/ground style continues to the labelled right ground symbol.

## Special Representation Checks

- `BUS-13KV-N` is correctly represented as the printed top source-bus label; `BUS-13.8KV` is not present in the final included graph.
- `PANEL-CTRL-MAIN` is correctly retained as a visible physical panel node.
- `GND-EQ-B` is correctly retained as a visible physical ground node.
- `TE-41` remains present only as a rejected node row and has no included final edge; no distinct connected TE symbol or signal line is visually supported below `CB-TIE-41`.
- No crossing-without-dot was identified as connected in the final graph.
- No supported source, bus, transformer, DG, charger/battery, DC bus, or regular load-center branch was found missing in the final saturation pass.

## Counts

- Node CSV rows: 201.
- Included matrix nodes: 200 (`TE-41` is marked `decision=reject`).
- Included edge rows: 201.
- Unique undirected edges: 201.
- Edge kinds: `power_feeder=155`, `bus_tie=3`, `control_interlock=15`, `instrument_signal=26`, `ground=2`.
- Confidence counts: `high=195`, `medium=6`.

## Validation

- Matrix built with `python codes\build_matrix_from_edges.py results\document27_round04_jennifer_edges.csv results\document27_round04_jennifer_nodes.csv results\document27_round04_jennifer_adjacency_matrix.csv results\document27_round04_jennifer_matrix_summary.json`.
- No unknown endpoints.
- No duplicate undirected pairs.
- Matrix node order matches included nodes from the nodes CSV.
- Matrix is symmetric.
- Matrix diagonal is zero.
- Round04 nodes, edges, and rebuilt adjacency matrix hash-match round03.
