import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\21")
ART = BASE / "Codes and artifacts"
RESULTS = BASE / "Results" / "Iteration_1"
COMPONENTS = ART / "component_labels_list.csv"
MATRIX_OUT = RESULTS / "round_01_diego_matrix.csv"
NOTES_OUT = RESULTS / "round_01_diego_notes.md"


RAW_VERIFIED_BUSES = [
    "BUS-101",
    "BUS-102",
    "BUS-201A",
    "BUS-201B",
    "BUS-202A",
    "BUS-202B",
    "BUS-301A",
    "BUS-301B",
    "BUS-302A",
    "BUS-302B",
    "BUS-401A",
    "BUS-401B",
    "BUS-501A",
    "BUS-501B",
]


def load_component_nodes():
    with COMPONENTS.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    labels = [row["normalized_label"] for row in rows]
    if len(labels) != len(set(labels)):
        dupes = sorted({label for label in labels if labels.count(label) > 1})
        raise ValueError(f"duplicate labels: {dupes}")
    return labels


component_nodes = load_component_nodes()

# CB-204A and DS-401B are raw-visible physical components that the component
# CSV missed; they are included because the raw schematic is primary.
extra_raw_components = ["CB-204A", "DS-401B"]

nodes = []
for label in component_nodes:
    nodes.append(label)
    if label == "CB-106":
        nodes.append("CB-204A")
    if label == "DS-401A":
        nodes.append("DS-401B")
nodes.extend(RAW_VERIFIED_BUSES)

node_set = set(nodes)
edges = set()
edge_notes = []


def add(a, b, group, evidence="solid/raw"):
    if a not in node_set:
        raise KeyError(f"missing node {a}")
    if b not in node_set:
        raise KeyError(f"missing node {b}")
    if a == b:
        raise ValueError(f"self edge {a}")
    edge = tuple(sorted((a, b)))
    edges.add(edge)
    edge_notes.append((group, a, b, evidence))


def chain(labels, group, evidence="solid/raw"):
    for a, b in zip(labels, labels[1:]):
        add(a, b, group, evidence)


# Incoming 13.8 kV sources and transformer feeders to 4.16 kV buses.
add("GEN-UT", "CB-101", "incoming sources")
add("GEN-UT", "CB-102", "incoming sources")
chain(["CB-101", "DS-101A", "TR-UAT1", "CB-201A", "BUS-201A"], "incoming sources")
chain(["CB-102", "DS-101B", "TR-UAT2", "CB-201B", "BUS-201B"], "incoming sources")
chain(["BUS-101", "CB-103", "DS-102A", "TR-SU1", "CB-202A", "BUS-202A"], "incoming sources")
chain(["BUS-102", "CB-104", "DS-102B", "TR-SU2", "CB-202B", "BUS-202B"], "incoming sources")

# 4.16 kV switchgear and EDG feeders.
chain(["BUS-201A", "DS-201A", "CB-105", "EDG-1A"], "upper switchgear / EDG")
chain(["BUS-201B", "CB-204A", "DS-201B", "CB-106", "EDG-1B"], "upper switchgear / EDG", "raw-visible; CB-204A detector-omitted")
chain(["BUS-202A", "DS-202A", "CB-203A", "EDG-2A"], "upper switchgear / EDG")
chain(["BUS-202B", "DS-202B", "CB-203B", "EDG-2B"], "upper switchgear / EDG")

# 4.16 kV feeder drops to 480 V transformers/load centers.
chain(["BUS-201A", "CB-301A", "DS-J01A", "TR-SA", "CB-501A", "BUS-301A"], "480 V transformer feeders")
chain(["BUS-202A", "CB-302A", "DS-J02A", "TR-NA", "CB-502A", "BUS-302A"], "480 V transformer feeders")
chain(["BUS-201B", "CB-301B", "DS-J01B", "TR-SB", "CB-501B", "BUS-301B"], "480 V transformer feeders")
chain(["BUS-202B", "CB-302B", "DS-J02B", "CB-502B", "TR-NB", "BUS-302B"], "480 V transformer feeders")

