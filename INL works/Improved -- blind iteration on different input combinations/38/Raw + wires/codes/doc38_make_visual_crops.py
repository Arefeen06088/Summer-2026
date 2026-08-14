from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires")
CROP_DIR = ROOT / "codes" / "crops"
CROP_DIR.mkdir(parents=True, exist_ok=True)

RAW = ROOT / "raw -- synthetic_npp_schematic_improved.png"
OVERLAY = ROOT / "wires_mask_overlay.png"
MASK = ROOT / "wires_mask.png"


CROPS = {
    "overview": (0, 0, 5100, 3300),
    "working_area": (0, 0, 5100, 2600),
    "top_left": (0, 0, 1700, 1100),
    "top_center": (1300, 0, 3400, 1200),
    "top_right": (3000, 0, 5100, 1200),
    "mid_left": (0, 650, 2100, 1900),
    "mid_center": (1500, 650, 3600, 2000),
    "mid_right": (3000, 650, 5100, 2000),
    "bottom_left": (0, 1700, 2000, 3300),
    "bottom_center": (1600, 1700, 3700, 3300),
    "bottom_right": (3100, 1700, 5100, 3300),
    "top_power_bus_ties": (300, 0, 4300, 1500),
    "central_ties": (1900, 650, 4000, 1850),
    "left_480_loads": (0, 1100, 2800, 2300),
    "right_480_loads": (2300, 1100, 5100, 2300),
    "left_dc_control": (1500, 1450, 4300, 2650),
    "right_dc_control": (2600, 1450, 5100, 2650),
    "lower_controls_wide": (0, 1650, 5000, 3050),
}


def save_crops(source: Path, prefix: str, invert_mask: bool = False) -> None:
    image = Image.open(source)
    if invert_mask:
        image = ImageOps.invert(image.convert("L")).convert("RGB")
    else:
        image = image.convert("RGB")
    for name, box in CROPS.items():
        crop = image.crop(box)
        crop.save(CROP_DIR / f"{prefix}__{name}.png")
        if name != "overview":
            crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS).save(
                CROP_DIR / f"{prefix}__{name}_2x.png"
            )


def main() -> None:
    save_crops(RAW, "raw")
    save_crops(OVERLAY, "wires_overlay")
    save_crops(MASK, "wires_mask_inv", invert_mask=True)
    print(f"source size: {Image.open(RAW).size[0]}x{Image.open(RAW).size[1]}")
    print(f"crops: {CROP_DIR}")


if __name__ == "__main__":
    main()
