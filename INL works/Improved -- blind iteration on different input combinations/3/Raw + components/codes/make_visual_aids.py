from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "codes" / "visual_aids"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_100_component_electrical_schematic.png",
    "overlay": BASE / "detected_components_and_logical_overlay.png",
}

CROPS = {
    "top_left_sources": (240, 210, 2100, 1260),
    "top_center_dc_ups": (2150, 520, 3380, 1850),
    "top_right_sources": (2780, 210, 5100, 1260),
    "middle_mcc_a": (250, 1190, 2300, 2050),
    "middle_mcc_b": (3000, 1190, 5010, 2050),
    "feeders_a": (260, 1900, 2700, 2860),
    "feeders_b": (2660, 1900, 5050, 2860),
    "lower_rps_a": (1180, 2760, 2600, 3800),
    "lower_rps_b": (3020, 2760, 4300, 3800),
    "full_left": (200, 210, 2850, 3820),
    "full_right": (2600, 210, 5200, 3820),
}


def main() -> None:
    for src_name, path in SOURCES.items():
        image = Image.open(path).convert("RGB")
        for crop_name, box in CROPS.items():
            image.crop(box).save(OUT / f"{src_name}_{crop_name}.png")


if __name__ == "__main__":
    main()
