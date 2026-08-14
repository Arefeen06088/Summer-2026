# Token Usage Estimates

OpenAI Responses input-token counting endpoint was not called because no API key is available.
The local estimate uses text characters / 4 plus a high-detail image tile estimate from image dimensions.
Actual cached input tokens, usage objects, and reasoning tokens were not exposed by the local subagent tools.

| Document | Iteration | Call | Actor | Input Est | Image/File Est | Output Est | Low | Expected | High |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 22 | 1 | doc22-main-aggregate | Main agent | 38958 | 35445 | 3000 | 33567 | 41958 | 52448 |
| 22 | 1 | doc22-r1-diego | Diego | 9387 | 9350 | 4300 | 10950 | 13687 | 17109 |
| 22 | 1 | doc22-r2-jennifer | Jennifer | 12649 | 9010 | 3300 | 12760 | 15949 | 19937 |
| 22 | 1 | doc22-r3-diego | Diego | 1334 | 0 | 500 | 1468 | 1834 | 2293 |
| 22 | 1 | doc22-r4-jennifer | Jennifer | 387 | 0 | 350 | 590 | 737 | 922 |
| 22 | 1 | TOTAL | all | 62715 | 53805 | 11450 | 59335 | 74165 | 92709 |
