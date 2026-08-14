from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\25\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"
CROPS_DIR = RESULTS_DIR / "visual_crops"

RAW = BASE_DIR / "raw -- synthetic_npp_electrical_schematic_revised_v4.png"
COMPONENTS = BASE_DIR / "detected_components_overlay.png"
WIRES = BASE_DIR / "wires_mask.png"
WIRES_OVERLAY = BASE_DIR / "wires_mask_overlay.png"

SOURCES = {
    "raw": RAW,
    "components": COMPONENTS,
    "wires": WIRES,
    "wires_overlay": WIRES_OVERLAY,
}


def scaled_box(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    ref_w, ref_h = 9200, 6200
    x0, y0, x1, y1 = box
    return (
        max(0, min(width, round(x0 * width / ref_w))),
        max(0, min(height, round(y0 * height / ref_h))),
        max(0, min(width, round(x1 * width / ref_w))),
        max(0, min(height, round(y1 * height / ref_h))),
    )


def save_resized_crop(img: Image.Image, box: tuple[int, int, int, int], out: Path, max_side: int = 2600) -> None:
    crop = img.crop(box)
    scale = min(max_side / max(crop.size), 1.0)
    if scale < 1.0:
        crop = crop.resize((int(crop.width * scale), int(crop.height * scale)))
    out.parent.mkdir(parents=True, exist_ok=True)
    crop.save(out)


def main() -> None:
    CROPS_DIR.mkdir(parents=True, exist_ok=True)
    with Image.open(RAW) as raw_img:
        width, height = raw_img.size

    for tag, path in SOURCES.items():
        with Image.open(path) as img:
            thumb = img.copy()
            thumb.thumbnail((2400, 1600))
            thumb.save(CROPS_DIR / f"{tag}_full_thumb.png")

    nx, ny = 4, 3
    overlap = 0.10
    tile_w = width / nx
    tile_h = height / ny
    regions: dict[str, tuple[int, int, int, int]] = {}
    for row in range(ny):
        for col in range(nx):
            x0 = max(0, int(col * tile_w - overlap * tile_w))
            y0 = max(0, int(row * tile_h - overlap * tile_h))
            x1 = min(width, int((col + 1) * tile_w + overlap * tile_w))
            y1 = min(height, int((row + 1) * tile_h + overlap * tile_h))
            regions[f"grid_r{row + 1}_c{col + 1}"] = (x0, y0, x1, y1)

    regions.update(
        {
            "top_sources_and_13kv": (0, 0, width, int(height * 0.30)),
            "upper_4160_all": (0, int(height * 0.16), width, int(height * 0.46)),
            "middle_distribution_all": (0, int(height * 0.30), width, int(height * 0.72)),
            "bottom_control_power_all": (0, int(height * 0.62), width, height),
            "left_half": (0, 0, int(width * 0.55), height),
            "right_half": (int(width * 0.45), 0, width, height),
            "center_overlap": (int(width * 0.24), int(height * 0.18), int(width * 0.76), int(height * 0.84)),
            "top_left_sources": (0, 0, int(width * 0.43), int(height * 0.38)),
            "top_mid_buses": (int(width * 0.27), int(height * 0.04), int(width * 0.73), int(height * 0.43)),
            "top_right_sources": (int(width * 0.57), 0, width, int(height * 0.38)),
            "lower_left_control": (0, int(height * 0.52), int(width * 0.55), height),
            "lower_right_control": (int(width * 0.45), int(height * 0.52), width, height),
            "title_notes": (int(width * 0.66), 0, width, int(height * 0.26)),
            "train_a_4160_feeders": (120, 620, 1840, 1940),
            "train_b_4160_feeders": (1700, 620, 3420, 1940),
            "train_c_4160_feeders": (3260, 620, 5000, 1940),
            "train_a_480v_branches": (120, 1720, 1850, 3500),
            "train_b_480v_branches": (1700, 1720, 3420, 3500),
            "train_c_480v_branches": (3260, 1720, 5000, 3500),
            "bottom_125v_rps_all": (120, 3280, 5000, 4300),
            "bottom_125v_rps_left": (120, 3280, 2600, 4300),
            "bottom_125v_rps_right": (2500, 3280, 5000, 4300),
        }
    )

    detailed_ref_regions = {
        "detail_top_div1": (450, 350, 4550, 1800),
        "detail_top_div2": (4550, 350, 8700, 1800),
        "detail_div1_feeders": (500, 1350, 4500, 3850),
        "detail_div2_feeders": (4700, 1350, 8700, 3850),
        "detail_div1_feeders_left": (500, 1450, 2250, 3850),
        "detail_div1_feeders_mid": (2050, 1450, 3450, 3850),
        "detail_div1_feeders_right": (3200, 1450, 4550, 3850),
        "detail_div2_feeders_left": (4700, 1450, 6250, 3850),
        "detail_div2_feeders_mid": (6000, 1450, 7350, 3850),
        "detail_div2_feeders_right": (7150, 1450, 8700, 3850),
        "detail_bottom_div1_dc_control": (500, 3650, 4300, 5700),
        "detail_bottom_div2_dc_control": (4700, 3650, 8700, 5700),
        "detail_bottom_center_control": (3450, 3650, 5600, 5700),
        "detail_bottom_instruments_div1": (500, 4550, 3000, 5700),
        "detail_bottom_instruments_div2": (5050, 4550, 8050, 5700),
        "detail_notes_legend_title": (500, 5200, 8700, 6100),
    }
    detailed_regions = {name: scaled_box(box, width, height) for name, box in detailed_ref_regions.items()}

    all_regions = regions | detailed_regions
    for name, box in all_regions.items():
        for tag, path in SOURCES.items():
            if tag == "wires":
                continue
            max_side = 4200 if name.startswith("detail_") else 2600
            with Image.open(path) as img:
                save_resized_crop(img, box, CROPS_DIR / f"{name}_{tag}.png", max_side=max_side)

    manifest = {
        "image_size": [width, height],
        "raw": RAW.name,
        "regions": {name: list(box) for name, box in all_regions.items()},
    }
    (CROPS_DIR / "crop_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
