# Token Usage Estimate - Document 23

Exact Responses usage objects were not exposed by the available subagent tooling, and no API key was available for `POST /v1/responses/input_tokens`. These values are proxy estimates.

| Call | Agent | Round | Input expected | Cached expected | Image input expected | Output expected | Total expected |
|---|---:|---:|---:|---:|---:|---:|---:|
| main_01_orchestration | main | orchestration | 26000 |  | 0 | 900 | 26900 |
| subagent_01_diego_round1 | Diego | Round 1 | 65012 |  | 64940 | 1750 | 66762 |
| subagent_02_jennifer_round1 | Jennifer | Round 1 | 65009 |  | 64940 | 1250 | 66259 |
| subagent_03_diego_round2 | Diego | Round 2 | 65015 | 64940 | 64940 | 250 | 65265 |
| subagent_04_jennifer_round2_final | Jennifer | Round 2 final | 65013 | 64940 | 64940 | 170 | 65183 |

Expected total: 290369 tokens (low 231598, high 350610).
