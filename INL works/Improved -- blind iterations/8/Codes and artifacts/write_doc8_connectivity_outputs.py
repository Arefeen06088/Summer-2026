import csv
import json
from datetime import datetime, timezone
from pathlib import Path


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\8")
INPUT_DIR = DOC_ROOT / "Input resources"
ARTIFACT_DIR = DOC_ROOT / "Codes and artifacts"
RESULT_DIR = DOC_ROOT / "Results" / "Iteration_1"

TRACKER_DIR = Path(
    r"C:\Users\AREFA\OneDrive - Idaho National Laboratory\Documents\Blind iteration on simples"
    r"\token_usage_estimate_2026-07-06"
)
TRACKER_CSV = TRACKER_DIR / "token_performance_tracking.csv"
TRACKER_NOTES = TRACKER_DIR / "token_performance_tracking_notes.md"

DIEGO_LOG = Path(
    r"C:\Users\AREFA\.codex\sessions\2026\07\12"
    r"\rollout-2026-07-12T16-20-52-019f586b-2e94-74e0-837d-23364424d762.jsonl"
)
JENNIFER_LOG = Path(
    r"C:\Users\AREFA\.codex\sessions\2026\07\12"
    r"\rollout-2026-07-12T16-29-36-019f5873-2ca5-7812-874a-d642533eb5c9.jsonl"
)

COMPONENT_CSV = INPUT_DIR / "component_visual_ocr_labels.csv"
DIEGO_NODES = RESULT_DIR / "proposed_nodes.csv"
DIEGO_HIGH = RESULT_DIR / "accepted_high_confidence_edges.csv"
DIEGO_LOW = RESULT_DIR / "plausible_lower_confidence_edges.csv"

DROP_INPUT_LABELS = {"CB-303"}
BASE_LABEL_MAP = {
    "GND-AJ": "GND-A",
    "NCC-2A1": "MCC-2A1",
    "NCC-2A2": "MCC-2A2",
    "NCC-2B1": "MCC-2B1",
    "NCC-2B2": "MCC-2B2",
    "NCC-2D": "MCC-2D",
}
FINAL_LABEL_MAP = {
    **BASE_LABEL_MAP,
    "MOV-8816A": "MOV-8810A",
    "MOV-8816B": "MOV-8810B",
}

ADDED_PHYSICAL_NODES = [
    ("MCC-2C", "component", "motor_control_center", "missed visible physical component"),
    ("CB-52B", "component", "breaker", "missed visible physical component"),
    ("PN-125B", "component", "panel", "missed visible physical component"),
    ("PUMP-AF-2B", "component", "pump", "missed visible physical component"),
]

BUS_NODES = [
    "BUS-4160-N2A",
    "BUS-4160-N2B",
    "BUS-4160-S2A",
    "BUS-4160-S2B",
    "BUS-480-E2A",
    "BUS-480-E2B",
    "BUS-480-N2A",
    "BUS-480-N2B",
    "BUS-125DC-A",
    "BUS-125DC-B",
    "BUS-120AC-A",
    "BUS-120AC-B",
]


def normalize(label, final_mov_names=True):
    mapping = FINAL_LABEL_MAP if final_mov_names else BASE_LABEL_MAP
    return mapping.get(label, label)


def edge_key(a, b):
    return tuple(sorted((a, b)))


def make_edge(a, b, edge_type="connection", evidence="", source="manual"):
    return {
        "node_a": a,
        "node_b": b,
        "edge_type": edge_type,
        "source": source,
        "evidence": evidence,
    }


def dedupe_edges(edges):
    seen = set()
    clean = []
    for edge in edges:
        a = edge["node_a"]
        b = edge["node_b"]
        if a == b:
            continue
        key = edge_key(a, b)
        if key in seen:
            continue
        seen.add(key)
        clean.append(edge)
    return clean


def build_final_nodes(final_mov_names=True):
    nodes = []
    seen = set()
    with COMPONENT_CSV.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            raw = row["final_label"]
            if raw in DROP_INPUT_LABELS:
                continue
            name = normalize(raw, final_mov_names)
            if name in seen:
                continue
            seen.add(name)
            nodes.append(
                {
                    "node_name": name,
                    "node_class": "component",
                    "subtype": row.get("component_type", ""),
                    "source": f"component_csv:{raw}" if raw == name else f"component_csv_corrected:{raw}",
                }
            )

    for name, node_class, subtype, source in ADDED_PHYSICAL_NODES:
        if name not in seen:
            seen.add(name)
            nodes.append(
                {
                    "node_name": name,
                    "node_class": node_class,
                    "subtype": subtype,
                    "source": source,
                }
            )

    for name in BUS_NODES:
        if name not in seen:
            seen.add(name)
            nodes.append(
                {
                    "node_name": name,
                    "node_class": "logical_node",
                    "subtype": "bus",
                    "source": "explicit named bus in raw schematic",
                }
            )

    return nodes


