import csv
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


DIEGO_R1_COMPONENTS = [
    "GRID-345A",
    "SWGR-52A",
    "RAT-1A",
    "MAIN-GEN-1",
    "GCB-1",
    "UAT-1A",
    "EDG-1A",
    "CB-EDG-A",
    "BUS-4KV-A",
    "CB-TIE-AB",
    "DS-TIE-AB",
    "GRID-345B",
    "SWGR-52B",
    "RAT-1B",
    "EDG-1B",
    "CB-EDG-B",
    "BUS-4KV-B",
    "CB-TIE-BC",
    "DS-TIE-BC",
    "EDG-1C",
    "CB-EDG-C",
    "AAC-GEN-1",
    "CB-AAC-C",
    "BUS-4KV-C",
    "CB-4A-01",
    "TR-480A",
    "CB-48A-01",
    "BUS-480-A",
    "CB-4B-01",
    "TR-480B",
    "CB-48B-01",
    "BUS-480-B",
    "CB-4C-01",
    "TR-480C",
    "CB-48C-01",
    "BUS-480-C",
    "CB-P201A",
    "MCC-01A",
    "RELAY-K201A",
    "PUMP-P201A",
    "CB-P202A",
    "MCC-02A",
    "RELAY-K202A",
    "PUMP-P202A",
    "CB-M301A",
    "MCC-03A",
    "RELAY-K301A",
    "MOTOR-FAN301A",
    "CB-V410A",
    "MCC-04A",
    "SOL-V410A",
    "VALVE-V410A",
    "CB-P201B",
    "MCC-01B",
    "RELAY-K201B",
    "PUMP-P201B",
    "CB-P202B",
    "MCC-02B",
    "RELAY-K202B",
    "PUMP-P202B",
    "CB-M301B",
    "MCC-03B",
    "RELAY-K301B",
    "MOTOR-FAN301B",
    "CB-V410B",
    "MCC-04B",
    "SOL-V410B",
    "VALVE-V410B",
    "CB-P501",
    "MCC-05C",
    "RELAY-K501",
    "PUMP-CCW501",
    "CB-M601",
    "MCC-06C",
    "RELAY-K601",
    "MOTOR-HVAC601",
    "CB-V502",
    "MCC-07C",
    "SOL-V502",
    "VALVE-V502",
    "CB-P503",
    "MCC-08C",
    "RELAY-K503",
    "PUMP-SW503",
    "CHG-125A",
    "BAT-125A",
    "BUS-125DC-A",
    "INV-120A",
    "BUS-120AC-A",
    "PNL-RPS-A",
    "RELAY-UV-A",
    "PT-A",
    "INSTR-PT-A",
    "CHG-125B",
    "BAT-125B",
    "BUS-125DC-B",
    "INV-120B",
    "BUS-120AC-B",
    "PNL-RPS-B",
    "RELAY-UV-B",
    "PT-B",
    "INSTR-PT-B",
    "N.O. DC TIE",
]


FINAL_COMPONENTS = [
    "GRID-345A",
    "SWGR-52A",
    "RAT-1A",
    "MAIN-GEN-1",
    "GCB-1",
    "UAT-1A",
    "EDG-1A",
    "CB-EDG-A",
    "BUS-4KV-A",
    "CB-TIE-AB",
    "DS-TIE-AB",
    "GRID-345B",
    "SWGR-52B",
    "RAT-1B",
    "EDG-1B",
    "CB-EDG-B",
    "BUS-4KV-B",
    "CB-TIE-BC",
    "DS-TIE-BC",
    "EDG-1C",
    "CB-EDG-C",
    "AAC-GEN-1",
    "CB-AAC-C",
    "BUS-4KV-C",
    "CB-4A-01",
    "TR-480A",
    "CB-48A-01",
    "BUS-480-A",
    "CB-4B-01",
    "TR-480B",
    "CB-48B-01",
    "BUS-480-B",
    "CB-4C-01",
    "TR-480C",
    "CB-48C-01",
    "BUS-480-C",
    "CB-P201A",
    "MCC-01A",
    "RELAY-K201A",
    "PUMP-P201A",
    "CB-P202A",
    "MCC-02A",
    "RELAY-K202A",
    "PUMP-P202A",
    "CB-M301A",
    "MCC-03A",
    "RELAY-K301A",
    "MOTOR-FAN301A",
    "CB-V410A",
    "MCC-04A",
    "SOL-V410A",
    "VALVE-V410A",
    "CB-P201B",
    "MCC-01B",
    "RELAY-K201B",
    "PUMP-P201B",
    "CB-P202B",
    "MCC-02B",
    "RELAY-K202B",
    "PUMP-P202B",
    "CB-M301B",
    "MCC-03B",
    "RELAY-K301B",
    "MOTOR-FAN301B",
    "CB-V410B",
    "MCC-04B",
    "SOL-V410B",
    "VALVE-V410B",
    "CB-P501",
    "MCC-05C",
    "RELAY-K501",
    "PUMP-CCW501",
    "CB-M601",
    "MCC-06C",
    "RELAY-K601",
    "MOTOR-HVAC601",
    "CB-V502",
    "MCC-07C",
    "SOL-V502",
    "VALVE-V502",
    "CB-P503",
    "MCC-08C",
    "RELAY-K503",
    "PUMP-SW503",
    "CHG-125A",
    "BAT-125A",
    "BUS-125DC-A",
    "N.O. DC TIE",
    "BUS-125DC-B",
    "INV-120A",
    "BUS-120AC-A",
    "PNL-RPS-A",
    "RELAY-UV-A",
    "PT-A-LINE_VISUAL_LABEL_PT",
    "INSTR-PT-A",
    "CHG-125B",
    "BAT-125B",
    "INV-120B",
    "BUS-120AC-B",
    "PNL-RPS-B",
    "RELAY-UV-B",
    "PT-B-LINE_VISUAL_LABEL_PT",
    "INSTR-PT-B",
]


