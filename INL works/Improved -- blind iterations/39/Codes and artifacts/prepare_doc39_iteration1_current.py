from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from PIL import Image


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\39")
INPUT_DIR = DOC_ROOT / "Input resources"
ARTIFACT_DIR = DOC_ROOT / "Codes and artifacts"
RESULTS_DIR = DOC_ROOT / "Results" / "Iteration_1"
CROP_DIR = ARTIFACT_DIR / "inspection_crops_current"

RAW = INPUT_DIR / "raw -- npp_schematic_improved_no_overlap.png"
COMPONENT_OVERLAY = INPUT_DIR / "component_and_logical_labels_banners_overlay.png"
WIRES_MASK = INPUT_DIR / "wires_mask.png"
WIRES_OVERLAY = INPUT_DIR / "wires_mask_overlay.png"
WIRE_NODES_OVERLAY = INPUT_DIR / "wire_nodes_overlay.png"
COMPONENTS_CSV = INPUT_DIR / "component_and_logical_visual_ocr_labels.csv"
WIRE_NODES_CSV = INPUT_DIR / "wire_nodes.csv"


def parse_pair(text: str) -> tuple[float, float]:
    left, right = text.strip().strip("[]").split(",", 1)
    return float(left), float(right)


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def crop_all(crops: dict[str, tuple[int, int, int, int]]) -> None:
    images = {
        "raw": RAW,
        "component_overlay": COMPONENT_OVERLAY,
        "wires_mask": WIRES_MASK,
        "wires_mask_overlay": WIRES_OVERLAY,
        "wire_nodes_overlay": WIRE_NODES_OVERLAY,
    }
    for suffix, path in images.items():
        with Image.open(path) as image:
            for name, box in crops.items():
                image.crop(box).save(CROP_DIR / f"{name}_{suffix}.png")


def write_component_lists(rows: list[dict[str, str]]) -> None:
    normalized = []
    for row in rows:
        label = row["normalized_label"].strip()
        cx, cy = parse_pair(row["centroid"])
        normalized.append(
            {
                "node_name": label,
                "node_kind": row.get("node_kind", "").strip(),
                "component_type": row.get("component_type", "").strip(),
                "center_x": f"{cx:.1f}",
                "center_y": f"{cy:.1f}",
                "bbox": row.get("bbox", "").strip(),
                "confidence": row.get("confidence", "").strip(),
                "evidence": row.get("evidence_description", "").strip(),
            }
        )
    normalized.sort(key=lambda r: (float(r["center_y"]), float(r["center_x"]), r["node_name"]))

    csv_path = ARTIFACT_DIR / "component_labels_list_current.csv"
    txt_path = ARTIFACT_DIR / "component_labels_list_current.txt"
    fields = ["node_name", "node_kind", "component_type", "center_x", "center_y", "bbox", "confidence", "evidence"]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(normalized)

    lines = []
    for row in normalized:
        lines.append(
            f"{row['node_name']:18s} | {row['node_kind']:17s} | {row['component_type']:20s} "
            f"| ({row['center_x']}, {row['center_y']}) | {row['bbox']}"
        )
    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CROP_DIR.mkdir(parents=True, exist_ok=True)

    component_rows = read_dicts(COMPONENTS_CSV)
    wire_rows = read_dicts(WIRE_NODES_CSV)
    write_component_lists(component_rows)

    with Image.open(RAW) as raw:
        width, height = raw.size

    crops = {
        "01_full_working_area": (0, 0, width, height),
        "02_division_i_4160_top": (250, 170, 2500, 980),
        "03_division_ii_4160_top": (2500, 170, 4520, 980),
        "04_bus_tie_4160_center": (2100, 650, 3180, 1020),
        "05_left_dc_stack_and_panels": (0, 820, 620, 2520),
        "06_right_dc_stack_and_panels": (4100, 820, 4700, 2520),
        "07_train_a_480_loads": (550, 1180, 2250, 2460),
        "08_train_b_480_loads": (2450, 1180, 4200, 2460),
        "09_bottom_control_room": (1650, 2050, 3940, 2570),
        "10_notes_schedule_title": (4500, 170, 5425, 3150),
        "11_top_bus_label_focus": (260, 780, 4300, 1120),
        "12_480_bus_label_focus": (250, 1450, 4300, 1680),
        "13_left_relay_jb_control": (300, 1800, 2500, 2520),
        "14_right_relay_jb_control": (2850, 1800, 4520, 2520),
    }
    crop_all(crops)

    component_type_counts = Counter(row.get("component_type", "") for row in component_rows)
    node_kind_counts = Counter(row.get("node_kind", "") for row in component_rows)
    wire_node_type_counts = Counter(row.get("node_type", "") for row in wire_rows)
    summary = [
        f"raw_image={RAW}",
        f"raw_size={width}x{height}",
        f"component_or_logical_label_count={len(component_rows)}",
        f"node_kind_counts={dict(node_kind_counts)}",
        f"component_type_counts={dict(component_type_counts)}",
        f"wire_node_count={len(wire_rows)}",
        f"wire_node_type_counts={dict(wire_node_type_counts)}",
        "",
        "crop_boxes:",
    ]
    for name, box in crops.items():
        summary.append(f"- {name}: {box}")
    (ARTIFACT_DIR / "input_resource_summary_current.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
