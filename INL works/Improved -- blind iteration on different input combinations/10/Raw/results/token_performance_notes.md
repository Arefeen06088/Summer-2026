# Token Performance Notes

- Token telemetry was not exposed by the runtime for this task, so the CSV records artifact-level counts and marks token telemetry unavailable.
- Two deployed subagents were used: Diego for high-recall extraction and Jennifer for precision review/refinement.
- The process saturated after Diego round 2 and Jennifer round 2 agreed on the same final matrix.
- Only the raw schematic PNG and crops generated from that raw PNG were used; no GT or GT-derived resources were used.
