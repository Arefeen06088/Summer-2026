# Token Usage Estimate - Document 20, Iteration 1

No OpenAI API key was available, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 20 | 1 | Diego round 1 | Diego | 22597 | 0 | 19125 | 25969 | 8000 | 56566 |
| 20 | 1 | Jennifer round 1 | Jennifer | 45113 | 0 | 19125 | 25937 | 7000 | 78050 |
| 20 | 1 | Diego round 2 | Diego | 74525 | 48566 | 0 | 53 | 1500 | 76078 |
| 20 | 1 | Jennifer round 2 final | Jennifer | 71122 | 71050 | 0 | 44 | 3000 | 74166 |
| 20 | 1 | All rounds | Main Codex agent | 69496 | 0 | 14025 | 1800 | 4000 | 75296 |

Low total estimate: 174260

Expected total estimate: 360156

High total estimate: 533436
