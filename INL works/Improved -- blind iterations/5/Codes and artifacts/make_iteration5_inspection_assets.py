from __future__ import annotations

import ast
import csv
from pathlib import Path

from PIL import Image, ImageDraw


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\5")
INPUT = BASE / "Input resources"
OUT = BASE / "Codes and artifacts" / "iteration_5_inspection"

RAW = INPUT / "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png"
OVERLAY = INPUT / "component_and_logical_labels_banners_overlay.png"
WIRE_OVERLAY = INPUT / "wires_mask_overlay.png"
NODES_OVERLAY = INPUT / "wire_nodes_overlay.png"
COMPONENTS = INPUT / "component_visual_ocr_labels.csv"


REGIONS = [
    ("full_topology", (0, 0, 6400, 4200)),
    ("top_switchyard_generation", (0, 0, 6400, 540)),
    ("aux_13kv_and_non1", (0, 420, 6400, 1140)),
    ("safety_train_ab", (0, 900, 3220, 2360)),
    ("safety_train_cd", (3180, 900, 6400, 2360)),
    ("loads_a", (260, 1700, 1740, 3150)),
    ("loads_b", (1750, 1700, 3230, 3150)),
    ("loads_c", (3240, 1700, 4720, 3150)),
    ("loads_d", (4660, 1700, 6150, 3150)),
    ("dc_125_a", (0, 2600, 3230, 3850)),
    ("dc_125_b", (3180, 2600, 6400, 3850)),
    ("dc_and_ups_full", (0, 2860, 6400, 4130)),
    ("ups_48_left", (0, 3220, 3300, 4130)),
    ("ups_48_right", (3100, 3220, 6400, 4130)),
    ("esf_control_bay", (5100, 760, 6280, 2300)),
    ("ground_rail_full", (0, 3380, 6400, 4200)),
    ("ground_left_480ab", (0, 1720, 3230, 4200)),
    ("ground_right_480cd_dc", (3180, 1720, 6400, 4200)),
]


def read_components():
    rows = []
    with COMPONENTS.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row = dict(row)
            row["bbox_tuple"] = tuple(ast.literal_eval(row["bbox"]))
            row["centroid_tuple"] = tuple(ast.literal_eval(row["centroid"]))
            rows.append(row)
    return rows


def save_resized_crop(image: Image.Image, name: str, box, suffix: str, max_width: int = 2200):
    crop = image.crop(box)
    if crop.width > max_width:
        scale = max_width / crop.width
        crop = crop.resize((max_width, int(crop.height * scale)), Image.Resampling.LANCZOS)
    path = OUT / f"{name}_{suffix}.png"
    crop.save(path)
    return path


def make_region_contact_sheet(images, name: str):
    thumbs = []
    for title, img in images:
        scale = min(1.0, 720 / img.width)
        thumb = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (thumb.width, thumb.height + 34), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((8, 8), title, fill=(0, 0, 0))
        canvas.paste(thumb.convert("RGB"), (0, 34))
        thumbs.append(canvas)
    width = sum(t.width for t in thumbs) + 16 * (len(thumbs) - 1)
    height = max(t.height for t in thumbs)
    sheet = Image.new("RGB", (width, height), "white")
    x = 0
    for thumb in thumbs:
        sheet.paste(thumb, (x, 0))
        x += thumb.width + 16
    path = OUT / f"{name}_contact_sheet.png"
    sheet.save(path)
    return path


def make_all_contact_sheet():
    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    wire = Image.open(WIRE_OVERLAY).convert("RGB")
    nodes = Image.open(NODES_OVERLAY).convert("RGB")

    rendered = []
    for name, box in REGIONS:
        rendered.append((name, raw.crop(box)))
        save_resized_crop(raw, name, box, "raw")
        save_resized_crop(overlay, name, box, "labels")
        save_resized_crop(wire, name, box, "wires")
        save_resized_crop(nodes, name, box, "wire_nodes")

    sheets = []
    for name, box in REGIONS:
        sheets.append(
            (
                name,
                [
                    ("raw", raw.crop(box)),
                    ("labels", overlay.crop(box)),
                    ("wires", wire.crop(box)),
                    ("wire_nodes", nodes.crop(box)),
                ],
            )
        )
    for name, image_set in sheets:
        make_region_contact_sheet(image_set, name)

    # A compact overview of all raw regions helps the agents jump around quickly.
    thumbs = []
    for name, image in rendered:
        scale = min(1.0, 500 / image.width)
        thumb = image.resize((int(image.width * scale), int(image.height * scale)), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (520, thumb.height + 30), "white")
        ImageDraw.Draw(canvas).text((6, 6), name, fill=(0, 0, 0))
        canvas.paste(thumb, (0, 30))
        thumbs.append(canvas)
    columns = 2
    width = columns * 540
    row_heights = []
    for i in range(0, len(thumbs), columns):
        row_heights.append(max(t.height for t in thumbs[i : i + columns]))
    overview = Image.new("RGB", (width, sum(row_heights) + 16 * (len(row_heights) - 1)), "white")
    y = 0
    for row_idx, i in enumerate(range(0, len(thumbs), columns)):
        x = 0
        for thumb in thumbs[i : i + columns]:
            overview.paste(thumb, (x, y))
            x += 540
        y += row_heights[row_idx] + 16
    overview.save(OUT / "iteration5_region_overview_raw.png")


def write_inventory(rows):
    with (OUT / "component_inventory_by_y.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["final_label", "component_type", "bbox", "centroid"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted(rows, key=lambda r: (r["centroid_tuple"][1], r["centroid_tuple"][0])):
            writer.writerow({name: row[name] for name in fieldnames})

    with (OUT / "component_labels.txt").open("w", encoding="utf-8") as f:
        for row in sorted(rows, key=lambda r: r["final_label"]):
            f.write(f"{row['final_label']}\n")

    counts = {}
    for row in rows:
        counts[row["component_type"]] = counts.get(row["component_type"], 0) + 1
    with (OUT / "component_type_counts.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["component_type", "count"])
        writer.writeheader()
        for component_type, count in sorted(counts.items()):
            writer.writerow({"component_type": component_type, "count": count})


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = read_components()
    write_inventory(rows)
    make_all_contact_sheet()
    print(f"wrote inspection assets to {OUT}")
    print(f"components={len(rows)}")


if __name__ == "__main__":
    main()
