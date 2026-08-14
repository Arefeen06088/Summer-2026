# Token Usage Estimate - Document 14, Iteration 1

No OpenAI API key was available, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 14 | 1 | Diego round 1 | Diego | 16460 | 0 | 13005 | 25008 | 8000 | 49468 |
| 14 | 1 | Jennifer round 1 | Jennifer | 38032 | 0 | 13005 | 24545 | 7000 | 69577 |
| 14 | 1 | Diego round 2 | Diego | 66031 | 41468 | 0 | 85 | 1500 | 67616 |
| 14 | 1 | Jennifer round 2 final | Jennifer | 62678 | 62577 | 0 | 51 | 3000 | 65729 |
| 14 | 1 | All rounds | Main Codex agent | 58665 | 0 | 5525 | 1800 | 4000 | 64465 |

Low total estimate: 165910

Expected total estimate: 316855

High total estimate: 757545
