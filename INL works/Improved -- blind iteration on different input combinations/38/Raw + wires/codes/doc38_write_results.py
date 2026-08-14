import csv
import json
from pathlib import Path


DOC = "38"
ITERATION = "1"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires")
RESULTS = BASE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


DIEGO_R1_NODES = [
    "GEN-U2A", "CB-101", "TR-UAT-2A", "DG-2A", "CB-103", "BUS-4160A", "CB-105",
    "BUS-4160B", "TR-SUT-2B", "CB-102", "DG-2B", "CB-104", "CB-201A", "TR-201A",
    "CB-301A", "BUS-480A", "CB-401A", "MCC-2A1", "PUMP-RHR2A", "PUMP-CCW2A",
    "PUMP-SW2A", "FAN-CR2A", "MOV-RHR141A", "MOV-SI221A", "TR-CPT-A", "CHGR-2A",
    "BAT-125A_S-125DC-A", "125VDC-TRAIN-A", "INV-2A", "BUS-120AC-A", "RELAY-86A",
    "RELAY-27A", "RPS-PNL-A", "CB-201B", "TR-201B", "CB-301B", "BUS-480B",
    "CB-401B", "MCC-2B1", "PUMP-RHR2B", "PUMP-CCW2B", "PUMP-SW2B", "FAN-CR2B",
    "MOV-RHR142B", "MOV-SI222B", "TR-CPT-B", "CHGR-2B", "BAT-125B_S-125DC-B",
    "125VDC-TRAIN-B", "INV-2B", "BUS-120AC-B", "RELAY-86B", "RELAY-27B", "RPS-PNL-B",
]

DIEGO_R1_EDGES = [
    ("GEN-U2A", "CB-101", "solid generator lead"),
    ("CB-101", "TR-UAT-2A", "solid breaker to transformer lead"),
    ("TR-UAT-2A", "BUS-4160A", "solid transformer secondary tap to bus"),
    ("DG-2A", "CB-103", "solid diesel generator lead"),
    ("CB-103", "BUS-4160A", "solid feeder to bus"),
    ("BUS-4160A", "CB-105", "solid left bus-tie lead"),
    ("CB-105", "BUS-4160B", "solid right bus-tie lead"),
    ("TR-SUT-2B", "CB-102", "solid startup transformer feeder"),
    ("CB-102", "BUS-4160B", "solid source feeder"),
    ("DG-2B", "CB-104", "solid diesel generator lead"),
    ("CB-104", "BUS-4160B", "solid feeder to bus"),
    ("BUS-4160A", "CB-201A", "solid feeder drop"),
    ("CB-201A", "TR-201A", "solid breaker to transformer lead"),
    ("TR-201A", "CB-301A", "solid transformer to breaker lead"),
    ("CB-301A", "BUS-480A", "solid tap to BUS-480A"),
    ("BUS-4160B", "CB-201B", "solid feeder drop"),
    ("CB-201B", "TR-201B", "solid breaker to transformer lead"),
    ("TR-201B", "CB-301B", "solid transformer to breaker lead"),
    ("CB-301B", "BUS-480B", "solid tap to BUS-480B"),
    ("BUS-480A", "CB-401A", "solid feeder drop"),
    ("CB-401A", "MCC-2A1", "solid breaker output into MCC"),
    ("BUS-480B", "CB-401B", "solid feeder drop"),
    ("CB-401B", "MCC-2B1", "solid breaker output into MCC"),
    ("MCC-2A1", "PUMP-RHR2A", "solid MCC load drop"),
    ("MCC-2A1", "PUMP-CCW2A", "solid MCC load drop"),
    ("MCC-2A1", "PUMP-SW2A", "solid MCC load drop"),
    ("MCC-2A1", "FAN-CR2A", "solid MCC load drop"),
    ("MCC-2A1", "MOV-RHR141A", "solid MCC load drop"),
    ("MCC-2A1", "MOV-SI221A", "solid MCC load drop"),
    ("MCC-2B1", "PUMP-RHR2B", "solid MCC load drop"),
    ("MCC-2B1", "PUMP-CCW2B", "solid MCC load drop"),
    ("MCC-2B1", "PUMP-SW2B", "solid MCC load drop"),
    ("MCC-2B1", "FAN-CR2B", "solid MCC load drop"),
    ("MCC-2B1", "MOV-RHR142B", "solid MCC load drop"),
    ("MCC-2B1", "MOV-SI222B", "solid MCC load drop"),
    ("BUS-480A", "TR-CPT-A", "solid 480V branch"),
    ("BUS-480A", "CHGR-2A", "solid 480V branch"),
    ("CHGR-2A", "125VDC-TRAIN-A", "solid charger output"),
    ("BAT-125A_S-125DC-A", "125VDC-TRAIN-A", "battery terminal on DC train"),
    ("125VDC-TRAIN-A", "INV-2A", "solid DC train tap"),
    ("INV-2A", "BUS-120AC-A", "solid inverter output"),
    ("BUS-120AC-A", "RPS-PNL-A", "solid AC bus drop"),
    ("TR-CPT-A", "BUS-120AC-A", "ambiguous CPT-A secondary, included by Diego R1"),
    ("125VDC-TRAIN-A", "RELAY-86A", "dashed/control path, included by Diego R1"),
    ("BUS-120AC-A", "RELAY-27A", "ambiguous UV relay A path, included by Diego R1"),
    ("RELAY-27A", "RPS-PNL-A", "dashed/control path, included by Diego R1"),
    ("BUS-480B", "TR-CPT-B", "solid 480V branch"),
    ("BUS-480B", "CHGR-2B", "solid 480V branch"),
    ("TR-CPT-B", "BUS-120AC-B", "solid CPT-B secondary to AC bus"),
    ("CHGR-2B", "125VDC-TRAIN-B", "solid charger output"),
    ("BAT-125B_S-125DC-B", "125VDC-TRAIN-B", "battery terminal on DC train"),
    ("125VDC-TRAIN-B", "INV-2B", "solid DC train tap"),
    ("INV-2B", "BUS-120AC-B", "solid inverter output"),
    ("BUS-120AC-B", "RPS-PNL-B", "solid AC bus drop"),
    ("BUS-120AC-B", "RELAY-27B", "solid UV relay B tap"),
    ("125VDC-TRAIN-B", "RELAY-86B", "dashed/control path, included by Diego R1"),
    ("RELAY-27B", "RPS-PNL-B", "dashed/control path, included by Diego R1"),
]

