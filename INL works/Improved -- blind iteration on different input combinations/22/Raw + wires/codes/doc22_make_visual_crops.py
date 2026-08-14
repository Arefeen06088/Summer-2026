from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


DOC = "22"
BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires")
CODES = BASE / "codes"
RESULTS = BASE / "results"
CROPS = CODES / "crops"

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_clean.png"
OVERLAY = BASE / "wires_mask_overlay.png"
MASK = BASE / "wires_mask.png"


def clamp_box(box: tuple[int, int, int, int], w: int, h: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    return max(0, x1), max(0, y1), min(w, x2), min(h, y2)


def save_crop(im: Image.Image, stem: str, name: str, box: tuple[int, int, int, int]) -> None:
    w, h = im.size
    crop = im.crop(clamp_box(box, w, h))
    out = CROPS / f"{stem}__{name}.png"
    crop.save(out)
    if crop.width * crop.height <= 2_800_000:
        crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS).save(
            CROPS / f"{stem}__{name}_2x.png"
        )


def main() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    CROPS.mkdir(parents=True, exist_ok=True)

    sources: list[tuple[str, Image.Image]] = [
        ("raw", Image.open(RAW).convert("RGB")),
        ("wires_overlay", Image.open(OVERLAY).convert("RGB")),
        ("wires_mask_inv", ImageOps.invert(Image.open(MASK).convert("L")).convert("RGB")),
    ]

    base_crops = {
        "overview": (0, 0, 7200, 5100),
        "working_area": (180, 160, 7060, 4920),
        "top_band": (180, 160, 7060, 1500),
        "upper_middle_band": (180, 1200, 7060, 2600),
        "middle_band": (180, 2250, 7060, 3650),
        "bottom_band": (180, 3450, 7060, 4920),
        "left_half": (180, 160, 3800, 4920),
        "right_half": (3450, 160, 7060, 4920),
        "center": (1900, 900, 5400, 4100),
        "left_core": (180, 850, 2700, 3880),
        "middle_core": (2450, 850, 5000, 3880),
        "right_core": (4750, 850, 7060, 3880),
        "title_notes": (4800, 3600, 7060, 4920),
    }

    for stem, im in sources:
        for name, box in base_crops.items():
            save_crop(im, stem, name, box)

    x1, y1, x2, y2 = base_crops["working_area"]
    cols = rows = 4
    pad = 100
    cell_w = (x2 - x1) // cols
    cell_h = (y2 - y1) // rows
    for stem, im in sources:
        for r in range(rows):
            for c in range(cols):
                bx1 = x1 + c * cell_w - pad
                by1 = y1 + r * cell_h - pad
                bx2 = x1 + (c + 1) * cell_w + pad
                by2 = y1 + (r + 1) * cell_h + pad
                save_crop(im, stem, f"grid_r{r + 1}c{c + 1}", (bx1, by1, bx2, by2))

    print(f"wrote crops to {CROPS}")


if __name__ == "__main__":
    main()
