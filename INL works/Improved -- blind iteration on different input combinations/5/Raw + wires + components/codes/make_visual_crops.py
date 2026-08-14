from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"

IMAGES = [
    "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png",
    "detected_components_and_logical_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]

REGIONS = {
    "full_top_sources_switchyard": (120, 20, 5280, 720),
    "top_left_grid_and_bus_a": (130, 30, 1800, 980),
    "top_center_switchyard_bus_tie": (2250, 20, 3500, 1050),
    "top_right_grid_and_bus_b": (4200, 30, 5320, 980),
    "train_a_division_i": (80, 740, 1350, 3050),
    "train_b_division_i": (1370, 740, 2600, 3050),
    "train_c_division_ii": (2560, 740, 3840, 3050),
    "train_d_division_ii": (3830, 740, 5080, 3050),
    "bus_ties_mid": (1120, 1050, 4200, 1550),
    "dc_vital_a_bottom": (500, 2750, 2350, 3700),
    "dc_vital_b_bottom": (3650, 2750, 5100, 3700),
    "bottom_ac_dc_strip": (450, 3350, 4650, 3830),
    "protection_control_bay_full": (5050, 720, 6250, 3600),
    "protection_relays_left": (5050, 980, 5750, 2350),
    "protection_relays_right": (5700, 980, 6250, 2350),
    "legend_title_blocks": (5200, 180, 6250, 4170),
}


def safe_stem(path):
    return Path(path).stem.replace(" ", "_").replace("-", "_")


def crop_all():
    out_root = RESULTS / "visual_crops"
    out_root.mkdir(parents=True, exist_ok=True)
    for image_name in IMAGES:
        image_path = BASE / image_name
        image = Image.open(image_path)
        image_out = out_root / safe_stem(image_name)
        image_out.mkdir(parents=True, exist_ok=True)
        width, height = image.size
        for region_name, box in REGIONS.items():
            left, top, right, bottom = box
            bounded = (
                max(0, left),
                max(0, top),
                min(width, right),
                min(height, bottom),
            )
            image.crop(bounded).save(image_out / f"{region_name}.png")


if __name__ == "__main__":
    crop_all()
    print(RESULTS / "visual_crops")
