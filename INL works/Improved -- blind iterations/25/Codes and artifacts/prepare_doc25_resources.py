from __future__ import annotations

import ast
import csv
from collections import Counter
from pathlib import Path

from PIL import Image


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\25")
INPUT_DIR = DOC_ROOT / "Input resources"
ARTIFACT_DIR = DOC_ROOT / "Codes and artifacts"
CROPS_DIR = ARTIFACT_DIR / "inspection_crops"

RAW_IMAGE = INPUT_DIR / "raw -- synthetic_npp_electrical_schematic_revised_v4.png"
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
        "01_top_sources_all": (250, 250, 4850, 850),
        "02_top_train_a_source": (250, 250, 1750, 850),
        "03_top_train_b_source": (1750, 250, 3350, 850),
        "04_top_train_c_source": (3350, 250, 4850, 850),
        "05_4kv_feeders_all": (250, 800, 4850, 1600),
        "06_4kv_train_a": (250, 800, 1750, 1600),
        "07_4kv_train_b": (1750, 800, 3350, 1600),
        "08_4kv_train_c": (3350, 800, 4850, 1600),
        "09_480_mcc_top_all": (250, 1450, 4850, 2800),
        "10_480_mcc_top_train_a": (250, 1450, 1750, 2800),
        "11_480_mcc_top_train_b": (1750, 1450, 3350, 2800),
        "12_480_mcc_top_train_c": (3350, 1450, 4850, 2800),
        "13_480_mcc_bottom_all": (250, 2100, 4850, 3400),
        "14_480_mcc_bottom_train_a": (250, 2100, 1750, 3400),
        "15_480_mcc_bottom_train_b": (1750, 2100, 3350, 3400),
        "16_480_mcc_bottom_train_c": (3350, 2100, 4850, 3400),
        "17_lower_dc_rps_left": (250, 3400, 2500, 4250),
        "18_lower_dc_rps_right": (1300, 3400, 4600, 4250),
        "19_full_working_area": (250, 250, 4900, 4250),
        "20_left_full": (250, 250, 1800, 4250),
        "21_center_full": (1700, 250, 3400, 4250),
        "22_right_full": (3300, 250, 4900, 4250),
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
