# Document 37 Connectivity Extraction

Generated: 2026-07-16T17:32:58

Allowed resources used: files under `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\37\Raw + wires + components + junctions` only. No GT or GT-derived feedback was used.

## Consensus

Diego R1 produced a high-recall graph. Jennifer R1 removed unsupported PLC-ESF cable-tray route candidates. Diego R2 re-inspected the top-center source/tie crop and removed GRID-345 -- CB-TIE-6K. Jennifer R2 confirmed the saturated final graph.

Final matrix:
- Nodes: 55
- Edges: 54
- Symmetric undirected matrix with zero diagonal
- Includes solid power conductors, ATS relay dashed control wires, and DC reference taps
- Excludes Pxx/Cxx path labels as nodes
- Excludes GRID-345 -- CB-TIE-6K because the raw crop shows no visible source-to-tie conductor
- Excludes PAN-RPS-A -- PLC-ESF and PLC-ESF -- PAN-RPS-B because C03/C06 look like functional cable-tray/routing paths without clear component-port terminations
- Keeps PLC-ESF as a visible isolated component/logical block

## Final Edge Decisions

- CB-TIE-6K connects BUS-6KA and BUS-6KB only.
- GRID-345 connects through CB-101 and CB-102 to AUX-TR-1A and AUX-TR-1B, but not directly to CB-TIE-6K.
- ATS-1A -- RELAY-K12A and ATS-1B -- RELAY-K12B are retained as visibly terminated dashed control edges.
- GND-01A and GND-01B are retained as DC reference nodes tied to BUS-125DCA and BUS-125DCB.

## Token Accounting Note

No API key was available, so the Responses token-counting endpoint could not be used. Actual model response usage objects were not exposed for the subagent calls. Token files therefore report a local estimate using prompt/context length plus an image/file input heuristic for the crops and source aids reviewed in each round.
