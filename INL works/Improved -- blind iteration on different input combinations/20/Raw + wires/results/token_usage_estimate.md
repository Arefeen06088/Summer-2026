# Document 20 Token Usage Estimate

No `OPENAI_API_KEY` or `OPENAI_BASE_URL` was present in the shell, so the OpenAI Responses input-token counting endpoint and actual response usage objects were not available.
Text token estimates use `tiktoken` with `o200k_base`; image/file token estimates use the high-detail 512px tile heuristic.

| Document | Iteration | Model call | Input est | Cached | Image/file est | Output low | Output expected | Output high | Reasoning | Expected total |
|---|---:|---|---:|---|---:|---:|---:|---:|---|---:|
| 20 | 1 | main-agent orchestration | 112 | unavailable | 0 | 1200 | 2500 | 4500 | unavailable | 2612 |
| 20 | 1 | Diego R1 high-recall extractor | 112 | unavailable | 18020 | 7000 | 12000 | 18000 | unavailable | 30132 |
| 20 | 1 | Jennifer R1 precision reviewer | 6612 | unavailable | 18020 | 700 | 1500 | 3500 | unavailable | 26132 |
| 20 | 1 | Diego R2 saturation response | 650 | unavailable | 0 | 150 | 350 | 900 | unavailable | 1000 |
| 20 | 1 | Jennifer R2 final confirmation | 650 | unavailable | 0 | 100 | 250 | 800 | unavailable | 900 |

Expected total estimate: 60776
Low estimate: 53326
High estimate: 71876
