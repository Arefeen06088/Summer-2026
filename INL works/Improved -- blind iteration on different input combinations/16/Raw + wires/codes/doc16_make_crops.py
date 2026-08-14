from pathlib import Path

from PIL import Image, ImageOps


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\16\Raw + wires")
OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc16_work\crops")

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_revised(1).png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    x0, y0, x1, y1 = box
    x0 = max(0, min(img.width, x0))
    y0 = max(0, min(img.height, y0))
    x1 = max(0, min(img.width, x1))
    y1 = max(0, min(img.height, y1))
    if x1 <= x0 or y1 <= y0:
        return
    img.crop((x0, y0, x1, y1)).save(OUT / name)


def save_preview(img: Image.Image, name: str, max_side: int = 1800) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    preview = img.copy()
    preview.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    preview.save(OUT / name)


def main() -> None:
    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    mask = Image.open(MASK).convert("L")
    inv_mask = ImageOps.invert(mask).convert("RGB")

    save_preview(raw, "raw_full_preview.png")
    save_preview(overlay, "overlay_full_preview.png")
    save_preview(inv_mask, "mask_full_preview_inverted.png")

    w, h = raw.size

    # Coarse grid: enough overlap to read labels close to crop boundaries.
    cols = 4
    rows = 4
    pad_x = 90
    pad_y = 80
    for row in range(rows):
        for col in range(cols):
            x0 = int(col * w / cols) - pad_x
            y0 = int(row * h / rows) - pad_y
            x1 = int((col + 1) * w / cols) + pad_x
            y1 = int((row + 1) * h / rows) + pad_y
            save_crop(raw, f"raw_grid_r{row+1}c{col+1}.png", (x0, y0, x1, y1))
            save_crop(overlay, f"overlay_grid_r{row+1}c{col+1}.png", (x0, y0, x1, y1))

    # Larger bands and likely dense zones for single-line schematics.
    boxes = {
        "top_band": (0, 0, w, int(h * 0.28)),
        "upper_middle_band": (0, int(h * 0.20), w, int(h * 0.50)),
        "middle_band": (0, int(h * 0.40), w, int(h * 0.72)),
        "bottom_band": (0, int(h * 0.65), w, h),
        "left_half": (0, 0, int(w * 0.54), h),
        "right_half": (int(w * 0.46), 0, w, h),
        "center": (int(w * 0.20), int(h * 0.18), int(w * 0.82), int(h * 0.82)),
        "title_block": (int(w * 0.58), int(h * 0.78), w, h),
        "notes_right": (int(w * 0.72), 0, w, int(h * 0.82)),
    }
    for name, box in boxes.items():
        save_crop(raw, f"raw_{name}.png", box)
        save_crop(overlay, f"overlay_{name}.png", box)

    close_boxes = {
        "close_480_tie_cb31a": (1280, 760, 1880, 1220),
        "close_mcc31a_cb11b": (1450, 780, 2250, 1250),
        "close_cb31a_label": (1460, 780, 1780, 1060),
        "close_cb11a_12a_21a": (250, 760, 1350, 1220),
        "close_cb11a": (300, 820, 700, 1160),
        "close_cb12a": (650, 820, 1050, 1160),
        "close_cb21a": (1000, 820, 1400, 1160),
        "close_vital_a": (430, 1690, 1500, 2270),
        "close_vital_b": (1900, 1690, 2950, 2270),
        "close_rps_control_a": (160, 1380, 1160, 1900),
        "close_rps_control_b": (1830, 1380, 2880, 1900),
        "close_esf_instruments": (1030, 1410, 1820, 1950),
        "close_b_instr": (2440, 1410, 3200, 1900),
    }
    for name, box in close_boxes.items():
        crop = raw.crop(box)
        crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS).save(OUT / f"{name}.png")

    print(f"wrote crops to {OUT}")
    print(f"source size={w}x{h}")


if __name__ == "__main__":
    main()
