from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


RESULTS = Path(__file__).resolve().parent
BASE = RESULTS.parent
COMPONENT_CSV = BASE / "component_visual_ocr_labels.csv"


def add_node(rows, node_id, label, node_kind, role, action, related, evidence, confidence):
    rows.append(
        {
            "node_id": node_id,
            "label": label,
            "node_kind": node_kind,
            "role_or_type": role,
            "action": action,
            "related_existing_node": related,
            "evidence": evidence,
            "confidence": confidence,
        }
    )


def add_edge(rows, a, b, kind, evidence, confidence):
    rows.append(
        {
            "node_a": a,
            "node_b": b,
            "kind": kind,
            "evidence": evidence,
            "confidence": confidence,
        }
    )


with COMPONENT_CSV.open(newline="", encoding="utf-8") as f:
    component_rows = list(csv.DictReader(f))

existing_labels = {r["final_label"] for r in component_rows}

node_rows = []

add_node(
    node_rows,
    "ADD-0001",
    "SWYD-230",
    "physical_component",
    "230 kV switchyard/switchgear block",
    "add_missing_component",
    "",
    "crop_raw_common_source_230kv_sut.png: rectangular block labeled SWYD-230 between GRID-230KV and DS-101.",
    "high",
)
add_node(
    node_rows,
    "ADD-0002",
    "BUS-230KV-SWITCHYARD",
    "logical_bus",
    "230 kV switchyard / station startup feed",
    "add_logical_bus",
    "",
    "crop_raw_common_source_230kv_sut.png: drawn title '230kV SWITCHYARD / STATION STARTUP FEED' above the incoming source conductor.",
    "high",
)
for idx, train in enumerate("ABCD", start=3):
    zone = {"A": "ZONE 1", "B": "ZONE 2", "C": "ZONE 3", "D": "ZONE 4"}[train]
    crop = "top" if train in "AB" else "bottom"
    add_node(
        node_rows,
        f"ADD-{idx:04d}",
        f"BUS-4{train}",
        "logical_bus",
        f"4.16 kV switchgear bus, 4KV SWGR {train} / {zone}",
        "add_logical_bus",
        "",
        f"crop_raw_{crop}_{train.lower()}_power.png and labels overlay: thick horizontal bus labeled BUS-4{train} 4.16 kV.",
        "high",
    )
for offset, train in enumerate("ABCD", start=7):
    add_node(
        node_rows,
        f"ADD-{offset:04d}",
        f"DC-BUS-{train}",
        "logical_bus",
        "125 VDC bus",
        "add_logical_bus",
        "",
        f"crop_raw_train_{train.lower()}_mcc_dc.png: thick DC bus labeled DC-BUS-{train} and 125 VDC.",
        "high",
    )
for offset, train in enumerate("ABCD", start=11):
    add_node(
        node_rows,
        f"ADD-{offset:04d}",
        f"LOCAL-IO-{train}",
        "logical_endpoint",
        "local I/O terminal on 480 V load-center bus",
        "add_logical_endpoint",
        "",
        f"crop_raw_train_{train.lower()}_mcc_dc.png / {train} power crop: 'LOCAL I/O' terminal marks at the right end of LC-480{train}.",
        "medium",
    )
add_node(
    node_rows,
    "ADD-0015",
    "UNIT-GENERATOR-AUX-FEED",
    "logical_source",
    "unit generator auxiliary feed",
    "add_logical_source",
    "",
    "crop_raw_middle_source_tie_cd.png: text 'UNIT GENERATOR AUXILIARY FEED' on lower source path feeding GEN-G1/CB-201/TR-UAT transformers.",
    "high",
)
for offset, train in enumerate("ABCD", start=16):
    add_node(
        node_rows,
        f"ADD-{offset:04d}",
        f"ESFAS-LO-PERMISSIVE-{train}",
        "logical_control_source",
        "L.O. permissive from ESFAS",
        "add_logical_control_node",
        "",
        f"crop_raw_train_{train.lower()}_mcc_dc.png: note {offset - 15} states 'L.O. permissive from ESFAS' near train {train} relay/control area.",
        "low",
    )
for offset, train in enumerate("ABCD", start=20):
    add_node(
        node_rows,
        f"ADD-{offset:04d}",
        f"DIESEL-GEN-{train}-AUTO-START",
        "logical_control_source",
        "diesel generator auto-start control",
        "add_logical_control_node",
        "",
        f"power-source crop for train {train}: text 'DIESEL GEN. {train} AUTO START' near EDG-{train}/CB-DG{train}.",
        "low",
    )
