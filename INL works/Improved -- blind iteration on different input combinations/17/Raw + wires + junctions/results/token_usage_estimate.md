# Token Usage Estimate - Document 17, Iteration 1

No OpenAI API key was available, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 17 | 1 | Diego round 1 | Diego | 16865 | 0 | 15045 | 25407 | 8000 | 50272 |
| 17 | 1 | Jennifer round 1 | Jennifer | 40471 | 0 | 15045 | 25167 | 7000 | 72638 |
| 17 | 1 | Diego round 2 | Diego | 67457 | 42272 | 0 | 43 | 1500 | 69000 |
| 17 | 1 | Jennifer round 2 final | Jennifer | 65697 | 65638 | 0 | 44 | 3000 | 68741 |
| 17 | 1 | All rounds | Main Codex agent | 58767 | 0 | 6290 | 1800 | 4000 | 64567 |

Low total estimate: 165648

Expected total estimate: 325218

High total estimate: 424378
