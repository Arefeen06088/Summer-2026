import csv
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\15")
INPUT = BASE / "Input resources"
ARTIFACTS = BASE / "Codes and artifacts"
CROPS = ARTIFACTS / "inspection_crops"


def parse_point(value):
    return tuple(float(x.strip()) for x in value.strip("[]").split(","))


def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    CROPS.mkdir(parents=True, exist_ok=True)

    components_path = INPUT / "component_visual_ocr_labels.csv"
    with components_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    def row_sort(row):
        x, y = parse_point(row["centroid"])
        return (y, x, row["normalized_label"])

    sorted_rows = sorted(rows, key=row_sort)
    labels_txt = ARTIFACTS / "component_labels_list.txt"
    with labels_txt.open("w", encoding="utf-8", newline="") as handle:
        handle.write("Doc 15 component/label inventory from Input resources only\n")
        handle.write("Columns: idx, label, type, kind, centroid, bbox, confidence\n\n")
        for idx, row in enumerate(sorted_rows, 1):
            handle.write(
                f"{idx:03d}\t{row['normalized_label']}\t{row['component_type']}\t"
                f"{row['node_kind']}\t{row['centroid']}\t{row['bbox']}\t"
                f"{row['confidence']}\n"
            )

    labels_csv = ARTIFACTS / "component_labels_list.csv"
    with labels_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "idx",
                "normalized_label",
                "component_type",
                "node_kind",
                "centroid",
                "bbox",
                "confidence",
            ],
        )
        writer.writeheader()
        for idx, row in enumerate(sorted_rows, 1):
            writer.writerow(
                {
                    "idx": idx,
                    "normalized_label": row["normalized_label"],
                    "component_type": row["component_type"],
                    "node_kind": row["node_kind"],
                    "centroid": row["centroid"],
                    "bbox": row["bbox"],
                    "confidence": row["confidence"],
                }
            )

    raw_path = next(INPUT.glob("raw*.png"))
    sources = [
        ("raw", Image.open(raw_path).convert("RGB")),
        (
            "components",
            Image.open(INPUT / "detected_components_and_logical_detection_plus_ocr_overlay.png").convert("RGB"),
        ),
        ("wires", Image.open(INPUT / "wires_mask_overlay.png").convert("RGB")),
        ("wire_nodes", Image.open(INPUT / "wire_nodes_overlay.png").convert("RGB")),
    ]
    width, height = sources[0][1].size

    overview_width = 2400
    overview_height = int(height * overview_width / width)
    for suffix, img in sources:
        img.resize((overview_width, overview_height), Image.Resampling.LANCZOS).save(
            CROPS / f"00_overview_{suffix}.png"
        )

    crops = [
        ("01_top_left_sources_bus_1", (380, 120, 1900, 1040)),
        ("02_top_center_left_bus_tie", (1650, 120, 3600, 1040)),
        ("03_top_center_right_sources", (3300, 120, 5150, 1040)),
        ("04_top_right_bus_and_notes", (4800, 120, 7350, 1650)),
        ("05_div_1_upper_ac", (360, 650, 1880, 2100)),
        ("06_div_1_lower_dc", (360, 1900, 1880, 3450)),
        ("07_div_1_bottom_dc_ground", (360, 3200, 1880, 4050)),
        ("08_div_1b_upper_ac", (1800, 650, 3330, 2100)),
        ("09_div_1b_lower_dc", (1800, 1900, 3330, 4050)),
        ("10_div_2a_upper_ac", (3250, 650, 4780, 2100)),
        ("11_div_2a_lower_dc", (3250, 1900, 4780, 4050)),
        ("12_div_2b_upper_ac", (4700, 650, 6250, 2100)),
        ("13_div_2b_lower_dc", (4700, 1900, 6250, 4050)),
        ("14_full_left_half", (250, 100, 3550, 4100)),
        ("15_full_right_half", (3300, 100, 6500, 4100)),
        ("16_full_power_top", (450, 100, 6100, 1600)),
        ("17_full_loads_controls", (450, 1300, 6200, 3950)),
        ("18_title_block", (5000, 3300, 7450, 4920)),
    ]

    for name, box in crops:
        x1, y1, x2, y2 = box
        x1 = max(0, min(width, x1))
        x2 = max(0, min(width, x2))
        y1 = max(0, min(height, y1))
        y2 = max(0, min(height, y2))
        for suffix, img in sources:
            img.crop((x1, y1, x2, y2)).save(CROPS / f"{name}_{suffix}.png")

    summary = ARTIFACTS / "input_resource_summary.txt"
    with summary.open("w", encoding="utf-8") as handle:
        handle.write(f"raw_image={raw_path.name}\n")
        handle.write(f"raw_size={width}x{height}\n")
        handle.write(f"component_rows={len(rows)}\n")
        for name, box in crops:
            handle.write(f"crop={name} box={box}\n")

    print(f"wrote {labels_txt}")
    print(f"wrote {labels_csv}")
    print(f"wrote crops to {CROPS}")
    print(f"component_rows={len(rows)} image_size={width}x{height}")


if __name__ == "__main__":
    main()
