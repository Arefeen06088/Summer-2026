import csv
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\21")
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
        handle.write("Doc 21 component/label inventory from Input resources only\n")
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

    overview_width = 2800
    overview_height = int(height * overview_width / width)
    for suffix, img in sources:
        img.resize((overview_width, overview_height), Image.Resampling.LANCZOS).save(
            CROPS / f"00_overview_{suffix}.png"
        )

    crops = [
        ("01_incoming_aux_sources_left", (260, 360, 2100, 1320)),
        ("02_top_4160_switchgear", (1950, 360, 5800, 1420)),
        ("03_top_edg_right_sources", (3900, 360, 5900, 1420)),
        ("04_480_train_a_load_centers", (260, 1350, 3050, 2700)),
        ("05_480_train_b_load_centers", (3000, 1350, 5850, 2700)),
        ("06_480_transformer_tie_area", (1900, 1150, 3850, 2050)),
        ("07_dc_ups_supplies_left", (260, 2620, 3000, 4300)),
        ("08_dc_ups_supplies_center", (1500, 2620, 3800, 4300)),
        ("09_control_logic_ladder", (2950, 2600, 5900, 4300)),
        ("10_control_logic_left_half", (2950, 2600, 4450, 4300)),
        ("11_control_logic_right_half", (4300, 2600, 5900, 4300)),
        ("12_full_working_area", (260, 360, 5900, 4300)),
        ("13_left_half_full", (260, 360, 3150, 4300)),
        ("14_right_half_full", (3000, 360, 5900, 4300)),
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
