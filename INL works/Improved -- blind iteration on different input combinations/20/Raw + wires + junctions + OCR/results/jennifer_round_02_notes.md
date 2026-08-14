# Jennifer Round 02 Precision Notes

Scope: inspected only the allowed document 20 resource folder and `precision_review_crops`. Used the raw schematic as authority; overlays/CSVs were aids only. No ground truth, evaluator feedback, previous-document outputs, or off-the-shelf OCR were used.

## Counts

- Diego input edges: 205
- Jennifer final-for-round edges: 202
- Removed Diego edges: 4
- Added/replacement edges: 1
- Net change: -3 edges

## Precision Decisions

- Removed `INV-UPS-A -- UPS-A AC OUTPUT` and `INV-UPS-B -- UPS-B AC OUTPUT`. The raw inverter crops show only short AC-side stubs with no labeled receiving component or clear logical destination.
- Replaced the two `A/B ESF INTERLOCK` logical-node edges with direct `RELAY-K106 -- RELAY-K108`. The raw lower-center crop shows a continuous dashed loop between the two relay branches; `A/B ESF INTERLOCK` is retained as a conductor label, not as a node.
- Kept `BUS-480-A -- RECT-125A` and `BUS-480-C -- RECT-125B` as medium-confidence power edges. Each has a visible solid AC-side tap from the 480 VAC load-center bus into the rectifier, with no separate labeled breaker visible.
- Kept `CS-4A -- HTR-PZR-01A`, `CS-6A -- MOT-CRN-01A`, and `CS-4B -- HTR-SUMP-02B` as medium-confidence control edges. The dashed branches terminate at the labeled load symbols.
- Kept `RELAY-K101 -- LT-512A` and `RELAY-K103 -- LT-512B` as medium-confidence instrument-signal edges. The side branches are visible, though less visually distinct than the pressure transmitter branches.
- Rechecked visible bus labels and preserved `BUS-13K-A/B`, `BUS-416-A/B`, `BUS-480-A/B/C/D`, and `BUS-125DCA/B`. Tie breakers, breakers, disconnects, transformers, MCC/JB devices, relays, and control switches remain as intermediate nodes where visible.

No additional obvious supported component edge was added beyond the ESF interlock replacement.