JENNIFER_R1_COMPONENTS = [
    *FINAL_COMPONENTS[:87],
    "INV-120A",
    "BUS-120AC-A",
    "PNL-RPS-A",
    "RELAY-UV-A",
    "PT-A-LINE_VISUAL_LABEL_PT",
    "INSTR-PT-A",
    "N.O. DC TIE",
    "CHG-125B",
    "BAT-125B",
    "BUS-125DC-B",
    "INV-120B",
    "BUS-120AC-B",
    "PNL-RPS-B",
    "RELAY-UV-B",
    "PT-B-LINE_VISUAL_LABEL_PT",
    "INSTR-PT-B",
]


BASE_EDGES = [
    ("GRID-345A", "SWGR-52A", "solid_power", "asserted"),
    ("SWGR-52A", "RAT-1A", "solid_power", "asserted"),
    ("RAT-1A", "BUS-4KV-A", "solid_power", "asserted"),
    ("MAIN-GEN-1", "GCB-1", "solid_power", "asserted"),
    ("GCB-1", "UAT-1A", "solid_power", "asserted"),
    ("UAT-1A", "BUS-4KV-A", "solid_power", "asserted"),
    ("EDG-1A", "CB-EDG-A", "solid_power", "asserted"),
    ("CB-EDG-A", "BUS-4KV-A", "solid_power", "asserted"),
    ("BUS-4KV-A", "CB-TIE-AB", "normally_open_power_tie", "asserted"),
    ("CB-TIE-AB", "DS-TIE-AB", "normally_open_power_tie", "asserted"),
    ("DS-TIE-AB", "BUS-4KV-B", "normally_open_power_tie", "asserted"),
    ("GRID-345B", "SWGR-52B", "solid_power", "asserted"),
    ("SWGR-52B", "RAT-1B", "solid_power", "asserted"),
    ("RAT-1B", "BUS-4KV-B", "solid_power", "asserted"),
    ("EDG-1B", "CB-EDG-B", "solid_power", "asserted"),
    ("CB-EDG-B", "BUS-4KV-B", "solid_power", "asserted"),
    ("BUS-4KV-B", "CB-TIE-BC", "normally_open_power_tie", "asserted"),
    ("CB-TIE-BC", "DS-TIE-BC", "normally_open_power_tie", "asserted"),
    ("DS-TIE-BC", "BUS-4KV-C", "normally_open_power_tie", "asserted"),
    ("EDG-1C", "CB-EDG-C", "solid_power", "asserted"),
    ("CB-EDG-C", "BUS-4KV-C", "solid_power", "asserted"),
    ("AAC-GEN-1", "CB-AAC-C", "solid_power", "asserted"),
    ("CB-AAC-C", "BUS-4KV-C", "solid_power", "asserted"),
    ("BUS-4KV-A", "CB-4A-01", "solid_power", "asserted"),
    ("CB-4A-01", "TR-480A", "solid_power", "asserted"),
    ("TR-480A", "CB-48A-01", "solid_power", "asserted"),
    ("CB-48A-01", "BUS-480-A", "solid_power", "asserted"),
    ("BUS-4KV-B", "CB-4B-01", "solid_power", "asserted"),
    ("CB-4B-01", "TR-480B", "solid_power", "asserted"),
    ("TR-480B", "CB-48B-01", "solid_power", "asserted"),
    ("CB-48B-01", "BUS-480-B", "solid_power", "asserted"),
    ("BUS-4KV-C", "CB-4C-01", "solid_power", "asserted"),
    ("CB-4C-01", "TR-480C", "solid_power", "asserted"),
    ("TR-480C", "CB-48C-01", "solid_power", "asserted"),
    ("CB-48C-01", "BUS-480-C", "solid_power", "asserted"),
    ("BUS-480-A", "CB-P201A", "solid_power", "asserted"),
    ("CB-P201A", "MCC-01A", "solid_power", "asserted"),
    ("MCC-01A", "RELAY-K201A", "solid_power", "asserted"),
    ("RELAY-K201A", "PUMP-P201A", "solid_power", "asserted"),
    ("BUS-480-A", "CB-P202A", "solid_power", "asserted"),
    ("CB-P202A", "MCC-02A", "solid_power", "asserted"),
    ("MCC-02A", "RELAY-K202A", "solid_power", "asserted"),
    ("RELAY-K202A", "PUMP-P202A", "solid_power", "asserted"),
    ("BUS-480-A", "CB-M301A", "solid_power", "asserted"),
    ("CB-M301A", "MCC-03A", "solid_power", "asserted"),
    ("MCC-03A", "RELAY-K301A", "solid_power", "asserted"),
    ("RELAY-K301A", "MOTOR-FAN301A", "solid_power", "asserted"),
    ("BUS-480-A", "CB-V410A", "solid_power", "asserted"),
    ("CB-V410A", "MCC-04A", "solid_power", "asserted"),
    ("MCC-04A", "SOL-V410A", "solid_power", "asserted"),
    ("SOL-V410A", "VALVE-V410A", "solid_power", "asserted"),
    ("BUS-480-A", "CHG-125A", "solid_power", "asserted"),
    ("CHG-125A", "BAT-125A", "solid_dc_power", "asserted"),
    ("BAT-125A", "BUS-125DC-A", "solid_dc_power", "asserted"),
    ("BUS-125DC-A", "INV-120A", "solid_dc_power", "asserted"),
    ("INV-120A", "BUS-120AC-A", "solid_ac_power", "asserted"),
    ("BUS-120AC-A", "PNL-RPS-A", "solid_ac_power", "asserted"),
    ("PNL-RPS-A", "RELAY-UV-A", "dashed_instrumentation", "asserted"),
    ("RELAY-UV-A", "PT-A-LINE_VISUAL_LABEL_PT", "dashed_instrumentation", "asserted"),
    ("PT-A-LINE_VISUAL_LABEL_PT", "INSTR-PT-A", "dashed_instrumentation", "asserted"),
    ("BUS-125DC-A", "N.O. DC TIE", "normally_open_dc_tie", "asserted"),
    ("N.O. DC TIE", "BUS-125DC-B", "normally_open_dc_tie", "asserted"),
    ("BUS-480-B", "CB-P201B", "solid_power", "asserted"),
    ("CB-P201B", "MCC-01B", "solid_power", "asserted"),
    ("MCC-01B", "RELAY-K201B", "solid_power", "asserted"),
    ("RELAY-K201B", "PUMP-P201B", "solid_power", "asserted"),
    ("BUS-480-B", "CB-P202B", "solid_power", "asserted"),
    ("CB-P202B", "MCC-02B", "solid_power", "asserted"),
    ("MCC-02B", "RELAY-K202B", "solid_power", "asserted"),
    ("RELAY-K202B", "PUMP-P202B", "solid_power", "asserted"),
    ("BUS-480-B", "CB-M301B", "solid_power", "asserted"),
    ("CB-M301B", "MCC-03B", "solid_power", "asserted"),
    ("MCC-03B", "RELAY-K301B", "solid_power", "asserted"),
    ("RELAY-K301B", "MOTOR-FAN301B", "solid_power", "asserted"),
    ("BUS-480-B", "CB-V410B", "solid_power", "asserted"),
    ("CB-V410B", "MCC-04B", "solid_power", "asserted"),
    ("MCC-04B", "SOL-V410B", "solid_power", "asserted"),
    ("SOL-V410B", "VALVE-V410B", "solid_power", "asserted"),
    ("BUS-480-B", "CHG-125B", "solid_power", "asserted"),
    ("CHG-125B", "BAT-125B", "solid_dc_power", "asserted"),
    ("BAT-125B", "BUS-125DC-B", "solid_dc_power", "asserted"),
    ("BUS-125DC-B", "INV-120B", "solid_dc_power", "asserted"),
    ("INV-120B", "BUS-120AC-B", "solid_ac_power", "asserted"),
    ("BUS-120AC-B", "PNL-RPS-B", "solid_ac_power", "asserted"),
    ("PNL-RPS-B", "RELAY-UV-B", "dashed_instrumentation", "asserted"),
    ("RELAY-UV-B", "PT-B-LINE_VISUAL_LABEL_PT", "dashed_instrumentation", "asserted"),
    ("PT-B-LINE_VISUAL_LABEL_PT", "INSTR-PT-B", "dashed_instrumentation", "asserted"),
    ("BUS-480-C", "CB-P501", "solid_power", "asserted"),
    ("CB-P501", "MCC-05C", "solid_power", "asserted"),
    ("MCC-05C", "RELAY-K501", "solid_power", "asserted"),
    ("RELAY-K501", "PUMP-CCW501", "solid_power", "asserted"),
    ("BUS-480-C", "CB-M601", "solid_power", "asserted"),
    ("CB-M601", "MCC-06C", "solid_power", "asserted"),
    ("MCC-06C", "RELAY-K601", "solid_power", "asserted"),
    ("RELAY-K601", "MOTOR-HVAC601", "solid_power", "asserted"),
    ("BUS-480-C", "CB-V502", "solid_power", "asserted"),
    ("CB-V502", "MCC-07C", "solid_power", "asserted"),
    ("MCC-07C", "SOL-V502", "solid_power", "asserted"),
    ("SOL-V502", "VALVE-V502", "solid_power", "asserted"),
    ("BUS-480-C", "CB-P503", "solid_power", "asserted"),
    ("CB-P503", "MCC-08C", "solid_power", "asserted"),
    ("MCC-08C", "RELAY-K503", "solid_power", "asserted"),
    ("RELAY-K503", "PUMP-SW503", "solid_power", "asserted"),
]


