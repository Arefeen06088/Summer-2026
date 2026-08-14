from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\6\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png",
    "detected": BASE / "detected_components_and_logical_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_left_generator_switchyard": (180, 180, 4700, 850),
    "top_mid_switchyard": (2700, 180, 7000, 950),
    "legend": (5200, 190, 6900, 590),
    "medium_voltage_left": (170, 760, 3800, 1700),
    "medium_voltage_right": (3300, 760, 6900, 1700),
    "load_centers_left": (250, 1560, 2500, 3000),
    "load_centers_mid": (2450, 1560, 4750, 3000),
    "load_centers_right": (4300, 1560, 6200, 3000),
    "dc_ups_left": (1850, 2870, 3450, 3850),
    "dc_ups_right": (3800, 2870, 5550, 3850),
    "grounds_bottom": (2000, 3600, 4800, 4050),
    "control_bay_full": (6600, 590, 8800, 2920),
    "control_bay_with_inputs": (5200, 520, 8850, 3150),
    "control_bay_top": (6750, 560, 8650, 1500),
    "control_bay_mid": (6750, 1200, 8650, 2500),
    "notes": (220, 3000, 1800, 3650),
    "title_block": (6750, 3800, 8750, 4250),
}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as img:
            for crop_name, box in CROPS.items():
                img.crop(box).save(RESULTS / f"{source_name}__{crop_name}.png")
    print(f"Wrote crops to {RESULTS}")


if __name__ == "__main__":
    main()
