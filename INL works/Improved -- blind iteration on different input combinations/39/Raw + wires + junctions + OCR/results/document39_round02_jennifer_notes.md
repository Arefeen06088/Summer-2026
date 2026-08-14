# Document 39 Round02 Jennifer Precision Notes

## Scope

- Reviewed only files inside `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\39\Raw + wires + junctions + OCR`.
- Treated `raw -- npp_schematic_improved_no_overlap.png` as authoritative. The wire overlays, component label CSV, wire-node CSV, and precision crops were used only as aids.
- No GT, GT-derived feedback, evaluator outputs, off-folder extraction sources, or off-the-shelf OCR were used.

## Round02 Decision Summary

- Removed `CONTROL-ROOM-ANNUNCIATION` from the node set. The raw bottom band shows this as text placed on/near a long dashed annunciation route, not as a physical component, terminal block, or busbar-equivalent graph node.
- Removed the four route-membership edges that used that annotation as a hub: `JB-A101 -- CONTROL-ROOM-ANNUNCIATION`, `ANN-CR01 -- CONTROL-ROOM-ANNUNCIATION`, `REC-SOE01 -- CONTROL-ROOM-ANNUNCIATION`, and `JB-B101 -- CONTROL-ROOM-ANNUNCIATION`.
- Kept `ANN-CR01 -- REC-SOE01` because the raw bottom band shows a direct dashed conductor between the annunciator and recorder blocks.
- Final node count is 54. Final included edge count is 56.

## Node Review

- Kept the physical/electrical component nodes and four bus logical nodes: `BUS-4160-A-DIV-I`, `BUS-4160-B-DIV-II`, `BUS-480-A`, and `BUS-480-B`.
- Confirmed annotation-only exclusions: division/train titles, `NORMAL OFFSITE FEED` labels, `LC-A`, `LC-B`, and `N.O. TIE`. These describe areas, routes, load-center labels, or breaker state and are not separate graph nodes.
- Kept `GND-PLANT` as a component/reference node because a solid vertical conductor drops from the right end of `BUS-480-A` into the ground/reference symbol. This is recorded as a ground/reference connection, not a load feeder.

## Power Topology Checks

- Confirmed A offsite path: `OFFSITE-230KV-A -- DS-230A -- TR-1A -- CB-1A -- BUS-4160-A-DIV-I`.
- Confirmed A diesel path: `EDG-1A -- CB-DG-A -- BUS-4160-A-DIV-I`.
- Confirmed tie is mediated only through `CB-TIE-AB`: `BUS-4160-A-DIV-I -- CB-TIE-AB -- BUS-4160-B-DIV-II`; no direct bus-to-bus edge was added.
- Confirmed B-side mirror: `OFFSITE-230KV-B -- DS-230B -- TR-1B -- CB-1B -- BUS-4160-B-DIV-II`, plus `EDG-1B -- CB-DG-B -- BUS-4160-B-DIV-II`.
- Confirmed 4.16 kV to 480 V paths: `BUS-4160-A-DIV-I -- TR-480-A -- CB-480-A -- BUS-480-A` and `BUS-4160-B-DIV-II -- TR-480-B -- CB-480-B -- BUS-480-B`.
- Kept UV sensing edges because dashed vertical routes visibly drop from the 4.16 kV buses to `RELAY-UV-A` and `RELAY-UV-B`.

## 480 V, Loads, and Side Stacks

- Confirmed `BUS-480-A` feeds only `MCC-A1`, `MCC-A2`, `CHG-125A`, `CB-480-A`, and `GND-PLANT` in the final graph; load fan-outs stay through MCCs.
- Confirmed `BUS-480-B` feeds only `MCC-B1`, `MCC-B2`, `CHG-125B`, and `CB-480-B` in the final graph; load fan-outs stay through MCCs.
- Kept `BUS-480-A -- CHG-125A` and `BUS-480-B -- CHG-125B` because the solid routes visibly leave the 480 V bus ends and land at the charger stacks. `LC-A` and `LC-B` remain route labels only.
- Kept side-stack edges `CHG-125A -- BAT-125A -- INV-120A -- PANEL-120A -- RPS-A` and the B-side mirror. The stack edges are visually supported by vertical conductors, but the battery-to-inverter edges remain moderate confidence because they use dashed/DC-style routing inside the stack rather than a busbar-style terminal.

## Control, JB, and Annunciation Routes

- Kept `RPS-A -- RELAY-KA1` and `RPS-B -- RELAY-KB1`; both dashed conductors terminate at the relay blocks and are supported by the visible terminal schedule rows KA1/KB1.
- Kept `RPS-A -- JB-A101` and `RPS-B -- JB-B101` at moderate confidence. The dashed routes and terminal schedule support RPS-to-field-JB/MOV routing, but explicit junction dots are sparse, so this remains noted rather than overstated.
- Kept `JB-A101 -- MOV-881A`, `JB-A101 -- MOV-742A`, `JB-B101 -- MOV-881B`, and `JB-B101 -- MOV-742B`; dashed conductors visibly drop from the MOVs to the corresponding field JB areas.
- Removed all edges through `CONTROL-ROOM-ANNUNCIATION`; the raw drawing supports it as a route annotation, not as a graph hub. No replacement direct JB-to-ANN or JB-to-REC edge was added because no clear terminal-to-terminal conductor is visible.

## Deliberately Not Added

- No direct `BUS-4160-A-DIV-I -- BUS-4160-B-DIV-II` edge.
- No `GND-PLANT -- BUS-480-B` edge.
- No direct relay-to-MCC or relay-to-pump/load edges for KA1/KB1.
- No direct `JB-A101 -- ANN-CR01`, `JB-A101 -- REC-SOE01`, `JB-B101 -- ANN-CR01`, or `JB-B101 -- REC-SOE01` edge.
