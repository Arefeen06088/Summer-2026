# Document 6 Token Usage Estimate

No API key or subagent usage objects were available, so these are local estimates.
Text tokens use tiktoken when installed, otherwise character/4. Image tokens use a high-detail tile estimate.

| document | iteration | call | agent | expected input | expected image/file input | expected output | expected total |
|---|---:|---|---|---:|---:|---:|---:|
| 6 | 1 | main_doc6_orchestration | main | 13206 | 12580 | 1800 | 15006 |
| 6 | 1 | diego_round1 | Diego | 12626 | 12580 | 4539 | 17165 |
| 6 | 1 | jennifer_round1 | Jennifer | 17165 | 12580 | 3846 | 21011 |
| 6 | 1 | diego_round2 | Diego | 16472 | 12580 | 3363 | 19835 |
| 6 | 1 | jennifer_round2_final | Jennifer | 15989 | 12580 | 3356 | 19345 |

Expected total tokens across listed calls: 92362