def read_diego_round1_nodes():
    nodes = []
    seen = set()
    with DIEGO_NODES.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            name = row["node_name"]
            if name in seen:
                continue
            seen.add(name)
            nodes.append(
                {
                    "node_name": name,
                    "node_class": row.get("node_class", ""),
                    "subtype": row.get("subtype", ""),
                    "source": f"diego_round1:{row.get('confidence', '')}",
                }
            )
    return nodes


def read_diego_round1_edges():
    edges = []
    with DIEGO_HIGH.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            edges.append(
                make_edge(
                    row["node_a"],
                    row["node_b"],
                    row.get("edge_type", ""),
                    row.get("evidence", ""),
                    "diego_round1_high_confidence",
                )
            )
    with DIEGO_LOW.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            evidence = row.get("evidence", "")
            reason = row.get("reason_for_lower_confidence", "")
            if reason:
                evidence = f"{evidence} Lower-confidence note: {reason}"
            edges.append(
                make_edge(
                    row["node_a"],
                    row["node_b"],
                    row.get("edge_type", ""),
                    evidence,
                    "diego_round1_plausible_lower_confidence",
                )
            )
    return dedupe_edges(edges)


def read_high_edges(final_mov_names=True):
    edges = []
    with DIEGO_HIGH.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            a = normalize(row["node_a"], final_mov_names)
            b = normalize(row["node_b"], final_mov_names)
            edges.append(
                make_edge(
                    a,
                    b,
                    row.get("edge_type", ""),
                    row.get("evidence", ""),
                    "diego_round1_high_retained_or_reviewed",
                )
            )
    return dedupe_edges(edges)


