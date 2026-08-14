# Document 27 Token Usage Estimate

No API key or subagent usage objects were available, so these are local estimates.
Text tokens use tiktoken when installed, otherwise character/4. Image tokens use a high-detail tile estimate.

| document | iteration | call | agent | expected input | expected image/file input | expected output | expected total |
|---|---:|---|---|---:|---:|---:|---:|
| 27 | 1 | main_doc27_orchestration | main | 11878 | 9350 | 1800 | 13678 |
| 27 | 1 | diego_round1 | Diego | 7200 | 7140 | 5681 | 12881 |
| 27 | 1 | jennifer_round1 | Jennifer | 12881 | 7140 | 5299 | 18180 |
| 27 | 1 | diego_round2 | Diego | 12499 | 7140 | 5046 | 17545 |
| 27 | 1 | jennifer_round2_final | Jennifer | 12246 | 7140 | 5140 | 17386 |

Expected total tokens across listed calls: 79670
