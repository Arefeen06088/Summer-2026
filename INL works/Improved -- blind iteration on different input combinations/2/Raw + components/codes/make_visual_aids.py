from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "codes" / "visual_aids"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": BASE / "raw -- schematic_image_variant_b_100.png",
    "overlay": BASE / "detected_components_and_logical_overlay.png",
}

CROPS = {
    "full_left_train_a": (700, 350, 5200, 6600),
    "full_right_train_b": (5000, 350, 9100, 6600),
    "top_sources_and_tie": (1400, 350, 9000, 1850),
    "left_480_loads": (750, 1600, 3650, 5350),
    "left_rps_dc": (3150, 1600, 4300, 6550),
    "left_cvcs": (4050, 1600, 5200, 5350),
    "right_480_loads": (5100, 1600, 7900, 5350),
    "right_rps_dc": (7550, 1600, 8650, 6550),
    "right_cvcs": (8350, 1600, 9250, 5350),
    "title_notes": (9000, 900, 10700, 6800),
}


def main() -> None:
    for src_name, path in SOURCES.items():
        image = Image.open(path)
        for crop_name, box in CROPS.items():
            image.crop(box).save(OUT / f"{src_name}_{crop_name}.png")


if __name__ == "__main__":
    main()
