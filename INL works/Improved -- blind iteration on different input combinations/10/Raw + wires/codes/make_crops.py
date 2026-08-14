from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"

RAW = BASE / "raw -- synthetic_nuclear_electrical_schematic_layout_labels_clear.png"
MASK = BASE / "wires_mask.png"
OVERLAY = BASE / "wires_mask_overlay.png"


def crop_grid(image_path: Path, prefix: str, rows: int = 3, cols: int = 4) -> None:
    image = Image.open(image_path)
    width, height = image.size
    out_dir = RESULTS / "crops"
    out_dir.mkdir(parents=True, exist_ok=True)
    for row in range(rows):
        for col in range(cols):
            left = round(col * width / cols)
            upper = round(row * height / rows)
            right = round((col + 1) * width / cols)
            lower = round((row + 1) * height / rows)
            tile = image.crop((left, upper, right, lower))
            tile.save(out_dir / f"{prefix}_r{row + 1}c{col + 1}.png")


def crop_regions(image_path: Path, prefix: str) -> None:
    image = Image.open(image_path)
    width, height = image.size
    out_dir = RESULTS / "crops"
    out_dir.mkdir(parents=True, exist_ok=True)
    regions = {
        "top": (0, 0, width, round(height * 0.36)),
        "middle": (0, round(height * 0.28), width, round(height * 0.72)),
        "bottom": (0, round(height * 0.64), width, height),
        "left": (0, 0, round(width * 0.36), height),
        "center": (round(width * 0.28), 0, round(width * 0.72), height),
        "right": (round(width * 0.64), 0, width, height),
        "title": (0, round(height * 0.82), width, height),
    }
    for name, box in regions.items():
        image.crop(box).save(out_dir / f"{prefix}_{name}.png")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for image_path, prefix in [(RAW, "raw"), (OVERLAY, "overlay"), (MASK, "mask")]:
        crop_grid(image_path, prefix)
        crop_regions(image_path, prefix)
    print(f"wrote crops under {RESULTS / 'crops'}")


if __name__ == "__main__":
    main()
