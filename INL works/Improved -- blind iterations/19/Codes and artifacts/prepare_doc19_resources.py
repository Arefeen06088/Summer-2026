import csv
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\19")
INPUT = BASE / "Input resources"
ARTIFACTS = BASE / "Codes and artifacts"
CROPS = ARTIFACTS / "inspection_crops"


def parse_point(value):
    return tuple(float(x.strip()) for x in value.strip("[]").split(","))


def clamp_box(box, width, height):
    x1, y1, x2, y2 = box
    return (
        max(0, min(width, x1)),
        max(0, min(height, y1)),
        max(0, min(width, x2)),
        max(0, min(height, y2)),
    )


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
        handle.write("Doc 19 component/label inventory from Input resources only\n")
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

    overview_width = 3000
    overview_height = int(height * overview_width / width)
    for suffix, img in sources:
        img.resize((overview_width, overview_height), Image.Resampling.LANCZOS).save(
            CROPS / f"00_overview_{suffix}.png"
        )

    crops = [
        ("01_top_left_sources_4160A", (350, 180, 2350, 920)),
        ("02_top_center_bus_tie", (2200, 180, 4550, 1060)),
        ("03_top_right_sources_4160B", (4550, 180, 7250, 1060)),
        ("04_top_full_switchgear", (350, 180, 7350, 1120)),
        ("05_480_bus_left", (350, 930, 2500, 1480)),
        ("06_480_bus_center_tie", (2250, 900, 4700, 1500)),
        ("07_480_bus_right", (4550, 930, 7350, 1500)),
        ("08_feeder_bank_left", (350, 1120, 2500, 2050)),
        ("09_feeder_bank_center_left", (2250, 1120, 4700, 2050)),
        ("10_feeder_bank_center_right", (4550, 1120, 6400, 2050)),
        ("11_feeder_bank_right", (6250, 1120, 7800, 2050)),
        ("12_loads_left", (350, 1900, 2500, 2860)),
        ("13_loads_center_left", (2250, 1900, 4700, 2860)),
        ("14_loads_center_right", (4550, 1900, 6400, 2860)),
        ("15_loads_right", (6250, 1900, 7800, 2860)),
        ("16_control_lower_left", (350, 3120, 3200, 4100)),
        ("17_control_lower_center", (3000, 3120, 5650, 4100)),
        ("18_control_lower_right", (5450, 3120, 7900, 4100)),
        ("19_full_working_area", (320, 180, 7900, 4100)),
        ("20_left_half_full", (320, 180, 4100, 4100)),
        ("21_right_half_full", (3950, 180, 7900, 4100)),
    ]

    for name, box in crops:
        crop_box = clamp_box(box, width, height)
        for suffix, img in sources:
            img.crop(crop_box).save(CROPS / f"{name}_{suffix}.png")

    summary = ARTIFACTS / "input_resource_summary.txt"
    with summary.open("w", encoding="utf-8") as handle:
        handle.write(f"raw_image={raw_path.name}\n")
        handle.write(f"raw_size={width}x{height}\n")
        handle.write(f"component_rows={len(rows)}\n")
        for name, box in crops:
            handle.write(f"crop={name} box={clamp_box(box, width, height)}\n")

    print(f"wrote {labels_txt}")
    print(f"wrote {labels_csv}")
    print(f"wrote crops to {CROPS}")
    print(f"component_rows={len(rows)} image_size={width}x{height}")


if __name__ == "__main__":
    main()
