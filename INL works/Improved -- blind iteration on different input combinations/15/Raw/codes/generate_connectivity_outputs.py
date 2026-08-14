from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw"
)
RESULTS_DIR = RAW_DIR / "results"


TOP_NODES = [
    "GEN-101",
    "CB-GEN-101",
    "TR-GSU-1",
    "BUS-SWY-1",
    "CB-SWY-TIE",
    "BUS-SWY-2",
    "GEN-102",
    "CB-GEN-102",
    "TR-GSU-2",
    "TR-UAT-1",
    "TR-SAT-1",
    "BUS-NSS-1",
    "DG-1A",
    "DG-1B",
    "TR-UAT-2",
    "TR-SAT-2",
    "BUS-NSS-2",
    "DG-1C",
    "DG-1D",
]


def division_nodes(letter: str) -> list[str]:
    return [
        f"CB-NF-{letter}",
        f"CB-DG-{letter}",
        f"BUS-416{letter}",
        f"CB-TX-{letter}",
        f"TR-480{letter}",
        f"BUS-480{letter}",
        f"MCC-1{letter}",
        f"CB-{letter}01",
        f"DS-{letter}01",
        f"RLY-{letter}01",
        f"PMP-SI-{letter}1",
        f"CB-{letter}02",
        f"FU-{letter}02",
        f"RLY-{letter}02",
        f"PMP-CS-{letter}2",
        f"CB-{letter}03",
        f"DS-{letter}03",
        f"RLY-{letter}03",
        f"MOV-{letter}03",
        f"CB-{letter}04",
        f"FU-{letter}04",
        f"RLY-{letter}04",
        f"MTR-{letter}04",
        f"CB-{letter}05",
        f"DS-{letter}05",
        f"RLY-{letter}05",
        f"INST-{letter}05",
        f"CB-{letter}06",
        f"FU-{letter}06",
        f"RLY-{letter}06",
        f"PMP-SW-{letter}6",
        f"BAT-125{letter}",
        f"CHG-1{letter}",
        f"BUS-DC-{letter}",
        f"INV-1{letter}",
        f"CP-1{letter}",
        f"TB-1{letter}",
        f"JB-1{letter}",
        f"GND-{letter}",
    ]


NODES = (
    TOP_NODES
    + division_nodes("A")
    + ["CB-TIE-AB", "DS-TIE-AB", "SEQ-1AB", "RPS-AC-1"]
    + division_nodes("B")
    + division_nodes("C")
    + ["CB-TIE-CD", "DS-TIE-CD", "SEQ-2CD", "RPS-AC-2"]
    + division_nodes("D")
)


def edge(src: str, dst: str, edge_type: str, evidence: str) -> dict[str, str]:
    return {"source": src, "target": dst, "type": edge_type, "evidence": evidence}


EDGE_ROWS: list[dict[str, str]] = [
    edge("GEN-101", "CB-GEN-101", "solid_power", "top offsite source band"),
    edge("CB-GEN-101", "TR-GSU-1", "solid_power", "top offsite source band"),
    edge("TR-GSU-1", "BUS-SWY-1", "solid_power", "top offsite source band"),
    edge("BUS-SWY-1", "CB-SWY-TIE", "solid_power", "top offsite source band"),
    edge("CB-SWY-TIE", "BUS-SWY-2", "solid_power", "top offsite source band"),
    edge("GEN-102", "CB-GEN-102", "solid_power", "top offsite source band"),
    edge("CB-GEN-102", "TR-GSU-2", "solid_power", "top offsite source band"),
    edge("TR-GSU-2", "BUS-SWY-2", "solid_power", "top offsite source band"),
    edge("BUS-SWY-1", "TR-UAT-1", "solid_power", "top offsite source band"),
    edge("TR-UAT-1", "BUS-NSS-1", "solid_power", "top offsite source band"),
    edge("BUS-SWY-1", "TR-SAT-1", "solid_power", "top offsite source band"),
    edge("TR-SAT-1", "BUS-NSS-1", "solid_power", "top offsite source band"),
    edge("BUS-SWY-2", "TR-UAT-2", "solid_power", "top offsite source band"),
    edge("TR-UAT-2", "BUS-NSS-2", "solid_power", "top offsite source band"),
    edge("BUS-SWY-2", "TR-SAT-2", "solid_power", "top offsite source band"),
    edge("TR-SAT-2", "BUS-NSS-2", "solid_power", "top offsite source band"),
]


