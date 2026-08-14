from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"

CROPS = {
    "top_4160_buses_and_sources": (650, 350, 9050, 1850),
    "left_train_a_feeders": (650, 1550, 5050, 5500),
    "right_train_b_feeders": (5000, 1550, 9100, 5500),
    "left_480_and_loads": (700, 2350, 3350, 5450),
    "right_480_and_loads": (5150, 2350, 8150, 5450),
    "cvcs_a_branch": (3950, 1650, 5200, 4600),
    "cvcs_b_branch": (8400, 1650, 9300, 4600),
    "left_dc_ac_rps": (3150, 3400, 4350, 6650),
    "right_dc_ac_rps": (7750, 3400, 8750, 6650),
    "bus_tie_detail": (4550, 1200, 5500, 1650),
}


def clean_stem(name: str) -> str:
    return name.replace(" -- ", "_").replace(" ", "_").replace(".png", "")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for image_name in [
        "raw -- schematic_image_variant_b_100.png",
        "detected_components_and_logical_overlay.png",
        "wire_nodes_overlay.png",
    ]:
        image = Image.open(BASE / image_name)
        stem = clean_stem(image_name)
        for crop_name, box in CROPS.items():
            image.crop(box).save(RESULTS / f"crop_{stem}_{crop_name}.png")


if __name__ == "__main__":
    main()
