from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"
CROP_DIR = RESULTS_DIR / "visual_crops"

RAW = BASE_DIR / "raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png"
OVERLAY = BASE_DIR / "detected_components_overlay.png"
WIRE_OVERLAY = BASE_DIR / "wires_mask_overlay.png"
WIRE_MASK = BASE_DIR / "wires_mask.png"


def clamp_box(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = box
    return max(0, left), max(0, top), min(width, right), min(height, bottom)


def save_crop(source: Path, out_name: str, box: tuple[int, int, int, int]) -> None:
    image = Image.open(source)
    crop = image.crop(clamp_box(box, image.width, image.height))
    crop.save(CROP_DIR / out_name)


def main() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)

    crops = {
        "top_all_sources_buses": (390, 200, 4660, 940),
        "top_left_13kv_4160a": (400, 215, 2460, 900),
        "top_right_13kv_4160b": (2140, 215, 4670, 900),
        "tie_between_4160_buses": (2150, 540, 3110, 880),
        "interface_416_to_480_all": (330, 760, 4710, 1240),
        "interface_416_to_480_left": (330, 760, 2460, 1240),
        "interface_416_to_480_right": (2350, 760, 4710, 1240),
        "load_centers_all": (330, 1080, 4710, 2250),
        "load_center_a": (330, 1080, 1500, 2220),
        "load_center_b": (1410, 1080, 2600, 2220),
        "load_center_c": (2500, 1080, 3670, 2220),
        "load_center_d": (3540, 1080, 4710, 2220),
        "tie_between_480_b_c": (2240, 1050, 3050, 1280),
        "lower_control_all": (330, 2220, 4730, 3380),
        "interface_480_to_125_all": (330, 1900, 4730, 2550),
        "interface_480_to_125_a": (330, 1900, 2050, 2550),
        "interface_480_to_125_b": (2500, 1900, 4730, 2550),
        "zoom_rectifier_a_feed": (720, 1500, 1370, 2380),
        "zoom_rectifier_b_feed": (3150, 1500, 3780, 2380),
        "lower_left_train_a": (330, 2220, 1600, 3300),
        "lower_mid_train_a": (1380, 2220, 2460, 3300),
        "lower_mid_train_b": (2460, 2220, 3600, 3300),
        "lower_right_train_b": (3540, 2220, 4730, 3300),
        "notes_legend": (4920, 295, 5980, 1230),
        "title_block": (4930, 3500, 5980, 4200),
    }

    for name, box in crops.items():
        save_crop(RAW, f"{name}_raw.png", box)
        save_crop(OVERLAY, f"{name}_components.png", box)
        save_crop(WIRE_OVERLAY, f"{name}_wires_overlay.png", box)

    broad = {
        "raw_full": RAW,
        "components_full": OVERLAY,
        "wires_overlay_full": WIRE_OVERLAY,
        "wires_mask_full": WIRE_MASK,
    }
    for name, source in broad.items():
        image = Image.open(source)
        image.thumbnail((2400, 1700))
        image.save(CROP_DIR / f"{name}_thumb.png")

    print(f"wrote crops to {CROP_DIR}")


if __name__ == "__main__":
    main()
