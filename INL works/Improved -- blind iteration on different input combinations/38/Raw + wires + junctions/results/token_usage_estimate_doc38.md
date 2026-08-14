# Document 38 Token Usage Estimate

No API key or subagent usage objects were available, so these are local estimates.
Text tokens use tiktoken when installed, otherwise character/4. Image tokens use a high-detail tile estimate.

| document | iteration | call | agent | expected input | expected image/file input | expected output | expected total |
|---|---:|---|---|---:|---:|---:|---:|
| 38 | 1 | main_doc38_orchestration | main | 8810 | 8415 | 1800 | 10610 |
| 38 | 1 | diego_round1 | Diego | 8461 | 8415 | 2108 | 10569 |
| 38 | 1 | jennifer_round1 | Jennifer | 10569 | 8415 | 1951 | 12520 |
| 38 | 1 | diego_round2 | Diego | 10412 | 8415 | 1997 | 12409 |
| 38 | 1 | jennifer_round2_final | Jennifer | 10458 | 8415 | 1911 | 12369 |

Expected total tokens across listed calls: 58477
