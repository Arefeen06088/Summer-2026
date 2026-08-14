import csv
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


COMPONENTS = """
US-345A
CB-UAT-A
TR-UAT-1
CB-IN-A
BUS-480-RB1
EDG-1A
CB-DG-A
US-230B
CB-SAT-B
TR-SAT-2
CB-IN-B
BUS-480-RB2
EDG-1B
CB-DG-B
CB-TIE-480
CB-F101
OL-F101
PMP-SI-1A
CB-F102
OL-F102
PMP-RHR-1A
CB-F103
OL-F103
FAN-CTMT-1A
CB-F104
OL-F104
MOV-RC-104
CB-F105
OL-F105
PMP-CCW-1A
CB-F106
OL-F106
MOV-TA-106
CB-F107
OL-F107
FAN-AHU-1A
CB-F108
OL-F108
PMP-CS-1A
CB-F109
OL-F109
MOV-EF-109
CB-F110
OL-F110
HTR-PZR-1
CB-F111
OL-F111
PMP-SI-1B
CB-F112
OL-F112
PMP-RHR-1B
CB-F113
OL-F113
FAN-CTMT-1B
CB-F114
OL-F114
MOV-RC-114
CB-F115
OL-F115
PNL-SPARE-F15
CB-LC-A
TR-LC-A
GND-NG-A
CB-LC-A2
BUS-480-LCA
CB-LC-TIE
CB-A201
OL-201
PMP-SW-2A
CB-A202
OL-202
PMP-CVC-2A
CB-A203
OL-203
MOV-SI-203
CB-A204
OL-204
FAN-CR-2A
CB-A205
OL-205
HTR-BATT-A
CB-CHG-A
CHG-125A
BAT-125A
BUS-125DCA
INV-120A
BUS-UPS-A
RPS-TRAIN-A
ESFAS-TRAIN-A
RELAY-K701
TB-ESF-A
ANN-CP-A
CB-CHG-B
CHG-125B
BAT-125B
BUS-125DCB
INV-120B
BUS-UPS-B
RPS-TRAIN-B
ESFAS-TRAIN-B
RELAY-K702
TB-ESF-B
REC-SER-01
CB-LC-B
TR-LC-B
GND-NG-B
CB-LC-B2
BUS-480-LCB
CB-B206
OL-206
PMP-SW-2B
CB-B207
OL-207
PMP-CVC-2B
CB-B208
OL-208
MOV-SI-208
CB-B209
OL-209
PNL-LTG-209
""".strip().splitlines()


