from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\11\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_relocated_names.png",
    "detected": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_sources_and_bus_tie": (520, 120, 5750, 720),
    "train_a_full": (420, 620, 1820, 3200),
    "train_b_full": (1780, 620, 3150, 3200),
    "train_c_full": (3150, 620, 4520, 3200),
    "train_d_full": (4520, 620, 5860, 3200),
    "train_a_loads": (520, 1750, 1800, 3150),
    "train_b_loads": (1850, 1750, 3120, 3150),
    "train_c_loads": (3220, 1750, 4490, 3150),
    "train_d_loads": (4600, 1750, 5840, 3150),
    "bottom_dc_control": (650, 3000, 5600, 4300),
    "bottom_dc_a_rps": (650, 3450, 2850, 4300),
    "bottom_ssps_ats": (2100, 2850, 4100, 3900),
    "ats_480_a_detail": (1850, 2550, 3000, 3900),
    "ats_480_b_detail": (4300, 2550, 5450, 3900),
    "panel_ic_a_to_dc_bus": (1250, 2650, 2300, 4300),
    "panel_ic_b_to_dc_bus": (2450, 2650, 3500, 4300),
    "panel_ic_c_to_dc_bus": (3650, 2650, 4700, 4300),
    "panel_ic_d_to_dc_bus": (4850, 2650, 5900, 4300),
    "bottom_dc_b_rps": (3400, 3450, 5600, 4300),
    "legend_notes": (5900, 300, 7050, 3000),
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
