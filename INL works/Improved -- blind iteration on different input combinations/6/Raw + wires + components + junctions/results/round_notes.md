# Document 6 Connectivity Extraction

Scope: blind extraction using only `Raw + wires + components + junctions` resources.

Rounds:
- `round_01_diego_high_recall`: Diego high-recall extraction; Jennifer later kept all supported edges.
- `round_02_jennifer_precision`: Jennifer precision review; no supported edges removed or added.
- `round_03_diego_saturation`: Diego final reconciliation; saturation confirmed with no graph changes.

Saturation: Jennifer kept Diego's supported graph unchanged, and Diego confirmed `SATURATED: yes` in the final reconciliation pass.

Node count: 105
Undirected edge count: 115

Important rule applied: no-dot crossings are visual crossings only; all included dashed/dot-dash/dotted links have visible terminal support.

Uncertain/excluded edges are recorded in `uncertain_excluded_edges.csv`.
