# Document 36 Connectivity Extraction

Generated: 2026-07-16T16:59:02

Allowed resources used: files under `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\36\Raw + wires + components + junctions` only. No GT or GT-derived feedback was used.

## Consensus

Diego R1 produced a high-recall graph. Jennifer R1 removed annotation-only RPS labels as nodes and refined control/interlock connectivity. Diego R2 agreed the correction was saturated. Jennifer R2 gave final confirmation.

Final matrix:
- Nodes: 63
- Edges: 68
- Symmetric undirected matrix with zero diagonal
- Includes solid power conductors and visibly terminated dashed control/interlock wires
- Excludes dashed enclosure boundaries, un-dotted crossings, EXC annotations, RPS-TRIP/RPS-LOCKOUT as nodes, and FAN-CONTAIN-A/B ESF control edges

## Final Control/Interlock Edges Included

- CB-13-TIE -- PNL-RPS-1
- CB-4K-TIE -- PNL-RPS-1
- JB-ESF-A -- PNL-ESF-A
- JB-ESF-B -- PNL-ESF-B
- PNL-ESF-A -- PUMP-AFW-A
- PNL-ESF-A -- VALVE-MOV-A
- PNL-ESF-B -- PUMP-AFW-B
- PNL-ESF-B -- VALVE-MOV-B

## Token Accounting Note

No API key was available, so the Responses token-counting endpoint could not be used. Actual model response usage objects were not exposed for subagent calls. Token files therefore report a local estimate using approximate text-token counts plus an image-tile heuristic for the crops supplied to each model call.