def diego_r1_edges():
    edges = []
    for a, b, edge_type, status in BASE_EDGES:
        a = a.replace("PT-A-LINE_VISUAL_LABEL_PT", "PT-A")
        b = b.replace("PT-A-LINE_VISUAL_LABEL_PT", "PT-A")
        a = a.replace("PT-B-LINE_VISUAL_LABEL_PT", "PT-B")
        b = b.replace("PT-B-LINE_VISUAL_LABEL_PT", "PT-B")
        if "N.O. DC TIE" in (a, b):
            status = "uncertain_plausible"
        edges.append((a, b, edge_type, status))
    return edges


def write_edges(path, edges):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["a", "b", "type", "status"])
        writer.writerows(edges)


def write_matrix(path, components, edges):
    index = {name: i for i, name in enumerate(components)}
    if len(index) != len(components):
        raise ValueError("Duplicate component names in matrix order")

    matrix = [[0 for _ in components] for _ in components]
    missing = []
    for a, b, _edge_type, _status in edges:
        if a not in index or b not in index:
            missing.append((a, b))
            continue
        i = index[a]
        j = index[b]
        if i == j:
            continue
        matrix[i][j] = 1
        matrix[j][i] = 1

    if missing:
        raise ValueError(f"Edges reference missing components: {missing}")

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["component", *components])
        for name, row in zip(components, matrix):
            writer.writerow([name, *row])


