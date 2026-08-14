from __future__ import annotations

import ast
import csv
import math
import re
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\40")
INPUT = BASE / "Input resources"
ARTIFACTS = BASE / "Codes and artifacts"
CROPS = ARTIFACTS / "inspection_crops_doc40_current"

RAW = INPUT / "synthetic_nuclear_distribution_schematic.png"
COMP_OVERLAY = INPUT / "component_and_logical_labels_banners_overlay.png"
WIRE_OVERLAY = INPUT / "wire_nodes_overlay.png"
MASK_OVERLAY = INPUT / "wires_mask_overlay.png"
COMP_CSV = INPUT / "component_and_logical_visual_ocr_labels.csv"
WIRE_CSV = INPUT / "wire_nodes.csv"


def parse_list(value: str) -> list[float]:
    parsed = ast.literal_eval(value)
    if not isinstance(parsed, list):
        raise ValueError(f"Expected list, got {value!r}")
    return parsed


def clean_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_")[:80]


def load_components() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with COMP_CSV.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            bbox = [float(v) for v in parse_list(row["bbox"])]
            centroid = [float(v) for v in parse_list(row["centroid"])]
            rows.append(
                {
                    "node_name": row["normalized_label"].strip() or row["final_label"].strip(),
                    "stable_node_id": row["stable_node_id"].strip(),
                    "detected_component_id": row["detected_component_id"].strip(),
                    "final_label": row["final_label"].strip(),
                    "bbox": bbox,
                    "centroid_x": centroid[0],
                    "centroid_y": centroid[1],
                    "component_type": row["component_type"].strip(),
                    "node_kind": row["node_kind"].strip(),
                    "label_source": row["label_source"].strip(),
                    "confidence": row["confidence"].strip(),
                    "evidence_description": row["evidence_description"].strip(),
                }
            )
    return sorted(rows, key=lambda r: (float(r["centroid_y"]), float(r["centroid_x"]), str(r["node_name"])))


def load_wire_nodes() -> list[dict[str, str]]:
    with WIRE_CSV.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def save_scaled(src: Path, dest: Path, max_width: int = 2200) -> None:
    img = Image.open(src).convert("RGB")
    scale = min(1.0, max_width / img.width)
    out = img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)
    out.save(dest)


def crop_grid(src: Path, prefix: str, cols: int = 3, rows: int = 3, overlap: int = 120) -> None:
    img = Image.open(src).convert("RGB")
    cell_w = math.ceil(img.width / cols)
    cell_h = math.ceil(img.height / rows)
    for r in range(rows):
        for c in range(cols):
            left = max(0, c * cell_w - overlap)
            top = max(0, r * cell_h - overlap)
            right = min(img.width, (c + 1) * cell_w + overlap)
            bottom = min(img.height, (r + 1) * cell_h + overlap)
            img.crop((left, top, right, bottom)).save(CROPS / f"{prefix}_r{r+1}c{c+1}.png")


def crop_components(rows: list[dict[str, object]], margin: int = 180) -> None:
    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(COMP_OVERLAY).convert("RGB")
    for idx, row in enumerate(rows, 1):
        x1, y1, x2, y2 = [int(round(v)) for v in row["bbox"]]  # type: ignore[index]
        box = (
            max(0, x1 - margin),
            max(0, y1 - margin),
            min(raw.width, x2 + margin),
            min(raw.height, y2 + margin),
        )
        label = clean_name(str(row["node_name"]))
        raw.crop(box).save(CROPS / f"component_{idx:03d}_{label}_raw.png")
        overlay.crop(box).save(CROPS / f"component_{idx:03d}_{label}_component_overlay.png")


def make_contact_sheet(rows: list[dict[str, object]], dest: Path, thumb_w: int = 360, thumb_h: int = 240) -> None:
    raw = Image.open(RAW).convert("RGB")
    font = ImageFont.load_default()
    cols = 5
    pad = 18
    label_h = 36
    sheet_w = cols * thumb_w + (cols + 1) * pad
    sheet_h = math.ceil(len(rows) / cols) * (thumb_h + label_h + pad) + pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(rows):
        x1, y1, x2, y2 = [int(round(v)) for v in row["bbox"]]  # type: ignore[index]
        margin = 130
        box = (
            max(0, x1 - margin),
            max(0, y1 - margin),
            min(raw.width, x2 + margin),
            min(raw.height, y2 + margin),
        )
        crop = raw.crop(box)
        crop.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        col = i % cols
        row_i = i // cols
        left = pad + col * (thumb_w + pad)
        top = pad + row_i * (thumb_h + label_h + pad)
        sheet.paste(crop, (left, top))
        draw.rectangle((left, top, left + thumb_w - 1, top + thumb_h - 1), outline=(180, 180, 180), width=1)
        label = f"{i+1:02d} {row['node_name']} ({row['component_type']})"
        draw.text((left, top + thumb_h + 5), label[:52], fill=(0, 0, 0), font=font)
    sheet.save(dest)


