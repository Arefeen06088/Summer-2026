from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

DOC = "27"
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\27\Raw + components"
)
CODES = ROOT / "codes"
RESULTS = ROOT / "results"

RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_readable.png"
OVERLAY = ROOT / "detected_components_and_logical_overlay.png"


def clamp_box(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    return max(0, x1), max(0, y1), min(width, x2), min(height, y2)


def fit_down(im: Image.Image, max_w: int = 3200, max_h: int = 2600) -> Image.Image:
    scale = min(max_w / im.width, max_h / im.height, 1.0)
    if scale >= 1.0:
        return im.copy()
    size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    return im.resize(size, Image.Resampling.LANCZOS)


def save_crop(
    im: Image.Image,
    stem: str,
    name: str,
    box: tuple[int, int, int, int],
    two_x: bool = False,
    max_w: int = 3200,
    max_h: int = 2600,
) -> None:
    crop = im.crop(clamp_box(box, im.width, im.height))
    fit_down(crop, max_w, max_h).save(RESULTS / f"{stem}_{name}.png")
    if two_x:
        two = crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS)
        fit_down(two, 3800, 3400).save(RESULTS / f"{stem}_{name}_2x.png")


def save_preview(im: Image.Image, stem: str) -> None:
    fit_down(im, 3200, 2300).save(RESULTS / f"{stem}_full_preview.png")
    fit_down(im, 5600, 4000).save(RESULTS / f"{stem}_full_preview_large.png")


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    sources = [("raw", raw), ("overlay", overlay)]
    width, height = raw.size

    named_crops = {
        "01_top_overview": (0, 0, width, 2050),
        "02_upper_middle_overview": (0, 1600, width, 3950),
        "03_lower_middle_overview": (0, 3550, width, 5900),
        "04_bottom_overview": (0, 5450, width, height),
        "05_left_core": (0, 650, 4350, 6750),
        "06_center_core": (3400, 650, 7500, 6750),
        "07_right_core": (6750, 650, width, 6750),
        "08_notes_title_area": (7200, 4100, width, height),
        "09_full_drawing_area": (0, 0, width, height),
    }

    for stem, im in sources:
        save_preview(im, stem)
        for name, box in named_crops.items():
            max_w, max_h = (5600, 4000) if name == "09_full_drawing_area" else (3400, 2800)
            save_crop(im, stem, name, box, max_w=max_w, max_h=max_h)

    rows, cols = 4, 5
    pad_x, pad_y = 220, 190
    cell_w = width // cols
    cell_h = height // rows
    for stem, im in sources:
        for r in range(rows):
            for c in range(cols):
                x1 = c * cell_w - pad_x
                y1 = r * cell_h - pad_y
                x2 = (c + 1) * cell_w + pad_x
                y2 = (r + 1) * cell_h + pad_y
                save_crop(im, stem, f"grid_r{r + 1}c{c + 1}", (x1, y1, x2, y2), two_x=True)

    print(f"wrote Doc{DOC} Raw + components visual aids to {RESULTS}")


if __name__ == "__main__":
    main()
