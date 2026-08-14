# Document 40 Token Usage Estimate

No API key or subagent usage objects were available, so these are local estimates.
Text tokens use tiktoken when installed, otherwise character/4. Image tokens use a high-detail tile estimate.

| document | iteration | call | agent | expected input | expected image/file input | expected output | expected total |
|---|---:|---|---|---:|---:|---:|---:|
| 40 | 1 | main_doc40_orchestration | main | 7447 | 7055 | 1800 | 9247 |
| 40 | 1 | diego_round1 | Diego | 7101 | 7055 | 2371 | 9472 |
| 40 | 1 | jennifer_round1 | Jennifer | 9472 | 7055 | 2342 | 11814 |
| 40 | 1 | diego_round2 | Diego | 9443 | 7055 | 2088 | 11531 |
| 40 | 1 | jennifer_round2_final | Jennifer | 9189 | 7055 | 1997 | 11186 |

Expected total tokens across listed calls: 53250
