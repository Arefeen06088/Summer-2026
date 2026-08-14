from __future__ import annotations

import ast
import csv
import math
import re
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\17")
INPUT = BASE / "Input resources"
ARTIFACTS = BASE / "Codes and artifacts"
CROPS = ARTIFACTS / "inspection_crops_doc17_current"

RAW = INPUT / "raw -- synthetic_npp_aux_power_schematic_overlap_fixed.png"
COMP_OVERLAY = INPUT / "detected_components_and_logical_detection_plus_ocr_overlay.png"
WIRE_OVERLAY = INPUT / "wire_nodes_overlay.png"
MASK_OVERLAY = INPUT / "wires_mask_overlay.png"
COMP_CSV = INPUT / "component_visual_ocr_labels.csv"
WIRE_CSV = INPUT / "wire_nodes.csv"


VISUAL_ADDITIONS = [
    # Raw-visible electrical/logical nodes not present as component rows in the OCR CSV.
    # Coordinates are approximate visual boxes used only for inspection/indexing.
    {"node_name": "GEN-001", "component_type": "generator", "node_kind": "physical_component", "bbox": [2050, 275, 2225, 420], "evidence_description": "Raw-visible main generator above UAT-1A/UAT-1B split feeder."},
    {"node_name": "AM-480-A", "component_type": "meter", "node_kind": "physical_component", "bbox": [1760, 1010, 1835, 1085], "evidence_description": "Raw-visible ammeter on Train A 480 V bus/instrument area."},
    {"node_name": "VM-480-A", "component_type": "meter", "node_kind": "physical_component", "bbox": [1910, 1010, 1985, 1085], "evidence_description": "Raw-visible voltmeter on Train A 480 V bus/instrument area."},
    {"node_name": "AM-480-B", "component_type": "meter", "node_kind": "physical_component", "bbox": [3760, 1010, 3835, 1085], "evidence_description": "Raw-visible ammeter on Train B 480 V bus/instrument area."},
    {"node_name": "VM-480-B", "component_type": "meter", "node_kind": "physical_component", "bbox": [3910, 1010, 3985, 1085], "evidence_description": "Raw-visible voltmeter on Train B 480 V bus/instrument area."},
    {"node_name": "GND-DC-B", "component_type": "ground", "node_kind": "physical_component", "bbox": [3845, 2680, 3925, 2755], "evidence_description": "Raw-visible ground symbol associated with Train B DC equipment."},
    {"node_name": "BUS-4160-A", "component_type": "bus", "node_kind": "logical_node", "bbox": [250, 675, 2000, 735], "evidence_description": "Named 4160 V Train A switchgear/bus rail."},
    {"node_name": "BUS-4160-B", "component_type": "bus", "node_kind": "logical_node", "bbox": [2220, 675, 4050, 735], "evidence_description": "Named 4160 V Train B switchgear/bus rail."},
    {"node_name": "BUS-480-A", "component_type": "bus", "node_kind": "logical_node", "bbox": [250, 1115, 2000, 1190], "evidence_description": "Named Train A 480 V load-center / switchgear bus rail."},
    {"node_name": "BUS-480-B", "component_type": "bus", "node_kind": "logical_node", "bbox": [2220, 1115, 4050, 1190], "evidence_description": "Named Train B 480 V load-center / switchgear bus rail."},
    {"node_name": "BUS-125DC-A", "component_type": "bus", "node_kind": "logical_node", "bbox": [260, 2535, 2040, 2610], "evidence_description": "Named 125 VDC Train A bus rail."},
    {"node_name": "BUS-125DC-B", "component_type": "bus", "node_kind": "logical_node", "bbox": [2210, 2535, 4070, 2610], "evidence_description": "Named 125 VDC Train B bus rail."},
    {"node_name": "BUS-120AC-A", "component_type": "bus", "node_kind": "logical_node", "bbox": [760, 2860, 1460, 2985], "evidence_description": "Train A 120 VAC bus/control source area around STS/PNL feed."},
    {"node_name": "BUS-120AC-B", "component_type": "bus", "node_kind": "logical_node", "bbox": [2780, 2860, 3480, 2985], "evidence_description": "Train B 120 VAC bus/control source area around STS/PNL feed."},
]


