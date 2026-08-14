import csv
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\35")
INPUT_DIR = DOC_ROOT / "Input resources"
RESULT_DIR = DOC_ROOT / "Results" / "Iteration_1"

MATRIX_PATH = RESULT_DIR / "round_01_diego_matrix.csv"
NOTES_PATH = RESULT_DIR / "round_01_diego_notes.md"


def read_inventory_labels():
    path = INPUT_DIR / "component_visual_ocr_labels.csv"
    labels = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            label = row["normalized_label"].strip()
            if label:
                labels.append(label)
    if len(labels) != len(set(labels)):
        raise ValueError("Inventory labels are not unique.")
    return labels


EXTRA_NODES = [
    "OPC-IA-2101",
    "IA-H-2101",
    "VNT-2101",
    "VNT-2140",
    "OPC-SW-2101",
    "H-SW-2101",
    "OPC-SW-2102",
    "OPC-DMW-2101",
    "OPC-2101",
    "H-2101",
    "SB-2101",
    "STR-2101",
    "T-2101",
    "T-2102",
    "T-2103",
    "H-2102",
    "T-2115",
    "T-2120",
    "T-2122A",
    "T-2122B",
    "T-2125",
    "T-2130",
    "T-2131",
    "T-2132",
    "OPC-2102",
    "OPC-CHEM-2101",
    "T-2110",
    "T-2140",
    "INJ-2140",
    "SAP-2101",
    "AN-2101",
    "AIC-2101",
    "OPC-DRN-2101",
    "OPC-DATA-2101",
    "HV-SW-DRAIN",
]


