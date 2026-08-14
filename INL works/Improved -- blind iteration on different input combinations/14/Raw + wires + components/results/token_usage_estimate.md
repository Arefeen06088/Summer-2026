# Document 14 Token Usage Estimate

Actual Responses usage objects were not exposed by this local/subagent workflow, and no API key was available for the Responses input-token counting endpoint. This file is therefore a reproducible estimate.

## Grouped Total

| Document | Iteration | Input expected | Image/file expected | Output expected | Total low | Total expected | Total high |
|---|---:|---:|---:|---:|---:|---:|---:|
| 14 | 1 | 95275 | 62475 | 18260 | 94335 | 113535 | 139327 |

## Call Inventory

| Document | Iteration | Round | Call | Caller | Input low | Input expected | Input high | Cached input | Image/file expected | Output low | Output expected | Output high | Reasoning | Total low | Total expected | Total high | Usage object |
|---|---:|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| 14 | 1 | setup | main-01 | Main | 7200 | 9000 | 11250 | not exposed; assumed 0 in totals | 0 | 455 | 700 | 1015 | not exposed by local/subagent tools | 7655 | 9700 | 12265 | no |
| 14 | 1 | round01_diego | diego-01 | Diego | 22261 | 24915 | 28815 | not exposed; assumed 0 in totals | 23290 | 5655 | 8700 | 12615 | not exposed by local/subagent tools | 27916 | 33615 | 41430 | no |
| 14 | 1 | round01_jennifer | jennifer-01 | Jennifer | 22365 | 25725 | 30372 | not exposed; assumed 0 in totals | 17850 | 4485 | 6900 | 10005 | not exposed by local/subagent tools | 26850 | 32625 | 40377 | no |
| 14 | 1 | integration | main-02 | Main | 14034 | 15885 | 18531 | not exposed; assumed 0 in totals | 13260 | 422 | 650 | 943 | not exposed by local/subagent tools | 14456 | 16535 | 19474 | no |
| 14 | 1 | round02_diego | diego-02 | Diego | 12067 | 14075 | 16787 | not exposed; assumed 0 in totals | 8075 | 117 | 180 | 261 | not exposed by local/subagent tools | 12184 | 14255 | 17048 | no |
| 14 | 1 | round02_jennifer | jennifer-02 | Jennifer | 140 | 175 | 219 | not exposed; assumed 0 in totals | 0 | 84 | 130 | 189 | not exposed by local/subagent tools | 224 | 305 | 408 | no |
| 14 | 1 | artifacts | main-03 | Main | 4400 | 5500 | 6875 | not exposed; assumed 0 in totals | 0 | 650 | 1000 | 1450 | not exposed by local/subagent tools | 5050 | 6500 | 8325 | no |

## Method

- Planned Responses input-token counting was not possible without an API key.
- Text input: estimated as character count divided by 4.
- Image/file input: estimated locally with the high-detail image formula: scale within 2048 px, short side to 768 px, then `85 + 170 * 512px tiles`.
- Cached input tokens and reasoning tokens were not exposed by the available tools; totals assume 0 cached tokens and do not separately account for hidden reasoning.
- Low/high ranges vary text inputs, image estimates, and unknown outputs to give the requested low / expected / high band.
