# Token Usage Estimate - Document 25, Iteration 1

No OpenAI API key was available, the Responses input-token counting endpoint could not be called, and the multi-agent tool did not expose usage objects. Text tokens were estimated locally with tiktoken when available, otherwise len(text)/4. Image/file input tokens use low thumbnail, expected high-detail tile, and high no-resize tile estimates.

| Document | Iteration | Round | Agent | Input expected | Cached expected | Image expected | Output expected | Reasoning expected | Total expected |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 25 | 1 | Setup and visual inspection | Main Codex agent | 14741 | 0 | 11730 | 1500 | 5000 | 21241 |
| 25 | 1 | Diego round 1 | Diego | 18063 | 0 | 15045 | 26597 | 8000 | 52660 |
| 25 | 1 | Jennifer round 1 | Jennifer | 44644 | 0 | 15045 | 25490 | 7000 | 77134 |
| 25 | 1 | Diego round 2 | Diego | 78586 | 44660 | 8415 | 25509 | 1500 | 105595 |
| 25 | 1 | Jennifer round 2 final | Jennifer | 104076 | 70134 | 8415 | 25490 | 3000 | 132566 |
| 25 | 1 | Generation and validation | Main Codex agent | 103110 | 0 | 0 | 1800 | 4000 | 108910 |

Low total estimate: 290451

Expected total estimate: 498106

High total estimate: 922835
