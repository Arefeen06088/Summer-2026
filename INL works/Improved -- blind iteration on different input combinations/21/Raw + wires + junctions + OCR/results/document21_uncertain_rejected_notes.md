# Document 21 Uncertain / Rejected Notes

Scope observed: only the permitted document 21 raw schematic, allowed overlays/CSVs, and precision review crops in the requested folder were used. No Ground Truth, evaluator feedback, previous-document outputs, or off-the-shelf OCR were used.

## Included With Medium/Low Confidence

- `4KV_SWITCHGEAR_LEFT_RISER` is included as a logical node. The raw full-left/top-center view shows a vertical solid riser with black dots at several 4.16 kV bus intersections and the `CB-301A` drop. It is visually plausible as an intentional tap/riser, but the electrical intent is ambiguous, so related edges are medium confidence.
- `DS-J02B` to `CB-502B` is included at medium confidence. The vertical feeder continues downward through the Train B block, while the nearby `BUS-301B` crossing is not promoted because the junction-dot evidence is not clear.
- `BUS-301A` to `DS-401A` and `BUS-301A` to `DS-402A` are included at medium confidence. A long solid feeder drops from the Train A 480 V area into the DC/UPS block; the visible alignment favors `BUS-301A`, but the long vertical routing crosses section boundaries.
- `BUS-401A` to `DS-402B`, `INV-120C` to `BUS-501A`, and `RECT-24C` to `BUS-501B` are included at medium confidence because the long lower DC/UPS feeder continuations are visible but extend across a wide span before reaching the ladder bus area.
- `DS-401B` to `BUS-401B` is included as `normally_open_tie` at medium confidence because the line style matches the heavy dashed N.O. tie legend and visibly descends from the `DS-401B` region toward `BUS-401B`.
- `BUS-501A/B` to `CP-CRD` are included at low confidence: the bottom U-shaped dashed bus/tie geometry visibly reaches the CP-CRD vertical dashed line, but routing is partly off the main ladder rows.

## Added Nodes Not In Component CSV

- Added buses/logical nodes: `BUS-101`, `BUS-102`, `BUS-201A`, `BUS-201B`, `BUS-202A`, `BUS-202B`, `BUS-301A`, `BUS-302A`, `BUS-301B`, `BUS-302B`, `BUS-401A`, `BUS-401B`, `BUS-501A`, `BUS-501B`, and `4KV_SWITCHGEAR_LEFT_RISER`.
- Added physical device nodes visible in the raw schematic but absent from the component CSV: `CB-204A`, `CB-204B`, and `DS-401B`. These are kept as intermediate nodes and not collapsed through.

## Rejected / Not Promoted

- The annotation strings `FEEDERS DROP TO 480 VLC`, `EDG FEEDERS/NO TIE CROSSING`, `DC FEEDERS CONTINUE BELOW`, and `CONTROL LADDER CIRCUITS` were rejected as labels/notes rather than graph nodes.
- The right-side `NOTES`, `LINE CODE`, `SYMBOL KEY`, `REVISION STATUS`, title block metadata, sheet grid border letters/numbers, component/connection count text, and connectivity-matrix filename were rejected as artifacts.
- The apparent `DS-J02B` vertical crossing at `BUS-301B` was not treated as a connection because there is no clear junction dot in the raw view.
- Generic line crossings in dense MCC and ladder regions were not promoted unless a black junction dot or direct device terminal contact was visible.
