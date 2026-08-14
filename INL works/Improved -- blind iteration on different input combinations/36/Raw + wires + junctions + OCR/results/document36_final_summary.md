# Document 36 Final Connectivity Summary

## Final matrix

- Final source round: `document36_round04_jennifer`
- Nodes: 55
- Unique included undirected edges: 60
- Validation: passed
- Matrix checks: symmetric, diagonal zero, no unknown endpoints, no duplicate undirected pairs, matrix edge set matches edge CSV

## Round progression

| Round | Agent | Nodes | Included edges | Added vs previous | Removed vs previous | Validation |
|---|---:|---:|---:|---:|---:|---|
| 01 | Diego | 55 | 62 | n/a | n/a | passed |
| 02 | Jennifer | 55 | 60 | 0 | 2 | passed |
| 03 | Diego | 55 | 60 | 0 | 0 | passed |
| 04 | Jennifer | 55 | 60 | 0 | 0 | passed |

## Final edge kinds

| Edge kind | Count |
|---|---:|
| power_feeder | 48 |
| control_interlock | 8 |
| bus_tie | 4 |

## Key round 02 refinements

- Removed unsupported low-confidence fan control candidates:
  - `PNL-ESF-A -- FAN-CONTAIN-A`
  - `PNL-ESF-B -- FAN-CONTAIN-B`
- Kept `CB-13-TIE -- PNL-RPS-1` as medium-confidence control/interlock.
- Kept `CB-4K-TIE -- PNL-RPS-1` as high-confidence control/interlock.
- Confirmed bus ties are represented through tie breaker nodes rather than direct bus-to-bus edges.
- Confirmed DC topology: rectifier, battery, and inverter connect to their respective `BUS-DC125-A/B` nodes.

## Token accounting

The OpenAI Responses input-token counting endpoint and response usage objects were unavailable because no API key was present and the subagent tool did not expose usage payloads. Estimates use `tiktoken` `o200k_base` for text plus public high-detail image tiling estimates for image inputs.

| Document | Iteration | Calls | Low | Expected | High | Expected text input | Expected image input | Expected output | API key |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 36 | 1 | 6 | 66381 | 174704 | 455741 | 42224 | 94180 | 38300 | no |

## Model calls recorded

| Call ID | Agent | Round | Role | Model | Expected total tokens | Usage object |
|---|---|---|---|---|---:|---|
| main-01 | main | setup | orchestrator | gpt-5.5 | 632 | unavailable |
| diego-01 | Diego | 01 | high-recall extractor | gpt-5.5 | 39108 | unavailable |
| jennifer-01 | Jennifer | 02 | precision reviewer | gpt-5.5 | 43649 | unavailable |
| diego-02 | Diego | 03 | saturation extractor | gpt-5.5 | 42580 | unavailable |
| jennifer-02 | Jennifer | 04 | final precision signoff | gpt-5.5 | 44188 | unavailable |
| main-02 | main | finalize | orchestrator | gpt-5.5 | 4547 | unavailable |

## Blind extraction constraint

Only resources inside `Raw + wires + junctions + OCR` were used. No GT, GT-derived feedback, evaluator output, TesseractOCR, RapidOCR, or other off-the-shelf OCR was used.
