from pathlib import Path

from PIL import Image


RAW_DIR = Path(__file__).resolve().parents[1]
RAW_IMAGE = RAW_DIR / "raw -- npp_schematic_improved_no_overlap.png"
OUT_DIR = RAW_DIR / "codes" / "crops"


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    img.crop(box).save(OUT_DIR / f"{name}.png")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.open(RAW_IMAGE)
    img.save(OUT_DIR / "full_sheet.png")

    crops = {
        "top_4160_sources_and_tie": (220, 190, 4250, 1120),
        "left_top_train_a_source": (230, 220, 2200, 1150),
        "center_tie_ground_relays": (1800, 760, 3000, 1900),
        "right_top_train_b_source": (2500, 220, 4300, 1150),
        "left_dc_stack_and_rps": (100, 960, 620, 2550),
        "right_dc_stack_and_rps": (4040, 960, 4560, 2550),
        "left_dc_stack_wide": (80, 850, 1500, 2350),
        "right_dc_stack_wide": (3300, 850, 4650, 2350),
        "train_a_480_mcc_loads": (560, 1370, 2220, 2520),
        "train_b_480_mcc_loads": (2480, 1370, 4170, 2520),
        "bottom_control_room": (1600, 2230, 3850, 2680),
        "left_rps_relay_jb": (240, 1780, 2050, 2650),
        "right_rps_relay_jb": (3120, 1780, 4560, 2650),
        "notes_schedules": (4500, 220, 5380, 2520),
        "title_block": (3650, 2520, 5390, 3260),
        "revision_block": (180, 2600, 3600, 3260),
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
