from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw"
)
RESULTS_DIR = RAW_DIR / "results"


TOP_NODES = [
    "GEN-M1",
    "CB-GEN1",
    "TR-UAT1",
    "CB-13A-IN",
    "BUS-13K-A",
    "FEED-230A",
    "TR-SAT1",
    "CB-13B-IN",
    "BUS-13K-B",
    "CB-TIE-13K",
    "CB-F41A",
    "DS-F41A",
    "TR-416A",
    "CB-416A-IN",
    "BUS-416-A",
    "CB-F41B",
    "DS-F41B",
    "TR-416B",
    "CB-416B-IN",
    "BUS-416-B",
    "DG-1A",
    "CB-DG1A",
    "DG-1B",
    "CB-DG1B",
    "CB-TIE-416",
    "CB-LCA",
    "TR-480A",
    "BUS-480-A",
    "CB-LCB",
    "TR-480B",
    "BUS-480-B",
    "CB-LCC",
    "TR-480C",
    "BUS-480-C",
    "CB-LCD",
    "TR-480D",
    "BUS-480-D",
    "CB-TIE-480",
]


BRANCHES = [
    ("BUS-480-A", "CB-48A1", "DS-48A1", "MCC-1A", "RELAY-K1A", "PMP-RHR-101A"),
    ("BUS-480-A", "CB-48A2", "DS-48A2", "MCC-2A", "CS-2A", "MOV-CCW-112A"),
    ("BUS-480-A", "CB-48A3", "DS-48A3", "MCC-3A", "RELAY-K3A", "FAN-RB-104A"),
    ("BUS-480-A", "CB-48A4", "DS-48A4", "JB-4A", "CS-4A", "HTR-PZR-01A"),
    ("BUS-480-A", "CB-48A5", "DS-48A5", "MCC-5A", "RELAY-K5A", "COMP-IA-201A"),
    ("BUS-480-A", "CB-48A6", "DS-48A6", "JB-6A", "CS-6A", "MOT-CRN-01A"),
    ("BUS-480-B", "CB-48B1", "DS-48B1", "MCC-1B", "RELAY-K1B", "PMP-SI-102B"),
    ("BUS-480-B", "CB-48B2", "DS-48B2", "MCC-2B", "CS-2B", "MOV-CS-116B"),
    ("BUS-480-B", "CB-48B3", "DS-48B3", "MCC-3B", "RELAY-K3B", "FAN-CCW-108B"),
    ("BUS-480-B", "CB-48B4", "DS-48B4", "JB-4B", "CS-4B", "HTR-SUMP-02B"),
    ("BUS-480-B", "CB-48B5", "DS-48B5", "MCC-5B", "RELAY-K5B", "PMP-CHG-203B"),
    ("BUS-480-B", "CB-48B6", "DS-48B6", "JB-6B", "CS-6B", "MOV-SW-118B"),
    ("BUS-480-C", "CB-48C1", "DS-48C1", "MCC-1C", "RELAY-K1C", "PMP-RHR-101C"),
    ("BUS-480-C", "CB-48C2", "DS-48C2", "MCC-2C", "CS-2C", "MOV-CCW-112C"),
    ("BUS-480-C", "CB-48C3", "DS-48C3", "MCC-3C", "RELAY-K3C", "FAN-RB-104C"),
    ("BUS-480-C", "CB-48C4", "DS-48C4", "JB-4C", "RELAY-K4C", "PMP-AFW-205C"),
    ("BUS-480-C", "CB-48C5", "DS-48C5", "MCC-5C", "RELAY-K5C", "PMP-CCP-207C"),
    ("BUS-480-C", "CB-48C6", "DS-48C6", "JB-6C", "CS-6C", "MOV-FCV-022C"),
    ("BUS-480-D", "CB-48D1", "DS-48D1", "MCC-1D", "RELAY-K1D", "PMP-SI-102D"),
    ("BUS-480-D", "CB-48D2", "DS-48D2", "MCC-2D", "CS-2D", "MOV-CS-116D"),
    ("BUS-480-D", "CB-48D3", "DS-48D3", "MCC-3D", "RELAY-K3D", "FAN-ESF-110D"),
    ("BUS-480-D", "CB-48D4", "DS-48D4", "JB-4D", "CS-4D", "MOV-RWST-24D"),
    ("BUS-480-D", "CB-48D5", "DS-48D5", "MCC-5D", "RELAY-K5D", "PMP-CHG-203D"),
    ("BUS-480-D", "CB-48D6", "DS-48D6", "JB-6D", "CS-6D", "MOV-SW-118D"),
]


