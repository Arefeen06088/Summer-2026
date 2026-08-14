# Document 7 Connectivity Extraction

Scope: blind extraction using only `Raw + wires + components + junctions` resources.

Rounds:
- `round_01_diego_high_recall`: Diego high-recall proposal before precision pruning. Edge count: 132.
- `round_02_jennifer_precision`: Jennifer precision review removed four unsupported candidates and added RELAY-K101--SR-101. Edge count: 129.
- `round_03_diego_saturation`: Diego final reconciliation after Jennifer's correction; graph saturated unchanged. Edge count: 129.

Saturation: Diego and Jennifer converged on the Jennifer-refined graph in round 3.

Node count: 120
Final undirected edge count: 129

Important rule applied: no-dot crossings are visual crossings only; raceway/region labels were not treated as components.

Jennifer changes from Diego round 1:
- Removed `BAT-125A -- BCHG-125A` and `BAT-125B -- BCHG-125B` because both sides land on their DC buses without a direct battery-to-charger terminal connection.
- Removed `PNL-AC-CR1 -- RELAY-K101` and `PNL-AC-CR2 -- RELAY-K201` because terminal taps are not visually supported.
- Added `RELAY-K101 -- SR-101` because the lower dashed control path ties RELAY-K101 to the SR-101 circuit.

Uncertain/excluded candidates are recorded in `uncertain_excluded_edges.csv`.
