from __future__ import annotations

from pathlib import Path

from PIL import Image


RAW_DIR = Path(__file__).resolve().parents[1]
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_v2(1).png"
CROP_DIR = RAW_DIR / "codes" / "crops"
CROP_DIR.mkdir(parents=True, exist_ok=True)


def crop(name: str, box: tuple[int, int, int, int], image: Image.Image) -> None:
    image.crop(box).save(CROP_DIR / f"{name}.png")


def main() -> None:
    image = Image.open(RAW_IMAGE).convert("RGB")
    width, height = image.size

    crop("full_sheet", (0, 0, width, height), image)
    crop("top_sources", (1480, 120, 3460, 620), image)
    crop("upper_left_train_a", (160, 430, 2500, 1510), image)
    crop("upper_center_tie", (2300, 420, 2900, 1350), image)
    crop("upper_right_train_b", (2600, 430, 4920, 1510), image)
    crop("lower_train_a", (190, 1390, 2530, 2780), image)
    crop("lower_center_dc_rps_esf", (1850, 1850, 3340, 3170), image)
    crop("lower_train_b", (2580, 1390, 4930, 2780), image)
    crop("dc_a_focus", (1850, 1830, 2550, 2740), image)
    crop("dc_b_focus", (2580, 1830, 3280, 2740), image)
    crop("bottom_panels", (1820, 2600, 3370, 3180), image)
    crop("notes_title", (3720, 980, 4920, 3210), image)
    crop("legend_revision", (150, 140, 1220, 3210), image)

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
