# Document 23 Token Usage Notes

- Actual model usage objects were not available to this local script.
- `OPENAI_API_KEY` was not present, so the OpenAI Responses input-token counting endpoint could not be called.
- Text estimates use `tiktoken` `o200k_base` when available, otherwise character/4.
- Image estimates use the public high-detail tiling approximation: 85 base tokens plus 170 per 512px tile after scaling.
- Low/expected/high ranges vary the amount of visual context and unknown output length.
- Detail CSV: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw + wires + junctions + OCR\results\document23_token_usage_estimates.csv`
- Totals CSV: `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw + wires + junctions + OCR\results\document23_token_usage_totals.csv`