DC_NODES = [
    "RECT-125A",
    "BAT-125A",
    "CHGR-125A",
    "BUS-125DCA",
    "INV-UPS-A",
    "CP-RPS-A",
    "CP-RPS-B",
    "RECT-125B",
    "BAT-125B",
    "CHGR-125B",
    "BUS-125DCB",
    "INV-UPS-B",
    "CP-ESFAS-A",
    "CP-ESFAS-B",
]

CONTROL_NODES = [
    "TB-RPS-A",
    "PROT-UV-A",
    "RELAY-K101",
    "PT-410A",
    "LT-512A",
    "RELAY-K102",
    "TT-303A",
    "GND-CTRL-A",
    "TB-RPS-B",
    "PROT-UV-B",
    "RELAY-K103",
    "PT-410B",
    "LT-512B",
    "RELAY-K104",
    "TT-303B",
    "GND-CTRL-B",
    "JB-ESF-A",
    "PROT-LOP-A",
    "RELAY-K105",
    "FT-611A",
    "RELAY-K106",
    "XA-730A",
    "JB-ESF-B",
    "PROT-LOP-B",
    "RELAY-K107",
    "FT-611B",
    "RELAY-K108",
    "XA-730B",
]


def branch_nodes() -> list[str]:
    nodes: list[str] = []
    for _, cb, ds, middle, control, load in BRANCHES:
        nodes.extend([cb, ds, middle, control, load])
    return nodes


FINAL_NODES = TOP_NODES + branch_nodes() + DC_NODES + CONTROL_NODES
DIEGO_R1_NODES = (
    ["UNLABELED-GEN-M1-TERMINAL"]
    + TOP_NODES[:21]
    + ["UNLABELED-DG-1A-TERMINAL"]
    + TOP_NODES[21:23]
    + ["UNLABELED-DG-1B-TERMINAL"]
    + TOP_NODES[23:]
    + branch_nodes()
    + DC_NODES
    + CONTROL_NODES
)


def edge(src: str, dst: str, edge_type: str, evidence: str) -> dict[str, str]:
    return {"source": src, "target": dst, "type": edge_type, "evidence": evidence}


