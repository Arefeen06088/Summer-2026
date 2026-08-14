from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\8\Raw + wires + junctions")
RESULTS = BASE / "results"
CROPS = RESULTS / "inspection_crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_schematic_improved_local_refined_v3.png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
    "nodes_overlay": BASE / "wire_nodes_overlay.png",
}

REGIONS = {
    "top_normal_sources_full": (140, 150, 3270, 710),
    "top_left_normal_source": (150, 150, 1420, 710),
    "top_center_generator_tie": (1300, 150, 2350, 710),
    "top_right_normal_source": (2200, 150, 3290, 710),
    "safety_4kv_full": (140, 650, 3330, 1120),
    "safety_4kv_left": (150, 650, 1450, 1120),
    "safety_4kv_center": (1350, 650, 2300, 1120),
    "safety_4kv_right": (2250, 650, 3330, 1120),
    "480_distribution_full": (140, 1080, 3330, 1500),
    "load_feeders_a": (140, 1320, 1510, 2300),
    "load_feeders_b": (1990, 1320, 3330, 2300),
    "dc_ups_control_a": (1320, 1250, 1990, 2300),
    "dc_ups_control_b": (2820, 1250, 3380, 2300),
    "bottom_control_crosslinks": (800, 1850, 3380, 2320),
    "left_lower_detail": (140, 1150, 2050, 2340),
    "right_lower_detail": (2000, 1150, 3380, 2340),
    "notes": (3380, 170, 4070, 850),
    "revision_record": (3380, 850, 4070, 1125),
    "legend": (3380, 1120, 4070, 1580),
    "cable_refs": (3380, 1580, 4070, 2090),
    "title_block": (3380, 2090, 4070, 2860),
}


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        with Image.open(source_path) as img:
            for region_name, box in REGIONS.items():
                output = CROPS / f"{source_name}__{region_name}.png"
                img.crop(box).save(output)
                print(output)


if __name__ == "__main__":
    main()
