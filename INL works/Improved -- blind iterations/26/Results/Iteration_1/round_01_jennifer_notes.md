# Round 01 Jennifer Precision Review Notes

## Evidence Boundary

I inspected only the raw schematic and supporting resources under `C:\Asif_all_python_projects\INL\Improved -- blind iterations\26\Input resources`, the derived/crop artifacts from those resources under `C:\Asif_all_python_projects\INL\Improved -- blind iterations\26\Codes and artifacts`, and Diego's round-01 files under `C:\Asif_all_python_projects\INL\Improved -- blind iterations\26\Results\Iteration_1`. No ground truth, GT-derived feedback, evaluator output, score feedback, or resources from any other document or iteration were used.

## Final Node Policy

The refined matrix keeps Diego's 200-node list: the 190 inventory physical components plus 10 raw-visible logical bus nodes. I did not add WN/W### route-point artifacts or small conductor/route tags as nodes. Route tags such as `4-416-*`, `480-A-11`, `480-B-14`, `DC-A-INV`, `DC-B-INV`, `120-A-N`, and `120-B-N` remain notes-only because the raw drawing uses them as conductor labels rather than independent connectivity objects.

The raw-visible bus spellings are retained exactly as `BUS-416A`, `BUS-416B`, `BUS-480A`, `BUS-480B`, `BUS-125DCA`, `BUS-125DCB`, `BUS-INV-A`, `BUS-INV-B`, `BUS-120N-A`, and `BUS-120N-B`.

## Edge Changes vs Diego

Removed four Diego edges that visually shortcut separate buses or panels:

| Edge | Jennifer action | Rationale |
|---|---|---|
| `BUS-INV-A` -- `BUS-120N-A` | Removed | The zoomed raw view shows separate inverter and 120N buses. The vertical crossing between them is dashed/control routing, while the solid power path passes through `PNL-AC-A`, not directly bus-to-bus. |
| `BUS-INV-B` -- `BUS-120N-B` | Removed | Same topology as Train A: separate inverter and 120N buses with no raw-visible direct solid tie. |
| `BUS-120N-A` -- `RPS-PNL-A` | Removed | `RPS-PNL-A` is solid-tapped from `BUS-INV-A` and dashed to `TB-UPS-A`; no direct solid tap from `BUS-120N-A` to the RPS panel is visible. |
| `BUS-120N-B` -- `RPS-PNL-B` | Removed | Same topology as Train A: no direct solid 120N-to-RPS-panel tap is visible. |

Added two visually supported component-mediated taps:

| Edge | Jennifer action | Rationale |
|---|---|---|
| `BUS-INV-A` -- `PNL-AC-A` | Added | A solid vertical conductor drops from `BUS-INV-A` into `PNL-AC-A`. `PNL-AC-A` then separately drops to `BUS-120N-A`. |
| `BUS-INV-B` -- `PNL-AC-B` | Added | Same topology as Train A: solid inverter-bus feed into the AC panel, then a separate AC-panel-to-120N tap. |

## Accepted Edge Rationale by Region

### 4.16 kV Sources and Safety Buses

Diego's source and 4.16 kV bus edges are retained. The raw top band shows `GEN-301 -> TR-UAT-31 -> CB-4A-IN1 -> BUS-416A`, `SAT-31A -> CB-4A-ST -> BUS-416A`, `DG-31A -> CB-4A-DG -> BUS-416A`, `SAT-31B -> CB-4B-ST -> BUS-416B`, and `DG-31B -> CB-4B-DG -> BUS-416B`. The A/B 4.16 kV tie remains breaker-mediated through `CB-4AB-TIE`; no direct `BUS-416A` -- `BUS-416B` shortcut was added.

### 4 kV Feeders and Grounds

The 4 kV feeder taps from `BUS-416A/B` to `CB-4A01..CB-4A06` and `CB-4B01..CB-4B06` are retained. Transformer feeders continue through `TR-480A1/A2/B1/B2` to the 480 V incoming/alternate breakers. Motor and pump feeders remain breaker/disconnect-to-load chains. The named grounds `GND-RCP-A`, `GND-RCP-B`, `GND-SW-A`, and `GND-SW-B` are retained only where the raw shows local named ground symbols directly tapped to those branches.

### 480 V Load Centers, MCCs, and Junction Boxes

