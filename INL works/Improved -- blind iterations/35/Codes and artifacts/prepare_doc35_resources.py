from __future__ import annotations

import ast
import csv
from collections import Counter
from pathlib import Path

from PIL import Image


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\35")
INPUT_DIR = DOC_ROOT / "Input resources"
ARTIFACT_DIR = DOC_ROOT / "Codes and artifacts"
CROPS_DIR = ARTIFACT_DIR / "inspection_crops"

RAW_IMAGE = INPUT_DIR / "raw -- synthetic_pid_ccw_skid_readable_r13.png"
COMPONENT_CSV = INPUT_DIR / "component_visual_ocr_labels.csv"
WIRE_NODES_CSV = INPUT_DIR / "wire_nodes.csv"


def read_components() -> list[dict[str, str]]:
    with COMPONENT_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["bbox_tuple"] = tuple(ast.literal_eval(row["bbox"]))
        row["centroid_tuple"] = tuple(ast.literal_eval(row["centroid"]))
    return rows


def write_component_inventory(rows: list[dict[str, str]]) -> None:
    rows_sorted = sorted(rows, key=lambda r: (r["centroid_tuple"][1], r["centroid_tuple"][0]))
    txt_lines = []
    for row in rows_sorted:
        cx, cy = row["centroid_tuple"]
        txt_lines.append(
            f"{row['final_label']}\t{row['component_type']}\t"
            f"centroid=({cx:.1f},{cy:.1f})\tbbox={row['bbox']}"
        )
    (ARTIFACT_DIR / "component_labels_list.txt").write_text("\n".join(txt_lines) + "\n", encoding="utf-8")

    fields = [
        "final_label",
        "component_type",
        "node_kind",
        "label_source",
        "confidence",
        "bbox",
        "centroid",
        "evidence_description",
    ]
    with (ARTIFACT_DIR / "component_labels_list.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows_sorted:
            writer.writerow({field: row.get(field, "") for field in fields})


def save_crop(image: Image.Image, box: tuple[int, int, int, int], name: str) -> None:
    image.crop(box).save(CROPS_DIR / name)


def write_crops() -> None:
    CROPS_DIR.mkdir(parents=True, exist_ok=True)
    raw = Image.open(RAW_IMAGE).convert("RGB")
    width, height = raw.size

    companions = []
    for name in [
        "detected_components_and_logical_detection_plus_ocr_overlay.png",
        "wires_mask_overlay.png",
        "wire_nodes_overlay.png",
    ]:
        path = INPUT_DIR / name
        if path.exists():
            companions.append((Path(name).stem, Image.open(path).convert("RGB")))

    crop_boxes = {
        "01_full_working_area": (0, 0, width, height),
        "02_upper_left_ia_tank": (350, 650, 2300, 2350),
        "03_upper_service_water": (1900, 900, 3700, 1700),
        "04_upper_a_train": (2300, 1600, 4550, 2400),
        "05_upper_filter_hx_control": (4550, 900, 7050, 2350),
        "06_upper_right_hx_swv": (7000, 850, 9100, 3000),
        "07_middle_b_train": (2300, 2900, 4550, 3700),
        "08_middle_hx_detail": (5200, 2200, 8900, 3600),
        "09_left_tank_controls": (350, 1200, 2300, 3100),
        "10_lower_chemical_tank": (700, 3600, 2300, 5100),
        "11_lower_chemical_pumps": (2200, 3600, 4700, 4700),
        "12_lower_sample_panels": (5500, 3600, 6600, 4550),
        "13_lower_drain_header": (3000, 4650, 7600, 5150),
        "14_bottom_control_bay": (4200, 5000, 8600, 6100),
        "15_left_full": (0, 600, 2500, 5200),
        "16_center_full": (2300, 900, 5400, 5200),
        "17_right_full": (5200, 800, 9300, 5200),
        "18_top_full": (0, 600, 9300, 2400),
        "19_mid_full": (0, 2200, 9300, 3800),
        "20_bottom_full": (0, 3600, 9300, 6200),
    }
    bounded_boxes = {}
    for key, (x1, y1, x2, y2) in crop_boxes.items():
        box = (max(0, x1), max(0, y1), min(width, x2), min(height, y2))
        bounded_boxes[key] = box
        save_crop(raw, box, f"{key}_raw.png")
        for stem, companion in companions:
            save_crop(companion, box, f"{key}_{stem}.png")

    summary_lines = [f"raw_image={RAW_IMAGE}", f"raw_size={width}x{height}", ""]
    summary_lines.append("crop_boxes:")
    for key, box in bounded_boxes.items():
        summary_lines.append(f"- {key}: {box}")
    (ARTIFACT_DIR / "input_resource_summary.txt").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def summarize(rows: list[dict[str, str]]) -> None:
    type_counts = Counter(row["component_type"] for row in rows)
    node_kind_counts = Counter(row["node_kind"] for row in rows)
    with WIRE_NODES_CSV.open(newline="", encoding="utf-8-sig") as handle:
        wire_rows = list(csv.DictReader(handle))
    wire_counts = Counter(row["node_type"] for row in wire_rows)
    lines = [
        f"component_count={len(rows)}",
        f"component_type_counts={dict(sorted(type_counts.items()))}",
        f"node_kind_counts={dict(sorted(node_kind_counts.items()))}",
        f"wire_node_count={len(wire_rows)}",
        f"wire_node_type_counts={dict(sorted(wire_counts.items()))}",
    ]
    (ARTIFACT_DIR / "resource_inventory_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_components()
    write_component_inventory(rows)
    write_crops()
    summarize(rows)
    print(f"wrote artifacts to {ARTIFACT_DIR}")
    print(f"components={len(rows)}")


if __name__ == "__main__":
    main()
