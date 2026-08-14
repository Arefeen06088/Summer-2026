from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


Image.MAX_IMAGE_PIXELS = None

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + wires")
CODES = BASE / "codes"
CROPS = CODES / "crops"
RESULTS = BASE / "results"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


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
    if crop.width * crop.height <= 2_500_000:
        crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS).save(
            CROPS / f"{source_name}__{crop_name}_2x.png"
        )


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    mask_inv = ImageOps.invert(Image.open(MASK).convert("L")).convert("RGB")
    w, h = raw.size

    boxes: dict[str, tuple[int, int, int, int]] = {
        "overview": (0, 0, w, h),
        "working_area": (80, 80, w - 120, h - 120),
        "top_band": (0, 0, w, int(h * 0.34)),
        "middle_band": (0, int(h * 0.28), w, int(h * 0.72)),
        "bottom_band": (0, int(h * 0.62), w, h),
        "left_half": (0, 0, int(w * 0.54), h),
        "right_half": (int(w * 0.46), 0, w, h),
        "center": (int(w * 0.18), int(h * 0.12), int(w * 0.84), int(h * 0.86)),
        "left_core": (0, int(h * 0.14), int(w * 0.46), int(h * 0.86)),
        "middle_core": (int(w * 0.25), int(h * 0.14), int(w * 0.75), int(h * 0.86)),
        "right_core": (int(w * 0.54), int(h * 0.14), w, int(h * 0.86)),
        "title_notes": (int(w * 0.62), int(h * 0.74), w, h),
    }

    cols = 4
    rows = 4
    pad_x = 150
    pad_y = 140
    for row in range(rows):
        for col in range(cols):
            boxes[f"grid_r{row + 1}c{col + 1}"] = (
                int(col * w / cols) - pad_x,
                int(row * h / rows) - pad_y,
                int((col + 1) * w / cols) + pad_x,
                int((row + 1) * h / rows) + pad_y,
            )

    sources = {
        "raw": raw,
        "wires_overlay": overlay,
        "wires_mask_inv": mask_inv,
    }
    for source_name, image in sources.items():
        for crop_name, box in boxes.items():
            save_crop(image, source_name, crop_name, box)

    print(f"crops: {CROPS}")
    print(f"source size: {w}x{h}")


if __name__ == "__main__":
    main()
