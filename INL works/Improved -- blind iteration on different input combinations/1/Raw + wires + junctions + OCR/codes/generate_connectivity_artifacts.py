from __future__ import annotations

import csv
import math
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


NODES = [
    ("N001", "BUS-4KV-A", "bus"),
    ("N002", "BUS-4KV-B", "bus"),
    ("N003", "BUS-4KV-C", "bus"),
    ("N004", "BUS-480-A", "bus"),
    ("N005", "BUS-480-B", "bus"),
    ("N006", "BUS-480-C", "bus"),
    ("N007", "BUS-125DC-A", "bus"),
    ("N008", "BUS-125DC-B", "bus"),
    ("N009", "BUS-120AC-A", "bus"),
    ("N010", "BUS-120AC-B", "bus"),
    ("N011", "GRID-345A", "component"),
    ("N012", "SWGR-52A", "component"),
    ("N013", "RAT-1A", "component"),
    ("N014", "MAIN-GEN-1", "component"),
    ("N015", "GCB-1", "component"),
    ("N016", "UAT-1A", "component"),
    ("N017", "EDG-1A", "component"),
    ("N018", "CB-EDG-A", "component"),
    ("N019", "CB-TIE-AB", "component"),
    ("N020", "DS-TIE-AB", "component"),
    ("N021", "GRID-345B", "component"),
    ("N022", "SWGR-52B", "component"),
    ("N023", "RAT-1B", "component"),
    ("N024", "EDG-1B", "component"),
    ("N025", "CB-EDG-B", "component"),
    ("N026", "CB-TIE-BC", "component"),
    ("N027", "DS-TIE-BC", "component"),
    ("N028", "EDG-1C", "component"),
    ("N029", "CB-EDG-C", "component"),
    ("N030", "AAC-GEN-1", "component"),
    ("N031", "CB-AAC-C", "component"),
    ("N032", "CB-4A-01", "component"),
    ("N033", "TR-480A", "component"),
    ("N034", "CB-48A-01", "component"),
    ("N035", "CB-4B-01", "component"),
    ("N036", "TR-480B", "component"),
    ("N037", "CB-48B-01", "component"),
    ("N038", "CB-4C-01", "component"),
    ("N039", "TR-480C", "component"),
    ("N040", "CB-48C-01", "component"),
    ("N041", "CB-P201A", "component"),
    ("N042", "MCC-01A", "component"),
    ("N043", "RELAY-K201A", "component"),
    ("N044", "PUMP-P201A", "component"),
    ("N045", "CB-P202A", "component"),
    ("N046", "MCC-02A", "component"),
    ("N047", "RELAY-K202A", "component"),
    ("N048", "PUMP-P202A", "component"),
    ("N049", "CB-M301A", "component"),
    ("N050", "MCC-03A", "component"),
    ("N051", "RELAY-K301A", "component"),
    ("N052", "MOTOR-FAN301A", "component"),
    ("N053", "CB-V410A", "component"),
    ("N054", "MCC-04A", "component"),
    ("N055", "SOL-V410A", "component"),
    ("N056", "VALVE-V410A", "component"),
    ("N057", "CB-P201B", "component"),
    ("N058", "MCC-01B", "component"),
    ("N059", "RELAY-K201B", "component"),
    ("N060", "PUMP-P201B", "component"),
    ("N061", "CB-P202B", "component"),
    ("N062", "MCC-02B", "component"),
    ("N063", "RELAY-K202B", "component"),
    ("N064", "PUMP-P202B", "component"),
    ("N065", "CB-M301B", "component"),
    ("N066", "MCC-03B", "component"),
    ("N067", "RELAY-K301B", "component"),
    ("N068", "MOTOR-FAN301B", "component"),
    ("N069", "CB-V410B", "component"),
    ("N070", "MCC-04B", "component"),
    ("N071", "SOL-V410B", "component"),
    ("N072", "VALVE-V410B", "component"),
    ("N073", "CB-P501", "component"),
    ("N074", "MCC-05C", "component"),
    ("N075", "RELAY-K501", "component"),
    ("N076", "PUMP-CCW501", "component"),
    ("N077", "CB-M601", "component"),
    ("N078", "MCC-06C", "component"),
    ("N079", "RELAY-K601", "component"),
    ("N080", "MOTOR-HVAC601", "component"),
    ("N081", "CB-V502", "component"),
    ("N082", "MCC-07C", "component"),
    ("N083", "SOL-V502", "component"),
    ("N084", "VALVE-V502", "component"),
    ("N085", "CB-P503", "component"),
    ("N086", "MCC-08C", "component"),
    ("N087", "RELAY-K503", "component"),
    ("N088", "PUMP-SW503", "component"),
    ("N089", "CHG-125A", "component"),
    ("N090", "BAT-125A", "component"),
    ("N091", "INV-120A", "component"),
    ("N092", "PNL-RPS-A", "component"),
    ("N093", "RELAY-UV-A", "component"),
    ("N094", "INSTR-PT-A", "component"),
    ("N095", "CHG-125B", "component"),
    ("N096", "BAT-125B", "component"),
    ("N097", "INV-120B", "component"),
    ("N098", "PNL-RPS-B", "component"),
    ("N099", "RELAY-UV-B", "component"),
    ("N100", "INSTR-PT-B", "component"),
    ("N101", "EXT-4KV-BUS-A-SH2", "external_terminal"),
    ("N102", "EXT-4KV-BUS-B-SH3", "external_terminal"),
    ("N103", "EXT-AAC-BUS-C-SH4", "external_terminal"),
]


