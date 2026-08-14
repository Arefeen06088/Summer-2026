import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\22")
ART = BASE / "Codes and artifacts"
OUT = BASE / "Results" / "Iteration_1"

COMPONENT_CSV = ART / "component_labels_list.csv"
MATRIX_CSV = OUT / "round_01_diego_matrix.csv"
NOTES_MD = OUT / "round_01_diego_notes.md"


BUS_NODES = [
    "BUS-13A",
    "BUS-13B",
    "BUS-4160-A",
    "BUS-4160-B",
    "BUS-4160-C",
    "BUS-4160-D",
    "BUS-480-A",
    "BUS-480-B",
    "BUS-480-C",
    "BUS-480-D",
    "BUS-125A",
    "BUS-125B",
    "BUS-UPS-A",
    "BUS-UPS-B",
]

RAW_VISIBLE_EXTRA_COMPONENTS = [
    "INST-PT-D",
    "CB-CH-D",
    "CB-VLV1-D",
    "CB-VLV2-D",
    "CB-SPARE-D",
]


def e(a, b):
    return tuple(sorted((a, b)))


edge_groups = {
    "Top generation, switchyard, 13.8 kV aux buses": [
        e("GEN-G01", "GSU-T01"),
        e("GSU-T01", "SWYD-345"),
        e("SWYD-345", "CB-13A1"),
        e("CB-13A1", "BUS-13A"),
        e("SWYD-345", "CB-13B1"),
        e("CB-13B1", "BUS-13B"),
        e("CB-13T", "BUS-13A"),
        e("CB-13T", "BUS-13B"),
        e("BUS-13A", "AUX-XFMR-1A"),
        e("AUX-XFMR-1A", "CB-4A-IN"),
        e("CB-4A-IN", "BUS-4160-A"),
        e("BUS-13A", "AUX-XFMR-1B"),
        e("AUX-XFMR-1B", "CB-4B-IN"),
        e("CB-4B-IN", "BUS-4160-B"),
        e("BUS-13B", "SAT-XFMR-1C"),
        e("SAT-XFMR-1C", "CB-4C-IN"),
        e("CB-4C-IN", "BUS-4160-C"),
        e("BUS-13B", "SAT-XFMR-1D"),
        e("SAT-XFMR-1D", "CB-4D-IN"),
        e("CB-4D-IN", "BUS-4160-D"),
        e("BUS-13A", "RELAY-87U"),
        e("RELAY-87U", "CB-4B-IN"),
        e("SYNC-PNL-1", "BUS-4160-A"),
        e("SYNC-PNL-1", "CB-DG-A"),
    ],
    "4160 V safety buses, DG feeders, ties, load-center transformers": [
        e("DG-1A", "CB-DG-A"),
        e("CB-DG-A", "BUS-4160-A"),
        e("CB-4AB-TIE", "BUS-4160-A"),
        e("CB-4AB-TIE", "BUS-4160-B"),
        e("CB-LC-A", "BUS-4160-A"),
        e("CB-LC-A", "TR-LC-A"),
        e("TR-LC-A", "BUS-480-A"),
        e("DG-1B", "CB-DG-B"),
        e("CB-DG-B", "BUS-4160-B"),
        e("CB-LC-B", "BUS-4160-B"),
        e("CB-LC-B", "TR-LC-B"),
        e("TR-LC-B", "BUS-480-B"),
        e("DG-1C", "CB-DG-C"),
        e("CB-DG-C", "BUS-4160-C"),
        e("CB-4CD-TIE", "BUS-4160-C"),
        e("CB-4CD-TIE", "BUS-4160-D"),
        e("CB-LC-C", "BUS-4160-C"),
        e("CB-LC-C", "TR-LC-C"),
        e("TR-LC-C", "BUS-480-C"),
        e("DG-1D", "CB-DG-D"),
        e("CB-DG-D", "BUS-4160-D"),
        e("CB-LC-D", "BUS-4160-D"),
        e("CB-LC-D", "TR-LC-D"),
        e("TR-LC-D", "BUS-480-D"),
    ],
    "480 V load centers and MCC/load branches": [],
    "120 V transformers, panels, relays, junction boxes, terminal blocks": [],
    "125 VDC and UPS buses": [
        e("BUS-480-A", "CB-DC-A1"),
        e("CB-DC-A1", "CHGR-125A"),
        e("CHGR-125A", "BUS-125A"),
        e("BUS-125A", "BAT-125A"),
        e("BUS-125A", "FUSE-FD-A"),
        e("FUSE-FD-A", "INV-UPS-A"),
        e("INV-UPS-A", "BUS-UPS-A"),
        e("BUS-125A", "DC-MCC-A"),
        e("DC-MCC-A", "SOL-SDV-A"),
        e("BUS-125A", "DIODE-OR-A"),
        e("BUS-125A", "GRD-DC-A"),
        e("BUS-UPS-A", "INST-RACK-A"),
        e("BUS-UPS-A", "PNL-RPS-A"),
        e("BUS-UPS-A", "PLC-SAF-A"),
        e("BUS-UPS-A", "ANN-PNL-CR"),
        e("PNL-RPS-A", "RELAY-RPS-A1"),
        e("PNL-RPS-A", "RELAY-ESF-A"),
        e("ANN-PNL-CR", "JB-CR-01"),
        e("JB-CR-01", "TERM-MTB-A"),
        e("JB-CR-01", "TERM-MTB-B"),
        e("BUS-480-B", "CB-DC-B1"),
        e("CB-DC-B1", "CHGR-125B"),
        e("CHGR-125B", "BUS-125B"),
        e("BUS-125B", "BAT-125B"),
        e("BUS-125B", "FUSE-FD-B"),
        e("FUSE-FD-B", "INV-UPS-B"),
        e("INV-UPS-B", "BUS-UPS-B"),
        e("BUS-125B", "DC-MCC-B"),
        e("DC-MCC-B", "SOL-SDV-B"),
        e("BUS-125B", "DIODE-OR-B"),
        e("BUS-125B", "GRD-DC-B"),
        e("BUS-UPS-B", "INST-RACK-B"),
        e("BUS-UPS-B", "PNL-RPS-B"),
        e("BUS-UPS-B", "PLC-SAF-B"),
        e("BUS-UPS-B", "REC-SEQ-1"),
        e("PNL-RPS-B", "RELAY-RPS-B1"),
        e("PNL-RPS-B", "RELAY-ESF-B"),
        e("XFMR-PT-1", "METER-V01"),
        e("XFMR-PT-1", "METER-A01"),
    ],
}


