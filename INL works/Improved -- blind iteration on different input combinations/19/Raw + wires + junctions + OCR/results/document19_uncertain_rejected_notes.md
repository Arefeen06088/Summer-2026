# Document 19 Uncertain And Rejected Notes

## Modeling Choices

- Inputs were limited to the raw schematic, provided wire/node overlays, and provided component/wire CSVs in the document 19 Raw + wires + junctions + OCR folder.
- Added logical bus/header nodes for labeled busbars and the lower CONTROL POWER / DC DISTRIBUTION header so components can connect to a bus instead of becoming a misleading component clique.
- Preserved breaker-mediated and tie-mediated connectivity: BUS-4160-A and BUS-4160-B connect only through CB-TIE-4160, and BUS-480-A and BUS-480-B connect only through CB-TIE-480.
- Feeder transformer symbols labeled `PT-201` etc. in the component CSV are visually labeled `CPT-201` etc. on the raw schematic, so the edge list uses `CPT-*` and records corrections.
- Repeated 480 V feeder columns were modeled as bus -> feeder breaker -> disconnect -> CPT -> MCC -> load breaker -> K relay/contact -> load, plus PR protection tap, A relay control branch, and local instrument/JB/TB/LCS signal/control chain.

## Crossings

- Crossings are not connected unless a filled dot/junction or clear landing is visible. This follows the note on the sheet: crossings without dots are not connected.
- Dotted feeder-module boundary rectangles are not nodes and were not treated as connected conductors.
- The lower control/DC distribution header crosses or parallels several module drops; only visible drops/landings to CB-301, CHGR-125A, CB-302, and CHGR-125B are modeled.

## Added Or Corrected Nodes

- Added logical busbars: BUS-4160-A, BUS-4160-B, BUS-480-A, BUS-480-B, BUS-120AC-A, BUS-120AC-B, BUS-125DC-A, BUS-125DC-B.
- Added logical header: CONTROL_POWER_DC_DISTRIBUTION_HEADER.
- Added missing physical devices visible on the raw drawing: CB-F402, DS-F301, and LCS-MOV601.
- Corrected feeder transformer labels from CSV `PT-*` to raw `CPT-*` for feeders 201, 202, 203, 204, 301, 302, 401, 402, 501, 502, 601, and 701.

## Uncertain Edges Kept With Medium Confidence

- CONTROL_POWER_DC_DISTRIBUTION_HEADER to CB-301/CB-302/CHGR-125A/CHGR-125B: the lower header and vertical drops are visible, but the simplified one-line/control-power layout compresses AC input and DC distribution behavior.
- BUS-120AC-A to JB-MAIN and BUS-125DC-A to JB-MAIN: JB-MAIN sits in a compact lower terminal area with vertical conductors to the AC and DC regions; included as plausible visible landings.
- BUS-120AC-B to CHGR-125B: there is a visible junction at the charger drop and BUS-120AC-B; modeled through the charger rather than directly tying AC and DC buses.
- Edges involving CB-F402, DS-F301, and LCS-MOV601 are medium confidence because these visually present devices were not present in the component CSV.

## Rejected Artifacts

- Title block, revision table, notes, legend samples, grid/frame lines, and coordinate ticks.
- Dotted module boundary rectangles around each feeder.
- Any apparent crossing where the raw schematic lacks a filled dot or component landing.

## Totals At Write Time

- Edge rows: 202
- Node decision rows: 28