CLOSED_PATHS = [
    ["GRID-345A", "SWGR-52A", "RAT-1A", "BUS-4KV-A"],
    ["MAIN-GEN-1", "GCB-1", "UAT-1A", "BUS-4KV-A"],
    ["EDG-1A", "CB-EDG-A", "BUS-4KV-A"],
    ["GRID-345B", "SWGR-52B", "RAT-1B", "BUS-4KV-B"],
    ["EDG-1B", "CB-EDG-B", "BUS-4KV-B"],
    ["EDG-1C", "CB-EDG-C", "BUS-4KV-C"],
    ["AAC-GEN-1", "CB-AAC-C", "BUS-4KV-C"],
    ["BUS-4KV-A", "CB-4A-01", "TR-480A", "CB-48A-01", "BUS-480-A"],
    ["BUS-4KV-B", "CB-4B-01", "TR-480B", "CB-48B-01", "BUS-480-B"],
    ["BUS-4KV-C", "CB-4C-01", "TR-480C", "CB-48C-01", "BUS-480-C"],
    ["BUS-480-A", "CB-P201A", "MCC-01A", "RELAY-K201A", "PUMP-P201A"],
    ["BUS-480-A", "CB-P202A", "MCC-02A", "RELAY-K202A", "PUMP-P202A"],
    ["BUS-480-A", "CB-M301A", "MCC-03A", "RELAY-K301A", "MOTOR-FAN301A"],
    ["BUS-480-A", "CB-V410A", "MCC-04A", "SOL-V410A", "VALVE-V410A"],
    ["BUS-480-B", "CB-P201B", "MCC-01B", "RELAY-K201B", "PUMP-P201B"],
    ["BUS-480-B", "CB-P202B", "MCC-02B", "RELAY-K202B", "PUMP-P202B"],
    ["BUS-480-B", "CB-M301B", "MCC-03B", "RELAY-K301B", "MOTOR-FAN301B"],
    ["BUS-480-B", "CB-V410B", "MCC-04B", "SOL-V410B", "VALVE-V410B"],
    ["BUS-480-C", "CB-P501", "MCC-05C", "RELAY-K501", "PUMP-CCW501"],
    ["BUS-480-C", "CB-M601", "MCC-06C", "RELAY-K601", "MOTOR-HVAC601"],
    ["BUS-480-C", "CB-V502", "MCC-07C", "SOL-V502", "VALVE-V502"],
    ["BUS-480-C", "CB-P503", "MCC-08C", "RELAY-K503", "PUMP-SW503"],
    ["BUS-480-A", "CHG-125A", "BAT-125A", "BUS-125DC-A", "INV-120A", "BUS-120AC-A", "PNL-RPS-A"],
    ["BUS-480-B", "CHG-125B", "BAT-125B", "BUS-125DC-B", "INV-120B", "BUS-120AC-B", "PNL-RPS-B"],
]