REGION_EDGES = {
    "Left makeup, IA, service water, and TK-210": [
        ("OPC-IA-2101", "HV-IA-2101"),
        ("HV-IA-2101", "PCV-IA-2101"),
        ("PCV-IA-2101", "IA-H-2101"),
        ("IA-H-2101", "PI-IA-2101"),
        ("VNT-2101", "HV-2103"),
        ("HV-2103", "TK-210"),
        ("PSV-2102", "VNT-2140"),
        ("OPC-SW-2101", "H-SW-2101"),
        ("H-SW-2101", "HV-SW-2101"),
        ("HV-SW-2101", "STR-SW-2101"),
        ("STR-SW-2101", "FT-SW-2101"),
        ("FT-SW-2101", "FCV-SW-2101"),
        ("FT-SW-2101", "FIC-SW-2101"),
        ("FIC-SW-2101", "FCV-SW-2101"),
        ("PT-SW-2101", "STR-SW-2101"),
        ("HS-2101", "FIC-SW-2101"),
        ("FCV-SW-2101", "HV-SW-2102"),
        ("HV-SW-2102", "CV-SW-2101"),
        ("CV-SW-2101", "OPC-SW-2102"),
        ("TT-SW-2101", "TIC-2130"),
        ("TIC-2130", "HV-SW-2102"),
        ("OPC-DMW-2101", "HV-2150"),
        ("HV-2150", "FT-2150"),
        ("FT-2150", "FCV-2150"),
        ("FCV-2150", "LV-2101"),
        ("LV-2101", "TK-210"),
        ("FIC-2150", "FT-2150"),
        ("FIC-2150", "FCV-2150"),
        ("LIC-2101", "LT-2101"),
        ("LIC-2101", "LV-2101"),
        ("LT-2101", "TK-210"),
        ("LI-2101", "TK-210"),
        ("LSHH-2101", "LAHH-2101"),
        ("LSHH-2101", "TK-210"),
        ("LAHH-2101", "TK-210"),
        ("LSL-2102", "LALL-2102"),
        ("LSL-2102", "TK-210"),
        ("LALL-2102", "TK-210"),
        ("TK-210", "HV-2104"),
        ("HV-2104", "DRN-2101"),
        ("TK-210", "HV-1102"),
        ("HV-1102", "T-2101"),
        ("OPC-2101", "H-2101"),
        ("H-2101", "HV-2101"),
        ("HV-2101", "SB-2101"),
        ("SB-2101", "STR-2101"),
        ("STR-2101", "T-2101"),
        ("PDI-2101", "STR-2101"),
        ("PI-2101", "T-2101"),
        ("PT-2101", "T-2101"),
        ("PI-2101", "PT-2101"),
    ],
    "A/B cleanup trains and pump discharge header": [
        ("T-2101", "HV-2110A"),
        ("HV-2110A", "STR-2110A"),
        ("STR-2110A", "P-2101A"),
        ("P-2101A", "CV-2110A"),
        ("CV-2110A", "HV-2111A"),
        ("HV-2111A", "MOV-2112A"),
        ("MOV-2112A", "T-2102"),
        ("T-2102", "H-2102"),
        ("T-2101", "HV-2110B"),
        ("HV-2110B", "STR-2110B"),
        ("STR-2110B", "P-2101B"),
        ("P-2101B", "CV-2110B"),
        ("CV-2110B", "HV-2111B"),
        ("HV-2111B", "MOV-2112B"),
        ("MOV-2112B", "T-2103"),
        ("T-2103", "H-2102"),
        ("H-2102", "T-2115"),
        ("T-2115", "FT-2110"),
        ("FT-2110", "HV-2113"),
        ("HV-2113", "T-2120"),
        ("TS-2110A", "PT-2110A"),
        ("PT-2110A", "PI-2110A"),
        ("PT-2110A", "P-2101A"),
        ("PI-2110A", "P-2101A"),
        ("TS-2110A", "P-2101A"),
        ("TS-2110B", "PT-2110B"),
        ("PT-2110B", "PI-2110B"),
        ("PT-2110B", "P-2101B"),
        ("PI-2110B", "P-2101B"),
        ("TS-2110B", "P-2101B"),
        ("HS-2101", "MOV-2112A"),
        ("HS-2102", "MOV-2112B"),
        ("FIC-2110", "FT-2110"),
        ("FIC-2110", "SV-2110"),
        ("FIC-2110", "FAH-2110"),
        ("FAH-2110", "FT-2110"),
        ("SV-2110", "PSV-2110"),
        ("PSV-2110", "T-2130"),
    ],
    "Filters, HX, bypass, and service-water return": [
        ("T-2120", "T-2130"),
        ("T-2130", "HV-2130"),
        ("HV-2130", "FCV-2130"),
        ("FCV-2130", "HV-2131"),
        ("HV-2131", "T-2132"),
        ("T-2132", "T-2131"),
        ("T-2130", "HV-2120A"),
        ("HV-2120A", "FLT-2120A"),
        ("FLT-2120A", "HV-2121A"),
        ("HV-2121A", "T-2122A"),
        ("T-2122A", "T-2125"),
        ("T-2120", "HV-2120B"),
        ("HV-2120B", "FLT-2120B"),
        ("FLT-2120B", "HV-2121B"),
        ("HV-2121B", "T-2122B"),
        ("T-2122B", "T-2125"),
        ("T-2125", "HV-2125"),
        ("HV-2125", "HX-2120"),
        ("HX-2120", "T-2131"),
        ("T-2131", "MOV-2125"),
        ("MOV-2125", "FCV-2125"),
        ("FCV-2125", "R-2125"),
        ("R-2125", "OPC-2102"),
        ("T-2131", "HV-SW-DRAIN"),
        ("HV-SW-DRAIN", "DRN-SW-2101"),
        ("PI-2120A", "T-2130"),
        ("DPIT-2120A", "FLT-2120A"),
        ("DPIT-2120A", "DPAH-2120"),
        ("PI-2120B", "FLT-2120B"),
        ("DPIT-2120B", "FLT-2120B"),
        ("DPIT-2120B", "DPAH-2120"),
        ("FT-2130", "FIC-2130"),
        ("FT-2130", "FCV-2130"),
        ("FIC-2130", "FCV-2130"),
        ("SV-2130", "FIC-2130"),
        ("SV-2130", "FCV-2130"),
        ("PIC-2101", "FCV-2130"),
        ("PI-2125", "T-2125"),
        ("TT-2120I", "HX-2120"),
        ("TT-2120I", "TT-2120O"),
        ("TT-2120O", "TAH-2120"),
        ("TT-2120O", "HX-2120"),
        ("TI-2120", "HX-2120"),
        ("TAL-2120", "TI-2120"),
        ("TAL-2120", "FCV-2125"),
        ("SV-2125", "FCV-2125"),
    ],
    "Chemical tank and chemical injection pumps": [
        ("OPC-CHEM-2101", "HV-2140"),
        ("HV-2140", "FLT-2140"),
        ("FLT-2140", "TK-2110"),
        ("TK-2110", "LT-2110"),
        ("TK-2110", "LSH-2110"),
        ("TK-2110", "HV-2141"),
        ("HV-2141", "T-2110"),
        ("TK-2110", "HV-2147"),
        ("HV-2147", "T-2110"),
        ("VNT-2140", "HV-2146"),
        ("HV-2146", "TK-2110"),
        ("TK-2110", "HV-2145"),
        ("HV-2145", "DRN-2140"),
        ("DRN-2140", "H-DRN-2101"),
        ("T-2110", "P-2110A"),
        ("P-2110A", "CV-2140A"),
        ("CV-2140A", "HV-2142A"),
        ("HV-2142A", "T-2140"),
        ("T-2110", "P-2110B"),
        ("P-2110B", "CV-2140B"),
        ("CV-2140B", "HV-2142B"),
        ("HV-2142B", "T-2140"),
        ("T-2140", "PI-2140"),
        ("PI-2140", "PCV-2132"),
        ("PCV-2132", "FCV-2114"),
        ("FCV-2114", "HV-2114"),
        ("HV-2114", "T-2103"),
        ("FIC-2140", "FI-2140"),
        ("FIC-2140", "PCV-2132"),
        ("FIC-2140", "FCV-2114"),
        ("PSV-2140", "T-2140"),
        ("FI-2140", "PI-2140"),
        ("HS-2102", "FIC-2140"),
        ("HS-2102", "P-2110A"),
        ("HS-2102", "P-2110B"),
        ("AIT-2140", "AI-2140"),
        ("AIT-2140", "FCV-2114"),
        ("T-2140", "HV-2143"),
        ("HV-2143", "XV-2144"),
        ("XV-2144", "INJ-2140"),
        ("XV-2144", "FCV-2114"),
        ("XV-2144", "SV-2144"),
        ("SV-2144", "HV-DRN-2107"),
        ("HV-2142B", "R-2114"),
        ("R-2114", "XV-2144"),
    ],
    "Sample panels, drains, and control/data bay": [
        ("T-2125", "HV-SAM-2101"),
        ("HV-SAM-2101", "SP-2101"),
        ("SP-2101", "SAP-2101"),
        ("T-2122B", "HV-SAM-2102"),
        ("HV-SAM-2102", "SP-2102"),
        ("SP-2102", "SAP-2101"),
        ("T-2131", "HV-SAM-2103"),
        ("HV-SAM-2103", "SP-2103"),
        ("SP-2103", "SAP-2101"),
        ("SAP-2101", "AN-2101"),
        ("AN-2101", "AIC-2101"),
        ("DRN-2101", "HV-DRN-2102"),
        ("HV-DRN-2102", "HV-DRN-2103"),
        ("HV-DRN-2103", "CP-CHEM-2101"),
        ("CP-CHEM-2101", "SV-2144"),
        ("SV-2144", "HV-DRN-2107"),
        ("HV-DRN-2107", "H-DRN-2101"),
        ("H-DRN-2101", "HV-DRN-2104"),
        ("HV-DRN-2104", "HV-DRN-2105"),
        ("HV-DRN-2105", "DRN-SW-2101"),
        ("DRN-SW-2101", "OPC-DRN-2101"),
        ("DRN-2101", "H-DRN-2101"),
        ("XA-2140", "CP-CHEM-2101"),
        ("XA-2140", "JB-2101"),
        ("CP-CHEM-2101", "JB-2101"),
        ("JB-2101", "JB-2102"),
        ("JB-2102", "JBX-2103"),
        ("JBX-2103", "PLC-2101"),
        ("PLC-2101", "DCS-2101"),
        ("DCS-2101", "OPC-DATA-2101"),
        ("JB-2102", "XA-2110"),
        ("HS-2110", "XA-2110"),
        ("XA-2110", "KQI-2101"),
        ("KQI-2101", "KQI-2102"),
        ("KQI-2102", "PLC-2101"),
    ],
}


