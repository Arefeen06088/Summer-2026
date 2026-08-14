# Document 12 Token Usage Estimate

Actual Responses usage objects were not available from this local/subagent workflow, and no API key was available for the Responses input-token counting endpoint. The table below is therefore a reproducible local estimate.

- Expected input tokens: 53880
- Expected image/file input tokens: 38930
- Expected output tokens: 19300
- Expected total tokens: 73180
- Low / expected / high total: 59541 / 73180 / 91445

| Document | Iteration | Round | Call | Caller | Input expected | Image/file expected | Output expected | Total low | Total expected | Total high | Usage object |
|---|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 12 | 1 | setup | main-01 | Main | 3055 | 1105 | 1000 | 3204 | 4055 | 5159 | no |
| 12 | 1 | round01_diego | diego-01 | Diego | 16400 | 15300 | 8400 | 20110 | 24800 | 31150 | no |
| 12 | 1 | round01_jennifer | jennifer-01 | Jennifer | 17845 | 11220 | 7100 | 20013 | 24945 | 31480 | no |
| 12 | 1 | round02_diego | diego-02 | Diego | 5180 | 4505 | 900 | 5179 | 6080 | 7330 | no |
| 12 | 1 | round02_jennifer | jennifer-02 | Jennifer | 3750 | 3400 | 500 | 3665 | 4250 | 5073 | no |
| 12 | 1 | artifacts | main-02 | Main | 7650 | 3400 | 1400 | 7370 | 9050 | 11253 | no |

## Method

- Text input estimate: character count divided by 4.
- Image/file estimate: local high-detail 512-tile approximation for each attached PNG.
- Cached input tokens: not exposed by the tools here; totals assume 0 cached tokens.
- Reasoning tokens: not exposed.
- Output ranges: low/expected/high estimates because subagent and final output length is not known in advance by the local estimator.