EXTERNAL_PATHS = [
    ["BUS-4KV-A", "EXT-4KV-BUS-A-SH2"],
    ["BUS-4KV-B", "EXT-4KV-BUS-B-SH3"],
    ["BUS-4KV-C", "EXT-AAC-BUS-C-SH4"],
]

NORMALLY_OPEN_PATHS = [
    ["BUS-4KV-A", "CB-TIE-AB", "DS-TIE-AB", "BUS-4KV-B"],
    ["BUS-4KV-B", "CB-TIE-BC", "DS-TIE-BC", "BUS-4KV-C"],
    ["BUS-125DC-A", "BUS-125DC-B"],
]

SIGNAL_PATHS = [
    ["PNL-RPS-A", "RELAY-UV-A", "INSTR-PT-A"],
    ["PNL-RPS-B", "RELAY-UV-B", "INSTR-PT-B"],
]


ROUNDS = [
    ("round_01_diego", "Diego high-recall: included normally-open physical tie paths; excluded dashed signals", CLOSED_PATHS + EXTERNAL_PATHS + NORMALLY_OPEN_PATHS),
    ("round_02_jennifer", "Jennifer precision: excluded normally-open ties and dashed signals from closed-power matrix", CLOSED_PATHS + EXTERNAL_PATHS),
    ("round_03_diego", "Diego revision: agreed with Jennifer closed-power interpretation", CLOSED_PATHS + EXTERNAL_PATHS),
    ("round_04_jennifer_final", "Jennifer final: saturated closed-power matrix", CLOSED_PATHS + EXTERNAL_PATHS),
]


def pairs_from_paths(paths: list[list[str]]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    valid = {label for _, label, _ in NODES}
    for path in paths:
        for a, b in zip(path, path[1:]):
            if a not in valid or b not in valid:
                raise ValueError(f"Unknown node in edge: {a!r}, {b!r}")
            pairs.add(tuple(sorted((a, b))))
    return pairs


def write_nodes() -> None:
    with (RESULTS / "nodes.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node_id", "name", "type"])
        writer.writerows(NODES)


def write_matrix(name: str, edge_pairs: set[tuple[str, str]]) -> None:
    labels = [label for _, label, _ in NODES]
    matrix = {label: {other: 0 for other in labels} for label in labels}
    for a, b in edge_pairs:
        matrix[a][b] = 1
        matrix[b][a] = 1

    with (RESULTS / f"{name}_matrix.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", *labels])
        for label in labels:
            writer.writerow([label, *[matrix[label][other] for other in labels]])


