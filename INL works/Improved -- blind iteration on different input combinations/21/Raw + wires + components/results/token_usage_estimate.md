# Token Usage Estimate

No API key was available, so the Responses input-token counting endpoint could not be called and subagent usage objects were not exposed by the local tool interface.
Estimates use text characters/4 plus an image 512-tile heuristic from the actual crop dimensions.

| Document | Iteration | Call | Text In | Image/File In | Cached In | Output | Reasoning | Low | Expected | High |
|---:|---:|---|---:|---:|---|---:|---|---:|---:|---:|
| 21 | 1 | main_visual_inspection | 1625 | 34595 | not_available | 2800 | not_available | 30435 | 39020 | 52677 |
| 21 | 1 | diego_round_1 | 475 | 32555 | not_available | 7200 | not_available | 31379 | 40230 | 54311 |
| 21 | 1 | jennifer_round_1 | 825 | 29580 | not_available | 2800 | not_available | 25899 | 33205 | 44827 |
| 21 | 1 | diego_round_2 | 238 | 12410 | not_available | 950 | not_available | 10606 | 13598 | 18358 |
| 21 | 1 | jennifer_round_2 | 213 | 12410 | not_available | 420 | not_available | 10173 | 13043 | 17609 |
| 21 | 1 | main_artifact_generation_final | 1800 | 0 | not_available | 1600 | not_available | 2652 | 3400 | 4590 |

Total low / expected / high: 111144 / 142496 / 192372 tokens.
