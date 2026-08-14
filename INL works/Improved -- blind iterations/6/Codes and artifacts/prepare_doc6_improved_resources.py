import ast
import csv
from collections import Counter
from pathlib import Path

from PIL import Image


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\6")
INPUT_DIR = DOC_ROOT / "Input resources"
ARTIFACT_DIR = DOC_ROOT / "Codes and artifacts"
CROP_DIR = ARTIFACT_DIR / "inspection_crops_improved"

RAW_IMAGE = INPUT_DIR / "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png"
COMPONENT_CSV = INPUT_DIR / "component_visual_ocr_labels.csv"
WIRE_NODES_CSV = INPUT_DIR / "wire_nodes.csv"


def parse_literal(value):
    if value is None or value == "":
        return None
    return ast.literal_eval(value)


def load_components():
    with COMPONENT_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    components = []
    for row in rows:
        bbox = parse_literal(row.get("bbox"))
        centroid = parse_literal(row.get("centroid"))
        label = row.get("normalized_label") or row.get("final_label")
        components.append(
            {
                "stable_node_id": row.get("stable_node_id", ""),
                "label": label,
                "component_type": row.get("component_type", ""),
                "node_kind": row.get("node_kind", ""),
                "bbox": bbox,
                "centroid": centroid,
                "confidence": row.get("confidence", ""),
            }
        )
    return components


def load_wire_nodes():
    if not WIRE_NODES_CSV.exists():
        return []
    with WIRE_NODES_CSV.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_component_summaries(components):
    txt_path = ARTIFACT_DIR / "component_labels_list_improved.txt"
    csv_path = ARTIFACT_DIR / "component_labels_list_improved.csv"
    with txt_path.open("w", encoding="utf-8") as handle:
        for comp in components:
            bbox = comp["bbox"]
            centroid = comp["centroid"]
            handle.write(
                f"{comp['stable_node_id']}\t{comp['label']}\t{comp['component_type']}\t"
                f"centroid=({centroid[0]:.1f},{centroid[1]:.1f})\t"
                f"bbox={bbox}\n"
            )
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "stable_node_id",
                "label",
                "component_type",
                "node_kind",
                "bbox",
                "centroid",
                "confidence",
            ],
        )
        writer.writeheader()
        writer.writerows(components)


def save_crops(image_path, suffix, crop_boxes):
    image = Image.open(image_path)
    for name, box in crop_boxes.items():
        crop = image.crop(box)
        crop.save(CROP_DIR / f"{name}_{suffix}.png")


def main():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    CROP_DIR.mkdir(parents=True, exist_ok=True)

    raw = Image.open(RAW_IMAGE)
    width, height = raw.size
    components = load_components()
    wire_nodes = load_wire_nodes()
    write_component_summaries(components)

    crop_boxes = {
        "01_full_working_area": (0, 0, width, height),
        "02_top_sources_switchyard": (150, 180, 4700, 900),
        "03_safety_bus_full": (150, 800, 5900, 1700),
        "04_left_480_loads": (150, 1550, 2500, 3050),
        "05_center_6kv_loads": (2350, 1650, 4200, 3050),
        "06_right_480_loads": (3950, 1550, 5900, 3050),
        "07_dc_ups_ground": (1900, 2950, 5200, 4200),
        "08_esfas_controls": (6000, 650, 8800, 2500),
        "09_full_right_controls": (5200, 400, 8850, 3500),
        "10_ground_detail": (1850, 3350, 5250, 4200),
    }

    sources = [
        (RAW_IMAGE, "raw"),
        (INPUT_DIR / "component_and_logical_detection_plus_ocr_overlay.png", "component_overlay"),
        (INPUT_DIR / "detected_components_and_logical_overlay.png", "detected_overlay"),
        (INPUT_DIR / "wire_nodes_overlay.png", "wire_nodes_overlay"),
        (INPUT_DIR / "wires_mask_overlay.png", "wires_mask_overlay"),
        (INPUT_DIR / "wires_mask.png", "wires_mask"),
    ]
    for path, suffix in sources:
        if path.exists():
            save_crops(path, suffix, crop_boxes)

    comp_type_counts = Counter(comp["component_type"] for comp in components)
    wire_type_counts = Counter(row.get("node_type", "") for row in wire_nodes)
    summary = [
        f"raw_image={RAW_IMAGE}",
        f"raw_size={width}x{height}",
        f"component_count={len(components)}",
        f"component_type_counts={dict(comp_type_counts)}",
        f"wire_node_count={len(wire_nodes)}",
        f"wire_node_type_counts={dict(wire_type_counts)}",
        "",
        "crop_boxes:",
    ]
    for name, box in crop_boxes.items():
        summary.append(f"- {name}: {box}")
    (ARTIFACT_DIR / "input_resource_summary_improved.txt").write_text(
        "\n".join(summary) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