def parse_list(value: str) -> list[float]:
    parsed = ast.literal_eval(value)
    if not isinstance(parsed, list):
        raise ValueError(f"Expected list, got {value!r}")
    return parsed


def clean_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_")[:80]


def centroid_from_bbox(bbox: list[float]) -> tuple[float, float]:
    return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)


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
                    "inventory_source": "component_visual_ocr_labels.csv",
                    "include_in_matrix": "Y",
                }
            )
    for idx, item in enumerate(VISUAL_ADDITIONS, 1):
        bbox = [float(v) for v in item["bbox"]]
        cx, cy = centroid_from_bbox(bbox)
        rows.append(
            {
                "node_name": item["node_name"],
                "stable_node_id": f"VISUAL-ADD-{idx:03d}",
                "detected_component_id": "",
                "final_label": item["node_name"],
                "bbox": bbox,
                "centroid_x": cx,
                "centroid_y": cy,
                "component_type": item["component_type"],
                "node_kind": item["node_kind"],
                "label_source": "raw_visual_addition",
                "confidence": "review",
                "evidence_description": item["evidence_description"],
                "inventory_source": "raw_visual_review",
                "include_in_matrix": "Y",
            }
        )
    return sorted(rows, key=lambda r: (float(r["centroid_y"]), float(r["centroid_x"]), str(r["node_name"])))


def load_wire_nodes() -> list[dict[str, str]]:
    with WIRE_CSV.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def save_scaled(src: Path, dest: Path, max_width: int = 2400) -> None:
    img = Image.open(src).convert("RGB")
    scale = min(1.0, max_width / img.width)
    out = img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)
    out.save(dest)


def crop_grid(src: Path, prefix: str, cols: int = 4, rows: int = 3, overlap: int = 120) -> None:
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


def crop_named_regions() -> None:
    img_paths = {"raw": RAW, "component_overlay": COMP_OVERLAY, "wire_nodes": WIRE_OVERLAY, "wire_mask": MASK_OVERLAY}
    regions = {
        "top_4160_sources_tie": (160, 240, 4200, 980),
        "middle_480_loads": (150, 900, 4200, 1820),
        "bottom_dc_ac_control": (150, 2300, 4200, 3400),
        "right_notes_legend": (4050, 160, 5450, 1850),
        "visual_additions_meters": (1650, 960, 4070, 1220),
        "visual_additions_dc_b_ground": (3550, 2450, 4100, 2820),
    }
    focus_dir = CROPS / "focus"
    focus_dir.mkdir(parents=True, exist_ok=True)
    for prefix, src in img_paths.items():
        img = Image.open(src).convert("RGB")
        for name, box in regions.items():
            img.crop(box).save(focus_dir / f"{prefix}_{name}.png")


def crop_components(rows: list[dict[str, object]], margin: int = 150) -> None:
    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(COMP_OVERLAY).convert("RGB")
    comp_dir = CROPS / "components"
    comp_dir.mkdir(parents=True, exist_ok=True)
    for idx, row in enumerate(rows, 1):
        x1, y1, x2, y2 = [int(round(v)) for v in row["bbox"]]  # type: ignore[index]
        box = (
            max(0, x1 - margin),
            max(0, y1 - margin),
            min(raw.width, x2 + margin),
            min(raw.height, y2 + margin),
        )
        label = clean_name(str(row["node_name"]))
        raw.crop(box).save(comp_dir / f"component_{idx:03d}_{label}_raw.png")
        overlay.crop(box).save(comp_dir / f"component_{idx:03d}_{label}_component_overlay.png")


