from pathlib import Path
from PIL import Image

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw + wires")
OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc13_work\crops")

RAW = BASE / "raw -- synthetic diagram _.png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


def crop_named(image_path: Path, prefix: str, boxes: dict[str, tuple[int, int, int, int]]) -> None:
    img = Image.open(image_path)
    for name, box in boxes.items():
        crop = img.crop(box)
        crop.save(OUT / f"{prefix}_{name}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    boxes = {
        "full_left_logic": (180, 300, 5150, 3650),
        "startup_feed_top_left": (280, 360, 2100, 850),
        "train_A_upper_left": (360, 760, 2520, 1840),
        "train_B_upper_right": (2620, 760, 4820, 1840),
        "train_C_lower_left": (360, 1940, 2520, 3270),
        "train_D_lower_right": (2620, 1940, 4820, 3270),
        "train_A_dc_right": (2140, 1110, 2570, 1810),
        "train_B_dc_right": (4420, 1110, 4850, 1810),
        "train_C_dc_right": (2140, 2290, 2570, 3250),
        "train_D_dc_right": (4420, 2290, 4850, 3250),
        "middle_intertrain_bus": (140, 1780, 5060, 2260),
        "bottom_ground_and_dc": (350, 3000, 3200, 3700),
        "right_notes_legend_schedule": (5060, 150, 6250, 3060),
        "title_block": (5000, 3340, 6260, 4160),
    }

    crop_named(RAW, "raw", boxes)
    crop_named(OVERLAY, "overlay", boxes)

    # Coarse grid keeps a fallback visual record for the subagents.
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

    mask = Image.open(MASK)
    mask.save(OUT / "wires_mask_full.png")


if __name__ == "__main__":
    main()
