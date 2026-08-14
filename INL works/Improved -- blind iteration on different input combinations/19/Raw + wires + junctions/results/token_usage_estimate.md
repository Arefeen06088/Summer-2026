# Token Usage Estimate - Document 19, Iteration 1

No OpenAI API key was available, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 19 | 1 | Diego round 1 | Diego | 20987 | 0 | 17340 | 26000 | 8000 | 54987 |
| 19 | 1 | Jennifer round 1 | Jennifer | 43359 | 0 | 17340 | 25786 | 7000 | 76145 |
| 19 | 1 | Diego round 2 | Diego | 72791 | 46987 | 0 | 51 | 1500 | 74342 |
| 19 | 1 | Jennifer round 2 final | Jennifer | 69212 | 69145 | 0 | 44 | 3000 | 72256 |
| 19 | 1 | All rounds | Main Codex agent | 68444 | 0 | 12920 | 1800 | 4000 | 74244 |

Low total estimate: 173982

Expected total estimate: 351974

High total estimate: 782804
