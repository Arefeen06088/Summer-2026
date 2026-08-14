# Document 27 Final Connectivity Summary

## Final matrix

- Final source round: `document27_round04_jennifer`
- Included nodes: 200
- Unique undirected edges: 201
- Validation: passed
- Matrix checks: symmetric, diagonal zero, no unknown endpoints, no duplicate undirected pairs, matrix edge set matches edge CSV

## Round progression

| Round | Agent | Included nodes | Edges | Added vs previous | Removed vs previous | Validation |
|---|---:|---:|---:|---:|---:|---|
| 01 | Diego | 201 | 202 | n/a | n/a | passed |
| 02 | Jennifer | 200 | 201 | 7 | 8 | passed |
| 03 | Diego | 200 | 201 | 0 | 0 | passed |
| 04 | Jennifer | 200 | 201 | 0 | 0 | passed |

## Final edge kinds

| Edge kind | Count |
|---|---:|
| power_feeder | 155 |
| instrument_signal | 26 |
| control_interlock | 15 |
| bus_tie | 3 |
| ground | 2 |

## Key round 02 refinements

- Renamed `BUS-13.8KV` to the visually printed `BUS-13KV-N`.
- Rejected `TE-41` and removed `CB-TIE-41 -- TE-41`.
- Replaced unsupported `DS-A10 -- CHGR-125A` with `DS-A10 -- JB-A10`.
- Added the visible charger tap `BUS-480-A -- CHGR-125A`.
- Removed duplicate direct `DC-BUS-125B -- PANEL-CTRL-MAIN`; retained `DC-BUS-125A -- PANEL-CTRL-MAIN`.

## Token accounting

The OpenAI Responses input-token counting endpoint and response usage objects were unavailable because no API key was present and the subagent tool did not expose usage payloads. Estimates use `tiktoken` `o200k_base` for text plus public high-detail image tiling estimates for image inputs.

| Document | Iteration | Calls | Low | Expected | High | Expected text input | Expected image input | Expected output | API key |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 27 | 1 | 6 | 171149 | 314396 | 633077 | 181916 | 94180 | 38300 | no |

## Model calls recorded

| Call ID | Agent | Round | Role | Model | Expected total tokens | Usage object |
|---|---|---|---|---|---:|---|
| main-01 | main | setup | orchestrator | gpt-5.5 | 632 | unavailable |
| diego-01 | Diego | 01 | high-recall extractor | gpt-5.5 | 56009 | unavailable |
| jennifer-01 | Jennifer | 02 | precision reviewer | gpt-5.5 | 79860 | unavailable |
| diego-02 | Diego | 03 | saturation extractor | gpt-5.5 | 80514 | unavailable |
| jennifer-02 | Jennifer | 04 | final precision signoff | gpt-5.5 | 92980 | unavailable |
| main-02 | main | finalize | orchestrator | gpt-5.5 | 4401 | unavailable |

## Blind extraction constraint

Only resources inside `Raw + wires + junctions + OCR` were used. No GT, GT-derived feedback, evaluator output, TesseractOCR, RapidOCR, or other off-the-shelf OCR was used.