def write_inventory(rows: list[dict[str, object]]) -> None:
    out_csv = ARTIFACTS / "component_inventory_doc40_current.csv"
    fields = [
        "node_name",
        "stable_node_id",
        "component_type",
        "node_kind",
        "bbox",
        "centroid_x",
        "centroid_y",
        "label_source",
        "confidence",
        "include_in_matrix",
        "evidence_description",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **{field: row.get(field, "") for field in fields},
                    "bbox": row["bbox"],
                    "include_in_matrix": "Y",
                }
            )

    comp_counts = Counter(str(r["component_type"]) for r in rows)
    kind_counts = Counter(str(r["node_kind"]) for r in rows)
    lines = [
        "# Doc 40 Input-Only Component Inventory",
        "",
        f"Source CSV: `{COMP_CSV}`",
        f"Raw schematic: `{RAW}`",
        "",
        f"Inventory rows: {len(rows)}",
        "",
        "## Component Type Counts",
        "",
    ]
    lines.extend(f"- {name or '<blank>'}: {count}" for name, count in sorted(comp_counts.items()))
    lines.extend(["", "## Node Kind Counts", ""])
    lines.extend(f"- {name or '<blank>'}: {count}" for name, count in sorted(kind_counts.items()))
    lines.extend(["", "## Ordered Nodes", ""])
    for i, row in enumerate(rows, 1):
        lines.append(
            f"{i}. `{row['node_name']}` - {row['component_type']}; "
            f"centroid=({row['centroid_x']:.1f}, {row['centroid_y']:.1f}); bbox={row['bbox']}"
        )
    (ARTIFACTS / "component_inventory_doc40_current.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_wire_summary(rows: list[dict[str, str]]) -> None:
    counts = Counter(r.get("node_type", "") for r in rows)
    lines = [
        "# Doc 40 Wire Node Summary",
        "",
        f"Source CSV: `{WIRE_CSV}`",
        f"Wire node rows: {len(rows)}",
        "",
        "## Node Type Counts",
        "",
    ]
    lines.extend(f"- {name or '<blank>'}: {count}" for name, count in sorted(counts.items()))
    lines.extend(["", "## Ordered Wire Nodes", ""])
    for row in rows:
        lines.append(
            f"- `{row['node_id']}` {row['node_type']} at ({row['x']}, {row['y']}), degree {row['degree']}"
        )
    (ARTIFACTS / "wire_node_summary_doc40_current.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(component_rows: list[dict[str, object]], wire_rows: list[dict[str, str]]) -> None:
    raw = Image.open(RAW)
    lines = [
        "# Doc 40 Prepared Resource Manifest",
        "",
        "All artifacts in this folder are derived only from `Input resources` and are not ground truth.",
        "",
        f"- Raw image size: {raw.width} x {raw.height}",
        f"- Component/logical inventory rows: {len(component_rows)}",
        f"- Wire node rows: {len(wire_rows)}",
        "",
        "Key prepared files:",
        "- `component_inventory_doc40_current.csv`",
        "- `component_inventory_doc40_current.md`",
        "- `wire_node_summary_doc40_current.md`",
        "- `inspection_crops_doc40_current/overview_raw_scaled.png`",
        "- `inspection_crops_doc40_current/overview_component_overlay_scaled.png`",
        "- `inspection_crops_doc40_current/overview_wire_nodes_scaled.png`",
        "- `inspection_crops_doc40_current/component_contact_sheet_raw.png`",
        "- 3x3 raw/component/wire/mask crop grids",
        "- per-component raw and component-overlay crops",
    ]
    (ARTIFACTS / "input_resource_summary_doc40_current.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    CROPS.mkdir(parents=True, exist_ok=True)
    component_rows = load_components()
    wire_rows = load_wire_nodes()

    write_inventory(component_rows)
    write_wire_summary(wire_rows)
    write_manifest(component_rows, wire_rows)

    save_scaled(RAW, CROPS / "overview_raw_scaled.png")
    save_scaled(COMP_OVERLAY, CROPS / "overview_component_overlay_scaled.png")
    save_scaled(WIRE_OVERLAY, CROPS / "overview_wire_nodes_scaled.png")
    save_scaled(MASK_OVERLAY, CROPS / "overview_wires_mask_scaled.png")

    crop_grid(RAW, "raw")
    crop_grid(COMP_OVERLAY, "component_overlay")
    crop_grid(WIRE_OVERLAY, "wire_nodes")
    crop_grid(MASK_OVERLAY, "wire_mask")
    crop_components(component_rows)
    make_contact_sheet(component_rows, CROPS / "component_contact_sheet_raw.png")

    print(f"Prepared {len(component_rows)} component rows and {len(wire_rows)} wire nodes.")
    print(f"Artifacts: {ARTIFACTS}")
    print(f"Crops: {CROPS}")


if __name__ == "__main__":
    main()