UNCERTAIN = [
    ("PSV-2102", "VNT-2140", "relief/vent routing is visible but crosses dense IA/SW/tank area"),
    ("PSV-2110", "T-2130", "safety valve is near the filter/bypass inlet header; exact tap point is small"),
    ("VNT-2140", "HV-2146", "long vertical line appears continuous but spans a large sheet region"),
    ("HV-2146", "TK-2110", "probable vent/top connection into lower chemical tank; visually distant"),
    ("HV-SW-DRAIN", "DRN-SW-2101", "named drain valve is not in inventory and the long drain run is partially outside crop"),
    ("HV-2114", "T-2103", "chemical/process tie-in uses a dense vertical riser near B-train discharge"),
    ("T-2122B", "HV-SAM-2102", "sample takeoff routing is visually plausible but partly dashed/overlapping"),
    ("T-2131", "HV-SAM-2103", "sample takeoff routing is visually plausible but partly routed through the HX outlet area"),
    ("XA-2140", "JB-2101", "control/data line continues into the bay but exact landing point is sparse"),
    ("KQI-2102", "PLC-2101", "bottom interlock/control bundle is represented as a local chain, not a bay clique"),
]


def flatten_edges():
    seen = set()
    edges = []
    for pairs in REGION_EDGES.values():
        for a, b in pairs:
            key = tuple(sorted((a, b)))
            if a == b:
                raise ValueError(f"Self edge requested: {a}")
            if key not in seen:
                seen.add(key)
                edges.append((a, b))
    return edges


