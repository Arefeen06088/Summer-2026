# Current Round 01 - Diego Notes

## Node Policy
- Used exactly the updated current inventory at `Codes and artifacts/component_inventory_doc15_current.csv`.
- Inventory count validated at 183 nodes: 163 OCR physical components plus 20 current visual additions (4 tie-control components and 16 logical bus nodes).
- Did not add WN-* wire nodes, anonymous junctions, title/legend/schedule text, or the removed `OFFSITE SOURCES` label.
- Matrix rows and columns follow the inventory order exactly; connectivity is undirected with zero diagonal.

## Major Buses
- Switchyard: `BUS-SWY-1`, `BUS-SWY-2`, joined only through `CB-SWY-TIE`.
- Normal station service: `BUS-NSS-1` feeds divisions A/B normal-feed breakers; `BUS-NSS-2` feeds divisions C/D normal-feed breakers.
- Safety 4.16 kV: `BUS-416A`, `BUS-416B`, `BUS-416C`, `BUS-416D`; A-B and C-D ties are represented as breaker/disconnect series chains.
- 480 V load centers: `BUS-480A` through `BUS-480D`, each feeding one MCC.
- DC buses: `BUS-DC-A` through `BUS-DC-D`, each tied to charger/inverter/ground/control-panel chains.

## Evidence By Topology Area
- Top switchyard: generators connect through generator breakers to GSU transformers, then to their switchyard buses. `TR-UAT-*` and `TR-SAT-*` visibly tap the switchyard buses and land on the corresponding NSS bus.
- Division A: `BUS-NSS-1 -> CB-NF-A -> BUS-416A`; `DG-1A -> CB-DG-A -> BUS-416A`; `BUS-416A -> CB-TX-A -> TR-480A -> BUS-480A -> MCC-1A`; six MCC feeders land on A loads.
- Division B: `BUS-NSS-1 -> CB-NF-B -> BUS-416B`; `DG-1B -> CB-DG-B -> BUS-416B`; `BUS-416B -> CB-TX-B -> TR-480B -> BUS-480B -> MCC-1B`; six MCC feeders land on B loads.
- Division C: `BUS-NSS-2 -> CB-NF-C -> BUS-416C`; `DG-1C -> CB-DG-C -> BUS-416C`; `BUS-416C -> CB-TX-C -> TR-480C -> BUS-480C -> MCC-1C`; six MCC feeders land on C loads.
- Division D: `BUS-NSS-2 -> CB-NF-D -> BUS-416D`; `DG-1D -> CB-DG-D -> BUS-416D`; `BUS-416D -> CB-TX-D -> TR-480D -> BUS-480D -> MCC-1D`; six MCC feeders land on D loads.
- Tie sections: A-B is `BUS-416A -> CB-TIE-AB -> DS-TIE-AB -> BUS-416B`; C-D is `BUS-416C -> CB-TIE-CD -> DS-TIE-CD -> BUS-416D`.
- MCC feeders: each MCC-to-breaker, breaker-to-disconnect/fuse, and disconnect/fuse-to-load conductor is represented as a solid power edge. Each breaker-to-relay dashed lead is represented as a control edge.
- DC/control blocks: each battery/charger/DC bus/inverter/control-panel/terminal/junction/ground chain was connected only where a dashed or solid line visibly lands on named endpoints.

## Uncertain High-Recall Candidates
- `BUS-NSS-1 -- DG-1A` and `BUS-NSS-2 -- DG-1C` are low-confidence because the NSS line appears to enter/exit those DG symbols in the raw/wire-node crop, but this may be a symbol-overlap artifact.
- `SEQ-1AB`/`RPS-AC-1` and `SEQ-2CD`/`RPS-AC-2` control edges are lower-confidence because the dashed side risers share unnamed junctions; no WN nodes were added, so nearest named endpoints were used.
- `RLY-A06/B06/C06/D06 -- TB-1A/B/C/D` are lower-confidence long dashed control leads; they are visible as continuations from the sixth MCC relay area down to the terminal block area, but the middle span is mostly open sheet.

## Likely Overconnection Risks For Jennifer
- The DG-to-NSS low-confidence edges may be false positives caused by the bus line visually passing behind or through the DG symbol.
- Dashed tie-control networks could be overconnected if the vertical risers are only routing guides rather than conductor continuity.
- Breaker-to-relay dashed edges are intentionally high-recall; if the target schema treats relays as annotations rather than electrical/control nodes, Jennifer may prune many of them.
- DC dashed lines are included as connectivity because named endpoints visibly land on the dashed conductors; if dashed means only reference/control association, those may need precision review.

## Output Summary
- Edge proposals written: 198
- Matrix size: 183 x 183 plus leading `node_name` column.
