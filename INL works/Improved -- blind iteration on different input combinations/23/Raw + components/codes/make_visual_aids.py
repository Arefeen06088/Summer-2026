from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

DOC = "23"
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw + components"
)
CODES = ROOT / "codes"
RESULTS = ROOT / "results"

RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png"
OVERLAY = ROOT / "detected_components_and_logical_overlay.png"


def clamp_box(box: tuple[int, int, int, int], w: int, h: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    return max(0, x1), max(0, y1), min(w, x2), min(h, y2)


def fit_down(im: Image.Image, max_w: int = 2600, max_h: int = 2200) -> Image.Image:
    scale = min(max_w / im.width, max_h / im.height, 1.0)
    if scale >= 1.0:
        return im.copy()
    size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    return im.resize(size, Image.Resampling.LANCZOS)


def save_crop(
    im: Image.Image,
    stem: str,
    name: str,
    box: tuple[int, int, int, int],
    two_x: bool = False,
    max_w: int = 2800,
    max_h: int = 2300,
) -> None:
    crop = im.crop(clamp_box(box, im.width, im.height))
    fit_down(crop, max_w, max_h).save(RESULTS / f"{stem}_{name}.png")
    if two_x:
        two = crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS)
        fit_down(two, 3600, 3200).save(RESULTS / f"{stem}_{name}_2x.png")


def save_preview(im: Image.Image, stem: str) -> None:
    fit_down(im, 3000, 2200).save(RESULTS / f"{stem}_full_preview.png")
    fit_down(im, 5200, 3800).save(RESULTS / f"{stem}_full_preview_large.png")


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    sources = [("raw", raw), ("overlay", overlay)]

    named_crops = {
        "01_top_4160_sources_full": (700, 520, 10400, 2500),
        "02_top_left_grid_uat_bus_a": (900, 600, 5200, 2350),
        "03_top_middle_tie_sync": (4300, 700, 7800, 2350),
        "04_top_right_grid_uat_bus_b": (6900, 600, 10400, 2350),
        "05_ats_dg_left": (700, 1750, 2500, 2850),
        "06_ats_dg_right": (8800, 1750, 10400, 2850),
        "07_upper_load_centers_full": (650, 2500, 10400, 5200),
        "08_load_center_1a": (720, 2550, 3650, 5200),
        "09_load_center_1c": (3700, 2550, 6900, 5200),
        "10_load_center_1b": (6800, 2550, 10400, 5200),
        "11_lower_load_centers_full": (650, 5000, 10400, 7350),
        "12_load_center_2a": (720, 5050, 3650, 7350),
        "13_load_center_2c": (3700, 5050, 6900, 7350),
        "14_load_center_2b": (6800, 5050, 10400, 7350),
        "15_bottom_dc_ups_full": (650, 7250, 10400, 9000),
        "16_bottom_dc_ups_left": (850, 7400, 5200, 9000),
        "17_bottom_dc_ups_right": (5100, 7400, 10400, 9000),
        "18_notes_legend": (10750, 1700, 13750, 5050),
        "19_reference_title": (10750, 5050, 13750, 9000),
        "20_main_drawing_area": (650, 520, 10400, 9000),
    }

    close_crops = {
        "21_close_top_left_chain": (1200, 640, 3600, 2050),
        "22_close_bus_4160_a": (3000, 1000, 6100, 2100),
        "23_close_tie_sync_metering": (5900, 900, 8300, 2050),
        "24_close_bus_4160_b": (7600, 900, 10200, 2100),
        "25_close_load_1a_left": (850, 3300, 2500, 5050),
        "26_close_load_1a_right": (2200, 3300, 3600, 5050),
        "27_close_load_1c_left": (3900, 3300, 5400, 5050),
        "28_close_load_1c_right": (5200, 3300, 6800, 5050),
        "29_close_load_1b_left": (7050, 3300, 8600, 5050),
        "30_close_load_1b_right": (8350, 3300, 10100, 5050),
        "31_close_load_2a_left": (850, 5700, 2500, 7200),
        "32_close_load_2a_right": (2200, 5700, 3600, 7200),
        "33_close_load_2c_left": (3900, 5700, 5400, 7200),
        "34_close_load_2c_right": (5200, 5700, 6800, 7200),
        "35_close_load_2b_left": (7050, 5700, 8600, 7200),
        "36_close_load_2b_right": (8350, 5700, 10100, 7200),
        "37_close_bottom_dc_left": (900, 7600, 5200, 8950),
        "38_close_bottom_dc_right": (5200, 7600, 10300, 8950),
        "39_close_bottom_center_controls": (4300, 8050, 7800, 9250),
        "40_close_legend": (10800, 1850, 13650, 5050),
    }

    for stem, im in sources:
        save_preview(im, stem)
        for name, box in named_crops.items():
            save_crop(im, stem, name, box)
        for name, box in close_crops.items():
            save_crop(im, stem, name, box, two_x=True)

    # Broad grid over the active drawing area; useful when shifted components make a close crop miss context.
    x1, y1, x2, y2 = 650, 520, 10400, 9000
    rows = cols = 4
    pad = 180
    cell_w = (x2 - x1) // cols
    cell_h = (y2 - y1) // rows
    for stem, im in sources:
        for r in range(rows):
            for c in range(cols):
                bx1 = x1 + c * cell_w - pad
                by1 = y1 + r * cell_h - pad
                bx2 = x1 + (c + 1) * cell_w + pad
                by2 = y1 + (r + 1) * cell_h + pad
                save_crop(im, stem, f"grid_r{r + 1}c{c + 1}", (bx1, by1, bx2, by2))

    print(f"wrote Doc{DOC} Raw + components visual aids to {RESULTS}")


if __name__ == "__main__":
    main()
