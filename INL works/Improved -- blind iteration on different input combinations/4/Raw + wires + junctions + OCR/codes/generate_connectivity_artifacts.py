from __future__ import annotations

import csv
import math
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
COMPONENT_CSV = BASE / "component_visual_ocr_labels.csv"
RESULTS.mkdir(parents=True, exist_ok=True)


BUS_NODES = [
    ("BUS-480-RB1", "bus"),
    ("BUS-480-RB2", "bus"),
    ("BUS-480-LCA", "bus"),
    ("BUS-480-LCB", "bus"),
    ("BUS-125DCA", "bus"),
    ("BUS-125DCB", "bus"),
    ("BUS-UPS-A", "bus"),
    ("BUS-UPS-B", "bus"),
]


SOURCE_AND_FEED_PATHS = [
    ["US-345A", "CB-UAT-A", "TR-UAT-1", "CB-IN-A", "BUS-480-RB1"],
    ["EDG-1A", "CB-DG-A", "BUS-480-RB1"],
    ["US-230B", "CB-SAT-B", "TR-SAT-2", "CB-IN-B", "BUS-480-RB2"],
    ["EDG-1B", "CB-DG-B", "BUS-480-RB2"],
    ["BUS-480-RB1", "CB-LC-A", "TR-LC-A", "CB-LC-A2", "BUS-480-LCA"],
    ["BUS-480-RB2", "CB-LC-B", "TR-LC-B", "CB-LC-B2", "BUS-480-LCB"],
]

RB_FEEDER_PATHS = [
    ["BUS-480-RB1", "CB-F101", "OL-F101", "PMP-SI-1A"],
    ["BUS-480-RB2", "CB-F102", "OL-F102", "PMP-RHR-1A"],
    ["BUS-480-RB1", "CB-F103", "OL-F103", "FAN-CTMT-1A"],
    ["BUS-480-RB2", "CB-F104", "OL-F104", "MOV-RC-104"],
    ["BUS-480-RB1", "CB-F105", "OL-F105", "PMP-CCW-1A"],
    ["BUS-480-RB2", "CB-F106", "OL-F106", "MOV-IA-106"],
    ["BUS-480-RB1", "CB-F107", "OL-F107", "FAN-AHU-1A"],
    ["BUS-480-RB2", "CB-F108", "OL-F108", "PMP-CS-1A"],
    ["BUS-480-RB1", "CB-F109", "OL-F109", "MOV-EF-109"],
    ["BUS-480-RB2", "CB-F110", "OL-F110", "HTR-PZR-1"],
    ["BUS-480-RB1", "CB-F111", "OL-F111", "PMP-SI-1B"],
    ["BUS-480-RB2", "CB-F112", "OL-F112", "PMP-RHR-1B"],
    ["BUS-480-RB1", "CB-F113", "OL-F113", "FAN-CTMT-1B"],
    ["BUS-480-RB2", "CB-F114", "OL-F114", "MOV-RC-114"],
    ["BUS-480-RB1", "CB-F115", "OL-F115", "PNL-SPARE-F15"],
]

LC_BRANCH_PATHS = [
    ["BUS-480-LCA", "CB-A201", "OL-201", "PMP-SW-2A"],
    ["BUS-480-LCA", "CB-A202", "OL-202", "PMP-CVC-2A"],
    ["BUS-480-LCA", "CB-A203", "OL-203", "MOV-SI-203"],
    ["BUS-480-LCA", "CB-A204", "OL-204", "FAN-CR-2A"],
    ["BUS-480-LCA", "CB-A205", "OL-205", "HTR-BATT-A"],
    ["BUS-480-LCB", "CB-B206", "OL-206", "PMP-SW-2B"],
    ["BUS-480-LCB", "CB-B207", "OL-207", "PMP-CVC-2B"],
    ["BUS-480-LCB", "CB-B208", "OL-208", "MOV-SI-208"],
    ["BUS-480-LCB", "CB-B209", "OL-209", "PNL-LTG-209"],
]