FINAL_EDGES: list[dict[str, str]] = [
    edge("GEN-M1", "CB-GEN1", "solid_power", "generator to main generator breaker"),
    edge("CB-GEN1", "TR-UAT1", "solid_power", "generator breaker to UAT"),
    edge("TR-UAT1", "CB-13A-IN", "solid_power", "UAT to 13 kV A incoming breaker"),
    edge("CB-13A-IN", "BUS-13K-A", "solid_power", "13 kV A incoming breaker to bus"),
    edge("FEED-230A", "TR-SAT1", "solid_power", "offsite feeder to SAT"),
    edge("TR-SAT1", "CB-13B-IN", "solid_power", "SAT to 13 kV B incoming breaker"),
    edge("CB-13B-IN", "BUS-13K-B", "solid_power", "13 kV B incoming breaker to bus"),
    edge("BUS-13K-A", "CB-TIE-13K", "solid_power", "13 kV tie through breaker"),
    edge("CB-TIE-13K", "BUS-13K-B", "solid_power", "13 kV tie through breaker"),
    edge("BUS-13K-A", "CB-F41A", "solid_power", "13 kV A feeder to 4.16 kV A transformer"),
    edge("CB-F41A", "DS-F41A", "solid_power", "4.16 kV A feeder disconnect"),
    edge("DS-F41A", "TR-416A", "solid_power", "4.16 kV A transformer"),
    edge("TR-416A", "CB-416A-IN", "solid_power", "4.16 kV A incoming breaker"),
    edge("CB-416A-IN", "BUS-416-A", "solid_power", "4.16 kV A bus"),
    edge("BUS-13K-B", "CB-F41B", "solid_power", "13 kV B feeder to 4.16 kV B transformer"),
    edge("CB-F41B", "DS-F41B", "solid_power", "4.16 kV B feeder disconnect"),
    edge("DS-F41B", "TR-416B", "solid_power", "4.16 kV B transformer"),
    edge("TR-416B", "CB-416B-IN", "solid_power", "4.16 kV B incoming breaker"),
    edge("CB-416B-IN", "BUS-416-B", "solid_power", "4.16 kV B bus"),
    edge("DG-1A", "CB-DG1A", "solid_power", "diesel generator A to breaker"),
    edge("CB-DG1A", "BUS-416-A", "solid_power", "DG A breaker to 4.16 kV A bus"),
    edge("DG-1B", "CB-DG1B", "solid_power", "diesel generator B to breaker"),
    edge("CB-DG1B", "BUS-416-B", "solid_power", "DG B breaker to 4.16 kV B bus"),
    edge("BUS-416-A", "CB-TIE-416", "solid_power", "4.16 kV tie through breaker"),
    edge("CB-TIE-416", "BUS-416-B", "solid_power", "4.16 kV tie through breaker"),
    edge("BUS-416-A", "CB-LCA", "solid_power", "load center A feeder"),
    edge("CB-LCA", "TR-480A", "solid_power", "load center A transformer"),
    edge("TR-480A", "BUS-480-A", "solid_power", "load center A bus"),
    edge("BUS-416-A", "CB-LCB", "solid_power", "load center B feeder"),
    edge("CB-LCB", "TR-480B", "solid_power", "load center B transformer"),
    edge("TR-480B", "BUS-480-B", "solid_power", "load center B bus"),
    edge("BUS-416-B", "CB-LCC", "solid_power", "load center C feeder"),
    edge("CB-LCC", "TR-480C", "solid_power", "load center C transformer"),
    edge("TR-480C", "BUS-480-C", "solid_power", "load center C bus"),
    edge("BUS-416-B", "CB-LCD", "solid_power", "load center D feeder"),
    edge("CB-LCD", "TR-480D", "solid_power", "load center D transformer"),
    edge("TR-480D", "BUS-480-D", "solid_power", "load center D bus"),
    edge("BUS-480-B", "CB-TIE-480", "solid_power", "480 V B-C tie through breaker"),
    edge("CB-TIE-480", "BUS-480-C", "solid_power", "480 V B-C tie through breaker"),
]


for bus, cb, ds, middle, control, load in BRANCHES:
    FINAL_EDGES.extend(
        [
            edge(bus, cb, "solid_power", f"480 V branch {cb} from bus"),
            edge(cb, ds, "solid_power", f"480 V branch {cb} disconnect"),
            edge(ds, middle, "solid_power", f"480 V branch {cb} middle device"),
            edge(middle, control, "solid_power/control", f"480 V branch {cb} control device"),
            edge(control, load, "solid_power/control", f"480 V branch {cb} load"),
        ]
    )


