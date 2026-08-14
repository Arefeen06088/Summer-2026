# Token Usage Estimate

Exact Responses token-count endpoint calls and model usage objects were not available because no API key or usage object was exposed through the local subagent tools. This file uses local text-token heuristics plus an OpenAI-style high-detail image tiling estimate for each planned image payload.

| Document | Iteration | Call | Actor | Input expected | Cached input | Output expected | Image/file tokens expected | Total low | Total expected | Total high |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 40 | 1 | main_agent_visual_orchestration | Main agent | 39690 | 0 | 3600 | 9690 | 33050 | 43290 | 55113 |
| 40 | 1 | round1_diego_high_recall | Diego | 9717 | 0 | 10000 | 9690 | 7877 | 19717 | 27146 |
| 40 | 1 | round1_jennifer_precision | Jennifer | 7904 | 0 | 10500 | 7480 | 8104 | 18404 | 25859 |
| 40 | 1 | round2_diego_saturation | Diego | 6454 | 0 | 1500 | 6035 | 1814 | 7954 | 11547 |
| 40 | 1 | round2_jennifer_final | Jennifer | 7899 | 0 | 1200 | 7480 | 1699 | 9099 | 12853 |
| 40 | 1 | **TOTAL** | all |  |  |  |  | **52544** | **98464** | **132518** |

Reasoning tokens: not available from the subagent tool responses.
Cached input tokens: recorded as 0 because cache accounting was not exposed.