JENNIFER_R1_NODES = [
    "GEN-U2A", "CB-101", "TR-UAT-2A", "DG-2A", "CB-103", "BUS-4160A", "CB-105",
    "BUS-4160B", "TR-SUT-2B", "CB-102", "DG-2B", "CB-104", "CB-201A", "TR-201A",
    "CB-301A", "BUS-480A", "CB-401A", "MCC-2A1", "PUMP-RHR2A", "PUMP-CCW2A",
    "PUMP-SW2A", "FAN-CR2A", "MOV-RHR141A", "MOV-SI221A", "TR-CPT-A", "CHGR-2A",
    "BAT-125A", "125VDC-TRAIN-A", "INV-2A", "BUS-120AC-A", "RELAY-86A",
    "RELAY-27A", "RPS-PNL-A", "CB-201B", "TR-201B", "CB-301B", "BUS-480B",
    "CB-401B", "MCC-2B1", "PUMP-RHR2B", "PUMP-CCW2B", "PUMP-SW2B", "FAN-CR2B",
    "MOV-RHR142B", "MOV-SI222B", "TR-CPT-B", "CHGR-2B", "BAT-125B",
    "125VDC-TRAIN-B", "INV-2B", "BUS-120AC-B", "RELAY-86B", "RELAY-27B", "RPS-PNL-B",
]

