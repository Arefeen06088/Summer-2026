from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\37\Raw + wires")
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


FINAL_NODES = [
    "GRID-345",
    "CB-101",
    "CB-102",
    "AUX-TR-1A",
    "AUX-TR-1B",
    "BUS-6KA",
    "BUS-6KB",
    "CB-TIE-6KV",
    "CB-103A",
    "CB-103B",
    "6.9 kV SWGR A",
    "6.9 kV SWGR B",
    "DG-1A",
    "CB-DG1A",
    "DG-1B",
    "CB-DG1B",
    "ATS-1A",
    "ATS-1B",
    "RELAY-K12A",
    "RELAY-K12B",
    "TR-480A",
    "TR-480B",
    "BUS-480A",
    "BUS-480B",
    "MCC-1A",
    "MCC-1B",
    "PUMP-SI-1A",
    "PUMP-RHR-1A",
    "PUMP-CCW-1A",
    "FAN-RB-1A",
    "MOV-HPCI-1A",
    "VALVE-SW-1A",
    "PUMP-SI-1B",
    "PUMP-RHR-1B",
    "PUMP-CCW-1B",
    "FAN-RB-1B",
    "MOV-HPCI-1B",
    "VALVE-SW-1B",
    "CHGR-125A",
    "CHGR-125B",
    "BAT-125A",
    "BAT-125B",
    "BUS-125DCA",
    "BUS-125DCB",
    "GND-01A",
    "GND-01B",
    "INV-120A",
    "INV-120B",
    "BUS-120A",
    "BUS-120B",
    "PAN-RPS-A",
    "PAN-RPS-B",
    "INST-RACK-A",
    "INST-RACK-B",
    "PLC-ESF",
]


DIEGO_R1_NODES = [
    "GRID-345",
    "CB-101",
    "CB-102",
    "AUX-TR-1A",
    "AUX-TR-1B",
    "BUS-6KA",
    "BUS-6KB",
    "CB-TIE-6KV",
    "CB-103A/SWGR-1EA",
    "CB-103B/SWGR-1EB",
    "6.9 kV SWGR A",
    "6.9 kV SWGR B",
    "DG-1A",
    "CB-DG1A",
    "DG-1B",
    "CB-DG1B",
    "ATS-1A",
    "ATS-1B",
    "RELAY-K12A",
    "RELAY-K12B",
    "TR-480A",
    "TR-480B",
    "BUS-480A",
    "BUS-480B",
    "MCC-1A",
    "MCC-1B",
    "PUMP-SI-1A",
    "PUMP-RHR-1A",
    "PUMP-CCW-1A",
    "FAN-RB-1A",
    "MOV-HPCI-1A",
    "VALVE-SW-1A",
    "PUMP-SI-1B",
    "PUMP-RHR-1B",
    "PUMP-CCW-1B",
    "FAN-RB-1B",
    "MOV-HPCI-1B",
    "VALVE-SW-1B",
    "CHGR-125A",
    "CHGR-125B",
    "BAT-125A",
    "BAT-125B",
    "BUS-125DCA",
    "BUS-125DCB",
    "GND-01A",
    "GND-01B",
    "INV-120A",
    "INV-120B",
    "BUS-120A",
    "BUS-120B",
    "PAN-RPS-A",
    "PAN-RPS-B",
    "INST-RACK-A",
    "INST-RACK-B",
    "PLC-ESF",
]


