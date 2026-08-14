# Diego Round 03 Saturation Notes

Scope: reviewed only the permitted document 21 folder, its raw schematic, available wires/junction/label crops, and the named Diego/Jennifer CSV and note files. No Ground Truth, evaluator feedback, previous-document outputs, GT-derived files, generated matrices, or off-the-shelf OCR were used. The raw schematic remained the authority.

## Decision

Accept Jennifer round 02 with no edge changes. Diego round 03 is a saturation pass and carries forward the same 202-edge set.

## Counts

- Jennifer round 02 input edges: 202
- Diego round 03 saturation edges: 202
- Round 03 additions: 0
- Round 03 removals: 0
- Round 03 corrections: 0
- Edge kinds: 122 power_feeder, 58 control_interlock, 15 instrument_signal, 6 ground, 1 normally_open_tie
- Confidence: 186 high, 16 medium, 0 low

## Visual Rationale

- Accepted removal of `4KV_SWITCHGEAR_LEFT_RISER`. The raw 4.16 kV switchgear view shows separate busbars with aligned tap/end geometry; retaining one abstract riser would overconnect `BUS-201A`, `BUS-201B`, `BUS-202A`, and `BUS-202B`. The replacement `BUS-201A -- CB-301A` preserves the visually supported feeder drop to `CB-301A` without tying the buses together.
- Accepted removal of `BUS-501A -- CP-CRD` and `BUS-501B -- CP-CRD`. The bottom control-ladder geometry is a U-shaped/dashed continuation near `CP-CRD`, not a clear independent terminal tap from both inverter buses.
- Confirmed retained raw-only devices `CB-204A`, `CB-204B`, and `DS-401B`. Each label and component symbol is visible on the raw schematic even though they are absent from the component CSV, and their adjacent feeder segments are visually supported.
- Confirmed retained `DS-J02B -- CB-502B`. The Train B vertical feeder continues through the `BUS-301B` area toward `CB-502B`; the crossing at `BUS-301B` lacks a junction dot, so no `BUS-301B` connection is added.
- Confirmed retained DC/UPS continuations: `BUS-301A -- DS-401A`, `BUS-301A -- DS-402A`, `BUS-401A -- DS-402B`, `INV-120C -- BUS-501A`, and `RECT-24C -- BUS-501B`.
- Confirmed retained `DS-401B -- BUS-401B` as `normally_open_tie`; the heavy dashed segment from `DS-401B` to the `BUS-401B` area matches the N.O. tie line style.

## Saturation Check

No additional visually supported edge was found missing from Jennifer's round-02 set. The graph pass found no component-index label absent from the edge-node set, and the only differences from Diego's original proposal are Jennifer's seven disputed removals plus the one `BUS-201A -- CB-301A` replacement.
