# Token Usage Estimate - Document 24

Exact Responses usage objects were not exposed by the available subagent tooling, and no API key was available for `POST /v1/responses/input_tokens`. These values are proxy estimates.

| Call | Agent | Round | Input expected | Cached expected | Image input expected | Output expected | Total expected |
|---|---:|---:|---:|---:|---:|---:|---:|
| main_01_orchestration | main | orchestration | 28000 |  | 0 | 900 | 28900 |
| subagent_01_diego_round1 | Diego | Round 1 | 63141 |  | 63070 | 1900 | 65041 |
| subagent_02_jennifer_round1 | Jennifer | Round 1 | 63139 |  | 63070 | 1500 | 64639 |
| subagent_03_diego_round2 | Diego | Round 2 | 63143 | 63070 | 63070 | 320 | 63463 |
| subagent_04_jennifer_round2_final | Jennifer | Round 2 final | 63140 | 63070 | 63070 | 180 | 63320 |

Expected total: 285363 tokens (low 227519, high 344627).
