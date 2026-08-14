# Token Usage Estimate

No OpenAI API key was available, so the Responses input-token counting endpoint and model usage objects could not be collected. Image input tokens are estimated with a local high-detail tile heuristic: 85 base tokens plus 170 tokens per 512 px tile. Text tokens are estimated from prompt sizes and transcript volume.

| Document | Iteration | Model call | Text input | Image/file input | Cached input | Expected output | Reasoning | Low total | Expected total | High total |
|---|---:|---|---:|---:|---:|---:|---|---:|---:|---:|
| 17 | 1 | main setup/resource inspection | 1800 | 0 | 0 | 500 | n/a | 2400 | 2300 | 3000 |
| 17 | 1 | Diego R1 extraction | 3200 | 30600 | 0 | 8500 | n/a | 38800 | 42300 | 44300 |
| 17 | 1 | Jennifer R1 precision review | 11800 | 19550 | 0 | 5200 | n/a | 34850 | 36550 | 38350 |
| 17 | 1 | main integration/artifact planning | 5200 | 0 | 0 | 1000 | n/a | 6100 | 6200 | 7200 |
| 17 | 1 | Diego R2 revision after corrections | 4600 | 3995 | 0 | 900 | n/a | 9095 | 9495 | 10095 |
| 17 | 1 | Jennifer R2 final saturation | 2500 | 3995 | 0 | 300 | n/a | 6645 | 6795 | 7195 |
| 17 | 1 | main final report | 2200 | 0 | 0 | 700 | n/a | 2700 | 2900 | 3400 |
| **17** | **1** | **Total** |  |  |  |  |  | **100590** | **106540** | **113540** |

Actual usage object fields are unavailable in this environment. Cached input and reasoning-token values are therefore reported as 0/n/a rather than guessed.
