import csv
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\4")
INPUT = ROOT / "Input resources"
ARTIFACTS = ROOT / "Codes and artifacts"
CROPS = ARTIFACTS / "inspection_crops"

RAW = INPUT / "raw -- synthetic_npp_120_component_electrical_schematic.png"
OVERLAY = INPUT / "detected_components_and_logical_overlay.png"
WIRES = INPUT / "wires_mask_overlay.png"
NODES = INPUT / "wire_nodes_overlay.png"
COMPONENTS = INPUT / "component_visual_ocr_labels.csv"


LOGICAL_NODES = [
    {"name": "BUS-480-RB1", "type": "bus", "bbox": [780, 685, 7265, 760], "evidence": "green logical bus label and top thick reactor bus"},
    {"name": "BUS-480-RB2", "type": "bus", "bbox": [835, 960, 7260, 1035], "evidence": "green logical bus label and second thick reactor bus"},
    {"name": "BUS-480-LCA", "type": "bus", "bbox": [820, 3650, 4240, 3730], "evidence": "green logical bus label and lower left load-center bus"},
    {"name": "BUS-480-LCB", "type": "bus", "bbox": [4540, 3650, 7145, 3730], "evidence": "green logical bus label and lower right load-center bus"},
    {"name": "BUS-125DCA", "type": "bus", "bbox": [4930, 2260, 5565, 2330], "evidence": "green 125 VDC bus A label between charger and inverter"},
    {"name": "BUS-UPS-A", "type": "bus", "bbox": [5805, 2260, 6490, 2330], "evidence": "green UPS bus A label between inverter and train A panels"},
    {"name": "BUS-125DCB", "type": "bus", "bbox": [4930, 3015, 5565, 3090], "evidence": "green 125 VDC bus B label between charger and inverter"},
    {"name": "BUS-UPS-B", "type": "bus", "bbox": [5805, 3015, 6490, 3090], "evidence": "green UPS bus B label between inverter and train B panels"},
    {"name": "GND-NG-A", "type": "ground", "bbox": [560, 2760, 750, 2840], "evidence": "green ground node near TR-LC-A neutral grounding"},
    {"name": "GND-NG-B", "type": "ground", "bbox": [7200, 2800, 7375, 2890], "evidence": "green ground node near TR-LC-B neutral grounding"},
]


CROP_BOXES = {
    "full_reference": (0, 0, 8800, 5734),
    "top_left_sources_rb_buses": (300, 230, 2650, 1250),
    "top_right_rb_bus_and_tie": (6200, 610, 7425, 1085),
    "rb_bus_loads_left": (1200, 1050, 3300, 2400),
    "rb_bus_loads_mid": (3200, 1050, 5150, 2400),
    "rb_bus_loads_right": (5050, 1050, 7050, 2400),
    "left_load_center_feed": (600, 2250, 1150, 3900),
    "right_load_center_feed": (6950, 2250, 7400, 3900),
    "dc_ups_a": (4350, 2050, 7100, 2750),
    "dc_ups_b": (4350, 2800, 7100, 3550),
    "bottom_load_center_a": (850, 3950, 3150, 5050),
    "bottom_load_center_b": (4300, 3950, 6000, 5050),
    "lower_bus_tie": (3800, 3600, 4700, 3850),
}


