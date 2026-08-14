import csv
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\41")
INPUT = ROOT / "Input resources"
ARTIFACTS = ROOT / "Codes and artifacts"
CROPS = ARTIFACTS / "inspection_crops_doc41"

RAW = INPUT / "raw -- synthetic_npp_electrical_schematic(2).png"
OVERLAY = INPUT / "component_and_logical_detection_plus_ocr_overlay.png"
WIRES = INPUT / "wires_mask_overlay.png"
NODES = INPUT / "wire_nodes_overlay.png"
COMPONENTS = INPUT / "component_visual_ocr_labels.csv"

EXCLUDED_COMPONENT_TYPES = {"unit_region"}

MANUAL_COMPONENTS = [
    {
        "name": "GND-1E",
        "type": "ground",
        "bbox": [625, 642, 720, 770],
        "evidence": "raw schematic shows a labeled ground symbol GND-1E tied to TR-1A; OCR did not list it as a component",
    }
]

CROP_BOXES = {
    "full_reference": (0, 0, 4800, 3200),
    "top_4kv_train_a": (250, 245, 2000, 900),
    "top_4kv_tie_train_b": (1900, 245, 3800, 900),
    "middle_transformers_and_480_buses": (250, 900, 3800, 1550),
    "mcc_a_loads": (250, 1450, 2150, 2250),
    "mcc_b_loads": (2100, 1450, 3850, 2250),
    "control_interlocks": (1600, 2100, 3050, 2600),
    "vital_train_a": (300, 2350, 2150, 3050),
    "vital_train_b": (2200, 2350, 3825, 3050),
    "charger_feeds_wide": (250, 1300, 3850, 3050),
}


def parse_bbox(text):
    return [int(float(part.strip())) for part in text.strip()[1:-1].split(",")]


def read_components():
    with COMPONENTS.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return [
        row
        for row in rows
        if row.get("component_type", "").strip() not in EXCLUDED_COMPONENT_TYPES
    ]


