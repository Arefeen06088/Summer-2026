from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "codes" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_100_component_electrical_schematic.png",
    "wire_nodes_overlay": ROOT / "wire_nodes_overlay.png",
    "wires_mask_overlay": ROOT / "wires_mask_overlay.png",
}

CROPS = {
    "top_left_train_a": (180, 180, 2480, 1280),
    "top_center_dc_ups": (2150, 460, 3820, 1770),
    "top_right_train_b": (3220, 180, 5260, 1280),
    "mid_mcc_train_a": (360, 880, 2300, 2100),
    "mid_mcc_train_b": (3420, 880, 5280, 2100),
    "feeders_left_train_a": (240, 1820, 2780, 2740),
    "feeders_right_train_b": (2520, 1820, 5200, 2740),
    "lower_controls": (1120, 2580, 4180, 3650),
    "notes_legend": (4920, 180, 5880, 2040),
    "source_breaker_a": (650, 420, 1180, 680),
    "source_breaker_b": (3880, 420, 4420, 680),
    "ground_reference": (2250, 520, 3150, 980),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as image:
            for crop_name, box in CROPS.items():
                crop = image.crop(box)
                crop.save(OUT / f"{source_name}_{crop_name}.png")


if __name__ == "__main__":
    main()
