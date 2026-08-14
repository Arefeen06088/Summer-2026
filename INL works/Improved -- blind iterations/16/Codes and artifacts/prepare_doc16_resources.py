import csv
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\16")
INPUT = ROOT / "Input resources"
ARTIFACTS = ROOT / "Codes and artifacts"
CROPS = ARTIFACTS / "inspection_crops"

RAW = INPUT / "raw -- synthetic_npp_electrical_schematic_revised(1).png"
OVERLAY = INPUT / "detected_components_and_logical_detection_plus_ocr_overlay.png"
WIRES = INPUT / "wires_mask_overlay.png"
NODES = INPUT / "wire_nodes_overlay.png"
COMPONENTS = INPUT / "component_visual_ocr_labels.csv"


LABEL_CORRECTIONS = {
    "JB-R": {
        "name": "JB-RPS-B3-1B",
        "evidence": "raw zoom crop reads JB-RPS-B3-1B; OCR inventory truncated this junction-box label to JB-R",
    }
}


LOGICAL_NODES = [
    {"name": "BUS-4KV-A", "type": "bus", "bbox": [1335, 352, 2705, 420], "evidence": "named upper 4160 V safety bus"},
    {"name": "BUS-4KV-B", "type": "bus", "bbox": [270, 505, 2705, 575], "evidence": "named lower 4160 V safety bus"},
    {"name": "BUS-480-A", "type": "bus", "bbox": [155, 880, 2850, 935], "evidence": "named upper 480 V load-center bus"},
    {"name": "BUS-480-B", "type": "bus", "bbox": [160, 995, 2850, 1052], "evidence": "lower 480 V load-center bus visually paired with BUS-480-A and tied through CB-TIE-480AB"},
    {"name": "BUS-125DC-A", "type": "bus", "bbox": [525, 2178, 910, 2236], "evidence": "named 125 VDC A vital bus near battery/charger/inverter A"},
    {"name": "BUS-125DC-B", "type": "bus", "bbox": [1995, 2178, 2388, 2236], "evidence": "named 125 VDC B vital bus near battery/charger/inverter B"},
    {"name": "BUS-120-RPS-A", "type": "bus", "bbox": [570, 2390, 1245, 2445], "evidence": "named 120 VAC RPS A bus below INV-120A"},
    {"name": "BUS-120-RPS-B", "type": "bus", "bbox": [2005, 2390, 2640, 2445], "evidence": "named 120 VAC RPS B bus below INV-120B"},
]


MANUAL_COMPONENTS = [
    {
        "name": "DB-RPS-A3-1A",
        "type": "junction_box",
        "bbox": [100, 1900, 270, 2000],
        "evidence": "raw zoom crop reads DB-RPS-A3-1A on the A-side RPS lower box; missed by OCR inventory",
    },
    {
        "name": "UCP-01",
        "type": "control_panel",
        "bbox": [1325, 2305, 1600, 2470],
        "evidence": "raw schematic shows labeled UCP-01 box above GND-NO; missed by OCR inventory",
    }
]


CROP_BOXES = {
    "full_reference": (0, 0, 4087, 2732),
    "top_4kv_sources_buses": (120, 170, 2760, 620),
    "left_480_infeed_and_tie": (640, 560, 1600, 1065),
    "right_480_infeed": (1950, 620, 2220, 1065),
    "mcc_row_left": (150, 1030, 930, 1335),
    "mcc_row_mid_left": (900, 1030, 1580, 1335),
    "mcc_row_mid_right": (1570, 1030, 2240, 1335),
    "mcc_row_right": (2240, 1030, 2945, 1335),
    "selected_safety_loads_a1": (160, 1250, 850, 1710),
    "selected_safety_loads_a2": (850, 1250, 1545, 1710),
    "selected_safety_loads_b1": (1580, 1250, 2245, 1710),
    "selected_safety_loads_b2": (2250, 1250, 2935, 1710),
    "control_protection_a": (120, 1760, 1310, 2185),
    "control_protection_b": (1550, 1760, 2755, 2185),
    "dc_vital_a": (180, 2160, 1250, 2460),
    "dc_vital_b": (1590, 2160, 2660, 2460),
    "ground_and_panel_bottom": (1390, 2450, 3285, 2635),
}


def read_components():
    with COMPONENTS.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return [
        row
        for row in rows
        if row.get("normalized_label", "").strip() != "PP-E1-480-125R"
    ]


def parse_bbox(text):
    return [int(float(part.strip())) for part in text.strip()[1:-1].split(",")]


def corrected_label(row):
    label = row["normalized_label"].strip()
    return LABEL_CORRECTIONS.get(label, {}).get("name", label)


def corrected_evidence(row):
    label = row["normalized_label"].strip()
    evidence = row.get("evidence_description", "")
    correction = LABEL_CORRECTIONS.get(label)
    if correction:
        evidence = f"{evidence} Label correction: {correction['evidence']}."
    return evidence


