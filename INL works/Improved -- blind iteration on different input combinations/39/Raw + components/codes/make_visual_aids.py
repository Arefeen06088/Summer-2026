from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


Image.MAX_IMAGE_PIXELS = None

ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\39\Raw + components"
)
RESULTS = ROOT / "results"
CODES = ROOT / "codes"

RAW = ROOT / "raw -- npp_schematic_improved_no_overlap.png"
OVERLAY = ROOT / "detected_components_and_logical_overlay.png"


def save_resized(im: Image.Image, path: Path, width: int) -> None:
    ratio = width / im.width
    out = im.resize((width, round(im.height * ratio)), Image.Resampling.LANCZOS)
    out.save(path, optimize=False)


def crop_and_save(
    im: Image.Image, box: tuple[int, int, int, int], path: Path, scale: float = 1.0
) -> None:
    crop = im.crop(box)
    if scale != 1.0:
        crop = crop.resize(
            (round(crop.width * scale), round(crop.height * scale)),
            Image.Resampling.LANCZOS,
        )
    crop.save(path, optimize=False)


def draw_grid(im: Image.Image, cols: int, rows: int) -> Image.Image:
    out = im.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    for c in range(1, cols):
        x = round(w * c / cols)
        draw.line((x, 0, x, h), fill=(240, 0, 0), width=8)
    for r in range(1, rows):
        y = round(h * r / rows)
        draw.line((0, y, w, y), fill=(240, 0, 0), width=8)
    return out


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)

    for prefix, path in (("raw", RAW), ("overlay", OVERLAY)):
        with Image.open(path) as im:
            im = im.convert("RGB")
            save_resized(im, RESULTS / f"{prefix}_full_preview.png", width=1800)
            save_resized(draw_grid(im, cols=4, rows=3), RESULTS / f"{prefix}_grid_index.png", width=1800)

            w, h = im.size
            bands = {
                "top": (0, 0, w, round(h * 0.30)),
                "upper_middle": (0, round(h * 0.20), w, round(h * 0.55)),
                "lower_middle": (0, round(h * 0.45), w, round(h * 0.78)),
                "bottom": (0, round(h * 0.66), w, h),
                "left_core": (0, round(h * 0.08), round(w * 0.43), round(h * 0.88)),
                "center_core": (round(w * 0.27), round(h * 0.08), round(w * 0.73), round(h * 0.88)),
                "right_core": (round(w * 0.57), round(h * 0.08), w, round(h * 0.88)),
                "title_notes_area": (round(w * 0.64), round(h * 0.58), w, h),
            }
            for name, box in bands.items():
                crop_and_save(im, box, RESULTS / f"{prefix}_{name}.png", scale=1.5)

            cols, rows = 4, 3
            for r in range(rows):
                for c in range(cols):
                    left = round(w * c / cols)
                    right = round(w * (c + 1) / cols)
                    top = round(h * r / rows)
                    bottom = round(h * (r + 1) / rows)
                    crop_and_save(
                        im,
                        (left, top, right, bottom),
                        RESULTS / f"{prefix}_grid_r{r + 1}c{c + 1}_2x.png",
                        scale=2.0,
                    )


if __name__ == "__main__":
    main()
