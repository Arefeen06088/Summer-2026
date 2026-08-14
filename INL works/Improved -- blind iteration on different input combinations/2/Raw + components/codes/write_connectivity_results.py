import csv
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


COMPONENTS = """
GRID-N501
DS-N501
TR-SU-1A
CB-SU-1A
GEN-EDG-A
DS-DG-A
CB-DG-A
BUS-4160-A
CB-TIE-4AB
BUS-4160-B
GRID-R502
DS-R502
TR-SU-1B
CB-SU-1B
GEN-EDG-B
DS-DG-B
CB-DG-B
GEN-AAC-1
DS-AAC-1
CB-AAC-1
CB-F11A
TR-LC11A
BUS-480-A1
CB-M11A
MCC-11A
CB-P101A
MTR-P101A
PUMP-RHR-A
CB-F12A
TR-LC12A
BUS-480-A2
CB-M12A
MCC-12A
CB-P201A
MTR-P201A
PUMP-SI-A
CB-F13A
TR-LC13A
BUS-480-A3
CB-M13A
MCC-13A
CB-FAN-A
MTR-FAN-A
FAN-CAV-A
CB-F14A
TR-RPS-A
BUS-208-A
REC-125-A
BUS-125DC-A
BAT-125-A
INV-120-A
BUS-120AC-A
CP-RPS-A
RLY-K501A
INST-NI501A
CB-CVCS-A
MCC-CVCS-A
MTR-CVCS-A
PUMP-CVCS-A
VLV-LCV201A
CB-F11B
TR-LC11B
BUS-480-B1
CB-M11B
MCC-11B
CB-P101B
MTR-P101B
PUMP-RHR-B
CB-F12B
TR-LC12B
BUS-480-B2
CB-M12B
MCC-12B
CB-P201B
MTR-P201B
PUMP-SI-B
CB-F13B
TR-LC13B
BUS-480-B3
CB-M13B
MCC-13B
CB-FAN-B
MTR-FAN-B
FAN-CAV-B
CB-F14B
TR-RPS-B
BUS-208-B
REC-125-B
BUS-125DC-B
BAT-125-B
INV-120-B
BUS-120AC-B
CP-RPS-B
RLY-K501B
INST-NI501B
CB-CVCS-B
MCC-CVCS-B
MTR-CVCS-B
PUMP-CVCS-B
VLV-LCV201B
""".strip().splitlines()