def reviewed_edges(final_mov_names=True, include_charger_battery=False):
    remove = {
        edge_key("GEN-U2", "2E-100"),
        edge_key("2E-100", "UAT-2A"),
        edge_key("2E-100", "UAT-2B"),
        edge_key("PN-480-A", "FAN-VENT-2A"),
        edge_key("PN-480-B", "PUMP-CHG-2B"),
        edge_key("PN-480-B", "FAN-VENT-2B"),
    }
    edges = [edge for edge in read_high_edges(final_mov_names) if edge_key(edge["node_a"], edge["node_b"]) not in remove]

    mov_a = "MOV-8810A" if final_mov_names else "MOV-8816A"
    mov_b = "MOV-8810B" if final_mov_names else "MOV-8816B"
    additions = [
        make_edge("GEN-U2", "UAT-2A", "power", "Collapsed labeled source run after excluding cable/run label 2E-100.", "jennifer_reviewed"),
        make_edge("GEN-U2", "UAT-2B", "power", "Collapsed labeled source run after excluding cable/run label 2E-100.", "jennifer_reviewed"),
        make_edge("BUS-480-E2A", "DS-480-A", "power_tie", "DS-480-A visually attached to the E2A 480 V tie path.", "jennifer_reviewed"),
        make_edge("DS-480-A", "DS-480-B", "power_tie", "Solid feeder tie between DS-480-A and DS-480-B.", "jennifer_reviewed"),
        make_edge("DS-480-B", "BUS-480-E2B", "power_tie", "DS-480-B visually attached to the E2B 480 V tie path.", "jennifer_reviewed"),
        make_edge("BUS-480-E2A", "GND-A", "ground", "Ground symbol GND-A is tied to the E2A 480 V bus area.", "jennifer_reviewed"),
        make_edge("BUS-480-E2B", "GND-B", "ground", "Ground symbol GND-B is tied to the E2B 480 V bus area.", "jennifer_reviewed"),
        make_edge("BUS-480-E2A", "CHGR-125A", "power", "Charger AC input has its own vertical feed from the E2A 480 V bus path.", "jennifer_reviewed"),
        make_edge("BUS-480-E2B", "CHGR-125B", "power", "Charger AC input has its own vertical feed from the E2B 480 V bus path.", "jennifer_reviewed"),
        make_edge("MCC-2C", "FAN-VENT-2A", "power", "Central load crop shows FAN-VENT-2A on the MCC-2C branch.", "jennifer_reviewed"),
        make_edge("MCC-2D", "PUMP-CHG-2B", "power", "Central/right load crop shows PUMP-CHG-2B on the MCC-2D branch.", "jennifer_reviewed"),
        make_edge("MCC-2D", "FAN-VENT-2B", "power", "Central/right load crop shows FAN-VENT-2B on the MCC-2D branch.", "jennifer_reviewed"),
        make_edge("PN-480-A", mov_a, "power", "Raw label reads MOV-8810A; PN-480-A feeder lands on the MOV branch.", "jennifer_final_label_check"),
        make_edge("PN-480-B", mov_b, "power", "Raw label reads MOV-8810B; PN-480-B feeder lands on the MOV branch.", "jennifer_final_label_check"),
    ]

    signal_edges = [
        ("BUS-4160-S2A", "CT-4160A", "instrument"),
        ("CT-4160A", "RELAY-50/51A", "instrument"),
        ("BUS-4160-S2A", "PT-4160A", "instrument"),
        ("PT-4160A", "RELAY-27A", "instrument"),
        ("RELAY-50/51A", "RELAY-86A", "control"),
        ("RELAY-27A", "RELAY-86A", "control"),
        ("RELAY-86A", "CB-EDG-A", "trip_control"),
        ("BUS-4160-S2B", "CT-4160B", "instrument"),
        ("CT-4160B", "RELAY-50/51B", "instrument"),
        ("BUS-4160-S2B", "PT-4160B", "instrument"),
        ("PT-4160B", "RELAY-27B", "instrument"),
        ("RELAY-50/51B", "RELAY-86B", "control"),
        ("RELAY-27B", "RELAY-86B", "control"),
        ("RELAY-86B", "CB-EDG-B", "trip_control"),
        ("MOV-8801A", "JB-2A1", "control"),
        ("MOV-8802A", "JB-2A1", "control"),
        ("JB-2A1", "RELAY-K1A", "control"),
        ("RELAY-K1A", "CP-ESFAS-A", "control"),
        ("RELAY-K1A", "CP-RPS-A", "control"),
        ("PN-125A", "CP-ESFAS-A", "control_power"),
        ("PN-120A", "CP-RPS-A", "control_power"),
        ("MOV-8801B", "JB-2B1", "control"),
        ("MOV-8802B", "JB-2B1", "control"),
        ("JB-2B1", "RELAY-K1B", "control"),
        ("RELAY-K1B", "CP-ESFAS-B", "control"),
        ("RELAY-K1B", "CP-RPS-B", "control"),
        ("PN-125B", "CP-ESFAS-B", "control_power"),
        ("PN-120B", "CP-RPS-B", "control_power"),
    ]
    additions.extend(
        make_edge(a, b, edge_type, "Dashed/signal terminals are visually supported in raw schematic.", "jennifer_reviewed")
        for a, b, edge_type in signal_edges
    )
    if include_charger_battery:
        additions.extend(
            [
                make_edge("CHGR-125A", "BAT-2A", "dc_link", "Dashed line directly links charger DC output to battery symbol.", "jennifer_final_check"),
                make_edge("CHGR-125B", "BAT-2B", "dc_link", "Dashed line directly links charger DC output to battery symbol.", "jennifer_final_check"),
            ]
        )

    return dedupe_edges(edges + additions)


def write_nodes(path, nodes):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node_name", "node_class", "subtype", "source"])
        writer.writeheader()
        writer.writerows(nodes)


def write_edges(path, edges):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node_a", "node_b", "edge_type", "source", "evidence"])
        writer.writeheader()
        writer.writerows(edges)


def write_matrix(path, nodes, edges):
    names = [node["node_name"] for node in nodes]
    index = {name: i for i, name in enumerate(names)}
    matrix = [[0 for _ in names] for _ in names]
    for edge in edges:
        a = edge["node_a"]
        b = edge["node_b"]
        if a not in index or b not in index:
            continue
        i = index[a]
        j = index[b]
        if i != j:
            matrix[i][j] = 1
            matrix[j][i] = 1

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([""] + names)
        for name, row in zip(names, matrix):
            writer.writerow([name] + row)


