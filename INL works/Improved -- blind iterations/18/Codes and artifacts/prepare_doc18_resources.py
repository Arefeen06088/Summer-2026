import csv
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\18")
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
        handle.write("Doc 18 component/label inventory from Input resources only\n")
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

    overview_width = 2600
    overview_height = int(height * overview_width / width)
    for suffix, img in sources:
        img.resize((overview_width, overview_height), Image.Resampling.LANCZOS).save(
            CROPS / f"00_overview_{suffix}.png"
        )

    crops = [
        ("01_top_left_grid_sources", (200, 120, 2100, 900)),
        ("02_top_center_sources_buses", (2000, 120, 4550, 900)),
        ("03_top_right_generator_aux", (4400, 120, 6850, 1000)),
        ("04_upper_left_transformers", (200, 820, 2500, 1650)),
        ("05_upper_center_buses", (2300, 820, 4650, 1700)),
        ("06_upper_right_buses_and_mcc", (4550, 820, 6850, 1750)),
        ("07_middle_left_train_loads", (200, 1550, 2500, 3000)),
        ("08_middle_center_train_loads", (2300, 1550, 4700, 3000)),
        ("09_middle_right_train_loads", (4550, 1550, 6850, 3050)),
        ("10_lower_left_dc_controls", (200, 2850, 2500, 4250)),
        ("11_lower_center_controls", (2300, 2850, 4700, 4250)),
        ("12_lower_right_dc_controls", (4550, 2850, 6850, 4250)),
        ("13_full_working_area", (180, 120, 6850, 4250)),
        ("14_left_half_full", (180, 120, 3600, 4250)),
        ("15_right_half_full", (3350, 120, 6850, 4250)),
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