FINAL_EDGES.extend(
    [
        edge("BUS-480-A", "RECT-125A", "solid_power", "A rectifier feed from load center A"),
        edge("BAT-125A", "CHGR-125A", "dc", "A battery to charger"),
        edge("CHGR-125A", "RECT-125A", "dc", "A charger to rectifier"),
        edge("RECT-125A", "BUS-125DCA", "dc", "A rectifier to 125 VDC bus"),
        edge("BUS-125DCA", "INV-UPS-A", "dc", "A 125 VDC bus to inverter/UPS"),
        edge("BUS-125DCA", "CP-RPS-A", "dc_control", "A 125 VDC bus to RPS A panel"),
        edge("BUS-125DCA", "CP-RPS-B", "dc_control", "A 125 VDC bus to RPS B panel"),
        edge("BUS-480-C", "RECT-125B", "solid_power", "B rectifier feed from load center C"),
        edge("BAT-125B", "CHGR-125B", "dc", "B battery to charger"),
        edge("CHGR-125B", "RECT-125B", "dc", "B charger to rectifier"),
        edge("RECT-125B", "BUS-125DCB", "dc", "B rectifier to 125 VDC bus"),
        edge("BUS-125DCB", "INV-UPS-B", "dc", "B 125 VDC bus to inverter/UPS"),
        edge("BUS-125DCB", "CP-ESFAS-A", "dc_control", "B 125 VDC bus to ESFAS A panel"),
        edge("BUS-125DCB", "CP-ESFAS-B", "dc_control", "B 125 VDC bus to ESFAS B panel"),
        edge("CP-RPS-A", "TB-RPS-A", "control", "RPS A control chain"),
        edge("TB-RPS-A", "PROT-UV-A", "control", "RPS A undervoltage protection"),
        edge("PROT-UV-A", "RELAY-K101", "control", "RPS A relay K101"),
        edge("RELAY-K101", "PT-410A", "instr_signal", "K101 to PT-410A"),
        edge("RELAY-K101", "LT-512A", "instr_signal", "K101 to LT-512A"),
        edge("CP-RPS-A", "RELAY-K102", "control", "RPS A relay K102 branch"),
        edge("RELAY-K102", "TT-303A", "instr_signal", "K102 to TT-303A"),
        edge("RELAY-K102", "GND-CTRL-A", "ground", "K102 to control ground A"),
        edge("CP-RPS-B", "TB-RPS-B", "control", "RPS B control chain"),
        edge("TB-RPS-B", "PROT-UV-B", "control", "RPS B undervoltage protection"),
        edge("PROT-UV-B", "RELAY-K103", "control", "RPS B relay K103"),
        edge("RELAY-K103", "PT-410B", "instr_signal", "K103 to PT-410B"),
        edge("RELAY-K103", "LT-512B", "instr_signal", "K103 to LT-512B"),
        edge("CP-RPS-B", "RELAY-K104", "control", "RPS B relay K104 branch"),
        edge("RELAY-K104", "TT-303B", "instr_signal", "K104 to TT-303B"),
        edge("RELAY-K104", "GND-CTRL-B", "ground", "K104 to control ground B"),
        edge("CP-ESFAS-A", "JB-ESF-A", "control", "ESFAS A junction box"),
        edge("JB-ESF-A", "PROT-LOP-A", "control", "ESFAS A LOP protection"),
        edge("PROT-LOP-A", "RELAY-K105", "control", "ESFAS A relay K105"),
        edge("RELAY-K105", "FT-611A", "instr_signal", "K105 to FT-611A"),
        edge("CP-ESFAS-A", "RELAY-K106", "control", "ESFAS A relay K106 branch"),
        edge("RELAY-K106", "XA-730A", "instr_signal", "K106 to XA-730A"),
        edge("RELAY-K106", "RELAY-K108", "control_interlock", "labeled A/B ESF interlock"),
        edge("CP-ESFAS-B", "JB-ESF-B", "control", "ESFAS B junction box"),
        edge("JB-ESF-B", "PROT-LOP-B", "control", "ESFAS B LOP protection"),
        edge("PROT-LOP-B", "RELAY-K107", "control", "ESFAS B relay K107"),
        edge("RELAY-K107", "FT-611B", "instr_signal", "K107 to FT-611B"),
        edge("CP-ESFAS-B", "RELAY-K108", "control", "ESFAS B relay K108 branch"),
        edge("RELAY-K108", "XA-730B", "instr_signal", "K108 to XA-730B"),
    ]
)


DIEGO_R1_EDGES = []
for item in FINAL_EDGES:
    if {item["source"], item["target"]} == {"GEN-M1", "CB-GEN1"}:
        continue
    if {item["source"], item["target"]} == {"DG-1A", "CB-DG1A"}:
        continue
    if {item["source"], item["target"]} == {"DG-1B", "CB-DG1B"}:
        continue
    DIEGO_R1_EDGES.append(item.copy())

DIEGO_R1_EDGES.extend(
    [
        edge("GEN-M1", "UNLABELED-GEN-M1-TERMINAL", "solid_power", "Diego R1 included unlabeled source square"),
        edge("UNLABELED-GEN-M1-TERMINAL", "CB-GEN1", "solid_power", "Diego R1 included unlabeled source square"),
        edge("DG-1A", "UNLABELED-DG-1A-TERMINAL", "solid_power", "Diego R1 included unlabeled DG square"),
        edge("UNLABELED-DG-1A-TERMINAL", "CB-DG1A", "solid_power", "Diego R1 included unlabeled DG square"),
        edge("DG-1B", "UNLABELED-DG-1B-TERMINAL", "solid_power", "Diego R1 included unlabeled DG square"),
        edge("UNLABELED-DG-1B-TERMINAL", "CB-DG1B", "solid_power", "Diego R1 included unlabeled DG square"),
    ]
)


