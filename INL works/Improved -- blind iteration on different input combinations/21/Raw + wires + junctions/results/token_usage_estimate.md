# Token Usage Estimate - Document 21, Iteration 1

No OpenAI API key was available, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 21 | 1 | Diego round 1 initial incomplete attempt | Diego | 23439 | 0 | 18445 | 20 | 4000 | 27459 |
| 21 | 1 | Diego round 1 | Diego | 23437 | 0 | 18445 | 24279 | 8000 | 55716 |
| 21 | 1 | Jennifer round 1 | Jennifer | 42743 | 0 | 18445 | 24312 | 7000 | 74055 |
| 21 | 1 | Diego round 2 | Diego | 72050 | 47716 | 0 | 43 | 1500 | 73593 |
| 21 | 1 | Jennifer round 2 final | Jennifer | 67117 | 67055 | 0 | 40 | 3000 | 70157 |
| 21 | 1 | All rounds | Main Codex agent | 67007 | 0 | 13345 | 1800 | 4000 | 72807 |

Low total estimate: 174776

Expected total estimate: 373787

High total estimate: 768927