add_node(
    node_rows,
    "ADD-0024",
    "ANNUNCIATOR-PLANT-PROCESS-COMPUTER",
    "offpage_endpoint",
    "annunciator / plant process computer continuation",
    "add_offpage_endpoint",
    "",
    "crop_raw_middle_source_tie_cd.png: right-pointing continuation text 'TO ANNUNCIATOR / PLANT PROCESS COMPUTER'.",
    "low",
)
add_node(
    node_rows,
    "ADD-0025",
    "125VDC-SYSTEM-SHT-DC-2",
    "offpage_endpoint",
    "125 VDC system sheet DC-2 continuation",
    "add_offpage_endpoint",
    "",
    "crop_raw_middle_source_tie_cd.png/raw left continuation text 'CONTINUATION TO 125 VDC SYSTEM SHT-DC-2'.",
    "low",
)

for offset, label in enumerate(("LC-480A", "LC-480B", "LC-480C", "LC-480D"), start=1):
    train = label[-1]
    add_node(
        node_rows,
        f"CORR-{offset:04d}",
        label,
        "physical_component_with_bus_behavior",
        "480 V load-center busbar",
        "interpret_existing_label_as_bus_node",
        label,
        f"crop_raw_train_{train.lower()}_mcc_dc.png: LC-480{train} is the thick 480 V distribution bus feeding PP/MCC/JB branches.",
        "high",
    )
for offset, label in enumerate(
    (
        "MCC-A1",
        "MCC-A2",
        "MCC-B1",
        "MCC-B2",
        "MCC-C1",
        "MCC-C2",
        "MCC-D1",
        "MCC-D2",
    ),
    start=5,
):
    train = label[4]
    add_node(
        node_rows,
        f"CORR-{offset:04d}",
        label,
        "physical_component_with_bus_behavior",
        "motor-control-center busbar",
        "interpret_existing_label_as_bus_node",
        label,
        f"crop_raw_train_{train.lower()}_mcc_dc.png: {label} is drawn as a horizontal MCC bus with multiple breaker taps.",
        "high",
    )
add_node(
    node_rows,
    "CORR-0013",
    "GND-PLANT",
    "physical_component_with_bus_behavior",
    "common plant grounding network",
    "interpret_existing_label_as_ground_net",
    "GND-PLANT",
    "crop_raw_plant_ground_center.png: GND-PLANT ground symbol joins long grounding conductors from individual train grounds.",
    "medium",
)

added_labels = {r["label"] for r in node_rows if r["action"].startswith("add_")}
known_labels = existing_labels | added_labels

edges = []

# Common 230 kV / startup source and A/B 4.16 kV buses.
add_edge(edges, "GRID-230KV", "BUS-230KV-SWITCHYARD", "ac_power_feeder", "crop_raw_common_source_230kv_sut.png: grid source is on the incoming 230 kV startup feed.", "high")
add_edge(edges, "BUS-230KV-SWITCHYARD", "SWYD-230", "ac_power_feeder", "crop_raw_common_source_230kv_sut.png: horizontal conductor enters SWYD-230 block.", "high")
add_edge(edges, "SWYD-230", "DS-101", "ac_power_feeder", "crop_raw_common_source_230kv_sut.png: conductor leaves SWYD-230 and enters DS-101.", "high")
add_edge(edges, "DS-101", "CB-101", "ac_power_feeder", "crop_raw_common_source_230kv_sut.png: DS-101 output continues right to CB-101.", "high")
add_edge(edges, "CB-101", "TR-SUT-1A", "ac_power_feeder", "crop_raw_common_source_230kv_sut.png: CB-101 upper branch enters TR-SUT-1A primary.", "high")
add_edge(edges, "CB-101", "TR-SUT-1B", "ac_power_feeder", "crop_raw_common_source_230kv_sut.png: CB-101 lower branch enters TR-SUT-1B primary.", "high")
add_edge(edges, "TR-SUT-1A", "BUS-4A", "ac_power_feeder", "common/top A crops: TR-SUT-1A secondary drops to BUS-4A near T4 with junction dots.", "high")
add_edge(edges, "TR-SUT-1B", "BUS-4B", "ac_power_feeder", "common/top B crops: TR-SUT-1B secondary continues to BUS-4B incoming side.", "medium")

