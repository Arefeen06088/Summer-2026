from __future__ import annotations

from pathlib import Path

from PIL import Image


RAW_DIR = Path(__file__).resolve().parents[1]
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_revised_v4.png"
OUT_DIR = RAW_DIR / "codes" / "crops"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def crop(img: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    width, height = img.size
    left, top, right, bottom = box
    left = max(0, min(width, left))
    right = max(0, min(width, right))
    top = max(0, min(height, top))
    bottom = max(0, min(height, bottom))
    if left >= right or top >= bottom:
        raise ValueError(f"Invalid crop {name}: {box}")
    img.crop((left, top, right, bottom)).save(OUT_DIR / f"{name}.png")


def main() -> None:
    img = Image.open(RAW_IMAGE).convert("RGB")
    w, h = img.size
    crop(img, "full_sheet", (0, 0, w, h))
    crop(img, "drawing_area", (120, 140, w - 140, h - 250))
    crop(img, "top_overview", (120, 120, w - 140, 1450))
    crop(img, "middle_overview", (120, 1250, w - 140, 3000))
    crop(img, "lower_overview", (120, 2750, w - 140, h - 220))
    crop(img, "left_full_height", (120, 140, 2500, h - 220))
    crop(img, "center_full_height", (2150, 140, 4550, h - 220))
    crop(img, "right_full_height", (4200, 140, w - 140, h - 220))

    # 3 x 4 grid crops across the primary drawing body.
    body_left, body_top, body_right, body_bottom = 120, 140, w - 140, h - 220
    cols, rows = 4, 3
    col_w = (body_right - body_left) // cols
    row_h = (body_bottom - body_top) // rows
    pad = 90
    for r in range(rows):
        for c in range(cols):
            left = body_left + c * col_w - pad
            right = body_left + (c + 1) * col_w + pad
            top = body_top + r * row_h - pad
            bottom = body_top + (r + 1) * row_h + pad
            crop(img, f"grid_r{r + 1}_c{c + 1}", (left, top, right, bottom))

    # Focus crops for expected dense schematic bands.
    crop(img, "upper_sources", (280, 320, w - 260, 1200))
    crop(img, "left_feeders", (260, 900, 2600, 2850))
    crop(img, "center_feeders", (2100, 900, 4700, 2850))
    crop(img, "right_feeders", (4000, 900, w - 260, 2850))
    crop(img, "lower_controls_left", (260, 2450, 2750, h - 430))
    crop(img, "lower_controls_center", (2250, 2450, 4750, h - 430))
    crop(img, "lower_controls_right", (4100, 2450, w - 260, h - 430))
    crop(img, "title_notes_legend", (300, h - 900, w - 300, h - 120))
    crop(img, "focus_train_a_feeder_01", (350, 760, 1250, 2450))
    crop(img, "focus_train_b_feeder_01", (2350, 760, 3250, 2450))
    crop(img, "focus_train_c_feeder_01", (4100, 760, 5000, 2450))
    crop(img, "focus_lower_rps_tc", (2500, 2940, 5650, 4320))

    print(f"Generated crops in {OUT_DIR}")


if __name__ == "__main__":
    main()
