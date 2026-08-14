from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

RAW_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\23\Raw"
)
RAW_IMAGE = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png"
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
        "top_overview": (0, 0, width, 2600),
        "middle_overview": (0, 2200, width, 6200),
        "lower_overview": (0, 5600, width, height),
        "left_full_height": (0, 0, 5200, height),
        "center_full_height": (4600, 0, 9800, height),
        "right_full_height": (9200, 0, width, height),
        "top_left": (0, 0, 5200, 3000),
        "top_center": (4600, 0, 9800, 3000),
        "top_right": (9200, 0, width, 3000),
        "mid_left": (0, 2200, 5200, 6500),
        "mid_center": (4600, 2200, 9800, 6500),
        "mid_right": (9200, 2200, width, 6500),
        "lower_left": (0, 5600, 5200, height),
        "lower_center": (4600, 5600, 9800, height),
        "lower_right": (9200, 5600, width, height),
        "top_switchgear_ats": (450, 650, 10400, 2750),
        "load_center_1a": (450, 2450, 4300, 5450),
        "load_center_1c": (4000, 2450, 7750, 5450),
        "load_center_1b": (7450, 2450, 11100, 5450),
        "load_center_2a": (450, 5000, 4300, 8150),
        "load_center_2c": (4000, 5000, 7750, 8150),
        "load_center_2b": (7450, 5000, 11100, 8150),
        "bottom_dc_rps_full": (450, 6600, 10450, 9250),
        "bottom_dc_left": (450, 6600, 5200, 9250),
        "bottom_dc_right": (4700, 6600, 10450, 9250),
    }

    # A 4 x 3 grid makes the large shifted schematic manageable without assuming layout.
    x_edges = [0, 3600, 7200, 10800, width]
    y_edges = [0, 3133, 6266, height]
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
