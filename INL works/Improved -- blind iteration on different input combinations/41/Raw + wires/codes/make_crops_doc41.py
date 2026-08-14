from pathlib import Path

from PIL import Image, ImageOps


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\41\Raw + wires"
)
OUT = BASE / "codes" / "crops"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic(2).png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


REGIONS = {
    "overview": (0, 0, 4800, 3200),
    "drawing_area": (180, 180, 3840, 3060),
    "top_switchgear_full": (250, 230, 3820, 990),
    "top_switchgear_train_a": (260, 250, 2050, 980),
    "top_switchgear_train_b": (2000, 250, 3820, 980),
    "top_tie_detail": (1780, 440, 2300, 760),
    "left_480_loads": (260, 930, 2120, 2240),
    "right_480_loads": (2080, 930, 3820, 2240),
    "left_mcc_load_detail": (380, 1380, 2050, 2240),
    "right_mcc_load_detail": (2180, 1380, 3720, 2240),
    "rps_interlocks_center": (1600, 2050, 2950, 2580),
    "rps_a_detail": (1650, 2100, 2300, 2580),
    "rps_b_detail": (2260, 2100, 2920, 2580),
    "bottom_dc_ups_full": (250, 2280, 3840, 3020),
    "left_vital_dc": (300, 2300, 2080, 3020),
    "right_vital_dc": (2200, 2300, 3820, 3020),
    "instrument_rack_ups": (1680, 2500, 2720, 3000),
    "notes": (3820, 280, 4580, 1230),
    "legend_reference": (3820, 1240, 4580, 2090),
    "terminal_schedule": (3820, 2100, 4580, 2380),
    "title_block": (3820, 2600, 4580, 3070),
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