DIEGO_R1_EDGES = [
    ("AUX-TR-1A", "CB-101"),
    ("CB-101", "GRID-345"),
    ("GRID-345", "CB-102"),
    ("CB-102", "AUX-TR-1B"),
    ("AUX-TR-1A", "BUS-6KA"),
    ("AUX-TR-1B", "BUS-6KB"),
    ("BUS-6KA", "CB-TIE-6KV"),
    ("CB-TIE-6KV", "BUS-6KB"),
    ("BUS-6KA", "CB-103A/SWGR-1EA"),
    ("CB-103A/SWGR-1EA", "6.9 kV SWGR A"),
    ("DG-1A", "CB-DG1A"),
    ("CB-DG1A", "6.9 kV SWGR A"),
    ("6.9 kV SWGR A", "ATS-1A"),
    ("ATS-1A", "TR-480A"),
    ("TR-480A", "BUS-480A"),
    ("BUS-6KB", "CB-103B/SWGR-1EB"),
    ("CB-103B/SWGR-1EB", "6.9 kV SWGR B"),
    ("DG-1B", "CB-DG1B"),
    ("CB-DG1B", "6.9 kV SWGR B"),
    ("6.9 kV SWGR B", "ATS-1B"),
    ("ATS-1B", "TR-480B"),
    ("TR-480B", "BUS-480B"),
    ("BUS-480A", "MCC-1A"),
    ("MCC-1A", "PUMP-SI-1A"),
    ("MCC-1A", "PUMP-RHR-1A"),
    ("MCC-1A", "PUMP-CCW-1A"),
    ("MCC-1A", "FAN-RB-1A"),
    ("MCC-1A", "MOV-HPCI-1A"),
    ("MCC-1A", "VALVE-SW-1A"),
    ("BUS-480B", "MCC-1B"),
    ("MCC-1B", "PUMP-SI-1B"),
    ("MCC-1B", "PUMP-RHR-1B"),
    ("MCC-1B", "PUMP-CCW-1B"),
    ("MCC-1B", "FAN-RB-1B"),
    ("MCC-1B", "MOV-HPCI-1B"),
    ("MCC-1B", "VALVE-SW-1B"),
    ("BUS-480A", "CHGR-125A"),
    ("CHGR-125A", "BUS-125DCA"),
    ("BAT-125A", "BUS-125DCA"),
    ("BUS-125DCA", "GND-01A"),
    ("BUS-125DCA", "INV-120A"),
    ("INV-120A", "BUS-120A"),
    ("BUS-120A", "PAN-RPS-A"),
    ("BUS-120A", "INST-RACK-A"),
    ("BUS-480B", "CHGR-125B"),
    ("CHGR-125B", "BUS-125DCB"),
    ("BAT-125B", "BUS-125DCB"),
    ("BUS-125DCB", "GND-01B"),
    ("BUS-125DCB", "INV-120B"),
    ("INV-120B", "BUS-120B"),
    ("BUS-120B", "PAN-RPS-B"),
    ("BUS-120B", "INST-RACK-B"),
    ("ATS-1A", "RELAY-K12A"),
    ("RELAY-K12A", "PLC-ESF"),
    ("PAN-RPS-A", "INST-RACK-A"),
    ("ATS-1B", "RELAY-K12B"),
    ("RELAY-K12B", "PLC-ESF"),
    ("PLC-ESF", "PAN-RPS-B"),
]


