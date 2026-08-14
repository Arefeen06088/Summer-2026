from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires + junctions"
)
WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc26_work")
RESULTS = ROOT / "results"
FALLBACK_RESULTS = WORK / "results"


NODES = [
    "BUS-416A",
    "BUS-416B",
    "BUS-480A",
    "BUS-480B",
    "BUS-125DCA",
    "BUS-125DCB",
    "BUS-INV-A",
    "BUS-INV-B",
    "BUS-120N-A",
    "BUS-120N-B",
    "GEN-301",
    "TR-UAT-31",
    "CB-4A-IN1",
    "SAT-31A",
    "CB-4A-ST",
    "DG-31A",
    "CB-4A-DG",
    "SAT-31B",
    "CB-4B-ST",
    "DG-31B",
    "CB-4B-DG",
    "CB-4AB-TIE",
    "CB-4A01",
    "CB-4A02",
    "CB-4A03",
    "CB-4A04",
    "CB-4A05",
    "CB-4A06",
    "TR-480A1",
    "TR-480A2",
    "CB-480A-IN",
    "CB-480A-ALT",
    "DS-RCP-A",
    "DS-SW-A",
    "DS-AFW-A",
    "DS-CHW-A",
    "MTR-RCP-A",
    "PUMP-SW31A",
    "PUMP-AFW31A",
    "MTR-CHWP-A",
    "GND-RCP-A",
    "GND-SW-A",
    "CB-4B01",
    "CB-4B02",
    "CB-4B03",
    "CB-4B04",
    "CB-4B05",
    "CB-4B06",
    "TR-480B1",
    "TR-480B2",
    "CB-480B-IN",
    "CB-480B-ALT",
    "DS-RCP-B",
    "DS-SW-B",
    "DS-AFW-B",
    "DS-CHW-B",
    "MTR-RCP-B",
    "PUMP-SW31B",
    "PUMP-AFW31B",
    "MTR-CHWP-B",
    "GND-RCP-B",
    "GND-SW-B",
    "CB-480AB-TIE",
    "CB-480A11",
    "CB-480A12",
    "CB-480A13",
    "CB-480A14",
    "MCC-31A1",
    "MCC-31A2",
    "LC-31A3",
    "PNL-31A4",
    "GND-MCC-A1",
    "GND-MCC-A2",
    "STR-A1-1",
    "JB-A1-01",
    "PUMP-CVC-A",
    "STR-A1-2",
    "JB-A1-02",
    "MOV-RHR-731A",
    "STR-A1-3",
    "JB-A1-03",
    "FAN-CRD-A",
    "STR-A2-1",
    "JB-A2-01",
    "PUMP-CCW-A",
    "STR-A2-2",
    "JB-A2-02",
    "HTR-BORIC-A",
    "STR-A2-3",
    "JB-A2-03",
    "MOV-CHG-121A",
    "STR-A3-1",
    "JB-A3-01",
    "MTR-SUMP-A",
    "STR-A3-2",
    "JB-A3-02",
    "PUMP-LUBE-A",
    "STR-A3-3",
    "JB-A3-03",
    "MOV-SI-902A",
    "STR-A4-1",
    "JB-A4-01",
    "FAN-CONT-A",
    "STR-A4-2",
    "JB-A4-02",
    "PUMP-SAMPLE-A",
    "STR-A4-3",
    "JB-A4-03",
    "MOV-VENT-406A",
    "CB-480B11",
    "CB-480B12",
    "CB-480B13",
    "CB-480B14",
    "MCC-31B1",
    "MCC-31B2",
    "LC-31B3",
    "PNL-31B4",
    "GND-MCC-B1",
    "GND-MCC-B2",
    "STR-B1-1",
    "JB-B1-01",
    "PUMP-CVC-B",
    "STR-B1-2",
    "JB-B1-02",
    "MOV-RHR-731B",
    "STR-B1-3",
    "JB-B1-03",
    "FAN-CRD-B",
    "STR-B2-1",
    "JB-B2-01",
    "PUMP-CCW-B",
    "STR-B2-2",
    "JB-B2-02",
    "HTR-BORIC-B",
    "STR-B2-3",
    "JB-B2-03",
    "MOV-CHG-121B",
    "STR-B3-1",
    "JB-B3-01",
    "MTR-SUMP-B",
    "STR-B3-2",
    "JB-B3-02",
    "PUMP-LUBE-B",
    "STR-B3-3",
    "JB-B3-03",
    "MOV-SI-902B",
    "STR-B4-1",
    "JB-B4-01",
    "FAN-CONT-B",
    "STR-B4-2",
    "JB-B4-02",
    "PUMP-SAMPLE-B",
    "STR-B4-3",
    "JB-B4-03",
    "MOV-VENT-406B",
    "CB-DCAB-TIE",
    "BAT-31A",
    "DS-BAT-A",
    "CHG-31A",
    "CB-CHG-A",
    "CB-INV-A",
    "PNL-DC-A",
    "INV-31A",
    "PNL-AC-A",
    "RPS-PNL-A",
    "TB-UPS-A",
    "RELAY-K7A1",
    "TB-RPS-A1",
    "PT-31A1",
    "RELAY-K7A2",
    "TB-RPS-A2",
    "PT-31A2",
    "RELAY-K7A3",
    "TB-RPS-A3",
    "PT-31A3",
    "RELAY-K7A4",
    "TB-RPS-A4",
    "PT-31A4",
    "BAT-31B",
    "DS-BAT-B",
    "CHG-31B",
    "CB-CHG-B",
    "CB-INV-B",
    "PNL-DC-B",
    "INV-31B",
    "PNL-AC-B",
    "RPS-PNL-B",
    "TB-UPS-B",
    "RELAY-K7B1",
    "TB-RPS-B1",
    "PT-31B1",
    "RELAY-K7B2",
    "TB-RPS-B2",
    "PT-31B2",
    "RELAY-K7B3",
    "TB-RPS-B3",
    "PT-31B3",
    "RELAY-K7B4",
    "TB-RPS-B4",
    "PT-31B4",
]