for train in "AB":
    add_edge(edges, f"BUS-4{train}", f"CB-DG{train}", "ac_power_feeder", f"crop_raw_top_{train.lower()}_power.png: EDG feeder breaker CB-DG{train} taps BUS-4{train}.", "high")
    add_edge(edges, f"CB-DG{train}", f"EDG-{train}", "ac_power_feeder", f"crop_raw_top_{train.lower()}_power.png: CB-DG{train} is in series with EDG-{train}.", "high")
add_edge(edges, "BUS-4A", "CB-TIE-AB", "ac_power_feeder", "top A/B crops: CB-TIE-AB is drawn on the horizontal tie from BUS-4A toward BUS-4B.", "high")
add_edge(edges, "CB-TIE-AB", "BUS-4B", "ac_power_feeder", "top A/B crops: right side of CB-TIE-AB continues into BUS-4B side.", "high")

# Unit auxiliary source and C/D 4.16 kV buses.
add_edge(edges, "UNIT-GENERATOR-AUX-FEED", "GEN-G1", "ac_power_source_label", "crop_raw_middle_source_tie_cd.png: GEN-G1 sits on the unit generator auxiliary feed label path.", "medium")
add_edge(edges, "GEN-G1", "CB-201", "ac_power_feeder", "crop_raw_middle_source_tie_cd.png: generator output conductor enters CB-201.", "high")
add_edge(edges, "CB-201", "UNIT-GENERATOR-AUX-FEED", "ac_power_feeder", "crop_raw_middle_source_tie_cd.png: CB-201 output is on the unit auxiliary feed conductor.", "medium")
add_edge(edges, "UNIT-GENERATOR-AUX-FEED", "TR-UAT-1A", "ac_power_feeder", "crop_raw_middle_source_tie_cd.png: unit auxiliary feed connects into TR-UAT-1A path.", "high")
add_edge(edges, "UNIT-GENERATOR-AUX-FEED", "TR-UAT-1B", "ac_power_feeder", "crop_raw_middle_source_tie_cd.png: long auxiliary feed continuation reaches TR-UAT-1B path.", "medium")
add_edge(edges, "TR-UAT-1A", "BUS-4C", "ac_power_feeder", "crop_raw_middle_source_tie_cd.png: TR-UAT-1A secondary drops to BUS-4C around T4.", "high")
add_edge(edges, "TR-UAT-1B", "BUS-4D", "ac_power_feeder", "crop_raw_middle_source_tie_cd.png: TR-UAT-1B secondary drops to BUS-4D around T4.", "high")
for train in "CD":
    add_edge(edges, f"BUS-4{train}", f"CB-DG{train}", "ac_power_feeder", f"crop_raw_middle_source_tie_cd.png: EDG feeder breaker CB-DG{train} taps BUS-4{train}.", "high")
    add_edge(edges, f"CB-DG{train}", f"EDG-{train}", "ac_power_feeder", f"crop_raw_middle_source_tie_cd.png: CB-DG{train} is in series with EDG-{train}.", "high")
add_edge(edges, "BUS-4C", "CB-TIE-CD", "ac_power_feeder", "middle/bottom C-D crops: CB-TIE-CD is drawn on the tie from BUS-4C toward BUS-4D.", "high")
add_edge(edges, "CB-TIE-CD", "BUS-4D", "ac_power_feeder", "middle/bottom C-D crops: right side of CB-TIE-CD continues into BUS-4D side.", "high")

