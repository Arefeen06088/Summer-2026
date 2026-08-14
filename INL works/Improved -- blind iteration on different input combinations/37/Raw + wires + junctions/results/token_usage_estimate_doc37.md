# Document 37 Token Usage Estimate

No API key or subagent usage objects were available, so these are local estimates.
Text tokens use tiktoken when installed, otherwise character/4. Image tokens use a high-detail tile estimate.

| document | iteration | call | agent | expected input | expected image/file input | expected output | expected total |
|---|---:|---|---|---:|---:|---:|---:|
| 37 | 1 | main_doc37_orchestration | main | 8338 | 7395 | 1800 | 10138 |
| 37 | 1 | diego_round1 | Diego | 11886 | 11815 | 2083 | 13969 |
| 37 | 1 | jennifer_round1 | Jennifer | 13969 | 11815 | 2079 | 16048 |
| 37 | 1 | diego_round2 | Diego | 13965 | 11815 | 1951 | 15916 |
| 37 | 1 | jennifer_round2_final | Jennifer | 13837 | 11815 | 1965 | 15802 |

Expected total tokens across listed calls: 71873
