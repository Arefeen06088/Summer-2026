import csv
import math
from collections import Counter
from pathlib import Path

from PIL import Image


DOCUMENT = "11"
ITERATION = "1"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw + wires + junctions + OCR")
CODES = BASE / "codes"
RESULTS = BASE / "results"

COMPONENTS_CSV = BASE / "component_visual_ocr_labels.csv"
DIEGO_NODE_CSV = RESULTS / "diego_node_additions_corrections.csv"
DIEGO_EDGE_CSV = RESULTS / "diego_edge_list.csv"

ACCEPTED_ADDITIONS = [
    "CB-MCC-A1",
    "BUS-13-8A",
    "BUS-13-8B",
    "BUS-4160-A",
    "BUS-4160-B",
    "BUS-4160-C",
    "BUS-4160-D",
    "BUS-480-A1",
    "BUS-480-A2",
    "BUS-480-B1",
    "BUS-480-B2",
    "BUS-480-C1",
    "BUS-480-C2",
    "BUS-480-D1",
    "BUS-480-D2",
    "BUS-DC-125A",
    "BUS-DC-125B",
    "GND-A",
    "GND-B",
    "GND-C",
    "GND-D",
]

DIVISIONS = ["A", "B", "C", "D"]


def canon(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def component_rows() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(COMPONENTS_CSV):
        rows.append(
            {
                "node": row["final_label"],
                "node_kind": row["node_kind"],
                "component_type": row["component_type"],
                "source": "component_visual_ocr_labels.csv",
                "evidence": row["evidence_description"],
            }
        )
    return rows


def final_nodes() -> list[dict[str, str]]:
    rows = component_rows()
    diego_additions = {row["node_name"]: row for row in read_csv(DIEGO_NODE_CSV)}
    for node in ACCEPTED_ADDITIONS:
        source = diego_additions.get(node, {})
        rows.append(
            {
                "node": node,
                "node_kind": source.get("node_kind", "accepted_logical_node"),
                "component_type": source.get("node_kind", "accepted_logical_node"),
                "source": "round_02_jennifer_precision_accepted",
                "evidence": source.get("evidence", "Accepted visible node from Jennifer precision review."),
            }
        )
    seen = {}
    for row in rows:
        if row["node"] in seen:
            raise ValueError(f"duplicate final node: {row['node']}")
        seen[row["node"]] = row
    return sorted(rows, key=lambda row: row["node"])


def diego_round1_nodes() -> list[dict[str, str]]:
    rows = component_rows()
    for row in read_csv(DIEGO_NODE_CSV):
        if row["action"] == "add":
            rows.append(
                {
                    "node": row["node_name"],
                    "node_kind": row["node_kind"],
                    "component_type": row["node_kind"],
                    "source": "diego_round_01_high_recall",
                    "evidence": row["evidence"],
                }
            )
    seen = {}
    for row in rows:
        if row["node"] in seen:
            raise ValueError(f"duplicate Diego node: {row['node']}")
        seen[row["node"]] = row
    return sorted(rows, key=lambda row: row["node"])


def load_diego_edges() -> list[dict[str, str]]:
    edges = []
    seen = set()
    for row in read_csv(DIEGO_EDGE_CSV):
        a = row["node_a"]
        b = row["node_b"]
        key = canon(a, b)
        if key in seen:
            raise ValueError(f"duplicate Diego edge: {a} -- {b}")
        seen.add(key)
        edges.append(
            {
                "node_a": a,
                "node_b": b,
                "edge_kind": row["kind"],
                "confidence": row["confidence"],
                "evidence": row["evidence"],
            }
        )
    return edges


def edge(a: str, b: str, kind: str, evidence: str, confidence: str = "high") -> dict[str, str]:
    return {"node_a": a, "node_b": b, "edge_kind": kind, "confidence": confidence, "evidence": evidence}


def final_edges() -> list[dict[str, str]]:
    edges: list[dict[str, str]] = [
        edge("GEN-01", "TR-UAT-1", "power", "Solid 13.8 kV generator lead enters TR-UAT-1."),
        edge("TR-UAT-1", "CB-UAT-1", "power", "UAT-1 secondary conductor lands on CB-UAT-1."),
        edge("CB-UAT-1", "BUS-13-8A", "power_bus_connection", "CB-UAT-1 connects into BUS-13-8A."),
        edge("TR-SUT-1", "CB-SUT-1", "power", "SUT-1 secondary conductor lands on CB-SUT-1."),
        edge("CB-SUT-1", "BUS-13-8A", "power_bus_connection", "CB-SUT-1 connects into BUS-13-8A."),
        edge("CB-SUT-1", "CB-13-TIE", "power_tie", "Right side of CB-SUT-1 continues on the 13T-A tie conductor."),
        edge("CB-13-TIE", "BUS-13-8B", "power_tie", "CB-13-TIE right side continues into BUS-13-8B."),
        edge("GEN-02", "TR-UAT-2", "power", "Solid 13.8 kV generator lead enters TR-UAT-2."),
        edge("TR-UAT-2", "CB-UAT-2", "power", "UAT-2 secondary conductor lands on CB-UAT-2."),
        edge("CB-UAT-2", "BUS-13-8B", "power_bus_connection", "CB-UAT-2 connects into BUS-13-8B."),
        edge("TR-SUT-2", "CB-SUT-2", "power", "SUT-2 secondary conductor lands on CB-SUT-2."),
        edge("CB-SUT-2", "BUS-13-8B", "power_bus_connection", "CB-SUT-2 connects into BUS-13-8B."),
    ]

    for div in DIVISIONS:
        source_bus = "BUS-13-8A" if div in ("A", "B") else "BUS-13-8B"
        dc_bus = "BUS-DC-125A" if div in ("A", "B") else "BUS-DC-125B"
        ats = "ATS-480-A" if div in ("A", "B") else "ATS-480-B"
        edges.extend(
            [
                edge(source_bus, f"CB-IN-{div}", "power", f"Normal incoming feeder for train {div} drops from {source_bus}."),
                edge(f"CB-IN-{div}", f"BUS-4160-{div}", "power_bus_connection", f"CB-IN-{div} lands on BUS-4160-{div}."),
                edge(f"DG-2{div}", f"CB-DG-{div}", "power", f"Diesel generator DG-2{div} lead enters CB-DG-{div}."),
                edge(f"CB-DG-{div}", f"BUS-4160-{div}", "power_bus_connection", f"CB-DG-{div} lands on BUS-4160-{div}."),
                edge(f"CB-IN-{div}", f"RELAY-27{div}", "control_interlock", f"Dashed interlock line from CB-IN-{div} to RELAY-27{div}.", "medium"),
                edge(f"RELAY-27{div}", f"CB-DG-{div}", "control_interlock", f"Dashed interlock line from RELAY-27{div} to CB-DG-{div}.", "medium"),
            ]
        )
        for branch in ("1", "2"):
            edges.extend(
                [
                    edge(f"BUS-4160-{div}", f"CB-4160-{div}{branch}", "power", f"4160 bus feeder {div}{branch}."),
                    edge(f"CB-4160-{div}{branch}", f"TR-480-{div}{branch}", "power", f"CB-4160-{div}{branch} feeds TR-480-{div}{branch}."),
                    edge(f"TR-480-{div}{branch}", f"CB-480-{div}{branch}", "power", f"TR-480-{div}{branch} secondary feeds CB-480-{div}{branch}."),
                    edge(f"CB-480-{div}{branch}", f"BUS-480-{div}{branch}", "power_bus_connection", f"CB-480-{div}{branch} lands on BUS-480-{div}{branch}."),
                ]
            )
        edges.extend(
            [
                edge(f"BUS-480-{div}1", f"BUS-480-{div}2", "power_bus_connection", f"Solid horizontal 480 V bus ties {div}1 and {div}2.", "medium"),
                edge(f"BUS-480-{div}1", f"CB-MCC-{div}1", "power", f"BUS-480-{div}1 drops to CB-MCC-{div}1."),
                edge(f"CB-MCC-{div}1", f"MCC-{div}1", "power", f"CB-MCC-{div}1 feeds MCC-{div}1."),
                edge(f"BUS-480-{div}2", f"CB-MCC-{div}2", "power", f"BUS-480-{div}2 drops to CB-MCC-{div}2."),
                edge(f"CB-MCC-{div}2", f"MCC-{div}2", "power", f"CB-MCC-{div}2 feeds MCC-{div}2."),
                edge(f"BUS-480-{div}2", f"RECT-125-{div}", "rectifier_ac_feed", f"BUS-480-{div}2 branch feeds RECT-125-{div}."),
                edge(f"RECT-125-{div}", f"PANEL-IC-{div}", "dc_power", f"RECT-125-{div} output conductor passes to PANEL-IC-{div}."),
                edge(f"PANEL-IC-{div}", dc_bus, "dc_bus_connection", f"PANEL-IC-{div} DC conductor continues to {dc_bus}."),
                edge(f"PANEL-IC-{div}", f"GND-{div}", "ground", f"PANEL-IC-{div} has local ground symbol GND-{div}."),
                edge(f"MCC-{div}1", f"PUMP-SI-{div}", "load_feeder", f"MCC-{div}1 left load feeder drops to PUMP-SI-{div}."),
                edge(f"MCC-{div}1", f"PUMP-CCW-{div}", "load_feeder", f"MCC-{div}1 center load feeder drops to PUMP-CCW-{div}."),
                edge(f"MCC-{div}1", f"FAN-HVAC-{div}", "load_feeder", f"MCC-{div}1 right load feeder drops to FAN-HVAC-{div}."),
                edge(f"MCC-{div}2", f"MOV-RHR-{div}", "load_feeder", f"MCC-{div}2 load feeder drops to MOV-RHR-{div}."),
                edge(f"MCC-{div}1", ats, "ats_input_feeder", f"MCC-{div}1 solid ATS feeder continues to {ats}.", "medium"),
                edge(f"MCC-{div}2", f"PANEL-IC-{div}", "control_interlock", f"Dashed interlock from MCC-{div}2 to PANEL-IC-{div}.", "medium"),
            ]
        )
    edges.extend(
        [
            edge("BAT-125A", "BUS-DC-125A", "dc_power", "BAT-125A lands on BUS-DC-125A."),
            edge("BUS-DC-125A", "INV-UPS-A", "dc_power", "BUS-DC-125A feeds INV-UPS-A."),
            edge("INV-UPS-A", "PANEL-RPS-A", "dc_power", "INV-UPS-A output lands on PANEL-RPS-A."),
            edge("ATS-480-A", "PANEL-RPS-A", "ats_output", "ATS-480-A output conductor lands on PANEL-RPS-A.", "medium"),
            edge("BAT-125B", "BUS-DC-125B", "dc_power", "BAT-125B lands on BUS-DC-125B."),
            edge("BUS-DC-125B", "INV-UPS-B", "dc_power", "BUS-DC-125B feeds INV-UPS-B."),
            edge("INV-UPS-B", "PANEL-RPS-B", "dc_power", "INV-UPS-B output lands on PANEL-RPS-B."),
            edge("ATS-480-B", "PANEL-RPS-B", "ats_output", "ATS-480-B output conductor lands on PANEL-RPS-B.", "medium"),
        ]
    )
    seen = set()
    for e in edges:
        key = canon(e["node_a"], e["node_b"])
        if key in seen:
            raise ValueError(f"duplicate final edge: {e['node_a']} -- {e['node_b']}")
        seen.add(key)
    return edges


def assert_edges_valid(nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> None:
    names = {row["node"] for row in nodes}
    missing = sorted({n for e in edges for n in (e["node_a"], e["node_b"]) if n not in names})
    if missing:
        raise ValueError(f"edge endpoint(s) missing from node list: {missing}")


def write_edges(path: Path, edges: list[dict[str, str]]) -> None:
    write_csv(path, edges, ["node_a", "node_b", "edge_kind", "confidence", "evidence"])


def write_matrix(path: Path, node_names: list[str], edges: list[dict[str, str]]) -> None:
    idx = {name: i for i, name in enumerate(node_names)}
    matrix = [[0 for _ in node_names] for _ in node_names]
    for e in edges:
        i = idx[e["node_a"]]
        j = idx[e["node_b"]]
        matrix[i][j] = 1
        matrix[j][i] = 1
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + node_names)
        for name, row in zip(node_names, matrix):
            writer.writerow([name] + row)


def image_tokens_high_detail(path: Path) -> int:
    with Image.open(path) as im:
        w, h = im.size
    scale = min(2048 / max(w, h), 1.0)
    w2, h2 = w * scale, h * scale
    shortest = min(w2, h2)
    if shortest > 768:
        scale2 = 768 / shortest
        w2, h2 = w2 * scale2, h2 * scale2
    return 85 + 170 * math.ceil(w2 / 512) * math.ceil(h2 / 512)


def text_tokens_est(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def file_text_tokens(path: Path) -> int:
    return text_tokens_est(path.read_text(encoding="utf-8", errors="replace"))


def write_local_artifact_token_counts() -> None:
    rows = []
    for path in sorted(BASE.glob("*.csv")) + sorted(RESULTS.glob("diego_*")) + sorted(CODES.glob("*.py")):
        if path.is_file():
            rows.append(
                {
                    "document": DOCUMENT,
                    "iteration": ITERATION,
                    "artifact": str(path.relative_to(BASE)),
                    "modality": "text",
                    "tokens_est": file_text_tokens(path),
                    "method": "ceil(characters/4)",
                }
            )
    for path in sorted(BASE.glob("*.png")) + sorted(CODES.glob("*.png")):
        rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "artifact": str(path.relative_to(BASE)),
                "modality": "image",
                "tokens_est": image_tokens_high_detail(path),
                "method": "85 + 170 per 512 tile after OpenAI high-detail scaling",
            }
        )
    write_csv(
        RESULTS / "local_artifact_token_counts.csv",
        rows,
        ["document", "iteration", "artifact", "modality", "tokens_est", "method"],
    )