FINAL_EDGES = [
    ("AUX-TR-1A", "CB-101"),
    ("CB-101", "GRID-345"),
    ("GRID-345", "CB-102"),
    ("CB-102", "AUX-TR-1B"),
    ("AUX-TR-1A", "BUS-6KA"),
    ("AUX-TR-1B", "BUS-6KB"),
    ("BUS-6KA", "CB-TIE-6KV"),
    ("CB-TIE-6KV", "BUS-6KB"),
    ("BUS-6KA", "CB-103A"),
    ("CB-103A", "6.9 kV SWGR A"),
    ("DG-1A", "CB-DG1A"),
    ("CB-DG1A", "6.9 kV SWGR A"),
    ("6.9 kV SWGR A", "ATS-1A"),
    ("ATS-1A", "TR-480A"),
    ("TR-480A", "BUS-480A"),
    ("BUS-6KB", "CB-103B"),
    ("CB-103B", "6.9 kV SWGR B"),
    ("DG-1B", "CB-DG1B"),
    ("CB-DG1B", "6.9 kV SWGR B"),
    ("6.9 kV SWGR B", "ATS-1B"),
    ("ATS-1B", "TR-480B"),
    ("TR-480B", "BUS-480B"),
    ("BUS-480A", "MCC-1A"),
    ("MCC-1A", "PUMP-SI-1A"),
    ("MCC-1A", "PUMP-RHR-1A"),
    ("MCC-1A", "PUMP-CCW-1A"),
    ("MCC-1A", "FAN-RB-1A"),
    ("MCC-1A", "MOV-HPCI-1A"),
    ("MCC-1A", "VALVE-SW-1A"),
    ("BUS-480B", "MCC-1B"),
    ("MCC-1B", "PUMP-SI-1B"),
    ("MCC-1B", "PUMP-RHR-1B"),
    ("MCC-1B", "PUMP-CCW-1B"),
    ("MCC-1B", "FAN-RB-1B"),
    ("MCC-1B", "MOV-HPCI-1B"),
    ("MCC-1B", "VALVE-SW-1B"),
    ("BUS-480A", "CHGR-125A"),
    ("CHGR-125A", "BUS-125DCA"),
    ("BAT-125A", "BUS-125DCA"),
    ("BUS-125DCA", "GND-01A"),
    ("BUS-125DCA", "INV-120A"),
    ("INV-120A", "BUS-120A"),
    ("BUS-120A", "PAN-RPS-A"),
    ("BUS-120A", "INST-RACK-A"),
    ("BUS-480B", "CHGR-125B"),
    ("CHGR-125B", "BUS-125DCB"),
    ("BAT-125B", "BUS-125DCB"),
    ("BUS-125DCB", "GND-01B"),
    ("BUS-125DCB", "INV-120B"),
    ("INV-120B", "BUS-120B"),
    ("BUS-120B", "PAN-RPS-B"),
    ("BUS-120B", "INST-RACK-B"),
    ("ATS-1A", "RELAY-K12A"),
    ("ATS-1B", "RELAY-K12B"),
    ("PAN-RPS-A", "INST-RACK-A"),
    ("PLC-ESF", "PAN-RPS-B"),
]


ROUNDS = [
    {
        "document": 37,
        "iteration": 1,
        "round": "R1",
        "agent": "Diego",
        "agent_id": "019f76e4-547a-7673-b2f0-8f62bea4d410",
        "nodes": DIEGO_R1_NODES,
        "edges": DIEGO_R1_EDGES,
        "status": "high-recall proposal",
    },
    {
        "document": 37,
        "iteration": 1,
        "round": "R1",
        "agent": "Jennifer",
        "agent_id": "019f76ea-6984-7e63-9576-40ef191c90ce",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "status": "precision refinement",
    },
    {
        "document": 37,
        "iteration": 1,
        "round": "R2",
        "agent": "Diego",
        "agent_id": "019f76ef-9fbd-77c2-9d95-fbffb7f9e552",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "status": "consensus reached",
    },
    {
        "document": 37,
        "iteration": 1,
        "round": "R2",
        "agent": "Jennifer",
        "agent_id": "019f76f3-ef72-7983-87ad-a30470372036",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
        "status": "final confirmation, unchanged",
    },
]


UNCERTAIN_EXCLUDED = [
    "RELAY-K12A -- PLC-ESF",
    "RELAY-K12B -- PLC-ESF",
    "PAN-RPS-A -- PLC-ESF",
    "INST-RACK-A -- PLC-ESF",
    "PLC-ESF -- INST-RACK-B",
    "CB-TIE-6KV -- PLC-ESF",
]


IMAGE_PAYLOADS = {
    "Diego R1": [
        (5100, 3300),
        (5100, 3300),
        (5100, 3300),
        (10200, 3000),
        (6000, 2400),
        (5600, 2400),
        (5600, 2400),
        (5600, 2400),
        (5600, 2400),
        (6000, 2400),
        (8200, 3200),
        (5600, 2400),
        (5600, 2400),
    ],
    "Jennifer R1": [
        (5100, 3300),
        (5100, 3300),
        (5100, 3300),
        (10200, 3000),
        (6000, 2400),
        (5600, 2400),
        (5600, 2400),
        (5600, 2400),
        (5600, 2400),
        (10000, 2800),
        (8200, 3200),
        (10000, 2800),
    ],
    "Diego R2": [
        (5100, 3300),
        (10200, 3000),
        (6000, 2400),
        (10000, 2800),
        (5600, 2400),
        (5600, 2400),
        (10000, 2800),
        (5100, 3300),
    ],
    "Jennifer R2": [
        (5100, 3300),
        (10200, 3000),
        (10000, 2800),
        (6000, 2400),
        (10000, 2800),
    ],
}


