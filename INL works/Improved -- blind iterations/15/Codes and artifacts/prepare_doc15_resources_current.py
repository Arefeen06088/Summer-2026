from __future__ import annotations

import csv
import json
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\15")
INPUT_DIR = BASE / "Input resources"
ARTIFACT_DIR = BASE / "Codes and artifacts"
CROP_DIR = ARTIFACT_DIR / "inspection_crops_doc15_current"

COMPONENT_CSV = INPUT_DIR / "component_visual_ocr_labels.csv"
WIRE_NODES_CSV = INPUT_DIR / "wire_nodes.csv"
RAW_IMAGE = INPUT_DIR / "raw -- improved_synthetic_nuclear_electrical_schematic.png"
OVERLAY_IMAGE = INPUT_DIR / "detected_components_and_logical_detection_plus_ocr_overlay.png"
WIRE_OVERLAY_IMAGE = INPUT_DIR / "wire_nodes_overlay.png"

INVENTORY_CSV = ARTIFACT_DIR / "component_inventory_doc15_current.csv"
INVENTORY_MD = ARTIFACT_DIR / "component_inventory_doc15_current.md"
SUMMARY_TXT = ARTIFACT_DIR / "input_resource_summary_doc15_current.txt"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def parse_box(text: str) -> tuple[int, int, int, int]:
    values = json.loads(text)
    return tuple(int(round(v)) for v in values)


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def crop_all() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    raw = Image.open(RAW_IMAGE)
    overlay = Image.open(OVERLAY_IMAGE)
    wire_overlay = Image.open(WIRE_OVERLAY_IMAGE)
    crops = {
        "full_reference": (0, 0, raw.width, raw.height),
        "top_switchyard_sources": (450, 0, 6100, 820),
        "division_a_medium_voltage": (320, 360, 1800, 1500),
        "division_b_medium_voltage": (1800, 360, 3280, 1500),
        "division_c_medium_voltage": (3280, 360, 4760, 1500),
        "division_d_medium_voltage": (4760, 360, 6240, 1500),
        "tie_ab_and_control": (1550, 720, 2120, 1320),
        "tie_cd_and_control": (4520, 720, 5080, 1320),
        "division_a_mcc_loads": (350, 1550, 1760, 2920),
        "division_b_mcc_loads": (1830, 1550, 3240, 2920),
        "division_c_mcc_loads": (3310, 1550, 4720, 2920),
        "division_d_mcc_loads": (4790, 1550, 6200, 2920),
        "division_a_dc_ground": (350, 3120, 1760, 3580),
        "division_b_dc_ground": (1830, 3120, 3240, 3580),
        "division_c_dc_ground": (3310, 3120, 4720, 3580),
        "division_d_dc_ground": (4790, 3120, 6200, 3580),
        "right_legend_notes": (6200, 420, 7240, 3160),
    }
    for name, box in crops.items():
        for suffix, image in (
            ("raw", raw),
            ("overlay", overlay),
            ("wire_nodes_overlay", wire_overlay),
        ):
            image.crop(box).save(CROP_DIR / f"{name}__{suffix}.png")


