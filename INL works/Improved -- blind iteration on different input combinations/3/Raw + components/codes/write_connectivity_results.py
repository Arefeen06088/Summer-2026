import csv
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


FINAL_COMPONENTS = """
GRID-1
AUX-TR-1A
CB-101
BUS-416A
BUS-TIE-41
BUS-416B
CB-102
AUX-TR-1B
GRID-2
EDG-1A
CB-DG1A
TR-480A1
CB-480A1
MCC-480A1
TR-480A2
CB-480A2
MCC-480A2
GND-1E
CB-CHG-A
CHGR-125A
BAT-125A
DC-BUS-A
INV-120A
BUS-120A
CB-CHG-B
CHGR-125B
BAT-125B
DC-BUS-B
INV-120B
BUS-120B
TR-480B1
CB-480B1
MCC-480B1
TR-480B2
CB-480B2
MCC-480B2
CB-DG1B
EDG-1B
FDB-A1
CB-SI-A1
PUMP-SI-A1
CB-RHR-A1
PUMP-RHR-A1
CB-CCW-A1
PUMP-CCW-A1
CB-FAN-A1
FAN-CR-A1
CB-MOV-A101
VALVE-SI-A101
CB-MOV-A102
VALVE-RHR-A102
FDB-A2
CB-CS-A2
PUMP-CS-A2
CB-SW-A2
PUMP-SW-A2
CB-AFW-A2
PUMP-AFW-A2
CB-FAN-A2
FAN-EB-A2
CB-MOV-A201
VALVE-CCW-A201
CB-HTR-A2
HTR-BAY-A2
FDB-B1
CB-SI-B1
PUMP-SI-B1
CB-RHR-B1
PUMP-RHR-B1
CB-CCW-B1
PUMP-CCW-B1
CB-FAN-B1
FAN-CR-B1
CB-MOV-B101
VALVE-SI-B101
CB-MOV-B102
VALVE-RHR-B102
FDB-B2
CB-CS-B2
PUMP-CS-B2
CB-SW-B2
PUMP-SW-B2
CB-FAN-B2
FAN-EB-B2
CB-MOV-B201
VALVE-CCW-B201
CB-HTR-B2
HTR-BAY-B2
INST-PT-A
INST-LT-A
RELAY-K27A
PANEL-RPS-A
PANEL-ESF-A
JB-A401
PANEL-RPS-B
PANEL-ESF-B
JB-B501
RELAY-K27B
INST-PT-B
INST-LT-B
""".strip().splitlines()


DIEGO_ROUND1_COMPONENTS = """
GRID-1
AUX-TR-1A
CB-101
BUS-416A
BUS-TIE-41
BUS-416B
CB-102
AUX-TR-1B
GRID-2
EDG-1A
CB-DG1A
TR-480A1
CB-480A1
MCC-480A1
TR-480A2
CB-480A2
MCC-480A2
GND-A
GND-1E
GND-B
CB-CHG-A
CHGR-125A
BAT-125A
DC-BUS-A
INV-120A
BUS-120A
CB-CHG-B
CHGR-125B
BAT-125B
DC-BUS-B
INV-120B
BUS-120B
TR-480B1
CB-480B1
MCC-480B1
TR-480B2
CB-480B2
MCC-480B2
CB-DG1B
EDG-1B
FDB-A1
CB-SI-A1
PUMP-SI-A1
CB-RHR-A1
PUMP-RHR-A1
CB-CCW-A1
PUMP-CCW-A1
CB-FAN-A1
FAN-CR-A1
CB-MOV-A101
VALVE-SI-A101
CB-MOV-A102
VALVE-RHR-A102
FDB-A2
CB-CS-A2
PUMP-CS-A2
CB-SW-A2
PUMP-SW-A2
CB-AFW-A2
PUMP-AFW-A2
CB-FAN-A2
FAN-EB-A2
CB-MOV-A201
VALVE-CCW-A201
CB-HTR-A2
HTR-BAY-A2
FDB-B1
CB-SI-B1
PUMP-SI-B1
CB-RHR-B1
PUMP-RHR-B1
CB-CCW-B1
PUMP-CCW-B1
CB-FAN-B1
FAN-CR-B1
CB-MOV-B101
VALVE-SI-B101
CB-MOV-B102
VALVE-RHR-B102
FDB-B2
CB-CS-B2
PUMP-CS-B2
CB-SW-B2
PUMP-SW-B2
CB-FAN-B2
FAN-EB-B2
CB-MOV-B201
VALVE-CCW-B201
CB-HTR-B2
HTR-BAY-B2
120A-CNTRL
120B-CNTRL
INST-PT-A
INST-LT-A
RELAY-K27A
PANEL-RPS-A
PANEL-ESF-A
JB-A401
PANEL-RPS-B
PANEL-ESF-B
JB-B501
RELAY-K27B
INST-PT-B
INST-LT-B
""".strip().splitlines()


