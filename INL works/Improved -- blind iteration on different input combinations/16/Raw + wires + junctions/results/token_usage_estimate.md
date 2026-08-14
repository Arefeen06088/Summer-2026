# Token Usage Estimate - Document 16, Iteration 1

No OpenAI API key was available, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 16 | 1 | Diego round 1 | Diego | 19405 | 0 | 15385 | 21940 | 8000 | 49345 |
| 16 | 1 | Jennifer round 1 | Jennifer | 37344 | 0 | 15385 | 21316 | 7000 | 65660 |
| 16 | 1 | Diego round 2 | Diego | 62679 | 41345 | 0 | 59 | 1500 | 64238 |
| 16 | 1 | Jennifer round 2 final | Jennifer | 58735 | 58660 | 0 | 51 | 3000 | 61786 |
| 16 | 1 | All rounds | Main Codex agent | 56562 | 0 | 9180 | 1800 | 4000 | 62362 |

Low total estimate: 148326

Expected total estimate: 303391

High total estimate: 363791
