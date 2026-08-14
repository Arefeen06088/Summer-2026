# Token Usage Estimate - Document 22, Iteration 1

No OpenAI API key was available, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 22 | 1 | Diego round 1 | Diego | 30847 | 0 | 23630 | 25608 | 8000 | 64455 |
| 22 | 1 | Jennifer round 1 | Jennifer | 49257 | 0 | 23630 | 25379 | 7000 | 81636 |
| 22 | 1 | Diego round 2 | Diego | 84831 | 56455 | 2975 | 69 | 1500 | 86400 |
| 22 | 1 | Jennifer round 2 final | Jennifer | 76594 | 74636 | 1870 | 68 | 3000 | 79662 |
| 22 | 1 | All rounds | Main Codex agent | 77972 | 0 | 19635 | 1800 | 4000 | 83772 |

Low total estimate: 180874

Expected total estimate: 395925

High total estimate: 828285
