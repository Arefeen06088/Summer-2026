# Document 26 Final Connectivity Summary

## Final matrix

- Final source round: `document26_round04_jennifer`
- Nodes: 200
- Unique undirected edges: 209
- Validation: passed
- Matrix checks: symmetric, diagonal zero, no unknown nodes, no duplicate undirected pairs, matrix edge set matches edge CSV

## Round progression

| Round | Agent | Nodes | Edges | Added vs previous | Removed vs previous | Validation |
|---|---:|---:|---:|---:|---:|---|
| 01 | Diego | 200 | 209 | n/a | n/a | passed |
| 02 | Jennifer | 200 | 209 | 0 | 0 | passed |
| 03 | Diego | 200 | 209 | 0 | 0 | passed |
| 04 | Jennifer | 200 | 209 | 0 | 0 | passed |

## Final edge kinds

| Edge kind | Count |
|---|---:|
| power_feeder | 169 |
| instrument_signal | 16 |
| control_interlock | 10 |
| ground | 8 |
| bus_tie | 6 |

## Token accounting

The OpenAI Responses input-token counting endpoint and response usage objects were unavailable because no API key was present and the subagent tool did not expose usage payloads. Estimates use `tiktoken` `o200k_base` for text plus public high-detail image tiling estimates for the image inputs.

| Document | Iteration | Calls | Low | Expected | High | Expected text input | Expected image input | Expected output | API key |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 26 | 1 | 6 | 141160 | 274412 | 572217 | 141932 | 94180 | 38300 | no |

## Model calls recorded

| Call ID | Agent | Round | Role | Model | Expected total tokens | Usage object |
|---|---|---|---|---|---:|---|
| main-01 | main | setup | orchestrator | gpt-5.5 | 632 | unavailable |
| diego-01 | Diego | 01 | high-recall extractor | gpt-5.5 | 58897 | unavailable |
| jennifer-01 | Jennifer | 02 | precision reviewer | gpt-5.5 | 73378 | unavailable |
| diego-02 | Diego | 03 | saturation extractor | gpt-5.5 | 66581 | unavailable |
| jennifer-02 | Jennifer | 04 | final precision signoff | gpt-5.5 | 70619 | unavailable |
| main-02 | main | finalize | orchestrator | gpt-5.5 | 4305 | unavailable |

## Blind extraction constraint

Only resources inside `Raw + wires + junctions + OCR` were used. No GT, GT-derived feedback, evaluator output, TesseractOCR, RapidOCR, or other off-the-shelf OCR was used.
