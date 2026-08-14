from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


Image.MAX_IMAGE_PIXELS = None

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\36\Raw + wires")
CODES = BASE / "codes"
CROPS = CODES / "crops"
RESULTS = BASE / "results"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_v2.png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"

CROPS_DEF = {
    "overview": (0, 0, 4800, 3400),
    "working_area": (80, 80, 4650, 3300),
    "top_left": (80, 80, 1700, 1250),
    "top_center": (1550, 80, 3250, 1250),
    "top_right": (3100, 80, 4650, 1250),
    "mid_left": (80, 1050, 1700, 2350),
    "mid_center": (1550, 1050, 3250, 2350),
    "mid_right": (3100, 1050, 4650, 2350),
    "bottom_left": (80, 2150, 1700, 3300),
    "bottom_center": (1550, 2150, 3250, 3300),
    "bottom_right": (3100, 2150, 4650, 3300),
    "central_ties": (2100, 900, 2900, 2500),
    "left_control": (80, 1850, 2350, 3300),
    "right_control": (2450, 1850, 4650, 3300),
    "top_power_bus_ties": (450, 240, 4400, 1450),
    "left_480_loads": (450, 1150, 2400, 2350),
    "right_480_loads": (2350, 1150, 4350, 2350),
    "left_dc_control": (450, 2050, 2350, 3200),
    "right_dc_control": (2450, 2050, 4350, 3200),
}


def save_crop(image: Image.Image, source_name: str, crop_name: str, box: tuple[int, int, int, int]) -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    x0, y0, x1, y1 = box
    x0 = max(0, min(image.width, x0))
    y0 = max(0, min(image.height, y0))
    x1 = max(0, min(image.width, x1))
    y1 = max(0, min(image.height, y1))
    if x1 <= x0 or y1 <= y0:
        return
    crop = image.crop((x0, y0, x1, y1))
    if crop_name == "overview":
        preview = crop.copy()
        preview.thumbnail((2400, 1700), Image.Resampling.LANCZOS)
        preview.save(CROPS / f"{source_name}__{crop_name}.png")
        return
    crop.save(CROPS / f"{source_name}__{crop_name}.png")
    crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS).save(
        CROPS / f"{source_name}__{crop_name}_2x.png"
    )


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    mask_inv = ImageOps.invert(Image.open(MASK).convert("L")).convert("RGB")

    for source_name, image in {"raw": raw, "wires_overlay": overlay, "wires_mask_inv": mask_inv}.items():
        for crop_name, box in CROPS_DEF.items():
            save_crop(image, source_name, crop_name, box)

    print(f"crops: {CROPS}")
    print(f"source size: {raw.size[0]}x{raw.size[1]}")


if __name__ == "__main__":
    main()
