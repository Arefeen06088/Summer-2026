# Diego Round 03 Saturation Notes

## Scope

- Reviewed only the document 19 folder: C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires + junctions + OCR.
- Used Jennifer round 02 kept/removed rows, the raw schematic, wire/node overlays, wire_nodes.csv, and component_visual_ocr_labels.csv.
- Did not use Ground Truth, evaluator feedback, files outside the folder, or off-the-shelf OCR.

## Decisions

- No removed Jennifer edge was restored.
- No new corrected edge was added.
- No additional edge was dropped or renamed relative to Jennifer round 02.
- Matrix status: saturated for this pass.

## Specific Review Points

- BUS-125DC-A -- JB-MAIN: agreed with removal. The raw lower A crop shows JB-MAIN landing by a dashed/drop connection to BUS-120AC-A; the BUS-125DC-A run begins below as a separate DC bus with no visible conductor or filled dot to JB-MAIN.
- BUS-120AC-B -- CHGR-125B: agreed with removal. The CHGR-125B/BAT-125B vertical crosses BUS-120AC-B without a filled dot. The wire-node aid marks the geometric crossing as a junction, but the raw schematic and note convention require a filled dot/clear landing, so this is not restored.
- LCS-MOV601 -> LS-MOV601: agreed. The raw MOV601 label reads LS-MOV601, and Jennifer's endpoints INST-601 -- LS-MOV601 -- JB-601 preserve the visible dotted local path.
- CONTROL_POWER_DC_DISTRIBUTION_HEADER to CB-301, CHGR-125A, CB-302, and CHGR-125B: kept as medium confidence. Each has a visible routed header drop to the device; no extra bus crossing or AC/DC overconnection was inferred.
- CPT-* labels: kept. No stale feeder PT-* endpoints remain; the only remaining PT-* endpoints are true PT-4160A and PT-4160B instrument taps.

## Counts

Total saturated edges: 200

By kind:
- ac_power: 5
- control: 24
- control_power: 4
- control_signal: 2
- dc_power: 6
- instrumentation_signal: 27
- power: 104
- protection_signal: 12
- signal: 12
- tie_power: 4

By confidence:
- high: 188
- medium: 12

Stale feeder PT endpoint count: 0

Round 03 changes relative to Jennifer round 02: none.
