from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "codes" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw.png",
    "wire_nodes_overlay": ROOT / "wire_nodes_overlay.png",
    "wires_mask_overlay": ROOT / "wires_mask_overlay.png",
}

CROPS = {
    "top_left_sources": (300, 260, 2400, 900),
    "upper_bus_left": (820, 650, 3300, 1250),
    "upper_bus_mid": (3100, 650, 5600, 1250),
    "upper_bus_right": (5400, 650, 7350, 1250),
    "upper_left_bus_source_detail": (720, 620, 1750, 1350),
    "upper_source_b_detail": (420, 1080, 2100, 1550),
    "upper_right_tie_detail": (6650, 650, 7350, 1250),
    "upper_loads_left": (360, 1000, 2500, 2150),
    "upper_loads_mid": (2250, 1000, 4700, 2200),
    "upper_loads_right": (4400, 1000, 7350, 2250),
    "dc_ups": (4200, 2050, 7050, 3550),
    "dc_ups_right_controls": (6200, 2000, 7900, 3650),
    "left_utility_feed": (620, 2180, 1100, 3550),
    "right_utility_feed": (6900, 2450, 7300, 3600),
    "lower_bus_tie": (3600, 3500, 4650, 3920),
    "lower_loads_left": (950, 3600, 3550, 5050),
    "lower_loads_right": (4100, 3600, 6350, 5050),
    "notes_legend": (7420, 300, 8580, 2150),
    "title_block": (7420, 4550, 8600, 5230),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as image:
            for crop_name, box in CROPS.items():
                image.crop(box).save(OUT / f"{source_name}_{crop_name}.png")


if __name__ == "__main__":
    main()