def write_inventory(rows):
    output_csv = ARTIFACTS / "component_inventory_doc41.csv"
    fields = [
        "node_name",
        "node_class",
        "component_type",
        "bbox_x1",
        "bbox_y1",
        "bbox_x2",
        "bbox_y2",
        "source",
        "evidence",
    ]
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            x1, y1, x2, y2 = parse_bbox(row["bbox"])
            node_kind = row.get("node_kind", "")
            node_class = "logical_node" if node_kind == "logical_node" else "physical_component"
            writer.writerow(
                {
                    "node_name": row["normalized_label"].strip(),
                    "node_class": node_class,
                    "component_type": row.get("component_type", ""),
                    "bbox_x1": x1,
                    "bbox_y1": y1,
                    "bbox_x2": x2,
                    "bbox_y2": y2,
                    "source": "component_visual_ocr_labels.csv",
                    "evidence": row.get("evidence_description", ""),
                }
            )
        for node in MANUAL_COMPONENTS:
            x1, y1, x2, y2 = node["bbox"]
            writer.writerow(
                {
                    "node_name": node["name"],
                    "node_class": "manual_physical_component",
                    "component_type": node["type"],
                    "bbox_x1": x1,
                    "bbox_y1": y1,
                    "bbox_x2": x2,
                    "bbox_y2": y2,
                    "source": "visual_raw_manual",
                    "evidence": node["evidence"],
                }
            )

    output_md = ARTIFACTS / "component_inventory_doc41.md"
    lines = [
        "# Doc 41 Component and Logical Node Inventory",
        "",
        "Built only from doc 41 input resources plus raw visual label review.",
        "",
        "## Retained OCR Components and Logical Nodes",
    ]
    for row in rows:
        lines.append(
            f"- `{row['normalized_label'].strip()}` ({row.get('component_type', '')}) "
            f"bbox={row['bbox']} node_kind={row.get('node_kind', '')}"
        )
    lines += ["", "## Manual Raw-Visible Components"]
    for node in MANUAL_COMPONENTS:
        lines.append(f"- `{node['name']}` ({node['type']}): {node['evidence']} bbox={tuple(node['bbox'])}")
    lines += [
        "",
        "## Exclusion Policy",
        "- Excluded OCR unit/region boxes such as `CLASS-1E-AC-DC`, `VITAL-POWER-TRAIN-A`, and `VITAL-POWER-TRAIN-B` because they are drawing regions/enclosures, not electrical connectivity nodes.",
        "- Exclude title block, notes, legend/reference drawings, cable labels, row/column coordinates, anonymous wire-node points, and pure wire crossings.",
    ]
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def crop_all(rows):
    CROPS.mkdir(parents=True, exist_ok=True)
    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    wires = Image.open(WIRES).convert("RGB")
    nodes = Image.open(NODES).convert("RGB")
    for name, box in CROP_BOXES.items():
        x0, y0, x1, y1 = box
        raw.crop(box).save(CROPS / f"{name}__raw.png")
        overlay.crop(box).save(CROPS / f"{name}__overlay.png")
        wires.crop(box).save(CROPS / f"{name}__wires_overlay.png")
        nodes.crop(box).save(CROPS / f"{name}__wire_nodes_overlay.png")
        annotated = raw.crop(box)
        draw = ImageDraw.Draw(annotated)
        for row in rows:
            bx1, by1, bx2, by2 = parse_bbox(row["bbox"])
            if bx2 < x0 or bx1 > x1 or by2 < y0 or by1 > y1:
                continue
            label = row["normalized_label"].strip()
            color = (0, 130, 50) if row.get("node_kind") == "logical_node" else (255, 128, 0)
            draw.rectangle((bx1 - x0, by1 - y0, bx2 - x0, by2 - y0), outline=color, width=2)
            draw.text((bx1 - x0, max(0, by1 - y0 - 14)), label, fill=color)
        for node in MANUAL_COMPONENTS:
            bx1, by1, bx2, by2 = node["bbox"]
            if bx2 < x0 or bx1 > x1 or by2 < y0 or by1 > y1:
                continue
            draw.rectangle((bx1 - x0, by1 - y0, bx2 - x0, by2 - y0), outline=(170, 0, 170), width=2)
            draw.text((bx1 - x0, max(0, by1 - y0 - 14)), node["name"], fill=(170, 0, 170))
        annotated.save(CROPS / f"{name}__annotated_raw.png")


def write_summary(rows):
    summary = ARTIFACTS / "input_resource_summary_doc41.txt"
    physical = sum(1 for row in rows if row.get("node_kind") != "logical_node")
    logical = sum(1 for row in rows if row.get("node_kind") == "logical_node")
    lines = [
        "Doc 41 input resource summary",
        "=============================",
        "Primary raw schematic: raw -- synthetic_npp_electrical_schematic(2).png (4800 x 3200)",
        "Matching derived resources: component_visual_ocr_labels.csv, component_and_logical_detection_plus_ocr_overlay.png, wires_mask.png, wires_mask_overlay.png, wire_nodes.csv, wire_nodes_overlay.png",
        f"Retained OCR rows after unit_region exclusion: {len(rows)}",
        f"Retained physical/components from OCR: {physical}",
        f"Retained logical nodes/buses from OCR: {logical}",
        f"Manual physical components from raw: {len(MANUAL_COMPONENTS)}",
        "",
        "Extraction warning: do not use Results/evaluation or any old results as extraction evidence; exclude anonymous wire nodes and region/title/legend text.",
    ]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    rows = read_components()
    write_inventory(rows)
    crop_all(rows)
    write_summary(rows)
    print(f"wrote inventory for {len(rows)} OCR rows + {len(MANUAL_COMPONENTS)} manual components")
    print(f"wrote crops to {CROPS}")


if __name__ == "__main__":
    main()