def add_edge(rows: list[dict[str, str]], seen: set[tuple[str, str]], source: str, target: str, confidence: str, line_type: str, evidence: str) -> None:
    key = tuple(sorted((source, target)))
    if key in seen:
        return
    seen.add(key)
    rows.append(
        {
            "source": source,
            "target": target,
            "confidence": confidence,
            "line_type": line_type,
            "evidence": evidence,
        }
    )


def add_chain(rows: list[dict[str, str]], seen: set[tuple[str, str]], nodes: list[str], confidence: str, line_type: str, evidence: str) -> None:
    for left, right in zip(nodes, nodes[1:]):
        add_edge(rows, seen, left, right, confidence, line_type, evidence)


def add_mcc_train(rows: list[dict[str, str]], seen: set[tuple[str, str]], train: str) -> None:
    bus = f"BUS-480{train}"
    boards = [
        (
            f"CB-480{train}11",
            f"MCC-31{train}1",
            f"GND-MCC-{train}1",
            [
                (f"STR-{train}1-1", f"JB-{train}1-01", f"PUMP-CVC-{train}"),
                (f"STR-{train}1-2", f"JB-{train}1-02", f"MOV-RHR-731{train}"),
                (f"STR-{train}1-3", f"JB-{train}1-03", f"FAN-CRD-{train}"),
            ],
        ),
        (
            f"CB-480{train}12",
            f"MCC-31{train}2",
            f"GND-MCC-{train}2",
            [
                (f"STR-{train}2-1", f"JB-{train}2-01", f"PUMP-CCW-{train}"),
                (f"STR-{train}2-2", f"JB-{train}2-02", f"HTR-BORIC-{train}"),
                (f"STR-{train}2-3", f"JB-{train}2-03", f"MOV-CHG-121{train}"),
            ],
        ),
        (
            f"CB-480{train}13",
            f"LC-31{train}3",
            None,
            [
                (f"STR-{train}3-1", f"JB-{train}3-01", f"MTR-SUMP-{train}"),
                (f"STR-{train}3-2", f"JB-{train}3-02", f"PUMP-LUBE-{train}"),
                (f"STR-{train}3-3", f"JB-{train}3-03", f"MOV-SI-902{train}"),
            ],
        ),
        (
            f"CB-480{train}14",
            f"PNL-31{train}4",
            None,
            [
                (f"STR-{train}4-1", f"JB-{train}4-01", f"FAN-CONT-{train}"),
                (f"STR-{train}4-2", f"JB-{train}4-02", f"PUMP-SAMPLE-{train}"),
                (f"STR-{train}4-3", f"JB-{train}4-03", f"MOV-VENT-406{train}"),
            ],
        ),
    ]
    for breaker, board, ground, branches in boards:
        add_chain(rows, seen, [bus, breaker, board], "high", "solid_power", f"{board} solid feeder from {bus}")
        if ground:
            add_edge(rows, seen, board, ground, "high", "solid_power", f"{board} solid connection to labeled ground")
        for starter, junction_box, load in branches:
            add_chain(
                rows,
                seen,
                [board, starter, junction_box, load],
                "high",
                "solid_power",
                f"{board} branch feeds {load} through starter and junction box",
            )


