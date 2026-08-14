# Token Usage Estimate - Document 18, Iteration 1

No OpenAI API key was available, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 18 | 1 | Diego round 1 | Diego | 23196 | 0 | 18275 | 25625 | 8000 | 56821 |
| 18 | 1 | Jennifer round 1 | Jennifer | 43919 | 0 | 18275 | 25270 | 7000 | 76189 |
| 18 | 1 | Diego round 2 | Diego | 74109 | 48821 | 0 | 46 | 1500 | 75655 |
| 18 | 1 | Jennifer round 2 final | Jennifer | 69251 | 69189 | 0 | 51 | 3000 | 72302 |
| 18 | 1 | All rounds | Main Codex agent | 61434 | 0 | 5525 | 1800 | 4000 | 67234 |

Low total estimate: 173091

Expected total estimate: 348201

High total estimate: 473031
