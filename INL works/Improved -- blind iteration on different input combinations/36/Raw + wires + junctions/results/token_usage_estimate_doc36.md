# Document 36 Token Usage Estimate

No API key or subagent usage objects were available, so these are local estimates.
Text tokens use tiktoken when installed, otherwise character/4. Image tokens use a high-detail tile estimate.

| document | iteration | call | agent | expected input | expected image/file input | expected output | expected total |
|---|---:|---|---|---:|---:|---:|---:|
| 36 | 1 | main_doc36_orchestration | main | 10005 | 8755 | 1600 | 11605 |
| 36 | 1 | diego_round1 | Diego | 11029 | 10965 | 2711 | 13740 |
| 36 | 1 | jennifer_round1 | Jennifer | 13740 | 10965 | 2639 | 16379 |
| 36 | 1 | diego_round2 | Diego | 13668 | 10965 | 2463 | 16131 |
| 36 | 1 | jennifer_round2_final | Jennifer | 13492 | 10965 | 2581 | 16073 |

Expected total tokens across listed calls: 73928