def write_edge_list(name: str, edge_pairs: set[tuple[str, str]]) -> None:
    id_by_label = {label: node_id for node_id, label, _ in NODES}
    with (RESULTS / f"{name}_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["u_id", "u_name", "v_id", "v_name"])
        for a, b in sorted(edge_pairs, key=lambda item: (id_by_label[item[0]], id_by_label[item[1]])):
            writer.writerow([id_by_label[a], a, id_by_label[b], b])


def write_round_summaries() -> None:
    with (RESULTS / "round_summaries.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["round_file_prefix", "agent", "summary", "included_edge_count"])
        for name, summary, paths in ROUNDS:
            agent = name.split("_", 2)[2]
            writer.writerow([name, agent, summary, len(pairs_from_paths(paths))])


def write_excluded_metadata() -> None:
    rows = []
    for path in NORMALLY_OPEN_PATHS:
        rows.append(("normally_open_excluded_from_final_closed_power", "--".join(path), "0", "Labeled N.O.; retained as status metadata only"))
    for path in SIGNAL_PATHS:
        rows.append(("signal_excluded_from_final_closed_power", "--".join(path), "0", "Dashed/dotted control/instrumentation, not solid power/DC"))

    with (RESULTS / "final_excluded_or_nonclosed_edges.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["status", "path", "include_in_final_closed_power_matrix", "reason"])
        writer.writerows(rows)


def image_tokens_high_detail(width: int, height: int) -> int:
    # Approximation using the common high-detail tiling rule: 85 base + 170 per 512px tile
    # after scaling to a 2048px max side and 768px shortest side.
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
    full_image = image_tokens_high_detail(4800, 3200)
    crop_top = image_tokens_high_detail(3200, 800)
    crop_dc = image_tokens_high_detail(2600, 1000)
    crop_loads = image_tokens_high_detail(3300, 1700)

    rows = [
        ["1", "1", "main-agent", "main-aggregate", "orchestration plus visual inspection", 65000, 25000, full_image * 4 + crop_top + crop_dc + crop_loads, 2500, 4500, 8000, "Usage object unavailable in Codex; cumulative estimate across main decision turns"],
        ["1", "1", "Diego", "diego-r1", "high-recall extraction", 18500, 0, full_image * 3, 9000, 14000, 22000, "Input estimated from prompt plus copied CSV aids; output estimated from returned node/edge/matrix text"],
        ["1", "1", "Jennifer", "jennifer-r1", "precision review", 4300, 0, full_image * 2 + crop_top + crop_dc, 1800, 2800, 4500, "Reviewed Diego summary plus raw/overlay/crops"],
        ["1", "1", "Diego", "diego-r2", "revision/agreement", 900, 500, 0, 400, 700, 1200, "Follow-up call in same subagent thread; cached tokens not exposed"],
        ["1", "1", "Jennifer", "jennifer-r2", "final saturation", 450, 300, 0, 150, 250, 500, "Final confirmation call; cached tokens not exposed"],
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

    total_expected = sum(int(r[5]) + int(r[7]) + int(r[9]) for r in rows)
    total_low = sum(int(r[5]) + int(r[7]) + int(r[8]) for r in rows)
    total_high = sum(int(r[5]) + int(r[7]) + int(r[10]) for r in rows)
    with (RESULTS / "token_usage_totals_by_document.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["document", "iteration", "total_tokens_low", "total_tokens_expected", "total_tokens_high", "method"])
        writer.writerow(["1", "1", total_low, total_expected, total_high, "local prompt/output estimates plus chars_div_4 artifact counts and high-detail image tiling estimates; no API key/usage objects; tiktoken encoding download failed local SSL verification"])


def write_local_artifact_token_counts() -> None:
    try:
        import tiktoken  # type: ignore

        encoder = tiktoken.get_encoding("o200k_base")

        def count_tokens(text: str) -> tuple[str, int]:
            return "tiktoken:o200k_base", len(encoder.encode(text))

    except Exception:

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

Interpretation: closed solid power/DC connectivity. Off-sheet terminals are included. Normally-open bus/DC ties and dashed/dotted control/instrumentation links are retained only in `final_excluded_or_nonclosed_edges.csv` and are encoded as 0 in the final matrix.

Token accounting note: no OpenAI API key or model usage object was available. Local `tiktoken` was installed, but tokenizer-data download failed SSL verification, so local text token counts use the transparent `chars_div_4` fallback and image counts use a high-detail tiling estimate.

Rows and columns use the same ordered component/node names. Matrices are symmetric and have zero diagonals.
"""
    (RESULTS / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    write_nodes()
    write_round_summaries()
    write_excluded_metadata()
    for name, _summary, paths in ROUNDS:
        pairs = pairs_from_paths(paths)
        write_matrix(name, pairs)
        write_edge_list(name, pairs)

    final_matrix = RESULTS / "round_04_jennifer_final_matrix.csv"
    final_edges = RESULTS / "round_04_jennifer_final_edges.csv"
    (RESULTS / "final_connectivity_matrix.csv").write_text(final_matrix.read_text(encoding="utf-8"), encoding="utf-8")
    (RESULTS / "final_connectivity_edges.csv").write_text(final_edges.read_text(encoding="utf-8"), encoding="utf-8")
    write_token_estimates()
    write_local_artifact_token_counts()
    write_readme()


if __name__ == "__main__":
    main()
