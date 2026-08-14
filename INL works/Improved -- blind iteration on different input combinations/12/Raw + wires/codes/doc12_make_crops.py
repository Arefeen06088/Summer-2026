from pathlib import Path
from PIL import Image

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\12\Raw + wires")
OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc12_work\crops")

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_rps_rerouted.png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


def crop_named(image_path: Path, prefix: str, boxes: dict[str, tuple[int, int, int, int]]) -> None:
    img = Image.open(image_path)
    for name, box in boxes.items():
        img.crop(box).save(OUT / f"{prefix}_{name}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    boxes = {
        "full_left_and_center": (120, 120, 3250, 2500),
        "top_4160_sources_left": (180, 120, 1750, 760),
        "top_4160_sources_right": (1700, 120, 3250, 760),
        "train_a_480_mcc1": (180, 650, 1400, 1450),
        "train_a_mcc2_and_dc_left": (180, 1360, 1500, 2150),
        "train_b_480_mcc1": (1750, 650, 3050, 1450),
        "train_b_mcc2_and_dc_right": (1750, 1360, 3050, 2150),
        "center_bus_tie": (1350, 430, 2050, 780),
        "left_dc_bus": (1020, 1830, 1880, 2310),
        "right_dc_bus": (1680, 1830, 2500, 2310),
        "bottom_control_logic": (760, 2180, 3050, 2800),
        "bottom_left_control": (760, 2170, 1700, 2800),
        "bottom_right_control": (1600, 2170, 3050, 2800),
        "right_notes_title": (3220, 190, 4100, 2850),
    }
    crop_named(RAW, "raw", boxes)
    crop_named(OVERLAY, "overlay", boxes)

    img = Image.open(RAW)
    w, h = img.size
    for row in range(3):
        for col in range(4):
            left = int(col * w / 4)
            upper = int(row * h / 3)
            right = int((col + 1) * w / 4)
            lower = int((row + 1) * h / 3)
            img.crop((left, upper, right, lower)).save(OUT / f"raw_grid_r{row + 1}_c{col + 1}.png")

    overlay = Image.open(OVERLAY)
    for row in range(3):
        for col in range(4):
            left = int(col * w / 4)
            upper = int(row * h / 3)
            right = int((col + 1) * w / 4)
            lower = int((row + 1) * h / 3)
            overlay.crop((left, upper, right, lower)).save(OUT / f"overlay_grid_r{row + 1}_c{col + 1}.png")

    Image.open(MASK).save(OUT / "wires_mask_full.png")


if __name__ == "__main__":
    main()
