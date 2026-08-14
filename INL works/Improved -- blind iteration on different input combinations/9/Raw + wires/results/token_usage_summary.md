# Token Usage Estimate

No OpenAI API key was available, so the Responses input-token counting endpoint and model usage objects could not be queried.

Local method: text is counted with `tiktoken` `o200k_base` when installed and falls back to `ceil(chars/4)`. Image input tokens use the common high-detail heuristic `85 + 170 * 512px_tiles_after_resize`.

| Document | Iteration | Model calls | Input expected | Image/file input | Output expected | Reasoning expected | Total low | Total expected | Total high |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 1 | 7 | 107723 | 99110 | 30900 | 61500 | 135930 | 200123 | 303517 |

Detailed per-call estimates are in `token_usage_estimate.csv`; per-image estimates are in `image_token_estimate_details.csv`.