JENNIFER_R1_EDGES = [
    ("GEN-U2A", "CB-101", "solid generator lead"),
    ("CB-101", "TR-UAT-2A", "solid breaker to transformer lead"),
    ("TR-UAT-2A", "BUS-4160A", "solid transformer secondary tap to bus"),
    ("DG-2A", "CB-103", "solid diesel generator lead"),
    ("CB-103", "BUS-4160A", "solid feeder to bus"),
    ("BUS-4160A", "CB-105", "solid left bus-tie lead"),
    ("CB-105", "BUS-4160B", "solid right bus-tie lead"),
    ("TR-SUT-2B", "CB-102", "solid startup transformer feeder"),
    ("CB-102", "BUS-4160B", "solid source feeder"),
    ("DG-2B", "CB-104", "solid diesel generator lead"),
    ("CB-104", "BUS-4160B", "solid feeder to bus"),
    ("BUS-4160A", "CB-201A", "solid feeder drop"),
    ("CB-201A", "TR-201A", "solid breaker to transformer lead"),
    ("TR-201A", "CB-301A", "solid transformer to breaker lead"),
    ("CB-301A", "BUS-480A", "solid tap to BUS-480A"),
    ("BUS-4160B", "CB-201B", "solid feeder drop"),
    ("CB-201B", "TR-201B", "solid breaker to transformer lead"),
    ("TR-201B", "CB-301B", "solid transformer to breaker lead"),
    ("CB-301B", "BUS-480B", "solid tap to BUS-480B"),
    ("BUS-480A", "CB-401A", "solid feeder drop"),
    ("CB-401A", "MCC-2A1", "solid breaker output into MCC"),
    ("BUS-480B", "CB-401B", "solid feeder drop"),
    ("CB-401B", "MCC-2B1", "solid breaker output into MCC"),
    ("MCC-2A1", "PUMP-RHR2A", "solid MCC load drop"),
    ("MCC-2A1", "PUMP-CCW2A", "solid MCC load drop"),
    ("MCC-2A1", "PUMP-SW2A", "solid MCC load drop"),
    ("MCC-2A1", "FAN-CR2A", "solid MCC load drop"),
    ("MCC-2A1", "MOV-RHR141A", "solid MCC load drop"),
    ("MCC-2A1", "MOV-SI221A", "solid MCC load drop"),
    ("MCC-2B1", "PUMP-RHR2B", "solid MCC load drop"),
    ("MCC-2B1", "PUMP-CCW2B", "solid MCC load drop"),
    ("MCC-2B1", "PUMP-SW2B", "solid MCC load drop"),
    ("MCC-2B1", "FAN-CR2B", "solid MCC load drop"),
    ("MCC-2B1", "MOV-RHR142B", "solid MCC load drop"),
    ("MCC-2B1", "MOV-SI222B", "solid MCC load drop"),
    ("BUS-480A", "TR-CPT-A", "solid 480V branch"),
    ("BUS-480A", "CHGR-2A", "solid 480V branch"),
    ("CHGR-2A", "125VDC-TRAIN-A", "solid charger output"),
    ("BAT-125A", "125VDC-TRAIN-A", "battery terminal on DC train"),
    ("125VDC-TRAIN-A", "INV-2A", "solid DC train tap"),
    ("INV-2A", "BUS-120AC-A", "solid inverter output"),
    ("BUS-120AC-A", "RPS-PNL-A", "solid AC bus drop"),
    ("BUS-480B", "TR-CPT-B", "solid 480V branch"),
    ("BUS-480B", "CHGR-2B", "solid 480V branch"),
    ("TR-CPT-B", "BUS-120AC-B", "solid CPT-B secondary to AC bus"),
    ("CHGR-2B", "125VDC-TRAIN-B", "solid charger output"),
    ("BAT-125B", "125VDC-TRAIN-B", "battery terminal on DC train"),
    ("125VDC-TRAIN-B", "INV-2B", "solid DC train tap"),
    ("INV-2B", "BUS-120AC-B", "solid inverter output"),
    ("BUS-120AC-B", "RPS-PNL-B", "solid AC bus drop"),
    ("BUS-120AC-B", "RELAY-27B", "solid UV relay B tap"),
]

DIEGO_R2_NODES = [
    "GEN-U2A", "CB-101", "TR-UAT-2A", "DG-2A", "CB-103", "BUS-4160A", "CB-105",
    "CB-201A", "TR-201A", "CB-301A", "BUS-480A", "CB-401A", "MCC-2A1",
    "PUMP-RHR2A", "PUMP-CCW2A", "PUMP-SW2A", "FAN-CR2A", "MOV-RHR141A",
    "MOV-SI221A", "TR-CPT-A", "CHGR-2A", "BAT-125A", "125VDC-TRAIN-A", "INV-2A",
    "BUS-120AC-A", "RPS-PNL-A", "TR-SUT-2B", "CB-102", "DG-2B", "CB-104",
    "BUS-4160B", "CB-201B", "TR-201B", "CB-301B", "BUS-480B", "CB-401B",
    "MCC-2B1", "PUMP-RHR2B", "PUMP-CCW2B", "PUMP-SW2B", "FAN-CR2B",
    "MOV-RHR142B", "MOV-SI222B", "TR-CPT-B", "CHGR-2B", "BAT-125B",
    "125VDC-TRAIN-B", "INV-2B", "BUS-120AC-B", "RPS-PNL-B", "RELAY-27B",
]

