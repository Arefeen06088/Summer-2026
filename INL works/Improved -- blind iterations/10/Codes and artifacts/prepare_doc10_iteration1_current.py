import csv
from collections import Counter
from pathlib import Path

from PIL import Image

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\10")
INPUT = BASE / "Input resources"
ART = BASE / "Codes and artifacts"
RESULTS = BASE / "Results" / "Iteration_1"
CROPS = ART / "inspection_crops_current"

RAW = INPUT / "raw -- synthetic_nuclear_electrical_schematic_layout_labels_clear.png"
OVERLAY = INPUT / "detected_components_and_logical_detection_plus_ocr_overlay.png"
WIRE_OVERLAY = INPUT / "wire_nodes_overlay.png"
WIRE_MASK_OVERLAY = INPUT / "wires_mask_overlay.png"
COMP_CSV = INPUT / "component_visual_ocr_labels.csv"
WIRE_NODES = INPUT / "wire_nodes.csv"

ART.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)
CROPS.mkdir(parents=True, exist_ok=True)


def parse_centroid(text):
    x, y = text.strip("[]").split(",")
    return float(x), float(y)


components = []
with COMP_CSV.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cx, cy = parse_centroid(row["centroid"])
        components.append(
            {
                "node_name": row["final_label"],
                "node_kind": row["node_kind"],
                "component_type": row["component_type"],
                "center_x": f"{cx:.1f}",
                "center_y": f"{cy:.1f}",
                "bbox": row["bbox"],
                "confidence": row["confidence"],
                "evidence": row["evidence_description"],
            }
        )

with (ART / "component_labels_list_current.csv").open("w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "node_name",
        "node_kind",
        "component_type",
        "center_x",
        "center_y",
        "bbox",
        "confidence",
        "evidence",
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(components)

type_counts = Counter(row["component_type"] for row in components)
kind_counts = Counter(row["node_kind"] for row in components)

with (ART / "component_labels_list_current.txt").open("w", encoding="utf-8") as f:
    f.write("Doc 10 current component/OCR inventory derived only from Input resources.\n\n")
    f.write("Counts by node_kind:\n")
    for key, count in sorted(kind_counts.items()):
        f.write(f"- {key}: {count}\n")
    f.write("\nCounts by component_type:\n")
    for key, count in sorted(type_counts.items(), key=lambda item: (-item[1], item[0])):
        f.write(f"- {key}: {count}\n")
    f.write("\nNode list in approximate visual order:\n")
    for row in sorted(components, key=lambda r: (float(r["center_y"]), float(r["center_x"]))):
        f.write(
            f"- {row['node_name']} | {row['component_type']} | "
            f"({row['center_x']}, {row['center_y']}) | {row['bbox']}\n"
        )

wire_count = 0
wire_types = Counter()
with WIRE_NODES.open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        wire_count += 1
        wire_types[row["node_type"]] += 1

summary = [
    "Doc 10 current input-resource summary.",
    "",
    f"Raw image: {RAW.name}",
    f"Canvas size: {Image.open(RAW).size[0]} x {Image.open(RAW).size[1]}",
    f"Component/OCR rows: {len(components)}",
    f"Wire node rows: {wire_count}",
    "Wire node types: " + ", ".join(f"{k}={v}" for k, v in sorted(wire_types.items())),
    "",
    "Important blind-extraction rule: no GT, evaluator output, archived result, or prior matrix was used to create these aids.",
]
(ART / "input_resource_summary_current.txt").write_text("\n".join(summary), encoding="utf-8")

crops = {
    "01_full_raw": (0, 0, 3304, 2176),
    "02_top_source_bus_tie_raw": (60, 80, 2650, 620),
    "03_train_a_switchgear_upper_raw": (80, 420, 1250, 1120),
    "04_train_b_switchgear_upper_raw": (1320, 420, 2480, 1120),
    "05_train_a_lc_mcc_loads_raw": (430, 860, 1180, 1760),
    "06_train_b_lc_mcc_loads_raw": (1660, 860, 2410, 1760),
    "07_train_a_dc_ups_ground_raw": (90, 1450, 1230, 2070),
    "08_train_b_dc_ups_ground_raw": (1320, 1450, 2460, 2070),
    "09_mcr_annunciator_control_bay_raw": (2400, 420, 2710, 1020),
    "10_notes_legend_title_raw": (2640, 90, 3260, 2030),
    "11_train_a_rps_esfas_control_raw": (60, 620, 620, 1500),
    "12_train_b_rps_esfas_control_raw": (1300, 620, 1850, 1500),
    "13_center_separation_crossing_raw": (1140, 530, 1420, 1800),
    "14_train_a_bottom_loads_raw": (420, 1310, 1200, 1745),
    "15_train_b_bottom_loads_raw": (1660, 1310, 2440, 1745),
}

images = {
    "raw": Image.open(RAW),
    "component_overlay": Image.open(OVERLAY),
    "wire_nodes_overlay": Image.open(WIRE_OVERLAY),
    "wires_mask_overlay": Image.open(WIRE_MASK_OVERLAY),
}

for crop_name, box in crops.items():
    for suffix, image in images.items():
        image.crop(box).save(CROPS / f"{crop_name}_{suffix}.png")

print(f"Wrote {ART / 'component_labels_list_current.csv'}")
print(f"Wrote {ART / 'component_labels_list_current.txt'}")
print(f"Wrote {ART / 'input_resource_summary_current.txt'}")
print(f"Wrote crops to {CROPS}")
