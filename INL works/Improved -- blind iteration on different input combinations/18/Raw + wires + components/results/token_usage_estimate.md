# Token Usage Estimate - Document 18

No OpenAI API key was available, so the Responses input-token counting endpoint and final usage objects could not be queried. Text tokens were estimated by local character/count heuristics; image tokens were estimated with a high-detail 512-tile method after downscaling large images. Cached input and reasoning tokens are therefore marked unavailable.

| document | iteration | call | actor | input text est | cached input | output est | reasoning | image/file input est | low total | expected total | high total | note |
|---|---:|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| 18 | 1 | main orchestration/artifact generation | main | 9000 | 0 | 900 | n/a | 2500 | 12400 | 16000 | 19500 | No API usage object exposed |
| 18 | 1 | Diego R1 high-recall extraction | subagent Diego | 2600 | 0 | 7200 | n/a | 7140 | 14500 | 17800 | 22500 | Actual subagent text returned; usage object unavailable |
| 18 | 1 | Jennifer R1 precision review | subagent Jennifer/current reviewer | 9800 | 0 | 5200 | n/a | 7480 | 17100 | 21100 | 26800 | Estimated from Diego R1 text plus attached crops |
| 18 | 1 | Diego R2 saturation check | subagent Diego | 4200 | 0 | 900 | n/a | 0 | 4300 | 5100 | 6800 | Planned text-only convergence pass |
| 18 | 1 | Jennifer R2 final signoff | subagent Jennifer | 2600 | 0 | 600 | n/a | 0 | 2600 | 3200 | 4600 | Planned text-only signoff |

Expected total tokens: 63200

Low / expected / high total: 50900 / 63200 / 80200