def write_inventory(rows):
    output_csv = ARTIFACTS / "component_inventory_doc16.csv"
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
            label = corrected_label(row)
            source = "component_visual_ocr_labels.csv"
            if row["normalized_label"].strip() in LABEL_CORRECTIONS:
                source = "component_visual_ocr_labels.csv+visual_raw_label_correction"
            writer.writerow(
                {
                    "node_name": label,
                    "node_class": "physical_component",
                    "component_type": row.get("component_type", ""),
                    "bbox_x1": x1,
                    "bbox_y1": y1,
                    "bbox_x2": x2,
                    "bbox_y2": y2,
                    "source": source,
                    "evidence": corrected_evidence(row),
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
                    "source": "visual_raw_overlay",
                    "evidence": node["evidence"],
                }
            )

    output_md = ARTIFACTS / "component_inventory_doc16.md"
    lines = [
        "# Doc 16 Component and Logical Node Inventory",
        "",
        "Derived only from doc 16 input resources. Physical components use component_visual_ocr_labels.csv; named buses are visually read from the raw/overlay.",
        "",
        "## Physical Components",
    ]
    for row in rows:
        label = corrected_label(row)
        suffix = ""
        if row["normalized_label"].strip() in LABEL_CORRECTIONS:
            suffix = f" corrected from `{row['normalized_label'].strip()}`"
        lines.append(f"- `{label}` ({row.get('component_type', '')}) bbox={row['bbox']}{suffix}")
    lines += ["", "## Manually Read Physical Components"]
    for node in MANUAL_COMPONENTS:
        lines.append(f"- `{node['name']}` ({node['type']}): {node['evidence']} bbox={tuple(node['bbox'])}")
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
    component_boxes = []
    for row in rows:
        x1, y1, x2, y2 = parse_bbox(row["bbox"])
        component_boxes.append((row["normalized_label"], x1, y1, x2, y2))

    for crop_name, box in CROP_BOXES.items():
        for image_name, image in images.items():
            image.crop(box).save(CROPS / f"{crop_name}__{image_name}.png")

        annotated = images["raw"].crop(box).copy()
        draw = ImageDraw.Draw(annotated)
        x0, y0, _, _ = box
        for label, x1, y1, x2, y2 in component_boxes:
            if x2 < box[0] or x1 > box[2] or y2 < box[1] or y1 > box[3]:
                continue
            draw.rectangle((x1 - x0, y1 - y0, x2 - x0, y2 - y0), outline=(255, 128, 0), width=2)
            draw.text((x1 - x0, max(0, y1 - y0 - 14)), label, fill=(0, 70, 180))
        for node in MANUAL_COMPONENTS:
            x1, y1, x2, y2 = node["bbox"]
            if x2 < box[0] or x1 > box[2] or y2 < box[1] or y1 > box[3]:
                continue
            draw.rectangle((x1 - x0, y1 - y0, x2 - x0, y2 - y0), outline=(190, 0, 190), width=2)
            draw.text((x1 - x0, max(0, y1 - y0 - 14)), node["name"], fill=(150, 0, 150))
        for node in LOGICAL_NODES:
            x1, y1, x2, y2 = node["bbox"]
            if x2 < box[0] or x1 > box[2] or y2 < box[1] or y1 > box[3]:
                continue
            draw.rectangle((x1 - x0, y1 - y0, x2 - x0, y2 - y0), outline=(0, 160, 70), width=2)
            draw.text((x1 - x0, max(0, y1 - y0 - 14)), node["name"], fill=(0, 120, 45))
        annotated.save(CROPS / f"{crop_name}__annotated_raw.png")


def write_summary(rows):
    summary = ARTIFACTS / "input_resource_summary_doc16.txt"
    lines = [
        "Doc 16 input resource summary",
        "=============================",
        "Primary raw schematic: raw -- synthetic_npp_electrical_schematic_revised(1).png (4087 x 2732)",
        "Matching derived resources: component_visual_ocr_labels.csv, detected_components_and_logical_detection_plus_ocr_overlay.png, wires_mask.png, wires_mask_overlay.png, wire_nodes.csv, wire_nodes_overlay.png",
        f"Physical component labels from CSV after title-block exclusion: {len(rows)}",
        f"Manual physical components from raw: {len(MANUAL_COMPONENTS)}",
        f"Manual named logical bus labels: {len(LOGICAL_NODES)}",
        "",
        "Logical nodes retained:",
    ]
    for node in LOGICAL_NODES:
        lines.append(f"- {node['name']} ({node['type']}): {node['evidence']}")
    lines.extend(
        [
            "",
            "Extraction warning: exclude note boxes, legend items, title block text, anonymous WN-* wire-node points, line ticks, and pure crossings.",
          "The OCR candidate PP-E1-480-125R is excluded from this inventory because it is title-block/drawing-number text, not a schematic component.",
          "The raw-visible UCP-01 box is added manually because it is a labeled schematic component connected to GND-NO.",
          "The raw-visible DB-RPS-A3-1A box is added manually because OCR missed the A-side RPS lower box label.",
          "The OCR candidate JB-R is retained as a label-corrected physical component named JB-RPS-B3-1B.",
      ]
  )
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    rows = read_components()
    write_inventory(rows)
    crop_all()
    write_summary(rows)
    print(f"wrote inventory for {len(rows)} physical components + {len(MANUAL_COMPONENTS)} manual components + {len(LOGICAL_NODES)} logical nodes")
    print(f"wrote crops to {CROPS}")


if __name__ == "__main__":
    main()
