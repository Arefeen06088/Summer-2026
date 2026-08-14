# Document 37 Iteration 1 Token Usage Estimate

Exact Responses token counting and usage objects were unavailable because no API key/usage object was exposed in this environment. Image tokens use an offline proxy: `85 + 170 * ceil(width/512) * ceil(height/512)` per image payload.

| Document | Iteration | Model call | Input est | Image/file input est | Cached input | Output low | Output expected | Output high | Reasoning |
|---:|---:|---|---:|---:|---|---:|---:|---:|---|
| 37 | 1 | Main orchestration | 2400 | 0 | not exposed | 1170 | 1800 | 2610 | not exposed |
| 37 | 1 | Diego R1 | 155785 | 153935 | not exposed | 1430 | 2200 | 3190 | not exposed |
| 37 | 1 | Jennifer R1 | 168550 | 165750 | not exposed | 1235 | 1900 | 2755 | not exposed |
| 37 | 1 | Diego R2 | 116880 | 114580 | not exposed | 585 | 900 | 1305 | not exposed |
| 37 | 1 | Jennifer R2 | 85375 | 83725 | not exposed | 227 | 350 | 507 | not exposed |
| 37 | 1 | TOTAL | 528990 | 517990 | not exposed | 4647 | 7150 | 10367 | not exposed |

Model calls identified:
- Main orchestration by Codex.
- Diego R1 high-recall extraction, agent `019f76e4-547a-7673-b2f0-8f62bea4d410`.
- Jennifer R1 precision review, agent `019f76ea-6984-7e63-9576-40ef191c90ce`.
- Diego R2 saturation pass, agent `019f76ef-9fbd-77c2-9d95-fbffb7f9e552`.
- Jennifer R2 final confirmation, agent `019f76f3-ef72-7983-87ad-a30470372036`.
