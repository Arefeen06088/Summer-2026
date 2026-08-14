# Document 13 Token Usage Estimate

Actual Responses usage objects were not available from this local/subagent workflow, and no API key was available for the Responses input-token counting endpoint. The table below is therefore a reproducible local estimate.

- Expected input tokens: 78005
- Expected image/file input tokens: 63155
- Expected output tokens: 18300
- Expected total tokens: 96305
- Low / expected / high total: 80611 / 96305 / 117730

| Document | Iteration | Round | Call | Caller | Input expected | Image/file expected | Output expected | Total low | Total expected | Total high | Usage object |
|---|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 13 | 1 | setup | main-01 | Main | 4510 | 2210 | 1100 | 4544 | 5610 | 7012 | no |
| 13 | 1 | round01_diego | diego-01 | Diego | 21275 | 19975 | 7400 | 23827 | 28675 | 35327 | no |
| 13 | 1 | round01_jennifer | jennifer-01 | Jennifer | 25675 | 19975 | 6800 | 26957 | 32475 | 39957 | no |
| 13 | 1 | round02_diego | diego-02 | Diego | 12275 | 11475 | 950 | 11584 | 13225 | 15575 | no |
| 13 | 1 | round02_jennifer | jennifer-02 | Jennifer | 3350 | 2975 | 550 | 3334 | 3900 | 4688 | no |
| 13 | 1 | artifacts | main-02 | Main | 10920 | 6545 | 1500 | 10365 | 12420 | 15171 | no |

## Method

- Text input estimate: character count divided by 4.
- Image/file estimate: local high-detail 512-tile approximation for each attached PNG.
- Cached input tokens: not exposed by the tools here; totals assume 0 cached tokens.
- Reasoning tokens: not exposed.
- Output ranges: low/expected/high estimates because subagent and final output length is not known in advance by the local estimator.
