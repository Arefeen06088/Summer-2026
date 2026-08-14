import csv
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\20")
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
        handle.write("Doc 20 component/label inventory from Input resources only\n")
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
        ("01_top_left_13kv_sources", (260, 120, 1750, 720)),
        ("02_top_center_13kv_tie", (1550, 120, 3350, 760)),
        ("03_top_right_13kv_sources", (3150, 120, 4700, 720)),
        ("04_4160_left", (260, 560, 2350, 1120)),
        ("05_4160_right", (2200, 560, 4700, 1120)),
        ("06_480_load_centers_A_B", (260, 1000, 2600, 1780)),
        ("07_480_load_centers_C_D", (2450, 1000, 4700, 1780)),
        ("08_loads_A_B", (260, 1480, 2600, 2350)),
        ("09_loads_C_D", (2450, 1480, 4700, 2350)),
        ("10_dc_sources_left", (260, 2180, 2300, 2570)),
        ("11_dc_sources_right", (2300, 2180, 4700, 2570)),
        ("12_controls_left", (260, 2470, 2300, 3400)),
        ("13_controls_right", (2300, 2470, 4700, 3400)),
        ("14_full_working_area", (260, 120, 4800, 3400)),
        ("15_left_half_full", (260, 120, 2600, 3400)),
        ("16_right_half_full", (2400, 120, 4800, 3400)),
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