FINAL_EDGE_TEXT = """
GRID-1,AUX-TR-1A,solid_power,asserted
AUX-TR-1A,CB-101,solid_power,asserted
CB-101,BUS-416A,solid_power,asserted
BUS-416A,BUS-TIE-41,solid_tie,asserted
BUS-TIE-41,BUS-416B,solid_tie,asserted
BUS-416B,CB-102,solid_power,asserted
CB-102,AUX-TR-1B,solid_power,asserted
AUX-TR-1B,GRID-2,solid_power,asserted
EDG-1A,CB-DG1A,solid_power,asserted
CB-DG1A,BUS-416A,solid_power,asserted
BUS-416A,TR-480A1,solid_power,asserted
TR-480A1,CB-480A1,solid_power,asserted
CB-480A1,MCC-480A1,solid_power,asserted
BUS-416A,TR-480A2,solid_power,asserted
TR-480A2,CB-480A2,solid_power,asserted
CB-480A2,MCC-480A2,solid_power,asserted
BUS-416A,GND-1E,ground_reference,asserted
BUS-416B,GND-1E,ground_reference,asserted
BUS-416A,CB-CHG-A,solid_power,asserted
CB-CHG-A,CHGR-125A,solid_power,asserted
CHGR-125A,DC-BUS-A,solid_power,asserted
BAT-125A,DC-BUS-A,solid_power,asserted
DC-BUS-A,INV-120A,solid_power,asserted
INV-120A,BUS-120A,solid_power,asserted
BUS-416B,CB-CHG-B,solid_power,asserted
CB-CHG-B,CHGR-125B,solid_power,asserted
CHGR-125B,DC-BUS-B,solid_power,asserted
BAT-125B,DC-BUS-B,solid_power,asserted
DC-BUS-B,INV-120B,solid_power,asserted
INV-120B,BUS-120B,solid_power,asserted
BUS-416B,TR-480B1,solid_power,asserted
TR-480B1,CB-480B1,solid_power,asserted
CB-480B1,MCC-480B1,solid_power,asserted
BUS-416B,TR-480B2,solid_power,asserted
TR-480B2,CB-480B2,solid_power,asserted
CB-480B2,MCC-480B2,solid_power,asserted
BUS-416B,CB-DG1B,solid_power,asserted
CB-DG1B,EDG-1B,solid_power,asserted
MCC-480A1,FDB-A1,solid_power,asserted
FDB-A1,CB-SI-A1,solid_power,asserted
CB-SI-A1,PUMP-SI-A1,solid_power,asserted
FDB-A1,CB-RHR-A1,solid_power,asserted
CB-RHR-A1,PUMP-RHR-A1,solid_power,asserted
FDB-A1,CB-CCW-A1,solid_power,asserted
CB-CCW-A1,PUMP-CCW-A1,solid_power,asserted
FDB-A1,CB-FAN-A1,solid_power,asserted
CB-FAN-A1,FAN-CR-A1,solid_power,asserted
FDB-A1,CB-MOV-A101,solid_power,asserted
CB-MOV-A101,VALVE-SI-A101,solid_power,asserted
FDB-A1,CB-MOV-A102,solid_power,asserted
CB-MOV-A102,VALVE-RHR-A102,solid_power,asserted
MCC-480A2,FDB-A2,solid_power,asserted
FDB-A2,CB-CS-A2,solid_power,asserted
CB-CS-A2,PUMP-CS-A2,solid_power,asserted
FDB-A2,CB-SW-A2,solid_power,asserted
CB-SW-A2,PUMP-SW-A2,solid_power,asserted
FDB-A2,CB-AFW-A2,solid_power,asserted
CB-AFW-A2,PUMP-AFW-A2,solid_power,asserted
FDB-A2,CB-FAN-A2,solid_power,asserted
CB-FAN-A2,FAN-EB-A2,solid_power,asserted
FDB-A2,CB-MOV-A201,solid_power,asserted
CB-MOV-A201,VALVE-CCW-A201,solid_power,asserted
FDB-A2,CB-HTR-A2,solid_power,asserted
CB-HTR-A2,HTR-BAY-A2,solid_power,asserted
MCC-480B1,FDB-B1,solid_power,asserted
FDB-B1,CB-SI-B1,solid_power,asserted
CB-SI-B1,PUMP-SI-B1,solid_power,asserted
FDB-B1,CB-RHR-B1,solid_power,asserted
CB-RHR-B1,PUMP-RHR-B1,solid_power,asserted
FDB-B1,CB-CCW-B1,solid_power,asserted
CB-CCW-B1,PUMP-CCW-B1,solid_power,asserted
FDB-B1,CB-FAN-B1,solid_power,asserted
CB-FAN-B1,FAN-CR-B1,solid_power,asserted
FDB-B1,CB-MOV-B101,solid_power,asserted
CB-MOV-B101,VALVE-SI-B101,solid_power,asserted
FDB-B1,CB-MOV-B102,solid_power,asserted
CB-MOV-B102,VALVE-RHR-B102,solid_power,asserted
MCC-480B2,FDB-B2,solid_power,asserted
FDB-B2,CB-CS-B2,solid_power,asserted
CB-CS-B2,PUMP-CS-B2,solid_power,asserted
FDB-B2,CB-SW-B2,solid_power,asserted
CB-SW-B2,PUMP-SW-B2,solid_power,asserted
FDB-B2,CB-FAN-B2,solid_power,asserted
CB-FAN-B2,FAN-EB-B2,solid_power,asserted
FDB-B2,CB-MOV-B201,solid_power,asserted
CB-MOV-B201,VALVE-CCW-B201,solid_power,asserted
FDB-B2,CB-HTR-B2,solid_power,asserted
CB-HTR-B2,HTR-BAY-B2,solid_power,asserted
BUS-120A,PANEL-RPS-A,dashed_control_power,asserted
INST-PT-A,PANEL-RPS-A,dotted_signal,asserted
INST-LT-A,PANEL-RPS-A,dotted_signal,asserted
RELAY-K27A,PANEL-RPS-A,dashed_control,asserted
RELAY-K27A,PANEL-ESF-A,dashed_control,asserted
PANEL-ESF-A,JB-A401,dashed_control,asserted
BUS-120B,PANEL-RPS-B,dashed_control_power,asserted
PANEL-RPS-B,INST-PT-B,dotted_signal,asserted
PANEL-RPS-B,INST-LT-B,dotted_signal,asserted
PANEL-RPS-B,RELAY-K27B,dashed_control,asserted
RELAY-K27B,PANEL-ESF-B,dashed_control,asserted
PANEL-ESF-B,JB-B501,dashed_control,asserted
""".strip().splitlines()