DC_UPS_PATHS = [
    ["BUS-480-LCB", "CB-CHG-A", "CHG-125A", "BUS-125DCA"],
    ["BUS-125DCA", "BAT-125A"],
    ["BUS-125DCA", "INV-120A", "BUS-UPS-A"],
    ["BUS-UPS-A", "RPS-TRAIN-A"],
    ["BUS-UPS-A", "ESFAS-TRAIN-A"],
    ["BUS-480-LCB", "CB-CHG-B", "CHG-125B", "BUS-125DCB"],
    ["BUS-125DCB", "BAT-125B"],
    ["BUS-125DCB", "INV-120B", "BUS-UPS-B"],
    ["BUS-UPS-B", "RPS-TRAIN-B"],
    ["BUS-UPS-B", "ESFAS-TRAIN-B"],
]

TIE_PATHS_DIEGO_R1 = [
    ["BUS-480-RB1", "CB-TIE-480", "BUS-480-RB2"],
    ["BUS-480-LCA", "CB-LC-TIE", "BUS-480-LCB"],
]

FINAL_CLOSED_PATHS = SOURCE_AND_FEED_PATHS + RB_FEEDER_PATHS + LC_BRANCH_PATHS + DC_UPS_PATHS

ROUNDS = [
    ("round_01_diego", "Diego high-recall: included two physical tie paths as closed/uncertain candidates", FINAL_CLOSED_PATHS + TIE_PATHS_DIEGO_R1),
    ("round_02_jennifer", "Jennifer precision: excluded CB-TIE-480 and normally-open CB-LC-TIE from closed matrix", FINAL_CLOSED_PATHS),
    ("round_03_diego", "Diego revision: agreed with Jennifer tie cleanup", FINAL_CLOSED_PATHS),
    ("round_04_jennifer_final", "Jennifer final: saturated closed solid-power/DC matrix", FINAL_CLOSED_PATHS),
]


def load_nodes() -> list[tuple[str, str, str]]:
    nodes: list[tuple[str, str, str]] = []
    for i, (label, node_type) in enumerate(BUS_NODES, start=1):
        nodes.append((f"N{i:03d}", label, node_type))

    with COMPONENT_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for offset, row in enumerate(reader, start=len(nodes) + 1):
            nodes.append((f"N{offset:03d}", row["final_label"], "component"))
    return nodes


def pairs_from_paths(paths: list[list[str]], labels: set[str]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for path in paths:
        for a, b in zip(path, path[1:]):
            if a not in labels or b not in labels:
                raise ValueError(f"Unknown node in edge: {a!r}, {b!r}")
            pairs.add(tuple(sorted((a, b))))
    return pairs


def write_nodes(nodes: list[tuple[str, str, str]]) -> None:
    with (RESULTS / "nodes.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node_id", "name", "type"])
        writer.writerows(nodes)


def write_matrix(name: str, nodes: list[tuple[str, str, str]], edge_pairs: set[tuple[str, str]]) -> None:
    labels = [label for _, label, _ in nodes]
    matrix = {label: {other: 0 for other in labels} for label in labels}
    for a, b in edge_pairs:
        matrix[a][b] = 1
        matrix[b][a] = 1

    with (RESULTS / f"{name}_matrix.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", *labels])
        for label in labels:
            writer.writerow([label, *[matrix[label][other] for other in labels]])


