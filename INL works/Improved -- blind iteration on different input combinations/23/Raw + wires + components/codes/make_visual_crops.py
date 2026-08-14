from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"
CROPS_DIR = RESULTS_DIR / "visual_crops"

RAW = BASE_DIR / "raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png"
COMPONENTS = BASE_DIR / "detected_components_overlay.png"
WIRES = BASE_DIR / "wires_mask.png"
WIRES_OVERLAY = BASE_DIR / "wires_mask_overlay.png"

SOURCES = {
    "raw": RAW,
    "components": COMPONENTS,
    "wires": WIRES,
    "wires_overlay": WIRES_OVERLAY,
}


def save_resized_crop(img: Image.Image, box: tuple[int, int, int, int], out: Path, max_side: int = 2400) -> None:
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

    # Full thumbnails.
    for tag, path in SOURCES.items():
        with Image.open(path) as img:
            thumb = img.copy()
            thumb.thumbnail((2400, 1600))
            thumb.save(CROPS_DIR / f"{tag}_full_thumb.png")

    # Overlapping grid. Useful for unexpected shifts.
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
            regions[f"grid_r{row+1}_c{col+1}"] = (x0, y0, x1, y1)

    # Broad schematic bands and likely detailed areas.
    regions.update(
        {
            "top_sources_and_13kv": (0, 0, width, int(height * 0.30)),
            "upper_4160_all": (0, int(height * 0.18), width, int(height * 0.46)),
            "middle_distribution_all": (0, int(height * 0.34), width, int(height * 0.72)),
            "bottom_control_power_all": (0, int(height * 0.64), width, height),
            "left_half": (0, 0, int(width * 0.55), height),
            "right_half": (int(width * 0.45), 0, width, height),
            "center_overlap": (int(width * 0.25), int(height * 0.20), int(width * 0.75), int(height * 0.82)),
            "top_left_sources": (0, 0, int(width * 0.42), int(height * 0.38)),
            "top_mid_buses": (int(width * 0.28), int(height * 0.05), int(width * 0.72), int(height * 0.43)),
            "top_right_sources": (int(width * 0.58), 0, width, int(height * 0.38)),
            "lower_left_control": (0, int(height * 0.55), int(width * 0.55), height),
            "lower_right_control": (int(width * 0.45), int(height * 0.55), width, height),
            "title_notes": (int(width * 0.70), 0, width, int(height * 0.25)),
        }
    )

    for name, box in regions.items():
        for tag, path in SOURCES.items():
            if tag == "wires":
                # The mask is mainly useful as a full thumbnail unless a specific
                # raw/overlay discrepancy appears.
                continue
            with Image.open(path) as img:
                save_resized_crop(img, box, CROPS_DIR / f"{name}_{tag}.png")

    detailed_regions = {
        "detail_top_train_a": (400, 500, 6000, 3100),
        "detail_top_train_b": (5700, 500, 10650, 3100),
        "detail_lc_1a": (400, 2550, 4050, 5150),
        "detail_lc_1c": (3600, 2550, 7550, 5150),
        "detail_lc_1b": (7050, 2550, 11100, 5150),
        "detail_lc_2a": (400, 5000, 4050, 7500),
        "detail_lc_2c": (3600, 5000, 7550, 7500),
        "detail_lc_2b": (7050, 5000, 11100, 7500),
        "detail_bottom_dc_left": (400, 7200, 5400, 9300),
        "detail_bottom_dc_right": (5200, 7200, 10300, 9300),
        "detail_bottom_center_tie": (3500, 7600, 7600, 9400),
        "detail_legend_notes": (10600, 1700, 14150, 7800),
    }
    for name, box in detailed_regions.items():
        for tag, path in SOURCES.items():
            if tag == "wires":
                continue
            with Image.open(path) as img:
                save_resized_crop(img, box, CROPS_DIR / f"{name}_{tag}.png", max_side=4200)

    manifest = {
        "image_size": [width, height],
        "raw": RAW.name,
        "regions": {name: list(box) for name, box in (regions | detailed_regions).items()},
    }
    (CROPS_DIR / "crop_manifest.json").write_text(__import__("json").dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