ASSERTED_EDGE_TEXT = """
US-345A,CB-UAT-A,solid_power
CB-UAT-A,TR-UAT-1,solid_power
TR-UAT-1,CB-IN-A,solid_power
CB-IN-A,BUS-480-RB1,solid_power
EDG-1A,CB-DG-A,solid_power
CB-DG-A,BUS-480-RB1,solid_power
US-230B,CB-SAT-B,solid_power
CB-SAT-B,TR-SAT-2,solid_power
TR-SAT-2,CB-IN-B,solid_power
CB-IN-B,BUS-480-RB2,solid_power
EDG-1B,CB-DG-B,solid_power
CB-DG-B,BUS-480-RB2,solid_power
BUS-480-RB1,CB-TIE-480,tie
CB-TIE-480,BUS-480-RB2,tie
BUS-480-RB1,CB-F101,solid_power
CB-F101,OL-F101,solid_power
OL-F101,PMP-SI-1A,solid_power
BUS-480-RB1,CB-F103,solid_power
CB-F103,OL-F103,solid_power
OL-F103,FAN-CTMT-1A,solid_power
BUS-480-RB1,CB-F105,solid_power
CB-F105,OL-F105,solid_power
OL-F105,PMP-CCW-1A,solid_power
BUS-480-RB1,CB-F107,solid_power
CB-F107,OL-F107,solid_power
OL-F107,FAN-AHU-1A,solid_power
BUS-480-RB1,CB-F109,solid_power
CB-F109,OL-F109,solid_power
OL-F109,MOV-EF-109,solid_power
BUS-480-RB1,CB-F111,solid_power
CB-F111,OL-F111,solid_power
OL-F111,PMP-SI-1B,solid_power
BUS-480-RB1,CB-F113,solid_power
CB-F113,OL-F113,solid_power
OL-F113,FAN-CTMT-1B,solid_power
BUS-480-RB1,CB-F115,solid_power
CB-F115,OL-F115,solid_power
OL-F115,PNL-SPARE-F15,solid_power
BUS-480-RB2,CB-F102,solid_power
CB-F102,OL-F102,solid_power
OL-F102,PMP-RHR-1A,solid_power
BUS-480-RB2,CB-F104,solid_power
CB-F104,OL-F104,solid_power
OL-F104,MOV-RC-104,solid_power
BUS-480-RB2,CB-F106,solid_power
CB-F106,OL-F106,solid_power
OL-F106,MOV-TA-106,solid_power
BUS-480-RB2,CB-F108,solid_power
CB-F108,OL-F108,solid_power
OL-F108,PMP-CS-1A,solid_power
BUS-480-RB2,CB-F110,solid_power
CB-F110,OL-F110,solid_power
OL-F110,HTR-PZR-1,solid_power
BUS-480-RB2,CB-F112,solid_power
CB-F112,OL-F112,solid_power
OL-F112,PMP-RHR-1B,solid_power
BUS-480-RB2,CB-F114,solid_power
CB-F114,OL-F114,solid_power
OL-F114,MOV-RC-114,solid_power
BUS-480-RB1,CB-LC-A,solid_power
CB-LC-A,TR-LC-A,solid_power
TR-LC-A,CB-LC-A2,solid_power
CB-LC-A2,BUS-480-LCA,solid_power
TR-LC-A,GND-NG-A,ground_reference
BUS-480-RB2,CB-LC-B,solid_power
CB-LC-B,TR-LC-B,solid_power
TR-LC-B,CB-LC-B2,solid_power
CB-LC-B2,BUS-480-LCB,solid_power
TR-LC-B,GND-NG-B,ground_reference
BUS-480-LCA,CB-LC-TIE,tie
CB-LC-TIE,BUS-480-LCB,tie
BUS-480-LCA,CB-A201,solid_power
CB-A201,OL-201,solid_power
OL-201,PMP-SW-2A,solid_power
BUS-480-LCA,CB-A202,solid_power
CB-A202,OL-202,solid_power
OL-202,PMP-CVC-2A,solid_power
BUS-480-LCA,CB-A203,solid_power
CB-A203,OL-203,solid_power
OL-203,MOV-SI-203,solid_power
BUS-480-LCA,CB-A204,solid_power
CB-A204,OL-204,solid_power
OL-204,FAN-CR-2A,solid_power
BUS-480-LCA,CB-A205,solid_power
CB-A205,OL-205,solid_power
OL-205,HTR-BATT-A,solid_power
BUS-480-LCB,CB-B206,solid_power
CB-B206,OL-206,solid_power
OL-206,PMP-SW-2B,solid_power
BUS-480-LCB,CB-B207,solid_power
CB-B207,OL-207,solid_power
OL-207,PMP-CVC-2B,solid_power
BUS-480-LCB,CB-B208,solid_power
CB-B208,OL-208,solid_power
OL-208,MOV-SI-208,solid_power
BUS-480-LCB,CB-B209,solid_power
CB-B209,OL-209,solid_power
OL-209,PNL-LTG-209,solid_power
BUS-480-LCB,CB-CHG-A,solid_power
CB-CHG-A,CHG-125A,solid_power
CHG-125A,BUS-125DCA,dc_power
BAT-125A,BUS-125DCA,dc_power
BUS-125DCA,INV-120A,dc_power
INV-120A,BUS-UPS-A,ups_power
BUS-UPS-A,RPS-TRAIN-A,ups_power
BUS-UPS-A,ESFAS-TRAIN-A,ups_power
RPS-TRAIN-A,RELAY-K701,dashed_control
ESFAS-TRAIN-A,RELAY-K701,dashed_control
RELAY-K701,TB-ESF-A,dashed_control
ANN-CP-A,TB-ESF-A,dashed_control
ANN-CP-A,REC-SER-01,dashed_control
BUS-480-LCB,CB-CHG-B,solid_power
CB-CHG-B,CHG-125B,solid_power
CHG-125B,BUS-125DCB,dc_power
BAT-125B,BUS-125DCB,dc_power
BUS-125DCB,INV-120B,dc_power
INV-120B,BUS-UPS-B,ups_power
BUS-UPS-B,RPS-TRAIN-B,ups_power
BUS-UPS-B,ESFAS-TRAIN-B,ups_power
RPS-TRAIN-B,RELAY-K702,dashed_control
ESFAS-TRAIN-B,RELAY-K702,dashed_control
RELAY-K702,TB-ESF-B,dashed_control
REC-SER-01,TB-ESF-B,dashed_control
""".strip().splitlines()


