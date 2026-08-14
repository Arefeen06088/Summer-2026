# Document 16 Extraction Notes

Allowed resources only: raw schematic, detected overlay, wire mask/overlay, wire-node overlay, and wire_nodes.csv from the `Raw + wires + components + junctions` folder.

No GT or GT-derived feedback was used. No off-the-shelf OCR was used; labels were read visually from raw/crop images.

Round outcome:
- Round 1 Diego: high-recall graph with three extra lower tail edges and `RELAY-KHV101A/B` labels.
- Round 1 Jennifer: removed `REC-SOE-1--BUS-125DC-A`, `ANN-501--BUS-125DC-A`, and `METER-VM-1--BUS-120-RPS-A`; corrected `RELAY-KYHV101A/B`; confirmed 480 rail interpretation.
- Round 2 Diego: agreed/saturated with Jennifer.

Final excluded:
- `REC-SOE-1--BUS-125DC-A`
- `ANN-501--BUS-125DC-A`
- `METER-VM-1--BUS-120-RPS-A`
- `CB-31A-FDR30-B--BUS-480-B`
