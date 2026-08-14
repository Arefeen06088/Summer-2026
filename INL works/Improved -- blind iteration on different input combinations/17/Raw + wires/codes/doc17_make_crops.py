from pathlib import Path

from PIL import Image, ImageOps


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\17\Raw + wires")
OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc17_work\crops")

RAW = BASE / "raw -- synthetic_npp_aux_power_schematic_overlap_fixed.png"
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


def save_preview(img: Image.Image, name: str, max_side: int = 1900) -> None:
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
    cols = 4
    rows = 4
    pad_x = 120
    pad_y = 110
    for row in range(rows):
        for col in range(cols):
            x0 = int(col * w / cols) - pad_x
            y0 = int(row * h / rows) - pad_y
            x1 = int((col + 1) * w / cols) + pad_x
            y1 = int((row + 1) * h / rows) + pad_y
            save_crop(raw, f"raw_grid_r{row+1}c{col+1}.png", (x0, y0, x1, y1))
            save_crop(overlay, f"overlay_grid_r{row+1}c{col+1}.png", (x0, y0, x1, y1))

    boxes = {
        "top_band": (0, 0, w, int(h * 0.27)),
        "upper_middle_band": (0, int(h * 0.18), w, int(h * 0.49)),
        "middle_band": (0, int(h * 0.38), w, int(h * 0.72)),
        "bottom_band": (0, int(h * 0.64), w, h),
        "left_half": (0, 0, int(w * 0.54), h),
        "right_half": (int(w * 0.46), 0, w, h),
        "center": (int(w * 0.17), int(h * 0.15), int(w * 0.85), int(h * 0.82)),
        "left_core": (0, int(h * 0.18), int(w * 0.45), int(h * 0.82)),
        "middle_core": (int(w * 0.28), int(h * 0.18), int(w * 0.72), int(h * 0.82)),
        "right_core": (int(w * 0.55), int(h * 0.18), w, int(h * 0.82)),
        "title_block": (int(w * 0.58), int(h * 0.78), w, h),
        "notes_right": (int(w * 0.72), 0, w, int(h * 0.82)),
    }
    for name, box in boxes.items():
        save_crop(raw, f"raw_{name}.png", box)
        save_crop(overlay, f"overlay_{name}.png", box)

    raw_named_close_boxes = {
        "close_a_feeders_left": (620, 1320, 2360, 2450),
        "close_a_feeders_right": (2160, 1320, 3340, 2450),
        "close_b_feeders_left": (2900, 1320, 4300, 2450),
        "close_b_feeders_right": (4000, 1320, 5350, 2450),
        "close_top_sources_a": (500, 260, 2500, 1250),
        "close_top_sources_b": (2400, 260, 5000, 1250),
        "close_dc_a": (700, 2280, 2600, 3400),
        "close_dc_b": (2950, 2280, 5200, 3400),
        "close_terminal_blocks": (2050, 700, 3150, 1350),
    }
    for name, box in raw_named_close_boxes.items():
        save_crop(raw, f"{name}.png", box)
        save_crop(overlay, f"overlay_{name}.png", box)

    prefixed_close_boxes = {
        "close_lower_soe_a": (1900, 2750, 3500, 3550),
        "close_lower_soe_b": (3000, 2750, 5200, 3550),
        "close_master_lane": (2050, 760, 3450, 1500),
        "close_ann_dcs_center": (2500, 2680, 4100, 3550),
    }
    for name, box in prefixed_close_boxes.items():
        save_crop(raw, f"raw_{name}.png", box)
        save_crop(overlay, f"overlay_{name}.png", box)

    print(f"wrote crops to {OUT}")
    print(f"source size={w}x{h}")


if __name__ == "__main__":
    main()
