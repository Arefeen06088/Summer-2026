# Document 39 Round03 Diego Saturation Notes

## Scope

- Reviewed only resources in `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\39\Raw + wires + junctions + OCR`.
- Used the raw schematic as authoritative; overlays, masks, crops, wire-node CSV, component CSV, and prior round result CSVs/notes were aids only.
- No GT, GT-derived feedback, evaluator outputs, off-folder files, or off-the-shelf OCR were used.

## Round03 Decision

I agree with Jennifer round02 and copied the 54-node / 56-edge graph forward as Diego round03. No removed edge or node should be restored, and I found no additional visually/geometrically supported missing edge.

## Dispute Review

### CONTROL-ROOM-ANNUNCIATION

- Do not restore `CONTROL-ROOM-ANNUNCIATION` as a graph node.
- In the raw bottom band, the text is a label printed near a long dashed annunciation route. It is not drawn as a terminal block, component, junction, busbar, or bus-equivalent connection point.
- The four route-membership edges removed by Jennifer remain excluded:
  - `JB-A101 -- CONTROL-ROOM-ANNUNCIATION`
  - `ANN-CR01 -- CONTROL-ROOM-ANNUNCIATION`
  - `REC-SOE01 -- CONTROL-ROOM-ANNUNCIATION`
  - `JB-B101 -- CONTROL-ROOM-ANNUNCIATION`
- No replacement direct JB-to-ANN or JB-to-REC edge was added; the raw drawing does not show a clear terminal-to-terminal conductor from either field JB to ANN/REC.

### ANN-CR01 -- REC-SOE01

- Keep `ANN-CR01 -- REC-SOE01`.
- The raw bottom band shows a direct dashed conductor between the right side of `ANN-CR01` and the left side of `REC-SOE01`, with a clear terminal-to-terminal route.

### RPS / JB / MOV Control Routes

- Keep `RPS-A -- JB-A101`, `JB-A101 -- MOV-881A`, and `JB-A101 -- MOV-742A`.
- Keep `RPS-B -- JB-B101`, `JB-B101 -- MOV-881B`, and `JB-B101 -- MOV-742B`.
- The raw drawing shows dashed control conductors from each RPS area toward its train field-JB route, and separate dashed drops from each MOV into the corresponding JB area. These are visually supported but correctly kept at moderate confidence because terminal dots are sparse on the long dashed runs.

### RPS / Relay Interlocks

- Keep `RPS-A -- RELAY-KA1` and `RPS-B -- RELAY-KB1`.
- The raw drawing shows dashed conductors terminating at the relay blocks, and the visible terminal schedule supports KA1/KB1 as RPS-to-relay interlocks.

### Ground Reference

- Keep `BUS-480-A -- GND-PLANT`.
- A solid vertical conductor visibly drops from the right end of the A 480 V bus to the ground/reference symbol labeled `GND-PLANT`.
- Do not add a B-side ground edge. No corresponding conductor is drawn from `BUS-480-B` to `GND-PLANT` or another B-side ground symbol.

## Solid Power / Bus Review

- A offsite chain remains supported: `OFFSITE-230KV-A -- DS-230A -- TR-1A -- CB-1A -- BUS-4160-A-DIV-I`.
- A diesel chain remains supported: `EDG-1A -- CB-DG-A -- BUS-4160-A-DIV-I`.
- Tie path remains mediated only through `CB-TIE-AB`: `BUS-4160-A-DIV-I -- CB-TIE-AB -- BUS-4160-B-DIV-II`; no direct A-bus-to-B-bus edge.
- B offsite and diesel chains remain supported as Jennifer kept them.
- 4.16 kV to 480 V transformer/breaker chains remain supported on both trains.
- `BUS-480-A` and `BUS-480-B` each feed their own MCCs and side charger stack only; no cross-train 480 V edge is visually present.
- MCC-to-load fanouts remain through the MCCs. No direct bus-to-pump/MOV edges were added.
- `LC-A`, `LC-B`, `NORMAL OFFSITE FEED`, division titles, and `N.O. TIE` remain annotations, not graph nodes.

## Final Round03 Graph

- Nodes: 54.
- Included edges: 56.
- This round03 graph intentionally matches Jennifer round02 after saturation review.