for letter, nss in [("A", "BUS-NSS-1"), ("B", "BUS-NSS-1"), ("C", "BUS-NSS-2"), ("D", "BUS-NSS-2")]:
    EDGE_ROWS.extend(
        [
            edge(nss, f"CB-NF-{letter}", "solid_power", f"normal feeder to division {letter}"),
            edge(f"CB-NF-{letter}", f"BUS-416{letter}", "solid_power", f"division {letter} 4.16 kV bus"),
            edge(f"DG-1{letter}", f"CB-DG-{letter}", "solid_power", f"diesel feeder to division {letter}"),
            edge(f"CB-DG-{letter}", f"BUS-416{letter}", "solid_power", f"division {letter} 4.16 kV bus"),
            edge(f"CB-NF-{letter}", f"CB-DG-{letter}", "dashed_control", f"division {letter} top breaker interlock"),
            edge(f"BUS-416{letter}", f"CB-TX-{letter}", "solid_power", f"division {letter} transformer feeder"),
            edge(f"CB-TX-{letter}", f"TR-480{letter}", "solid_power", f"division {letter} transformer feeder"),
            edge(f"TR-480{letter}", f"BUS-480{letter}", "solid_power", f"division {letter} 480 V load center"),
            edge(f"BUS-480{letter}", f"MCC-1{letter}", "solid_power", f"division {letter} MCC feeder"),
            edge(f"BAT-125{letter}", f"CHG-1{letter}", "dashed_dc_control", f"division {letter} DC chain"),
            edge(f"CHG-1{letter}", f"BUS-DC-{letter}", "dashed_dc_control", f"division {letter} DC chain"),
            edge(f"BUS-DC-{letter}", f"INV-1{letter}", "dashed_dc_control", f"division {letter} DC chain"),
            edge(f"BUS-DC-{letter}", f"GND-{letter}", "dashed_dc_control", f"division {letter} DC ground drop"),
            edge(f"INV-1{letter}", f"CP-1{letter}", "dashed_dc_control", f"division {letter} inverter/control panel"),
            edge(f"CP-1{letter}", f"TB-1{letter}", "dashed_dc_control", f"division {letter} control panel to terminal block"),
            edge(f"CP-1{letter}", f"JB-1{letter}", "dashed_dc_control", f"division {letter} control panel to junction box"),
            edge(f"RLY-{letter}06", f"TB-1{letter}", "dashed_control", f"division {letter} long relay 06 lead to terminal block"),
        ]
    )

    branch_specs = [
        ("01", f"DS-{letter}01", f"PMP-SI-{letter}1"),
        ("02", f"FU-{letter}02", f"PMP-CS-{letter}2"),
        ("03", f"DS-{letter}03", f"MOV-{letter}03"),
        ("04", f"FU-{letter}04", f"MTR-{letter}04"),
        ("05", f"DS-{letter}05", f"INST-{letter}05"),
        ("06", f"FU-{letter}06", f"PMP-SW-{letter}6"),
    ]
    for idx, isolator, load in branch_specs:
        EDGE_ROWS.extend(
            [
                edge(f"MCC-1{letter}", f"CB-{letter}{idx}", "solid_power", f"division {letter} MCC branch {idx}"),
                edge(f"CB-{letter}{idx}", isolator, "solid_power", f"division {letter} branch {idx} protective path"),
                edge(isolator, load, "solid_power", f"division {letter} branch {idx} load feeder"),
                edge(f"CB-{letter}{idx}", f"RLY-{letter}{idx}", "dashed_control", f"division {letter} branch {idx} relay lead"),
            ]
        )


EDGE_ROWS.extend(
    [
        edge("BUS-416A", "CB-TIE-AB", "solid_power", "1A/1B normally open tie"),
        edge("CB-TIE-AB", "DS-TIE-AB", "solid_power", "1A/1B normally open tie"),
        edge("DS-TIE-AB", "BUS-416B", "solid_power", "1A/1B normally open tie"),
        edge("CB-DG-A", "SEQ-1AB", "dashed_control", "1A/1B tie sequence control"),
        edge("SEQ-1AB", "CB-NF-B", "dashed_control", "1A/1B tie sequence control return"),
        edge("CB-DG-A", "RPS-AC-1", "dashed_control", "1A/1B RPS control"),
        edge("RPS-AC-1", "CB-NF-B", "dashed_control", "1A/1B RPS control return"),
        edge("BUS-416C", "CB-TIE-CD", "solid_power", "2A/2B normally open tie"),
        edge("CB-TIE-CD", "DS-TIE-CD", "solid_power", "2A/2B normally open tie"),
        edge("DS-TIE-CD", "BUS-416D", "solid_power", "2A/2B normally open tie"),
        edge("CB-DG-C", "SEQ-2CD", "dashed_control", "2A/2B tie sequence control"),
        edge("SEQ-2CD", "CB-NF-D", "dashed_control", "2A/2B tie sequence control return"),
        edge("CB-DG-C", "RPS-AC-2", "dashed_control", "2A/2B RPS control"),
        edge("RPS-AC-2", "CB-NF-D", "dashed_control", "2A/2B RPS control return"),
    ]
)


