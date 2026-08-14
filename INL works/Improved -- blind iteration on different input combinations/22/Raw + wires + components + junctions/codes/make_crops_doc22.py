from pathlib import Path
from PIL import Image


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires + components + junctions")
OUT = ROOT / "codes" / "crops"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_clean.png",
    "components": ROOT / "detected_components_overlay.png",
    "wire_nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
}

CROPS = {
    "full_working_area": (360, 230, 6500, 4850),
    "top_source_and_aux_buses": (420, 230, 5900, 1320),
    "top_source_left_detail": (420, 250, 1800, 850),
    "aux_bus_a_b_detail": (950, 420, 3300, 1200),
    "aux_bus_c_d_detail": (3300, 420, 6100, 1200),
    "train_a_full": (420, 1180, 1900, 3450),
    "train_b_full": (1850, 1180, 3350, 3450),
    "train_c_full": (3300, 1180, 4850, 3450),
    "train_d_full": (4750, 1180, 6250, 3450),
    "train_a_loads_detail": (520, 1850, 1780, 2850),
    "train_b_loads_detail": (1950, 1850, 3220, 2850),
    "train_c_loads_detail": (3400, 1850, 4700, 2850),
    "train_d_loads_detail": (4860, 1850, 6120, 2850),
    "train_a_lower_controls": (500, 2750, 1800, 3350),
    "train_b_lower_controls": (1920, 2750, 3230, 3350),
    "train_c_lower_controls": (3370, 2750, 4700, 3350),
    "train_d_lower_controls": (4820, 2750, 6150, 3350),
    "dc_ups_full": (420, 3440, 5900, 4840),
    "dc_ups_left": (420, 3440, 2950, 4840),
    "dc_ups_right": (2950, 3440, 5900, 4840),
    "dc_bus_a_ups_a": (520, 3600, 2700, 4550),
    "dc_bus_b_ups_b": (3000, 3600, 5000, 4550),
    "control_power_center": (2100, 3850, 5400, 4850),
    "notes_legend": (6100, 350, 7000, 2500),
    "title_block": (6100, 3700, 7000, 4850),
}


def main() -> None:
    for prefix, src in SOURCES.items():
        with Image.open(src) as image:
            for name, box in CROPS.items():
                crop = image.crop(box)
                crop.save(OUT / f"{prefix}__{name}.png")
                crop.resize((crop.width * 2, crop.height * 2)).save(OUT / f"{prefix}__{name}_2x.png")
    print(f"Wrote crops to {OUT}")


if __name__ == "__main__":
    main()
