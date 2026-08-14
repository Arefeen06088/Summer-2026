# Round 02 Diego High-Recall Review Notes

## Scope

Reviewed only the allowed doc 39 raw/input resources, the current fresh aids/crops, Diego round 01, and Jennifer round 01 precision artifacts. Ground Truth, scoring/eval outputs, prior results, and archives were not used.

The raw schematic PNG was treated as authoritative. Current overlays and temporary magnified crops from the allowed raw PNG were used only to inspect endpoints and line continuity.

## Agree With Jennifer R01

- `LC-A` and `LC-B` should not be final nodes. In the 480 V load-center crop, each appears as text printed at the end of the `BUS-480-*` conductor, not as a separate boxed component, terminal strip, or distinct bus node.
- `CONTROL-ROOM-ANNUNCIATION` should not be a final node. The lower raw area shows it as route text beneath the lower dashed/control-room path, not as a terminal, component, or cleanly bounded bus.
- Charger feeds should be `BUS-480-A -> CHG-125A` and `BUS-480-B -> CHG-125B`. The raw A/B charger areas show solid L-shaped conductors from the charger tops to the LC-A/LC-B 480 V load-center ends. No distinct 4160-to-charger terminal landing is visible.
- `ANN-CR01 -> REC-SOE01` should remain keep. The lower crop shows a direct dashed segment between the right side of `ANN-CR01` and the left side of `REC-SOE01`.
- `JB-A101 -> ANN-CR01` and `REC-SOE01 -> JB-B101` should remain remove. The lower crop shows visible gaps rather than direct endpoint-to-endpoint dashed connections.
- All clearly supported solid power/load topology from Jennifer R01 is preserved, including source-to-switch-to-transformer-to-breaker paths, bus tie through `CB-TIE-AB`, 4160-to-480 transformer/breaker paths, MCC/load feeders, DC stack sequences, and the A-side ground reference.

## Disagree With Jennifer R01

- Changed `RPS-A -> JB-A101` from uncertain to keep. The magnified raw left lower-control area shows a continuous dashed control conductor leaving the lower `RPS-A` terminal area, descending, turning right along the lower route, and terminating at the left side of `JB-A101`. The raw terminal schedule also lists A101 from `RPS-A`, which supports the intended endpoint.
- Changed `RPS-B -> JB-B101` from uncertain to keep. The magnified raw right lower-control area shows a continuous dashed control conductor leaving the right side of `RPS-B`, running down the right-side route, turning left, and terminating at the right side of `JB-B101`. The raw terminal schedule also lists B101 from `RPS-B`, which supports the intended endpoint.

These two are long routed conductors, but the raw diagram shows continuous terminal-to-terminal paths without requiring a promoted intermediate route/bus node.

## Final Node Policy

Final nodes match Jennifer R01. No `WIRE-NODE-*` points were promoted. Annotation-only labels, including `LC-A`, `LC-B`, and `CONTROL-ROOM-ANNUNCIATION`, were not restored.

## Matrix Policy

The matrix includes keep edges only. Remove rows remain documented in `round_02_diego_edges.csv` for auditability. The two former uncertain RPS-to-JB rows are included in the matrix as keep edges.

## Saturation Recommendation

Recommend saturation after this round. The remaining high-risk ambiguities were rechecked visually, and only the two long RPS-to-JB dashed conductors changed from Jennifer R01.
