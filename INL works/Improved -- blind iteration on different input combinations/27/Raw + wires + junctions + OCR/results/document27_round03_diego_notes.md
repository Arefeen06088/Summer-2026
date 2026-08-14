# Document 27 Round 03 Diego Notes

## Scope

- High-recall saturation review used only the allowed document-27 folder: raw/label/wire/node crops, round01 Diego outputs, round02 Jennifer outputs, and `codes/build_matrix_from_edges.py`.
- No Ground Truth, GT-derived feedback, evaluator outputs, outside data, or off-the-shelf OCR were used.
- Independently inspected the requested focus crops: `labels__row1_col2.png`, `labels__row2_col2.png`, `labels__row3_col1.png`, `labels__row3_col3.png`, plus corresponding raw/wire/node crops.

## Round03 Decision

- I agree with Jennifer round02 after the visual saturation pass.
- Round03 nodes were copied exactly from `results/document27_round02_jennifer_nodes.csv`.
- Round03 edges were copied exactly from `results/document27_round02_jennifer_edges.csv`.
- No restored or newly added edge had clearer visual evidence than Jennifer's round02 graph.

## Visual Verification

- `BUS-13KV-N` is the printed top bus label in row1/top-band crops, so the round02 rename from `BUS-13.8KV` is retained.
- `TE-41` remains rejected: row1-col2 label/raw/wire/node views show no distinct connected TE symbol or signal line below `CB-TIE-41`; the tie breaker only carries the solid 4160 V bus-tie path.
- `DS-A10 -- JB-A10` is retained and `DS-A10 -- CHGR-125A` remains removed: row2-col2 shows the A10 vertical branch continuing through `DS-A10` to `JB-A10`, while `CHGR-125A` has its own visible bus tap.
- `BUS-480-A -- CHGR-125A` and `BUS-480-B -- CHGR-125B` remain medium confidence because the solid charger taps are visible but unlabelled as separate breaker branches.
- `DC-BUS-125A -- DC-BUS-125B` remains medium confidence: the DC bus band is visually continuous, but A/B logical separation is still schematic-style.
- Only `DC-BUS-125A -- PANEL-CTRL-MAIN` is retained: row2-col2 shows one visible dashed tap from the DC bus band to the control panel, not two separate panel taps.
- `BUS-480-C -- GND-EQ-A` and `BUS-480-D -- GND-EQ-B` remain medium-confidence ground edges; row3-col1 and row3-col3 show dash-dot DC/ground style terminating at labelled ground symbols.

## Counts

- Node CSV rows: 201.
- Included matrix nodes: 200 (`TE-41` is marked `decision=reject`).
- Included edge rows: 201.
- Unique undirected edges: 201.
- Edge kinds: `power_feeder=155`, `bus_tie=3`, `control_interlock=15`, `instrument_signal=26`, `ground=2`.
- Confidence counts: `high=195`, `medium=6`.

## Validation

- Matrix built with `python codes\build_matrix_from_edges.py results\document27_round03_diego_edges.csv results\document27_round03_diego_nodes.csv results\document27_round03_diego_adjacency_matrix.csv results\document27_round03_diego_matrix_summary.json`.
- No unknown endpoints.
- No duplicate undirected pairs.
- Matrix node order matches included nodes from the nodes CSV.
- Matrix is symmetric.
- Matrix diagonal is zero.
- Round03 edge set changed from round02: no.
