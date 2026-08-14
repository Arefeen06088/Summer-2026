from __future__ import annotations

from pathlib import Path
from PIL import Image


RAW_DIR = Path(__file__).resolve().parents[1]
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic(2).png"
CROP_DIR = RAW_DIR / "codes" / "crops"


CROPS = {
    "full_sheet": (0, 0, 4800, 3200),
    "top_train_a_4160": (240, 230, 2080, 1030),
    "top_train_b_4160": (1980, 230, 3820, 1030),
    "middle_train_a_loads": (240, 900, 2180, 2140),
    "middle_train_b_loads": (2100, 900, 3820, 2140),
    "bottom_vital_power_rps": (240, 2000, 3820, 3000),
    "center_rps_interlocks": (1640, 1780, 2960, 2630),
    "left_dc_and_rps": (280, 2020, 2080, 3000),
    "right_dc_and_rps": (2250, 2020, 3820, 3000),
    "bottom_center_ups_rps_detail": (1750, 2050, 3300, 2770),
    "right_notes_legend_title": (3740, 250, 4560, 3050),
    "legend_line_types": (3740, 1260, 4560, 1770),
    "terminal_schedule_title": (3740, 2050, 4560, 3050),
}


def main() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.open(RAW_IMAGE)
    for name, box in CROPS.items():
        crop = img.crop(box)
        crop.save(CROP_DIR / f"{name}.png")

    # Grid crops provide independent coverage without relying on any external derived resources.
    cols, rows = 4, 4
    w, h = img.size
    for r in range(rows):
        for c in range(cols):
            left = c * w // cols
            top = r * h // rows
            right = (c + 1) * w // cols
            bottom = (r + 1) * h // rows
            img.crop((left, top, right, bottom)).save(CROP_DIR / f"grid_r{r+1}_c{c+1}.png")


if __name__ == "__main__":
    main()