def validate(nodes, edges):
    names = [node["node_name"] for node in nodes]
    missing = []
    seen = set()
    duplicate_edges = []
    for edge in edges:
        a = edge["node_a"]
        b = edge["node_b"]
        if a not in names or b not in names:
            missing.append((a, b))
        key = edge_key(a, b)
        if key in seen:
            duplicate_edges.append((a, b))
        seen.add(key)
    return {
        "node_count": len(names),
        "unique_node_count": len(set(names)),
        "edge_count": len(dedupe_edges(edges)),
        "missing_edge_endpoint_count": len(missing),
        "missing_edge_endpoints": missing,
        "duplicate_edge_count": len(duplicate_edges),
        "duplicate_edges": duplicate_edges,
        "diagonal_policy": "all diagonal entries written as 0",
        "symmetric_policy": "all accepted edges written symmetrically",
    }


def materialize_round(prefix, nodes, edges):
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    write_nodes(RESULT_DIR / f"{prefix}_nodes.csv", nodes)
    write_edges(RESULT_DIR / f"{prefix}_edges.csv", edges)
    write_matrix(RESULT_DIR / f"{prefix}_connectivity_matrix.csv", nodes, edges)
    with (RESULT_DIR / f"{prefix}_validation.json").open("w", encoding="utf-8") as handle:
        json.dump(validate(nodes, edges), handle, indent=2)


def append_missing_edge_nodes(nodes, edges):
    names = {node["node_name"] for node in nodes}
    for edge in edges:
        for endpoint in (edge["node_a"], edge["node_b"]):
            if endpoint not in names:
                names.add(endpoint)
                nodes.append(
                    {
                        "node_name": endpoint,
                        "node_class": "round_edge_endpoint",
                        "subtype": "",
                        "source": "added to keep Diego round matrix complete",
                    }
                )
    return nodes