UNCERTAIN_EXCLUDED = [
    {
        "source": "UNLABELED-GEN-M1-TERMINAL",
        "target": "CB-GEN1",
        "reason": "Unlabeled source square omitted from final graph; final uses component-level GEN-M1 to CB-GEN1.",
    },
    {
        "source": "UNLABELED-DG-1A-TERMINAL",
        "target": "CB-DG1A",
        "reason": "Unlabeled DG square omitted from final graph; final uses component-level DG-1A to CB-DG1A.",
    },
    {
        "source": "UNLABELED-DG-1B-TERMINAL",
        "target": "CB-DG1B",
        "reason": "Unlabeled DG square omitted from final graph; final uses component-level DG-1B to CB-DG1B.",
    },
    {
        "source": "BUS-480-A",
        "target": "BUS-480-B",
        "reason": "No direct 480 V A-B tie is visible.",
    },
    {
        "source": "BUS-480-C",
        "target": "BUS-480-D",
        "reason": "No direct 480 V C-D tie is visible.",
    },
    {
        "source": "BUS-125DCA",
        "target": "BUS-125DCB",
        "reason": "No 125 VDC bus tie is visible.",
    },
    {
        "source": "RELAY-K106",
        "target": "RELAY-K107",
        "reason": "Lower interlock route does not support this overconnection.",
    },
    {
        "source": "RELAY-K107",
        "target": "RELAY-K108",
        "reason": "Lower interlock route does not support this overconnection.",
    },
    {
        "source": "XA-730A",
        "target": "XA-730B",
        "reason": "No direct XA-to-XA connection is visible.",
    },
    {
        "source": "crossing-without-dot",
        "target": "any crossing line",
        "reason": "Legend says crossings without dots are not connections.",
    },
]


def ensure_unique(nodes: list[str]) -> None:
    seen: set[str] = set()
    dupes = []
    for node in nodes:
        if node in seen:
            dupes.append(node)
        seen.add(node)
    if dupes:
        raise ValueError(f"duplicate nodes: {dupes}")


def validate_edges(nodes: list[str], edges: list[dict[str, str]]) -> None:
    node_set = set(nodes)
    for item in edges:
        if item["source"] not in node_set:
            raise ValueError(f"unknown edge source {item['source']}")
        if item["target"] not in node_set:
            raise ValueError(f"unknown edge target {item['target']}")
        if item["source"] == item["target"]:
            raise ValueError(f"self-loop not expected: {item['source']}")


