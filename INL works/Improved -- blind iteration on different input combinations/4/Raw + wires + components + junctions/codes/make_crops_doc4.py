from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\4\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

SOURCES = {
    "raw": BASE / "raw.png",
    "detected": BASE / "detected_components_and_logical_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_left_sources": (300, 250, 2400, 1050),
    "upper_buses_left": (750, 650, 3900, 1650),
    "upper_buses_right": (3600, 650, 7350, 1650),
    "upper_loads_left": (700, 1150, 2850, 2350),
    "upper_loads_mid": (2550, 1150, 5300, 2350),
    "upper_loads_right": (5000, 1150, 7350, 2350),
    "left_vertical_source_to_lc": (650, 2350, 1250, 3900),
    "dc_ups_top": (4300, 2050, 7350, 3150),
    "dc_ups_bottom": (4300, 2850, 7350, 3850),
    "lower_bus_tie": (3700, 3500, 4650, 3950),
    "lower_loads_left": (950, 3800, 3700, 5250),
    "lower_loads_right": (4200, 3800, 6500, 5250),
    "title_notes": (7350, 250, 8500, 5200),
}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        image = Image.open(source_path)
        for crop_name, box in CROPS.items():
            out_path = RESULTS / f"{source_name}__{crop_name}.png"
            image.crop(box).save(out_path)
            print(out_path)


if __name__ == "__main__":
    main()
