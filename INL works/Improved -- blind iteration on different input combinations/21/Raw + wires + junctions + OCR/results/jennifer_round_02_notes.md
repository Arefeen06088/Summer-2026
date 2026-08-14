# Jennifer Round 02 Precision Notes

Scope: reviewed only the permitted document 21 folder, Diego result CSV/notes, the raw schematic, and generated precision-review crops/CSVs. No Ground Truth, evaluator feedback, previous-document outputs, GT-derived files, or off-the-shelf OCR were used.

## Counts

- Diego proposed edges reviewed: 208
- Removed Diego edges: 7
- Added/replacement edges: 1
- Jennifer kept edge set: 202
- Node/label decision rows: 32

## Key Precision Decisions

- Rejected `4KV_SWITCHGEAR_LEFT_RISER` as an unsupported logical node. The raw view shows aligned 4.16 kV busbar end/boundary geometry; promoting it electrically overconnects `BUS-201A/B` and `BUS-202A/B`. Added replacement `BUS-201A -- CB-301A` so the visible CB-301A feeder remains represented without tying separate buses together.
- Confirmed raw-only devices `CB-204A`, `CB-204B`, and `DS-401B` as visible labeled intermediate nodes. Their connected breaker/disconnect/transformer chains stay intact.
- Kept `DS-J02B -- CB-502B`; the vertical Train B feeder crosses the `BUS-301B` area without a junction dot and then lands on `CB-502B`. The `BUS-301B` crossing remains rejected.
- Kept medium DC/UPS continuations: `BUS-301A -- DS-401A`, `BUS-301A -- DS-402A`, `BUS-401A -- DS-402B`, `INV-120C -- BUS-501A`, and `RECT-24C -- BUS-501B`.
- Kept `DS-401B -- BUS-401B` as `normally_open_tie`; the heavy dashed segment visibly lands from the DS-401B area to BUS-401B.
- Removed `BUS-501A -- CP-CRD` and `BUS-501B -- CP-CRD`; the evidence is bottom U-shaped/dashed routing, not a clear independent bus-to-CP-CRD terminal tap.
- Kept UVLS branches and the ladder rows: panel/module to relay chain to JB, then dotted JB-to-instrument continuations. Crossings without junction dots were not promoted.