FINAL_EDGES = [tuple(line.split(",")) for line in FINAL_EDGE_TEXT]


def without_edges(edges, pairs_to_remove):
    blocked = {frozenset(pair) for pair in pairs_to_remove}
    return [edge for edge in edges if frozenset(edge[:2]) not in blocked]


def replace_edges(edges, replacements):
    result = list(edges)
    for old_pairs, new_edges in replacements:
        result = without_edges(result, old_pairs)
        result.extend(new_edges)
    return result


def diego_round1_edges():
    uncertain_source = {
        frozenset(("CB-101", "BUS-416A")),
        frozenset(("BUS-416B", "CB-102")),
    }
    edges = []
    for a, b, edge_type, status in FINAL_EDGES:
        if frozenset((a, b)) in uncertain_source:
            status = "uncertain_plausible"
        if {a, b} == {"BUS-416A", "GND-1E"}:
            edges.extend([
                ("BUS-416A", "GND-A", "ground_reference", "asserted"),
                ("GND-A", "GND-1E", "ground_reference", "asserted"),
            ])
        elif {a, b} == {"BUS-416B", "GND-1E"}:
            edges.extend([
                ("BUS-416B", "GND-B", "ground_reference", "asserted"),
                ("GND-B", "GND-1E", "ground_reference", "asserted"),
            ])
        elif {a, b} == {"BUS-120A", "PANEL-RPS-A"}:
            edges.extend([
                ("BUS-120A", "120A-CNTRL", "dashed_control_power", "asserted"),
                ("120A-CNTRL", "PANEL-RPS-A", "dashed_control_power", "asserted"),
            ])
        elif {a, b} == {"BUS-120B", "PANEL-RPS-B"}:
            edges.extend([
                ("BUS-120B", "120B-CNTRL", "dashed_control_power", "asserted"),
                ("120B-CNTRL", "PANEL-RPS-B", "dashed_control_power", "asserted"),
            ])
        else:
            edges.append((a, b, edge_type, status))
    edges.append(("BUS-TIE-41", "GND-1E", "ground_reference", "uncertain_plausible"))
    return edges


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
        if a not in index or b not in index:
            raise ValueError(f"Missing component in edge: {a}, {b}")
        if status == "excluded":
            continue
        i = index[a]
        j = index[b]
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
    total = 0
    for row in rows[1:]:
        total += sum(int(value) for value in row[1:])
    return total // 2


