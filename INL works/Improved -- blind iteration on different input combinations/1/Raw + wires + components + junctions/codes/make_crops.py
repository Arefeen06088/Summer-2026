from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"

CROPS = {
    "top_4kv_buses": (450, 170, 3800, 780),
    "middle_480_loads": (450, 1000, 3820, 2000),
    "bottom_dc_ac_buses": (450, 1900, 2920, 2910),
    "left_class_1e_4kv_a": (500, 170, 1750, 610),
    "center_class_1e_4kv_b": (1750, 170, 3020, 610),
    "right_common_aac_4kv_c": (3020, 170, 3950, 610),
    "left_480_feeders_a": (500, 1050, 1700, 1980),
    "center_480_feeders_b": (1750, 1050, 2920, 1980),
    "right_480_feeders_c": (3020, 1050, 3820, 1980),
    "left_dc_ac_detail": (500, 1980, 1740, 2910),
    "right_dc_ac_detail": (1760, 1980, 2920, 2910),
}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for image_name in [
        "raw -- schematic_image_clean_100_connected.png",
        "detected_components_and_logical_overlay.png",
        "wire_nodes_overlay.png",
    ]:
        image = Image.open(BASE / image_name)
        stem = image_name.replace(" -- ", "_").replace(" ", "_").replace(".png", "")
        for crop_name, box in CROPS.items():
            crop = image.crop(box)
            crop.save(RESULTS / f"crop_{stem}_{crop_name}.png")


if __name__ == "__main__":
    main()