The 480 V bus labels and breaker taps are retained with tie connectivity only through `CB-480AB-TIE`. Each feeder is modeled as bus -> breaker -> MCC/load center/panel -> starter -> junction box -> load. I retained the junction boxes as physical nodes because they are explicitly drawn and labeled. I did not promote dashed interlock lanes between 480 V loads and the lower DC/UPS area into extra power edges.

### 125 VDC Battery, Charger, Inverter, and DC Tie

The DC bus spellings `BUS-125DCA` and `BUS-125DCB` are retained. Battery and charger branches stay component-mediated through `DS-BAT-A/B` and `CB-CHG-A/B`; the A/B DC tie stays mediated by `CB-DCAB-TIE`. `INV-31A/B` remain connected to their DC buses and to `BUS-INV-A/B` because the raw shows the inverters tapped between the 125 VDC bus and the inverter bus. The nearby `CB-INV-A/B` taps are retained as bus taps, but no extra `CB-INV` -- `INV` edge was added because the visible bus dot already represents the named bus connection point.

### Inverter, 120N, RPS, UPS, and Relays

The key refinement is that `BUS-INV-A/B` and `BUS-120N-A/B` are separate buses. The solid raw-visible path is `BUS-INV-A -> PNL-AC-A -> BUS-120N-A` and `BUS-INV-B -> PNL-AC-B -> BUS-120N-B`, while `RPS-PNL-A/B` are solid-tapped from `BUS-INV-A/B` and dashed to `TB-UPS-A/B`. Relay taps from `BUS-120N-A/B` to `RELAY-K7A1..K7A4` and `RELAY-K7B1..K7B4` are retained. The relay-to-terminal-block-to-potential-transformer chains are retained where the dashed/dotted endpoint chains terminate on named devices.

## Uncertain / Plausible Candidates

| Candidate | Status | Reason |
|---|---|---|
| `BUS-125DCA` -- `CB-INV-A` and `BUS-125DCB` -- `CB-INV-B` | Kept but noted | The breakers are visually tapped at the DC bus near the inverter feeder tag. The raw drawing does not justify adding a separate `CB-INV` -- `INV` edge without over-interpreting the bus tap. |
| `BUS-125DCA` -- `INV-31A` and `BUS-125DCB` -- `INV-31B` | Kept but noted | The inverter vertical conductor lands on the DC bus dot and continues down to the inverter, so the bus-to-inverter edge is directly visible even though the adjacent breaker symbol implies protection. |
| `RPS-PNL-A` -- `TB-UPS-A` and `RPS-PNL-B` -- `TB-UPS-B` | Kept but noted | These are dashed/control endpoint links rather than power feeders. They are retained because both endpoints are named devices and the dashed line terminates between them. |
| `RELAY-K7*` -- `TB-RPS-*` -- `PT-31*` chains | Kept but noted | The chains are endpoint-supported, but the final terminal-block-to-PT segment is dotted/instrument-style rather than a solid power feeder. |
| Small route labels such as `120-A-N`, `120-B-N`, `DC-A-INV`, and `DC-B-INV` | Notes-only | These are plausible conductor identifiers, not independent nodes. |

## Removed / Rejected Candidates

| Candidate | Decision | Reason |
|---|---|---|
| `BUS-INV-A` -- `BUS-120N-A` | Removed | No direct solid bus-to-bus electrical tie is drawn; the apparent crossing is dashed/control routing and the supported solid path is through `PNL-AC-A`. |
| `BUS-INV-B` -- `BUS-120N-B` | Removed | Same as Train A. |
| `BUS-120N-A` -- `RPS-PNL-A` | Removed | The RPS panel is tapped from `BUS-INV-A`; no local 120N tap into the RPS panel is visible. |
| `BUS-120N-B` -- `RPS-PNL-B` | Removed | Same as Train A. |
| Direct `BUS-416A` -- `BUS-416B`, `BUS-480A` -- `BUS-480B`, or `BUS-125DCA` -- `BUS-125DCB` | Rejected | All train ties are breaker-mediated in the raw schematic. |
| WN/W### wire-route artifacts | Rejected | They are derived route points, not raw-visible electrical objects. |
| Broad dashed-lane connectivity across 480 V loads into DC/UPS/RPS | Rejected | Dashed lanes crossing boundaries are control/interlock routing and do not establish broad component connectivity without named endpoints. |

## Output Summary

- Nodes: 200
- Unique undirected edges: 201
- Matrix file: `round_01_jennifer_matrix.csv`
- Notes file: `round_01_jennifer_notes.md`
