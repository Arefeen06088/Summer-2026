# Document 39 Round04 Jennifer Final Precision Sign-Off

## Scope

- Reviewed only resources under `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\39\Raw + wires + junctions + OCR`.
- Treated `raw -- npp_schematic_improved_no_overlap.png` as authoritative.
- Used overlays, crops, `component_visual_ocr_labels.csv`, `wire_nodes.csv`, and prior in-folder round CSVs/notes only as aids.
- Did not use GT, GT-derived feedback, evaluator feedback, outside folders, or off-the-shelf OCR.

## Final Decision

I agree with Diego round03 unchanged. Jennifer round04 copies the same 54-node / 56-edge graph forward, and saturation is reached.

No visually supported node or edge should be added or removed.

## Final Precision Findings

### CONTROL-ROOM-ANNUNCIATION

- Keep `CONTROL-ROOM-ANNUNCIATION` excluded as a graph node.
- In the raw bottom band, the text is printed alongside the long dashed annunciation route. It is not drawn as a component, terminal block, busbar, junction box, or bus-equivalent connection point.
- Keep the four route-membership edges removed:
  - `JB-A101 -- CONTROL-ROOM-ANNUNCIATION`
  - `ANN-CR01 -- CONTROL-ROOM-ANNUNCIATION`
  - `REC-SOE01 -- CONTROL-ROOM-ANNUNCIATION`
  - `JB-B101 -- CONTROL-ROOM-ANNUNCIATION`
- Do not replace those with direct JB-to-ANN or JB-to-REC edges; no clear terminal-to-terminal conductor from either field JB to ANN/REC is visible.

### ANN / REC

- Keep `ANN-CR01 -- REC-SOE01`.
- The raw bottom band shows a direct dashed conductor between the ANN and REC blocks.

### RPS / JB / MOV Control Routes

- Keep `RPS-A -- JB-A101`.
- Keep `JB-A101 -- MOV-881A`.
- Keep `JB-A101 -- MOV-742A`.
- Keep `RPS-B -- JB-B101`.
- Keep `JB-B101 -- MOV-881B`.
- Keep `JB-B101 -- MOV-742B`.
- These routes remain visually supported by dashed control wiring and the visible terminal schedule, but the long RPS-to-JB routes correctly remain moderate-confidence because explicit junction dots are sparse.

### RPS / Relay Interlocks

- Keep `RPS-A -- RELAY-KA1`.
- Keep `RPS-B -- RELAY-KB1`.
- The dashed conductors terminate at the relay blocks, and the visible terminal schedule supports KA1/KB1 as RPS-to-relay interlocks.

### Ground Reference

- Keep `BUS-480-A -- GND-PLANT`.
- The raw schematic shows a solid vertical conductor from the right end of `BUS-480-A` to the ground/reference symbol.
- Do not add a B-side ground edge; no corresponding `BUS-480-B` ground conductor is drawn.

### Power / Bus / MCC / Side Stack

- The offsite, EDG, tie, 4.16 kV to 480 V, MCC fan-out, charger, and 125 VDC/120 VAC side-stack edges remain visually supported as kept in round03.
- The tie remains mediated through `CB-TIE-AB`; no direct `BUS-4160-A-DIV-I -- BUS-4160-B-DIV-II` edge is supported.
- `LC-A`, `LC-B`, normal-feed labels, division labels, and `N.O. TIE` remain annotations only.

## Final Round04 Graph

- Nodes: 54.
- Included undirected edges: 56.
- Round04 action: copied Diego round03 unchanged.
- Saturation status: reached.