def validate_round(name, components, edges, expected_edges):
    node_set = set(components)
    for a, b, _edge_type, _status in edges:
        if a not in node_set or b not in node_set:
            raise ValueError(f"{name}: edge references unknown node: {a}, {b}")
    unique_pairs = {frozenset((a, b)) for a, b, _t, status in edges if status != "excluded" and a != b}
    if len(unique_pairs) != expected_edges:
        raise ValueError(f"{name}: expected {expected_edges} unique edges, got {len(unique_pairs)}")


def write_summary():
    text = """# Connectivity Extraction Summary

Document: 3 / Raw + components

Allowed visual inputs:
- raw -- synthetic_npp_100_component_electrical_schematic.png
- detected_components_and_logical_overlay.png
- generated crops in codes/visual_aids, derived only from the two allowed images

Round sequence:
1. Diego round 1: high-recall extraction. Proposed 104 nodes by treating GND-A, GND-B, 120A-CNTRL, and 120B-CNTRL as possible nodes; carried the two source breaker-to-bus edges and BUS-TIE-41--GND-1E as uncertain/plausible.
2. Jennifer round 1: precision refinement. Reduced to the 100 visually supported components, collapsed control labels, replaced local ground labels with BUS-416A/B--GND-1E, and withheld CB-101--BUS-416A plus CB-102--BUS-416B as uncertain because of the small visual gap.
3. Diego round 2: agreed with Jennifer round 1; no changes requested.
4. Jennifer round 2: saturated=true. Added CB-101--BUS-416A and CB-102--BUS-416B after considering the raw annotation VISIBLE COMPONENTS = 100; VISIBLE CONNECTIONS = 100 and the aligned source leads/bus landing dots. BUS-TIE-41--GND-1E remains excluded.

Final component count: 100
Final undirected edge count: 100

Important modeling decisions:
- GND-A and GND-B are local reference labels, not standalone matrix nodes.
- 120A-CNTRL and 120B-CNTRL are control-line labels, not standalone matrix nodes.
- BUS-416A and BUS-416B remain separate bus nodes connected through BUS-TIE-41.
- CB-101--BUS-416A and CB-102--BUS-416B are included in the final matrix.
- BUS-TIE-41--GND-1E is not included.
- B2 contains five visible feeder/load pairs; no AFW-B2 component is visible.
"""
    (RESULTS / "round_summaries.md").write_text(text, encoding="utf-8")