trains = {
    "A": {
        "crop": "crop_raw_train_a_mcc_dc.png",
        "power_crop": "crop_raw_top_a_power.png",
        "bus4": "BUS-4A",
        "cb4": "CB-4A-48",
        "tr480": "TR-480A",
        "cb48": "CB-48A",
        "lc": "LC-480A",
        "pp": "PP-A1",
        "mcc1": "MCC-A1",
        "mcc2": "MCC-A2",
        "jb": "JB-A1",
        "bat": "BAT-125A",
        "chg": "CHG-125A",
        "dc": "DC-BUS-A",
        "inv": "INV-A",
        "ups": "UPS-A",
        "local": "LOCAL-IO-A",
        "ground": "GND-A",
        "esfas": "ESFAS-LO-PERMISSIVE-A",
        "branches": [
            ("MCC-A1", "CB-A01", "DS-A01", "PMP-SI-A01"),
            ("MCC-A1", "CB-A02", "", "PMP-RHR-A02"),
            ("MCC-A1", "CB-A03", "DS-A03", "MTR-CCW-A03"),
            ("MCC-A1", "CB-A04", "", "FAN-VC-A04"),
            ("MCC-A1", "CB-A05", "", "MOV-RCS-A05"),
            ("MCC-A2", "CB-A06", "DS-A06", "PMP-CHG-A06"),
            ("MCC-A2", "CB-A07", "", "HTR-CAB-A07"),
            ("MCC-A2", "CB-A08", "", "INST-RK-A08"),
            ("MCC-A2", "CB-A09", "", "VLV-HPI-A09"),
            ("MCC-A2", "CB-A10", "", "PNL-ESF-A10"),
        ],
        "relays": [
            ("MCC-A1", "RLY-KA01", "CB-A01"),
            ("MCC-A1", "RLY-KA02", "CB-A02"),
            ("MCC-A1", "RLY-KA05", "CB-A05"),
            ("MCC-A2", "RLY-KA07", "CB-A07"),
        ],
    },
    "B": {
        "crop": "crop_raw_train_b_mcc_dc.png",
        "power_crop": "crop_raw_top_b_power.png",
        "bus4": "BUS-4B",
        "cb4": "CB-4B-48",
        "tr480": "TR-480B",
        "cb48": "CB-48B",
        "lc": "LC-480B",
        "pp": "PP-B1",
        "mcc1": "MCC-B1",
        "mcc2": "MCC-B2",
        "jb": "JB-B1",
        "bat": "BAT-125B",
        "chg": "CHG-125B",
        "dc": "DC-BUS-B",
        "inv": "INV-B",
        "ups": "UPS-B",
        "local": "LOCAL-IO-B",
        "ground": "GND-B",
        "esfas": "ESFAS-LO-PERMISSIVE-B",
        "branches": [
            ("MCC-B1", "CB-B01", "", "PMP-SI-B01"),
            ("MCC-B1", "CB-B02", "DS-B02", "PMP-RHR-B02"),
            ("MCC-B1", "CB-B03", "", "MTR-CCW-B03"),
            ("MCC-B1", "CB-B04", "", "FAN-VC-B04"),
            ("MCC-B1", "CB-B05", "DS-B05", "MOV-RCS-B05"),
            ("MCC-B2", "CB-B06", "", "PMP-CHG-B06"),
            ("MCC-B2", "CB-B07", "", "HTR-CAB-B07"),
            ("MCC-B2", "CB-B08", "DS-B08", "INST-RK-B08"),
            ("MCC-B2", "CB-B09", "", "VLV-HPI-B09"),
            ("MCC-B2", "CB-B10", "", "PNL-ESF-B10"),
        ],
        "relays": [
            ("MCC-B1", "RLY-KB02", "CB-B02"),
            ("MCC-B1", "RLY-KB04", "CB-B04"),
            ("MCC-B2", "RLY-KB06", "CB-B06"),
        ],
    },
    "C": {
        "crop": "crop_raw_train_c_mcc_dc.png",
        "power_crop": "crop_raw_bottom_c_power.png",
        "bus4": "BUS-4C",
        "cb4": "CB-4C-48",
        "tr480": "TR-480C",
        "cb48": "CB-48C",
        "lc": "LC-480C",
        "pp": "PP-C1",
        "mcc1": "MCC-C1",
        "mcc2": "MCC-C2",
        "jb": "JB-C1",
        "bat": "BAT-125C",
        "chg": "CHG-125C",
        "dc": "DC-BUS-C",
        "inv": "INV-C",
        "ups": "UPS-C",
        "local": "LOCAL-IO-C",
        "ground": "GND-C",
        "esfas": "ESFAS-LO-PERMISSIVE-C",
        "branches": [
            ("MCC-C1", "CB-C01", "DS-C01", "PMP-SI-C01"),
            ("MCC-C1", "CB-C02", "", "PMP-RHR-C02"),
            ("MCC-C1", "CB-C03", "", "MTR-CCW-C03"),
            ("MCC-C1", "CB-C04", "DS-C04", "FAN-VC-C04"),
            ("MCC-C1", "CB-C05", "", "MOV-RCS-C05"),
            ("MCC-C2", "CB-C06", "", "PMP-CHG-C06"),
            ("MCC-C2", "CB-C07", "DS-C07", "HTR-CAB-C07"),
            ("MCC-C2", "CB-C08", "", "INST-RK-C08"),
            ("MCC-C2", "CB-C09", "", "VLV-HPI-C09"),
            ("MCC-C2", "CB-C10", "", "PNL-ESF-C10"),
        ],
        "relays": [
            ("MCC-C1", "RLY-KC01", "CB-C01"),
            ("MCC-C1", "RLY-KC03", "CB-C03"),
            ("MCC-C2", "RLY-KC08", "CB-C08"),
        ],
    },
    "D": {
        "crop": "crop_raw_train_d_mcc_dc.png",
        "power_crop": "crop_raw_bottom_d_power.png",
        "bus4": "BUS-4D",
        "cb4": "CB-4D-48",
        "tr480": "TR-480D",
        "cb48": "CB-48D",
        "lc": "LC-480D",
        "pp": "PP-D1",
        "mcc1": "MCC-D1",
        "mcc2": "MCC-D2",
        "jb": "JB-D1",
        "bat": "BAT-125D",
        "chg": "CHG-125D",
        "dc": "DC-BUS-D",
        "inv": "INV-D",
        "ups": "UPS-D",
        "local": "LOCAL-IO-D",
        "ground": "GND-D",
        "esfas": "ESFAS-LO-PERMISSIVE-D",
        "branches": [
            ("MCC-D1", "CB-D01", "", "PMP-SI-D01"),
            ("MCC-D1", "CB-D02", "DS-D02", "PMP-RHR-D02"),
            ("MCC-D1", "CB-D03", "", "MTR-CCW-D03"),
            ("MCC-D1", "CB-D04", "", "FAN-VC-D04"),
            ("MCC-D1", "CB-D05", "", "MOV-RCS-D05"),
            ("MCC-D2", "CB-D06", "DS-D06", "PMP-CHG-D06"),
            ("MCC-D2", "CB-D07", "", "HTR-CAB-D07"),
            ("MCC-D2", "CB-D08", "", "INST-RK-D08"),
            ("MCC-D2", "CB-D09", "DS-D09", "VLV-HPI-D09"),
            ("MCC-D2", "CB-D10", "", "PNL-ESF-D10"),
        ],
        "relays": [
            ("MCC-D1", "RLY-KD02", "CB-D02"),
            ("MCC-D1", "RLY-KD05", "CB-D05"),
            ("MCC-D2", "RLY-KD07", "CB-D07"),
            ("MCC-D2", "RLY-KD10", "CB-D10"),
        ],
    },
}

