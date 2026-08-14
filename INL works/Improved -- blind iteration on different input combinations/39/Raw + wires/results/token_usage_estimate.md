# Token Usage Estimate

Exact Responses token-count endpoint calls and model usage objects were not available because no API key/runtime usage object was exposed. This file uses local text-token heuristics plus an OpenAI-style high-detail image tiling estimate for each planned image payload.

| Document | Iteration | Call | Actor | Input expected | Cached input | Output expected | Image expected | Total low | Total expected | Total high |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 39 | 1 | main_agent_visual_orchestration | Main agent | 43890 | 0 | 4500 | 19890 | 28330 | 48390 | 61663 |
| 39 | 1 | round1_diego_high_recall | Diego | 10255 | 0 | 11500 | 9605 | 9915 | 21755 | 27787 |
| 39 | 1 | round1_jennifer_precision | Jennifer | 11355 | 0 | 5800 | 9605 | 6015 | 17155 | 22607 |
| 39 | 1 | round2_diego_saturation | Diego | 9775 | 0 | 300 | 8075 | 2475 | 10075 | 12734 |
| 39 | 1 | round2_jennifer_final | Jennifer | 10730 | 0 | 450 | 9180 | 2480 | 11180 | 14235 |
| 39 | 1 | **TOTAL** | all |  |  |  |  | **49215** | **108555** | **139026** |

Reasoning tokens: not available from the subagent tool responses.
Cached input tokens: recorded as 0 because cache accounting was not exposed.
