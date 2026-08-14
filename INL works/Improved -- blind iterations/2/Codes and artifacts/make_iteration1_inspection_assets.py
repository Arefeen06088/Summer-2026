from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\2")
INPUT = BASE / "Input resources"
OUT = BASE / "Codes and artifacts" / "iteration_1_inspection"

RAW = INPUT / "raw -- schematic_image_variant_b_100.png"
OVERLAY = INPUT / "component_and_logical_labels_banners_overlay.png"
WIRE_OVERLAY = INPUT / "wires_mask_overlay.png"
NODES_OVERLAY = INPUT / "wire_nodes_overlay.png"
COMPONENTS = INPUT / "component_visual_ocr_labels.csv"
ALL_LABELS = INPUT / "component_and_logical_visual_ocr_labels.csv"

REGIONS = [
    ("full_topology", (0, 0, 10800, 7200)),
    ("top_4160_sources", (1350, 300, 8750, 1600)),
    ("train_a_4160_and_feeders", (650, 1250, 5050, 5300)),
    ("train_b_4160_and_feeders", (4850, 1250, 9050, 5300)),
    ("a_feed_loads", (700, 1500, 3350, 5200)),
    ("b_feed_loads", (5000, 1500, 7650, 5200)),
    ("a_rps_dc_ac", (3000, 1500, 4300, 6600)),
    ("b_rps_dc_ac", (7350, 1500, 8400, 6600)),
    ("a_cvcs", (3900, 1500, 5150, 4450)),
    ("b_cvcs", (8250, 1500, 9100, 4450)),
    ("rps_control_a", (3180, 5100, 3820, 6450)),
    ("rps_control_b", (7470, 5100, 8100, 6450)),
    ("dc_bus_a", (3000, 2900, 4050, 4200)),
    ("dc_bus_b", (7350, 2900, 8250, 4200)),
    ("ac_bus_a", (3100, 4300, 4100, 5050)),
    ("ac_bus_b", (7400, 4300, 8350, 5050)),
]


def parse_bbox(text: str):
    parts = [int(part.strip()) for part in text.split(",")]
    if len(parts) != 4:
        raise ValueError(f"bad bbox: {text!r}")
    return tuple(parts)


def read_rows(path: Path):
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row = dict(row)
            row["label"] = row["normalized_text"]
            row["bbox_tuple"] = parse_bbox(row["bbox"])
            x1, y1, x2, y2 = row["bbox_tuple"]
            row["centroid_tuple"] = ((x1 + x2) / 2, (y1 + y2) / 2)
            rows.append(row)
    return rows


def save_resized_crop(image: Image.Image, name: str, box, suffix: str, max_width: int = 2400):
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
        scale = min(1.0, 760 / img.width)
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
    sheet.save(OUT / f"{name}_contact_sheet.png")


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
    row_heights = [max(t.height for t in thumbs[i : i + columns]) for i in range(0, len(thumbs), columns)]
    overview = Image.new("RGB", (width, sum(row_heights) + 16 * (len(row_heights) - 1)), "white")
    y = 0
    for row_idx, i in enumerate(range(0, len(thumbs), columns)):
        x = 0
        for thumb in thumbs[i : i + columns]:
            overview.paste(thumb, (x, y))
            x += 540
        y += row_heights[row_idx] + 16
    overview.save(OUT / "iteration1_region_overview_raw.png")


def write_inventory(component_rows, all_rows):
    with (OUT / "component_inventory_by_y.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["label", "bbox", "centroid"])
        writer.writeheader()
        for row in sorted(component_rows, key=lambda r: (r["centroid_tuple"][1], r["centroid_tuple"][0])):
            writer.writerow(
                {
                    "label": row["label"],
                    "bbox": row["bbox"],
                    "centroid": f"{row['centroid_tuple'][0]:.1f},{row['centroid_tuple'][1]:.1f}",
                }
            )

    with (OUT / "component_labels.txt").open("w", encoding="utf-8") as f:
        for row in sorted(component_rows, key=lambda r: r["label"]):
            f.write(f"{row['label']}\n")

    logical = [row for row in all_rows if row["label"].startswith("BUS-")]
    with (OUT / "bus_label_candidates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["label", "bbox", "centroid"])
        writer.writeheader()
        for row in sorted(logical, key=lambda r: (r["centroid_tuple"][1], r["centroid_tuple"][0])):
            writer.writerow(
                {
                    "label": row["label"],
                    "bbox": row["bbox"],
                    "centroid": f"{row['centroid_tuple'][0]:.1f},{row['centroid_tuple'][1]:.1f}",
                }
            )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    component_rows = read_rows(COMPONENTS)
    all_rows = read_rows(ALL_LABELS)
    write_inventory(component_rows, all_rows)
    make_assets()
    print(f"wrote inspection assets to {OUT}")
    print(f"components={len(component_rows)}")
    print(f"bus_candidates={sum(1 for row in all_rows if row['label'].startswith('BUS-'))}")


if __name__ == "__main__":
    main()
