from __future__ import annotations

import ast
import csv
from collections import Counter
from pathlib import Path

from PIL import Image


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\29")
INPUT_DIR = DOC_ROOT / "Input resources"
ARTIFACT_DIR = DOC_ROOT / "Codes and artifacts"
CROPS_DIR = ARTIFACT_DIR / "inspection_crops"

RAW_IMAGE = INPUT_DIR / "raw -- readable_synthetic_pid_ccw_v3_final.png"
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
        "02_top_left_supply_and_tk101": (250, 250, 1900, 1850),
        "03_top_pump101a_train": (1750, 800, 3300, 1400),
        "04_top_pump101b_train": (1750, 1650, 3300, 2150),
        "05_top_controls_ft101_inj501": (3100, 1050, 4550, 1650),
        "06_top_filters_hx_a_b": (4450, 850, 6550, 2150),
        "07_top_right_hv231_and_sample": (6900, 900, 7800, 1750),
        "08_mid_pressure_temp_control": (2450, 2150, 4300, 2750),
        "09_mid_temp_injection_250": (4850, 2550, 6250, 3150),
        "10_mid_right_pressure401": (6750, 2100, 7850, 2500),
        "11_mid_right_hv241_stack": (7300, 2500, 7850, 3500),
        "12_bottom_left_tk201_pumps": (350, 3450, 2550, 4625),
        "13_bottom_analyzer_mixer": (3000, 3725, 4200, 4200),
        "14_bottom_right_control_panels": (7250, 3600, 8050, 4450),
        "15_bottom_tk301_separator": (5900, 4200, 7600, 5050),
        "16_far_bottom_left_fr101": (700, 4800, 1200, 5350),
        "17_left_full": (0, 0, 3400, height),
        "18_center_full": (3000, 0, 6800, height),
        "19_right_full": (6500, 0, width, height),
        "20_top_full": (0, 0, width, 2250),
        "21_mid_full": (0, 2100, width, 3550),
        "22_bottom_full": (0, 3400, width, height),
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