def build_inventory() -> list[dict[str, str]]:
    rows = read_csv(COMPONENT_CSV)
    inventory: list[dict[str, str]] = []
    for row in rows:
        x1, y1, x2, y2 = parse_box(row["bbox"])
        inventory.append(
            {
                "node_name": row["final_label"],
                "source": "component_visual_ocr_labels.csv",
                "node_kind": row.get("node_kind") or "physical_component",
                "component_type": row.get("component_type", ""),
                "stable_node_id": row.get("stable_node_id", ""),
                "bbox": row["bbox"],
                "centroid": row["centroid"],
                "notes": "physical/OCR component retained from input component CSV",
            }
        )

    # Logical nodes are visually labeled in the input overlay/raw but not listed
    # as rows in component_visual_ocr_labels.csv. These are buses/source nodes,
    # not WN intermediate points or note text.
    visual_components = [
        ("SEQ-1AB", "protective_relay_logic", [710, 1038, 1185, 1210], "visual component in AB tie dashed control path"),
        ("RPS-AC-1", "protective_relay_logic", [710, 1380, 1185, 1555], "visual component in AB tie dashed control path"),
        ("SEQ-2CD", "protective_relay_logic", [3665, 1038, 4145, 1210], "visual component in CD tie dashed control path"),
        ("RPS-AC-2", "protective_relay_logic", [3665, 1380, 4145, 1555], "visual component in CD tie dashed control path"),
    ]
    for i, (name, ctype, bbox, notes) in enumerate(visual_components, start=1):
        x1, y1, x2, y2 = bbox
        inventory.append(
            {
                "node_name": name,
                "source": "visual component from input raw",
                "node_kind": "physical_component",
                "component_type": ctype,
                "stable_node_id": f"VISUAL-CURRENT-{i:04d}",
                "bbox": json.dumps(bbox),
                "centroid": json.dumps([(x1 + x2) / 2, (y1 + y2) / 2]),
                "notes": notes,
            }
        )

    logical_nodes = [
        ("BUS-SWY-1", "bus", [540, 210, 2955, 282], "left top switchyard bus"),
        ("BUS-SWY-2", "bus", [3265, 210, 5955, 282], "right top switchyard bus"),
        ("BUS-NSS-1", "bus", [540, 515, 2955, 585], "normal station service bus 1"),
        ("BUS-NSS-2", "bus", [3265, 515, 5955, 585], "normal station service bus 2"),
        ("BUS-416A", "bus", [540, 845, 1665, 918], "division A 4.16 kV safety bus"),
        ("BUS-416B", "bus", [1940, 845, 3155, 918], "division B 4.16 kV safety bus"),
        ("BUS-416C", "bus", [3420, 845, 4635, 918], "division C 4.16 kV safety bus"),
        ("BUS-416D", "bus", [4900, 845, 6115, 918], "division D 4.16 kV safety bus"),
        ("BUS-480A", "bus", [540, 1400, 1665, 1475], "division A 480 V load-center bus"),
        ("BUS-480B", "bus", [1940, 1400, 3155, 1475], "division B 480 V load-center bus"),
        ("BUS-480C", "bus", [3420, 1400, 4635, 1475], "division C 480 V load-center bus"),
        ("BUS-480D", "bus", [4900, 1400, 6115, 1475], "division D 480 V load-center bus"),
        ("BUS-DC-A", "bus", [760, 3268, 1110, 3318], "division A DC bus"),
        ("BUS-DC-B", "bus", [2240, 3268, 2590, 3318], "division B DC bus"),
        ("BUS-DC-C", "bus", [3720, 3268, 4070, 3318], "division C DC bus"),
        ("BUS-DC-D", "bus", [5200, 3268, 5550, 3318], "division D DC bus"),
    ]
    for i, (name, kind, bbox, notes) in enumerate(logical_nodes, start=1):
        x1, y1, x2, y2 = bbox
        inventory.append(
            {
                "node_name": name,
                "source": "visual logical node from input raw/overlay",
                "node_kind": "logical_" + kind,
                "component_type": kind,
                "stable_node_id": f"LOGICAL-CURRENT-{i:04d}",
                "bbox": json.dumps(bbox),
                "centroid": json.dumps([(x1 + x2) / 2, (y1 + y2) / 2]),
                "notes": notes,
            }
        )
    return inventory


def main() -> None:
    components = read_csv(COMPONENT_CSV)
    wire_nodes = read_csv(WIRE_NODES_CSV)
    crop_all()
    inventory = build_inventory()
    fields = [
        "node_name",
        "source",
        "node_kind",
        "component_type",
        "stable_node_id",
        "bbox",
        "centroid",
        "notes",
    ]
    write_csv(INVENTORY_CSV, inventory, fields)

    with INVENTORY_MD.open("w", encoding="utf-8") as f:
        f.write("# Doc 15 Current Node Inventory\n\n")
        f.write("Built only from doc 15 Input resources. WN-* intermediate wire nodes, title blocks, legends, and note text are excluded.\n\n")
        f.write(f"- Physical/OCR components retained: {len(components)}\n")
        f.write(f"- Added visual logical bus/source nodes: {len(inventory) - len(components)}\n")
        f.write(f"- Total matrix nodes: {len(inventory)}\n\n")
        f.write("| # | node_name | kind | type | source | notes |\n")
        f.write("|---:|---|---|---|---|---|\n")
        for idx, row in enumerate(inventory, start=1):
            f.write(
                f"| {idx} | {row['node_name']} | {row['node_kind']} | {row['component_type']} | "
                f"{row['source']} | {row['notes']} |\n"
            )

    with SUMMARY_TXT.open("w", encoding="utf-8") as f:
        f.write("Doc 15 current input resource summary\n")
        f.write("=====================================\n")
        f.write(f"Raw image: {RAW_IMAGE}\n")
        with Image.open(RAW_IMAGE) as raw:
            f.write(f"Raw dimensions: {raw.width} x {raw.height}\n")
        f.write(f"Component CSV rows: {len(components)}\n")
        f.write(f"Wire nodes CSV rows: {len(wire_nodes)}\n")
        f.write(f"Inventory nodes: {len(inventory)}\n")
        f.write(f"Inspection crops directory: {CROP_DIR}\n")
        f.write("\nNode policy:\n")
        f.write("- Include physical/OCR components from input CSV.\n")
        f.write("- Include visually labeled logical source/bus nodes from the input raw/overlay.\n")
        f.write("- Exclude WN-* wire nodes, title/revision/legend/notes, area labels, and pure crossings.\n")

    print(
        json.dumps(
            {
                "component_rows": len(components),
                "wire_node_rows": len(wire_nodes),
                "inventory_nodes": len(inventory),
                "crop_dir": str(CROP_DIR),
                "inventory_csv": str(INVENTORY_CSV),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