TEXT_TOKEN_ESTIMATES = {
    "Main orchestration": {"input": 2400, "output_expected": 1800},
    "Diego R1": {"input": 1850, "output_expected": 2200},
    "Jennifer R1": {"input": 2800, "output_expected": 1900},
    "Diego R2": {"input": 2300, "output_expected": 900},
    "Jennifer R2": {"input": 1650, "output_expected": 350},
}


def image_tokens(width: int, height: int) -> int:
    """Offline proxy: OpenAI low-detail base plus tiled 512px high-detail cost."""
    return 85 + 170 * math.ceil(width / 512) * math.ceil(height / 512)


def write_edges(round_info: dict) -> None:
    out = RESULTS / f"doc37_iteration1_{round_info['agent'].lower()}_{round_info['round'].lower()}_edges.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["source", "target"])
        for source, target in round_info["edges"]:
            writer.writerow([source, target])


def write_matrix(round_info: dict) -> None:
    nodes = round_info["nodes"]
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for source, target in round_info["edges"]:
        if source not in index or target not in index:
            raise ValueError(f"Unknown node in {round_info['agent']} {round_info['round']}: {source} -- {target}")
        i = index[source]
        j = index[target]
        if i == j:
            raise ValueError(f"Self-loop not expected: {source}")
        matrix[i][j] = 1
        matrix[j][i] = 1

    out = RESULTS / f"doc37_iteration1_{round_info['agent'].lower()}_{round_info['round'].lower()}_matrix.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + nodes)
        for node, row in zip(nodes, matrix):
            writer.writerow([node] + row)

    if round_info["agent"] == "Jennifer" and round_info["round"] == "R2":
        final_out = RESULTS / "connectivity_matrix_final.csv"
        final_edges = RESULTS / "connectivity_edges_final.csv"
        final_out.write_text(out.read_text(encoding="utf-8"), encoding="utf-8")
        final_edges.write_text(
            (RESULTS / "doc37_iteration1_jennifer_r2_edges.csv").read_text(encoding="utf-8"),
            encoding="utf-8",
        )


def write_notes() -> None:
    notes = {
        "document": 37,
        "iteration": 1,
        "resource_folder": str(ROOT),
        "constraints": [
            "Only Raw + wires resources used.",
            "No GT or GT-derived feedback used.",
            "No off-the-shelf OCR used.",
            "Pxx, Cxx, G01/G02 treated as evidence tags, not matrix nodes.",
        ],
        "canonical_nodes": FINAL_NODES,
        "final_edges": [f"{source} -- {target}" for source, target in FINAL_EDGES],
        "excluded_uncertain_edges": UNCERTAIN_EXCLUDED,
        "rounds": [
            {
                "round": f"{item['agent']} {item['round']}",
                "agent_id": item["agent_id"],
                "status": item["status"],
                "node_count": len(item["nodes"]),
                "edge_count": len(item["edges"]),
            }
            for item in ROUNDS
        ],
        "visual_evidence_summary": [
            "Solid AUX/TR-CB-GRID-CB-TR chain and 6.9 kV bus tie through CB-TIE-6KV are visible in top crop.",
            "CB-103A/B are retained as breaker nodes feeding the 6.9 kV SWGR A/B panels; SWGR-1EA/B text is not used as a separate node.",
            "MCC-1A/B are the matrix nodes; SAFETY MCC A/B captions are not separate nodes.",
            "DC/120 V taps to chargers, batteries, grounds, inverters, buses, panels, and racks show filled junction dots.",
            "C01/C04 support ATS-to-relay control edges; C03 supports PAN-RPS-A to INST-RACK-A; C06 supports PLC-ESF to PAN-RPS-B.",
            "C02/C05 relay-to-PLC paths do not show clean endpoints and are excluded.",
        ],
    }
    (RESULTS / "doc37_iteration1_consensus_notes.json").write_text(
        json.dumps(notes, indent=2), encoding="utf-8"
    )


