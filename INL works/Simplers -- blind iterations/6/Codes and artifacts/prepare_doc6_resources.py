import ast
import csv
from collections import Counter
from pathlib import Path

from PIL import Image


DOC_ROOT = Path(r"C:\Asif_all_python_projects\INL\Simplers -- blind iterations\6")
INPUT_DIR = DOC_ROOT / "Input resources"
ARTIFACT_DIR = DOC_ROOT / "Codes and artifacts"
CROP_DIR = ARTIFACT_DIR / "inspection_crops"

RAW_IMAGE = INPUT_DIR / "raw -- synthetic_npp_electrical_schematic(2).png"
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
    txt_path = ARTIFACT_DIR / "component_labels_list.txt"
    csv_path = ARTIFACT_DIR / "component_labels_list.csv"
    with txt_path.open("w", encoding="utf-8") as handle:
        for comp in components:
            bbox = comp["bbox"]
            centroid = comp["centroid"]
            handle.write(
                f"{comp['label']}\t{comp['component_type']}\t"
                f"centroid=({centroid[0]:.1f},{centroid[1]:.1f})\t"
                f"bbox={bbox}\n"
            )
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["label", "component_type", "node_kind", "bbox", "centroid", "confidence"],
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
        "02_top_sources_and_bus": (0, 180, width, 760),
        "03_upper_feeders": (0, 600, width, 1320),
        "04_middle_distribution": (0, 1050, width, 2050),
        "05_lower_distribution": (0, 1850, width, height),
        "06_left_half": (0, 180, 2500, height),
        "07_right_half": (2300, 180, width, height),
        "08_center_controls": (1200, 900, 3600, 2600),
    }

    sources = [
        (RAW_IMAGE, "raw"),
        (INPUT_DIR / "component_and_logical_detection_plus_ocr_overlay.png", "component_overlay"),
        (INPUT_DIR / "wire_nodes_overlay.png", "wire_nodes_overlay"),
        (INPUT_DIR / "wires_mask_overlay.png", "wires_mask_overlay"),
        (INPUT_DIR / "wires_mask.png", "wires_mask"),
    ]
    for path, suffix in sources:
        if path.exists():
            save_crops(path, suffix, crop_boxes)

    comp_type_counts = Counter(comp["component_type"] for comp in components)
    node_kind_counts = Counter(comp["node_kind"] for comp in components)
    wire_type_counts = Counter(row.get("node_type", "") for row in wire_nodes)

    summary = [
        f"raw_image={RAW_IMAGE}",
        f"raw_size={width}x{height}",
        f"component_count={len(components)}",
        f"component_type_counts={dict(comp_type_counts)}",
        f"node_kind_counts={dict(node_kind_counts)}",
        f"wire_node_count={len(wire_nodes)}",
        f"wire_node_type_counts={dict(wire_type_counts)}",
        "",
        "crop_boxes:",
    ]
    for name, box in crop_boxes.items():
        summary.append(f"- {name}: {box}")
    (ARTIFACT_DIR / "input_resource_summary.txt").write_text(
        "\n".join(summary) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