for train, t in trains.items():
    add_edge(edges, t["bus4"], t["cb4"], "ac_power_feeder", f"{t['power_crop']}: BUS-4{train} tap drops through {t['cb4']}.", "high")
    add_edge(edges, t["cb4"], t["tr480"], "ac_power_feeder", f"{t['power_crop']}: {t['cb4']} lower terminal enters {t['tr480']}.", "high")
    add_edge(edges, t["tr480"], t["cb48"], "ac_power_feeder", f"{t['power_crop']}: {t['tr480']} secondary is wired to {t['cb48']}.", "high")
    add_edge(edges, t["cb48"], t["lc"], "ac_power_feeder", f"{t['power_crop']}: {t['cb48']} output drops to the LC-480{train} 480 V bus.", "high")

    add_edge(edges, t["lc"], t["pp"], "ac_power_feeder", f"{t['crop']}: left vertical feeder from LC-480{train} enters {t['pp']}.", "high")
    add_edge(edges, t["lc"], t["mcc1"], "ac_power_feeder", f"{t['crop']}: LC-480{train} vertical feeder supplies {t['mcc1']} bus.", "high")
    add_edge(edges, t["lc"], t["mcc2"], "ac_power_feeder", f"{t['crop']}: LC-480{train} vertical feeder supplies {t['mcc2']} bus.", "high")
    add_edge(edges, t["lc"], t["jb"], "instrument_or_io", f"{t['crop']}: vertical drop from right side of LC-480{train} enters {t['jb']} / local I/O area.", "medium")
    add_edge(edges, t["lc"], t["local"], "instrument_or_io", f"{t['power_crop']}: LOCAL I/O terminal symbol sits at the right end of LC-480{train}.", "medium")
    add_edge(edges, t["local"], t["jb"], "instrument_or_io", f"{t['crop']}: LOCAL I/O/JB-{train}1 graphics are co-located on the same right-side terminal area.", "low")
    add_edge(edges, t["jb"], t["dc"], "control_trip", f"{t['crop']}: dashed vertical/control line from JB-{train}1 descends to the DC bus region.", "low")

    add_edge(edges, t["bat"], t["chg"], "dc_power_feeder", f"{t['crop']}: BAT-125{train} is wired vertically into CHG-125{train}.", "high")
    add_edge(edges, t["chg"], t["dc"], "dc_power_feeder", f"{t['crop']}: CHG-125{train} lower terminal connects to DC-BUS-{train}.", "high")
    add_edge(edges, t["dc"], t["inv"], "dc_power_feeder", f"{t['crop']}: DC-BUS-{train} drops into INV-{train}.", "high")
    add_edge(edges, t["inv"], t["ups"], "ac_or_dc_power_feeder", f"{t['crop']}: INV-{train} lower path continues into UPS-{train}.", "medium")
    add_edge(edges, t["ups"], t["pp"], "control_or_aux_power_loop", f"{t['crop']}: thin rectangular loop visually connects UPS-{train} side path back toward {t['pp']}.", "low")
    add_edge(edges, t["pp"], t["ground"], "grounding", f"{t['crop']}: {t['pp']} lower/enclosure path visually continues to train {train} ground area.", "low")

    for mcc, cb, ds, load in t["branches"]:
        add_edge(edges, mcc, cb, "ac_power_feeder", f"{t['crop']}: vertical tap from {mcc} bus feeds {cb}.", "high")
        if ds:
            add_edge(edges, cb, ds, "ac_power_feeder", f"{t['crop']}: {cb} output continues to {ds}.", "high")
            add_edge(edges, ds, load, "ac_power_feeder", f"{t['crop']}: {ds} lower terminal feeds {load}.", "high")
        else:
            add_edge(edges, cb, load, "ac_power_feeder", f"{t['crop']}: {cb} output continues directly to {load}.", "high")

    for mcc, relay, cb in t["relays"]:
        add_edge(edges, mcc, relay, "control_trip", f"{t['crop']}: relay {relay} is drawn on/adjacent to the vertical control branch from {mcc}.", "medium")
        add_edge(edges, relay, cb, "control_trip", f"{t['crop']}: dashed/vertical permissive line associates {relay} with {cb}.", "medium")
        add_edge(edges, t["esfas"], relay, "control_trip_uncertain", f"{t['crop']}: nearby note says L.O. permissive from ESFAS; exact wire to {relay} is not individually traced.", "low")