# Train A 480 V load centers and MCC load taps.
add("BUS-301A", "GND-1", "480 V train A")
chain(["BUS-301A", "CB-303A", "MCC-1A"], "480 V train A")
chain(["BUS-301A", "CB-304A", "MCC-2A"], "480 V train A")
chain(["BUS-302A", "CB-503A", "MCC-3A"], "480 V train A")
add("MCC-3A", "GND-5", "480 V train A")
for load in ["MOTOR-SI101A", "PUMP-SI101A", "MOTOR-CCW101A", "PUMP-CCW101A", "VLV-8801A"]:
    add("MCC-1A", load, "480 V train A MCC loads")
for load in ["MOTOR-AFW101A", "PUMP-AFW101A", "MOTOR-RHR101A", "PUMP-RHR101A", "VLV-8802A"]:
    add("MCC-2A", load, "480 V train A MCC loads")
for load in ["MOTOR-SW101A", "PUMP-SW101A", "MOTOR-CHG101A", "PUMP-CHG101A", "MOTOR-FAN101A", "VLV-8901A"]:
    add("MCC-3A", load, "480 V train A MCC loads")

# Train B 480 V load centers and MCC load taps.
add("BUS-301B", "GND-2", "480 V train B")
chain(["BUS-301B", "CB-303B", "MCC-1B"], "480 V train B")
chain(["BUS-301B", "CB-304B", "MCC-2B"], "480 V train B")
chain(["BUS-302B", "CB-503B", "MCC-3B"], "480 V train B")
add("MCC-3B", "GND-6", "480 V train B")
for load in ["MOTOR-SI101B", "PUMP-SI101B", "MOTOR-CCW101B", "PUMP-CCW101B", "VLV-8801B"]:
    add("MCC-1B", load, "480 V train B MCC loads")
for load in ["MOTOR-AFW101B", "PUMP-AFW101B", "MOTOR-RHR101B", "PUMP-RHR101B", "VLV-8802B"]:
    add("MCC-2B", load, "480 V train B MCC loads")
for load in ["MOTOR-SW101B", "PUMP-SW101B", "MOTOR-CHG101B", "PUMP-CHG101B", "MOTOR-FAN101B", "VLV-8901B"]:
    add("MCC-3B", load, "480 V train B MCC loads")

# DC/UPS supplies, including plausible upstream 480 V feeder taps visible as long drops.
chain(["BUS-301A", "DS-401A", "TR-DC-A", "RECT-125A", "BUS-401A"], "DC/UPS supplies", "solid/raw; upstream 480 V tap plausible")
chain(["BUS-301B", "DS-401B", "TR-DC-B", "RECT-125B", "BUS-401B"], "DC/UPS supplies", "solid/raw; upstream 480 V tap plausible")
chain(["BUS-302A", "DS-402A", "TR-INV-A", "INV-120C", "BUS-501A"], "DC/UPS supplies", "solid/raw; INV-120C output to control bus plausible")
chain(["BUS-302B", "DS-402B", "TR-INV-B", "RECT-24C", "BUS-401B"], "DC/UPS supplies", "solid/raw; RECT-24C return/feed plausible")
for dc_load in ["BAT-1A", "BAT-2A", "GND-3", "INV-120A"]:
    add("BUS-401A", dc_load, "DC/UPS supplies")
for dc_load in ["BAT-1B", "BAT-2B", "GND-4", "INV-120B"]:
    add("BUS-401B", dc_load, "DC/UPS supplies")
add("INV-120A", "BUS-501A", "DC/UPS to ladder rails")
add("INV-120B", "BUS-501B", "DC/UPS to ladder rails")
add("BAT-EDG-A", "CP-EDG-A", "DC/UPS dashed EDG battery link", "dashed/weak")
add("BAT-EDG-B", "CP-EDG-B", "DC/UPS dashed EDG battery link", "dashed/weak")
add("BAT-EDG-A", "BAT-EDG-B", "DC/UPS dashed EDG battery link", "dashed/weak")

