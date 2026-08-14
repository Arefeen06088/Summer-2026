from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


Image.MAX_IMAGE_PIXELS = None

DOC = "24"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\24\Raw + wires")
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = CODES / "crops"

RAW = next(BASE.glob("raw -- *.png"))
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


def fit_down(im: Image.Image, max_w: int, max_h: int) -> Image.Image:
    scale = min(max_w / im.width, max_h / im.height, 1.0)
    if scale >= 1:
        return im.copy()
    size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    return im.resize(size, Image.Resampling.LANCZOS)


def clamp_box(box: tuple[int, int, int, int], w: int, h: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    return max(0, x1), max(0, y1), min(w, x2), min(h, y2)


def save_crop(
    im: Image.Image,
    stem: str,
    name: str,
    box: tuple[int, int, int, int],
    max_w: int = 2800,
    max_h: int = 2200,
) -> None:
    w, h = im.size
    crop = im.crop(clamp_box(box, w, h))
    fit_down(crop, max_w, max_h).save(CROPS / f"{stem}__{name}.png")


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    CROPS.mkdir(parents=True, exist_ok=True)

    sources = [
        ("raw", Image.open(RAW).convert("RGB")),
        ("wires_overlay", Image.open(OVERLAY).convert("RGB")),
        ("wires_mask_inv", ImageOps.invert(Image.open(MASK).convert("L")).convert("RGB")),
    ]
    w, h = sources[0][1].size

    base_crops = {
        "overview": (0, 0, w, h),
        "overview_large": (0, 0, w, h),
        "top_band": (0, 0, w, int(h * 0.30)),
        "upper_middle_band": (0, int(h * 0.20), w, int(h * 0.50)),
        "middle_band": (0, int(h * 0.38), w, int(h * 0.72)),
        "bottom_band": (0, int(h * 0.62), w, h),
        "left_half": (0, 0, int(w * 0.54), h),
        "right_half": (int(w * 0.46), 0, w, h),
        "left_core": (0, int(h * 0.12), int(w * 0.40), int(h * 0.82)),
        "middle_core": (int(w * 0.30), int(h * 0.10), int(w * 0.72), int(h * 0.82)),
        "right_core": (int(w * 0.60), int(h * 0.10), w, int(h * 0.82)),
        "lower_left": (0, int(h * 0.50), int(w * 0.42), h),
        "lower_mid": (int(w * 0.30), int(h * 0.50), int(w * 0.72), h),
        "lower_right": (int(w * 0.60), int(h * 0.50), w, h),
        "title_notes": (int(w * 0.64), int(h * 0.58), w, h),
    }

    for stem, im in sources:
        for name, box in base_crops.items():
            max_w, max_h = (4200, 3000) if name == "overview_large" else (2800, 2200)
            save_crop(im, stem, name, box, max_w, max_h)

    cols, rows = 5, 4
    pad_x, pad_y = int(w * 0.018), int(h * 0.022)
    cell_w, cell_h = w // cols, h // rows
    for stem, im in sources:
        for r in range(rows):
            for c in range(cols):
                box = (
                    c * cell_w - pad_x,
                    r * cell_h - pad_y,
                    (c + 1) * cell_w + pad_x,
                    (r + 1) * cell_h + pad_y,
                )
                save_crop(im, stem, f"grid_r{r + 1}c{c + 1}", box, 3000, 2400)

    extras = {
        "top_source_bus": (0, 0, int(w * 0.66), int(h * 0.34)),
        "upper_left_trains": (0, int(h * 0.14), int(w * 0.52), int(h * 0.58)),
        "upper_right_trains": (int(w * 0.44), int(h * 0.14), w, int(h * 0.58)),
        "mid_left_loads": (0, int(h * 0.30), int(w * 0.44), int(h * 0.72)),
        "mid_right_loads": (int(w * 0.42), int(h * 0.30), w, int(h * 0.72)),
        "bottom_left_controls": (0, int(h * 0.58), int(w * 0.48), h),
        "bottom_right_controls": (int(w * 0.42), int(h * 0.58), w, h),
    }
    for stem, im in sources:
        for name, box in extras.items():
            save_crop(im, stem, name, box, 3600, 2600)

    print(f"raw={RAW.name} size={w}x{h}")
    print(f"wrote crops to {CROPS}")


if __name__ == "__main__":
    main()
