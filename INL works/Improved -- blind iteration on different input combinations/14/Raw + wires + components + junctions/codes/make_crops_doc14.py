from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\14\Raw + wires + components + junctions"
)
CROPS = BASE / "codes" / "crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png",
    "detected": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROP_BOXES = {
    "train_a_4160": (480, 210, 2850, 1600),
    "train_b_4160": (2950, 210, 5350, 1600),
    "train_a_480_mcc": (480, 1500, 2850, 2950),
    "train_b_480_mcc": (2950, 1500, 5350, 2950),
    "train_a_dc_ups": (500, 2750, 2850, 4050),
    "train_b_dc_ups": (2950, 2750, 5350, 4050),
    "center_ties": (2650, 450, 3300, 3850),
    "a_mcc_left_close": (1120, 1700, 1900, 2700),
    "a_mcc_right_close": (1950, 1700, 2700, 2700),
    "b_mcc_left_close": (3650, 1700, 4400, 2700),
    "b_mcc_right_close": (4400, 1700, 5200, 2700),
    "a_4160_loads_close": (1760, 650, 2650, 1550),
    "b_4160_loads_close": (3950, 650, 5000, 1550),
    "notes_legend": (5350, 270, 6300, 1380),
    "title_block": (5350, 3100, 6300, 3950),
    "terminal_blocks": (480, 3730, 2860, 4140),
    "a_panel_harness_close": (520, 2450, 2920, 3350),
    "b_panel_harness_close": (3000, 2450, 5350, 3350),
    "center_panel_control_close": (2600, 2200, 3400, 3550),
    "left_half": (350, 180, 2920, 4000),
    "right_half": (2860, 180, 5420, 4000),
}


def main():
    CROPS.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        image = Image.open(source_path)
        for crop_name, box in CROP_BOXES.items():
            output = CROPS / f"{source_name}__{crop_name}.png"
            image.crop(box).save(output)
            print(output)


if __name__ == "__main__":
    main()
