# Document 11 Token Usage Estimate

Actual Responses usage objects were not available from this local/subagent workflow, and no API key was available for the Responses input-token counting endpoint. The table below is therefore a reproducible local estimate.

- Expected input tokens: 73075
- Expected image/file input tokens: 57800
- Expected output tokens: 13450
- Expected total tokens: 86525
- Low / expected / high total: 72981 / 86525 / 105068

| Document | Iteration | Round | Call | Caller | Input expected | Image/file expected | Output expected | Total low | Total expected | Total high | Usage object |
|---|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 11 | 1 | setup | main-01 | Main | 1750 | 0 | 900 | 1985 | 2650 | 3493 | no |
| 11 | 1 | round01_diego | diego-01 | Diego | 21500 | 19125 | 5300 | 22557 | 26800 | 32648 | no |
| 11 | 1 | round01_jennifer | jennifer-01 | Jennifer | 20960 | 14960 | 4200 | 20994 | 25160 | 30794 | no |
| 11 | 1 | round02_diego | diego-02 | Diego | 11320 | 10370 | 900 | 10678 | 12220 | 14418 | no |
| 11 | 1 | round02_jennifer | jennifer-02 | Jennifer | 9625 | 8925 | 750 | 9079 | 10375 | 12227 | no |
| 11 | 1 | artifacts | main-02 | Main | 7920 | 4420 | 1400 | 7688 | 9320 | 11488 | no |

## Method

- Text input estimate: character count divided by 4.
- Image/file estimate: local high-detail 512-tile approximation for each attached PNG.
- Cached input tokens: not exposed by the tools here; totals assume 0 cached tokens.
- Reasoning tokens: not exposed.
- Output ranges: low/expected/high estimates because subagent and final output length is not known in advance by the local estimator.
