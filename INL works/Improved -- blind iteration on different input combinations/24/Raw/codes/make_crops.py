from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\24\Raw"
)
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_rev2.png"
CROP_DIR = RAW_DIR / "codes" / "crops"


def clamp_box(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    return max(0, x1), max(0, y1), min(width, x2), min(height, y2)


def main() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.open(RAW_IMAGE)
    width, height = image.size

    crops: dict[str, tuple[int, int, int, int]] = {
        "full_drawing_area": (0, 0, width, height),
        "top_overview": (0, 0, width, 2200),
        "middle_overview": (0, 1700, width, 4300),
        "lower_overview": (0, 3700, width, height),
        "left_full_height": (0, 0, 3400, height),
        "center_full_height": (2900, 0, 6300, height),
        "right_full_height": (5800, 0, width, height),
        "top_left": (0, 0, 3400, 2400),
        "top_center": (2900, 0, 6300, 2400),
        "top_right": (5800, 0, width, 2400),
        "mid_left": (0, 1600, 3400, 4300),
        "mid_center": (2900, 1600, 6300, 4300),
        "mid_right": (5800, 1600, width, 4300),
        "lower_left": (0, 3600, 3400, height),
        "lower_center": (2900, 3600, 6300, height),
        "lower_right": (5800, 3600, width, height),
        "upper_switchgear": (250, 650, 8950, 2150),
        "left_4160_480": (250, 1350, 3300, 4200),
        "center_4160_480": (3000, 1350, 6200, 4200),
        "right_4160_480": (5900, 1350, 8950, 4200),
        "dc_ups_full": (250, 4000, 8950, 6000),
        "dc_ups_left": (250, 4000, 3300, 6000),
        "dc_ups_center": (3000, 4000, 6200, 6000),
        "dc_ups_right": (5900, 4000, 8950, 6000),
    }

    x_edges = [0, width // 4, width // 2, (3 * width) // 4, width]
    y_edges = [0, height // 3, (2 * height) // 3, height]
    for yi in range(3):
        for xi in range(4):
            crops[f"grid_r{yi + 1}_c{xi + 1}"] = (
                x_edges[xi],
                y_edges[yi],
                x_edges[xi + 1],
                y_edges[yi + 1],
            )

    for name, box in crops.items():
        image.crop(clamp_box(box, width, height)).save(CROP_DIR / f"{name}.png")

    print(f"wrote {len(crops)} crops to {CROP_DIR}")


if __name__ == "__main__":
    main()
