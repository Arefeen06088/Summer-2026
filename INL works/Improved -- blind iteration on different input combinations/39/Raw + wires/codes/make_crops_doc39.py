from pathlib import Path

from PIL import Image, ImageOps


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\39\Raw + wires")
OUT = BASE / "codes" / "crops"

RAW = BASE / "raw -- npp_schematic_improved_no_overlap.png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


REGIONS = {
    "overview": (0, 0, 5500, 3362),
    "drawing_area": (120, 120, 4340, 2550),
    "title_and_notes": (3650, 150, 5350, 3180),
    "left_train_full": (160, 150, 2220, 2570),
    "right_train_full": (2350, 150, 4350, 2570),
    "top_bus_tie": (520, 160, 3150, 1210),
    "left_top_power": (470, 190, 1780, 1040),
    "right_top_power": (2810, 190, 4200, 1040),
    "center_tie_relays": (1680, 780, 2860, 1540),
    "left_480_loads": (480, 1080, 2250, 2520),
    "right_480_loads": (2370, 1080, 4110, 2520),
    "left_dc_control": (100, 970, 920, 2560),
    "right_dc_control": (4010, 970, 4460, 2560),
    "left_control_lower_wide": (80, 1600, 2400, 2640),
    "right_control_lower_wide": (2700, 1600, 4450, 2640),
    "bottom_controls": (300, 1950, 4380, 2570),
    "annunciation_center": (1850, 2260, 3400, 2550),
    "jb_a101_ann_detail": (1650, 2120, 3050, 2580),
    "jb_b101_ann_detail": (3250, 2120, 4300, 2580),
    "left_bottom_devices": (320, 1900, 2200, 2470),
    "right_bottom_devices": (2400, 1900, 4140, 2470),
}


def save_crop(img: Image.Image, name: str, bbox: tuple[int, int, int, int], suffix: str, scale: int = 1) -> None:
    crop = img.crop(bbox)
    if scale != 1:
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.LANCZOS)
    crop.save(OUT / f"{name}_{suffix}{'_2x' if scale != 1 else ''}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    mask = Image.open(MASK).convert("L")
    mask_inv = ImageOps.invert(mask)

    for name, bbox in REGIONS.items():
        save_crop(raw, name, bbox, "raw")
        save_crop(overlay, name, bbox, "overlay")
        save_crop(mask_inv, name, bbox, "mask_inv")
        if name != "overview":
            save_crop(raw, name, bbox, "raw", scale=2)
            save_crop(overlay, name, bbox, "overlay", scale=2)
            save_crop(mask_inv, name, bbox, "mask_inv", scale=2)

    print(f"Wrote crops to {OUT}")


if __name__ == "__main__":
    main()
