# Token Usage Estimate - Document 15, Iteration 1

No OpenAI API key was available, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 15 | 1 | Diego round 1 | Diego | 23207 | 0 | 19295 | 25393 | 8000 | 56600 |
| 15 | 1 | Jennifer round 1 | Jennifer | 44707 | 0 | 19295 | 25057 | 7000 | 76764 |
| 15 | 1 | Diego round 2 | Diego | 73675 | 48600 | 0 | 72 | 1500 | 75247 |
| 15 | 1 | Jennifer round 2 final | Jennifer | 69852 | 69764 | 0 | 82 | 3000 | 72934 |
| 15 | 1 | All rounds | Main Codex agent | 59697 | 0 | 5185 | 1800 | 4000 | 65497 |

Low total estimate: 170558

Expected total estimate: 347042

High total estimate: 853862
