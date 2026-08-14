# Document 8 Connectivity Extraction

Scope: blind extraction using only `Raw + wires + components + junctions` resources.

Rounds:
- `round_01_diego_high_recall`: Diego high-recall proposal before precision pruning. Edge count: 144.
- `round_02_jennifer_precision`: Jennifer precision patch applied to Diego graph. Edge count: 140.
- `round_03_diego_saturation`: Diego final reconciliation; Jennifer-patched graph saturated unchanged. Edge count: 140.

Saturation: Jennifer corrected Diego's high-recall graph; Diego agreed with the patch in round 3.

Node count: 120
Final undirected edge count: 140

Important rule applied: crossings without filled dots are not electrically connected, and cable/table/title text was excluded as graph nodes.

Precision changes:
- Removed `BUS-4160-N2A -- TR-480-N2A`.
- Removed `BUS-4160-N2B -- TR-480-N2B`.
- Removed `BUS-480-N2A -- BUS-480-E2A`.
- Removed `BUS-480-N2B -- BUS-480-E2B`.
- Removed `BUS-125DC-A -- MCC-2C`.
- Removed `FAN-VENT-2A -- CP-ESFAS-A`.
- Removed `JB-2A1 -- CP-ESFAS-A`.
- Removed `PN-125B -- VLV-HV-302B`.
- Removed `CB-54B -- RELAY-K1B`.
- Added `BUS-4160-S2A -- TR-480-N2A`.
- Added `BUS-4160-S2B -- TR-480-N2B`.
- Added `CB-N1 -- MCC-2C`.
- Added `PN-125A -- BUS-120AC-A`.
- Added `PN-125B -- BUS-120AC-B`.

Uncertain/excluded candidates are recorded in `uncertain_excluded_edges.csv`.