def write_model_usage_estimates() -> None:
    full_images = [
        BASE / "raw -- synthetic_npp_electrical_schematic_relocated_names.png",
        BASE / "wire_nodes_overlay.png",
        BASE / "component_labels_banners_overlay.png",
    ]
    crop_images = list(CODES.glob("crop_raw_*.png")) + list(CODES.glob("contrast_crop_raw_*.png"))
    full_image_tokens = sum(image_tokens_high_detail(p) for p in full_images)
    crop_tokens = sum(image_tokens_high_detail(p) for p in crop_images)
    csv_bundle = file_text_tokens(COMPONENTS_CSV) + file_text_tokens(BASE / "wire_nodes.csv")
    diego_bundle = file_text_tokens(DIEGO_NODE_CSV) + file_text_tokens(DIEGO_EDGE_CSV)

    calls = [
        {
            "call_id": "main-01",
            "round": "setup",
            "agent": "Main",
            "description": "Inventory document 11 resources, inspect full images, create evidence crops.",
            "input_tokens_est": full_image_tokens + text_tokens_est("document 11 setup prompt"),
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": full_image_tokens,
            "output_tokens_low": 800,
            "output_tokens_expected": 1500,
            "output_tokens_high": 3000,
            "reasoning_tokens_low": 1500,
            "reasoning_tokens_expected": 4500,
            "reasoning_tokens_high": 9000,
        },
        {
            "call_id": "subagent-01",
            "round": "01",
            "agent": "Diego",
            "description": "High-recall extraction from raw/overlays/crops.",
            "input_tokens_est": full_image_tokens + crop_tokens + csv_bundle,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": full_image_tokens + crop_tokens,
            "output_tokens_low": 6000,
            "output_tokens_expected": 10000,
            "output_tokens_high": 15000,
            "reasoning_tokens_low": 9000,
            "reasoning_tokens_expected": 16000,
            "reasoning_tokens_high": 26000,
        },
        {
            "call_id": "subagent-02",
            "round": "01",
            "agent": "Jennifer",
            "description": "Independent precision orientation from raw/overlays/crops.",
            "input_tokens_est": full_image_tokens + crop_tokens + csv_bundle,
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": full_image_tokens + crop_tokens,
            "output_tokens_low": 900,
            "output_tokens_expected": 1800,
            "output_tokens_high": 3200,
            "reasoning_tokens_low": 3500,
            "reasoning_tokens_expected": 8000,
            "reasoning_tokens_high": 14000,
        },
        {
            "call_id": "subagent-03",
            "round": "02",
            "agent": "Jennifer",
            "description": "Precision review of Diego high-recall proposal.",
            "input_tokens_est": diego_bundle + 1300,
            "cached_input_tokens_est": full_image_tokens + crop_tokens,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 1800,
            "output_tokens_expected": 3500,
            "output_tokens_high": 6000,
            "reasoning_tokens_low": 5000,
            "reasoning_tokens_expected": 11000,
            "reasoning_tokens_high": 20000,
        },
        {
            "call_id": "subagent-04",
            "round": "03",
            "agent": "Diego",
            "description": "Saturation check against Jennifer precision rule set.",
            "input_tokens_est": 2200,
            "cached_input_tokens_est": full_image_tokens + crop_tokens + diego_bundle,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 500,
            "output_tokens_expected": 1000,
            "output_tokens_high": 2200,
            "reasoning_tokens_low": 1500,
            "reasoning_tokens_expected": 4000,
            "reasoning_tokens_high": 8000,
        },
        {
            "call_id": "subagent-05",
            "round": "04",
            "agent": "Jennifer",
            "description": "Final confirmation of saturated 120-node/136-edge result.",
            "input_tokens_est": 600,
            "cached_input_tokens_est": full_image_tokens + crop_tokens + diego_bundle,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 300,
            "output_tokens_expected": 600,
            "output_tokens_high": 1400,
            "reasoning_tokens_low": 900,
            "reasoning_tokens_expected": 2200,
            "reasoning_tokens_high": 5000,
        },
        {
            "call_id": "main-02",
            "round": "artifact",
            "agent": "Main",
            "description": "Generate round matrices, validate final matrix, summarize usage.",
            "input_tokens_est": diego_bundle + file_text_tokens(CODES / "generate_connectivity_artifacts.py"),
            "cached_input_tokens_est": 0,
            "image_file_input_tokens_est": 0,
            "output_tokens_low": 700,
            "output_tokens_expected": 1400,
            "output_tokens_high": 2800,
            "reasoning_tokens_low": 1500,
            "reasoning_tokens_expected": 4000,
            "reasoning_tokens_high": 8500,
        },
    ]
    for call in calls:
        call["total_tokens_low"] = call["input_tokens_est"] + call["output_tokens_low"] + call["reasoning_tokens_low"]
        call["total_tokens_expected"] = call["input_tokens_est"] + call["output_tokens_expected"] + call["reasoning_tokens_expected"]
        call["total_tokens_high"] = call["input_tokens_est"] + call["output_tokens_high"] + call["reasoning_tokens_high"]
    rows = []
    for call in calls:
        row = {"document": DOCUMENT, "iteration": ITERATION, "usage_object_available": "no"}
        row.update(call)
        rows.append(row)
    fields = [
        "document",
        "iteration",
        "call_id",
        "round",
        "agent",
        "description",
        "input_tokens_est",
        "cached_input_tokens_est",
        "image_file_input_tokens_est",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_low",
        "reasoning_tokens_expected",
        "reasoning_tokens_high",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "usage_object_available",
    ]
    write_csv(RESULTS / "model_call_usage_estimates.csv", rows, fields)
    totals = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "api_key_available": "no",
        "responses_token_count_endpoint_used": "no_api_key",
        "usage_objects_collected": "not_exposed_by_multi_agent_tool",
        "model_calls_counted": len(rows),
        "total_tokens_low": sum(row["total_tokens_low"] for row in rows),
        "total_tokens_expected": sum(row["total_tokens_expected"] for row in rows),
        "total_tokens_high": sum(row["total_tokens_high"] for row in rows),
        "method": "Local estimate: chars/4 for text plus OpenAI-style high-detail image tile estimate; low/expected/high bands for unknown output and reasoning.",
    }
    write_csv(
        RESULTS / "token_usage_totals_by_document.csv",
        [totals],
        [
            "document",
            "iteration",
            "api_key_available",
            "responses_token_count_endpoint_used",
            "usage_objects_collected",
            "model_calls_counted",
            "total_tokens_low",
            "total_tokens_expected",
            "total_tokens_high",
            "method",
        ],
    )


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    r1_nodes = diego_round1_nodes()
    r1_edges = load_diego_edges()
    final_node_rows = final_nodes()
    final_edge_rows = final_edges()

    assert_edges_valid(r1_nodes, r1_edges)
    assert_edges_valid(final_node_rows, final_edge_rows)

    r1_node_names = [row["node"] for row in r1_nodes]
    final_node_names = [row["node"] for row in final_node_rows]
    write_csv(RESULTS / "nodes.csv", final_node_rows, ["node", "node_kind", "component_type", "source", "evidence"])
    write_csv(RESULTS / "round_01_diego_high_recall_nodes.csv", r1_nodes, ["node", "node_kind", "component_type", "source", "evidence"])

    rounds = [
        ("01", "Diego", "round_01_diego_high_recall", r1_node_names, r1_edges, "High-recall proposal; includes conductor-label nodes and uncertain dashed/global interlocks."),
        ("02", "Jennifer", "round_02_jennifer_precision", final_node_names, final_edge_rows, "Precision review collapsed conductor labels and removed unsupported/global interlocks."),
        ("03", "Diego", "round_03_diego_saturation", final_node_names, final_edge_rows, "Diego saturation check accepted Jennifer precision result."),
        ("04", "Jennifer", "round_04_jennifer_final", final_node_names, final_edge_rows, "Final Jennifer confirmation of saturated result."),
    ]
    summaries = []
    prev = None
    for round_no, agent, basename, names, edges, notes in rounds:
        write_edges(RESULTS / f"{basename}_edges.csv", edges)
        write_matrix(RESULTS / f"{basename}_matrix.csv", names, edges)
        summaries.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "round": round_no,
                "agent": agent,
                "interpretation": basename,
                "node_count": len(names),
                "edge_count": len(edges),
                "delta_edges_from_previous_round": "" if prev is None else len(edges) - prev,
                "edge_kind_counts": "; ".join(f"{k}:{v}" for k, v in sorted(Counter(e["edge_kind"] for e in edges).items())),
                "notes": notes,
            }
        )
        prev = len(edges)
    write_edges(RESULTS / "final_connectivity_edges.csv", final_edge_rows)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", final_node_names, final_edge_rows)

    decisions = []
    accepted = set(ACCEPTED_ADDITIONS)
    for row in read_csv(DIEGO_NODE_CSV):
        name = row["node_name"]
        if name in accepted:
            status = "accepted_final_node"
            reason = "Accepted by Jennifer precision review as durable physical/logical node."
        elif row["action"] == "add":
            status = "collapsed_to_edge_evidence"
            reason = "Printed conductor/feeder/interlock label used as evidence, not a final matrix node."
        else:
            status = "alias_note_only"
            reason = "Alias note retained in review; original component CSV label used in matrix."
        decisions.append(
            {
                "node_name": name,
                "diego_action": row["action"],
                "node_kind": row["node_kind"],
                "final_status": status,
                "reason": reason,
            }
        )
    write_csv(
        RESULTS / "node_addition_decisions.csv",
        decisions,
        ["node_name", "diego_action", "node_kind", "final_status", "reason"],
    )

    r1_edges_by_key = {canon(e["node_a"], e["node_b"]): e for e in r1_edges}
    final_keys = {canon(e["node_a"], e["node_b"]) for e in final_edge_rows}
    rejected = []
    for e in r1_edges:
        if canon(e["node_a"], e["node_b"]) not in final_keys:
            rejected.append(
                {
                    "node_a": e["node_a"],
                    "node_b": e["node_b"],
                    "original_edge_kind": e["edge_kind"],
                    "original_confidence": e["confidence"],
                    "final_status": "excluded_or_collapsed",
                    "reason": "Excluded directly from final matrix; either collapsed through conductor-label node or removed as unsupported/global dashed interlock.",
                }
            )
    write_csv(
        RESULTS / "rejected_or_collapsed_edges.csv",
        rejected,
        ["node_a", "node_b", "original_edge_kind", "original_confidence", "final_status", "reason"],
    )
    write_csv(
        RESULTS / "round_summaries.csv",
        summaries,
        [
            "document",
            "iteration",
            "round",
            "agent",
            "interpretation",
            "node_count",
            "edge_count",
            "delta_edges_from_previous_round",
            "edge_kind_counts",
            "notes",
        ],
    )

    write_local_artifact_token_counts()
    write_model_usage_estimates()
    readme = """# Document 11 Connectivity Extraction

Blind extraction using only resources in `Raw + wires + junctions + OCR`.

- Base component labels: 99
- Accepted added nodes: 21
- Final nodes: 120
- Diego round 1 high-recall nodes/edges: 225 / 253
- Final saturated precision edges: 136
- Final matrix: `final_connectivity_matrix.csv`
- Final edge list: `final_connectivity_edges.csv`

No GT or GT-derived resources were used. No off-the-shelf OCR was used.
Token counts are local estimates because no API key / Responses token-count endpoint was available.
"""
    (RESULTS / "README.md").write_text(readme, encoding="utf-8")
    print(
        f"round1_nodes={len(r1_node_names)} round1_edges={len(r1_edges)} "
        f"final_nodes={len(final_node_names)} final_edges={len(final_edge_rows)} "
        f"kind_counts={dict(Counter(e['edge_kind'] for e in final_edge_rows))}"
    )


if __name__ == "__main__":
    main()