DIEGO_R2_EDGES = JENNIFER_R1_EDGES

JENNIFER_R2_NODES = [
    "GEN-U2A", "CB-101", "TR-UAT-2A", "DG-2A", "CB-103", "BUS-4160A", "CB-105",
    "TR-SUT-2B", "CB-102", "DG-2B", "CB-104", "BUS-4160B", "CB-201A", "TR-201A",
    "CB-301A", "BUS-480A", "CB-201B", "TR-201B", "CB-301B", "BUS-480B",
    "CB-401A", "MCC-2A1", "PUMP-RHR2A", "PUMP-CCW2A", "PUMP-SW2A", "FAN-CR2A",
    "MOV-RHR141A", "MOV-SI221A", "TR-CPT-A", "CHGR-2A", "BAT-125A",
    "125VDC-TRAIN-A", "INV-2A", "BUS-120AC-A", "RPS-PNL-A", "RELAY-86A",
    "RELAY-27A", "CB-401B", "MCC-2B1", "PUMP-RHR2B", "PUMP-CCW2B",
    "PUMP-SW2B", "FAN-CR2B", "MOV-RHR142B", "MOV-SI222B", "TR-CPT-B",
    "CHGR-2B", "BAT-125B", "125VDC-TRAIN-B", "INV-2B", "BUS-120AC-B",
    "RPS-PNL-B", "RELAY-86B", "RELAY-27B",
]
JENNIFER_R2_EDGES = JENNIFER_R1_EDGES


def edge_set(edges):
    return {tuple(sorted((a, b))) for a, b, _ in edges}


def write_edges(path, nodes, edges, reviewer, round_name, notes=None):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["document", "iteration", "round", "reviewer", "source", "target", "evidence"])
        for a, b, evidence in edges:
            writer.writerow([DOC, ITERATION, round_name, reviewer, a, b, evidence])
    if notes:
        note_path = path.with_suffix(".notes.json")
        note_path.write_text(json.dumps(notes, indent=2), encoding="utf-8")


def write_matrix(path, nodes, edges):
    idx = {node: i for i, node in enumerate(nodes)}
    missing = sorted({x for edge in edges for x in edge[:2] if x not in idx})
    if missing:
        raise ValueError(f"{path.name}: edge nodes missing from node order: {missing}")
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b, _ in edges:
        if a == b:
            continue
        i, j = idx[a], idx[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])
    return matrix


def validate_matrix(nodes, matrix):
    diag_zero = all(matrix[i][i] == 0 for i in range(len(nodes)))
    symmetric = all(matrix[i][j] == matrix[j][i] for i in range(len(nodes)) for j in range(len(nodes)))
    edge_count = sum(sum(row) for row in matrix) // 2
    return {"nodes": len(nodes), "edges": edge_count, "symmetric": symmetric, "diagonal_zero": diag_zero}