def write_token_report() -> None:
    rows = []
    for call_name, estimate in TEXT_TOKEN_ESTIMATES.items():
        image_total = sum(image_tokens(w, h) for w, h in IMAGE_PAYLOADS.get(call_name, []))
        input_total = estimate["input"] + image_total
        expected_output = estimate["output_expected"]
        rows.append(
            {
                "document": 37,
                "iteration": 1,
                "model_call": call_name,
                "input_tokens_est": input_total,
                "cached_input_tokens": "not exposed",
                "output_tokens_low_est": int(expected_output * 0.65),
                "output_tokens_expected_est": expected_output,
                "output_tokens_high_est": int(expected_output * 1.45),
                "reasoning_tokens": "not exposed",
                "image_file_input_tokens_est": image_total,
                "usage_object": "unavailable in Codex subagent tool response",
            }
        )

    total_input = sum(row["input_tokens_est"] for row in rows)
    total_image = sum(row["image_file_input_tokens_est"] for row in rows)
    total_low = sum(row["output_tokens_low_est"] for row in rows)
    total_expected = sum(row["output_tokens_expected_est"] for row in rows)
    total_high = sum(row["output_tokens_high_est"] for row in rows)
    rows.append(
        {
            "document": 37,
            "iteration": 1,
            "model_call": "TOTAL",
            "input_tokens_est": total_input,
            "cached_input_tokens": "not exposed",
            "output_tokens_low_est": total_low,
            "output_tokens_expected_est": total_expected,
            "output_tokens_high_est": total_high,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est": total_image,
            "usage_object": "offline estimate only",
        }
    )

    token_csv = RESULTS / "doc37_iteration1_token_usage_estimate.csv"
    with token_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md = [
        "# Document 37 Iteration 1 Token Usage Estimate",
        "",
        "Exact Responses token counting and usage objects were unavailable because no API key/usage object was exposed in this environment. Image tokens use an offline proxy: `85 + 170 * ceil(width/512) * ceil(height/512)` per image payload.",
        "",
        "| Document | Iteration | Model call | Input est | Image/file input est | Cached input | Output low | Output expected | Output high | Reasoning |",
        "|---:|---:|---|---:|---:|---|---:|---:|---:|---|",
    ]
    for row in rows:
        md.append(
            f"| {row['document']} | {row['iteration']} | {row['model_call']} | "
            f"{row['input_tokens_est']} | {row['image_file_input_tokens_est']} | "
            f"{row['cached_input_tokens']} | {row['output_tokens_low_est']} | "
            f"{row['output_tokens_expected_est']} | {row['output_tokens_high_est']} | "
            f"{row['reasoning_tokens']} |"
        )
    md.extend(
        [
            "",
            "Model calls identified:",
            "- Main orchestration by Codex.",
            "- Diego R1 high-recall extraction, agent `019f76e4-547a-7673-b2f0-8f62bea4d410`.",
            "- Jennifer R1 precision review, agent `019f76ea-6984-7e63-9576-40ef191c90ce`.",
            "- Diego R2 saturation pass, agent `019f76ef-9fbd-77c2-9d95-fbffb7f9e552`.",
            "- Jennifer R2 final confirmation, agent `019f76f3-ef72-7983-87ad-a30470372036`.",
        ]
    )
    (RESULTS / "doc37_iteration1_token_usage_estimate.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def validate_final() -> dict:
    final_matrix = RESULTS / "connectivity_matrix_final.csv"
    with final_matrix.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    nodes = rows[0][1:]
    matrix = [[int(value) for value in row[1:]] for row in rows[1:]]
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    diagonal_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    undirected_edges = sum(sum(row) for row in matrix) // 2
    result = {
        "node_count": len(nodes),
        "edge_count": undirected_edges,
        "symmetric": symmetric,
        "diagonal_zero": diagonal_zero,
    }
    (RESULTS / "doc37_iteration1_validation.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    return result


def main() -> None:
    for round_info in ROUNDS:
        write_edges(round_info)
        write_matrix(round_info)
    write_notes()
    write_token_report()
    validation = validate_final()
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
