import ast
import csv
from collections import Counter
from pathlib import Path

from PIL import Image


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\14")
INPUT_DIR = DOC_ROOT / "Input resources"
ARTIFACT_DIR = DOC_ROOT / "Codes and artifacts"
CROP_DIR = ARTIFACT_DIR / "inspection_crops_current"

RAW_IMAGE = INPUT_DIR / "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png"
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
    with WIRE_NODES_CSV.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_component_summaries(components):
    txt_path = ARTIFACT_DIR / "component_labels_list_current.txt"
    csv_path = ARTIFACT_DIR / "component_labels_list_current.csv"
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
        "02_train_a_4160_top": (520, 250, 2850, 1620),
        "03_train_b_4160_top": (3040, 250, 5350, 1620),
        "04_train_a_480_middle": (520, 1580, 2850, 2840),
        "05_train_b_480_middle": (3040, 1580, 5350, 2840),
        "06_panels_and_links": (800, 2550, 5050, 3120),
        "07_dc_ups_train_a": (520, 3000, 2850, 3920),
        "08_dc_ups_train_b": (3040, 3000, 5350, 3920),
        "09_bus_tie_center": (2600, 600, 3340, 3850),
        "10_notes_legend_title": (5260, 250, 6400, 4000),
        "11_top_bus_labels_focus": (620, 560, 5150, 820),
        "12_middle_bus_labels_focus": (620, 1680, 5150, 1880),
        "13_lower_dc_bus_labels_focus": (620, 3400, 5150, 3920),
    }

    sources = [
        (RAW_IMAGE, "raw"),
        (INPUT_DIR / "detected_components_and_logical_detection_plus_ocr_overlay.png", "component_overlay"),
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
    (ARTIFACT_DIR / "input_resource_summary_current.txt").write_text(
        "\n".join(summary) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