def token_usage_rows(final_nodes, final_edges):
    # Offline estimates: text counted with tiktoken when available; image tokens approximated from
    # high-detail tiled image inputs (85 base + 170 per 512px tile after fit to 2048 max side).
    return [
        {
            "document": DOC,
            "iteration": ITERATION,
            "model_call": "main_orchestration_doc38",
            "role": "main agent",
            "model": "GPT-5 Codex session",
            "input_tokens_est": 6500,
            "cached_input_tokens_est": 0,
            "output_tokens_est_low": 900,
            "output_tokens_est_expected": 1600,
            "output_tokens_est_high": 2600,
            "reasoning_tokens": "not available",
            "image_file_input_tokens_est": 0,
            "total_tokens_expected_est": 8100,
            "usage_object_available": "no",
            "notes": "Main agent model usage is not exposed in this environment.",
        },
        {
            "document": DOC,
            "iteration": ITERATION,
            "model_call": "Diego_R1_high_recall_extraction",
            "role": "Diego",
            "model": "gpt-5.5",
            "input_tokens_est": 2400,
            "cached_input_tokens_est": 0,
            "output_tokens_est_low": 5000,
            "output_tokens_est_expected": 6800,
            "output_tokens_est_high": 9000,
            "reasoning_tokens": "not available",
            "image_file_input_tokens_est": 85170,
            "total_tokens_expected_est": 94370,
            "usage_object_available": "no",
            "notes": "13 images attached; exact Responses token counter unavailable without API key.",
        },
        {
            "document": DOC,
            "iteration": ITERATION,
            "model_call": "Jennifer_R1_precision_review",
            "role": "Jennifer",
            "model": "gpt-5.5",
            "input_tokens_est": 3600,
            "cached_input_tokens_est": 0,
            "output_tokens_est_low": 4500,
            "output_tokens_est_expected": 6200,
            "output_tokens_est_high": 8500,
            "reasoning_tokens": "not available",
            "image_file_input_tokens_est": 85255,
            "total_tokens_expected_est": 95055,
            "usage_object_available": "no",
            "notes": "13 images attached; included Diego R1 summary.",
        },
        {
            "document": DOC,
            "iteration": ITERATION,
            "model_call": "Diego_R2_reconciliation",
            "role": "Diego",
            "model": "gpt-5.5",
            "input_tokens_est": 2700,
            "cached_input_tokens_est": 0,
            "output_tokens_est_low": 1700,
            "output_tokens_est_expected": 2600,
            "output_tokens_est_high": 3900,
            "reasoning_tokens": "not available",
            "image_file_input_tokens_est": 65535,
            "total_tokens_expected_est": 70835,
            "usage_object_available": "no",
            "notes": "10 images attached; focused reconciliation.",
        },
        {
            "document": DOC,
            "iteration": ITERATION,
            "model_call": "Jennifer_R2_final_confirmation",
            "role": "Jennifer",
            "model": "gpt-5.5",
            "input_tokens_est": 2300,
            "cached_input_tokens_est": 0,
            "output_tokens_est_low": 900,
            "output_tokens_est_expected": 1500,
            "output_tokens_est_high": 2600,
            "reasoning_tokens": "not available",
            "image_file_input_tokens_est": 37740,
            "total_tokens_expected_est": 41540,
            "usage_object_available": "no",
            "notes": "6 images attached; final node-policy confirmation.",
        },
    ]


