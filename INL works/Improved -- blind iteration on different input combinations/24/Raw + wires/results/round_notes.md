# Document 24 Round Notes

## Scope
- Used only resources under `Raw + wires`.
- No ground-truth file or GT-derived feedback was used.
- No OCR engine was used. Labels were read by visual inspection.

## Diego Round 1 - High Recall
Diego identified the two-train class 1E AC/DC drawing: offsite sources, EDG/generator paths, `BUS-101A/B`, tie breaker `CB-TIE-1`, transformer feeds to `BUS-201A/B`, 18 feeder channels, and bottom DC/control/signal panels. His high-recall pass used `DG-1A/B` for the generator labels and included route-channel candidates around `SYNC-CAB`, `LOAD-SHED-CAB`, `ESFAS`, `TRIP-MOD`, and alarm signals.

## Jennifer Round 1 - Precision Refinement
Jennifer corrected generator labels to `EDG-1A/B`, confirmed `PMP-LP208A/B`, full relay labels, and accepted visually confirmed solid, dashed, and dotted connections as typed edges. She rejected route-channel candidates without clean terminal evidence and crossings without junction dots.

## Diego Round 2 - Agreement Check
Diego agreed with Jennifer's corrections and recommended that the required binary matrix set `1` for every visually accepted line type, while the edge list preserves `edge_type` metadata.

## Jennifer Round 2 - Saturated Final
Jennifer confirmed the same scope: final binary matrix includes solid power/DC, dashed control/trip, dotted signal, and ground/reference edges. Rejected or uncertain routes remain excluded. Final status: SATURATED FINAL.