def write_uncertain_candidates():
    rows = [
        ("CB-303", "excluded", "Overlay/OCR artifact in feeder-tie area; no visually supported breaker box."),
        ("2E-100", "excluded", "Cable/source-run label, not a component/bus/ground node."),
        ("DS-480-A -- BUS-480-N2A", "excluded", "Tie line crosses N2A feeder without a visible junction dot."),
        ("DS-480-B -- BUS-480-N2B", "excluded", "Tie line crosses N2B feeder without a visible junction dot."),
        ("MCC-2C -- PUMP-CHG-2A", "excluded", "PUMP-CHG-2A is visually better supported from PN-480-A."),
        ("CB-N1 -- CHGR-125A", "excluded", "Charger AC feed is separate from the CB-N1-to-MCC-2C branch."),
        ("CB-N2 -- CHGR-125B", "excluded", "Charger AC feed is separate from the CB-N2-to-MCC-2D branch."),
        ("direct equipment grounds beyond GND-A/B bus ties", "excluded", "Only the two bus-ground links are visually supported."),
    ]
    with (RESULT_DIR / "final_uncertain_candidates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["candidate", "decision", "reason"])
        writer.writerows(rows)


def write_summary(final_validation):
    text = f"""# Doc 8 Iteration 1 Connectivity Extraction

No ground-truth or evaluator-derived feedback was used. Extraction used only the doc 8 input resources, generated inspection crops, and Diego/Jennifer review rounds.

## Saturated Final

- Final nodes: {final_validation['node_count']}
- Final unique undirected edges: {final_validation['edge_count']}
- Matrix symmetry: enforced by writer
- Diagonal: 0 for all nodes

## Final Node Decisions

- Dropped unsupported OCR/overlay artifact `CB-303`.
- Normalized `GND-AJ` to raw visual label `GND-A`.
- Replaced OCR-bad `NCC-*` labels with raw visual `MCC-*` labels.
- Corrected raw labels `MOV-8816A/B` to `MOV-8810A/B`.
- Added visible physical components missed by OCR: `MCC-2C`, `CB-52B`, `PN-125B`, `PUMP-AF-2B`.
- Added 12 explicit bus nodes and excluded cable/run labels such as `2E-100`.

## Round Trail

- `round_01_diego_*`: Diego high-recall proposal, including plausible lower-confidence candidates.
- `round_01_jennifer_*`: Jennifer precision-refined proposal before final label/DC-link corrections.
- `round_02_diego_*`: Diego agreement with Jennifer's first refinement.
- `round_02_jennifer_*`: Jennifer final correction adding charger-battery links and correcting `MOV-8810A/B`.
- `round_03_diego_*`: Diego final agreement; same matrix as saturated final.

## Final Outputs

- `final_connectivity_matrix.csv`
- `connectivity_matrix.csv`
- `final_edges.csv`
- `final_connectivity_edges.csv`
- `final_connectivity_nodes.csv`
- `final_connectivity_validation.json`
- `final_uncertain_candidates.csv`
"""
    (RESULT_DIR / "final_connectivity_summary.md").write_text(text, encoding="utf-8")


def parse_usage(log_path):
    count = 0
    latest = {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
        "total_tokens": 0,
    }
    with log_path.open(encoding="utf-8") as handle:
        for line in handle:
            if '"type":"token_count"' not in line:
                continue
            payload = json.loads(line)
            usage = payload["payload"]["info"]["total_token_usage"]
            latest = {key: int(usage.get(key, 0)) for key in latest}
            count += 1
    return {"model_calls": count, **latest}


def update_token_tracker(final_validation):
    if not TRACKER_CSV.exists():
        return None

    diego = parse_usage(DIEGO_LOG)
    jennifer = parse_usage(JENNIFER_LOG)
    completed = {
        "model_calls": diego["model_calls"] + jennifer["model_calls"],
        "input_tokens": diego["input_tokens"] + jennifer["input_tokens"],
        "cached_input_tokens": diego["cached_input_tokens"] + jennifer["cached_input_tokens"],
        "output_tokens": diego["output_tokens"] + jennifer["output_tokens"],
        "reasoning_output_tokens": diego["reasoning_output_tokens"] + jennifer["reasoning_output_tokens"],
        "total_tokens": diego["total_tokens"] + jennifer["total_tokens"],
    }

    main_low = 1_250_000
    main_expected = 2_500_000
    main_high = 5_000_000
    workflow_low = completed["total_tokens"] + main_low
    workflow_expected = completed["total_tokens"] + main_expected
    workflow_high = completed["total_tokens"] + main_high

    with TRACKER_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = rows[0].keys() if rows else []
    fieldnames = list(fieldnames)

    rows = [
        row
        for row in rows
        if not (
            row.get("family") == "Improved"
            and row.get("document") == "8"
            and row.get("iteration") == "1"
            and row.get("record_type") == "multi_agent_token_usage_unvalidated_final"
        )
    ]

    row = {field: "" for field in fieldnames}
    row.update(
        {
            "family": "Improved",
            "document": "8",
            "iteration": "1",
            "workflow_label": "Improved doc 8 / Iteration 1",
            "record_type": "multi_agent_token_usage_unvalidated_final",
            "metric_label": "Final connectivity -- unvalidated",
            "metric_agent": "Final",
            "metric_round": "final",
            "is_selected_final_metric": "1",
            "final_metric_selection_basis": "final saturated multi-agent extraction; validation metrics pending",
            "validation_note": "No GT or GT-derived validation metric file used during extraction; metrics intentionally blank pending after-the-fact validation.",
            "actual_multi_agent_model_calls": str(completed["model_calls"]),
            "actual_multi_agent_input_tokens": str(completed["input_tokens"]),
            "actual_multi_agent_cached_input_tokens": str(completed["cached_input_tokens"]),
            "actual_multi_agent_output_tokens": str(completed["output_tokens"]),
            "actual_multi_agent_reasoning_output_tokens": str(completed["reasoning_output_tokens"]),
            "actual_multi_agent_total_tokens": str(completed["total_tokens"]),
            "image_file_input_note": "not separately exposed; included in input_tokens",
            "token_usage_basis": "actual completed subagent Codex token_count logs; live main-agent orchestration/finalization estimated",
            "diego_model_calls": str(diego["model_calls"]),
            "diego_input_tokens": str(diego["input_tokens"]),
            "diego_cached_input_tokens": str(diego["cached_input_tokens"]),
            "diego_output_tokens": str(diego["output_tokens"]),
            "diego_reasoning_output_tokens": str(diego["reasoning_output_tokens"]),
            "diego_total_tokens": str(diego["total_tokens"]),
            "jennifer_model_calls": str(jennifer["model_calls"]),
            "jennifer_input_tokens": str(jennifer["input_tokens"]),
            "jennifer_cached_input_tokens": str(jennifer["cached_input_tokens"]),
            "jennifer_output_tokens": str(jennifer["output_tokens"]),
            "jennifer_reasoning_output_tokens": str(jennifer["reasoning_output_tokens"]),
            "jennifer_total_tokens": str(jennifer["total_tokens"]),
            "data_limitations": "No GT or GT-derived validation metric file used. FP/FN/precision/recall/F1 are intentionally blank until an after-the-fact validation CSV is available. actual_multi_agent_* columns in this row represent completed subagents only; use workflow_*_estimate_total_tokens for total-turn planning.",
            "performance_status": "pending_validation_metrics_no_gt_used_during_extraction",
            "completed_subagent_model_calls": str(completed["model_calls"]),
            "completed_subagent_input_tokens": str(completed["input_tokens"]),
            "completed_subagent_cached_input_tokens": str(completed["cached_input_tokens"]),
            "completed_subagent_output_tokens": str(completed["output_tokens"]),
            "completed_subagent_reasoning_output_tokens": str(completed["reasoning_output_tokens"]),
            "completed_subagent_total_tokens": str(completed["total_tokens"]),
            "main_low_estimate_tokens": str(main_low),
            "main_expected_estimate_tokens": str(main_expected),
            "main_high_estimate_tokens": str(main_high),
            "workflow_low_estimate_total_tokens": str(workflow_low),
            "workflow_expected_estimate_total_tokens": str(workflow_expected),
            "workflow_high_estimate_total_tokens": str(workflow_high),
            "token_update_timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        }
    )
    rows.append(row)

    with TRACKER_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    notes = f"""

## Doc 8 Iteration 1 Update - {datetime.now().date().isoformat()}

Added `Improved doc 8 / Iteration 1` as `record_type=multi_agent_token_usage_unvalidated_final`.

Token status:
- Diego actual completed usage: {diego['model_calls']} calls, {diego['total_tokens']:,} total tokens.
- Jennifer actual completed usage: {jennifer['model_calls']} calls, {jennifer['total_tokens']:,} total tokens.
- Completed subagent total: {completed['model_calls']} calls, {completed['total_tokens']:,} total tokens.
- Main-agent live orchestration/finalization is estimated as low/expected/high = {main_low:,} / {main_expected:,} / {main_high:,} tokens.
- Workflow low/expected/high total estimate = {workflow_low:,} / {workflow_expected:,} / {workflow_high:,} tokens.

Extraction status:
- Final output stored at `{RESULT_DIR}`.
- Saturated final matrix has {final_validation['node_count']} nodes and {final_validation['edge_count']} visually supported unique edges.
- No validation metrics were used during extraction.
- FP/FN/precision/recall/F1 are blank for doc 8 until an after-the-fact validation metrics CSV is available.
"""
    with TRACKER_NOTES.open("a", encoding="utf-8") as handle:
        handle.write(notes)

    return {
        "diego": diego,
        "jennifer": jennifer,
        "completed": completed,
        "workflow_estimates": {
            "low": workflow_low,
            "expected": workflow_expected,
            "high": workflow_high,
        },
    }


def main():
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    round1_diego_edges = read_diego_round1_edges()
    round1_diego_nodes = append_missing_edge_nodes(read_diego_round1_nodes(), round1_diego_edges)
    materialize_round("round_01_diego", round1_diego_nodes, round1_diego_edges)

    round1_jennifer_nodes = build_final_nodes(final_mov_names=False)
    round1_jennifer_edges = reviewed_edges(final_mov_names=False, include_charger_battery=False)
    materialize_round("round_01_jennifer", round1_jennifer_nodes, round1_jennifer_edges)

    materialize_round("round_02_diego", round1_jennifer_nodes, round1_jennifer_edges)

    final_nodes = build_final_nodes(final_mov_names=True)
    final_edges = reviewed_edges(final_mov_names=True, include_charger_battery=True)
    materialize_round("round_02_jennifer", final_nodes, final_edges)
    materialize_round("round_03_diego", final_nodes, final_edges)

    write_nodes(RESULT_DIR / "final_connectivity_nodes.csv", final_nodes)
    write_edges(RESULT_DIR / "final_edges.csv", final_edges)
    write_edges(RESULT_DIR / "final_connectivity_edges.csv", final_edges)
    write_matrix(RESULT_DIR / "final_connectivity_matrix.csv", final_nodes, final_edges)
    write_matrix(RESULT_DIR / "connectivity_matrix.csv", final_nodes, final_edges)

    final_validation = validate(final_nodes, final_edges)
    with (RESULT_DIR / "final_connectivity_validation.json").open("w", encoding="utf-8") as handle:
        json.dump(final_validation, handle, indent=2)

    write_uncertain_candidates()
    write_summary(final_validation)
    token_status = update_token_tracker(final_validation)

    print(json.dumps({"final_validation": final_validation, "token_status": token_status}, indent=2))


if __name__ == "__main__":
    main()
