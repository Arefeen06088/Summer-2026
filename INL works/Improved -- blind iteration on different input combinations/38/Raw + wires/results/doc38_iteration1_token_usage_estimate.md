# Token Usage Estimate - Document 38 Iteration 1

Exact OpenAI usage objects and the Responses input-token counting endpoint were not available in this environment because no API key was provided/exposed.
Text estimates use local token-count approximation; image/file estimates use a documented high-detail image tiling approximation (85 base tokens plus 170 tokens per 512 px tile after max-side scaling).

| Document | Iteration | Call | Role | Input | Image/File | Output Low | Output Expected | Output High | Expected Total |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| 38 | 1 | main_orchestration_doc38 | main agent | 6500 | 0 | 900 | 1600 | 2600 | 8100 |
| 38 | 1 | Diego_R1_high_recall_extraction | Diego | 2400 | 85170 | 5000 | 6800 | 9000 | 94370 |
| 38 | 1 | Jennifer_R1_precision_review | Jennifer | 3600 | 85255 | 4500 | 6200 | 8500 | 95055 |
| 38 | 1 | Diego_R2_reconciliation | Diego | 2700 | 65535 | 1700 | 2600 | 3900 | 70835 |
| 38 | 1 | Jennifer_R2_final_confirmation | Jennifer | 2300 | 37740 | 900 | 1500 | 2600 | 41540 |

Expected total estimate: 309900
Low total estimate: 304200
High total estimate: 317800
