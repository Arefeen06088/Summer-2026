# Jennifer Round 02 Precision Notes

## Scope

- Reviewed only files inside C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires + junctions + OCR.
- Used the raw schematic and provided visual aids/crops; no Ground Truth, evaluator feedback, outside files, or off-the-shelf OCR.
- Started from Diego's 202 high-recall edge rows and applied strict precision review.

## Major Decisions

- Kept raw bus labels where visible: BUS-4160-A/B, BUS-480-A/B, BUS-120AC-A/B, and BUS-125DC-A/B.
- Preserved breaker-mediated and tie-mediated connectivity; no direct A/B bus joins were added.
- Kept CB-F402 and DS-F301 as visible physical devices with landed connections.
- Corrected Diego's added LCS-MOV601 to LS-MOV601; the MOV601 lower instrument circle is visibly labeled LS-MOV601, and its dotted signal path lands through JB-601/TB-601.
- Kept CPT-* corrections for feeders 201, 202, 203, 204, 301, 302, 401, 402, 501, 502, 601, and 701 because the raw transformer text visibly reads CPT-*.

## Removed Edges

- Removed BUS-125DC-A to JB-MAIN: JB-MAIN visibly lands on BUS-120AC-A only; no visible conductor/junction dot lands on BUS-125DC-A.
- Removed BUS-120AC-B to CHGR-125B: the CHGR-125B/battery vertical crosses or abuts BUS-120AC-B without a filled dot or clear landing.

## Retained With Caution

- Kept the labeled CONTROL POWER / DC DISTRIBUTION header drops to CB-301, CHGR-125A, CB-302, and CHGR-125B where visible vertical drops land on the devices.
- Kept BUS-120AC-A to JB-MAIN because a filled bus dot and dotted landing to JB-MAIN are visible.
- Kept dashed/dotted feeder signal/control edges only where they visibly land component-to-component; dotted module boundaries remain rejected artifacts.

## Counts

- Diego input edges: 202
- Jennifer kept edges: 200
- Jennifer removed edges: 2
- Node decision rows: 28
- Node renames/corrections: 13 (12 CPT corrections plus LCS-MOV601 -> LS-MOV601)
- Rejected artifact categories: 4

## Residual Uncertainty

- 12 kept edges remain medium confidence, mainly around added/renamed physical devices and compact lower control-power/DC-distribution header routing. Unsupported compact AC/DC overconnections were dropped rather than guessed.