def read_components():
    with COMPONENTS.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_inventory(rows):
    output_csv = ARTIFACTS / "component_inventory_doc4.csv"
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
            writer.writerow(
                {
                    "node_name": row["normalized_label"],
                    "node_class": "physical_component",
                    "component_type": "",
                    "bbox_x1": row["bbox_x1"],
                    "bbox_y1": row["bbox_y1"],
                    "bbox_x2": row["bbox_x2"],
                    "bbox_y2": row["bbox_y2"],
                    "source": "component_visual_ocr_labels.csv",
                    "evidence": row.get("evidence_description", ""),
                }
            )
        for node in LOGICAL_NODES:
            x1, y1, x2, y2 = node["bbox"]
            writer.writerow(
                {
                    "node_name": node["name"],
                    "node_class": "logical_" + node["type"],
                    "component_type": node["type"],
                    "bbox_x1": x1,
                    "bbox_y1": y1,
                    "bbox_x2": x2,
                    "bbox_y2": y2,
                    "source": "visual_overlay/raw",
                    "evidence": node["evidence"],
                }
            )

    output_md = ARTIFACTS / "component_inventory_doc4.md"
    lines = [
        "# Doc 4 Component and Logical Node Inventory",
        "",
        "This inventory is derived only from doc 4 input resources. The 8800x5734 schematic, matching 110-component CSV, wire mask, and wire nodes are used as the doc 4 source set.",
        "",
        "## Physical Components",
    ]
    for row in rows:
        lines.append(f"- `{row['normalized_label']}` bbox=({row['bbox_x1']},{row['bbox_y1']},{row['bbox_x2']},{row['bbox_y2']})")
    lines += ["", "## Visual Logical Nodes"]
    for node in LOGICAL_NODES:
        lines.append(f"- `{node['name']}`: {node['evidence']} bbox={tuple(node['bbox'])}")
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def crop_all():
    CROPS.mkdir(parents=True, exist_ok=True)
    images = {
        "raw": Image.open(RAW).convert("RGB"),
        "overlay": Image.open(OVERLAY).convert("RGB"),
        "wires_overlay": Image.open(WIRES).convert("RGB"),
        "wire_nodes_overlay": Image.open(NODES).convert("RGB"),
    }
    rows = read_components()
    for crop_name, box in CROP_BOXES.items():
        for image_name, image in images.items():
            crop = image.crop(box)
            crop.save(CROPS / f"{crop_name}__{image_name}.png")

        annotated = images["raw"].crop(box).copy()
        draw = ImageDraw.Draw(annotated)
        x0, y0, _, _ = box
        for row in rows:
            x1 = int(float(row["bbox_x1"]))
            y1 = int(float(row["bbox_y1"]))
            x2 = int(float(row["bbox_x2"]))
            y2 = int(float(row["bbox_y2"]))
            if x2 < box[0] or x1 > box[2] or y2 < box[1] or y1 > box[3]:
                continue
            draw.rectangle((x1 - x0, y1 - y0, x2 - x0, y2 - y0), outline=(255, 128, 0), width=3)
            draw.text((x1 - x0, max(0, y1 - y0 - 18)), row["normalized_label"], fill=(0, 80, 180))
        for node in LOGICAL_NODES:
            x1, y1, x2, y2 = node["bbox"]
            if x2 < box[0] or x1 > box[2] or y2 < box[1] or y1 > box[3]:
                continue
            draw.rectangle((x1 - x0, y1 - y0, x2 - x0, y2 - y0), outline=(0, 160, 70), width=3)
            draw.text((x1 - x0, max(0, y1 - y0 - 18)), node["name"], fill=(0, 120, 50))
        annotated.save(CROPS / f"{crop_name}__annotated_raw.png")


def write_summary(rows):
    summary = ARTIFACTS / "input_resource_summary_doc4.txt"
    lines = [
        "Doc 4 input resource summary",
        "============================",
        "Primary raw schematic: raw -- synthetic_npp_120_component_electrical_schematic.png (8800 x 5734)",
        "Matching derived resources: component_visual_ocr_labels.csv, detected_components_and_logical_overlay.png, wires_mask.png, wires_mask_overlay.png, wire_nodes.csv, wire_nodes_overlay.png",
        "Ignored as mismatched aid unless explicitly needed: 5500 x 3362 raw/62-label component_and_logical files, which align with a different mirrored-train drawing.",
        f"Physical component labels retained from matching CSV: {len(rows)}",
        f"Logical buses/grounds manually read from matching overlay/raw: {len(LOGICAL_NODES)}",
        "",
        "Logical nodes:",
    ]
    for node in LOGICAL_NODES:
        lines.append(f"- {node['name']} ({node['type']}): {node['evidence']}")
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    rows = read_components()
    write_inventory(rows)
    crop_all()
    write_summary(rows)
    print(f"wrote inventory for {len(rows)} physical components + {len(LOGICAL_NODES)} logical nodes")
    print(f"wrote crops to {CROPS}")


if __name__ == "__main__":
    main()
