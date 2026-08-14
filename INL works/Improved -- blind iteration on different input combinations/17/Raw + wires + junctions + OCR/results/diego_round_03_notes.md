# Diego Round 03 Saturation Notes

Scope: only the document 17 `Raw + wires + junctions + OCR` folder was used. I reviewed Jennifer round 02 kept/removed edges against the raw drawing, wire/component overlays, and prepared review crops. I did not use Ground Truth, evaluator feedback, files outside the allowed folder, or off-the-shelf OCR.

## Agreement With Jennifer

I agree with Jennifer's precision pass on the major removals. The removed MASTER-TERMINAL-BLOCKS edges do not visibly land on the master terminal block or tie breakers. The broad DCS/PNL-ANN/ANN-ESF/REC-SOE overconnections are enclosure/corridor-adjacent rather than clear point-to-point landed leads. The long lower MCC/control continuations from TBs, LSs, and JB-RAD nodes cross dense dashed corridors and are not continuously traceable to landed endpoints, so I did not restore them.

I also agree with Jennifer's raw-label normalizations: BUS-4160-A/B and BUS-120AC-A/B are the labels visible in the raw drawing, and no separate MCC alias conductor should be retained.

## Round 03 Additions

Two corrected control-signal edges are visually supported and were missing after round 02:

- `PNL-ESF-A -> RELAY-RPS-A`: `raw_left_control.png` shows a continuous dashed lead from the lower-left route of `PNL-ESF-A` landing on the top dot of `RELAY-RPS-A`.
- `PNL-ESF-B -> RELAY-RPS-B`: `raw_right_control.png` shows the symmetric continuous dashed lead from `PNL-ESF-B` landing on the top dot of `RELAY-RPS-B`.

These are not restorations of the dropped `PNL-RPS-A/B -> RELAY-RPS-A/B` edges. Jennifer was right that the visible landed source is the ESF panel routing, so round 03 adds corrected substitute edges instead.

## Saturation Decision

After the two corrected ESF-to-RPS-relay additions, I do not see any remaining removed edge that should be restored under the landed-connection rule. The round 03 matrix is saturated for visually/geometrically supported edges available from the allowed raw/aids.
