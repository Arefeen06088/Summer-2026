# Document 41 Token Usage Notes

- Actual model usage objects were unavailable from the local subagent tool responses.
- No API key was available, so the Responses token-counting endpoint could not be called.
- Text estimates use `tiktoken` `o200k_base` where available; image estimates use public high-detail image tiling.
- Low/expected/high ranges vary visual context volume and unknown output length.
