# Round 01 Diego Extraction Notes

## Evidence Boundary

I inspected only the resources under `C:\Asif_all_python_projects\INL\Improved -- blind iterations\26\Input resources` and the derived/crop artifacts already present under `C:\Asif_all_python_projects\INL\Improved -- blind iterations\26\Codes and artifacts`. No ground truth, GT-derived feedback, evaluator output, score feedback, or resources from any other document/iteration were used.

## Node List Rationale

The matrix contains 200 nodes: 190 visually/OCR-supported physical components from `component_visual_ocr_labels.csv` / `component_labels_list.txt`, plus 10 printed logical bus nodes read from the raw schematic crops. I did not include wire-node artifacts such as `WN`/`W*`, route tags such as `4-416-A-01`, `480-A-11`, `DC-A-INV`, `DC-B-INV`, or neutral-style tags `120-A-N` / `120-B-N` as standalone nodes because they appear to label conductors rather than act as independent connectivity objects.

Printed bus/logical nodes included: `BUS-416A`, `BUS-416B`, `BUS-480A`, `BUS-480B`, `BUS-125DCA`, `BUS-125DCB`, `BUS-INV-A`, `BUS-INV-B`, `BUS-120N-A`, and `BUS-120N-B`.

Physical component category summary: {'loads/sources/other devices': 41, 'transformers': 7, 'breakers': 36, 'disconnect switches': 10, 'grounds': 8, 'panels/load centers/MCCs': 14, 'control/distribution endpoints': 74}.

## Edge Evidence by Region

### 4.16 kV Sources and Safety Buses

The upper raw crop shows direct vertical source chains into the two printed 4.16 kV buses. I modeled `GEN-301 -> TR-UAT-31 -> CB-4A-IN1 -> BUS-416A`, `SAT-31A -> CB-4A-ST -> BUS-416A`, `DG-31A -> CB-4A-DG -> BUS-416A`, `SAT-31B -> CB-4B-ST -> BUS-416B`, and `DG-31B -> CB-4B-DG -> BUS-416B`. The tie is represented through `CB-4AB-TIE` as `BUS-416A -> CB-4AB-TIE -> BUS-416B`; there is no direct bus-to-bus shortcut edge.

### 4 kV Feeder Rows

The feeder breakers `CB-4A01..CB-4A06` and `CB-4B01..CB-4B06` are direct bus taps. Transformer feeders are chained through their transformer to the visible lower 480 V incoming/alternate breakers. Motor/pump feeders are chained as breaker to disconnect to terminal load. Ground taps are included where the raw crop shows named ground symbols terminating on the RCP and SW motor/pump branches: `GND-RCP-A/B` and `GND-SW-A/B`.

### 480 V Load Centers and MCCs

The printed `BUS-480A` and `BUS-480B` nodes collect the transformer incoming/alternate breakers and directly feed `CB-480A11..14` / `CB-480B11..14`. The 480 V bus tie is modeled through `CB-480AB-TIE`. Each feeder breaker is connected only to its visually aligned MCC/load center/panel, then each MCC/load center/panel is connected to its three visible starters; each starter is connected to its junction box and load. MCC ground symbols `GND-MCC-A1`, `GND-MCC-A2`, `GND-MCC-B1`, and `GND-MCC-B2` are connected to their adjacent MCC sections.

### 125 VDC / UPS / RPS

The lower raw crops show battery and charger branches into `BUS-125DCA` / `BUS-125DCB` through their disconnect/breaker devices, with `CB-DCAB-TIE` between the two DC buses. DC panels and inverters are direct bus taps. Inverters feed the printed inverter buses `BUS-INV-A` / `BUS-INV-B`, which in turn align with the printed `BUS-120N-A` / `BUS-120N-B` buses and the RPS/UPS endpoint structures.

For the RPS area, relay-to-terminal-block-to-potential-transformer chains are included for `K7A1..K7A4` and `K7B1..K7B4` because the vertical/dashed endpoint chains terminate on named devices. `RPS-PNL-A/B` to `TB-UPS-A/B` are included because the dashed horizontal lines visibly terminate between those named blocks.

## Ambiguous Cases

- Section titles such as `4.16 kV SAFETY BUS - TRAIN A`, `480 V LOAD CENTER / MCC - TRAIN A`, and `125 VDC / UPS / RPS - TRAIN A/B` were not included as connectivity nodes.
- Small labels including `4-416-*`, `480-*`, `DC-A-INV`, `DC-B-INV`, `120-A-N`, and `120-B-N` were treated as route/neutral tags, not independent nodes. The printed bus labels `BUS-120N-A` and `BUS-120N-B` were included.
- Dashed runs from the 480 V load/starter area toward the DC/UPS region are visually present, but several intermediate paths pass through or near dashed boundaries without unambiguous named electrical endpoints. I did not convert those into broad cross-region edges; the clearer named endpoint pairs in the RPS/UPS lower region were retained.
- The inverter-to-120N bus relationships are high-recall inclusions: the vertical conductors align through the printed inverter buses and terminate on the printed 120N buses, but the exact role of the nearby neutral route tags is uncertain.
- Ground edges are limited to named ground symbols with direct local taps. I did not infer additional equipment grounding where no named ground symbol is drawn.

## Output Summary

- Nodes: 200
- Unique undirected edges: 203
- Matrix file: `round_01_diego_matrix.csv`
- Notes file: `round_01_diego_notes.md`
