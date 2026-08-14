# Document 17 Extraction Notes

Allowed resources only: raw schematic, detected overlay, wire mask/overlay, wire-node overlay, and wire_nodes.csv from the `Raw + wires + components + junctions` folder.

No GT or GT-derived feedback was used. No off-the-shelf OCR was used; labels were read visually from the raw/crop images.

Round outcome:
- Round 1 Diego: high-recall graph, including aggregated master terminal block and two dotted relay-to-recorder candidates.
- Round 1 Jennifer: removed the master-terminal-block node/edge, corrected labels, removed the two relay-to-recorder dotted edges pending support.
- Round 2 Diego: agreed with Jennifer except restored `RELAY-ESF-A--REC-SOE-1` and `RELAY-ESF-B--REC-SOE-2`.
- Round 2 Jennifer: accepted both restored dotted relay-to-recorder edges. Saturated.

Final excluded:
- `MASTER-TB-21-29` and `CB-TR-A2--MASTER-TB-21-29`.
- Long dashed side-channel crossings without black-dot terminations.
