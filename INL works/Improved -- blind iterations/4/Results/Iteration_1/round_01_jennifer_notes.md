# Round 01 Jennifer Notes

## Source Use
- Used the matching 8800x5734 doc 4 raw schematic, matching visual OCR labels, detected overlay, wire masks/nodes, inspection crops, and Diego Round 1 CSV/notes.
- Ignored the mismatched 5500x3362 raw/component-logical files as topology and naming evidence.
- Kept all named components, named buses, and named grounds from Diego's node order; excluded anonymous wire nodes and pure crossing geometry.

## Counts
- Node count: 120
- Edge count: 124

## Changes From Diego

### Removed Edges
- BUS-480-RB2 -> CB-F101
- BUS-480-RB2 -> CB-F103
- BUS-480-RB2 -> CB-F105
- BUS-480-RB2 -> CB-F107
- BUS-480-RB2 -> CB-F109
- BUS-480-RB2 -> CB-F111
- BUS-480-RB2 -> CB-F113
- BUS-480-RB2 -> CB-F115
- BUS-480-LCB -> CB-CHG-A

### Added Edges
- BUS-480-RB1 -> CB-F101
- BUS-480-RB1 -> CB-F103
- BUS-480-RB1 -> CB-F105
- BUS-480-RB1 -> CB-F107
- BUS-480-RB1 -> CB-F109
- BUS-480-RB1 -> CB-F111
- BUS-480-RB1 -> CB-F113
- BUS-480-RB1 -> CB-F115
- BUS-480-LCA -> CB-CHG-A

## Evidence Notes
- Reactor-building feeder taps: the upper Train A normal bus is BUS-480-RB1 and the lower Train B alternate bus is BUS-480-RB2. The actual tap dots support odd feeders F101/F103/F105/F107/F109/F111/F113/F115 on BUS-480-RB1 and even feeders F102/F104/F106/F108/F110/F112/F114 on BUS-480-RB2. Crossings without the feeder dot were not used as bus taps.
- Charger feeds: CB-CHG-A is fed from the LC-A side of CB-LC-TIE at the LC-TIE1 side and then rises to the charger breaker. CB-CHG-B remains fed from the LC-B side near LC-TIE2.
- Source B chain: CB-SAT-B -> TR-SAT-2 remains; the conductor crosses the LC-A riser with no visible junction dot or tap.
- TB-ESF-A/B: neither terminal block was inserted into the solid LC-B power chain. Their retained edges are dashed control/signal endpoints only.
- Dashed control/signal area: retained only named endpoint pairs that visibly terminate at ANN-CP-A, REC-SER-01, RPS/ESFAS panels, RELAY-K701/K702, and TB-ESF-A/B. No unnamed signal-bus node was added.

## Output Consistency
- `round_01_jennifer_matrix.csv` keeps the same row/column order as Diego's matrix.
- Matrix is symmetric with a zero diagonal.
- `round_01_jennifer_edges.csv` and the matrix contain the same 124 undirected edges.