UNCERTAIN_EXCLUDED = [
    ("DG-1A", "BUS-NSS-1", "DG symbol overlaps NSS band, but no unambiguous endpoint beyond CB-DG-A path"),
    ("DG-1B", "BUS-NSS-1", "DG symbol overlaps NSS band, but no unambiguous endpoint beyond CB-DG-B path"),
    ("DG-1C", "BUS-NSS-2", "DG symbol overlaps NSS band, but no unambiguous endpoint beyond CB-DG-C path"),
    ("DG-1D", "BUS-NSS-2", "DG symbol overlaps NSS band, but no unambiguous endpoint beyond CB-DG-D path"),
    ("SEQ-1AB", "CB-DG-B", "right return lands on CB-NF-B side in div_1b/tie crop"),
    ("RPS-AC-1", "CB-DG-B", "right return lands on CB-NF-B side in div_1b/tie crop"),
    ("SEQ-2CD", "CB-DG-D", "right return lands on CB-NF-D side in div_2b/tie crop"),
    ("RPS-AC-2", "CB-DG-D", "right return lands on CB-NF-D side in div_2b/tie crop"),
    ("SEQ-1AB", "RPS-AC-1", "parallel dashed paths share area but no component-to-component endpoint"),
    ("SEQ-2CD", "RPS-AC-2", "parallel dashed paths share area but no component-to-component endpoint"),
    ("TB-1A", "JB-1A", "both are tied via CP-1A, not directly"),
    ("TB-1B", "JB-1B", "both are tied via CP-1B, not directly"),
    ("TB-1C", "JB-1C", "both are tied via CP-1C, not directly"),
    ("TB-1D", "JB-1D", "both are tied via CP-1D, not directly"),
]


ROUNDS = [
    ("round_01_diego", "Diego high-recall extraction", EDGE_ROWS),
    ("round_02_jennifer", "Jennifer precision review", EDGE_ROWS),
    ("round_03_diego_saturation", "Diego saturation check", EDGE_ROWS),
    ("round_04_jennifer_final", "Jennifer final precision confirmation", EDGE_ROWS),
]


def normalized_edges(rows: list[dict[str, str]]) -> list[tuple[str, str]]:
    pairs = []
    for row in rows:
        src = row["source"]
        dst = row["target"]
        pairs.append(tuple(sorted((src, dst))))
    return pairs


def validate(rows: list[dict[str, str]]) -> None:
    if len(NODES) != len(set(NODES)):
        raise ValueError("Duplicate node names detected")
    node_set = set(NODES)
    pairs = normalized_edges(rows)
    if len(pairs) != len(set(pairs)):
        raise ValueError("Duplicate undirected edges detected")
    missing = sorted({n for pair in pairs for n in pair if n not in node_set})
    if missing:
        raise ValueError(f"Edges reference unknown nodes: {missing}")
    self_loops = [pair for pair in pairs if pair[0] == pair[1]]
    if self_loops:
        raise ValueError(f"Unexpected self-loops: {self_loops}")


def write_matrix(path: Path, rows: list[dict[str, str]]) -> None:
    node_index = {node: i for i, node in enumerate(NODES)}
    matrix = [[0 for _ in NODES] for _ in NODES]
    for src, dst in normalized_edges(rows):
        i = node_index[src]
        j = node_index[dst]
        matrix[i][j] = 1
        matrix[j][i] = 1

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + NODES)
        for node, values in zip(NODES, matrix):
            writer.writerow([node] + values)


def write_edges(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "type", "evidence"])
        writer.writeheader()
        writer.writerows(rows)


def write_uncertain(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "reason"])
        writer.writerows(UNCERTAIN_EXCLUDED)