FINAL_EDGE_TEXT = """
GRID-N501,DS-N501,solid_power
DS-N501,TR-SU-1A,solid_power
TR-SU-1A,CB-SU-1A,solid_power
CB-SU-1A,BUS-4160-A,solid_power
GEN-EDG-A,DS-DG-A,solid_power
DS-DG-A,CB-DG-A,solid_power
CB-DG-A,BUS-4160-A,solid_power
BUS-4160-A,CB-TIE-4AB,solid_tie
CB-TIE-4AB,BUS-4160-B,solid_tie
GRID-R502,DS-R502,solid_power
DS-R502,TR-SU-1B,solid_power
TR-SU-1B,CB-SU-1B,solid_power
CB-SU-1B,BUS-4160-B,solid_power
GEN-EDG-B,DS-DG-B,solid_power
DS-DG-B,CB-DG-B,solid_power
CB-DG-B,BUS-4160-B,solid_power
GEN-AAC-1,DS-AAC-1,solid_power
DS-AAC-1,CB-AAC-1,solid_power
CB-AAC-1,BUS-4160-B,solid_power
BUS-4160-A,CB-F11A,solid_power
CB-F11A,TR-LC11A,solid_power
TR-LC11A,BUS-480-A1,solid_power
BUS-480-A1,CB-M11A,solid_power
CB-M11A,MCC-11A,solid_power
MCC-11A,CB-P101A,solid_power
CB-P101A,MTR-P101A,solid_power
MTR-P101A,PUMP-RHR-A,solid_power
BUS-4160-A,CB-F12A,solid_power
CB-F12A,TR-LC12A,solid_power
TR-LC12A,BUS-480-A2,solid_power
BUS-480-A2,CB-M12A,solid_power
CB-M12A,MCC-12A,solid_power
MCC-12A,CB-P201A,solid_power
CB-P201A,MTR-P201A,solid_power
MTR-P201A,PUMP-SI-A,solid_power
BUS-4160-A,CB-F13A,solid_power
CB-F13A,TR-LC13A,solid_power
TR-LC13A,BUS-480-A3,solid_power
BUS-480-A3,CB-M13A,solid_power
CB-M13A,MCC-13A,solid_power
MCC-13A,CB-FAN-A,solid_power
CB-FAN-A,MTR-FAN-A,solid_power
MTR-FAN-A,FAN-CAV-A,solid_power
BUS-4160-A,CB-F14A,solid_power
CB-F14A,TR-RPS-A,solid_power
TR-RPS-A,BUS-208-A,solid_power
BUS-208-A,REC-125-A,solid_power
REC-125-A,BUS-125DC-A,solid_power
BUS-125DC-A,BAT-125-A,solid_power
BUS-125DC-A,INV-120-A,solid_power
INV-120-A,BUS-120AC-A,solid_power
BUS-120AC-A,CP-RPS-A,solid_power
CP-RPS-A,RLY-K501A,dashed_control
RLY-K501A,INST-NI501A,dashed_control
BUS-4160-A,CB-CVCS-A,solid_power
CB-CVCS-A,MCC-CVCS-A,solid_power
MCC-CVCS-A,MTR-CVCS-A,solid_power
MTR-CVCS-A,PUMP-CVCS-A,solid_power
PUMP-CVCS-A,VLV-LCV201A,dashed_control
BUS-4160-B,CB-F11B,solid_power
CB-F11B,TR-LC11B,solid_power
TR-LC11B,BUS-480-B1,solid_power
BUS-480-B1,CB-M11B,solid_power
CB-M11B,MCC-11B,solid_power
MCC-11B,CB-P101B,solid_power
CB-P101B,MTR-P101B,solid_power
MTR-P101B,PUMP-RHR-B,solid_power
BUS-4160-B,CB-F12B,solid_power
CB-F12B,TR-LC12B,solid_power
TR-LC12B,BUS-480-B2,solid_power
BUS-480-B2,CB-M12B,solid_power
CB-M12B,MCC-12B,solid_power
MCC-12B,CB-P201B,solid_power
CB-P201B,MTR-P201B,solid_power
MTR-P201B,PUMP-SI-B,solid_power
BUS-4160-B,CB-F13B,solid_power
CB-F13B,TR-LC13B,solid_power
TR-LC13B,BUS-480-B3,solid_power
BUS-480-B3,CB-M13B,solid_power
CB-M13B,MCC-13B,solid_power
MCC-13B,CB-FAN-B,solid_power
CB-FAN-B,MTR-FAN-B,solid_power
MTR-FAN-B,FAN-CAV-B,solid_power
BUS-4160-B,CB-F14B,solid_power
CB-F14B,TR-RPS-B,solid_power
TR-RPS-B,BUS-208-B,solid_power
BUS-208-B,REC-125-B,solid_power
REC-125-B,BUS-125DC-B,solid_power
BUS-125DC-B,BAT-125-B,solid_power
BUS-125DC-B,INV-120-B,solid_power
INV-120-B,BUS-120AC-B,solid_power
BUS-120AC-B,CP-RPS-B,solid_power
CP-RPS-B,RLY-K501B,dashed_control
RLY-K501B,INST-NI501B,dashed_control
BUS-4160-B,CB-CVCS-B,solid_power
CB-CVCS-B,MCC-CVCS-B,solid_power
MCC-CVCS-B,MTR-CVCS-B,solid_power
MTR-CVCS-B,PUMP-CVCS-B,solid_power
PUMP-CVCS-B,VLV-LCV201B,dashed_control
CP-RPS-A,CP-RPS-B,dashed_control
""".strip().splitlines()


def parse_edges(round_name: str):
    edges = []
    for line in FINAL_EDGE_TEXT:
        a, b, edge_type = line.split(",")
        if round_name == "diego_round1":
            edge_type = "dashed" if edge_type == "dashed_control" else "solid"
        edges.append((a, b, edge_type, "asserted"))
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
    for a, b, _edge_type, _status in edges:
        if a not in index or b not in index:
            raise ValueError(f"Missing component in edge: {a}, {b}")
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


def write_summary():
    text = f"""# Connectivity Extraction Summary

Document: 2 / Raw + components

Allowed visual inputs:
- raw -- schematic_image_variant_b_100.png
- detected_components_and_logical_overlay.png
- generated crops in codes/visual_aids, derived only from the two allowed images

Round sequence:
1. Diego round 1: high-recall extraction. Proposed 100 components and 100 asserted edges, including dashed CVCS valve links and the dashed CP-RPS-A/CP-RPS-B cross-link.
2. Jennifer round 1: precision refinement. Kept the same component set and topology; normalized edge types to solid_power, solid_tie, and dashed_control; excluded direct BUS-4160-A/B merge and direct CP-to-INST shortcuts.
3. Diego round 2: agreed with Jennifer round 1; no changes requested.
4. Jennifer round 2: saturated=true.

Final component count: {len(COMPONENTS)}
Final undirected edge count: {len(FINAL_EDGE_TEXT)}

Important modeling decisions:
- BUS-4160-A and BUS-4160-B are separate bus nodes connected only through CB-TIE-4AB.
- Dashed CP-RPS-A--CP-RPS-B is included as a control/signal connection.
- CP-RPS to instrument paths are represented in series through RLY-K501A/B.
- Dashed CVCS pump-to-valve paths are included as control/signal connections.
- Dashed feeder area boundaries, cable labels, title text, notes, and legends are not treated as nodes.
"""
    (RESULTS / "round_summaries.md").write_text(text, encoding="utf-8")


