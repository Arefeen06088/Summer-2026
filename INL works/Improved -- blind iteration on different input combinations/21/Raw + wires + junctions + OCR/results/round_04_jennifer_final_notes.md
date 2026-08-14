# Jennifer Round 04 Final Confirmation Notes

Scope: reviewed only the permitted document 21 folder and crops under `C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\21\Raw + wires + junctions + OCR`, plus the named round 02/03 CSV and note inputs. No Ground Truth, evaluator feedback, previous-document outputs, GT-derived files, generated matrices, or off-the-shelf OCR were used.

## Final Decision

I confirm agreement with Diego round 03 saturation. The final edge set matches Jennifer round 02 precision and Diego round 03 with no round 04 edge changes.

No `round_04_jennifer_changes.csv` is created because no additions, removals, or corrections were made.

## Counts

- Final edges: 202
- Round 04 additions: 0
- Round 04 removals: 0
- Round 04 corrections: 0
- Edge kinds: 122 power_feeder, 58 control_interlock, 15 instrument_signal, 6 ground, 1 normally_open_tie
- Confidence: 186 high, 16 medium, 0 low

## Required Confirmations

- `4KV_SWITCHGEAR_LEFT_RISER` is not present as a final endpoint. I agree with excluding this abstract riser because it would overconnect the 4.16 kV switchgear bus geometry.
- `BUS-201A -- CB-301A` remains in the final set as a medium-confidence `power_feeder`. The raw top-left/top-center view supports the feeder drop from the BUS-201A-side bus/tap geometry into `CB-301A`.
- `BUS-501A -- CP-CRD` and `BUS-501B -- CP-CRD` are absent. The bottom-center crop shows a U-shaped/dashed continuation near the BUS-501 rails and `CP-CRD`, but not a clear direct terminal tap from either bus rail into `CP-CRD`.
- Raw-only devices remain where supported:
  - `CB-204A` remains with `BUS-201B -- CB-204A` and `CB-204A -- DS-201B`.
  - `CB-204B` remains with `BUS-202A -- CB-204B` and `CB-204B -- DS-202A`.
  - `DS-401B` remains with `BUS-401A -- DS-401B`, `DS-401B -- TR-DC-B`, and medium-confidence `DS-401B -- BUS-401B` as the `normally_open_tie`.

## Rationale

The reviewed raw and wire crops support Diego's no-change saturation decision. I did not find a remaining precision issue in the disputed areas. The final set preserves supported raw-only components, avoids the overbroad 4 kV riser abstraction, keeps the localized `BUS-201A -- CB-301A` replacement, and rejects unsupported BUS-501A/B direct taps to `CP-CRD`.

## Residual Medium-Confidence Edges

The final set contains 16 medium-confidence edges:

- `DS-J02B -- CB-502B` (`power_feeder`)
- `BUS-301A -- DS-401A` (`power_feeder`)
- `DS-401B -- BUS-401B` (`normally_open_tie`)
- `BUS-301A -- DS-402A` (`power_feeder`)
- `INV-120C -- BUS-501A` (`power_feeder`)
- `BUS-401A -- DS-402B` (`power_feeder`)
- `RECT-24C -- BUS-501B` (`power_feeder`)
- `BAT-EDG-A -- CP-CRD` (`control_interlock`)
- `BAT-EDG-B -- CP-CRD` (`control_interlock`)
- `BUS-501A -- CP-SWGR` (`control_interlock`)
- `CP-SWGR -- CP-SI-A` (`control_interlock`)
- `BUS-501A -- UVLS-A` (`control_interlock`)
- `BUS-501B -- UVLS-B` (`control_interlock`)
- `UVLS-A -- RELAY-K101` (`control_interlock`)
- `UVLS-B -- RELAY-K102` (`control_interlock`)
- `BUS-201A -- CB-301A` (`power_feeder`)
