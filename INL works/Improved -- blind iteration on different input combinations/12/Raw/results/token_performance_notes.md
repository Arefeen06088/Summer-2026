# Token Performance Notes

- Token telemetry was not exposed by the runtime for this task, so the CSV records artifact-level counts and marks token telemetry unavailable.
- Two deployed subagents were used: Diego for high-recall extraction and Jennifer for precision review/refinement.
- The process saturated after Diego accepted Jennifer's edge-supported final matrix and Jennifer final-confirmed it.
- There was no Input resources folder; only the raw schematic PNG and crops generated from it were used. No GT or GT-derived resources were used.