def write_edge_list(name: str, nodes: list[tuple[str, str, str]], edge_pairs: set[tuple[str, str]]) -> None:
    id_by_label = {label: node_id for node_id, label, _ in nodes}
    with (RESULTS / f"{name}_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["u_id", "u_name", "v_id", "v_name"])
        for a, b in sorted(edge_pairs, key=lambda item: (id_by_label[item[0]], id_by_label[item[1]])):
            writer.writerow([id_by_label[a], a, id_by_label[b], b])


def write_round_summaries(nodes: list[tuple[str, str, str]]) -> None:
    labels = {label for _, label, _ in nodes}
    with (RESULTS / "round_summaries.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["round_file_prefix", "agent", "summary", "included_edge_count"])
        for name, summary, paths in ROUNDS:
            writer.writerow([name, name.split("_", 2)[2], summary, len(pairs_from_paths(paths, labels))])


def write_excluded_metadata() -> None:
    rows = [
        ("physical_tie_excluded_from_final_closed_power", "BUS-480-RB1--CB-TIE-480--BUS-480-RB2", "0", "Physical tie exists, but closed state is not supported by raw drawing"),
        ("normally_open_tie_excluded_from_final_closed_power", "BUS-480-LCA--CB-LC-TIE--BUS-480-LCB", "0", "Note 8 marks CB-LC-TIE normally open"),
        ("signal_excluded_from_final_closed_power", "RPS-TRAIN-A--RELAY-K701", "0", "Dashed control/signal"),
        ("signal_excluded_from_final_closed_power", "ESFAS-TRAIN-A--RELAY-K701", "0", "Dashed control/signal"),
        ("signal_excluded_from_final_closed_power", "RELAY-K701--TB-ESF-A", "0", "Dashed control/signal"),
        ("signal_excluded_from_final_closed_power", "ANN-CP-A--TB-ESF-A", "0", "Dashed SIGA-01"),
        ("signal_excluded_from_final_closed_power", "ANN-CP-A--REC-SER-01", "0", "Dashed SIG-X2"),
        ("signal_excluded_from_final_closed_power", "RPS-TRAIN-B--RELAY-K702", "0", "Dashed control/signal"),
        ("signal_excluded_from_final_closed_power", "ESFAS-TRAIN-B--RELAY-K702", "0", "Dashed control/signal"),
        ("signal_excluded_from_final_closed_power", "RELAY-K702--TB-ESF-B", "0", "Dashed control/signal"),
        ("signal_excluded_from_final_closed_power", "REC-SER-01--TB-ESF-B", "0", "Dashed SIGB-01"),
    ]
    with (RESULTS / "final_excluded_or_nonclosed_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["status", "path", "include_in_final_closed_power_matrix", "reason"])
        writer.writerows(rows)


def image_tokens_high_detail(width: int, height: int) -> int:
    scale = min(2048 / max(width, height), 1.0)
    w = width * scale
    h = height * scale
    if min(w, h) > 768:
        scale2 = 768 / min(w, h)
        w *= scale2
        h *= scale2
    tiles = math.ceil(w / 512) * math.ceil(h / 512)
    return 85 + 170 * tiles


def write_token_estimates() -> None:
    full_image = image_tokens_high_detail(8800, 5734)
    crop_top = image_tokens_high_detail(7450, 1000)
    crop_upper = image_tokens_high_detail(6400, 1350)
    crop_dc = image_tokens_high_detail(3100, 1800)
    crop_left = image_tokens_high_detail(1300, 2900)
    crop_right = image_tokens_high_detail(1200, 2000)
    crop_lc_a = image_tokens_high_detail(2500, 650)
    crop_lc_tie = image_tokens_high_detail(1600, 750)
    crop_taps = image_tokens_high_detail(1600, 850) + image_tokens_high_detail(2400, 850) + image_tokens_high_detail(1900, 850)
    crop_chg = image_tokens_high_detail(1200, 1850)
    crop_lc_b = image_tokens_high_detail(550, 1850)

    rows = [
        ["4", "1", "main-agent", "main-aggregate", "orchestration, local visual inspection, artifact generation", 76000, 28000, full_image * 3 + crop_top + crop_upper + crop_dc + crop_left + crop_right + crop_lc_a + crop_lc_tie + crop_taps + crop_chg + crop_lc_b, 2500, 4500, 8500, "Usage object unavailable in Codex; cumulative estimate across main turns"],
        ["4", "1", "Diego", "diego-r1", "high-recall extraction", 5600, 0, full_image * 3 + crop_top + crop_upper + crop_dc + crop_left + crop_right + crop_lc_a + crop_lc_tie, 2500, 4200, 7500, "Prompt plus images; output estimated from returned path proposal"],
        ["4", "1", "Jennifer", "jennifer-r1", "precision review", 6200, 0, full_image * 3 + crop_taps + crop_chg + crop_dc + crop_lc_a + crop_lc_tie + crop_lc_b, 1300, 2300, 4200, "Reviewed Diego proposal plus focused crops"],
        ["4", "1", "Diego", "diego-r2", "narrow cleanup agreement", 550, 400, 0, 150, 300, 700, "Follow-up call in same subagent thread; cached tokens not exposed"],
        ["4", "1", "Jennifer", "jennifer-r2", "final saturation", 450, 350, 0, 120, 220, 450, "Final confirmation call; cached tokens not exposed"],
    ]
    with (RESULTS / "model_call_usage_estimates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "document",
            "iteration",
            "agent",
            "call_id",
            "call_purpose",
            "input_text_tokens_expected",
            "cached_input_tokens_estimate",
            "image_file_tokens_expected",
            "output_tokens_low",
            "output_tokens_expected",
            "output_tokens_high",
            "reasoning_tokens_available",
            "reasoning_tokens_estimate",
            "usage_object_collected",
            "total_tokens_low",
            "total_tokens_expected",
            "total_tokens_high",
            "notes",
        ])
        for r in rows:
            total_low = int(r[5]) + int(r[7]) + int(r[8])
            total_expected = int(r[5]) + int(r[7]) + int(r[9])
            total_high = int(r[5]) + int(r[7]) + int(r[10])
            writer.writerow([*r[:11], "not_exposed", "not_available", "no", total_low, total_expected, total_high, r[11]])

    total_low = sum(int(r[5]) + int(r[7]) + int(r[8]) for r in rows)
    total_expected = sum(int(r[5]) + int(r[7]) + int(r[9]) for r in rows)
    total_high = sum(int(r[5]) + int(r[7]) + int(r[10]) for r in rows)
    with (RESULTS / "token_usage_totals_by_document.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["document", "iteration", "total_tokens_low", "total_tokens_expected", "total_tokens_high", "method"])
        writer.writerow(["4", "1", total_low, total_expected, total_high, "local prompt/output estimates plus chars_div_4 artifact counts and high-detail image tiling estimates; no API key/usage objects; tiktoken encoding download failed local SSL verification"])


def write_local_artifact_token_counts() -> None:
    def count_tokens(text: str) -> tuple[str, int]:
        return "fallback:chars_div_4", round(len(text) / 4)

    files = [
        "final_connectivity_matrix.csv",
        "final_connectivity_edges.csv",
        "round_01_diego_matrix.csv",
        "round_02_jennifer_matrix.csv",
        "round_03_diego_matrix.csv",
        "round_04_jennifer_final_matrix.csv",
        "model_call_usage_estimates.csv",
    ]
    with (RESULTS / "local_artifact_token_counts.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "method", "estimated_text_tokens"])
        for file_name in files:
            text = (RESULTS / file_name).read_text(encoding="utf-8")
            method, token_count = count_tokens(text)
            writer.writerow([file_name, method, token_count])


def write_readme() -> None:
    text = """# Connectivity Extraction Results

Final selected file: `round_04_jennifer_final_matrix.csv`, duplicated as `final_connectivity_matrix.csv`.

Interpretation: closed solid power/DC connectivity. Buses are explicit nodes. `CB-TIE-480`, normally-open `CB-LC-TIE`, and dashed control/signal components are retained as nodes but encoded with 0 closed-power degree unless they also have accepted solid-power edges. Nonclosed/signal paths are listed in `final_excluded_or_nonclosed_edges.csv`.

Token accounting note: no OpenAI API key or model usage object was available. Local tokenizer use was not reliable in this environment, so local text token counts use the transparent `chars_div_4` fallback and image counts use a high-detail tiling estimate.

Rows and columns use the same ordered component/node names. Matrices are symmetric and have zero diagonals.
"""
    (RESULTS / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    nodes = load_nodes()
    labels = {label for _, label, _ in nodes}
    write_nodes(nodes)
    write_round_summaries(nodes)
    write_excluded_metadata()

    for name, _summary, paths in ROUNDS:
        pairs = pairs_from_paths(paths, labels)
        write_matrix(name, nodes, pairs)
        write_edge_list(name, nodes, pairs)

    final_matrix = RESULTS / "round_04_jennifer_final_matrix.csv"
    final_edges = RESULTS / "round_04_jennifer_final_edges.csv"
    (RESULTS / "final_connectivity_matrix.csv").write_text(final_matrix.read_text(encoding="utf-8"), encoding="utf-8")
    (RESULTS / "final_connectivity_edges.csv").write_text(final_edges.read_text(encoding="utf-8"), encoding="utf-8")
    write_token_estimates()
    write_local_artifact_token_counts()
    write_readme()


if __name__ == "__main__":
    main()
