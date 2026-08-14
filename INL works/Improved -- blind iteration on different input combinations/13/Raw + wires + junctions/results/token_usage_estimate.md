# Token Usage Estimate - Document 13, Iteration 1

No OpenAI API key was available, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 13 | 1 | Diego round 1 | Diego | 23979 | 0 | 18955 | 25232 | 8000 | 57211 |
| 13 | 1 | Jennifer round 1 | Jennifer | 44206 | 0 | 18955 | 25031 | 7000 | 76237 |
| 13 | 1 | Diego round 2 | Diego | 74260 | 49211 | 0 | 80 | 1500 | 75840 |
| 13 | 1 | Jennifer round 2 final | Jennifer | 69333 | 69237 | 0 | 51 | 3000 | 72384 |
| 13 | 1 | All rounds | Main Codex agent | 62299 | 0 | 6885 | 1800 | 4000 | 68099 |

Low total estimate: 172693

Expected total estimate: 349771

High total estimate: 687101