def write_token_usage():
    rows = [
        {
            "document": "3",
            "iteration": "1",
            "call_id": "main_coordinator_aggregate",
            "model": "GPT-5/Codex main",
            "input_tokens_est_low": 9000,
            "input_tokens_est_expected": 13500,
            "input_tokens_est_high": 19000,
            "cached_input_tokens": "unknown",
            "output_tokens_est_low": 1200,
            "output_tokens_est_expected": 2200,
            "output_tokens_est_high": 3500,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est_expected": 10500,
            "usage_object_available": "no",
            "notes": "Main inspected raw, overlay, generated crops, and integrated subagent outputs. Official Responses token counting was not callable because no API key is available in this environment.",
        },
        {
            "document": "3",
            "iteration": "1",
            "call_id": "diego_round1",
            "model": "gpt-5.5",
            "input_tokens_est_low": 14500,
            "input_tokens_est_expected": 20500,
            "input_tokens_est_high": 28500,
            "cached_input_tokens": "unknown",
            "output_tokens_est_low": 2500,
            "output_tokens_est_expected": 4200,
            "output_tokens_est_high": 6500,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est_expected": 16500,
            "usage_object_available": "no",
            "notes": "High-recall extraction over full images plus visual crops.",
        },
        {
            "document": "3",
            "iteration": "1",
            "call_id": "jennifer_round1",
            "model": "gpt-5.5",
            "input_tokens_est_low": 13000,
            "input_tokens_est_expected": 18500,
            "input_tokens_est_high": 26000,
            "cached_input_tokens": "unknown",
            "output_tokens_est_low": 1800,
            "output_tokens_est_expected": 3200,
            "output_tokens_est_high": 5200,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est_expected": 14500,
            "usage_object_available": "no",
            "notes": "Precision review of Diego round 1 using raw and derived visual resources.",
        },
        {
            "document": "3",
            "iteration": "1",
            "call_id": "diego_round2",
            "model": "gpt-5.5",
            "input_tokens_est_low": 8500,
            "input_tokens_est_expected": 12500,
            "input_tokens_est_high": 18000,
            "cached_input_tokens": "unknown",
            "output_tokens_est_low": 250,
            "output_tokens_est_expected": 650,
            "output_tokens_est_high": 1200,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est_expected": 9000,
            "usage_object_available": "no",
            "notes": "Focused disagreement review on source breaker bus landings, ground treatment, and control labels.",
        },
        {
            "document": "3",
            "iteration": "1",
            "call_id": "jennifer_round2_final",
            "model": "gpt-5.5",
            "input_tokens_est_low": 10500,
            "input_tokens_est_expected": 15000,
            "input_tokens_est_high": 21500,
            "cached_input_tokens": "unknown",
            "output_tokens_est_low": 300,
            "output_tokens_est_expected": 750,
            "output_tokens_est_high": 1300,
            "reasoning_tokens": "not exposed",
            "image_file_input_tokens_est_expected": 10500,
            "usage_object_available": "no",
            "notes": "Final saturation pass. Usage object was not returned by the multi-agent wrapper.",
        },
    ]
    total_expected = sum(r["input_tokens_est_expected"] + r["output_tokens_est_expected"] for r in rows)
    rows.append({
        "document": "3",
        "iteration": "1",
        "call_id": "TOTAL_ESTIMATE",
        "model": "",
        "input_tokens_est_low": sum(r["input_tokens_est_low"] for r in rows),
        "input_tokens_est_expected": sum(r["input_tokens_est_expected"] for r in rows),
        "input_tokens_est_high": sum(r["input_tokens_est_high"] for r in rows),
        "cached_input_tokens": "unknown",
        "output_tokens_est_low": sum(r["output_tokens_est_low"] for r in rows),
        "output_tokens_est_expected": sum(r["output_tokens_est_expected"] for r in rows),
        "output_tokens_est_high": sum(r["output_tokens_est_high"] for r in rows),
        "reasoning_tokens": "not exposed",
        "image_file_input_tokens_est_expected": sum(r["image_file_input_tokens_est_expected"] for r in rows),
        "usage_object_available": "no",
        "notes": f"Expected total input+output tokens estimate: {total_expected}. Low/high totals can be derived from columns.",
    })
    fieldnames = list(rows[0].keys())
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    jennifer_round1_edges = without_edges(
        FINAL_EDGES,
        [("CB-101", "BUS-416A"), ("BUS-416B", "CB-102")],
    )
    diego_round2_edges = list(jennifer_round1_edges)
    diego1_edges = diego_round1_edges()

    rounds = [
        ("diego_round1", DIEGO_ROUND1_COMPONENTS, diego1_edges, 105),
        ("jennifer_round1", FINAL_COMPONENTS, jennifer_round1_edges, 98),
        ("diego_round2", FINAL_COMPONENTS, diego_round2_edges, 98),
        ("jennifer_round2_final", FINAL_COMPONENTS, FINAL_EDGES, 100),
        ("final", FINAL_COMPONENTS, FINAL_EDGES, 100),
    ]
    for name, components, edges, expected_edges in rounds:
        validate_round(name, components, edges, expected_edges)
        matrix_name = "final_connectivity_matrix.csv" if name == "final" else f"{name}_matrix.csv"
        edges_name = "final_edges.csv" if name == "final" else f"{name}_edges.csv"
        write_edges(RESULTS / edges_name, edges)
        write_matrix(RESULTS / matrix_name, components, edges)
        counted = count_matrix_edges(RESULTS / matrix_name)
        if counted != expected_edges:
            raise ValueError(f"{name}: matrix has {counted} edges; expected {expected_edges}")

    write_summary()
    write_token_usage()
    print("Wrote connectivity artifacts to", RESULTS)
    print("Final components:", len(FINAL_COMPONENTS))
    print("Final undirected edges:", len({frozenset(edge[:2]) for edge in FINAL_EDGES}))


if __name__ == "__main__":
    main()
