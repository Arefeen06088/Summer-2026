# Token Usage Estimate

Document: 20
Iteration: 1

The OpenAI Responses input-token counting endpoint and per-response usage objects could not be used because no API key is available in this environment. A local estimate was used instead: text input is approximated as characters/4, and image/file input is approximated with a high-detail tile-style visual payload heuristic from the images/crops supplied to each model call.

| Document | Iteration | Call | Actor | Phase | Text input est | Cached input | Image/file input est | Output est | Reasoning tokens | Low total | Expected total | High total | Usage object |
|---:|---:|---|---|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| 20 | 1 | main-01 | Main agent | Resource inspection, visual crops, and local visual tracing | 6500 | 0 | 42000 | 3800 | unavailable | 40000 | 52300 | 68000 | not exposed |
| 20 | 1 | diego-r1 | Diego | Round 1 high-recall extraction | 3500 | 0 | 31500 | 15500 | unavailable | 41000 | 50500 | 64000 | not exposed |
| 20 | 1 | jennifer-r1 | Jennifer | Round 1 precision review | 20000 | 0 | 35000 | 14000 | unavailable | 56000 | 69000 | 88000 | not exposed |
| 20 | 1 | diego-r2a | Diego | Round 2 initial saturation prompt superseded by tighter crop | 1400 | 0 | 0 | 0 | unavailable | 900 | 1400 | 2200 | not exposed |
| 20 | 1 | diego-r2b | Diego | Round 2 corrected saturation check | 1200 | 0 | 5500 | 120 | unavailable | 5000 | 6820 | 9000 | not exposed |
| 20 | 1 | jennifer-r2 | Jennifer | Round 2 final signoff | 1500 | 0 | 5500 | 40 | unavailable | 5200 | 7040 | 9500 | not exposed |
| 20 | 1 | main-02 | Main agent | Artifact generation, validation, and final response | 6000 | 0 | 0 | 1200 | unavailable | 5500 | 7200 | 9500 | not exposed |

| Document | Iteration | Low total | Expected total | High total |
|---:|---:|---:|---:|---:|
| 20 | 1 | 153600 | 194260 | 250200 |

Low / expected / high bounds are provided because exact output length, hidden reasoning effort, caching behavior, and image-token accounting are unavailable without API usage metadata.