for train in "ABCD":
    add_edge(edges, f"GND-{train}", "GND-PLANT", "grounding", f"crop_raw_plant_ground_center.png and train {train} crop: individual train ground joins common grounding network.", "medium")
    add_edge(edges, f"DIESEL-GEN-{train}-AUTO-START", f"EDG-{train}", "control_trip_uncertain", f"source crop for train {train}: auto-start text placed by EDG-{train}.", "low")
    add_edge(edges, f"DIESEL-GEN-{train}-AUTO-START", f"CB-DG{train}", "control_trip_uncertain", f"source crop for train {train}: auto-start text is on the EDG breaker/generator control path.", "low")

add_edge(edges, "BUS-4D", "ANNUNCIATOR-PLANT-PROCESS-COMPUTER", "offpage_continuation_uncertain", "crop_raw_middle_source_tie_cd.png: right side of train D bus/line has continuation arrow to annunciator / plant process computer.", "low")
add_edge(edges, "125VDC-SYSTEM-SHT-DC-2", "DC-BUS-C", "offpage_continuation_uncertain", "raw/middle source area: left continuation text names 125 VDC system sheet DC-2; nearest lower-train DC bus is DC-BUS-C.", "low")

missing = sorted({node for e in edges for node in (e["node_a"], e["node_b"]) if node not in known_labels})
if missing:
    raise SystemExit(f"Unknown edge endpoint labels: {missing}")

edge_pairs = Counter(tuple(sorted((e["node_a"], e["node_b"]))) for e in edges)
duplicates = [pair for pair, count in edge_pairs.items() if count > 1]
if duplicates:
    raise SystemExit(f"Duplicate undirected edges: {duplicates[:10]}")

