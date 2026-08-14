from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\1")
INPUT = BASE / "Input resources"
OUT = BASE / "Codes and artifacts" / "iteration_1_inspection"

RAW = INPUT / "raw -- schematic_image_clean_100_connected.png"
OVERLAY = INPUT / "component_and_logical_labels_banners_overlay.png"
WIRE_OVERLAY = INPUT / "wires_mask_overlay.png"
NODES_OVERLAY = INPUT / "wire_nodes_overlay.png"
COMPONENTS = INPUT / "component_visual_ocr_labels.csv"

REGIONS = [
    ("full_topology", (0, 0, 4800, 3200)),
    ("top_sources_switchgear", (360, 120, 3700, 700)),
    ("a_train_power", (420, 180, 1450, 1000)),
    ("b_train_power", (1580, 180, 2550, 1000)),
    ("c_train_power", (2680, 180, 3600, 1000)),
    ("480_bus_a_b_c", (360, 520, 3600, 1120)),
    ("mcc_loads_a_left", (420, 1080, 1450, 1880)),
    ("mcc_loads_b_middle", (1600, 1080, 2560, 1880)),
    ("mcc_loads_c_right", (2800, 1080, 3660, 1880)),
    ("load_row_full", (360, 1080, 3720, 1900)),
    ("dc_125_a_b", (1180, 1800, 2820, 2180)),
    ("inverters_rps_uv", (520, 2260, 2680, 2850)),
    ("rps_a_detail", (560, 2500, 1140, 2780)),
    ("rps_b_detail", (1840, 2500, 2320, 2780)),
    ("rps_pt_detail", (1180, 2500, 2660, 2780)),
    ("lower_full", (360, 1800, 2820, 2920)),
]


def parse_bbox(text: str):
    parts = [int(part.strip()) for part in text.split(",")]
    if len(parts) != 4:
        raise ValueError(f"bad bbox: {text!r}")
    return tuple(parts)


def read_components():
    rows = []
    with COMPONENTS.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row = dict(row)
            row["label"] = row["normalized_text"]
            row["bbox_tuple"] = parse_bbox(row["bbox"])
            x1, y1, x2, y2 = row["bbox_tuple"]
            row["centroid_tuple"] = ((x1 + x2) / 2, (y1 + y2) / 2)
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


def make_region_contact_sheet(name: str, images):
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


def make_assets():
    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    wire = Image.open(WIRE_OVERLAY).convert("RGB")
    nodes = Image.open(NODES_OVERLAY).convert("RGB")

    overview_items = []
    for name, box in REGIONS:
        raw_crop = raw.crop(box)
        save_resized_crop(raw, name, box, "raw")
        save_resized_crop(overlay, name, box, "labels")
        save_resized_crop(wire, name, box, "wires")
        save_resized_crop(nodes, name, box, "wire_nodes")
        make_region_contact_sheet(
            name,
            [
                ("raw", raw_crop),
                ("labels", overlay.crop(box)),
                ("wires", wire.crop(box)),
                ("wire_nodes", nodes.crop(box)),
            ],
        )
        overview_items.append((name, raw_crop))

    thumbs = []
    for name, image in overview_items:
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
    overview.save(OUT / "iteration1_region_overview_raw.png")


def write_inventory(rows):
    with (OUT / "component_inventory_by_y.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["label", "bbox", "centroid"])
        writer.writeheader()
        for row in sorted(rows, key=lambda r: (r["centroid_tuple"][1], r["centroid_tuple"][0])):
            writer.writerow(
                {
                    "label": row["label"],
                    "bbox": row["bbox"],
                    "centroid": f"{row['centroid_tuple'][0]:.1f},{row['centroid_tuple'][1]:.1f}",
                }
            )

    with (OUT / "component_labels.txt").open("w", encoding="utf-8") as f:
        for row in sorted(rows, key=lambda r: r["label"]):
            f.write(f"{row['label']}\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = read_components()
    write_inventory(rows)
    make_assets()
    print(f"wrote inspection assets to {OUT}")
    print(f"components={len(rows)}")


if __name__ == "__main__":
    main()
