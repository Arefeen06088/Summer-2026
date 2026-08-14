from __future__ import annotations

from pathlib import Path

from PIL import Image


RAW_DIR = Path(__file__).resolve().parents[1]
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_v2.png"
CROP_DIR = RAW_DIR / "codes" / "crops"
CROP_DIR.mkdir(parents=True, exist_ok=True)


def crop(name: str, box: tuple[int, int, int, int], image: Image.Image) -> None:
    image.crop(box).save(CROP_DIR / f"{name}.png")


def main() -> None:
    image = Image.open(RAW_IMAGE).convert("RGB")
    width, height = image.size

    crop("full_sheet", (0, 0, width, height), image)
    crop("top_sources", (120, 110, 4680, 880), image)
    crop("upper_left_sources", (120, 120, 1300, 850), image)
    crop("upper_center_buses", (1180, 480, 3600, 900), image)
    crop("upper_right_sources", (3520, 120, 4680, 850), image)
    crop("mid_4160", (1120, 820, 3720, 1660), image)
    crop("train_a_4160", (1120, 880, 2380, 1660), image)
    crop("train_b_4160", (2460, 880, 3720, 1660), image)
    crop("lower_loads_overview", (480, 1520, 4320, 3180), image)
    crop("train_a_loads", (480, 1520, 2300, 3060), image)
    crop("train_b_loads", (2450, 1520, 4320, 3060), image)
    crop("dc_control_center", (2020, 1420, 2820, 3040), image)
    crop("train_a_dc", (520, 2500, 2200, 3230), image)
    crop("train_b_dc", (2600, 2500, 4320, 3230), image)
    crop("title_notes_legend", (60, 2920, 4680, 3330), image)

    # Uniform grid crops are useful for quick independent review.
    rows = 4
    cols = 4
    for row in range(rows):
        for col in range(cols):
            x1 = int(col * width / cols)
            y1 = int(row * height / rows)
            x2 = int((col + 1) * width / cols)
            y2 = int((row + 1) * height / rows)
            crop(f"grid_r{row + 1}_c{col + 1}", (x1, y1, x2, y2), image)

    print(f"Wrote crops to {CROP_DIR}")


if __name__ == "__main__":
    main()
