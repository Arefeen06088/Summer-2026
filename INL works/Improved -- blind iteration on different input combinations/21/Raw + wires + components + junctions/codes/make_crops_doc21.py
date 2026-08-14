from pathlib import Path
from PIL import Image


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\21\Raw + wires + components + junctions")
OUT = ROOT / "codes" / "crops"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_fixed.png",
    "components": ROOT / "detected_components_overlay.png",
    "wire_nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
}

CROPS = {
    "full_working_area": (250, 250, 6400, 4550),
    "top_left_incoming_sources": (300, 400, 2050, 1400),
    "top_switchgear_full": (2000, 380, 5750, 1400),
    "top_switchgear_left": (2000, 420, 3900, 1360),
    "top_switchgear_right": (3700, 420, 5750, 1360),
    "edg_branches_201b_202a_detail": (3650, 790, 5150, 1250),
    "edg_branches_202a_202b_detail": (3650, 1080, 5200, 1500),
    "train_a_480_overview": (280, 1350, 3000, 2950),
    "train_b_480_overview": (2950, 1350, 5750, 2950),
    "train_a_loads_detail": (380, 1780, 3000, 2780),
    "train_b_loads_detail": (3300, 1780, 5750, 2780),
    "train_a_bus_ties_transformers": (1250, 1250, 3000, 2050),
    "train_b_bus_ties_transformers": (3000, 1250, 4100, 2100),
    "dc_ups_left": (300, 2750, 3050, 4350),
    "dc_ups_middle": (1450, 2700, 3700, 4450),
    "dc_ups_lower": (300, 3600, 3600, 4500),
    "control_logic_full": (2920, 2800, 5750, 4450),
    "control_logic_bus_inputs": (2920, 2850, 3500, 4300),
    "control_logic_rows_left": (3370, 2850, 4550, 4300),
    "control_logic_rows_right": (4450, 2850, 5700, 4300),
    "notes_legend": (5850, 420, 6800, 2850),
    "title_block": (5850, 3550, 7050, 4550),
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
