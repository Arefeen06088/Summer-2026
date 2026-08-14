# Document 22 Connectivity Extraction

Scope: one blind iteration using only the `Raw + wires + components + junctions` folder. No GT or GT-derived feedback was used.

Visual method: native visual inspection of the raw diagram and derived overlays/crops. No off-the-shelf OCR engine was used.

Final policy: primary matrix contains visually supported solid power/DC/UPS supply conductors. Dashed control and dotted/instrument relationships are retained as notes only.

Final node count: 158
Final edge count: 160

Final saturation detail: Diego identified four solid UPS feeder drops that Jennifer accepted in the last round:
- BUS-UPS-A -- PNL-RPS-A
- BUS-UPS-A -- PLC-SAF-A
- BUS-UPS-B -- PNL-RPS-B
- BUS-UPS-B -- PLC-SAF-B

Notes-only visual candidates removed from the primary matrix:
- RELAY-87U, C-031, W-011, SYNC-PNL-1
- INST-PT-A/B/C/D and INST-CT-A/B/C/D
- RELAY-K* lower-control relays, JB-* junction boxes, TERM-* terminals
- SOL-SDV-A/B, DIODE-OR-A/B, XFMR-PT-1, METER-V01, METER-A01
- ANN-PNL-CR, REC-SEQ-1, JB-CR-01, TERM-MTB-A/B, downstream UPS relays

Round artifacts:
- round_01_diego_high_recall: Diego, 203 nodes, 219 edges, round_01_diego_high_recall_connectivity_matrix.csv
- round_02_jennifer_precision: Jennifer, 154 nodes, 156 edges, round_02_jennifer_precision_connectivity_matrix.csv
- round_03_diego_saturation: Diego, 158 nodes, 160 edges, round_03_diego_saturation_connectivity_matrix.csv
- round_04_jennifer_final: Jennifer, 158 nodes, 160 edges, round_04_jennifer_final_connectivity_matrix.csv

Token accounting note: the OpenAI Responses input-token counting endpoint was not called because no API key is available in this environment. Estimates use a local tokenizer when installed, a chars/4 fallback for text, and a high-detail image tile heuristic for image inputs.