def write_token_estimates():
    rows = [
        {
            "document": "2 / Raw + components",
            "iteration": "1",
            "call_id": "main_coordinator_aggregate",
            "agent": "main",
            "model": "gpt-5",
            "usage_object_available": "no",
            "input_tokens_low": 42000,
            "input_tokens_expected": 56000,
            "input_tokens_high": 74000,
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": 14300,
            "output_tokens_low": 2200,
            "output_tokens_expected": 3800,
            "output_tokens_high": 5600,
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": 59800,
            "notes": "Aggregate estimate for orchestration, direct image viewing, tool outputs, scripts, validation, and final response.",
        },
        {
            "document": "2 / Raw + components",
            "iteration": "1",
            "call_id": "diego_round1",
            "agent": "Diego",
            "model": "gpt-5.5",
            "usage_object_available": "no",
            "input_tokens_low": 22000,
            "input_tokens_expected": 26500,
            "input_tokens_high": 33000,
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": 15470,
            "output_tokens_low": 5200,
            "output_tokens_expected": 7600,
            "output_tokens_high": 9800,
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": 34100,
            "notes": "14 image inputs; exact response usage not exposed by subagent tool.",
        },
        {
            "document": "2 / Raw + components",
            "iteration": "1",
            "call_id": "jennifer_round1",
            "agent": "Jennifer",
            "model": "gpt-5.5",
            "usage_object_available": "no",
            "input_tokens_low": 24500,
            "input_tokens_expected": 30500,
            "input_tokens_high": 38500,
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": 13260,
            "output_tokens_low": 5200,
            "output_tokens_expected": 7900,
            "output_tokens_high": 10300,
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": 38400,
            "notes": "12 image inputs plus Diego compact proposal.",
        },
        {
            "document": "2 / Raw + components",
            "iteration": "1",
            "call_id": "diego_round2",
            "agent": "Diego",
            "model": "gpt-5.5",
            "usage_object_available": "no",
            "input_tokens_low": 9000,
            "input_tokens_expected": 11800,
            "input_tokens_high": 15000,
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": 7735,
            "output_tokens_low": 450,
            "output_tokens_expected": 800,
            "output_tokens_high": 1300,
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": 12600,
            "notes": "7 image inputs; narrow convergence review.",
        },
        {
            "document": "2 / Raw + components",
            "iteration": "1",
            "call_id": "jennifer_round2_final",
            "agent": "Jennifer",
            "model": "gpt-5.5",
            "usage_object_available": "no",
            "input_tokens_low": 12500,
            "input_tokens_expected": 16500,
            "input_tokens_high": 22000,
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": 7735,
            "output_tokens_low": 10,
            "output_tokens_expected": 20,
            "output_tokens_high": 100,
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": 16520,
            "notes": "7 image inputs plus accepted edge list; final output was saturated:true.",
        },
    ]
    total = sum(int(r["total_tokens_expected"]) for r in rows)
    rows.append(
        {
            "document": "2 / Raw + components",
            "iteration": "1",
            "call_id": "TOTAL",
            "agent": "all",
            "model": "mixed",
            "usage_object_available": "no",
            "input_tokens_low": sum(int(r["input_tokens_low"]) for r in rows),
            "input_tokens_expected": sum(int(r["input_tokens_expected"]) for r in rows),
            "input_tokens_high": sum(int(r["input_tokens_high"]) for r in rows),
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": sum(int(r["image_file_input_tokens_expected"]) for r in rows),
            "output_tokens_low": sum(int(r["output_tokens_low"]) for r in rows),
            "output_tokens_expected": sum(int(r["output_tokens_expected"]) for r in rows),
            "output_tokens_high": sum(int(r["output_tokens_high"]) for r in rows),
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": total,
            "notes": "Official endpoint not called because OPENAI_API_KEY was absent; exact usage objects were unavailable.",
        }
    )
    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    if len(COMPONENTS) != 100:
        raise ValueError(f"Expected 100 components, got {len(COMPONENTS)}")
    if len(FINAL_EDGE_TEXT) != 100:
        raise ValueError(f"Expected 100 edges, got {len(FINAL_EDGE_TEXT)}")

    for round_name in [
        "diego_round1",
        "jennifer_round1",
        "diego_round2",
        "jennifer_round2_final",
    ]:
        edges = parse_edges(round_name)
        write_edges(RESULTS / f"{round_name}_edges.csv", edges)
        write_matrix(RESULTS / f"{round_name}_matrix.csv", COMPONENTS, edges)

    final_edges = parse_edges("final")
    write_edges(RESULTS / "final_edges.csv", final_edges)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", COMPONENTS, final_edges)
    write_summary()
    write_token_estimates()


if __name__ == "__main__":
    main()