UNCERTAIN_DIEGO_ROUND1 = [
    ("ANN-CP-A", "REC-SER-01", "dashed_control", "uncertain_plausible"),
    ("ANN-CP-A", "BUS-UPS-B", "dashed_control", "uncertain_plausible"),
    ("REC-SER-01", "BUS-UPS-B", "dashed_control", "uncertain_plausible"),
    ("TB-ESF-A", "TB-ESF-B", "dashed_control", "uncertain_plausible"),
    ("RELAY-K701", "CB-LC-B", "dashed_control", "uncertain_plausible"),
    ("RELAY-K702", "CB-LC-B2", "dashed_control", "uncertain_plausible"),
]

EXCLUDED_AFTER_REVIEW = [
    ("ANN-CP-A", "BUS-UPS-B", "dashed_control", "excluded"),
    ("REC-SER-01", "BUS-UPS-B", "dashed_control", "excluded"),
    ("TB-ESF-A", "TB-ESF-B", "dashed_control", "excluded"),
    ("RELAY-K701", "CB-LC-B", "dashed_control", "excluded"),
    ("RELAY-K702", "CB-LC-B2", "dashed_control", "excluded"),
]


def parse_asserted_edges(include_ann_rec: bool):
    rows = []
    for line in ASSERTED_EDGE_TEXT:
        a, b, edge_type = line.split(",")
        if not include_ann_rec and {a, b} == {"ANN-CP-A", "REC-SER-01"}:
            continue
        rows.append((a, b, edge_type, "asserted"))
    return rows


def write_edges(path: Path, edges):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["a", "b", "type", "status"])
        writer.writerows(edges)


def write_matrix(path: Path, components, edges):
    index = {name: i for i, name in enumerate(components)}
    if len(index) != len(components):
        raise ValueError("Duplicate component names")
    matrix = [[0 for _ in components] for _ in components]
    for a, b, _edge_type, status in edges:
        if status == "excluded":
            continue
        if a not in index or b not in index:
            raise ValueError(f"Missing component in edge: {a}, {b}")
        i, j = index[a], index[b]
        if i != j:
            matrix[i][j] = 1
            matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component", *components])
        for name, row in zip(components, matrix):
            writer.writerow([name, *row])