def validate(labels, edges):
    label_set = set(labels)
    problems = []
    for a, b in edges:
        if a not in label_set:
            problems.append(f"edge endpoint not in nodes: {a}")
        if b not in label_set:
            problems.append(f"edge endpoint not in nodes: {b}")
    degree = {label: 0 for label in labels}
    for a, b in edges:
        if a in degree and b in degree:
            degree[a] += 1
            degree[b] += 1
    isolated = [label for label, value in degree.items() if value == 0]
    if isolated:
        problems.append("isolated nodes: " + ", ".join(isolated))
    if problems:
        raise ValueError("\n".join(problems))
    return degree


def write_matrix(labels, edges):
    index = {label: i for i, label in enumerate(labels)}
    matrix = [["0" for _ in labels] for _ in labels]
    for a, b in edges:
        i = index[a]
        j = index[b]
        matrix[i][j] = "1"
        matrix[j][i] = "1"
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    with MATRIX_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + labels)
        for label, row in zip(labels, matrix):
            writer.writerow([label] + row)
    return matrix


def matrix_validation_summary(labels, matrix, degree, edges):
    row_count = len(matrix)
    width_ok = all(len(row) == len(labels) for row in matrix)
    symmetric = True
    diagonal_zero = True
    values_ok = True
    for i in range(len(labels)):
        if matrix[i][i] != "0":
            diagonal_zero = False
        for j in range(len(labels)):
            if matrix[i][j] not in {"0", "1"}:
                values_ok = False
            if matrix[i][j] != matrix[j][i]:
                symmetric = False
    return {
        "node_count": len(labels),
        "inventory_node_count": len(read_inventory_labels()),
        "added_node_count": len(EXTRA_NODES),
        "edge_count": len(edges),
        "row_count": row_count,
        "width_ok": width_ok,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
        "values_ok": values_ok,
        "isolated_count": sum(1 for value in degree.values() if value == 0),
        "min_degree": min(degree.values()),
        "max_degree": max(degree.values()),
    }


def format_edge_list(edges):
    return ", ".join(f"{a}-{b}" for a, b in edges)


