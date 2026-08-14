# Document 16 Token Usage Estimate

No OpenAI API key was available, so the Responses input-token counting endpoint and actual response usage objects could not be queried. Counts below are estimates from local prompt length plus approximate high-detail image tile accounting. Cached input and reasoning tokens are not available in this environment.

| Document | Iteration | Call | Model call | Input est. | Cached input | Image/file input est. | Output est. | Reasoning | Total est. | Low | High |
|---:|---:|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| 16 | 1 | main-setup-and-crop-inspection | main agent | 4200 | 0 | 8245 | 1200 | not available | 13645 | 4500 | 12000 |
| 16 | 1 | Diego R1 high-recall extraction | subagent Diego | 5200 | 0 | 24735 | 9500 | not available | 39435 | 22000 | 45000 |
| 16 | 1 | Jennifer R1 precision review | subagent Jennifer | 7600 | 0 | 24735 | 8500 | not available | 40835 | 23000 | 47000 |
| 16 | 1 | Diego R2 saturation check | subagent Diego | 2300 | 0 | 0 | 900 | not available | 3200 | 2000 | 6500 |
| 16 | 1 | Jennifer R2 final signoff | subagent Jennifer | 1600 | 0 | 0 | 450 | not available | 2050 | 1200 | 5000 |
| 16 | 1 | main integration and artifact generation | main agent | 8500 | 0 | 0 | 1600 | not available | 10100 | 6000 | 18000 |
| 16 | 1 | **Total** | all calls |  |  |  |  |  | **109265** | **58700** | **133500** |

## Estimation Method

- Text input estimate: local character count approximated at about 4 characters per token, rounded upward for structured prompts.
- Image input estimate: high-detail approximation of `85 + 170 * ceil(width/512) * ceil(height/512)` tokens for full-size 4087 x 2732 images; crops are conservatively folded into the same expected buckets.
- Output estimates are observed-size estimates from the extracted edge lists and review summaries.
- Actual `usage` objects could not be collected because this run used in-product subagents rather than direct API responses with accessible usage metadata.
