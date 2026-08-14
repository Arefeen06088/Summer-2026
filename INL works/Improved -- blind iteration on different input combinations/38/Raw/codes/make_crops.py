from pathlib import Path

from PIL import Image


RAW_DIR = Path(__file__).resolve().parents[1]
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_schematic_improved.png"
OUT_DIR = RAW_DIR / "codes" / "crops"


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    crop = img.crop(box)
    crop.save(OUT_DIR / f"{name}.png")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.open(RAW_IMAGE)
    img.save(OUT_DIR / "full_sheet.png")

    crops = {
        "top_sources_and_4160_buses": (190, 180, 3620, 850),
        "upper_left_train_a_sources": (350, 250, 1700, 1000),
        "upper_center_tie_and_transformers": (1200, 250, 3300, 1050),
        "upper_right_train_b_sources": (2500, 250, 3700, 1000),
        "left_train_a_mcc_loads": (360, 850, 2050, 1950),
        "right_train_b_mcc_loads": (2150, 850, 3700, 1950),
        "lower_left_dc_ac_controls": (350, 1750, 2050, 2700),
        "lower_right_dc_ac_controls": (2200, 1750, 3700, 2700),
        "center_lower_control_crossovers": (1400, 1800, 3600, 2800),
        "left_ground_and_cable_routes": (300, 650, 1200, 3050),
        "right_cable_routes": (3200, 650, 3800, 2750),
        "notes_and_schedules": (3650, 240, 4770, 2600),
        "title_block": (3500, 2650, 4880, 3180),
    }
    for name, box in crops.items():
        save_crop(img, name, box)

    width, height = img.size
    for row in range(4):
        for col in range(4):
            left = col * width // 4
            upper = row * height // 4
            right = (col + 1) * width // 4
            lower = (row + 1) * height // 4
            save_crop(img, f"grid_r{row + 1}_c{col + 1}", (left, upper, right, lower))

    print(f"Wrote crops to {OUT_DIR}")


if __name__ == "__main__":
    main()