train_cfg = {
    "A": {
        "bus": "BUS-480-A",
        "pt": "INST-PT-A",
        "mcc_a": "MCC-AA",
        "mcc_b": "MCC-AB",
        "cb_mcc_a": "CB-MCC-AA",
        "cb_mcc_b": "CB-MCC-AB",
        "xfmr": "XFMR-120-A",
        "gnd": "GND-A",
        "ct": "INST-CT-A",
        "rhr": ("CB-RHR-A", "PUMP-RHR-A"),
        "si": ("CB-SI-A", "PUMP-SI-A"),
        "ccw": ("CB-CCW-A", "PUMP-CCW-A"),
        "fan": ("CB-FAN-A", "FAN-CR-A"),
        "ch": ("CB-CH-A", "CHILLER-A"),
        "vlv1": ("CB-VLV1-A", "MOV-HV1-A"),
        "vlv2": ("CB-VLV2-A", "MOV-HV2-A"),
        "spare": ("CB-SPARE-A", "SPARE-LOAD-A"),
        "panel": "PNL-120-A",
        "relays": ("RELAY-KA1", "RELAY-KA2"),
        "jb": "JB-A1",
        "term": "TERM-A",
    },
    "B": {
        "bus": "BUS-480-B",
        "pt": "INST-PT-B",
        "mcc_a": "MCC-BA",
        "mcc_b": "MCC-BB",
        "cb_mcc_a": "CB-MCC-BA",
        "cb_mcc_b": "CB-MCC-BB",
        "xfmr": "XFMR-120-B",
        "gnd": "GND-B",
        "ct": "INST-CT-B",
        "rhr": ("CB-RHR-B", "PUMP-RHR-B"),
        "si": ("CB-SI-B", "PUMP-SI-B"),
        "ccw": ("CB-CCW-B", "PUMP-CCW-B"),
        "fan": ("CB-FAN-B", "FAN-CR-B"),
        "ch": ("CB-CH-B", "CHILLER-B"),
        "vlv1": ("CB-VLV1-B", "MOV-HV1-B"),
        "vlv2": ("CB-VLV2-B", "MOV-HV2-B"),
        "spare": ("CB-SPARE-B", "SPARE-LOAD-B"),
        "panel": "PNL-120-B",
        "relays": ("RELAY-KB1", "RELAY-KB2"),
        "jb": "JB-B1",
        "term": "TERM-B",
    },
    "C": {
        "bus": "BUS-480-C",
        "pt": "INST-PT-C",
        "mcc_a": "MCC-CA",
        "mcc_b": "MCC-CB",
        "cb_mcc_a": "CB-MCC-CA",
        "cb_mcc_b": "CB-MCC-CB",
        "xfmr": "XFMR-120-C",
        "gnd": "GND-C",
        "ct": "INST-CT-C",
        "rhr": ("CB-RHR-C", "PUMP-RHR-C"),
        "si": ("CB-SI-C", "PUMP-SI-C"),
        "ccw": ("CB-CCW-C", "PUMP-CCW-C"),
        "fan": ("CB-FAN-C", "FAN-CR-C"),
        "ch": ("CB-CH-C", "CHILLER-C"),
        "vlv1": ("CB-VLV1-C", "MOV-HV1-C"),
        "vlv2": ("CB-VLV2-C", "MOV-HV2-C"),
        "spare": ("CB-SPARE-C", "SPARE-LOAD-C"),
        "panel": "PNL-120-C",
        "relays": ("RELAY-KC1", "RELAY-KC2"),
        "jb": "JB-C1",
        "term": "TERM-C",
    },
    "D": {
        "bus": "BUS-480-D",
        "pt": "INST-PT-D",
        "mcc_a": "MCC-DA",
        "mcc_b": "MCC-DB",
        "cb_mcc_a": "CB-MCC-DA",
        "cb_mcc_b": "CB-MCC-DB",
        "xfmr": "XFMR-120-D",
        "gnd": "GND-D",
        "ct": "INST-CT-D",
        "rhr": ("CB-RHR-D", "PUMP-RHR-D"),
        "si": ("CB-SI-D", "PUMP-SI-D"),
        "ccw": ("CB-CCW-D", "PUMP-CCW-D"),
        "fan": ("CB-FAN-D", "FAN-CR-D"),
        "ch": ("CB-CH-D", "CHILLER-D"),
        "vlv1": ("CB-VLV1-D", "MOV-HV1-D"),
        "vlv2": ("CB-VLV2-D", "MOV-HV2-D"),
        "spare": ("CB-SPARE-D", "SPARE-LOAD-D"),
        "panel": "PNL-120-D",
        "relays": ("RELAY-KD1", "RELAY-KD2"),
        "jb": "JB-D1",
        "term": "TERM-D",
    },
}