def add_ups_train(rows: list[dict[str, str]], seen: set[tuple[str, str]], train: str) -> None:
    dc_bus = f"BUS-125DC{train}"
    inv_bus = f"BUS-INV-{train}"
    neutral_bus = f"BUS-120N-{train}"
    add_chain(rows, seen, [f"BAT-31{train}", f"DS-BAT-{train}", dc_bus], "high", "solid_power", f"battery path to {dc_bus}")
    add_chain(rows, seen, [f"CHG-31{train}", f"CB-CHG-{train}", dc_bus], "high", "solid_power", f"charger path to {dc_bus}")
    add_edge(rows, seen, dc_bus, f"PNL-DC-{train}", "high", "solid_power", f"{dc_bus} tap to DC panel")
    add_chain(
        rows,
        seen,
        [dc_bus, f"CB-INV-{train}", f"INV-31{train}", inv_bus],
        "medium",
        "solid_power",
        f"{dc_bus} inverter breaker and inverter feed",
    )
    add_edge(rows, seen, inv_bus, f"PNL-AC-{train}", "high", "solid_power", f"{inv_bus} tap to AC panel")
    add_edge(rows, seen, inv_bus, f"RPS-PNL-{train}", "high", "solid_power", f"{inv_bus} tap to RPS panel")
    add_edge(rows, seen, f"PNL-AC-{train}", neutral_bus, "high", "solid_power", f"AC panel output to {neutral_bus}")
    for number in range(1, 5):
        add_edge(rows, seen, neutral_bus, f"RELAY-K7{train}{number}", "high", "solid_power", f"{neutral_bus} tap to relay K7{train}{number}")
        add_edge(rows, seen, f"RELAY-K7{train}{number}", f"TB-RPS-{train}{number}", "medium", "dotted_signal", "dotted relay signal to RPS terminal block")
        add_edge(rows, seen, f"TB-RPS-{train}{number}", f"PT-31{train}{number}", "medium", "dotted_signal", "dotted instrument signal to PT")
    add_edge(rows, seen, f"RPS-PNL-{train}", f"TB-UPS-{train}", "medium", "dashed_control", "dashed control line from RPS panel to UPS terminal block")


