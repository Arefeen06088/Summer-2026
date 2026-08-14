from __future__ import annotations

from pathlib import Path

from PIL import Image


RAW_DIR = Path(__file__).resolve().parents[1]
IMAGE_PATH = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_readable.png"
CROP_DIR = Path(__file__).resolve().parent / "crops"


def save_crop(image: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    crop = image.crop(box)
    if crop.mode == "RGBA":
        background = Image.new("RGB", crop.size, "white")
        background.paste(crop, mask=crop.split()[-1])
        crop = background
    crop.save(CROP_DIR / f"{name}.png")


def main() -> None:
    image = Image.open(IMAGE_PATH)
    width, height = image.size

    crops: dict[str, tuple[int, int, int, int]] = {
        "full_sheet": (0, 0, width, height),
        "drawing_area": (0, 0, int(width * 0.86), height),
        "title_notes_legend": (int(width * 0.72), int(height * 0.56), width, height),
        "top_overview": (0, 0, width, int(height * 0.25)),
        "middle_overview": (0, int(height * 0.22), width, int(height * 0.58)),
        "lower_overview": (0, int(height * 0.52), width, height),
        "left_full_height": (0, 0, int(width * 0.36), height),
        "center_full_height": (int(width * 0.30), 0, int(width * 0.70), height),
        "right_full_height": (int(width * 0.64), 0, width, height),
        "upper_sources": (0, 0, int(width * 0.86), int(height * 0.25)),
        "left_feeders": (0, int(height * 0.15), int(width * 0.39), int(height * 0.65)),
        "center_feeders": (int(width * 0.31), int(height * 0.15), int(width * 0.70), int(height * 0.65)),
        "right_feeders": (int(width * 0.62), int(height * 0.15), width, int(height * 0.65)),
        "lower_controls_left": (0, int(height * 0.52), int(width * 0.42), height),
        "lower_controls_center": (int(width * 0.30), int(height * 0.52), int(width * 0.72), height),
        "lower_controls_right": (int(width * 0.60), int(height * 0.52), width, height),
        "focus_top_left": (0, 0, int(width * 0.42), int(height * 0.30)),
        "focus_top_center": (int(width * 0.28), 0, int(width * 0.68), int(height * 0.30)),
        "focus_top_right": (int(width * 0.55), 0, int(width * 0.90), int(height * 0.30)),
        "focus_mid_left": (0, int(height * 0.25), int(width * 0.42), int(height * 0.57)),
        "focus_mid_center": (int(width * 0.28), int(height * 0.25), int(width * 0.70), int(height * 0.57)),
        "focus_mid_right": (int(width * 0.55), int(height * 0.25), int(width * 0.90), int(height * 0.57)),
        "focus_low_left": (0, int(height * 0.48), int(width * 0.42), height),
        "focus_low_center": (int(width * 0.28), int(height * 0.48), int(width * 0.70), height),
        "focus_low_right": (int(width * 0.55), int(height * 0.48), int(width * 0.90), height),
    }

    for row in range(4):
        for col in range(4):
            x0 = int(width * col / 4)
            x1 = int(width * (col + 1) / 4)
            y0 = int(height * row / 4)
            y1 = int(height * (row + 1) / 4)
            crops[f"grid_r{row + 1}_c{col + 1}"] = (x0, y0, x1, y1)

    for name, box in crops.items():
        save_crop(image, name, box)

    print(f"saved {len(crops)} crops to {CROP_DIR}")


if __name__ == "__main__":
    main()