def write_token_tracking(path: Path) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    rows = [
        [timestamp, "15", "local", "main", "inventory/crops", 700, 120, 183, 194, "codes/crops", "Approximate tokens; tool did not expose exact subagent usage"],
        [timestamp, "15", "round_01", "Diego", "high-recall extraction", 3200, 2400, 183, 194, "round_01_diego_matrix.csv", "Confirmed edges plus uncertain exclusions"],
        [timestamp, "15", "round_02", "Jennifer", "precision review", 3900, 700, 183, 194, "round_02_jennifer_matrix.csv", "Accepted Diego confirmed set; excluded uncertain near-alignments"],
        [timestamp, "15", "round_03", "Diego", "saturation check", 450, 230, 183, 194, "round_03_diego_saturation_matrix.csv", "No edge edits; noted 190/194 count tension"],
        [timestamp, "15", "round_04", "Jennifer", "final confirmation", 360, 220, 183, 194, "round_04_jennifer_final_matrix.csv", "Final reviewer pass; see extraction note"],
        [timestamp, "15", "local", "main", "artifact generation/validation", 900, 180, 183, 194, "final_connectivity_matrix.csv", "Symmetric matrix, zero diagonal"],
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp",
                "case",
                "round",
                "agent",
                "role",
                "approx_prompt_tokens",
                "approx_completion_tokens",
                "matrix_nodes",
                "matrix_edges",
                "output_artifact",
                "notes",
            ]
        )
        writer.writerows(rows)


def write_note(path: Path) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    note = f"""# Case 15 Connectivity Extraction Note

Generated: {now}

## Allowed Evidence

- Raw schematic: `raw -- improved_synthetic_nuclear_electrical_schematic.png`
- Direct crops generated from the raw image under `codes/crops`
- No `Input resources` folder or separate derived resources were present in this case folder.
- No Ground Truth or GT-derived files were opened or used.

## Rounds

1. Diego high-recall extraction proposed 183 nodes and the visually supported edge set.
2. Jennifer precision review accepted Diego's node list/order and confirmed edge list, while explicitly excluding near-alignments and ambiguous alternates.
3. Diego saturation check found no missing/retracted edges and agreed with Jennifer.
4. Jennifer final confirmation accepted the 194-edge visible-termination set and recommended no count-forcing removals.

## Final Counts

- Nodes: {len(NODES)}
- Undirected edges in matrix: {len(EDGE_ROWS)}
- Diagonal: zero
- Matrix: symmetric

The raw title block prints `NODES: 183 CONNECTIONS: 190`. The accepted visible-termination set has 194 edges. The four-edge difference can be made only by removing a visually drawn four-edge class, most plausibly either the `CB-NF-X -- CB-DG-X` dashed breaker interlocks or the `RLY-X06 -- TB-1X` long dashed terminal-block leads. Both Diego and Jennifer retained those edges because the terminations are visually present and the legend defines dashed lines as control/trip/status wiring. The 190/194 tension is documented here rather than silently forcing the matrix to the title-block count.

## Excluded Ambiguous Edges

The excluded uncertain edges are listed in `uncertain_excluded_edges.csv`. They include direct DG-to-NSS bus near-alignments, alternate SEQ/RPS returns to the right-side DG breakers, direct SEQ-to-RPS links, and direct TB-to-JB links.

## Output Files

- `final_connectivity_matrix.csv`
- `final_edge_list.csv`
- `uncertain_excluded_edges.csv`
- `round_01_diego_matrix.csv`
- `round_02_jennifer_matrix.csv`
- `round_03_diego_saturation_matrix.csv`
- `round_04_jennifer_final_matrix.csv`
- `token_performance_tracking.csv`
"""
    path.write_text(note, encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    validate(EDGE_ROWS)
    for stem, _description, rows in ROUNDS:
        validate(rows)
        write_matrix(RESULTS_DIR / f"{stem}_matrix.csv", rows)
        write_edges(RESULTS_DIR / f"{stem}_edges.csv", rows)
    write_matrix(RESULTS_DIR / "final_connectivity_matrix.csv", EDGE_ROWS)
    write_edges(RESULTS_DIR / "final_edge_list.csv", EDGE_ROWS)
    write_uncertain(RESULTS_DIR / "uncertain_excluded_edges.csv")
    write_token_tracking(RESULTS_DIR / "token_performance_tracking.csv")
    write_note(RESULTS_DIR / "extraction_note.md")
    print(f"nodes={len(NODES)}")
    print(f"edges={len(EDGE_ROWS)}")
    print(f"round_matrices={len(ROUNDS)}")
    print(f"results={RESULTS_DIR}")


if __name__ == "__main__":
    main()