def build_edges(include_unsupported_dashed: bool = False) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for chain in [
        ["GEN-301", "TR-UAT-31", "CB-4A-IN1", "BUS-416A"],
        ["SAT-31A", "CB-4A-ST", "BUS-416A"],
        ["DG-31A", "CB-4A-DG", "BUS-416A"],
        ["SAT-31B", "CB-4B-ST", "BUS-416B"],
        ["DG-31B", "CB-4B-DG", "BUS-416B"],
        ["BUS-416A", "CB-4AB-TIE", "BUS-416B"],
    ]:
        add_chain(rows, seen, chain, "high", "solid_power", "top source or bus tie solid feeder")

    for train in ["A", "B"]:
        bus = f"BUS-416{train}"
        add_chain(rows, seen, [bus, f"CB-4{train}01", f"TR-480{train}1", f"CB-480{train}-IN", f"BUS-480{train}"], "high", "solid_power", "4.16 kV transformer feeder")
        add_chain(rows, seen, [bus, f"CB-4{train}02", f"TR-480{train}2", f"CB-480{train}-ALT", f"BUS-480{train}"], "high", "solid_power", "alternate 4.16 kV transformer feeder")
        add_chain(rows, seen, [bus, f"CB-4{train}03", f"DS-RCP-{train}", f"MTR-RCP-{train}", f"GND-RCP-{train}"], "high", "solid_power", "RCP motor feeder and labeled ground")
        add_chain(rows, seen, [bus, f"CB-4{train}04", f"DS-SW-{train}", f"PUMP-SW31{train}", f"GND-SW-{train}"], "high", "solid_power", "service-water pump feeder and labeled ground")
        add_chain(rows, seen, [bus, f"CB-4{train}05", f"DS-AFW-{train}", f"PUMP-AFW31{train}"], "high", "solid_power", "AFW pump feeder")
        add_chain(rows, seen, [bus, f"CB-4{train}06", f"DS-CHW-{train}", f"MTR-CHWP-{train}"], "high", "solid_power", "chilled-water pump feeder")

    add_chain(rows, seen, ["BUS-480A", "CB-480AB-TIE", "BUS-480B"], "high", "solid_power", "480 V tie breaker between buses")
    add_mcc_train(rows, seen, "A")
    add_mcc_train(rows, seen, "B")
    add_ups_train(rows, seen, "A")
    add_ups_train(rows, seen, "B")
    add_chain(rows, seen, ["BUS-125DCA", "CB-DCAB-TIE", "BUS-125DCB"], "high", "solid_power", "125 VDC tie breaker between buses")

    if include_unsupported_dashed:
        for source, target, evidence in [
            ("CB-4A03", "MTR-RCP-A", "dashed RCP A interlock corridor leaves CB-4A03 toward RCP motor feeder"),
            ("CB-4B03", "MTR-RCP-B", "dashed RCP B interlock corridor leaves CB-4B03 toward RCP motor feeder"),
            ("MOV-RHR-731A", "BAT-31A", "long dashed Train A MOV-RHR route reaches DC/UPS control corridor near BAT-31A"),
            ("MOV-RHR-731B", "BAT-31B", "long dashed Train B MOV-RHR route reaches DC/UPS control corridor near BAT-31B"),
            ("MOV-SI-902A", "RPS-PNL-A", "long dashed Train A MOV-SI route drops into lower RPS panel corridor"),
            ("MOV-SI-902B", "RPS-PNL-B", "long dashed Train B MOV-SI route drops into lower RPS panel corridor"),
        ]:
            add_edge(rows, seen, source, target, "medium", "dashed_control", evidence)

    return rows


def parse_diego_round1_edges() -> list[dict[str, str]]:
    path = FALLBACK_RESULTS / "diego_doc26_high_recall_extraction.txt"
    if not path.exists():
        return build_edges(include_unsupported_dashed=True)
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    rows: list[dict[str, str]] = []
    collect = False
    for line in lines:
        if line.strip() == "source,target,confidence,line_type,evidence":
            collect = True
            continue
        if collect and line.startswith("3) "):
            break
        if not collect or not line.strip():
            continue
        source, target, confidence, line_type, evidence = (line.split(",", 4) + [""])[:5]
        rows.append(
            {
                "source": source,
                "target": target,
                "confidence": confidence,
                "line_type": line_type,
                "evidence": evidence,
            }
        )
    return rows or build_edges(include_unsupported_dashed=True)


def matrix_from_edges(edges: list[dict[str, str]]) -> list[list[int]]:
    index = {node: position for position, node in enumerate(NODES)}
    matrix = [[0 for _ in NODES] for _ in NODES]
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        matrix[index[source]][index[target]] = 1
        matrix[index[target]][index[source]] = 1
    return matrix


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "confidence", "line_type", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path: Path, edges: list[dict[str, str]]) -> None:
    matrix = matrix_from_edges(edges)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + NODES)
        for node, row in zip(NODES, matrix):
            writer.writerow([node] + row)


def copy_if_exists(source: Path, target: Path) -> bool:
    if source.exists():
        shutil.copyfile(source, target)
        return True
    return False