def write_summary():
    text = f"""# Connectivity Extraction Summary

Document: 1 / Raw + components

Allowed visual inputs:
- raw -- schematic_image_clean_100_connected.png
- detected_components_and_logical_overlay.png
- generated crops in codes/visual_aids, derived only from the two allowed images

Round sequence:
1. Diego round 1: high-recall extraction. Kept PT-A/PT-B as inferred local names and marked the unboxed N.O. DC TIE as uncertain-plausible.
2. Jennifer round 1: precision refinement. Renamed PT-A/PT-B to PT-A-LINE_VISUAL_LABEL_PT and PT-B-LINE_VISUAL_LABEL_PT because the printed label is only PT. Retained N.O. DC TIE as a logical normally-open tie node.
3. Diego round 2: agreed with Jennifer round 1; no changes requested.
4. Jennifer round 2: saturated=true; endorsed final matrix.

Final component count: {len(FINAL_COMPONENTS)}
Final undirected edge count: {len(BASE_EDGES)}

Important modeling decisions:
- BUS-4KV-A/B/C, BUS-480-A/B/C, BUS-125DC-A/B, and BUS-120AC-A/B are explicit logical nodes.
- The 4 kV normally-open ties are represented through CB-TIE/DS-TIE components, with no direct bus-to-bus merge.
- The unboxed N.O. DC TIE is represented as a logical normally-open tie node, with no direct BUS-125DC-A to BUS-125DC-B merge.
- The two small inline PT circles are retained as visual-label nodes using disambiguating names because the raw schematic only prints PT.
- Annotation text such as elementary-diagram sheet references and feeder cable IDs is not treated as a node.
"""
    (RESULTS / "round_summaries.md").write_text(text, encoding="utf-8")


