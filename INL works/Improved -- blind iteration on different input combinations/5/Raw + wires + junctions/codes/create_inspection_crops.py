from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\5\Raw + wires + junctions")
RESULTS = BASE / "results"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_final_cleaned_v4.png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
    "nodes_overlay": BASE / "wire_nodes_overlay.png",
}

CROPS = {
    "top_left_offsite": (180, 60, 1200, 560),
    "top_center_generator_aux": (2350, 60, 3700, 700),
    "top_right_offsite": (4300, 60, 5450, 560),
    "aux_bus_tie": (2200, 620, 3500, 1080),
    "train_a": (80, 820, 1420, 2620),
    "train_b": (1320, 820, 2670, 2620),
    "train_c": (2570, 820, 3920, 2620),
    "train_d": (3820, 820, 5170, 2620),
    "dc_ups_a": (1000, 2550, 2550, 3700),
    "dc_ups_b": (3500, 2550, 5050, 3700),
    "bottom_power_control": (420, 3150, 4550, 3820),
    "protection_control": (4950, 720, 6340, 2680),
    "legend_notes": (5150, 160, 6280, 800),
}


def main() -> None:
    crop_dir = RESULTS / "inspection_crops"
    crop_dir.mkdir(parents=True, exist_ok=True)

    for source_name, source_path in SOURCES.items():
        image = Image.open(source_path)
        for crop_name, box in CROPS.items():
            image.crop(box).save(crop_dir / f"{source_name}__{crop_name}.png")

    print(f"Wrote {len(SOURCES) * len(CROPS)} crops to {crop_dir}")


if __name__ == "__main__":
    main()
