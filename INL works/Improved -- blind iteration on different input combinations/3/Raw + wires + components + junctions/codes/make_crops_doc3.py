from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\3\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_100_component_electrical_schematic.png",
    "detected": BASE / "detected_components_and_logical_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_sources_and_buses": (200, 220, 5000, 900),
    "train_a_4160_mcc": (250, 350, 2450, 1800),
    "train_b_4160_mcc": (3000, 350, 5000, 1800),
    "dc_ups_center": (2200, 650, 3400, 1850),
    "charger_feed_detail": (2000, 450, 3500, 1350),
    "mcc_feeders_a_left": (250, 1850, 1600, 2750),
    "mcc_feeders_a_right": (1450, 1850, 2850, 2750),
    "mcc_feeders_b_left": (2700, 1850, 4100, 2750),
    "mcc_feeders_b_right": (3900, 1850, 5050, 2750),
    "lower_rps_a": (1200, 2800, 2400, 3750),
    "lower_rps_b": (3100, 2800, 4350, 3750),
    "bus_tie_detail": (2350, 430, 2900, 760),
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
