# Document 25 Extraction Notes

Scope: visual extraction from `Raw + wires + components + junctions` only. No GT or GT-derived feedback was used. No off-the-shelf OCR was used; labels and edges were read from the raw schematic and local visual crops/overlays.

Agent rounds:
- Round 01 Diego high-recall: broad graph including plausible branch-01 direct breaker-to-MS edges and lower RPS route interpretations.
- Round 02 Jennifer precision: accepted source/train structure, moved branch-01 MS feeds downstream of DS-4X01, removed MCC-to-MCC and pass-by dashed/dotted overconnections, added visible charger feeder edges from MCC-A2/B2.
- Round 03 Diego saturation: accepted Jennifer final unchanged.
- Round 04 Jennifer final: confirmed final accepted unchanged.

Important conventions applied:
- Crossings without dots are not junctions.
- Bus dots/taps are true terminals.
- Solid lines are power/DC power; dashed lines are control/interlock/trip; dotted lines are instrument signal.
- Ground references such as GND-ESF-X05 are kept as tagged nodes where visibly labelled.
- The title-block CSV filename was ignored as non-visual/GT-adjacent reference text.

Remaining uncertainties not included:
- Pin-level detail inside TC-52-4A.
- Dashed-lane junctions near TC-52-4A without visible terminals/dots.
- Any direct connection from 480V CHGR-B FEEDER to INV-120-1A, PNL-RPS-A, or RELAY-K501A.
- Any direct MCC-X1 to MCC-X2 tie.
- Any off-sheet continuation beyond the visible RPS TRIP BUS arrow.

Final stats:
- round_01_diego_high_recall: 204 nodes, 205 edges, symmetric=True, diagonal_zero=True
- round_02_jennifer_precision: 204 nodes, 207 edges, symmetric=True, diagonal_zero=True
- round_03_diego_saturation: 204 nodes, 207 edges, symmetric=True, diagonal_zero=True
- round_04_jennifer_final: 204 nodes, 207 edges, symmetric=True, diagonal_zero=True