def count_matrix_edges(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return sum(sum(int(x) for x in row[1:]) for row in rows[1:]) // 2


def validate_round(name, components, edges, expected_edges):
    node_set = set(components)
    if len(node_set) != len(components):
        raise ValueError(f"{name}: duplicate components")
    pairs = set()
    for a, b, _edge_type, status in edges:
        if a not in node_set or b not in node_set:
            raise ValueError(f"{name}: edge references unknown node: {a}, {b}")
        if status != "excluded" and a != b:
            pairs.add(frozenset((a, b)))
    if len(pairs) != expected_edges:
        raise ValueError(f"{name}: expected {expected_edges} matrix edges, got {len(pairs)}")


def write_summary():
    text = """# Connectivity Extraction Summary

Document: 4 / Raw + components

Allowed visual inputs:
- raw.png
- detected_components_and_logical_overlay.png
- generated crops in codes/visual_aids, derived only from the two allowed images

Round sequence:
1. Diego round 1: high-recall extraction. Proposed 120 components, 122 asserted edges, and 6 uncertain/plausible dashed-control candidates.
2. Jennifer round 1: precision refinement. Kept the 120-component set, retained Diego's asserted edges, added ANN-CP-A--REC-SER-01, and excluded the other 5 dashed candidates as crossings/routing without visible component termination.
3. Diego round 2: agreed with Jennifer round 1; final round-2 set is 120 components and 123 asserted edges.
4. Jennifer round 2: saturated=true.

Final component count: 120
Final undirected edge count: 123

Important modeling decisions:
- BUS-480-RB1 and BUS-480-RB2 are separate bus nodes connected only through CB-TIE-480.
- BUS-480-LCA and BUS-480-LCB are separate load-center buses connected through CB-LC-TIE.
- CB-LC-TIE and CB-TIE-480 are included as physical tie connections even though the symbols show normally open breakers.
- TR-LC-A--GND-NG-A and TR-LC-B--GND-NG-B are included as ground-reference edges.
- CB-CHG-A and CB-CHG-B are supplied from BUS-480-LCB.
- ANN-CP-A--REC-SER-01 is included as the only cross-panel dashed-control edge added during precision review.
- Dashed crossings near BUS-UPS-B, TB-ESF-A/B, CB-LC-B, and CB-LC-B2 are not included without terminal evidence.
"""
    (RESULTS / "round_summaries.md").write_text(text, encoding="utf-8")


def write_token_usage():
    rows = [
        {
            "document": "4",
            "iteration": "1",
            "call_id": "main_coordinator_aggregate",
            "model": "GPT-5/Codex main",
            "input_tokens_est_low": 16000,
            "input_tokens_est_expected": 24500,
            "input_tokens_est_high": 36000,
            "cached_input_tokens": "unknown",
            "output_tokens_est_low": 1800,
            "output_tokens_est_expected": 3200,
            "output_tokens_est_high": 5200,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est_expected": 19000,
            "usage_object_available": "no",
            "notes": "Main inspected raw, overlay, many derived crops, and integrated four subagent round outputs. No API key available for official token counting.",
        },
        {
            "document": "4",
            "iteration": "1",
            "call_id": "diego_round1",
            "model": "gpt-5.5",
            "input_tokens_est_low": 22000,
            "input_tokens_est_expected": 33000,
            "input_tokens_est_high": 47000,
            "cached_input_tokens": "unknown",
            "output_tokens_est_low": 3000,
            "output_tokens_est_expected": 5200,
            "output_tokens_est_high": 7800,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est_expected": 26500,
            "usage_object_available": "no",
            "notes": "High-recall extraction using full raw/overlay and broad crop set.",
        },
        {
            "document": "4",
            "iteration": "1",
            "call_id": "jennifer_round1",
            "model": "gpt-5.5",
            "input_tokens_est_low": 20000,
            "input_tokens_est_expected": 30500,
            "input_tokens_est_high": 44000,
            "cached_input_tokens": "unknown",
            "output_tokens_est_low": 1000,
            "output_tokens_est_expected": 1800,
            "output_tokens_est_high": 3000,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est_expected": 23000,
            "usage_object_available": "no",
            "notes": "Precision review of Diego round 1 and focused crops.",
        },
        {
            "document": "4",
            "iteration": "1",
            "call_id": "diego_round2",
            "model": "gpt-5.5",
            "input_tokens_est_low": 8500,
            "input_tokens_est_expected": 13000,
            "input_tokens_est_high": 19000,
            "cached_input_tokens": "unknown",
            "output_tokens_est_low": 250,
            "output_tokens_est_expected": 650,
            "output_tokens_est_high": 1200,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est_expected": 8500,
            "usage_object_available": "no",
            "notes": "Focused saturation check on dashed-control disputed edges.",
        },
        {
            "document": "4",
            "iteration": "1",
            "call_id": "jennifer_round2_final",
            "model": "gpt-5.5",
            "input_tokens_est_low": 3500,
            "input_tokens_est_expected": 6000,
            "input_tokens_est_high": 9500,
            "cached_input_tokens": "unknown",
            "output_tokens_est_low": 150,
            "output_tokens_est_expected": 350,
            "output_tokens_est_high": 800,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est_expected": 3000,
            "usage_object_available": "no",
            "notes": "Final saturation confirmation using focused crops.",
        },
    ]
    total_input_expected = sum(int(r["input_tokens_est_expected"]) for r in rows)
    total_output_expected = sum(int(r["output_tokens_est_expected"]) for r in rows)
    rows.append({
        "document": "4",
        "iteration": "1",
        "call_id": "TOTAL_ESTIMATE",
        "model": "",
        "input_tokens_est_low": sum(int(r["input_tokens_est_low"]) for r in rows),
        "input_tokens_est_expected": total_input_expected,
        "input_tokens_est_high": sum(int(r["input_tokens_est_high"]) for r in rows),
        "cached_input_tokens": "unknown",
        "output_tokens_est_low": sum(int(r["output_tokens_est_low"]) for r in rows),
        "output_tokens_est_expected": total_output_expected,
        "output_tokens_est_high": sum(int(r["output_tokens_est_high"]) for r in rows),
        "reasoning_tokens": "not exposed",
        "image_file_input_tokens_est_expected": sum(int(r["image_file_input_tokens_est_expected"]) for r in rows),
        "usage_object_available": "no",
        "notes": f"Expected total input+output tokens estimate: {total_input_expected + total_output_expected}. Official Responses token counting not called because OPENAI_API_KEY_PRESENT=false.",
    })
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    diego_round1_edges = parse_asserted_edges(include_ann_rec=False) + UNCERTAIN_DIEGO_ROUND1
    jennifer_round1_edges = parse_asserted_edges(include_ann_rec=True) + EXCLUDED_AFTER_REVIEW
    diego_round2_edges = parse_asserted_edges(include_ann_rec=True) + EXCLUDED_AFTER_REVIEW
    jennifer_round2_edges = parse_asserted_edges(include_ann_rec=True) + EXCLUDED_AFTER_REVIEW
    final_edges = parse_asserted_edges(include_ann_rec=True)

    rounds = [
        ("diego_round1", COMPONENTS, diego_round1_edges, 128),
        ("jennifer_round1", COMPONENTS, jennifer_round1_edges, 123),
        ("diego_round2", COMPONENTS, diego_round2_edges, 123),
        ("jennifer_round2_final", COMPONENTS, jennifer_round2_edges, 123),
        ("final", COMPONENTS, final_edges, 123),
    ]
    for name, components, edges, expected_edges in rounds:
        validate_round(name, components, edges, expected_edges)
        matrix_name = "final_connectivity_matrix.csv" if name == "final" else f"{name}_matrix.csv"
        edge_name = "final_edges.csv" if name == "final" else f"{name}_edges.csv"
        write_edges(RESULTS / edge_name, edges)
        write_matrix(RESULTS / matrix_name, components, edges)
        counted = count_matrix_edges(RESULTS / matrix_name)
        if counted != expected_edges:
            raise ValueError(f"{name}: matrix has {counted} edges; expected {expected_edges}")

    write_summary()
    write_token_usage()
    print("Wrote connectivity artifacts to", RESULTS)
    print("Final components:", len(COMPONENTS))
    print("Final undirected edges:", len({frozenset(edge[:2]) for edge in final_edges}))


if __name__ == "__main__":
    main()
