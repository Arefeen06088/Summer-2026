# Token Usage Estimate

Document: 19
Iteration: 1

The OpenAI Responses input-token counting endpoint and per-response usage objects could not be used because no API key is available in this environment. The estimates below use a local heuristic: text input is estimated at roughly 4 characters per token, and image/file input is estimated with a high-detail tile-style visual payload heuristic from the viewed images/crops.

| Document | Iteration | Call | Actor | Phase | Text input est | Cached input | Image/file input est | Output est | Reasoning tokens | Low total | Expected total | High total | Usage object |
|---:|---:|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| 19 | 1 | main-01 | Main agent | Resource inspection and crop planning | 4500 | 0 | 16000 | 900 | unavailable | 18000 | 21400 | 27000 | not exposed |
| 19 | 1 | diego-r1 | Diego | Round 1 high-recall extraction | 3200 | 0 | 23800 | 12500 | unavailable | 33000 | 39500 | 49000 | not exposed |
| 19 | 1 | jennifer-r1 | Jennifer | Round 1 precision review | 15600 | 0 | 23800 | 10500 | unavailable | 42000 | 49900 | 62000 | not exposed |
| 19 | 1 | diego-r2 | Diego | Round 2 saturation check | 2700 | 0 | 0 | 550 | unavailable | 2000 | 3250 | 4200 | not exposed |
| 19 | 1 | jennifer-r2 | Jennifer | Round 2 final signoff | 1800 | 0 | 0 | 250 | unavailable | 1600 | 2050 | 3000 | not exposed |
| 19 | 1 | main-02 | Main agent | Artifact generation, validation, and final response | 5200 | 0 | 0 | 1000 | unavailable | 4800 | 6200 | 8000 | not exposed |

| Document | Iteration | Low total | Expected total | High total |
|---:|---:|---:|---:|---:|
| 19 | 1 | 101400 | 122300 | 153200 |

Low / expected / high bounds are provided because output length, hidden reasoning effort, and exact image-token accounting are not available without API usage metadata.
