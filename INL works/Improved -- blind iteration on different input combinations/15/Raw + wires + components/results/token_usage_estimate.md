# Document 15 Token Usage Estimate

Actual Responses usage objects were not exposed by this local/subagent workflow, and no API key was available for the Responses input-token counting endpoint. This file is therefore a reproducible estimate.

## Grouped Total

| Document | Iteration | Input expected | Image/file expected | Output expected | Total low | Total expected | Total high |
|---|---:|---:|---:|---:|---:|---:|---:|
| 15 | 1 | 60361 | 38760 | 19400 | 64774 | 79761 | 99708 |

## Call Inventory

| Document | Iteration | Round | Call | Caller | Input low | Input expected | Input high | Cached input | Image/file expected | Output low | Output expected | Output high | Reasoning | Total low | Total expected | Total high | Usage object |
|---|---:|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| 15 | 1 | setup | main-01 | Main | 20942 | 23755 | 27756 | not exposed; assumed 0 in totals | 19380 | 780 | 1200 | 1740 | not exposed by local/subagent tools | 21722 | 24955 | 29496 | no |
| 15 | 1 | round01_diego | diego-01 | Diego | 6395 | 7250 | 8468 | not exposed; assumed 0 in totals | 5950 | 5785 | 8900 | 12905 | not exposed by local/subagent tools | 12180 | 16150 | 21373 | no |
| 15 | 1 | integration | main-02 | Main | 6315 | 7150 | 8343 | not exposed; assumed 0 in totals | 5950 | 390 | 600 | 870 | not exposed by local/subagent tools | 6705 | 7750 | 9213 | no |
| 15 | 1 | round01_jennifer | jennifer-01 | Jennifer | 14132 | 16730 | 20165 | not exposed; assumed 0 in totals | 7480 | 4810 | 7400 | 10730 | not exposed by local/subagent tools | 18942 | 24130 | 30895 | no |
| 15 | 1 | round02_diego | diego-02 | Diego | 270 | 338 | 423 | not exposed; assumed 0 in totals | 0 | 117 | 180 | 261 | not exposed by local/subagent tools | 387 | 518 | 684 | no |
| 15 | 1 | round02_jennifer | jennifer-02 | Jennifer | 110 | 138 | 173 | not exposed; assumed 0 in totals | 0 | 78 | 120 | 174 | not exposed by local/subagent tools | 188 | 258 | 347 | no |
| 15 | 1 | artifacts | main-03 | Main | 4000 | 5000 | 6250 | not exposed; assumed 0 in totals | 0 | 650 | 1000 | 1450 | not exposed by local/subagent tools | 4650 | 6000 | 7700 | no |

## Method

- Planned Responses input-token counting was not possible without an API key.
- Text input: estimated as character count divided by 4.
- Image/file input: estimated locally with the high-detail image formula: scale within 2048 px, short side to 768 px, then `85 + 170 * 512px tiles`.
- Cached input tokens and reasoning tokens were not exposed by the available tools; totals assume 0 cached tokens and do not separately account for hidden reasoning.
- Low/high ranges vary text inputs, image estimates, and unknown outputs to give the requested low / expected / high band.
