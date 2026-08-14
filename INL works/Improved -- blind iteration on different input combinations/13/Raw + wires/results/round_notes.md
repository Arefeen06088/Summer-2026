# Document 13 Round Notes

Inputs used: raw schematic, wires mask, wires mask overlay, and local crops derived from those same files. No GT or GT-derived resources were used.

| round | agent | matrix | notes |
|---|---|---|---|
| round_01_diego_high_recall | Diego | connectivity_matrix_round_01_diego_high_recall.csv | High-recall proposal; includes plausible but later excluded label/ground/continuation edges. |
| round_01_jennifer_precision | Jennifer | connectivity_matrix_round_01_jennifer_precision.csv | Precision pass; demoted dashed/control and inverter-to-UPS visual links to uncertain. |
| round_02_diego_saturation | Diego | connectivity_matrix_round_02_diego_saturation.csv | Saturation pass; restored visibly terminating dashed/control and inverter-to-UPS links. |
| round_02_jennifer_final | Jennifer | connectivity_matrix_round_02_jennifer_final.csv | Final precision agreement with visual/geometric policy. |

Final saturation: Jennifer R2 agreed with Diego R2 that the requested visual/geometric matrix should include visibly terminating dashed/control links and solid inverter-to-UPS links.

Final excluded classes: unsupported crossings, continuation arrows without a component termination, ground/reference labels, and label-only associations.
