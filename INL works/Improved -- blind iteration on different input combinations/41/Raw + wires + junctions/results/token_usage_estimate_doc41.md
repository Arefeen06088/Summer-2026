# Document 41 Token Usage Estimate

No API key or subagent usage objects were available, so these are local estimates.
Text tokens use tiktoken when installed, otherwise character/4. Image tokens use a high-detail tile estimate.

| document | iteration | call | agent | expected input | expected image/file input | expected output | expected total |
|---|---:|---|---|---:|---:|---:|---:|
| 41 | 1 | main_doc41_orchestration | main | 7447 | 7055 | 1800 | 9247 |
| 41 | 1 | diego_round1 | Diego | 7101 | 7055 | 2113 | 9214 |
| 41 | 1 | jennifer_round1 | Jennifer | 9214 | 7055 | 2095 | 11309 |
| 41 | 1 | diego_round2 | Diego | 9196 | 7055 | 2144 | 11340 |
| 41 | 1 | jennifer_round2_final | Jennifer | 9245 | 7055 | 1962 | 11207 |

Expected total tokens across listed calls: 52317