def write_notes(labels, edges, degree, summary):
    region_lines = []
    for region, pairs in REGION_EDGES.items():
        unique_pairs = []
        seen = set()
        for a, b in pairs:
            key = tuple(sorted((a, b)))
            if key not in seen:
                seen.add(key)
                unique_pairs.append((a, b))
        region_lines.append(
            f"- **{region}** ({len(unique_pairs)} edges): {format_edge_list(unique_pairs)}."
        )

    extra_lines = [
        f"- `{node}`: visible named non-inventory endpoint/component/tie point used to avoid anonymous WN/junction nodes."
        for node in EXTRA_NODES
    ]
    uncertain_lines = [f"- `{a}` - `{b}`: {why}." for a, b, why in UNCERTAIN]

    scrutinize = [
        "- Vent/relief links around `PSV-2102`, `VNT-2140`, and `HV-2146` because the vertical routing spans multiple crop regions.",
        "- Header/tie modeling around `T-2130`, `T-2120`, `T-2122A/B`, `T-2125`, `T-2131`, and `T-2132`; I represented local adjacent pairs only, not header cliques.",
        "- Chemical injection riser edges `HV-2114`-`T-2103`, `FCV-2114`-`HV-2114`, and `XV-2144`-`FCV-2114` because the lower-middle riser is visually dense.",
        "- Sample panel takeoffs `T-2125`/`T-2122B`/`T-2131` to `HV-SAM-*`; these are visually plausible dashed/sample routes but should be checked against the raw crop.",
        "- Bottom control bay chain `JB-2101`-`JB-2102`-`JBX-2103`-`PLC-2101`-`DCS-2101` and `HS-2110`/`XA-2110`/`KQI-*`; intentionally sparse but uncertain at exact landing points.",
    ]

    validation = [
        f"- Matrix path: `{MATRIX_PATH}`",
        f"- Nodes: {summary['node_count']} total = {summary['inventory_node_count']} inventory + {summary['added_node_count']} added named non-inventory nodes.",
        f"- Unique undirected accepted edges: {summary['edge_count']}.",
        f"- Row count equals column count: {summary['row_count'] == summary['node_count'] and summary['width_ok']}.",
        f"- Row/column label order identical by construction: True.",
        f"- Symmetric: {summary['symmetric']}.",
        f"- Values restricted to 0/1: {summary['values_ok']}.",
        f"- Diagonal zero: {summary['diagonal_zero']}.",
        f"- Isolated accepted nodes: {summary['isolated_count']} (minimum degree {summary['min_degree']}, maximum degree {summary['max_degree']}).",
    ]

    text = "\n".join(
        [
            "# Round 01 Diego High-Recall Connectivity Notes",
            "",
            "## Scope And Inputs",
            "",
            "Used only doc35 Input resources and generated doc35 artifacts: the raw schematic image, component inventory CSV/list, component/wire overlays, wire-node aid overlay, resource summaries, and inspection crops. No ground truth, evaluator output, validation metrics, previous-doc feedback, or outside resources were used.",
            "",
            "## Node List Rationale",
            "",
            "All 144 visually supported inventory component labels from `component_visual_ocr_labels.csv` are retained exactly as normalized in the inventory. I added only visible named endpoints, headers, tie points, sample/control endpoints, and a few visible named non-inventory components where they prevent replacing a named schematic object with an anonymous WN/junction.",
            "",
            "Added non-inventory nodes:",
            "",
            *extra_lines,
            "",
            "I intentionally excluded WN ids, unlabeled dots, elbows, continuation ticks, and line-number-only labels such as pipe spec tags. Long headers are represented by adjacent named pairs through explicit `H-*`, `OPC-*`, and `T-*` nodes where visible.",
            "",
            "## Edge Evidence By Region",
            "",
            *region_lines,
            "",
            "## Ambiguous / Plausible But Uncertain Candidates",
            "",
            *uncertain_lines,
            "",
            "## High-Recall Edges Jennifer Should Scrutinize",
            "",
            *scrutinize,
            "",
            "## Basic Validation Summary",
            "",
            *validation,
            "",
        ]
    )
    NOTES_PATH.write_text(text, encoding="utf-8")


def main():
    inventory = read_inventory_labels()
    duplicate_extras = sorted(set(inventory) & set(EXTRA_NODES))
    if duplicate_extras:
        raise ValueError("Extra nodes duplicate inventory labels: " + ", ".join(duplicate_extras))
    labels = inventory + EXTRA_NODES
    if len(labels) != len(set(labels)):
        raise ValueError("Final node labels are not unique.")
    edges = flatten_edges()
    degree = validate(labels, edges)
    matrix = write_matrix(labels, edges)
    summary = matrix_validation_summary(labels, matrix, degree, edges)
    write_notes(labels, edges, degree, summary)
    print(
        "wrote",
        MATRIX_PATH,
        NOTES_PATH,
        f"nodes={summary['node_count']}",
        f"edges={summary['edge_count']}",
        f"isolated={summary['isolated_count']}",
    )


if __name__ == "__main__":
    main()
