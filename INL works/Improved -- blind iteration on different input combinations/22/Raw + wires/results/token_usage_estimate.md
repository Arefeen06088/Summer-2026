# Token Usage Estimate - Document 22

Exact Responses usage objects were not exposed by the available subagent tooling, and no API key was available for the Responses input-token counting endpoint. These values are proxy estimates.

| Call | Agent | Round | Input expected | Image input expected | Output expected | Total expected |
|---|---:|---:|---:|---:|---:|---:|
| main_01_orchestration | main | orchestration | 24000 | 0 | 900 | 24900 |
| subagent_01_diego_round1 | Diego | Round 1 | 233764 | 233665 | 1700 | 235464 |
| subagent_02_jennifer_round1 | Jennifer | Round 1 | 198913 | 198815 | 1450 | 200363 |
| subagent_03_diego_round2 | Diego | Round 2 | 128783 | 128690 | 450 | 129233 |
| subagent_04_jennifer_round2_final | Jennifer | Round 2 final | 74132 | 74035 | 180 | 74312 |

Expected total: 664272 tokens (low 563702, high 766032).