node_path = RESULTS / "document13_node_additions_corrections.csv"
edge_path = RESULTS / "document13_edge_list.csv"
notes_path = RESULTS / "document13_uncertain_rejected_notes.md"
counts_path = RESULTS / "document13_final_counts.json"

with node_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(node_rows[0].keys()))
    writer.writeheader()
    writer.writerows(node_rows)

with edge_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["node_a", "node_b", "kind", "evidence", "confidence"])
    writer.writeheader()
    writer.writerows(edges)

notes = """# Document 13 Uncertain / Rejected Notes

Scope: extraction used only files in this document 13 folder: raw schematic, component label overlay/CSV, wire overlays/mask, and the prepared crop/contrast images in `codes`. No Ground Truth, evaluator output, GT-derived feedback, or off-the-shelf OCR was used.

## Included But Uncertain

- `ESFAS-LO-PERMISSIVE-A/B/C/D` to relay edges are low confidence. The notes explicitly say L.O. permissive from ESFAS near the relay areas, but individual ESFAS wires are not separately traced.
- `DIESEL-GEN-*-AUTO-START` edges to EDGs and diesel-generator breakers are low confidence control candidates. The labels are visually present near the EDG source paths, but the exact terminal endpoints are not drawn as ordinary point-to-point wires.
- `JB-*1 -- DC-BUS-*`, `LOCAL-IO-* -- JB-*1`, and `UPS-* -- PP-*1` are retained as low/medium confidence because the thin/dashed local I/O and rectangular auxiliary loops are visually connected but semantically different from the main solid power feeders.
- `PP-*1 -- GND-*` and `GND-* -- GND-PLANT` are included as grounding candidates. The individual and plant ground conductors are visible, but the panel/enclosure-to-ground semantics are less explicit than the main feeder paths.
- `BUS-4D -- ANNUNCIATOR-PLANT-PROCESS-COMPUTER` and `125VDC-SYSTEM-SHT-DC-2 -- DC-BUS-C` are off-page/continuation candidates with low confidence.
- `TR-SUT-1B -- BUS-4B` and `UNIT-GENERATOR-AUX-FEED -- TR-UAT-1B` are medium confidence because they are long routed feeder continuations across crop boundaries.

## Rejected / Not Listed As Edges

- Wire crossings without junction dots were not connected, following note 5 on the drawing.
- Title block, revision table, notes, legend, and cable/feed schedule text were not treated as nodes.
- Direct all-to-all edges among loads on the same MCC or load-center bus were not emitted; bus nodes (`LC-480*`, `MCC-*`, `BUS-4*`, `DC-BUS-*`) carry that shared connectivity.
- Direct `BAT-125* -- DC-BUS-*` edges were not listed because the visible path runs through `CHG-125*`.
- Direct `LC-480* -- CHG-125*` AC-input edges were not listed because no ordinary solid conductor is clearly visible from the LC bus to the charger symbol; the charger/DC-bus/battery path is retained instead.
- Components that are visually close but separated by non-junction crossings or gaps were not connected.
"""
notes_path.write_text(notes, encoding="utf-8")

confidence_counts = Counter(e["confidence"] for e in edges)
kind_counts = Counter(e["kind"] for e in edges)
added_count = sum(1 for r in node_rows if r["action"].startswith("add_"))
correction_count = len(node_rows) - added_count
counts = {
    "document": 13,
    "existing_component_nodes_from_component_visual_ocr_labels": len(component_rows),
    "added_node_count": added_count,
    "correction_or_interpretation_row_count": correction_count,
    "node_additions_corrections_rows": len(node_rows),
    "final_proposed_unique_node_count": len(component_rows) + added_count,
    "edge_count": len(edges),
    "edge_confidence_counts": dict(sorted(confidence_counts.items())),
    "edge_kind_counts": dict(sorted(kind_counts.items())),
    "uncertain_edge_count_low_confidence": confidence_counts.get("low", 0),
    "output_files": {
        "node_additions_corrections": node_path.name,
        "edge_list": edge_path.name,
        "uncertain_rejected_notes": notes_path.name,
        "final_counts": counts_path.name,
    },
}
counts_path.write_text(json.dumps(counts, indent=2, sort_keys=True) + "\n", encoding="utf-8")

print(json.dumps(counts, indent=2, sort_keys=True))
