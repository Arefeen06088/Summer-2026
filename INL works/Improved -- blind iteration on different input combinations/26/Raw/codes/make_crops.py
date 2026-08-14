from __future__ import annotations

from pathlib import Path

from PIL import Image


RAW_DIR = Path(__file__).resolve().parents[1]
IMAGE_PATH = RAW_DIR / "raw -- synthetic_npp_electrical_schematic_v3(1).png"
CROP_DIR = Path(__file__).resolve().parent / "crops"


def save_crop(image: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    crop = image.crop(box)
    crop.save(CROP_DIR / f"{name}.png")


def main() -> None:
    image = Image.open(IMAGE_PATH)
    width, height = image.size

    crops: dict[str, tuple[int, int, int, int]] = {
        "full_sheet": (0, 0, width, height),
        "drawing_area": (0, 0, width, int(height * 0.86)),
        "title_notes_legend": (int(width * 0.66), int(height * 0.70), width, height),
        "top_overview": (0, 0, width, int(height * 0.28)),
        "upper_middle_overview": (0, int(height * 0.20), width, int(height * 0.52)),
        "lower_middle_overview": (0, int(height * 0.46), width, int(height * 0.74)),
        "bottom_overview": (0, int(height * 0.68), width, height),
        "left_full_height": (0, 0, int(width * 0.34), height),
        "center_full_height": (int(width * 0.30), 0, int(width * 0.70), height),
        "right_full_height": (int(width * 0.66), 0, width, height),
        "upper_sources": (0, 0, width, int(height * 0.22)),
        "left_feeders": (0, int(height * 0.16), int(width * 0.38), int(height * 0.78)),
        "center_feeders": (int(width * 0.31), int(height * 0.16), int(width * 0.69), int(height * 0.78)),
        "right_feeders": (int(width * 0.62), int(height * 0.16), width, int(height * 0.78)),
        "lower_controls_left": (0, int(height * 0.58), int(width * 0.40), height),
        "lower_controls_center": (int(width * 0.30), int(height * 0.58), int(width * 0.72), height),
        "lower_controls_right": (int(width * 0.60), int(height * 0.58), width, height),
        "focus_a_mcc_loads": (700, 1400, 2950, 3100),
        "focus_b_mcc_loads": (3300, 1400, 5600, 3100),
        "focus_a_dc_rps": (700, 2550, 3800, height),
        "focus_b_dc_rps": (3000, 2550, 6300, height),
        "focus_ab_ties": (2300, 650, 3900, 3000),
        "focus_top_sources_a": (850, 250, 3300, 1050),
        "focus_top_sources_b": (3000, 250, 5900, 1050),
        "grid_r1_c1": (0, 0, int(width * 0.25), int(height * 0.34)),
        "grid_r1_c2": (int(width * 0.25), 0, int(width * 0.50), int(height * 0.34)),
        "grid_r1_c3": (int(width * 0.50), 0, int(width * 0.75), int(height * 0.34)),
        "grid_r1_c4": (int(width * 0.75), 0, width, int(height * 0.34)),
        "grid_r2_c1": (0, int(height * 0.30), int(width * 0.25), int(height * 0.66)),
        "grid_r2_c2": (int(width * 0.25), int(height * 0.30), int(width * 0.50), int(height * 0.66)),
        "grid_r2_c3": (int(width * 0.50), int(height * 0.30), int(width * 0.75), int(height * 0.66)),
        "grid_r2_c4": (int(width * 0.75), int(height * 0.30), width, int(height * 0.66)),
        "grid_r3_c1": (0, int(height * 0.62), int(width * 0.25), height),
        "grid_r3_c2": (int(width * 0.25), int(height * 0.62), int(width * 0.50), height),
        "grid_r3_c3": (int(width * 0.50), int(height * 0.62), int(width * 0.75), height),
        "grid_r3_c4": (int(width * 0.75), int(height * 0.62), width, height),
    }

    for name, box in crops.items():
        save_crop(image, name, box)

    print(f"saved {len(crops)} crops to {CROP_DIR}")


if __name__ == "__main__":
    main()
