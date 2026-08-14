from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\18\Raw + wires + components + junctions"
)
OUT = BASE / "codes" / "crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_nuclear_electrical_schematic_readable.png",
    "components": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
}

# Coordinates are in original 7000 x 4400 image pixels.
CROPS = {
    "full_working_area": (220, 210, 5650, 3650),
    "top_left_power_sources": (250, 250, 1750, 1120),
    "top_center_bus_links": (1600, 250, 3850, 1120),
    "top_right_power_sources": (3650, 250, 5550, 1120),
    "top_right_generator_detail": (4200, 250, 5200, 1050),
    "source_to_4160a_detail": (350, 250, 2000, 1450),
    "source_to_4160b_detail": (3600, 250, 5600, 1450),
    "dg_b_far_right_detail": (5000, 700, 6100, 1900),
    "middle_panel_450a": (280, 1120, 1600, 2300),
    "middle_panel_400b": (1600, 1120, 3000, 2300),
    "middle_panel_400c": (3000, 1120, 4380, 2300),
    "middle_panel_400d": (4380, 1120, 5650, 2300),
    "bottom_train_a": (280, 2550, 2960, 3650),
    "bottom_train_b": (3020, 2550, 5650, 3650),
    "relay_block_train_a": (1800, 2850, 2920, 3520),
    "relay_block_train_b": (4380, 2850, 5550, 3520),
    "relay_block_train_a_detail": (2080, 2820, 2700, 3240),
    "relay_block_train_b_detail": (4670, 2820, 5320, 3240),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source_name, path in SOURCES.items():
        image = Image.open(path)
        for crop_name, box in CROPS.items():
            crop = image.crop(box)
            crop.save(OUT / f"{source_name}__{crop_name}.png")
            if crop_name.endswith("_detail"):
                crop.resize((crop.size[0] * 2, crop.size[1] * 2)).save(
                    OUT / f"{source_name}__{crop_name}_2x.png"
                )
    print(f"Wrote crops to {OUT}")


if __name__ == "__main__":
    main()
