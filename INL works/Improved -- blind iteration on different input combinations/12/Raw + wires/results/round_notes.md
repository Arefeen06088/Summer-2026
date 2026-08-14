# Document 12 Round Notes

Inputs used: only raw schematic, wires mask, wires overlay, and local crops derived from those files. No GT or GT-derived feedback/resources were used.

| round | agent | matrix | notes |
|---|---|---|---|
| round_01_diego_high_recall | Diego | connectivity_matrix_round_01_diego_high_recall.csv | High-recall pass with broad dashed/control fan-out and direct ESFAS bus edges. |
| round_01_jennifer_precision_stalled | Jennifer | connectivity_matrix_round_01_jennifer_precision_stalled.csv | First Jennifer pass was shut down after timing out; no usable matrix returned. |
| round_01_jennifer_precision | Jennifer | connectivity_matrix_round_01_jennifer_precision.csv | Targeted precision pass: removed direct ESF bus to ESFAS panels and broad control fan-out. |
| round_02_diego_saturation | Diego | connectivity_matrix_round_02_diego_saturation.csv | Restored six directly visible control edges; left broad fan-out uncertain. |
| round_02_jennifer_final | Jennifer | connectivity_matrix_round_02_jennifer_final.csv | Final saturation: accepted the six restorations and demoted BUS-120VAC-ESF--SEQ-REC-1 to uncertain. |

Final saturation: Jennifer R2 accepted Diego R2's six directly visible control-edge restorations and kept broader relay/TB/RPS fan-out uncertain.

Final removed edges: direct BUS-120VAC-ESF--PNL-ESFAS-A and BUS-120VAC-ESF--PNL-ESFAS-B.
