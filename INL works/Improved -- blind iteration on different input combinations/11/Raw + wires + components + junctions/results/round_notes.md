# Document 11 Round Notes

Only resources from `Raw + wires + components + junctions` were used. No GT or GT-derived feedback was used. No off-the-shelf OCR was used.

## Round Sequence

1. Diego R1 high-recall extraction proposed top feeders, four train graphs, DC/control nodes, and uncertain ATS/DC/ground candidates.
2. Jennifer R1 removed label-only pseudo-nodes, rejected unsupported ATS input and panel-IC-to-bus mappings, and kept ATS outputs to RPS panels.
3. Diego R2 returned `AGREED_FINAL`; final matrix equals Jennifer R1.

## Final Excluded / Ambiguous Cases

- TIE-A12/B12/C12/D12, FDR, LC, BC, 52, 480, NORM, L, ATS-AOUT/BOUT, DC-A125/B125/C125/D125: line/cable/function labels, not standalone components.
- ATS-480-A/B input-side mappings: ATS output to RPS panels is visible, but input source mapping to train feeders is ambiguous.
- PANEL-IC-X to BUS-DC-125A/B: conductors route through bottom crossings; Diego and Jennifer agreed the named-bus mapping is not reliable enough.
- GND-A/B/C/D: visible ground references, excluded from ordinary component connectivity.

## Final Counts

- Final nodes: 116
- Final undirected edges: 130