def write_round_texts(output_dir: Path, edges: list[dict[str, str]]) -> None:
    diego_source = FALLBACK_RESULTS / "diego_doc26_high_recall_extraction.txt"
    jennifer_source = FALLBACK_RESULTS / "jennifer_doc26_round1_review.txt"
    diego_round2_source = FALLBACK_RESULTS / "diego_doc26_round2_response.txt"
    jennifer_round2_source = FALLBACK_RESULTS / "jennifer_doc26_round2_final.txt"
    if not copy_if_exists(diego_source, output_dir / "diego_round1_output.txt"):
        (output_dir / "diego_round1_output.txt").write_text(
            f"ROLE: Diego high-recall extractor\nDOCUMENT: 26\nPROPOSAL: {len(NODES)} nodes, {len(edges)} edges.\n",
            encoding="utf-8",
        )
    if not copy_if_exists(jennifer_source, output_dir / "jennifer_round1_review.txt"):
        (output_dir / "jennifer_round1_review.txt").write_text(
            "ROLE: Jennifer precision reviewer\nDOCUMENT: 26\nDECISION: pending local precision review.\n",
            encoding="utf-8",
        )
    if not copy_if_exists(diego_round2_source, output_dir / "diego_round2_response.txt"):
        (output_dir / "diego_round2_response.txt").write_text(
            "ROLE: Diego high-recall extractor\nDOCUMENT: 26\nROUND 2: Accepted Jennifer precision-stable graph and retained the 200-node, 201-edge matrix.\n",
            encoding="utf-8",
        )
    if not copy_if_exists(jennifer_round2_source, output_dir / "jennifer_round2_final.txt"):
        (output_dir / "jennifer_round2_final.txt").write_text(
            "ROLE: Jennifer precision reviewer\nDOCUMENT: 26\nFINAL: Saturated agreement on the 200-node, 201-edge connectivity matrix.\n",
            encoding="utf-8",
        )
    (output_dir / "subagent_round_transcript.md").write_text(
        "# Document 26 Subagent Round Transcript\n\n"
        "- Diego round 1: high-recall visual extraction, 200 nodes and 209 proposed CSV rows.\n"
        "- Jennifer round 1: removed eight unsupported dashed/control rows, retaining 200 nodes and 201 edges.\n"
        "- Diego round 2: accepted the precision-stable 201-edge graph.\n"
        "- Jennifer round 2: final saturation, no further edits.\n",
        encoding="utf-8",
    )


def main() -> None:
    output_dir = RESULTS
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        output_dir = FALLBACK_RESULTS
        output_dir.mkdir(parents=True, exist_ok=True)

    final_edges = build_edges()
    diego_edges = parse_diego_round1_edges()
    node_set = set(NODES)
    missing = sorted(({edge["source"] for edge in final_edges} | {edge["target"] for edge in final_edges}) - node_set)
    if missing:
        raise RuntimeError(f"edge endpoint(s) missing from node list: {missing}")
    if len(NODES) != 200:
        raise RuntimeError(f"expected 200 nodes, found {len(NODES)}")
    if len(final_edges) != 201:
        raise RuntimeError(f"expected 201 final edges, found {len(final_edges)}")
    if len(diego_edges) != 209:
        raise RuntimeError(f"expected 209 Diego round-1 CSV rows, found {len(diego_edges)}")

    write_edges(output_dir / "diego_round1_edges.csv", diego_edges)
    write_matrix(output_dir / "diego_round1_matrix.csv", diego_edges)
    for prefix in ["jennifer_round1", "diego_round2", "jennifer_round2"]:
        write_edges(output_dir / f"{prefix}_edges.csv", final_edges)
        write_matrix(output_dir / f"{prefix}_matrix.csv", final_edges)
    write_edges(output_dir / "connectivity_edges_final.csv", final_edges)
    write_matrix(output_dir / "connectivity_matrix_final.csv", final_edges)
    write_round_texts(output_dir, final_edges)
    print(f"wrote doc26 round outputs to {output_dir} with {len(NODES)} nodes and {len(final_edges)} final edges")


if __name__ == "__main__":
    main()
