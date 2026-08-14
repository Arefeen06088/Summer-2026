from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

DOC = "26"
ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + components"
)
CODES = ROOT / "codes"
RESULTS = ROOT / "results"

RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_v3(1).png"
OVERLAY = ROOT / "detected_components_and_logical_overlay.png"


def clamp_box(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    return max(0, x1), max(0, y1), min(width, x2), min(height, y2)


def fit_down(im: Image.Image, max_w: int = 3000, max_h: int = 2400) -> Image.Image:
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
    max_w: int = 3000,
    max_h: int = 2400,
) -> None:
    crop = im.crop(clamp_box(box, im.width, im.height))
    fit_down(crop, max_w, max_h).save(RESULTS / f"{stem}_{name}.png")
    if two_x:
        two = crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS)
        fit_down(two, 3600, 3200).save(RESULTS / f"{stem}_{name}_2x.png")


def save_preview(im: Image.Image, stem: str) -> None:
    fit_down(im, 3000, 2200).save(RESULTS / f"{stem}_full_preview.png")
    fit_down(im, 5200, 3600).save(RESULTS / f"{stem}_full_preview_large.png")


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    raw = Image.open(RAW).convert("RGB")
    overlay = Image.open(OVERLAY).convert("RGB")
    sources = [("raw", raw), ("overlay", overlay)]
    width, height = raw.size

    named_crops = {
        "01_top_overview": (0, 0, width, 1350),
        "02_upper_middle_overview": (0, 950, width, 2520),
        "03_lower_middle_overview": (0, 2200, width, 3500),
        "04_bottom_overview": (0, 3150, width, height),
        "05_left_core": (0, 450, 2850, 3900),
        "06_center_core": (2300, 450, 5000, 3900),
        "07_right_core": (4450, 450, width, 3900),
        "08_notes_title_area": (4550, 2850, width, height),
        "09_full_drawing_area": (0, 0, width, height),
    }

    for stem, im in sources:
        save_preview(im, stem)
        for name, box in named_crops.items():
            max_w, max_h = (5200, 3600) if name == "09_full_drawing_area" else (3400, 2600)
            save_crop(im, stem, name, box, max_w=max_w, max_h=max_h)

    rows, cols = 4, 4
    pad_x, pad_y = 170, 140
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