for div, cfg in train_cfg.items():
    mcc_edges = edge_groups["480 V load centers and MCC/load branches"]
    mcc_edges.extend(
        [
            e(cfg["bus"], cfg["pt"]),
            e(cfg["bus"], cfg["cb_mcc_a"]),
            e(cfg["cb_mcc_a"], cfg["mcc_a"]),
            e(cfg["bus"], cfg["cb_mcc_b"]),
            e(cfg["cb_mcc_b"], cfg["mcc_b"]),
            e(cfg["bus"], cfg["xfmr"]),
            e(cfg["bus"], cfg["gnd"]),
            e(cfg["mcc_a"], cfg["ct"]),
            e(cfg["ct"], cfg["rhr"][0]),
            e(cfg["mcc_a"], cfg["si"][0]),
            e(cfg["mcc_a"], cfg["ccw"][0]),
            e(cfg["mcc_a"], cfg["fan"][0]),
            e(cfg["mcc_b"], cfg["ch"][0]),
            e(cfg["mcc_b"], cfg["vlv1"][0]),
            e(cfg["mcc_b"], cfg["vlv2"][0]),
            e(cfg["mcc_b"], cfg["spare"][0]),
            e(cfg["rhr"][0], cfg["rhr"][1]),
            e(cfg["si"][0], cfg["si"][1]),
            e(cfg["ccw"][0], cfg["ccw"][1]),
            e(cfg["fan"][0], cfg["fan"][1]),
            e(cfg["ch"][0], cfg["ch"][1]),
            e(cfg["vlv1"][0], cfg["vlv1"][1]),
            e(cfg["vlv2"][0], cfg["vlv2"][1]),
            e(cfg["spare"][0], cfg["spare"][1]),
            e(cfg["rhr"][0], cfg["si"][0]),
        ]
    )

    panel_edges = edge_groups[
        "120 V transformers, panels, relays, junction boxes, terminal blocks"
    ]
    panel_edges.extend(
        [
            e(cfg["xfmr"], cfg["panel"]),
            e(cfg["panel"], cfg["relays"][0]),
            e(cfg["panel"], cfg["relays"][1]),
            e(cfg["panel"], cfg["jb"]),
            e(cfg["jb"], cfg["term"]),
        ]
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    with COMPONENT_CSV.open(newline="", encoding="utf-8") as f:
        inventory_nodes = [row["final_label"] for row in csv.DictReader(f)]

    nodes = inventory_nodes + RAW_VISIBLE_EXTRA_COMPONENTS + BUS_NODES
    if len(nodes) != len(set(nodes)):
        dupes = sorted({n for n in nodes if nodes.count(n) > 1})
        raise RuntimeError(f"Duplicate nodes: {dupes}")

    all_edges = set()
    for group_edges in edge_groups.values():
        all_edges.update(group_edges)

    node_set = set(nodes)
    missing = sorted({p for edge in all_edges for p in edge if p not in node_set})
    if missing:
        raise RuntimeError(f"Edge endpoint(s) missing from node list: {missing}")

    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in sorted(all_edges):
        ia, ib = index[a], index[b]
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1

    with MATRIX_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name"] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)

    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    isolated = [node for node, row in zip(nodes, matrix) if sum(row) == 0]

    notes = []
    notes.append("# Round 01 Diego Connectivity Notes")
    notes.append("")
    notes.append("## Source Boundary")
    notes.append("")
    notes.append(
        "Used only doc 22 raw/derived resources in `Input resources` and raw-derived inspection crops in `Codes and artifacts/inspection_crops`. Ground truth, evaluator output, metric feedback, and GT-derived files were not opened or used."
    )
    notes.append("")
    notes.append("## Node List Rationale")
    notes.append("")
    notes.append(
        f"- Started from the 181 physical-component labels in `component_labels_list.csv`."
    )
    notes.append(
        "- Added 14 raw-visible printed logical bus nodes: "
        + ", ".join(BUS_NODES)
        + "."
    )
    notes.append(
        "- Added 5 raw-visible D-train components absent from the prepared inventory: "
        + ", ".join(RAW_VISIBLE_EXTRA_COMPONENTS)
        + ". These are visible in the raw right-edge 480 V train D area; the added crop `19_480_train_d_right_raw.png` documents the four D-side load breakers, and `18_inst_pt_d_raw.png` documents `INST-PT-D`."
    )
    notes.append(
        "- Did not add WN-* wire nodes, unlabeled junction dots, drawing titles, note text, voltage descriptions, or dashed section boundaries."
    )
    notes.append("")
    notes.append("## Edge Evidence By Area")
    notes.append("")
    for group_name, group_edges in edge_groups.items():
        notes.append(f"### {group_name}")
        notes.append("")
        for a, b in sorted(set(group_edges)):
            notes.append(f"- `{a}` -- `{b}`")
        notes.append("")

    notes.append("## Uncertain / High-Recall Candidates")
    notes.append("")
    notes.append(
        "- Included `BUS-13A` -- `RELAY-87U` and `RELAY-87U` -- `CB-4B-IN` because the raw crop shows a dashed protection/control path from the 13.8 kV bus area down through relay 87U toward the 4B incoming breaker."
    )
    notes.append(
        "- Included `SYNC-PNL-1` -- `BUS-4160-A` and `SYNC-PNL-1` -- `CB-DG-A` because the dashed synchronizing panel path visibly terminates at the 4160 A / DG-A area."
    )
    notes.append(
        "- Included short dashed `CB-RHR-*` -- `CB-SI-*` links in each 480 V train. The longer dashed continuation below the SI pumps was left out as a matrix edge because its named endpoint is not visually unambiguous."
    )
    notes.append(
        "- Included `BUS-480-A` -- `CB-DC-A1` and `BUS-480-B` -- `CB-DC-B1` as long solid charger supply runs. They are less local than most bus taps but are traceable in the raw lower section."
    )
    notes.append(
        "- Did not connect line crossings without dots. Printed buses are represented as bus nodes, so components on the same printed bus attach to the bus node rather than being expanded into pairwise cliques."
    )
    notes.append("")
    notes.append("## Validation Summary")
    notes.append("")
    notes.append(f"- Node count: {len(nodes)}")
    notes.append(f"- Edge count: {len(all_edges)}")
    notes.append(f"- Symmetric: {symmetric}")
    notes.append(f"- Diagonal zero: {diagonal_zero}")
    notes.append(
        "- Isolated nodes: " + (", ".join(f"`{n}`" for n in isolated) if isolated else "none")
    )
    notes.append("")

    NOTES_MD.write_text("\n".join(notes), encoding="utf-8")

    print(f"matrix={MATRIX_CSV}")
    print(f"notes={NOTES_MD}")
    print(f"nodes={len(nodes)} edges={len(all_edges)} symmetric={symmetric} diagonal_zero={diagonal_zero} isolated={isolated}")


if __name__ == "__main__":
    main()
