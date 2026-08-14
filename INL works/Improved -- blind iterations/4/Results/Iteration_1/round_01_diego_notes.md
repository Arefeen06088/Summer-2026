# Round 01 Diego Notes

## Source Restrictions
- Used only the doc 4 matching 8800x5734 raw schematic, matching OCR/overlay/wire resources, inspection crops, and component_inventory_doc4.csv.
- Ignored the mismatched 5500x3362 raw/62-label resource set as naming/topology evidence.
- Excluded anonymous wire-node IDs, unlabeled junction dots, elbows, pure crossings, title/revision/legend text, and cable-number annotations.

## Extraction Policy Applied
- Preserved all 120 inventory nodes: 110 physical components plus 10 named logical buses/grounds.
- Represented named buses as hub nodes rather than clique-expanding feeders on the same bus.
- Used visually chained load feeders: bus -> circuit breaker -> overload -> terminal load.
- Included solid power wiring and dashed control/signal wiring only where it terminates at named components.

## Counts
- Node count: 120
- Edge count: 124

## Uncertain Candidates For Jennifer Review
- The dashed SIG-X2 vertical between ANN-CP-A and REC-SER-01 crosses/taps the BUS-UPS-B line. I represented ANN-CP-A--REC-SER-01, but did not add BUS-UPS-B--ANN-CP-A or BUS-UPS-B--REC-SER-01 because the crossing/tap semantics are ambiguous.
- The central dashed control trunk is represented as TB-ESF-A--TB-ESF-B plus terminal-panel edges ANN-CP-A--TB-ESF-A and REC-SER-01--TB-ESF-B. If the intended abstraction is a clique for that unnamed signal net, additional ANN/TB/REC pairings may be expected.
- CB-SAT-B/TR-SAT-2 crosses the LC-A riser without a visible junction dot; I treated it as a pure crossing and kept the source B chain separate from the LC-A riser.
- TB-ESF-A and TB-ESF-B sit beside the solid LC-B feeder path; I kept them on dashed control wiring only and did not insert them into the 480 VAC power chain.
- Both charger breakers CB-CHG-A and CB-CHG-B are represented as fed from BUS-480-LCB via the visible left AC supply riser tied to the LC-B side of the lower 480 VAC bus/tie area.
