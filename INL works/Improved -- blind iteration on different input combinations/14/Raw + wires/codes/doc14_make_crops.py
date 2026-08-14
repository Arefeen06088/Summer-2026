from pathlib import Path
from PIL import Image

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\14\Raw + wires")
OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc14_work\crops")

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


def crop_named(path: Path, prefix: str, boxes: dict[str, tuple[int, int, int, int]]) -> None:
    img = Image.open(path)
    for name, box in boxes.items():
        img.crop(box).save(OUT / f"{prefix}_{name}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    boxes = {
        "full_left_train_a": (420, 220, 2850, 2920),
        "full_right_train_b": (3000, 220, 5300, 2920),
        "top_train_a_safety": (560, 260, 2750, 1450),
        "top_train_b_safety": (3060, 260, 5280, 1450),
        "loadcenter_a": (560, 1450, 2760, 2820),
        "loadcenter_b": (3060, 1450, 5280, 2820),
        "center_ties": (2550, 600, 3260, 1850),
        "bottom_dc_ups_a": (560, 2700, 2830, 4020),
        "bottom_dc_ups_b": (3040, 2700, 5320, 4020),
        "terminal_blocks": (480, 3630, 3400, 4120),
        "right_notes_title": (5350, 250, 6420, 3920),
        "left_mcc_detail": (1160, 1460, 2740, 2700),
        "right_mcc_detail": (3650, 1460, 5280, 2700),
        "left_top_branch_detail": (1480, 620, 2680, 1450),
        "right_top_branch_detail": (3970, 620, 5180, 1450),
        "bottom_center_transfer": (2460, 2740, 3560, 4040),
    }
    crop_named(RAW, "raw", boxes)
    crop_named(OVERLAY, "overlay", boxes)

    raw = Image.open(RAW)
    overlay = Image.open(OVERLAY)
    w, h = raw.size
    for row in range(3):
        for col in range(4):
            box = (
                int(col * w / 4),
                int(row * h / 3),
                int((col + 1) * w / 4),
                int((row + 1) * h / 3),
            )
            raw.crop(box).save(OUT / f"raw_grid_r{row + 1}_c{col + 1}.png")
            overlay.crop(box).save(OUT / f"overlay_grid_r{row + 1}_c{col + 1}.png")

    Image.open(MASK).save(OUT / "wires_mask_full.png")


if __name__ == "__main__":
    main()
