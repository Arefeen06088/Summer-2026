# Document 9 Connectivity Extraction

Scope: blind extraction using only `Raw + wires + components + junctions` resources.

Rounds:
- `round_01_diego_high_recall`: Diego high-recall proposal before precision pruning. Edge count: 193.
- `round_02_jennifer_precision`: Jennifer precision patch applied to Diego graph. Edge count: 191.
- `round_03_diego_saturation`: Diego final reconciliation; Jennifer-patched graph saturated unchanged. Edge count: 191.

Saturation: Jennifer corrected Diego's high-recall graph; Diego agreed with the patch in round 3.

Node count: 180
Final undirected edge count: 191

Important rule applied: crossings without filled dots are not electrically connected, and note/legend/title/region/overlay text was excluded as graph nodes.

Precision changes:
- Removed `PN-LTG-1B -- JB-NORM-A`.
- Removed `FAN-CR-B -- PN-MOV-B`.
- Removed `INV-120B -- PLC-ESF-B`.
- Added `MCC-SAF-B2 -- PN-MOV-B`.

Uncertain/excluded candidates are recorded in `uncertain_excluded_edges.csv`.
