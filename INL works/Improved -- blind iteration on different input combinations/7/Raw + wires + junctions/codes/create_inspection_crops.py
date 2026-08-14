from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw + wires + junctions")
RESULTS = BASE / "results"
CROPS = RESULTS / "inspection_crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_clean (1).png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
    "nodes_overlay": BASE / "wire_nodes_overlay.png",
}

REGIONS = {
    "top_sources_full": (250, 230, 5700, 1650),
    "top_left_offsite_gen": (380, 240, 1850, 1580),
    "top_mid_bus_tie": (1650, 520, 3600, 1600),
    "top_right_standby": (3500, 420, 5600, 1600),
    "train_ab_load_centers": (350, 1500, 2850, 3050),
    "train_a_loads": (420, 1750, 1500, 3030),
    "train_b_loads": (1550, 1750, 2680, 3030),
    "train_cd_load_centers": (3100, 1500, 5650, 3050),
    "train_c_loads": (3180, 1750, 4280, 3030),
    "train_d_loads": (4300, 1750, 5600, 3030),
    "dc_control_a": (360, 3000, 2850, 4380),
    "dc_control_a_detail": (1000, 3450, 2300, 4350),
    "dc_control_b": (3150, 3000, 5650, 4380),
    "dc_control_b_detail": (3820, 3450, 5300, 4350),
    "control_relay_crosslinks": (1650, 2750, 5400, 4480),
    "notes": (5800, 370, 6950, 1050),
    "legend": (5800, 1080, 6950, 1580),
    "revision_status": (5800, 1660, 6950, 2120),
    "title_block": (5720, 3760, 7000, 4580),
}


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as img:
            for region_name, box in REGIONS.items():
                crop = img.crop(box)
                output = CROPS / f"{source_name}__{region_name}.png"
                crop.save(output)
                print(output)


if __name__ == "__main__":
    main()
