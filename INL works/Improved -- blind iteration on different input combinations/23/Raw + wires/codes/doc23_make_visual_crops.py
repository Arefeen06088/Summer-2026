from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


Image.MAX_IMAGE_PIXELS = None

DOC = "23"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw + wires")
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
    new_size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    return im.resize(new_size, Image.Resampling.LANCZOS)


def clamp_box(box: tuple[int, int, int, int], w: int, h: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    return max(0, x1), max(0, y1), min(w, x2), min(h, y2)


def save_crop(
    im: Image.Image,
    stem: str,
    name: str,
    box: tuple[int, int, int, int],
    max_w: int = 2600,
    max_h: int = 2200,
) -> None:
    w, h = im.size
    crop = im.crop(clamp_box(box, w, h))
    crop = fit_down(crop, max_w, max_h)
    crop.save(CROPS / f"{stem}__{name}.png")


def save_full_views(im: Image.Image, stem: str) -> None:
    fit_down(im, 3000, 2200).save(CROPS / f"{stem}__overview.png")
    fit_down(im, 5000, 3600).save(CROPS / f"{stem}__overview_large.png")


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    CROPS.mkdir(parents=True, exist_ok=True)

    sources: list[tuple[str, Image.Image]] = [
        ("raw", Image.open(RAW).convert("RGB")),
        ("wires_overlay", Image.open(OVERLAY).convert("RGB")),
        ("wires_mask_inv", ImageOps.invert(Image.open(MASK).convert("L")).convert("RGB")),
    ]
    w, h = sources[0][1].size

    for stem, im in sources:
        save_full_views(im, stem)

    # Broad proportional crops, intentionally overlapping for shifted components.
    base_crops = {
        "top_band": (0, 0, w, int(h * 0.30)),
        "upper_middle_band": (0, int(h * 0.20), w, int(h * 0.48)),
        "middle_band": (0, int(h * 0.38), w, int(h * 0.72)),
        "bottom_band": (0, int(h * 0.62), w, h),
        "left_half": (0, 0, int(w * 0.54), h),
        "right_half": (int(w * 0.46), 0, w, h),
        "left_core": (0, int(h * 0.14), int(w * 0.38), int(h * 0.78)),
        "middle_core": (int(w * 0.28), int(h * 0.12), int(w * 0.72), int(h * 0.78)),
        "right_core": (int(w * 0.62), int(h * 0.12), w, int(h * 0.78)),
        "lower_left": (0, int(h * 0.52), int(w * 0.38), h),
        "lower_mid": (int(w * 0.30), int(h * 0.52), int(w * 0.70), h),
        "lower_right": (int(w * 0.62), int(h * 0.52), w, h),
        "title_notes": (int(w * 0.66), int(h * 0.66), w, h),
    }

    for stem, im in sources:
        for name, box in base_crops.items():
            save_crop(im, stem, name, box)

    cols, rows = 5, 4
    pad_x, pad_y = int(w * 0.015), int(h * 0.018)
    cell_w, cell_h = w // cols, h // rows
    for stem, im in sources:
        for r in range(rows):
            for c in range(cols):
                bx1 = c * cell_w - pad_x
                by1 = r * cell_h - pad_y
                bx2 = (c + 1) * cell_w + pad_x
                by2 = (r + 1) * cell_h + pad_y
                save_crop(im, stem, f"grid_r{r + 1}c{c + 1}", (bx1, by1, bx2, by2), 3000, 2400)

    # Extra high-detail crops for common dense regions.
    extra = {
        "top_source_bus": (int(w * 0.02), 0, int(w * 0.62), int(h * 0.28)),
        "upper_left_trains": (0, int(h * 0.14), int(w * 0.48), int(h * 0.54)),
        "upper_right_trains": (int(w * 0.45), int(h * 0.14), w, int(h * 0.54)),
        "trainA_mcc_feeders": (0, int(h * 0.36), int(w * 0.32), int(h * 0.76)),
        "trainB_mcc_feeders": (int(w * 0.22), int(h * 0.36), int(w * 0.56), int(h * 0.76)),
        "trainC_mcc_feeders": (int(w * 0.44), int(h * 0.36), int(w * 0.78), int(h * 0.76)),
        "trainD_mcc_feeders": (int(w * 0.66), int(h * 0.36), w, int(h * 0.76)),
        "dc_ups_left": (0, int(h * 0.62), int(w * 0.46), h),
        "dc_ups_right": (int(w * 0.42), int(h * 0.62), w, h),
    }
    for stem, im in sources:
        for name, box in extra.items():
            save_crop(im, stem, name, box, 3600, 2600)

    print(f"raw={RAW.name} size={w}x{h}")
    print(f"wrote crops to {CROPS}")


if __name__ == "__main__":
    main()