def write_token_usage(rows):
    csv_path = RESULTS / "doc38_iteration1_token_usage_estimate.csv"
    keys = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
    total_expected = sum(int(row["total_tokens_expected_est"]) for row in rows)
    low = sum(int(row["input_tokens_est"]) + int(row["image_file_input_tokens_est"]) + int(row["output_tokens_est_low"]) for row in rows)
    high = sum(int(row["input_tokens_est"]) + int(row["image_file_input_tokens_est"]) + int(row["output_tokens_est_high"]) for row in rows)
    md = [
        "# Token Usage Estimate - Document 38 Iteration 1",
        "",
        "Exact OpenAI usage objects and the Responses input-token counting endpoint were not available in this environment because no API key was provided/exposed.",
        "Text estimates use local token-count approximation; image/file estimates use a documented high-detail image tiling approximation (85 base tokens plus 170 tokens per 512 px tile after max-side scaling).",
        "",
        "| Document | Iteration | Call | Role | Input | Image/File | Output Low | Output Expected | Output High | Expected Total |",
        "|---|---:|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        md.append(
            f"| {row['document']} | {row['iteration']} | {row['model_call']} | {row['role']} | "
            f"{row['input_tokens_est']} | {row['image_file_input_tokens_est']} | "
            f"{row['output_tokens_est_low']} | {row['output_tokens_est_expected']} | "
            f"{row['output_tokens_est_high']} | {row['total_tokens_expected_est']} |"
        )
    md.extend([
        "",
        f"Expected total estimate: {total_expected}",
        f"Low total estimate: {low}",
        f"High total estimate: {high}",
    ])
    (RESULTS / "doc38_iteration1_token_usage_estimate.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def write_round_log(final_nodes, final_edges, validation):
    text = f"""# Document 38 Iteration 1 Round Log

Resource folder: `{BASE}`

Ground-truth policy: no GT or GT-derived files used. Only Raw + wires images and generated crops from that folder were inspected.

Rounds:
1. Diego R1 high-recall extraction: proposed 54 nodes and included dashed/control ambiguous edges in the draft matrix.
2. Jennifer R1 precision review: normalized batteries to `BAT-125A/B`, removed dashed/control/ground edges, excluded `TR-CPT-A--BUS-120AC-A`, kept `BUS-120AC-B--RELAY-27B`.
3. Diego R2 reconciliation: agreed with Jennifer R1 and reported consensus, while omitting isolated relay nodes from his proposed final node list.
4. Jennifer R2 final confirmation: final node policy applied in generated final files.

Final validation:
- Nodes: {validation['nodes']}
- Edges: {validation['edges']}
- Symmetric: {validation['symmetric']}
- Diagonal zero: {validation['diagonal_zero']}

Final excluded/uncertain:
- Dashed control/routing/ground paths are excluded.
- `TR-CPT-A--BUS-120AC-A` excluded due visible gap/terminal dot rather than solid tie.
- `125VDC-TRAIN-A/B--RELAY-86A/B`, `BUS-120AC-A--RELAY-27A`, and relay-to-RPS dashed paths excluded.
- Direct bus collapses (`BUS-4160A--BUS-4160B`, `BUS-480A--BUS-480B`) excluded.
- `S-125DC-A/B` treated as equipment text associated with `BAT-125A/B`, not separate nodes.
"""
    (RESULTS / "doc38_iteration1_round_log.md").write_text(text, encoding="utf-8")


def run():
    final_nodes = JENNIFER_R2_NODES or DIEGO_R2_NODES
    final_edges = JENNIFER_R2_EDGES or DIEGO_R2_EDGES
    rounds = [
        ("doc38_iteration1_diego_r1", "Diego", "round1", DIEGO_R1_NODES, DIEGO_R1_EDGES),
        ("doc38_iteration1_jennifer_r1", "Jennifer", "round1", JENNIFER_R1_NODES, JENNIFER_R1_EDGES),
        ("doc38_iteration1_diego_r2", "Diego", "round2", DIEGO_R2_NODES, DIEGO_R2_EDGES),
        ("doc38_iteration1_jennifer_r2", "Jennifer", "round2", final_nodes, final_edges),
    ]
    validations = {}
    for stem, reviewer, round_name, nodes, edges in rounds:
        write_edges(RESULTS / f"{stem}_edges.csv", nodes, edges, reviewer, round_name)
        matrix = write_matrix(RESULTS / f"{stem}_matrix.csv", nodes, edges)
        validations[stem] = validate_matrix(nodes, matrix)

    write_edges(RESULTS / "connectivity_edges_final.csv", final_nodes, final_edges, "Jennifer", "final")
    final_matrix = write_matrix(RESULTS / "connectivity_matrix_final.csv", final_nodes, final_edges)
    final_validation = validate_matrix(final_nodes, final_matrix)
    validations["connectivity_matrix_final"] = final_validation

    consensus = {
        "document": DOC,
        "iteration": ITERATION,
        "final_nodes": final_nodes,
        "final_edges": [{"source": a, "target": b, "evidence": e} for a, b, e in final_edges],
        "consensus": "Diego R2 agreed with Jennifer R1 edge set; Jennifer R2 kept visible isolated relays as all-zero nodes.",
        "excluded_edges": [
            "TR-CPT-A--BUS-120AC-A",
            "125VDC-TRAIN-A--RELAY-86A",
            "125VDC-TRAIN-B--RELAY-86B",
            "BUS-120AC-A--RELAY-27A",
            "RELAY-27A--RPS-PNL-A",
            "RELAY-27B--RPS-PNL-B",
            "BUS-4160A--BUS-4160B direct collapse",
            "BUS-480A--BUS-480B reserved/no connection",
            "GND-STA control/ground reference",
            "S-125DC-A/B as separate nodes",
        ],
        "validations": validations,
    }
    (RESULTS / "doc38_iteration1_consensus_notes.json").write_text(json.dumps(consensus, indent=2), encoding="utf-8")
    (RESULTS / "doc38_iteration1_validation.json").write_text(json.dumps(validations, indent=2), encoding="utf-8")
    write_round_log(final_nodes, final_edges, final_validation)
    write_token_usage(token_usage_rows(final_nodes, final_edges))
    print(json.dumps(final_validation, indent=2))


if __name__ == "__main__":
    run()
