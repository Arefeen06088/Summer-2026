# Document 10 Connectivity Extraction Rounds

Only resources in the `Raw + wires` folder were used. No GT or GT-derived feedback was used.

## Round 1 - Diego

High-recall extraction with 123 nodes and 123 edges. Diego included the two cable tray labels and the MCR/annunciator bay title as plausible route/area nodes.

## Round 2 - Jennifer

Precision refinement with 120 nodes and 116 edges. Jennifer removed `CT-CAB-A CONTROL CABLE TRAY`, `CT-CAB-B CONTROL CABLE TRAY`, and `MCR / ANNUNCIATOR CONTROL BAY` as annotations, not true endpoints.

Removed unsupported edges: `RLY-86A -- FUSE-A01`, `CB-A06 -- PT-4160-A`, `PNL-RPS-A -- PNL-ESFAS-A`, `RLY-86B -- FUSE-B01`, `CB-B06 -- PT-4160-B`, `PNL-RPS-B -- PNL-ESFAS-B`.

## Round 3 - Diego

Diego agreed with Jennifer's refined graph. Final graph has 120 nodes, 116 edges, and no uncertain edges.

Ground nodes `GND-A` and `GND-B` remain visible but isolated, because no named component endpoint tie was visually supported.
