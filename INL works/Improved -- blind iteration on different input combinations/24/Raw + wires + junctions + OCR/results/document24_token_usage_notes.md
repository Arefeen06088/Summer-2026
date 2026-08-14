# Document 24 Token Usage Notes

- Actual model usage objects were unavailable to this local script.
- `OPENAI_API_KEY` was not present if the totals CSV says `no`, so the OpenAI Responses token-counting endpoint could not be called.
- Text estimates use `tiktoken` `o200k_base`; image estimates use public high-detail image tiling.
- Low/expected/high ranges vary visual context volume and unknown output length.
