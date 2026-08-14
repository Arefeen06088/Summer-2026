# Round 01 Diego Connectivity Proposal - Doc 15

## Scope and Inputs

This proposal was prepared from the current doc 15 input resources and generated inspection aids only:

- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\15\Input resources\raw -- improved_synthetic_nuclear_electrical_schematic.png`
- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\15\Input resources\component_visual_ocr_labels.csv`
- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\15\Input resources\wire_nodes.csv`
- wire mask/overlay images in the input folder
- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\15\Codes and artifacts\component_labels_list.txt`
- `C:\Asif_all_python_projects\INL\Improved -- blind iterations\15\Codes and artifacts\inspection_crops`

No ground truth, evaluator output, validation metrics, or previous document outputs were used.

## Node Policy

- All 163 detected component inventory labels from `component_visual_ocr_labels.csv` / `component_labels_list.txt` were retained.
- Visually named bus candidates were confirmed and added as nodes: BUS-SWY-1, BUS-SWY-2, BUS-NSS-1, BUS-NSS-2, BUS-416A/B/C/D, BUS-480A/B/C/D, and BUS-DC-A/B/C/D.
- MCC-1A/B/C/D and GND-A/B/C/D were already present in the component inventory and retained.
- Four visually named control panels not present in the component CSV were added because dashed wiring visibly connects to them: SEQ-1AB, RPS-AC-1, SEQ-2CD, and RPS-AC-2.
- Anonymous WN-* points from `wire_nodes.csv` were not used as graph endpoints. The wire-node overlay was used only as an inspection aid for dots/endpoints/crossings.

## High-Confidence Solid Connectivity

High-confidence edges are direct solid-wire or solid named-bus connections. This includes:

- Generator/source trains: GEN-101 -> CB-GEN-101 -> TR-GSU-1 -> BUS-SWY-1 and GEN-102 -> CB-GEN-102 -> TR-GSU-2 -> BUS-SWY-2.
- Switchyard tie: BUS-SWY-1 -> CB-SWY-TIE -> BUS-SWY-2.
- Transformer drops from switchyard to station-service buses through TR-UAT-1, TR-SAT-1, TR-UAT-2, and TR-SAT-2.
- Normal and diesel feeder paths from BUS-NSS-1/2 through CB-NF-* and DG-1*/CB-DG-* down to BUS-416A/B/C/D.
- Normally open visual tie paths BUS-416A -> CB-TIE-AB -> DS-TIE-AB -> BUS-416B and BUS-416C -> CB-TIE-CD -> DS-TIE-CD -> BUS-416D.
- The 416 V to 480 V to MCC chains in all four divisions.
- Solid MCC load feeder drops through each CB and downstream disconnect/fuse to the final load.

## Plausible / Lower-Confidence Connectivity

Plausible edges are retained for high recall but separated because they are dashed control/trip/status wiring, long routed dashed paths, or otherwise not solid feeder wiring. This includes:

- Dashed trip/control relationships among CB-NF-*, CB-DG-*, SEQ-1AB/RPS-AC-1, and SEQ-2CD/RPS-AC-2.
- Dashed breaker-to-relay associations for all feeder relays RLY-A01 through RLY-D06.
- The long dashed RLY-*06 to TB-1* paths.
- Dashed 125 VDC/control row connections BAT -> CHG -> BUS-DC -> INV -> CP -> TB/JB and BUS-DC -> GND. The DC buses are visually named and retained, but their equipment leads are dashed in the raw drawing.

## Ambiguities and Assumptions

- The DG symbols DG-1A/B/C/D are visually on/touched by the BUS-NSS-1 or BUS-NSS-2 horizontal bus line and also have solid vertical drops to CB-DG-A/B/C/D. For a visual high-recall graph, BUS-NSS-X to DG-1X was kept as a high-confidence visual contact. If the intended functional model treats DG symbols as merely adjacent labels/sources, these four bus-to-DG edges are candidates for review.
- The AB and CD ties are annotated normally open. They remain in the high-confidence file because the solid drawn path is visually present; the `edge_type` marks them as normally open tie connectivity.
- Dashed control wiring sometimes branches or routes through shared vertical runs. Where a panel/breaker association was visible but the precise branch ownership was not as solid as a direct feeder, it was placed in the plausible file.
- Crossings without dots were not converted into edges. Dots on named buses were treated as intentional junctions.
- The drawing legend states dashed line = control/trip/status wiring, so dashed DC/control and relay links were not mixed with the high-confidence solid feeder list.

## File Counts

- Nodes: 183 total = 163 inventory labels + 16 visually named buses + 4 visually named control panels.
- High-confidence edges: 130.
- Plausible/lower-confidence edges: 68.
