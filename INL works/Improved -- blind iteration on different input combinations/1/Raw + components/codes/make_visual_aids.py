from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "codes" / "visual_aids"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": BASE / "raw -- schematic_image_clean_100_connected.png",
    "overlay": BASE / "detected_components_and_logical_overlay.png",
}

CROPS = {
    "train_a": (420, 160, 1620, 1940),
    "train_b": (1600, 160, 2820, 1940),
    "train_c": (2800, 160, 3750, 1940),
    "top_ties": (1380, 260, 3160, 620),
    "dc_ups_rps": (420, 1880, 2920, 2920),
    "left_mid_loads": (420, 940, 1620, 1940),
    "center_mid_loads": (1600, 940, 2820, 1940),
    "right_mid_loads": (2800, 940, 3750, 1940),
}


def main() -> None:
    for src_name, path in SOURCES.items():
        image = Image.open(path)
        for crop_name, box in CROPS.items():
            crop = image.crop(box)
            crop.save(OUT / f"{src_name}_{crop_name}.png")


if __name__ == "__main__":
    main()
