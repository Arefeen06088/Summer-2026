# Document 23 Connectivity Extraction

Scope: one blind iteration using only the document 23 `Raw + wires + components + junctions` folder and generated crops. No GT or GT-derived feedback was used.

Visual method: native visual inspection of the raw diagram and derived overlays/crops. No off-the-shelf OCR engine was used.

Final policy: primary matrix contains visually supported solid power/DC/UPS paths, direct solid panel/fuse drops, and direct solid grounding drops. Dashed control/interlock and long-dashed instrument/metering relationships are notes only.

Final node count: 152
Final edge count: 152

Jennifer precision additions retained in final:
- BUS-4160-A -- GND-41A
- BUS-4160-B -- GND-41B
- BUS-24DC-C -- PNL-DCS-A
- BUS-24DC-C -- PNL-DCS-B

Notes-only visual candidates removed from primary scoring matrix:
- Top relays/meters/PT/sync: RELAY-87A/B, RELAY-27A/B, METER-A/B, PT-41A/B, SYNC-41
- Load-center instruments and control wiring: INST-*, JB-*-1, RELAY-K*, dashed local XV controls
- DC/RPS metering and controls: METER-DC-A/B, RELAY-KA/KB/KTIE, ANN-A/B, REC-SER-A/B, INST-NIS-A/B, JB-CTRL-A/B
- PNL-DCS-A/B to JB-CTRL-A/B continuations are dashed/control notes only

Round artifacts:
- round_01_diego_high_recall: Diego, 198 nodes, 210 edges, round_01_diego_high_recall_connectivity_matrix.csv
- round_02_jennifer_precision: Jennifer, 152 nodes, 152 edges, round_02_jennifer_precision_connectivity_matrix.csv
- round_03_diego_saturation: Diego, 152 nodes, 152 edges, round_03_diego_saturation_connectivity_matrix.csv
- round_04_jennifer_final: Jennifer, 152 nodes, 152 edges, round_04_jennifer_final_connectivity_matrix.csv

Token accounting: usage objects were not exposed by the subagent/tool responses, and no API key is available for the Responses input-token counting endpoint. The saved table uses local estimates.
