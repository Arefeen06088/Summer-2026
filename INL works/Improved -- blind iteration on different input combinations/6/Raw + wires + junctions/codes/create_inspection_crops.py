from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\6\Raw + wires + junctions")
RESULTS = BASE / "results"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
    "nodes_overlay": BASE / "wire_nodes_overlay.png",
}

CROPS = {
    "generator_switchyard": (160, 150, 4700, 900),
    "top_left_source": (180, 350, 1650, 900),
    "top_center_safety_source": (1600, 250, 4850, 1150),
    "top_right_source": (4200, 260, 6500, 1150),
    "mv_safety_buses": (200, 950, 6000, 1750),
    "mv_left_detail": (220, 850, 2750, 1800),
    "mv_right_detail": (3300, 850, 6100, 1800),
    "load_center_a": (350, 1600, 2550, 3050),
    "load_center_b": (3600, 1600, 5850, 3050),
    "load_center_mid_lp": (2500, 1550, 3800, 2750),
    "dc_ups_a": (1900, 2900, 3300, 3850),
    "dc_ups_b": (3700, 2900, 5200, 3850),
    "grounding_bottom": (1900, 3500, 4700, 4150),
    "esfas_rps_bay": (6400, 570, 8850, 2450),
    "esfas_left_terminals": (6200, 600, 7350, 1700),
    "esfas_right_relays": (7300, 650, 8750, 2250),
    "legend": (5250, 210, 6900, 560),
    "notes": (160, 3180, 1800, 3700),
    "title_block": (6850, 3850, 8900, 4250),
}


def main() -> None:
    crop_dir = RESULTS / "inspection_crops"
    crop_dir.mkdir(parents=True, exist_ok=True)

    for source_name, source_path in SOURCES.items():
        image = Image.open(source_path)
        thumb = image.copy()
        thumb.thumbnail((2400, 1600))
        if source_name == "raw":
            thumb.save(crop_dir / "raw_overview_2400.png")
        elif source_name == "wires_overlay":
            thumb.save(crop_dir / "wires_overview_2400.png")
        elif source_name == "nodes_overlay":
            thumb.save(crop_dir / "nodes_overview_2400.png")
        for crop_name, box in CROPS.items():
            image.crop(box).save(crop_dir / f"{source_name}__{crop_name}.png")

    print(f"Wrote {len(SOURCES) * len(CROPS)} crops plus overviews to {crop_dir}")


if __name__ == "__main__":
    main()
