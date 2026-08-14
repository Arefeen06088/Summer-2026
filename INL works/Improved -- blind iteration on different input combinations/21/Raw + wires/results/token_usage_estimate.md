# Document 21 Token Usage Estimate

No `OPENAI_API_KEY` was available, so exact usage objects and the Responses input-token counting endpoint were unavailable.
Text estimates use `tiktoken` when installed; image estimates use the high-detail 512px-tile heuristic.

| Document | Iteration | Model call | Input est | Cached | Image/file est | Output low | Output expected | Output high | Reasoning | Expected total |
|---|---:|---|---:|---|---:|---:|---:|---:|---|---:|
| 21 | 1 | Main Codex orchestration and crop generation | 12031 | unavailable | 0 | 1500 | 3000 | 6000 | unavailable | 15031 |
| 21 | 1 | Diego R1 high-recall extractor | 5022 | unavailable | 51255 | 4000 | 7500 | 12000 | unavailable | 63777 |
| 21 | 1 | Jennifer R1 precision reviewer | 7522 | unavailable | 43605 | 1500 | 3000 | 6000 | unavailable | 54127 |
| 21 | 1 | Diego R2 saturation check | 1716 | unavailable | 0 | 150 | 500 | 1200 | unavailable | 2216 |
| 21 | 1 | Jennifer R2 final confirmation | 917 | unavailable | 0 | 100 | 250 | 800 | unavailable | 1167 |
| 21 | 1 | Main Codex artifact finalization | 3500 | unavailable | 0 | 500 | 1200 | 2500 | unavailable | 4700 |

Low estimate: 133318
Expected estimate: 141018
High estimate: 154068