def make_contact_sheet(rows: list[dict[str, object]], dest: Path, thumb_w: int = 260, thumb_h: int = 190) -> None:
    raw = Image.open(RAW).convert("RGB")
    font = ImageFont.load_default()
    cols = 6
    pad = 12
    label_h = 34
    sheet_w = cols * thumb_w + (cols + 1) * pad
    sheet_h = math.ceil(len(rows) / cols) * (thumb_h + label_h + pad) + pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(rows):
        x1, y1, x2, y2 = [int(round(v)) for v in row["bbox"]]  # type: ignore[index]
        margin = 110
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
        label = f"{i+1:03d} {row['node_name']}"
        draw.text((left, top + thumb_h + 4), label[:42], fill=(0, 0, 0), font=font)
    sheet.save(dest)


def write_inventory(rows: list[dict[str, object]]) -> None:
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
        "inventory_source",
        "include_in_matrix",
        "evidence_description",
    ]
    with (ARTIFACTS / "component_inventory_doc17_current.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})

    comp_counts = Counter(str(r["component_type"]) for r in rows)
    kind_counts = Counter(str(r["node_kind"]) for r in rows)
    lines = [
        "# Doc 17 Input-Only Component Inventory",
        "",
        "This inventory is derived from `Input resources` and raw visual review only. It is not ground truth.",
        "",
        f"Inventory rows: {len(rows)}",
        f"OCR/component CSV rows: {len(rows) - len(VISUAL_ADDITIONS)}",
        f"Raw-visual additions: {len(VISUAL_ADDITIONS)}",
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
            f"{i}. `{row['node_name']}` - {row['component_type']}; {row['node_kind']}; "
            f"centroid=({float(row['centroid_x']):.1f}, {float(row['centroid_y']):.1f}); source={row['inventory_source']}"
        )
    (ARTIFACTS / "component_inventory_doc17_current.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_wire_summary(rows: list[dict[str, str]]) -> None:
    counts = Counter(r.get("node_type", "") for r in rows)
    lines = [
        "# Doc 17 Wire Node Summary",
        "",
        "Wire nodes are used as geometric aids only and are not promoted into the matrix by default.",
        "",
        f"Wire node rows: {len(rows)}",
        "",
        "## Node Type Counts",
        "",
    ]
    lines.extend(f"- {name or '<blank>'}: {count}" for name, count in sorted(counts.items()))
    lines.extend(["", "## Ordered Wire Nodes", ""])
    for row in rows:
        lines.append(f"- `{row['node_id']}` {row['node_type']} at ({row['x']}, {row['y']}), degree {row['degree']}")
    (ARTIFACTS / "wire_node_summary_doc17_current.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(component_rows: list[dict[str, object]], wire_rows: list[dict[str, str]]) -> None:
    raw = Image.open(RAW)
    lines = [
        "# Doc 17 Prepared Resource Manifest",
        "",
        "All artifacts here are derived only from `Input resources` plus raw visual inspection.",
        "",
        f"- Raw image size: {raw.width} x {raw.height}",
        f"- Component/logical inventory rows: {len(component_rows)}",
        f"- Wire node rows: {len(wire_rows)}",
        "",
        "Key files:",
        "- `component_inventory_doc17_current.csv`",
        "- `component_inventory_doc17_current.md`",
        "- `wire_node_summary_doc17_current.md`",
        "- `inspection_crops_doc17_current/overview_raw_scaled.png`",
        "- `inspection_crops_doc17_current/overview_component_overlay_scaled.png`",
        "- `inspection_crops_doc17_current/overview_wire_nodes_scaled.png`",
        "- `inspection_crops_doc17_current/overview_wires_mask_scaled.png`",
        "- 4x3 raw/component/wire/mask crop grids",
        "- focus crops under `inspection_crops_doc17_current/focus`",
        "- per-component crops under `inspection_crops_doc17_current/components`",
    ]
    (ARTIFACTS / "input_resource_summary_doc17_current.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    crop_named_regions()
    crop_components(component_rows)
    make_contact_sheet(component_rows, CROPS / "component_contact_sheet_raw.png")
    print(f"Prepared {len(component_rows)} inventory rows and {len(wire_rows)} wire nodes.")
    print(f"Artifacts: {ARTIFACTS}")
    print(f"Crops: {CROPS}")


if __name__ == "__main__":
    main()
