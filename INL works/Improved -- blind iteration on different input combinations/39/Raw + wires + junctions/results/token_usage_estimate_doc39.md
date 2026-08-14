# Document 39 Token Usage Estimate

No API key or subagent usage objects were available, so these are local estimates.
Text tokens use tiktoken when installed, otherwise character/4. Image tokens use a high-detail tile estimate.

| document | iteration | call | agent | expected input | expected image/file input | expected output | expected total |
|---|---:|---|---|---:|---:|---:|---:|
| 39 | 1 | main_doc39_orchestration | main | 7107 | 6715 | 1800 | 8907 |
| 39 | 1 | diego_round1 | Diego | 6761 | 6715 | 2023 | 8784 |
| 39 | 1 | jennifer_round1 | Jennifer | 8784 | 6715 | 2120 | 10904 |
| 39 | 1 | diego_round2 | Diego | 8881 | 6715 | 1933 | 10814 |
| 39 | 1 | jennifer_round2_final | Jennifer | 8694 | 6715 | 1891 | 10585 |

Expected total tokens across listed calls: 49994
