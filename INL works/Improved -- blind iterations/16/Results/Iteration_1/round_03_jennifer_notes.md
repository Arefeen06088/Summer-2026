# Round 03 Jennifer Notes - Doc 16 / Iteration 1

## Source Boundary
- Used only doc 16 input resources, generated crops/artifacts, and saved round outputs.
- Excluded outside answer artifacts and kept anonymous `WN-*` nodes, title/drawing text, legend/note text, line ticks, cable labels, enclosure borders, and pure crossings out of the matrix.

## Decision
- Accepted Diego Round 3 topology: the RPS A/B control-panel-to-undervoltage paths should be split through the visible local boxes instead of collapsed as direct `CP-RPS-* -- PROT-UV-*` edges.
- Accepted `JB-R` -> `JB-RPS-B3-1B`: the B-side raw and magnified crops clearly show `JB-RPS-B3-1B`.
- Adjusted the new A-side node spelling from Diego's `JB-RPS-A3-1A` to `DB-RPS-A3-1A`: the A-side raw and magnified crops show `DB-RPS-A3-1A`.

## Jennifer Round 3 Changes From Diego Round 3
- Renamed node `JB-RPS-A3-1A` to `DB-RPS-A3-1A` in the matrix row/column labels.
- Updated the two affected edge endpoints and their evidence text to use `DB-RPS-A3-1A`.
- Made no numeric connectivity changes from Diego Round 3.

## Accepted Split Edges
- `CP-RPS-A -- DB-RPS-A3-1A`: visible vertical conductor from `CP-RPS-A` bottom terminal to the local A-side box.
- `DB-RPS-A3-1A -- PROT-UV-A`: visible vertical conductor from the local A-side box bottom terminal to `PROT-UV-A`.
- `CP-RPS-B -- JB-RPS-B3-1B`: visible vertical conductor from `CP-RPS-B` bottom terminal to the local B-side box.
- `JB-RPS-B3-1B -- PROT-UV-B`: visible vertical conductor from the local B-side box bottom terminal to `PROT-UV-B`.

## File Checks
- Node count: 178
- Edge count: 175
- Matrix mirror check: True
- Matrix diagonal zero: True
- Edge/matrix count agreement: True
- Changed Diego Round 3: Yes, label spelling only; topology unchanged.
