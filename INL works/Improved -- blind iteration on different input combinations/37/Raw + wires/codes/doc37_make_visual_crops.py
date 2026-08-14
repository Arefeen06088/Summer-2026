from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


Image.MAX_IMAGE_PIXELS = None

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\37\Raw + wires"
)
CODES = BASE / "codes"
CROPS = CODES / "crops"
RESULTS = BASE / "results"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_v2(1).png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"

CROPS_DEF = {
    "overview": (0, 0, 5100, 3300),
    "working_area": (80, 70, 4980, 3200),
    "top_left": (80, 70, 1850, 1180),
    "top_center": (1650, 70, 3450, 1180),
    "top_right": (3250, 70, 4980, 1180),
    "mid_left": (80, 1020, 1850, 2200),
    "mid_center": (1650, 1020, 3450, 2200),
    "mid_right": (3250, 1020, 4980, 2200),
    "bottom_left": (80, 2050, 1850, 3200),
    "bottom_center": (1650, 2050, 3450, 3200),
    "bottom_right": (3250, 2050, 4980, 3200),
    "top_power_bus_ties": (430, 190, 4650, 1450),
    "central_ties": (2050, 860, 3100, 2450),
    "left_480_loads": (420, 1120, 2550, 2320),
    "right_480_loads": (2500, 1120, 4650, 2320),
    "left_dc_control": (420, 1970, 2550, 3180),
    "right_dc_control": (2500, 1970, 4650, 3180),
    "lower_controls_wide": (350, 1700, 4750, 3200),
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
        preview.thumbnail((2600, 1700), Image.Resampling.LANCZOS)
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

    print(f"source size: {raw.size[0]}x{raw.size[1]}")
    for source_name, image in {"raw": raw, "wires_overlay": overlay, "wires_mask_inv": mask_inv}.items():
        for crop_name, box in CROPS_DEF.items():
            save_crop(image, source_name, crop_name, box)
    print(f"crops: {CROPS}")


if __name__ == "__main__":
    main()