# Control ladder rows. These are dashed/dotted control and signal conductors.
ladder_rows = [
    ("CP-SI-A", ["RELAY-K101", "RELAY-K102", "RELAY-K103", "JB-101", "INST-PT101", "INST-PT102"]),
    ("CP-SI-B", ["RELAY-K104", "RELAY-K105", "RELAY-K106", "JB-102", "INST-PT103", "INST-FT201"]),
    ("CP-CCW-A", ["RELAY-K107", "RELAY-K108", "RELAY-K109", "JB-103", "INST-FT202", "INST-LT301"]),
    ("CP-CCW-B", ["RELAY-K110", "RELAY-K111", "RELAY-K112", "JB-104", "INST-LT302", "INST-TT401"]),
    ("CP-EDG-A", ["RELAY-K113", "RELAY-K114", "RELAY-K115", "JB-105", "INST-TT402", "INST-CT501"]),
    ("CP-EDG-B", ["RELAY-K116", "RELAY-K117", "RELAY-K118", "JB-106", "INST-CT502"]),
    ("RPS-A", ["RELAY-K119", "RELAY-K120", "RELAY-K121", "JB-107", "INST-VT601"]),
    ("RPS-B", ["RELAY-K122", "RELAY-K123", "RELAY-K124", "JB-108", "INST-VT602"]),
    ("ESFAS-A", ["RELAY-K125", "RELAY-K126", "RELAY-K127", "JB-109", "INST-ZS701"]),
    ("ESFAS-B", ["RELAY-K128", "RELAY-K129", "RELAY-K130", "JB-110", "INST-ZS702"]),
]
for first, rest in ladder_rows:
    add("BUS-501A", first, "control ladder rails", "dashed/control")
    add("BUS-501B", first, "control ladder rails", "dashed/control")
    chain([first] + rest, f"control ladder row {first}", "dashed/dotted control-signal")

for panel in ["CP-SWGR", "CP-CRD"]:
    add("BUS-501A", panel, "control ladder rails", "dashed/control")
    add("BUS-501B", panel, "control ladder rails", "dashed/control")
add("CP-SWGR", "CP-SI-A", "control ladder vertical interlock", "dashed/control")
add("CP-SWGR", "UVLS-A", "control ladder top interlock", "dashed/weak")
add("UVLS-A", "UVLS-B", "control ladder top interlock", "dashed/weak")
add("UVLS-A", "RELAY-K101", "control ladder top interlock", "dashed/weak")
add("UVLS-B", "RELAY-K102", "control ladder top interlock", "dashed/weak")

chain(["CP-EDG-A", "CP-EDG-B", "RPS-A", "RPS-B", "ESFAS-A", "ESFAS-B", "CP-CRD"], "control ladder vertical interlock", "dashed/control")


def write_matrix():
    RESULTS.mkdir(parents=True, exist_ok=True)
    index = {label: i for i, label in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for a, b in edges:
        ia, ib = index[a], index[b]
        matrix[ia][ib] = 1
        matrix[ib][ia] = 1
    for i in range(len(nodes)):
        matrix[i][i] = 0

    with MATRIX_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node"] + nodes)
        for label, row in zip(nodes, matrix):
            writer.writerow([label] + row)
    return matrix


def validate(matrix):
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix)))
    diag_zero = all(matrix[i][i] == 0 for i in range(len(matrix)))
    edge_count = sum(sum(row) for row in matrix) // 2
    return symmetric, diag_zero, edge_count