def write_token_estimates():
    rows = [
        {
            "document": "1 / Raw + components",
            "iteration": "1",
            "call_id": "main_coordinator_aggregate",
            "agent": "main",
            "model": "gpt-5",
            "usage_object_available": "no",
            "input_tokens_low": 32000,
            "input_tokens_expected": 43000,
            "input_tokens_high": 58000,
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": 9945,
            "output_tokens_low": 2200,
            "output_tokens_expected": 3600,
            "output_tokens_high": 5200,
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": 46600,
            "notes": "Aggregate estimate for orchestration, visual inspection, tool-result reading, and final response. Includes images viewed directly by main agent.",
        },
        {
            "document": "1 / Raw + components",
            "iteration": "1",
            "call_id": "diego_round1",
            "agent": "Diego",
            "model": "gpt-5.5",
            "usage_object_available": "no",
            "input_tokens_low": 18000,
            "input_tokens_expected": 20500,
            "input_tokens_high": 24500,
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": 13260,
            "output_tokens_low": 3600,
            "output_tokens_expected": 5200,
            "output_tokens_high": 7200,
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": 25700,
            "notes": "12 image inputs; output was known after execution but exact tokenizer count unavailable.",
        },
        {
            "document": "1 / Raw + components",
            "iteration": "1",
            "call_id": "jennifer_round1",
            "agent": "Jennifer",
            "model": "gpt-5.5",
            "usage_object_available": "no",
            "input_tokens_low": 21500,
            "input_tokens_expected": 25800,
            "input_tokens_high": 31500,
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": 13260,
            "output_tokens_low": 4200,
            "output_tokens_expected": 6200,
            "output_tokens_high": 8200,
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": 32000,
            "notes": "12 image inputs plus Diego proposal summary.",
        },
        {
            "document": "1 / Raw + components",
            "iteration": "1",
            "call_id": "diego_round2",
            "agent": "Diego",
            "model": "gpt-5.5",
            "usage_object_available": "no",
            "input_tokens_low": 8000,
            "input_tokens_expected": 10200,
            "input_tokens_high": 13000,
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": 5865,
            "output_tokens_low": 900,
            "output_tokens_expected": 1500,
            "output_tokens_high": 2200,
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": 11700,
            "notes": "Narrow convergence review with 5 image inputs.",
        },
        {
            "document": "1 / Raw + components",
            "iteration": "1",
            "call_id": "jennifer_round2_final",
            "agent": "Jennifer",
            "model": "gpt-5.5",
            "usage_object_available": "no",
            "input_tokens_low": 10500,
            "input_tokens_expected": 13800,
            "input_tokens_high": 17500,
            "cached_input_tokens": "unknown",
            "image_file_input_tokens_expected": 6970,
            "output_tokens_low": 1200,
            "output_tokens_expected": 2100,
            "output_tokens_high": 3200,
            "reasoning_tokens": "not exposed",
            "total_tokens_expected": 15900,
            "notes": "Final saturation check with accepted edge list and 6 image inputs.",
        },
    ]

    total = sum(int(r["total_tokens_expected"]) for r in rows)
    rows.append(
        {
            "document": "1 / Raw + components",
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
            "notes": "Expected total across main aggregate and all subagent calls. Official endpoint not called because OPENAI_API_KEY was absent.",
        }
    )

    with (RESULTS / "token_usage_estimate.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    rounds = [
        ("diego_round1", DIEGO_R1_COMPONENTS, diego_r1_edges()),
        ("jennifer_round1", JENNIFER_R1_COMPONENTS, BASE_EDGES),
        ("diego_round2", FINAL_COMPONENTS, BASE_EDGES),
        ("jennifer_round2_final", FINAL_COMPONENTS, BASE_EDGES),
    ]

    for name, components, edges in rounds:
        write_edges(RESULTS / f"{name}_edges.csv", edges)
        write_matrix(RESULTS / f"{name}_matrix.csv", components, edges)

    write_edges(RESULTS / "final_edges.csv", BASE_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_COMPONENTS, BASE_EDGES)
    write_summary()
    write_token_estimates()


if __name__ == "__main__":
    main()