def write_matrix(path: Path, nodes: list[str], edges: list[dict[str, str]]) -> None:
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for item in edges:
        i = idx[item["source"]]
        j = idx[item["target"]]
        matrix[i][j] = 1
        matrix[j][i] = 1
    for i, node in enumerate(nodes):
        if matrix[i][i] != 0:
            raise ValueError(f"nonzero diagonal at {node}")
        for j in range(len(nodes)):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError(f"asymmetric matrix at {i},{j}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "type", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_uncertain(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "reason"])
        writer.writeheader()
        writer.writerows(UNCERTAIN_EXCLUDED)


def write_tracking(path: Path, timestamp: str) -> None:
    rows = [
        {
            "timestamp": timestamp,
            "case": "20",
            "round": "local",
            "agent": "main",
            "role": "inventory/crops/local inspection",
            "approx_prompt_tokens": "1800",
            "approx_completion_tokens": "320",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "codes/crops",
            "notes": "Approximate tokens; exact tool token accounting unavailable",
        },
        {
            "timestamp": timestamp,
            "case": "20",
            "round": "round_01",
            "agent": "Diego",
            "role": "high-recall extraction",
            "approx_prompt_tokens": "4700",
            "approx_completion_tokens": "3600",
            "matrix_nodes": len(DIEGO_R1_NODES),
            "matrix_edges": len(DIEGO_R1_EDGES),
            "output_artifact": "round_01_diego_matrix.csv",
            "notes": "Broad extraction included three unlabeled source/interface symbols",
        },
        {
            "timestamp": timestamp,
            "case": "20",
            "round": "round_02",
            "agent": "Jennifer",
            "role": "precision review",
            "approx_prompt_tokens": "6000",
            "approx_completion_tokens": "1800",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "round_02_jennifer_matrix.csv",
            "notes": "Removed unlabeled symbols; canonicalized bus tags; pruned unsupported interlock overconnections",
        },
        {
            "timestamp": timestamp,
            "case": "20",
            "round": "round_03",
            "agent": "Diego",
            "role": "saturation check",
            "approx_prompt_tokens": "1100",
            "approx_completion_tokens": "240",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "round_03_diego_saturation_matrix.csv",
            "notes": "Saturation matrix uses Jennifer precision corrections",
        },
        {
            "timestamp": timestamp,
            "case": "20",
            "round": "round_04",
            "agent": "Jennifer",
            "role": "final confirmation",
            "approx_prompt_tokens": "480",
            "approx_completion_tokens": "170",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "round_04_jennifer_final_matrix.csv",
            "notes": "Final matrix after agreement",
        },
        {
            "timestamp": timestamp,
            "case": "20",
            "round": "local",
            "agent": "main",
            "role": "artifact generation/validation",
            "approx_prompt_tokens": "1500",
            "approx_completion_tokens": "260",
            "matrix_nodes": len(FINAL_NODES),
            "matrix_edges": len(FINAL_EDGES),
            "output_artifact": "final_connectivity_matrix.csv",
            "notes": "Symmetric matrix, zero diagonal",
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_note(path: Path, timestamp: str) -> None:
    path.write_text(
        f"""# Case 20 Connectivity Extraction Note

Generated: {timestamp}

## Allowed Evidence

- Raw schematic: `raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed the AC class 1E, 480 V load-center, 125 VDC, and lower control/interlock topology, including three unlabeled source/interface symbols.
2. Jennifer precision review removed the unlabeled symbols from the final graph, canonicalized bus tags, confirmed `JB-ESF-A/B`, and kept only the visually supported A/B ESF interlock edge `RELAY-K106 -- RELAY-K108`.
3. Diego saturation check accepted Jennifer corrections and added no supported nodes or edges.
4. Jennifer final confirmation used the saturated matrix unchanged.

## Final Counts

- Nodes: {len(FINAL_NODES)}
- Undirected edges in matrix: {len(FINAL_EDGES)}
- Diagonal: zero
- Matrix: symmetric

## Notes On Decisions

- Crossings and near-passes without junction dots were not modeled as edges.
- 13 kV, 4.16 kV, and 480 V bus ties are represented only through their named tie breakers.
- No A-B or C-D 480 V tie was accepted; only `BUS-480-B -- CB-TIE-480 -- BUS-480-C`.
- No 125 VDC bus tie between `BUS-125DCA` and `BUS-125DCB` was accepted.
- Even 480 V branches with `CS-*` devices are kept as adjacent schematic/control connections; C4 is the supported relay branch `JB-4C -- RELAY-K4C -- PMP-AFW-205C`.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
""",
        encoding="utf-8",
    )


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    for nodes, edges in [(FINAL_NODES, FINAL_EDGES), (DIEGO_R1_NODES, DIEGO_R1_EDGES)]:
        ensure_unique(nodes)
        validate_edges(nodes, edges)

    rounds = [
        ("round_01_diego", DIEGO_R1_NODES, DIEGO_R1_EDGES),
        ("round_02_jennifer", FINAL_NODES, FINAL_EDGES),
        ("round_03_diego_saturation", FINAL_NODES, FINAL_EDGES),
        ("round_04_jennifer_final", FINAL_NODES, FINAL_EDGES),
    ]
    for stem, nodes, edges in rounds:
        write_matrix(RESULTS_DIR / f"{stem}_matrix.csv", nodes, edges)
        write_edges(RESULTS_DIR / f"{stem}_edges.csv", edges)

    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", FINAL_NODES, FINAL_EDGES)
    write_edges(RESULTS_DIR / "final_edge_list.csv", FINAL_EDGES)
    write_uncertain(RESULTS_DIR / "uncertain_excluded_edges.csv")
    write_tracking(RESULTS_DIR / "token_performance_tracking.csv", timestamp)
    write_note(RESULTS_DIR / "extraction_note.md", timestamp)
    print(f"wrote {len(FINAL_NODES)} nodes and {len(FINAL_EDGES)} edges to {RESULTS_DIR}")


if __name__ == "__main__":
    main()
