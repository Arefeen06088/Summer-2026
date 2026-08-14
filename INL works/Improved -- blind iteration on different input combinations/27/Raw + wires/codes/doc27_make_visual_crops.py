from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\27\Raw + wires"
)
CODES = BASE / "codes"
CROPS = CODES / "crops"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_readable.png"
MASK = BASE / "wires_mask.png"
OVERLAY = BASE / "wires_mask_overlay.png"


def save_crop(image: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = box
    left = max(0, left)
    top = max(0, top)
    right = min(image.width, right)
    bottom = min(image.height, bottom)
    image.crop((left, top, right, bottom)).save(CROPS / f"{name}.png")


def save_resized(image: Image.Image, name: str, width: int) -> None:
    height = round(image.height * width / image.width)
    image.resize((width, height), Image.Resampling.LANCZOS).save(CROPS / f"{name}.png")


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    mask = Image.open(MASK).convert("L")
    mask_inv = ImageOps.invert(mask)

    print(f"raw={RAW.name} size={raw.width}x{raw.height}")
    save_resized(raw, "raw__overview_large", 2600)
    save_resized(overlay, "wires_overlay__overview_large", 2600)
    save_resized(mask_inv.convert("RGB"), "wires_mask_inv__overview_large", 2600)

    w, h = raw.size
    regions = {
        "top_band": (0, 0, w, 1120),
        "top_source_bus": (0, 360, w, 1560),
        "upper_left_trains": (0, 440, 3600, 2420),
        "upper_right_trains": (3300, 440, w, 2420),
        "mid_left_loads": (0, 1720, 3650, 3300),
        "mid_right_loads": (3300, 1720, w, 3300),
        "bottom_left_controls": (0, 2700, 3650, h),
        "bottom_right_controls": (3300, 2700, w, h),
        "bottom_controls_wide": (0, 2500, w, h),
        "title_notes": (5100, 0, w, h),
        "count_strip": (5150, 1800, w, 3050),
        "left_core": (0, 850, 3900, 3600),
        "right_core": (3100, 850, w, 3600),
        "lower_center": (2100, 2500, 5150, h),
        "focus_a_rcp_interlock": (1160, 750, 1780, 1730),
        "focus_b_rcp_interlock": (4440, 750, 5080, 1730),
        "focus_a_mov_controls": (0, 1850, 3600, 3520),
        "focus_b_mov_controls": (3250, 1850, w, 3520),
        "focus_a_dc_ups_controls": (0, 2500, 3950, h),
        "focus_b_dc_ups_controls": (3050, 2500, w, h),
        "zoom_rcp_a": (1230, 760, 1660, 1705),
        "zoom_rcp_b": (4505, 760, 4945, 1705),
        "zoom_a10_dc": (2850, 2600, 4550, 4100),
        "zoom_b01_dc": (3950, 2600, 5650, 4100),
        "zoom_dc_panel": (3300, 3050, 4900, 4200),
        "zoom_a10_b01_dc": (3000, 2550, 5600, 4200),
        "zoom_c_ground": (950, 3150, 2300, 5950),
        "zoom_d_ground": (6600, 3150, 8050, 5950),
    }
    for label, box in regions.items():
        save_crop(raw, f"raw__{label}", box)
        save_crop(overlay, f"wires_overlay__{label}", box)

    cols, rows = 5, 4
    for y in range(rows):
        for x in range(cols):
            box = (
                round(w * x / cols),
                round(h * y / rows),
                round(w * (x + 1) / cols),
                round(h * (y + 1) / rows),
            )
            save_crop(raw, f"raw__grid_r{y + 1}c{x + 1}", box)
            save_crop(overlay, f"wires_overlay__grid_r{y + 1}c{x + 1}", box)

    print(f"wrote crops to {CROPS}")


if __name__ == "__main__":
    main()