def write_notes(matrix):
    symmetric, diag_zero, edge_count = validate(matrix)
    by_group = {}
    for group, a, b, evidence in edge_notes:
        by_group.setdefault(group, []).append((a, b, evidence))

    lines = []
    lines.append("# Diego Round 01 Connectivity Notes")
    lines.append("")
    lines.append("## Extraction Scope")
    lines.append("- Inputs inspected only from doc 21 `Input resources` and doc 21 `Codes and artifacts`.")
    lines.append("- Raw schematic was treated as primary; component/OCR lists, wire masks, wire-node overlays, and inspection crops were used as aids.")
    lines.append("- WN-* wire-node IDs and arbitrary intermediate points were not used as matrix nodes.")
    lines.append("")
    lines.append("## Node List Rationale")
    lines.append(f"- Included {len(component_nodes)} physical component labels from `component_labels_list.csv`.")
    lines.append("- Added raw-verified logical bus nodes: " + ", ".join(RAW_VERIFIED_BUSES) + ".")
    lines.append("- Added `CB-204A` because the raw EDG-1B/BUS-201B feeder visibly labels a breaker `CB-204A`, although the detector/component CSV omitted that physical breaker.")
    lines.append("- Added `DS-401B` because the raw DC/UPS B-side chain visibly labels the disconnect `DS-401B`, although the detector/component CSV omitted that physical disconnect.")
    lines.append("- Did not include section headers, notes, line-code legend text, WN-* wire IDs, or unlabeled small breaker symbols as named nodes.")
    lines.append("")
    lines.append("## Edge Evidence by Area")
    for group in [
        "incoming sources",
        "upper switchgear / EDG",
        "480 V transformer feeders",
        "480 V train A",
        "480 V train A MCC loads",
        "480 V train B",
        "480 V train B MCC loads",
        "DC/UPS supplies",
        "DC/UPS to ladder rails",
        "DC/UPS dashed EDG battery link",
        "control ladder rails",
        "control ladder vertical interlock",
        "control ladder top interlock",
    ]:
        if group not in by_group:
            continue
        lines.append(f"### {group}")
        for a, b, evidence in by_group[group]:
            lines.append(f"- `{a}` -- `{b}` ({evidence})")
    lines.append("### control ladder rows")
    for group in sorted(g for g in by_group if g.startswith("control ladder row ")):
        first = group.replace("control ladder row ", "")
        pieces = by_group[group]
        chain_text = " -- ".join([pieces[0][0]] + [b for _, b, _ in pieces])
        lines.append(f"- `{first}` row: `{chain_text}` (dashed/dotted control-signal)")
    lines.append("")
    lines.append("## Uncertain / High-Recall Candidates")
    lines.append("- Included `CB-204A` and `DS-401B` as raw-visible physical components despite detector omission.")
    lines.append("- Included plausible upstream 480 V feeder taps from `BUS-301A/BUS-301B/BUS-302A/BUS-302B` into the DC/UPS disconnect chains; the long drops are visible, but their exact source-bus assignment is inferred from alignment.")
    lines.append("- Included `INV-120C` to `BUS-501A` and `RECT-24C` to `BUS-401B` as plausible output/feed connections from the raw paths.")
    lines.append("- Included dashed `BAT-EDG-A/B` links to `CP-EDG-A/B` and to each other as weak high-recall candidates; these dashed paths are visually present but not as solid power conductors.")
    lines.append("- Included row-wise ladder connections and vertical interlock links as dashed/dotted control/signal evidence, not solid power feeders.")
    lines.append("- Kept out unlabeled small breaker-like symbols on some EDG feeders because no exact raw-printed label was verified except `CB-204A`.")
    lines.append("")
    lines.append("## Validation Summary")
    lines.append(f"- Node count: {len(nodes)}")
    lines.append(f"- Edge count: {edge_count}")
    lines.append(f"- Symmetric: {symmetric}")
    lines.append(f"- Diagonal zero: {diag_zero}")
    lines.append("- Row and column labels: identical and in the same order by construction.")
    NOTES_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    m = write_matrix()
    write_notes(m)
    sym, diag, ec = validate(m)
    print(f"wrote {MATRIX_OUT}")
    print(f"wrote {NOTES_OUT}")
    print(f"nodes={len(nodes)} edges={ec} symmetric={sym} diagonal_zero={diag}")
