from __future__ import annotations

from pathlib import Path

from PIL import Image


DOC = "15"
RESOURCE_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw + wires"
)
RAW = RESOURCE_DIR / "raw -- improved_synthetic_nuclear_electrical_schematic.png"
OVERLAY = RESOURCE_DIR / "wires_mask_overlay.png"
MASK = RESOURCE_DIR / "wires_mask.png"
OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc15_work\crops")


BOXES = {
    "full_schematic_left": (250, 80, 6250, 3700),
    "offsite_sources_top": (450, 70, 6100, 620),
    "division_1a_full": (330, 460, 1900, 3650),
    "division_1b_full": (1800, 460, 3350, 3650),
    "division_2a_full": (3250, 460, 4900, 3650),
    "division_2b_full": (4750, 460, 6350, 3650),
    "div_1a_top_safety": (430, 430, 1850, 1450),
    "div_1b_top_safety": (1820, 430, 3290, 1450),
    "div_2a_top_safety": (3300, 430, 4800, 1450),
    "div_2b_top_safety": (4800, 430, 6300, 1450),
    "div_1a_mcc": (430, 1450, 1840, 2860),
    "div_1b_mcc": (1840, 1450, 3290, 2860),
    "div_2a_mcc": (3330, 1450, 4800, 2860),
    "div_2b_mcc": (4820, 1450, 6300, 2860),
    "div_1a_dc_ups": (430, 2800, 1850, 3650),
    "div_1b_dc_ups": (1840, 2800, 3290, 3650),
    "div_2a_dc_ups": (3330, 2800, 4800, 3650),
    "div_2b_dc_ups": (4820, 2800, 6300, 3650),
    "tie_1a_1b": (1550, 500, 2100, 1450),
    "tie_2a_2b": (4500, 500, 5100, 1450),
    "right_notes": (6250, 430, 7420, 3450),
    "title_block": (5250, 4300, 7380, 4860),
    "revision_block": (120, 4300, 1700, 4860),
}


def save_crops(source: Path, prefix: str) -> None:
    with Image.open(source) as img:
        for name, box in BOXES.items():
            crop = img.crop(box)
            crop.save(OUT / f"{prefix}_{name}.png")

        width, height = img.size
        cols = 4
        rows = 4
        for row in range(rows):
            for col in range(cols):
                left = round(col * width / cols)
                top = round(row * height / rows)
                right = round((col + 1) * width / cols)
                bottom = round((row + 1) * height / rows)
                img.crop((left, top, right, bottom)).save(OUT / f"{prefix}_grid_r{row + 1}_c{col + 1}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    save_crops(RAW, "raw")
    save_crops(OVERLAY, "overlay")
    with Image.open(MASK) as mask:
        mask.save(OUT / "wires_mask_full.png")
    print(f"wrote crops to {OUT}")


if __name__ == "__main__":
    main()
